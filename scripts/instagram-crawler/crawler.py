#!/usr/bin/env python3
"""
Instagram Hashtag Image Crawler (gallery-dl 기반)
- 쿠키 파일로 인증 (Chrome 익스텐션 Get cookies.txt LOCALLY 로 내보내기)
- 이미지 포스트만 수집 (동영상 자동 제외)
- 날짜 필터: --since N개월
- 저장 경로: workspace/moodboard/instagram_YYYYMMDD/{hashtag}/
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

WORKSPACE_ROOT = Path(__file__).resolve().parents[2] / "workspace" / "moodboard"
DEFAULT_COOKIES = Path(__file__).parent / "www.instagram.com_cookies.txt"


def sanitize_folder_name(name: str) -> str:
    name = name.lstrip("#")
    for ch in r'\/:*?"<>|':
        name = name.replace(ch, "")
    return name.strip() or "unknown"


def setup_output_dir(hashtag: str, date_str: str) -> tuple[Path, Path]:
    folder_name = sanitize_folder_name(hashtag)
    session_dir = WORKSPACE_ROOT / f"instagram_{date_str}"
    tag_dir = session_dir / folder_name
    tag_dir.mkdir(parents=True, exist_ok=True)
    return tag_dir, session_dir


def load_metadata(session_dir: Path) -> dict:
    meta_path = session_dir / "_metadata.json"
    if meta_path.exists():
        with open(meta_path, encoding="utf-8") as f:
            return json.load(f)
    return {
        "collected_at": datetime.now().isoformat(),
        "tags": [],
        "quality_filter": {"videos_excluded": True}
    }


def save_metadata(session_dir: Path, meta: dict):
    meta_path = session_dir / "_metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def crawl_hashtag(hashtag: str, count: int, date_str: str,
                  cookies: Path, since_months: int | None = None) -> dict:
    tag_dir, session_dir = setup_output_dir(hashtag, date_str)
    folder_name = sanitize_folder_name(hashtag)
    tag_clean = hashtag.lstrip("#")
    url = f"https://www.instagram.com/explore/tags/{quote(tag_clean)}/"

    since_label = f"최근 {since_months}개월" if since_months else "제한 없음"
    print(f"\n[INFO] #{tag_clean} 수집 시작")
    print(f"       목표: {count}장 | 기간: {since_label}")
    print(f"       저장: {tag_dir}")

    cmd = [
        "gallery-dl",
        "--cookies", str(cookies),
        "-D", str(tag_dir),
        "-o", f"image-range=1-{count}",
        "--no-skip",
    ]

    # 날짜 필터
    if since_months:
        since_date = (datetime.now(timezone.utc) - timedelta(days=since_months * 30)).strftime("%Y-%m-%dT%H:%M:%S")
        cmd += ["-o", f"image-filter=date > datetime.datetime.fromisoformat('{since_date}')"]

    cmd.append(url)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        output_lines = [l for l in result.stdout.splitlines() if l.strip() and not l.startswith("#")]
        collected = len(output_lines)

        if result.returncode != 0 and collected == 0:
            print(f"[ERROR] 수집 실패: {result.stderr.strip()[:200]}")
            return {"tag": tag_clean, "collected": 0, "filtered_out": 0, "filter_reasons": [], "folder": folder_name}

        print(f"  → {collected}장 수집 완료")
        for line in output_lines:
            fname = Path(line.strip()).name if line.strip() else ""
            if fname:
                print(f"  ✓ {fname}")

        return {
            "tag": tag_clean,
            "collected": collected,
            "filtered_out": 0,
            "filter_reasons": [],
            "folder": folder_name
        }

    except FileNotFoundError:
        print("[ERROR] gallery-dl이 설치되어 있지 않습니다. pip install gallery-dl")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Instagram 해시태그 이미지 크롤러")
    parser.add_argument("--hashtag", required=True, help="수집할 해시태그 (# 없이)")
    parser.add_argument("--count", type=int, default=20, help="수집 장수 (기본값: 20)")
    parser.add_argument("--no-videos", action="store_true", default=True, help="동영상 제외 (기본값: True)")
    parser.add_argument("--since", type=int, default=None, help="최근 N개월 이내만 수집")
    parser.add_argument("--cookies", default=str(DEFAULT_COOKIES), help="cookies.txt 경로")
    parser.add_argument("--date", default=None, help="날짜 문자열 YYYYMMDD (기본: 오늘)")
    args = parser.parse_args()

    date_str = args.date or datetime.now().strftime("%Y%m%d")
    cookies = Path(args.cookies)

    if not cookies.exists():
        print(f"[ERROR] 쿠키 파일이 없습니다: {cookies}")
        print("        Chrome에서 instagram.com 로그인 후 'Get cookies.txt LOCALLY' 익스텐션으로 내보내기")
        print(f"        저장 경로: {DEFAULT_COOKIES}")
        sys.exit(1)

    print("=" * 60)
    print("  Instagram Hashtag Crawler (gallery-dl)")
    print(f"  태그: #{args.hashtag} | 목표: {args.count}장")
    print(f"  날짜: {date_str} | 기간: {f'최근 {args.since}개월' if args.since else '제한 없음'}")
    print("=" * 60)

    _, session_dir = setup_output_dir(args.hashtag, date_str)
    meta = load_metadata(session_dir)

    result = crawl_hashtag(
        hashtag=args.hashtag,
        count=args.count,
        date_str=date_str,
        cookies=cookies,
        since_months=args.since
    )

    existing = next((t for t in meta["tags"] if t["tag"] == result["tag"]), None)
    if existing:
        existing.update(result)
    else:
        meta["tags"].append(result)

    meta["total_collected"] = sum(t["collected"] for t in meta["tags"])
    meta["collected_at"] = datetime.now().isoformat()
    save_metadata(session_dir, meta)

    print("\n" + "=" * 60)
    print(f"  저장 경로: {session_dir}")
    print(f"  전체 수집: {meta['total_collected']}장")
    print("=" * 60)


if __name__ == "__main__":
    main()
