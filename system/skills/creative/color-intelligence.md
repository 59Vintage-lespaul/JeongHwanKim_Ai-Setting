---
type: skill
id: color-intelligence
name: 컬러 인텔리전스
agency: creative-studio
role: 컬러 스트래티지스트 (Color Strategist)
phase: plan → design
triggers:
  - 시즌 컬러 팔레트 만들어줘
  - 컬러 전략 짜줘
  - 경쟁사 컬러 분석해줘
  - 이번 시즌 어떤 컬러 써야 해?
  - 카테고리별 컬러 배분해줘
  - 악센트 컬러 뭐가 좋아?
  - 씨빅 시즌 컬러 정해줘
presets:
  - visual-identity.json
  - brand.config.json
  - categories.json
  - personas.json
feeds:
  - skills/data/trend-radar.md
  - skills/creative/moodboard.md
  - skills/data/musinsa-ranking.md
outputs:
  - "workspace/[시즌]/season-strategy/plan_color-palette_YYYY-MM-DD.md"
---

# 컬러 인텔리전스 (Color Intelligence)

> 브랜드 시그니처 컬러, 트렌드 팔레트, 경쟁사 전략, 소비자 선호도를 분석하여
> 시즌 마스터 팔레트와 카테고리별 컬러 배분을 설계하는 독립 스킬.
> `moodboard`(정성적 방향 설정)와 `design-spec`(아이템 실행) 사이를 정량적으로 연결한다.

## 기존 스킬과의 관계

| 연계 스킬 | 관계 |
|----------|------|
| `trend-radar` | 비주얼 시그널의 컬러 데이터를 피드로 수신 |
| `moodboard` | 무드보드의 정성적 컬러 방향을 정량 팔레트로 구체화 |
| `design-spec` | 완성된 팔레트를 아이템별 컬러웨이로 연결 |
| `design-generator` | 컬러웨이 매트릭스를 디자인 시안 생성에 제공 |

## 언제 사용

- PDCA Plan 단계 — 시즌 시작 전 컬러 전략 수립
- trend-radar 직후 — 비주얼 시그널 컬러 데이터를 팔레트로 전환
- 씨빅 패딩 등 히어로 아이템의 시즌 컬러 확장 결정 시
- 카테고리별 컬러 배분이 BTA 가이드라인과 맞는지 검증 시

---

## 실행 절차

### Step 1: 브랜드 DNA 컬러 고정 확인

`visual-identity.json`에서 불변 시그니처 컬러를 확인하고 고정한다.

**커버낫 시그니처 컬러 (변경 불가):**
| 컬러 | HEX | 용도 |
|------|-----|------|
| Covernat Navy | #1a2a3a | 로고, 주요 베이직 아이템, 크리에이티브 배경 |
| Clean White | #FFFFFF | 기본 아이템, 캠페인 배경, 클린 버전 |
| Charcoal Gray | #3a3a3a | 베이직 아이템, 아우터, 바텀 |

**시즌 악센트 컬러 규칙** (`visual-identity.json` > `accent_rule`):
- 스테디셀러 모델 1개(보통 씨빅)에 시즌 악센트 컬러 전개
- BTA 악센트 컬러 운용 규칙 준수
- 예시: 버건디, 모카, 카키 등 — 매 시즌 신규 선정

---

### Step 2: 트렌드 컬러 수집

**데이터 소스:**
- `trend-radar` 결과물의 비주얼 시그널 컬러 데이터
- 웹서치: "PANTONE color of the year 2026", "fashion color trend 2026 SS/FW"
- 무신사 랭킹 상위 아이템 컬러 분포 (musinsa-ranking 데이터)
- 런웨이 컬러 리포트 (Vogue, WWD, Hypebeast 등)

**수집 항목:**
```
트렌드 컬러 #[N]:
- 컬러명: [트렌드 네이밍]
- HEX 근사값: [#xxxxxx]
- 출처: [PANTONE/런웨이/SNS]
- 검색량·언급량: [숫자]
- 커버낫 DNA 적합도: [높음/중간/낮음] + 이유
```

---

### Step 3: 경쟁사 컬러 스캔

경쟁 브랜드의 시즌 컬러 전략을 파악하여 화이트스페이스를 찾는다.

**주요 모니터링 브랜드:** 디스이즈네버댓, 마하그리드, 엑스라지, 스투시, 폴로

**수집 항목:**
| 브랜드 | 시즌 주력 컬러 | 포지셔닝 | 커버낫 대비 공백 |
|--------|-------------|---------|--------------|
| [브랜드A] | | | |
| [브랜드B] | | | |

---

### Step 4: 마스터 팔레트 설계 (12~16색)

