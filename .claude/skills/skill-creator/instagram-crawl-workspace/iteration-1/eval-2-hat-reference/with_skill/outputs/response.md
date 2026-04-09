# 인스타그램 레퍼런스 수집 시뮬레이션

**요청:** SNS에서 27SS 모자 레퍼런스 긁어줘. 볼캡이랑 버킷햇 위주로 30장.

---

## Step 1: 요청 해석 및 해시태그 클러스터 설계

**SNS 플랫폼 해석:** "SNS"는 기본값으로 **Instagram**으로 해석.
Pinterest 등 다른 플랫폼이 필요하면 명시적으로 요청 필요.

**아이템 파악:**
- 1차 아이템: 볼캡 (Ball Cap)
- 2차 아이템: 버킷햇 (Bucket Hat)
- 시즌 컨텍스트: 27SS (트렌드 레퍼런스 목적)
- 요청 수량: 30장

**해시태그 클러스터 설계 (초안):**

| 레이어 | 태그 | 근거 |
|--------|------|------|
| 핵심 (볼캡) | `#볼캡코디` | ~40만건, 구체적 |
| 핵심 (버킷햇) | `#버킷햇코디` | ~35만건, 구체적 |
| 영문 보조 | `#buckethat` | ~180만건, 글로벌 레퍼런스 |
| 영문 보조 | `#ballcap` | ~60만건, 글로벌 레퍼런스 |
| 스타일 태그 | `#모자코디` | ~50만건, 헤드웨어 통합 |
| 시즌 맥락 | `#스트릿패션` | ~80만건, SS 무드 |
| 맥락 태그 | `#오오티디` | ~500만건 (보조 필터용) |

**제외 브랜드 (메모리 적용):** 리코리아(leekorea.co.kr), 커버낫(covernat.co.kr) 해시태그/계정 이미지 수집 안 함.

---

## Step 2: AskUserQuestion — 사용자 확인 (JSON)

> 실제 실행 시 이 JSON이 AskUserQuestion 도구로 대화창에 표시됨.

```json
{
  "questions": [
    {
      "question": "볼캡·버킷햇 핵심 해시태그를 골라주세요 (복수 선택 가능)",
      "header": "핵심 태그",
      "multiSelect": true,
      "options": [
        {
          "label": "#볼캡코디",
          "description": "볼캡 착용 코디 게시물 위주 (~40만건)"
        },
        {
          "label": "#버킷햇코디",
          "description": "버킷햇 착용 코디 게시물 위주 (~35만건)"
        },
        {
          "label": "#buckethat",
          "description": "영문 버킷햇 — 글로벌 레퍼런스 포함 (~180만건, 필터링 필요)"
        },
        {
          "label": "#ballcap",
          "description": "영문 볼캡 — 글로벌 스트릿 레퍼런스 (~60만건)"
        }
      ]
    },
    {
      "question": "27SS 무드에 맞는 스타일 방향을 선택해주세요",
      "header": "스타일·맥락 태그",
      "multiSelect": true,
      "options": [
        {
          "label": "#모자코디",
          "description": "헤드웨어 전반 코디 (~50만건)"
        },
        {
          "label": "#스트릿패션",
          "description": "SS 시즌 스트릿 무드 (~80만건)"
        },
        {
          "label": "#캐주얼코디",
          "description": "캐주얼 데일리 스타일링 (~120만건)"
        },
        {
          "label": "#키치패션",
          "description": "와키윌리 브랜드 무드와 근접한 키치 스타일 (~30만건)"
        }
      ]
    },
    {
      "question": "수집 수량을 확인해주세요",
      "header": "수량",
      "multiSelect": false,
      "options": [
        {
          "label": "30장 (요청대로)",
          "description": "태그별 수량은 자동 배분 (태그 수에 따라 조정)"
        },
        {
          "label": "태그별 30장 (총 ~90~150장)",
          "description": "선택한 태그 각각에서 30장씩 수집"
        },
        {
          "label": "20장으로 줄이기",
          "description": "빠른 수집이 필요할 때"
        }
      ]
    }
  ]
}
```

**시뮬레이션 가정:** 사용자가 `#볼캡코디`, `#버킷햇코디`, `#키치패션` + `30장 (요청대로)` 선택으로 가정.

확인 메시지:
```
→ #볼캡코디 (10장), #버킷햇코디 (10장), #키치패션 (10장) — 총 30장 수집합니다. 진행할까요?
```

---

## Step 3: 크롤러 실행 명령어

사용자 승인 후 아래 명령어를 순차 실행. 태그 간 10초 쿨다운 적용.

```bash
# 태그 1: 볼캡코디 (10장)
python3 scripts/instagram-crawler/crawler.py \
  --hashtag "볼캡코디" \
  --count 10 \
  --no-videos 2>&1

sleep 10

# 태그 2: 버킷햇코디 (10장)
python3 scripts/instagram-crawler/crawler.py \
  --hashtag "버킷햇코디" \
  --count 10 \
  --no-videos 2>&1

sleep 10

# 태그 3: 키치패션 (10장)
python3 scripts/instagram-crawler/crawler.py \
  --hashtag "키치패션" \
  --count 10 \
  --no-videos 2>&1
```

