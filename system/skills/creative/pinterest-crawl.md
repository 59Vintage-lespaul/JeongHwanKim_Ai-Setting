---
type: skill
id: pinterest-crawl
name: 핀터레스트 이미지 수집
agency: creative-studio
role: 크리에이티브 디렉터 (Creative Director)
phase: any
triggers:
  - 핀터레스트에서 이미지 수집해줘
  - 레퍼런스 이미지 모아줘
  - 키워드로 이미지 검색해줘
  - 무드보드 이미지 크롤링해줘
  - 수집한 이미지 필터링해줘
  - 브랜드 적합도 검사해줘
  - 이거랑 비슷한 이미지 찾아줘
presets:
  - visual-identity.json
  - brand.config.json
scripts:
  - system/scripts/pinterest-crawler/crawler.py
  - system/scripts/pinterest-crawler/filter.py
outputs:
  - "workspace/moodboard/pinterest_YYYYMMDD/[keyword-folder]/"
---

# 핀터레스트 이미지 수집

> 사용자가 자연어로 키워드를 말하거나 이미지를 보여주면,
> 최적의 검색 키워드를 설계하여 Pinterest에서 이미지를 수집하고
> 키워드별 폴더로 자동 분류하는 파이프라인.

## 언제 사용

이 스킬은 사용자가 아래와 같이 요청할 때 작동한다:
- "도파민 드레싱 이미지 수집해줘"
- "핀터레스트에서 캐주얼 패션 검색해줘"
- "볼꾸 레퍼런스 30장 모아줘"
- "이거랑 비슷한 이미지 찾아줘" (이미지 첨부)
- "수집한 이미지 AI 필터링 돌려줘"

사용자가 특정 키워드와 함께 "이미지", "레퍼런스", "수집", "검색", "크롤링", "모아줘" 같은
표현을 쓰면 이 스킬에 해당할 가능성이 높다.

---

## Step 1: 검색 키워드 설계 (사용자 확인 필수)

키워드 품질이 수집 결과를 결정한다.
사용자 입력(텍스트 또는 이미지)을 분석하여 검색 키워드를 설계하고,
**반드시 사용자에게 확인받은 후** 크롤링을 시작한다.

### 1-A: 텍스트 키워드가 주어진 경우

사용자의 자연어를 아래 공식으로 변환한다:

**키워드 구조**: `[소재/디테일] + [아이템] + [맥락/스타일]`

| 구조 | 예시 | 결과 품질 |
|------|------|----------|
| 아이템만 | `슬리퍼` | 너무 넓음 |
| 아이템 + 디테일 | `fur slide sandal` | 중간 |
| 디테일 + 아이템 + 맥락 | `luxury fur slide sandal logo` | 정확도 높음 |

**변환 규칙:**
- 한국어 줄임말/트렌드어는 영문 동의어로 변환 (예: "볼꾸" → `embroidered trucker cap`)
- 추상적 표현은 구체적 영문으로 (예: "구동화" → `chunky sneaker street outfit`)
- 영문이 메인, 한국어는 보조 (Pinterest는 영문 결과가 압도적)
- 키워드는 3~5단어가 최적. 6개 이상은 오히려 노이즈 증가

**잘 먹히는 수식어:**
- `lookbook`, `outfit`, `street snap` → 착장컷
- `editorial`, `campaign` → 화보/광고컷
- `2025`, `2026` → 최신 트렌드
- `colorful`, `bold`, `vivid` → 커버낫 무드 매칭

**피해야 할 패턴:**
- 브랜드명 단독 (`Celine shoes`) → 상품 판매 페이지만 나옴
- 너무 추상적 (`예쁜 신발`, `트렌디한`) → 노이즈 많음

### 1-B: 이미지가 주어진 경우

이미지를 분석하여 아래 5가지 요소를 순서대로 추출한다:

```
① 소재/텍스처  →  fur, suede, leather, knit, denim, canvas
② 형태/실루엣  →  mule, slide, chunky, oversized, cropped, boxy
③ 디테일       →  ribbon, logo, embroidered, patchwork, buckle
④ 컬러         →  beige, neon, color-blocking, pastel, monochrome
⑤ 맥락         →  street, outfit, styling, editorial, lookbook
```

이 5요소에서 3~5개를 조합하여 영문 검색 키워드를 만든다.

### 1-C: 사용자 선택형 확인 (AskUserQuestion 사용)

키워드 설계 후, `AskUserQuestion` 도구로 **대화창 내 클릭 선택지**를 제시한다.
사용자가 클릭만으로 방향을 고를 수 있어 가장 빠르게 의도를 반영할 수 있다.