**4축 스코어링** (각 1~10점):
| 축 | 기준 |
|---|------|
| Trend Strength | 트렌드 데이터에서 얼마나 강한 시그널인가 |
| Brand Alignment | 커버낫 DNA(Timeless/Authentic/Clean)와 맞는가 |
| Commercial Viability | 실제 판매 가능성, 소비자 수용도 |
| Whitespace | 경쟁사 미선점 여부 |

**팔레트 구조:**
| 구분 | 색 수 | 설명 |
|------|-------|------|
| Core | 3색 | 시그니처 컬러 (Navy/White/Charcoal) — 불변 |
| Season Main | 4~6색 | 트렌드 검증된 시즌 주력 컬러 |
| Accent | 2~3색 | 실험적·시즌 차별화 컬러 (씨빅 등 악센트) |
| Neutral | 2~3색 | 스타일링 베이스 (Beige/Earth Khaki 계열) |

---

### Step 5: 라인별 · 카테고리별 컬러 배분

**라인 감도 차별화:**
| 라인 | 컬러 방향 | 특징 |
|------|---------|------|
| COVERNAT_LINE | Core + Season Main 중심 | 브랜드 아이덴티티 전달, 대중적 수용성 |
| AUTHENTIC_LINE | Core + Neutral 중심 | 소재·봉제 퀄리티 강조, 절제된 컬러 |
| COLLEGE_LINE | Core + Accent 활용 | 아치 로고, 캠퍼스 무드, 젊은 에너지 |

**BTA별 컬러 규칙:**
| BTA | 컬러 원칙 |
|-----|---------|
| Basic | Core 컬러(Navy/White/Charcoal) 위주 — 리오더 베이직 |
| Trend | Season Main 컬러 — 시즌 감도 전달 |
| Accent | Accent 컬러 + Core 조합 — 아이캐칭, 컬렉터블 |

**악센트 컬러 배분 원칙:** 씨빅 패딩 + 스테디셀러 1~2개에만 집중 적용

---

### Step 6: 컬러 스토리 작성

팔레트 전체를 관통하는 시즌 서사를 작성한다.

```
[시즌] 컬러 스토리

테마: [시즌 테마와 컬러의 연결]
서사: [2~3문장으로 팔레트가 전달하는 이야기]
핵심 컬러: [이번 시즌을 대표하는 1~2색과 이유]
소비자 감성: [페르소나 기준 어떤 감정을 불러일으키는가]
```

---

## 산출물 포맷

```markdown
# [시즌] 컬러 팔레트 — YYYY-MM-DD

## 시즌 컬러 스토리
[Step 6 서사]

## 마스터 팔레트

### Core (불변)
| 컬러명 | HEX | 용도 |
|--------|-----|------|
| Covernat Navy | #1a2a3a | 로고·베이직 |
| Clean White | #FFFFFF | 기본·배경 |
| Charcoal Gray | #3a3a3a | 베이직·아우터 |

### Season Main
| # | 컬러명 | HEX | 트렌드점수 | 브랜드점수 | 상업점수 | 공백점수 | BTA |
|---|--------|-----|----------|----------|---------|---------|-----|

### Accent (씨빅 시즌 컬러 포함)
| # | 컬러명 | HEX | 적용 아이템 | 이유 |
|---|--------|-----|-----------|------|

### Neutral
| # | 컬러명 | HEX | 활용 방식 |
|---|--------|-----|---------|

## 라인별 컬러 배분
[Step 5 테이블]

## 경쟁사 화이트스페이스 분석
[Step 3 테이블]

## 연결 스킬
- `design-generator` → 컬러웨이 매트릭스 전달
- `design-spec` → 아이템별 컬러 지정
- `moodboard` → 팔레트 비주얼화
```

---

## 완료 조건

- [ ] 시그니처 컬러 3색 확인 및 고정 완료
- [ ] 트렌드 컬러 최소 10색 이상 수집 및 스코어링
- [ ] 경쟁사 컬러 전략 분석 및 화이트스페이스 식별
- [ ] 마스터 팔레트 12~16색 확정 (Core/Main/Accent/Neutral 구분)
- [ ] 씨빅 패딩 시즌 악센트 컬러 확정
- [ ] 라인별·BTA별 배분 완료
- [ ] 컬러 스토리 작성

## 체크리스트

- [ ] 악센트 컬러가 스테디셀러 1개 집중 원칙을 준수하는가?
- [ ] BTA 컬러 배분이 bta-guideline.md와 정합하는가?
- [ ] 3B 착장 금지 (베이직 아이템 + 베이직 컬러 + 베이직 로고) 고려하여 배분?
- [ ] AUTHENTIC_LINE의 절제된 컬러 감도가 반영되었는가?
- [ ] COLLEGE_LINE에 아치 로고 연계 컬러 방향이 포함되었는가?