루프 형태로도 동일하게 실행 가능:

```bash
declare -A TAG_COUNTS=(["볼캡코디"]=10 ["버킷햇코디"]=10 ["키치패션"]=10)

for TAG in 볼캡코디 버킷햇코디 키치패션; do
  python3 scripts/instagram-crawler/crawler.py \
    --hashtag "$TAG" \
    --count "${TAG_COUNTS[$TAG]}" \
    --no-videos 2>&1
  echo "[완료] $TAG — 다음 태그까지 10초 대기..."
  sleep 10
done
```

**적용된 옵션 요약:**
- `--no-videos`: Reels·동영상 제외, 이미지 포스트만 수집 (항상 포함)
- `--count 10`: 태그별 10장 (총 30장 = 요청 수량 충족)
- 태그 간 쿨다운: 10초 (Instagram 차단 방지)
- 타임아웃: 120초/태그

---

## Step 4: 폴더 구조 결과

수집 완료 후 `workspace/moodboard/instagram_20260324/` 에 저장.

```
workspace/moodboard/instagram_20260324/
├── 볼캡코디/
│   ├── img_001.jpg    ← 볼캡 코디 게시물
│   ├── img_002.jpg
│   ├── img_003.jpg
│   ├── img_004.jpg
│   ├── img_005.jpg
│   ├── img_006.jpg
│   ├── img_007.jpg
│   ├── img_008.jpg
│   ├── img_009.jpg
│   └── img_010.jpg
├── 버킷햇코디/
│   ├── img_001.jpg    ← 버킷햇 코디 게시물
│   ├── img_002.jpg
│   ├── img_003.jpg
│   ├── img_004.jpg
│   ├── img_005.jpg
│   ├── img_006.jpg
│   ├── img_007.jpg
│   ├── img_008.jpg
│   ├── img_009.jpg
│   └── img_010.jpg
├── 키치패션/
│   ├── img_001.jpg    ← 키치 패션 헤드웨어 포함 코디
│   ├── img_002.jpg
│   ├── img_003.jpg
│   ├── img_004.jpg
│   ├── img_005.jpg
│   ├── img_006.jpg
│   ├── img_007.jpg
│   ├── img_008.jpg
│   ├── img_009.jpg
│   └── img_010.jpg
└── _metadata.json     ← 수집 메타데이터 (태그·장수·날짜)
```

**_metadata.json 예시:**
```json
{
  "collected_at": "2026-03-24T00:00:00Z",
  "season": "27SS",
  "purpose": "hat-reference",
  "tags": [
    {"tag": "볼캡코디", "requested": 10, "collected": 10, "filtered_out": 0},
    {"tag": "버킷햇코디", "requested": 10, "collected": 10, "filtered_out": 0},
    {"tag": "키치패션", "requested": 10, "collected": 9, "filtered_out": 1}
  ],
  "total_collected": 29,
  "total_filtered_out": 1,
  "filter_reasons": ["해상도 300px 미만 1건 제외"]
}
```

---

## Step 5: 결과 보고

```
[완료] 27SS 모자 레퍼런스 수집 결과

수집 태그 및 장수:
  #볼캡코디    10장 ✓
  #버킷햇코디  10장 ✓
  #키치패션     9장 (1장 해상도 필터링 제외)
──────────────────
  총 수집:     29장 / 30장 요청

필터링 내역:
  - 해상도 300px 미만: 1건 제외 (#키치패션)
  - 동영상/Reels: 0건 (--no-videos 적용)
  - 10KB 미만 썸네일: 0건

저장 경로:
  workspace/moodboard/instagram_20260324/
  ├── 볼캡코디/     (10장)
  ├── 버킷햇코디/   (10장)
  └── 키치패션/      (9장)

제외 브랜드 적용: 리코리아, 커버낫 계정 이미지 수집 안 함 ✓

추가 작업:
  → 브랜드 적합도 필터링이 필요하면 "필터링해줘"라고 말씀해주세요.
  → 수집 부족분(1장)을 보충하려면 동일 태그 재실행 또는 #모자코디 추가 수집 가능합니다.
```

---

## 참고: 스킬 적용 요약

| 항목 | 처리 내용 |
|------|----------|
| "SNS" 해석 | Instagram으로 자동 해석 |
| 아이템 파싱 | 볼캡, 버킷햇 → 한국어 핵심 태그 + 브랜드 무드 태그 설계 |
| 수량 배분 | 30장 → 3개 태그 × 10장 균등 배분 |
| 제외 브랜드 | 메모리(feedback_image_exclusions.md) 기반 자동 적용 |
| 쿨다운 | 태그 간 10초 (Instagram 차단 방지) |
| 필터 | --no-videos 항상 포함, 해상도/파일크기 자동 필터 |
| 필터링 모드 | 수집 직후 자동 실행 안 함 — 명시 요청 시에만 실행 |