**제약사항**: AskUserQuestion은 한 번에 최대 4개 질문, 각 최대 4개 옵션.
5요소를 두 번에 나눠 질문한다:

**1차 질문** (4개 동시, multiSelect: true):
- ① 소재/텍스처 — 키워드에서 파생된 3~4개 선택지
- ② 형태/실루엣 — 키워드에서 파생된 3~4개 선택지
- ③ 디테일 — 키워드에서 파생된 3~4개 선택지
- ④ 컬러 — 키워드에서 파생된 3~4개 선택지

**2차 질문** (1~2개):
- ⑤ 맥락/스타일 — street, editorial, lookbook, runway 등
- 수량 — 기본 30장, 변경 필요 시

각 옵션은 `label`(영문 키워드)과 `description`(한글 설명)으로 구성한다.

**예시** (파자마 패션):
```json
{
  "questions": [
    {
      "question": "소재/텍스처를 골라주세요",
      "header": "소재",
      "multiSelect": true,
      "options": [
        {"label": "Satin / Silk", "description": "광택감 있는 새틴·실크"},
        {"label": "Cotton / Jersey", "description": "캐주얼한 코튼·저지"},
        {"label": "Velvet", "description": "벨벳 질감"},
        {"label": "상관없음", "description": "소재 제한 없이 검색"}
      ]
    }
  ]
}
```

사용자 선택을 반영한 최종 키워드를 한 줄로 확인 후 크롤링을 시작한다:
```
→ "satin pajama set street outfit" + "새틴 파자마 세트 스트릿" 30장 수집합니다.
```

**단순 키워드의 경우**: 영문 키워드가 이미 구체적인 경우 (예: `/pinterest dopamine dressing`)는
선택지 없이 간략하게 확인한다:
```
"dopamine dressing" 30장 수집합니다. 진행할까요?
```

### 1-D: 키워드 압축 및 분리 (5단어 규칙)

사용자 선택을 모두 반영하면 키워드가 6단어 이상이 될 수 있다.
Pinterest는 단어가 많을수록 개별 단어에 분산 매칭하여 **노이즈가 급증**한다.

**반드시 지켜야 할 규칙:**
- 각 검색 키워드는 **최대 5단어**로 압축한다.
- 5단어를 초과하면, 의미 단위로 **복수의 검색 키워드로 분리**한다.
- 분리된 키워드 각각으로 크롤러를 실행하고, 결과는 하나의 폴더에 합친다.

**압축 우선순위**: 핵심 아이템 > 소재/디테일 > 맥락 > 컬러 (컬러는 생략해도 비주얼로 필터 가능)

**분리 예시:**

| 사용자 선택 전체 | 분리 결과 |
|-----------------|----------|
| `satin mesh soccer jersey cropped layered stripe pastel street outfit` (10단어) | ① `soccer jersey street outfit` (4단어) ② `cropped soccer jersey styling` (4단어) |
| `fur ribbon mule slide sandal editorial` (6단어) | ① `fur ribbon mule sandal` (4단어) ② `ribbon slide editorial` (3단어) |
| `oversized hoodie graphic print street` (5단어) | 그대로 사용 (5단어 이내) |

**분리 후 확인**: 최종 검색 키워드 목록을 사용자에게 보여주고 확인받는다:
```
검색 키워드 (5단어 이내로 분리):
  ① "soccer jersey street outfit" (EN) + "싸커티셔츠 스트릿 코디" (KR)
  ② "cropped soccer jersey layered" (EN) + "크롭 싸커저지 레이어드" (KR)
  → 각 30장, 총 60장 수집합니다. 진행할까요?
```

---

## Step 2: 크롤러 실행

사용자 확인 후 크롤링을 실행한다.

```bash
cd "{PROJECT_ROOT}/system/scripts/pinterest-crawler" && \
python3 crawler.py --keyword "{키워드}" --count {수량} --headless 2>&1
```

핵심 옵션:
- `--headless`: 항상 기본 (브라우저 안 띄움)
- `--count`: 파싱된 수량 (기본 30)
- 타임아웃: 180초 (3분)

**복수 키워드 실행**: 1-D에서 분리된 키워드가 있으면 각각 크롤러를 실행한다.
분리된 키워드 + 한국어 보조 키워드까지 포함하면 총 실행 횟수 = 분리 키워드 수 × 2.

**영문 + 한국어 병렬 검색**: 한국어 보조 키워드가 있으면 두 번 실행하여
글로벌 레퍼런스 + 국내 스타일링을 모두 수집한다.

---

## Step 3: 키워드별 폴더 분류

크롤러는 모든 custom 키워드 이미지를 `custom/` 폴더에 저장하므로,
크롤링 후 키워드별 폴더로 분류한다.

