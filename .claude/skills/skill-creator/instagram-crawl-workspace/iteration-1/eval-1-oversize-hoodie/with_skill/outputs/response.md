# Instagram 이미지 수집 — 시뮬레이션 실행 결과

> 스킬: `instagram-crawl`
> 요청: "인스타 해시태그 #오버사이즈후드 #후드티코디 로 이미지 수집해줘. 릴스는 빼고."
> 실행 날짜: 2026-03-24

---

## Step 1: 해시태그 설계 단계 — 스킵

사용자가 `#오버사이즈후드`, `#후드티코디` 두 개의 해시태그를 **직접 명시**했으므로,
스킬 지침 §1-B "단순 요청의 경우"에 따라 클러스터 설계 단계를 생략하고 바로 확인으로 진행합니다.

---

## Step 2: 확인 메시지 (사용자에게 보여지는 내용)

```
#오버사이즈후드, #후드티코디 이미지 각 20장씩, 총 40장 수집합니다.
릴스·동영상은 제외합니다 (--no-videos).

진행할까요?
```

---

## Step 3: 크롤러 명령어

사용자가 확인하면 아래 명령어를 순차 실행합니다.
태그 간 **10초 쿨다운**을 포함합니다.

```bash
# 태그 1: 오버사이즈후드
python3 scripts/instagram-crawler/crawler.py \
  --hashtag "오버사이즈후드" \
  --count 20 \
  --no-videos

# 10초 쿨다운 (Instagram 차단 방지)
sleep 10

# 태그 2: 후드티코디
python3 scripts/instagram-crawler/crawler.py \
  --hashtag "후드티코디" \
  --count 20 \
  --no-videos
```

**루프 형태 (동등한 방식):**
```bash
for TAG in 오버사이즈후드 후드티코디; do
  python3 scripts/instagram-crawler/crawler.py --hashtag "$TAG" --count 20 --no-videos
  sleep 10
done
```

옵션 설명:
- `--hashtag`: `#` 없이 태그명만 전달
- `--count 20`: 기본값 20장
- `--no-videos`: Reels·동영상 제외 — 사용자 명시 요청("릴스는 빼고")에 따라 강제 적용

---

## Step 4: 폴더 구조 (수집 완료 후 예상 결과)

```
workspace/moodboard/instagram_20260324/
├── 오버사이즈후드/
│   ├── img_001.jpg
│   ├── img_002.jpg
│   ├── img_003.jpg
│   ├── ...
│   └── img_020.jpg         ← 총 20장
├── 후드티코디/
│   ├── img_001.jpg
│   ├── img_002.jpg
│   ├── ...
│   └── img_020.jpg         ← 총 20장
└── _metadata.json
```

`_metadata.json` 내용 예시:
```json
{
  "collected_at": "2026-03-24T00:00:00",
  "tags": [
    { "hashtag": "오버사이즈후드", "count": 20, "folder": "오버사이즈후드" },
    { "hashtag": "후드티코디",     "count": 20, "folder": "후드티코디" }
  ],
  "total": 40,
  "filters_applied": ["no-videos", "min-size-10kb", "min-resolution-300px"]
}
```

---

## Step 5: 결과 보고 (수집 완료 후 사용자에게 전달되는 메시지)

```
✅ 수집 완료

태그별 수집 결과:
  #오버사이즈후드   20장  →  workspace/moodboard/instagram_20260324/오버사이즈후드/
  #후드티코디       20장  →  workspace/moodboard/instagram_20260324/후드티코디/

전체: 40장 수집 완료
릴스·동영상: 전체 제외됨 (--no-videos)
자동 품질 필터: 10KB 미만·300px 미만 이미지 제거 (해당 없음 가정)

저장 경로: workspace/moodboard/instagram_20260324/

브랜드 적합도 필터링이 필요하면 "필터링해줘"라고 말씀해 주세요.
```

---

## 비고

- AI 브랜드 적합도 필터링(filter.py)은 이번 수집에서 **실행하지 않음** — 사용자가 별도 요청할 때만 실행.
- 저작권 주의: 수집 이미지는 내부 무드보드·리서치 목적으로만 사용 가능. 외부 공개·상업적 사용 금지.
