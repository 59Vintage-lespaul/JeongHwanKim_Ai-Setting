#!/usr/bin/env python3
"""
Instagram Following-Based Image Crawler (API 직접 호출 방식)
1. 팔로잉 목록 조회 (Instagram API)
2. 각 계정 최근 포스트 캡션 키워드 매칭 (API)
3. 매칭 이미지 직접 다운로드 (requests)

cookies.txt 인증 필요 (Get cookies.txt LOCALLY 익스텐션)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from http.cookiejar import MozillaCookieJar
from pathlib import Path
from urllib.parse import urlparse

import requests

WORKSPACE_ROOT = Path(__file__).resolve().parents[2] / "workspace" / "moodboard"
DEFAULT_COOKIES = Path(__file__).parent / "www.instagram.com_cookies.txt"

# 트러커캡 관련 키워드 (기본 번들)
TRUCKER_CAP_KEYWORDS = [
    "트러커캡", "트러커햇", "트러커", "trucker cap", "truckercap",
    "trucker hat", "trucker_cap", "mesh cap", "meshcap",
    "볼캡", "ball cap", "snapback"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8",
    "X-IG-App-ID": "936619743392459",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.instagram.com/",
}


# ── 인증 ─────────────────────────────────────────────────────────────────────

def load_session(cookies_path: Path) -> requests.Session:
    jar = MozillaCookieJar()
    jar.load(str(cookies_path), ignore_discard=True, ignore_expires=True)
    s = requests.Session()
    s.cookies = jar  # type: ignore
    s.headers.update(HEADERS)
    # CSRF 토큰 주입
    for c in jar:
        if c.name == "csrftoken":
            s.headers["X-CSRFToken"] = c.value
    return s


def get_my_user_id(session: requests.Session) -> str:
    for c in session.cookies:
        if c.name == "ds_user_id" and c.value:
            return c.value
    raise RuntimeError("ds_user_id 쿠키가 없습니다. 쿠키가 만료됐을 수 있습니다.")


# ── 팔로잉 목록 ───────────────────────────────────────────────────────────────

def get_followings(session: requests.Session, user_id: str,
                   max_count: int = 500) -> list[dict]:
    followings = []
    next_max_id = ""
    print(f"[INFO] 팔로잉 목록 조회 중 (최대 {max_count}명)...")

    while len(followings) < max_count:
        params = {"count": 100}
        if next_max_id:
            params["max_id"] = next_max_id

        try:
            r = session.get(
                f"https://www.instagram.com/api/v1/friendships/{user_id}/following/",
                params=params, timeout=15
            )
            if r.status_code != 200:
                print(f"  [WARNING] 팔로잉 조회 실패 (status {r.status_code})")
                break
            data = r.json()
        except Exception as e:
            print(f"  [WARNING] 팔로잉 조회 오류: {e}")
            break

        users = data.get("users", [])
        if not users:
            break

        for u in users:
            followings.append({
                "username": u.get("username", ""),
                "pk": str(u.get("pk", "")),
                "full_name": u.get("full_name", ""),
            })

        next_max_id = data.get("next_max_id", "")
        if not next_max_id:
            break
        time.sleep(0.5)

    print(f"  완료: {len(followings)}명")
    return followings


# ── 계정 최근 포스트 조회 ─────────────────────────────────────────────────────

def get_user_posts(session: requests.Session, user_id: str,
                   count: int = 20) -> list[dict]:
    """계정의 최근 포스트 리스트 반환"""
    posts = []
    try:
        r = session.get(
            f"https://www.instagram.com/api/v1/feed/user/{user_id}/",
            params={"count": count},
            timeout=15
        )
        if r.status_code != 200:
            return []
        data = r.json()
        items = data.get("items", [])
        for item in items:
            caption_text = ""
            if item.get("caption"):
                caption_text = item["caption"].get("text", "")

            # 이미지 URL 추출 (캐러셀 포함)
            image_urls = []
            if item.get("carousel_media"):
                for m in item["carousel_media"]:
                    candidates = m.get("image_versions2", {}).get("candidates", [])
                    if candidates:
                        image_urls.append(candidates[0]["url"])
            else:
                candidates = item.get("image_versions2", {}).get("candidates", [])
                if candidates:
                    image_urls.append(candidates[0]["url"])

            # 동영상 포스트 제외
            if item.get("media_type") == 2:  # 2 = video
                continue

            taken_at = item.get("taken_at", 0)

            posts.append({
                "pk": str(item.get("pk", "")),
                "shortcode": item.get("code", ""),
                "caption": caption_text,
                "taken_at": taken_at,
                "image_urls": image_urls,
            })
    except Exception as e:
        pass
    return posts


# ── 키워드 매칭 ───────────────────────────────────────────────────────────────

def caption_matches(caption: str, keywords: list[str]) -> bool:
    caption_lower = caption.lower()
    return any(kw.lower() in caption_lower for kw in keywords)


# ── 이미지 다운로드 ───────────────────────────────────────────────────────────

def download_image(session: requests.Session, url: str, out_path: Path) -> bool:
    try:
        r = session.get(url, timeout=20, stream=True)
        if r.status_code == 200:
            with open(out_path, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            # 최소 크기 검사 (10KB)
            if out_path.stat().st_size < 10 * 1024:
                out_path.unlink()
                return False
            return True
    except Exception:
        pass
    return False


# ── 메인 ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="팔로잉 계정에서 키워드 매칭 이미지 수집 (API 방식)"
    )
    parser.add_argument("--keyword", required=True, help="검색 키워드 (예: 트러커캡)")
    parser.add_argument("--count", type=int, default=20, help="목표 수집 장수 (기본: 20)")
    parser.add_argument("--since", type=int, default=None, help="최근 N개월 이내만 수집")
    parser.add_argument("--posts-per-account", type=int, default=30,
                        help="계정당 스캔할 최근 포스트 수 (기본: 30)")
    parser.add_argument("--max-followings", type=int, default=500,
                        help="조회할 팔로잉 수 상한 (기본: 500)")
    parser.add_argument("--extra-keywords", nargs="*", default=[],
                        help="추가 검색 키워드 (공백 구분)")
    parser.add_argument("--cookies", default=str(DEFAULT_COOKIES))
    parser.add_argument("--date", default=None)
    args = parser.parse_args()

    date_str = args.date or datetime.now().strftime("%Y%m%d")
    cookies = Path(args.cookies)

    if not cookies.exists():
        print(f"[ERROR] 쿠키 파일 없음: {cookies}")
        sys.exit(1)

    # 키워드 목록
    base_keywords = TRUCKER_CAP_KEYWORDS if args.keyword.lower() in \
        [k.lower() for k in TRUCKER_CAP_KEYWORDS] else [args.keyword]
    keywords = list(dict.fromkeys(base_keywords + args.extra_keywords))

    # 날짜 필터
    since_ts = None
    if args.since:
        since_ts = (datetime.now(timezone.utc) - timedelta(days=args.since * 30)).timestamp()

    out_dir = WORKSPACE_ROOT / f"instagram_{date_str}" / args.keyword
    out_dir.mkdir(parents=True, exist_ok=True)
    session_dir = WORKSPACE_ROOT / f"instagram_{date_str}"

    print("=" * 60)
    print(f"  Instagram Following Crawler (API)")
    print(f"  키워드: {args.keyword} ({len(keywords)}개 동의어)")
    print(f"  목표: {args.count}장 | 기간: {f'최근 {args.since}개월' if args.since else '제한 없음'}")
    print("=" * 60)

    session = load_session(cookies)
    user_id = get_my_user_id(session)
    print(f"[INFO] 로그인 확인 (user_id: {user_id})")

    followings = get_followings(session, user_id, max_count=args.max_followings)
    if not followings:
        print("[ERROR] 팔로잉 목록 없음")
        sys.exit(1)

    total_downloaded = 0
    matched_accounts = []
    img_counter = 1

    print(f"\n[INFO] {len(followings)}개 계정 스캔 시작 (계정당 최근 {args.posts_per_account}개 포스트)...")

    for i, user in enumerate(followings, 1):
        if total_downloaded >= args.count:
            break

        username = user["username"]
        pk = user["pk"]
        print(f"  [{i:03d}/{len(followings)}] @{username} ...", end=" ", flush=True)

        # 최근 포스트 조회
        posts = get_user_posts(session, pk, count=args.posts_per_account)
        if not posts:
            print("(포스트 없음)")
            time.sleep(1)
            continue

        # 날짜 필터 + 키워드 매칭
        matched = []
        for post in posts:
            if since_ts and post["taken_at"] < since_ts:
                continue
            if caption_matches(post["caption"], keywords):
                matched.extend(post["image_urls"])

        if not matched:
            print("매칭 없음")
            time.sleep(1)
            continue

        # 매칭 이미지 다운로드
        downloaded_this = 0
        for url in matched:
            if total_downloaded >= args.count:
                break
            ext = "jpg"
            fname = f"img_{img_counter:03d}_{username}.{ext}"
            out_path = out_dir / fname
            ok = download_image(session, url, out_path)
            if ok:
                total_downloaded += 1
                img_counter += 1
                downloaded_this += 1

        print(f"✓ {downloaded_this}장 (캡션 매칭 {len(matched)}개)")
        if downloaded_this > 0:
            matched_accounts.append({"username": username, "count": downloaded_this})

        time.sleep(1.5)

    # 메타데이터 저장
    meta = {
        "collected_at": datetime.now().isoformat(),
        "mode": "following",
        "keyword": args.keyword,
        "keywords_used": keywords,
        "since_months": args.since,
        "followings_scanned": min(i, len(followings)),
        "matched_accounts": matched_accounts,
        "total_collected": total_downloaded,
    }
    with open(session_dir / "_metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"  완료: {total_downloaded}장 수집")
    print(f"  매칭 계정: {len(matched_accounts)}개 — {[m['username'] for m in matched_accounts]}")
    print(f"  저장 경로: {out_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