분류 로직:
1. `_metadata.json`에서 방금 수집한 키워드의 이미지 목록 읽기
2. 키워드를 폴더명으로 변환 (공백→하이픈, 소문자, 파일시스템 안전 문자만)
3. `custom/` → `{keyword-folder}/`로 이동
4. `custom/` 폴더가 비면 삭제

폴더명 변환 예시:
| 키워드 | 폴더명 |
|--------|--------|
| dopamine dressing | `dopamine-dressing/` |
| 볼캡 꾸미기 | `bolcap-decorating/` |
| borderless casual | `borderless-casual/` |

한국어 키워드의 폴더명은 영문 음역 또는 의미 번역으로 만든다.
영문+한국어 병렬 검색의 경우 하나의 폴더에 합친다.
이전에 같은 키워드로 수집한 이력이 있으면 기존 폴더명을 따른다.

```python
# 분류 스크립트 패턴
import json, os, shutil

with open('_metadata.json') as f:
    meta = json.load(f)

keywords = ['{EN키워드}', '{KR키워드}']  # 병렬 검색 시 복수
for item in meta['categories'].get('custom', {}).get('items', []):
    if item.get('keyword') in keywords:
        fn = item.get('filename', '')
        if not fn:
            continue
        src = os.path.join('custom', fn)
        if os.path.exists(src):
            shutil.move(src, os.path.join('{keyword-folder}', fn))
```

---

## Step 4: 결과 보고

수집 완료 후 사용자에게 보고:
- 수집 장수 (신규/전체)
- 저장 경로
- 소형 이미지 필터링 수 (있으면)
- 현재까지 전체 수집 현황 (폴더별 장수)

---

## 모드 2: 카테고리 크롤링

사용자가 "브랜드 무드 전체 크롤링해줘" 같이 카테고리 단위를 요청하면:

```bash
python3 crawler.py --category brand_mood --headless 2>&1
```

사용 가능한 카테고리:
| 카테고리 | 설명 |
|----------|------|
| `brand_mood` | 보더리스 캐주얼 무드 |
| `character_ip` | 캐릭터·그래픽·IP 감성 |
| `color_vivid` | 비비드 컬러 트렌드 |
| `target_styling` | 20~27세 코어타겟 스타일링 |
| `campaign_ref` | 캠페인·룩북 레퍼런스 |
| `accessories` | 용품·악세서리 |
| `visual_merch` | VM·매장 디스플레이 |

## 모드 3: AI 브랜드 적합도 필터링

사용자가 "필터링해줘", "브랜드에 맞는 것만 골라줘" 등을 요청할 때만 실행.
크롤링 직후 자동 실행하지 않는다.

```bash
cd "{PROJECT_ROOT}/system/scripts/pinterest-crawler" && \
python3 filter.py {대상_디렉토리} -r --threshold {점수} 2>&1
```

- 기본 threshold: 7점 (10점 만점)
- `--dry-run` 옵션으로 미리보기 가능
- 부적합 이미지는 `_filtered/` 하위 폴더로 이동
- 결과 리포트: `_filter_report.json`

## 이미지 품질 필터

크롤러(`crawler.py`)에 내장된 자동 필터:
- **파일 크기**: 5KB 미만 자동 제외 (아이콘, 깨진 이미지)
- **해상도**: 100px 미만 (가로 또는 세로) 자동 제외

이 필터는 항상 작동하며 별도 설정 불필요.

## 저장 경로

```
workspace/moodboard/pinterest_YYYYMMDD/
├── {keyword-folder-1}/     ← 키워드별 폴더
├── {keyword-folder-2}/
├── {category-folder}/      ← 카테고리 크롤링 시
├── _metadata.json           ← 크롤링 메타데이터
└── _filter_report.json      ← AI 필터링 리포트 (필터 실행 시)
```

## 에러 대응

| 에러 | 원인 | 해결 |
|------|------|------|
| `NoSuchWindowException` | 브라우저 창 닫힘 | `--headless` 모드로 재실행 |
| `WebDriverException` | ChromeDriver 버전 불일치 | `webdriver-manager`가 자동 해결 |
| 이미지 0장 수집 | 키워드에 결과 없음 | 영문/한글 키워드 변형 시도 |
| Google 로그인 차단 | Selenium 감지 | `--login` (Chrome 프로필 모드) 사용 |

## 주의사항

- Pinterest ToS는 자동 크롤링을 금지한다. 내부 리서치/무드보드 용도로만 사용.
- 과도한 크롤링 시 IP 차단 가능. 키워드 간 2초, 카테고리 간 3초 쿨다운 내장.
- AI 필터링은 Anthropic API 키 필요 (환경변수 `ANTHROPIC_API_KEY`).
