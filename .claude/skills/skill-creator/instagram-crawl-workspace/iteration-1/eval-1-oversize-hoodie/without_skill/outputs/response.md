# 인스타그램 이미지 수집 — #오버사이즈후드 #후드티코디

## 요청 해석

- 수집 대상: 인스타그램 해시태그 페이지
- 해시태그: `#오버사이즈후드`, `#후드티코디`
- 필터 조건: 릴스(동영상) 제외, 이미지(정지 사진) 만 수집

---

## 수집 방법 — 단계별 계획

### 1단계: 도구 선택

인스타그램은 공식 API가 일반 크롤링에 제한적이므로, 실무에서 주로 사용하는 방법은 아래 두 가지입니다.

| 방법 | 도구 | 특징 |
|------|------|------|
| A. Instaloader (Python 오픈소스) | `instaloader` | 해시태그별 게시물 수집, 이미지/동영상 분리 가능 |
| B. 브라우저 자동화 | `playwright` + 수동 스크래핑 | 로그인 세션 활용, 더 유연하나 복잡 |

**추천: Instaloader** — 해시태그 수집에 최적화, 미디어 타입 필터링 지원.

---

### 2단계: 실행 커맨드 (Instaloader)

```bash
# 설치
pip install instaloader

# #오버사이즈후드 해시태그에서 이미지만 수집 (동영상 제외)
instaloader "#오버사이즈후드" \
  --no-videos \
  --no-video-thumbnails \
  --dirname-pattern="output/instagram/{hashtag}" \
  --filename-pattern="{date_utc}_UTC_{shortcode}" \
  --count=100

# #후드티코디 해시태그에서 이미지만 수집
instaloader "#후드티코디" \
  --no-videos \
  --no-video-thumbnails \
  --dirname-pattern="output/instagram/{hashtag}" \
  --filename-pattern="{date_utc}_UTC_{shortcode}" \
  --count=100
```

**주요 옵션 설명:**
- `--no-videos`: 동영상(릴스 포함) 다운로드 제외
- `--no-video-thumbnails`: 동영상 썸네일도 제외 (릴스 커버 이미지 배제)
- `--count=100`: 각 해시태그당 최대 100개 게시물 수집
- `--dirname-pattern`: 해시태그별 폴더 자동 분리

---

### 3단계: 저장 구조

```
output/instagram/
├── #오버사이즈후드/
│   ├── 2026-03-20_UTC_ABC123.jpg
│   ├── 2026-03-20_UTC_ABC123.txt   ← 캡션/메타데이터
│   ├── 2026-03-19_UTC_DEF456.jpg
│   └── ...
└── #후드티코디/
    ├── 2026-03-21_UTC_GHI789.jpg
    ├── 2026-03-21_UTC_GHI789.txt
    └── ...
```

---

### 4단계: 추가 필터링 (Python 스크립트)

Instaloader의 `--no-videos`만으로도 릴스가 대부분 제외되지만, 캐러셀 중 동영상 슬라이드가 섞인 경우를 대비해 추가 필터링을 적용합니다.

```python
import os
from pathlib import Path

def filter_images_only(folder: str):
    """jpg/png 이미지 파일만 남기고 나머지 삭제"""
    allowed_ext = {'.jpg', '.jpeg', '.png', '.webp'}
    folder_path = Path(folder)

    removed = 0
    for f in folder_path.rglob('*'):
        if f.is_file() and f.suffix.lower() not in allowed_ext and f.suffix != '.txt':
            print(f"제거: {f.name}")
            f.unlink()
            removed += 1

    print(f"정리 완료: {removed}개 비이미지 파일 제거")

filter_images_only("output/instagram")
```

---

### 5단계: 수집 결과 활용

수집된 이미지는 아래 목적으로 활용 가능합니다.

- **트렌드 분석**: 오버사이즈 후드 스타일링 패턴 파악 (색상, 레이어링, 하의 조합)
- **무드보드 소재**: `moodboard` 스킬 실행 시 레퍼런스 이미지로 활용
- **경쟁사 모니터링**: 동일 해시태그 사용 브랜드 파악

---

## 제약 사항 및 주의점

1. **인스타그램 이용약관**: 자동 수집은 Instagram ToS에 위배될 수 있습니다. 수집된 이미지는 내부 트렌드 리서치 목적으로만 사용하고, 외부 배포 금지.
2. **레이트 리밋**: 한 번에 너무 많이 수집하면 계정이 임시 차단될 수 있으므로, `--count=100` 수준으로 제한 권장.
3. **로그인 필요**: 해시태그 수집 시 로그인 세션이 있어야 더 많은 게시물에 접근 가능.
   ```bash
   instaloader --login=your_instagram_id "#오버사이즈후드" --no-videos
   ```
4. **메모리 제외 브랜드**: 리코리아, 커버낫 계정 게시물이 포함된 경우 수동으로 제거할 것 (feedback_image_exclusions.md 참조).

---

## 실행하려면

위 커맨드를 실제로 실행하려면:
1. Python 환경에서 `pip install instaloader` 실행
2. 인스타그램 계정 로그인 정보 준비
3. 위 커맨드 실행

또는 `/brief trend-research` 스킬을 통해 트렌드 분석 맥락 안에서 이미지 수집을 체계적으로 진행할 수 있습니다.
