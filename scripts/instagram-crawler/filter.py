#!/usr/bin/env python3
"""
Instagram 이미지 AI 브랜드 적합도 필터
- Claude Vision API로 이미지별 와키윌리 브랜드 적합도 점수 산출
- threshold 미만 이미지는 _filtered/ 폴더로 이동
- 결과: _filter_report.json 생성
"""

import argparse
import base64
import json
import os
import shutil
import sys
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("[ERROR] anthropic SDK가 설치되어 있지 않습니다.")
    print("        pip install anthropic  으로 설치 후 재실행하세요.")
    sys.exit(1)


# ── 설정 ──────────────────────────────────────────────────────────────────────

DEFAULT_THRESHOLD = 7  # 10점 만점 기준 기본 통과 점수
BRAND_PROMPT = """당신은 와키윌리(Wacky Willy) 패션 브랜드의 크리에이티브 디렉터입니다.

브랜드 DNA:
- 컨셉: Kitsch Street & IP Universe
- 코어 타겟: 18~25세 자유로운 트렌드리더
- 스타일: 비비드 컬러, 오버사이즈, 캐릭터 그래픽, 스트릿 감성
- 선호: 컬러블록, 레이어드 스타일링, 팝아트, 믹스매치
- 기피: 무채색 단독, 타이트 미니멀, 하이패션 과잉

아래 이미지의 브랜드 적합도를 1~10점으로 평가하세요.

평가 기준:
- 10점: 와키윌리 캠페인에 바로 쓸 수 있는 레퍼런스
- 7~9점: 방향성 맞음, 활용 가능
- 4~6점: 부분적으로 참고 가능, 수정 필요
- 1~3점: 브랜드 무드와 맞지 않음

응답은 반드시 아래 JSON 형식으로만 답하세요:
{
  "score": <1~10 정수>,
  "reason": "<한 문장 이유>",
  "tags": ["<특징1>", "<특징2>"]
}"""


# ── 채점 ──────────────────────────────────────────────────────────────────────

def score_image(client: anthropic.Anthropic, image_path: Path) -> dict:
    """Claude Vision으로 이미지 브랜드 적합도 채점"""
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    # 이미지 확장자로 미디어 타입 판단
    ext = image_path.suffix.lower()
    media_type = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }.get(ext, "image/jpeg")

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",  # 빠르고 저렴한 모델 사용
            max_tokens=256,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {"type": "text", "text": BRAND_PROMPT}
                    ],
                }
            ],
        )

        result = json.loads(response.content[0].text)
        return {
            "score": int(result.get("score", 0)),
            "reason": result.get("reason", ""),
            "tags": result.get("tags", [])
        }

    except json.JSONDecodeError:
        # JSON 파싱 실패 시 응답 텍스트에서 점수 추출 시도
        text = response.content[0].text if response.content else ""
        import re
        m = re.search(r'"score"\s*:\s*(\d+)', text)
        score = int(m.group(1)) if m else 5
        return {"score": score, "reason": "파싱 오류 — 기본값 적용", "tags": []}
    except Exception as e:
        return {"score": -1, "reason": f"API 오류: {e}", "tags": []}


# ── 메인 필터 ─────────────────────────────────────────────────────────────────

def run_filter(target_dir: Path, threshold: int, dry_run: bool, recursive: bool):
    """디렉토리 내 이미지를 채점하고 threshold 미만을 _filtered/로 이동"""

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("[ERROR] ANTHROPIC_API_KEY 환경변수가 설정되어 있지 않습니다.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # 대상 이미지 수집
    extensions = {".jpg", ".jpeg", ".png", ".webp"}
    if recursive:
        images = [p for p in target_dir.rglob("*")
                  if p.suffix.lower() in extensions and "_filtered" not in str(p)]
    else:
        images = [p for p in target_dir.iterdir()
                  if p.suffix.lower() in extensions]

    if not images:
        print(f"[WARNING] {target_dir} 에 이미지 파일이 없습니다.")
        return

    print(f"\n[INFO] 총 {len(images)}장 채점 시작 (threshold: {threshold}/10)")
    if dry_run:
        print("[INFO] --dry-run 모드: 파일 이동 없이 미리보기만 실행\n")

    results = []
    passed = []
    filtered = []

    for i, img_path in enumerate(images, 1):
        print(f"  [{i:02d}/{len(images):02d}] {img_path.name} 채점 중...", end=" ", flush=True)
        score_result = score_image(client, img_path)
        score = score_result["score"]

        entry = {
            "file": str(img_path.relative_to(target_dir)),
            "score": score,
            "reason": score_result["reason"],
            "tags": score_result["tags"],
            "action": "pass" if score >= threshold else "filtered"
        }
        results.append(entry)

        if score >= threshold:
            passed.append(img_path)
            print(f"✓ {score}/10 — {score_result['reason']}")
        else:
            filtered.append(img_path)
            print(f"✗ {score}/10 — {score_result['reason']}")

        if not dry_run and score < threshold:
            # _filtered/ 폴더로 이동
            filtered_dir = img_path.parent / "_filtered"
            filtered_dir.mkdir(exist_ok=True)
            shutil.move(str(img_path), filtered_dir / img_path.name)

    # 리포트 저장
    report = {
        "filtered_at": __import__("datetime").datetime.now().isoformat(),
        "threshold": threshold,
        "dry_run": dry_run,
        "total": len(images),
        "passed": len(passed),
        "filtered": len(filtered),
        "pass_rate": f"{len(passed)/len(images)*100:.1f}%",
        "results": sorted(results, key=lambda x: x["score"], reverse=True)
    }

    report_path = target_dir / "_filter_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 50)
    print(f"  채점 완료: {len(passed)}장 통과 / {len(filtered)}장 필터링")
    print(f"  통과율: {report['pass_rate']}")
    print(f"  리포트: {report_path}")
    if not dry_run and filtered:
        print(f"  필터링된 이미지: {target_dir}/_filtered/")
    print("=" * 50)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="와키윌리 브랜드 적합도 AI 필터 (Claude Vision)"
    )
    parser.add_argument("directory",
                        help="필터링할 이미지 디렉토리 경로")
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD,
                        help=f"통과 최소 점수 (기본값: {DEFAULT_THRESHOLD}/10)")
    parser.add_argument("--dry-run", action="store_true",
                        help="미리보기 — 실제 파일 이동 없음")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="하위 폴더까지 재귀 처리")

    args = parser.parse_args()
    target = Path(args.directory)

    if not target.exists():
        print(f"[ERROR] 디렉토리가 존재하지 않습니다: {target}")
        sys.exit(1)

    run_filter(target, args.threshold, args.dry_run, args.recursive)


if __name__ == "__main__":
    main()
