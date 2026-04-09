# FPOF — 커버낫 (Covernat) 패션 하우스 시스템

> **Fashion PDCA Orchestration Framework v2.2**
>
> AI가 커버낫(Covernat) 브랜드의 시즌 기획부터 런칭까지를 함께 운영하는 패션 하우스 오케스트레이션 시스템입니다.
>
> 패션 실무자가 자연어로 지시하면, 브랜드 DNA와 전략을 완벽히 숙지한 AI 전문가가 실무 산출물을 만듭니다.

---

## 📋 목차

1. [시스템 개요](#-시스템-개요)
2. [스킬 아키텍처](#️-스킬-아키텍처)
3. [사용법](#-사용법)
4. [PDCA 워크플로우](#-pdca-워크플로우)
5. [스킬 전체 목록](#-스킬-전체-목록)
6. [명령어 가이드](#-명령어-가이드)
7. [폴더 구조](#-폴더-구조)

---

## 🎯 시스템 개요

### 핵심 개념

FPOF는 **2계층 스킬 아키텍처**로 구성된 패션 하우스 시스템입니다.

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: FPOF Main Skills (system/skills/)                 │
│  ─────────────────────────────────────────────────────────  │
│  27개 패션 실무 전용 스킬 (커버낫 브랜드 DNA 내장)            │
│  + Supanova 디자인 엔진 4개                                   │
│  + 50개 PM 프레임워크 스킬                                    │
│  총 81개 스킬 / 15개 카테고리                                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: 브랜드 프리셋 & 전사 가이드라인                     │
│  ─────────────────────────────────────────────────────────  │
│  커버낫 브랜드 프리셋 6종 (system/presets/covernat/)          │
│  비케이브 전사 가이드라인 6종 (system/presets/bcave/)         │
│  모든 스킬 실행 시 자동 참조                                  │
└─────────────────────────────────────────────────────────────┘
```

### 주요 특징

| 특징 | 설명 |
|------|------|
| **브랜드 중심** | 커버낫 브랜드 DNA(Borderless Casual)가 모든 스킬에 내장 |
| **PDCA 워크플로우** | Plan → Design → Do → Check → Act 자동화 |
| **품질 게이트** | 각 단계 완료 시 자동 검수 (QG1~QG4) |
| **자연어 라우팅** | 의도 기반 에이전시/역할/스킬 자동 매핑 |
| **전사 가이드 연동** | BTA·3B 금지·B.A.M.P·SNS 3균형 자동 적용 |
| **50개 PM 프레임워크** | 전략·리서치·디스커버리·실행 관리 통합 |
| **44개 슬래시 명령어** | 자주 쓰는 작업 단축 실행 |
| **상태 관리** | `.fpof-state.json`으로 실시간 진행 상황 추적 |

### 브랜드 정보

| 항목 | 내용 |
|------|------|
| **브랜드명** | 커버낫 (Covernat) |
| **컨셉** | Borderless Casual |
| **코어 타겟** | UNISEX 20–27세(core) / WOMEN 23–27세(core) |
| **앰버서더** | 추영우(국내) · TXT 수빈(아시아) · 최윤지(글로벌) |
| **비전** | K-컬처 기반 창조적 글로벌 캐주얼 브랜드 |
| **North Star** | 현시대의 소비자를 위해, 과거를 존중하며 미래의 가치를 제안한다 |
| **매출** | ~1,500억원 (2024) |

### 2026 5대 경영목표

| # | 목표 | 핵심 지표 |
|---|------|----------|
| 1 | **브랜드 아이덴티티 강화** | 코어타겟 매출 비중, 인지도/선호도 상승 |
| 2 | **히트상품 + IMC 강화** | 씨빅 빅IMC 성과, ROAS 목표 달성 |
| 3 | **슈즈 카테고리 안착** | 2026년 30억 달성, 캐주얼슈즈 포지셔닝 확립 |
| 4 | **K-컬처 앰버서더 전략** | 신규 S급 셀럽, 아시아 인지도 확대 |
| 5 | **글로벌 대응 강화** | 중국·일본·동남아 채널 확장, 해외 재구매 비중 증가 |

---

## 🏗️ 스킬 아키텍처

### 패션 실무 스킬 (27개)

#### 전략기획실 — `system/skills/strategy/` (4개)

| 스킬 | 설명 | PDCA |
|------|------|------|
| `trend-research` | 시즌 트렌드 분석, 경쟁사 동향, TAM/SAM/SOM 시장 규모 | Plan |
| `brand-strategy` | 시즌 테마 수립, SWOT 크로스 분석, 브랜드 포지셔닝 | Plan |
| `md-planning` | SKU 구성, BTA 카테고리 믹스, 물량 기획 | Plan |
| `line-sheet` | 시즌 라인시트, 상품 구성표 | Plan |

#### 크리에이티브 스튜디오 — `system/skills/creative/` (5개)

| 스킬 | 설명 | PDCA |
|------|------|------|
| `moodboard` | 시즌 무드보드, 비주얼 톤 & 무드 설정 | Design |
| `design-spec` | 디자인 스펙 정의, 소재/컬러/디테일 | Design |
| `visual-generation` | 이미지 생성, 비주얼 에셋 제작 | Design |
| `pinterest-crawl` | 핀터레스트 이미지 수집 및 분류 | Design |
| `html-slide` | HTML 기반 프레젠테이션 슬라이드 생성 | All |

#### 프로덕트 랩 — `system/skills/product/` (3개)

| 스킬 | 설명 | PDCA |
|------|------|------|
| `costing-ve` | 원가 계산, 마진 검증, VE(Value Engineering) | Design/Do |
| `techpack` | 테크팩 작성, 생산 사양서 | Do |
| `qr-process` | 리오더(Quick Response) 발주 프로세스 | Do |

#### 마케팅 쇼룸 — `system/skills/marketing/` (4개)

| 스킬 | 설명 | PDCA |
|------|------|------|
| `imc-strategy` | 통합 마케팅 커뮤니케이션 전략, BAM 기획, GTM | Do |
| `visual-content` | 화보·숏폼 기획, 콘텐츠 아이디어 | Do |
| `copywriting` | 상품 설명, 인스타 캡션, 브랜드 카피 | Do |
| `social-viral` | 인플루언서 전략, 소셜 바이럴 시퀀스 | Do |

#### 데이터 인텔리전스 — `system/skills/data/` (6개)

| 스킬 | 설명 | PDCA |
|------|------|------|
| `sales-analysis` | 매출 분석, 채널별 실적, North Star Metric 대시보드 | Check |
| `insight-archiving` | 인사이트 도출, 감성 분석, 테마 클러스터링 | Check |
| `musinsa-ranking` | 무신사 카테고리별 랭킹 수집 | Check/운영 |
| `musinsa-release` | 무신사 신규 발매 상품 수집 | Check/운영 |
| `weekly-sales-dashboard` | 주간 판매 대시보드 생성 | 운영 |
| `market-intelligence` | 시장 인텔리전스 수집 및 분석 | Plan/Check |

#### QC 본부 — `system/skills/quality/` (4개)

| 스킬 | 설명 | PDCA |
|------|------|------|
| `quality-gate` | 단계별 품질 검수 (QG1~QG4), Pre-Mortem | All |
| `gap-analysis` | 목표 대비 갭 분석 | Check |
| `completion-report` | 시즌 완료 리포트 | Check |
| `pdca-iteration` | Match Rate < 90% 자동 루프 실행 | Act |

#### Supanova 디자인 엔진 — `system/skills/design/supanova/` (4개)

| 엔진 | 설명 |
|------|------|
| `redesign-engine` | 기존 디자인 리디자인 엔진 |
| `soft-engine` | 소프트 감성 디자인 엔진 |
| `taste-engine` | 브랜드 취향 기반 디자인 엔진 |
| `output-enforcement` | 디자인 산출물 품질 강제 |

#### 태스크 유틸리티 — `system/skills/task/` (1개)

| 스킬 | 설명 |
|------|------|
| `format-conversion` | 파일 포맷 변환 유틸리티 |

---

### PM 프레임워크 스킬 (50개)

#### PM 전략 스킬 (10개) — `system/skills/pm-strategy/`

| 스킬 | 설명 |
|------|------|
| `pestle-analysis` | 거시 환경 분석 (Political/Economic/Social/Tech/Legal/Environmental) |
| `porters-five-forces` | 패션 산업 경쟁 구조 분석 |
| `ansoff-matrix` | 성장 방향 전략 (시장/제품 확장) |
| `business-model-canvas` | 9블록 비즈니스 모델 설계 |
| `lean-canvas` | 린 스타트업 캔버스 (빠른 가설 수립) |
| `value-proposition` | JTBD 기반 밸류 프로포지션 설계 |
| `product-strategy-canvas` | 9섹션 프로덕트 전략 캔버스 |
| `product-vision` | 브랜드 비전 한 문장 정의 |
| `monetization-strategy` | 수익 모델 다양화 전략 |
| `startup-canvas` | 린 캔버스 변형 스타트업 캔버스 |

#### PM 리서치 스킬 (4개) — `system/skills/pm-research/`

| 스킬 | 설명 |
|------|------|
| `customer-journey-map` | 고객 구매 여정 시각화 |
| `market-segments` | 시장 세그먼트 분석 |
| `user-personas` | 데이터 기반 사용자 페르소나 정의 |
| `user-segmentation` | 고객 그룹 세분화 |

#### PM GTM 스킬 (3개) — `system/skills/pm-gtm/`

| 스킬 | 설명 |
|------|------|
| `beachhead-segment` | 글로벌 첫 진입 시장 선택 (중국/일본/동남아) |
| `competitive-battlecard` | 경쟁사 비교 배틀카드 |
| `ideal-customer-profile` | ICP (이상적 고객 프로파일) 정의 |

#### PM 디스커버리 스킬 (12개) — `system/skills/pm-discovery/`

| 스킬 | 설명 |
|------|------|
| `opportunity-solution-tree` | 기회-솔루션 트리 구조화 |
| `brainstorm-ideas-new` | 신규 아이디어 브레인스토밍 |
| `brainstorm-ideas-existing` | 기존 상품 개선 아이디어 |
| `brainstorm-experiments-new` | 신규 실험 설계 |
| `brainstorm-experiments-existing` | 기존 실험 개선 설계 |
| `identify-assumptions-new` | 신규 가설 도출 |
| `identify-assumptions-existing` | 기존 가설 재검토 |
| `prioritize-assumptions` | 가설 우선순위 결정 |
| `prioritize-features` | 피처 우선순위 결정 (RICE/ICE/Kano) |
| `analyze-feature-requests` | 고객 피처 요청 분석 |
| `interview-script` | 고객 인터뷰 스크립트 작성 |
| `summarize-interview` | 인터뷰 결과 요약 |

#### PM 실행 스킬 (13개) — `system/skills/pm-execution/`

| 스킬 | 설명 |
|------|------|
| `brainstorm-okrs` | OKR 수립 브레인스토밍 |
| `create-prd` | PRD (제품 요구사항 문서) 작성 |
| `user-stories` | 유저 스토리 작성 |
| `job-stories` | 잡 스토리 작성 |
| `outcome-roadmap` | 아웃컴 중심 로드맵 변환 |
| `stakeholder-map` | 이해관계자 맵 작성 |
| `sprint-plan` | 스프린트 계획 수립 |
| `retro` | 스프린트/시즌 회고 |
| `summarize-meeting` | 회의록 정리 |
| `release-notes` | 릴리즈 노트 작성 |
| `test-scenarios` | QA 테스트 시나리오 작성 |
| `dummy-dataset` | 테스트 더미 데이터 생성 |
| `wwas` | What Went / Will / Action Summary |

#### PM 애널리틱스 스킬 (3개) — `system/skills/pm-analytics/`

| 스킬 | 설명 |
|------|------|
| `ab-test-analysis` | A/B 테스트 결과 분석 |
| `cohort-analysis` | 코호트 분석 (리텐션/이탈 패턴) |
| `sql-queries` | 데이터 쿼리 SQL 작성 |

#### PM 마케팅 스킬 (1개) — `system/skills/pm-marketing/`

| 스킬 | 설명 |
|------|------|
| `product-name` | 상품/라인 네이밍 |

#### PM 툴킷 스킬 (4개) — `system/skills/pm-toolkit/`

| 스킬 | 설명 |
|------|------|
| `grammar-check` | 문법 & 흐름 교정 |
| `draft-nda` | NDA (비밀유지계약서) 작성 |
| `privacy-policy` | 개인정보처리방침 작성 |
| `review-resume` | 이력서 검토 |

---

## 🚀 사용법

### 시작하기

#### 1. 필수 환경

- [Claude Code](https://claude.ai/code) 설치 (CLI 또는 데스크탑 앱)

#### 2. 저장소 클론

```bash
git clone https://github.com/59Vintage-lespaul/JeongHwanKim_Ai-Setting
cd JeongHwanKim_Ai-Setting
```

#### 3. 의존성 설치

```bash
cd system
npm install
```

#### 4. Claude Code로 열기

```bash
claude .
```

세션이 시작되면 AI가 자동으로 `.fpof-state.json`을 읽고 현재 시즌·단계를 파악합니다.

---

### 자연어 요청

FPOF는 의도를 파악하여 자동으로 적합한 스킬로 라우팅합니다.

```
"요즘 캐주얼 트렌드 어때?"         → trend-research
"26SS 시즌 테마 잡아줘"            → brand-strategy
"무드보드 만들어줘"                → moodboard
"인스타 캡션 써줘"                 → copywriting
"무신사 랭킹 가져와"               → musinsa-ranking
"경쟁사 비교표 만들어줘"           → competitive-battlecard
"OKR 짜줘"                        → brainstorm-okrs
"이번 주 매출 분석해줘"            → sales-analysis
```

### 슬래시 명령어

자주 사용하는 작업은 슬래시 명령어로 빠르게 실행합니다.

```
/status              # 현재 상태 확인
/brief trend         # 트렌드 브리프 생성
/market-scan         # 거시환경 종합 분석
/musinsa-ranking     # 무신사 랭킹 수집
/musinsa-release     # 무신사 발매판 수집
/discover            # 프로덕트 디스커버리 사이클
/launch              # GTM 런칭 전략
/review              # 품질 게이트 검수
/next                # 다음 PDCA 단계 전환
```

---

## 🔄 PDCA 워크플로우

```
Plan (기획)
  ↓  trend-research → brand-strategy → md-planning → line-sheet
  ↓  Quality Gate 1 (QG1)
Design (디자인)
  ↓  moodboard → design-spec → costing-ve → visual-generation
  ↓  Quality Gate 2 (QG2)
Do (실행)
  ↓  techpack → imc-strategy → visual-content → copywriting → social-viral
  ↓  Quality Gate 3 (QG3)
Check (분석)
  ↓  sales-analysis → insight-archiving → gap-analysis → completion-report
  ↓  Quality Gate 4 (QG4)
Act (개선)
  ↓  pdca-iteration (Match Rate < 90% 시 자동 루프)
```

### 품질 게이트 (QG)

| 게이트 | 기준 | 통과 조건 |
|--------|------|----------|
| **QG1** | Plan → Design | 트렌드 브리프, 브랜드 전략, MD 플래닝, 라인시트, BTA 구성 완료 |
| **QG2** | Design → Do | 무드보드, 디자인 스펙, 원가 검증, 비주얼 에셋, 3B 착장 금지 확인 |
| **QG3** | Do → Check | 테크팩, 캠페인 브리프, 콘텐츠 기획서, 카피 데크, 런칭 시퀀스 |
| **QG4** | Check → Next Cycle | Match Rate ≥ 90% → COMPLETE / < 90% → Act |

---

## 📚 스킬 전체 목록

### 자연어 → 스킬 라우팅 가이드

#### 시즌 기획 & 전략

| 이렇게 말하면 | 스킬 |
|-------------|------|
| "요즘 뭐가 유행이야?", "경쟁사 뭐 하고 있어?" | `trend-research` |
| "시즌 테마 잡아줘", "브랜드 방향 정리해줘" | `brand-strategy` |
| "SKU 어떻게 짜?", "카테고리 믹스 해줘" | `md-planning` |
| "라인시트 만들어줘", "물량 얼마나 잡아?" | `line-sheet` |
| "외부 환경 봐줘", "세상이 어떻게 변해?" | `pestle-analysis` |
| "업계 경쟁 상황이 어때?" | `porters-five-forces` |
| "어디로 성장해야 해?" | `ansoff-matrix` |
| "사업 모델 정리해줘" | `business-model-canvas` |
| "고객한테 어떤 가치를 줘?" | `value-proposition` |
| "브랜드 비전 한 문장으로" | `product-vision` |

#### 디자인 & 비주얼

| 이렇게 말하면 | 스킬 |
|-------------|------|
| "무드보드 만들어줘", "시즌 비주얼 톤은?" | `moodboard` |
| "핀터레스트에서 이미지 수집해줘" | `pinterest-crawl` |
| "디자인 스펙 잡아줘", "소재/컬러 정리해줘" | `design-spec` |
| "이미지 만들어줘", "에셋 제작해줘" | `visual-generation` |

#### 경쟁 & GTM

| 이렇게 말하면 | 스킬 |
|-------------|------|
| "경쟁사 비교표 만들어줘", "슈즈 경쟁사 분석해줘" | `competitive-battlecard` |
| "글로벌 첫 시장은 어디?" | `beachhead-segment` |
| "핵심 고객 정의해줘" | `ideal-customer-profile` |

#### 생산 & 원가

| 이렇게 말하면 | 스킬 |
|-------------|------|
| "원가 맞아?", "마진 계산해줘", "VE 해줘" | `costing-ve` |
| "테크팩 만들어줘" | `techpack` |
| "리오더 진행해줘" | `qr-process` |

#### 마케팅 & 콘텐츠

| 이렇게 말하면 | 스킬 |
|-------------|------|
| "마케팅 전략 짜줘", "BAM 기획해줘", "IMC 계획" | `imc-strategy` |
| "화보 기획해줘", "숏폼 기획" | `visual-content` |
| "상품 설명 써줘", "인스타 캡션 써줘" | `copywriting` |
| "인플루언서 찾아줘", "런칭 시퀀스" | `social-viral` |
| "이름 뭐로 하지?", "상품명 후보 뽑아줘" | `product-name` |

#### 데이터 & 분석

| 이렇게 말하면 | 스킬 |
|-------------|------|
| "매출 분석해줘", "채널별 비교" | `sales-analysis` |
| "인사이트 뽑아줘", "왜 잘 팔렸어?" | `insight-archiving` |
| "무신사 랭킹 가져와" | `musinsa-ranking` |
| "무신사 발매 뭐 있어?" | `musinsa-release` |
| "주간 대시보드 만들어줘" | `weekly-sales-dashboard` |
| "시장 동향 모아줘" | `market-intelligence` |
| "A/B 테스트 결과 어때?" | `ab-test-analysis` |
| "재구매율", "코호트 분석" | `cohort-analysis` |
| "SQL 만들어줘" | `sql-queries` |

#### 아이디어 & 검증

| 이렇게 말하면 | 스킬 |
|-------------|------|
| "고객 기회 구조화해보자" | `opportunity-solution-tree` |
| "아이디어 좀 내봐" | `brainstorm-ideas-new` / `brainstorm-ideas-existing` |
| "이거 어떻게 테스트해?" | `brainstorm-experiments-*` |
| "잘못 가정하는 거 없어?" | `identify-assumptions-*` |
| "뭐부터 해야 해?" | `prioritize-features` / `prioritize-assumptions` |
| "고객들이 뭘 원해?" | `analyze-feature-requests` |
| "인터뷰 질문지 만들어줘" | `interview-script` |

#### 리서치 & 페르소나

| 이렇게 말하면 | 스킬 |
|-------------|------|
| "고객 여정 그려줘" | `customer-journey-map` |
| "고객 페르소나 잡아줘" | `user-personas` |
| "고객 그룹 나눠줘" | `user-segmentation` / `market-segments` |

#### 실행 & 관리

| 이렇게 말하면 | 스킬 |
|-------------|------|
| "OKR 짜줘" | `brainstorm-okrs` |
| "PRD 만들어줘" | `create-prd` |
| "로드맵 아웃컴으로 바꿔줘" | `outcome-roadmap` |
| "이해관계자 정리해줘" | `stakeholder-map` |
| "스프린트 계획 짜줘" | `sprint-plan` |
| "회의 내용 정리해줘" | `summarize-meeting` |
| "이번 시즌 회고해보자" | `retro` |

#### 품질 & 검수

| 이렇게 말하면 | 스킬 |
|-------------|------|
| "검수해줘", "다음 단계 갈 수 있어?" | `quality-gate` |
| "갭 분석해줘" | `gap-analysis` |
| "시즌 끝! 리포트 만들어줘" | `completion-report` |
| "문법 틀린 데 없어?" | `grammar-check` |

---

## 🎮 명령어 가이드

### 핵심 FPOF 명령어

| 명령어 | 기능 |
|--------|------|
| `/status` | 현재 시즌·PDCA 단계·산출물 현황 |
| `/brief [유형]` | 산출물 템플릿 기반 문서 작성 |
| `/review` | 현재 단계 Quality Gate 검수 |
| `/next` | 다음 PDCA 단계 전환 |
| `/team` | 에이전시 팀 현황 조회 |
| `/export` | 시즌 산출물 목록 정리 |

### 문서 생성 명령어

| 명령어 | 기능 |
|--------|------|
| `/deck [유형]` | 프레젠테이션(PPTX) 생성 |
| `/pdf [유형]` | PDF 보고서 생성 |
| `/sheet [유형]` | 엑셀(XLSX) 시트 생성 |
| `/doc [유형]` | 워드(DOCX) 문서 생성 |

### 전략 & 분석 명령어

| 명령어 | 기능 |
|--------|------|
| `/market-scan` | 거시환경 종합 분석 (PESTLE+Porter's+Ansoff) |
| `/market-intel` | 시장 인텔리전스 수집 및 동향 파악 |
| `/pricing` | 가격 전략 설계 |
| `/business-model` | 비즈니스 모델 캔버스 |
| `/strategy-canvas` | 9섹션 프로덕트 전략 캔버스 |
| `/value-prop` | JTBD 밸류 프로포지션 설계 |
| `/competitive` | 경쟁 환경 분석 |
| `/battlecard` | 경쟁 배틀카드 |
| `/growth` | 그로스 루프 + GTM 모션 전략 |
| `/launch` | GTM 런칭 전략 |
| `/north-star` | North Star Metric 정의 |

### 콘텐츠 & 마케팅 명령어

| 명령어 | 기능 |
|--------|------|
| `/marketing` | 마케팅 크리에이티브 툴킷 |
| `/instagram` | 인스타그램 콘텐츠 기획 및 캡션 |
| `/pinterest` | 핀터레스트 이미지 수집 및 무드 설정 |

### 데이터 & 무신사 명령어

| 명령어 | 기능 |
|--------|------|
| `/musinsa-ranking` | 무신사 카테고리별 랭킹 수집 |
| `/musinsa-release` | 무신사 신규 발매 상품 수집 |
| `/musinsa` | 무신사 종합 분석 (랭킹 + 발매 통합) |
| `/ab-test` | A/B 테스트 분석 |
| `/cohorts` | 코호트 분석 |
| `/metrics` | 메트릭스 대시보드 설계 |

### 리서치 & 디스커버리 명령어

| 명령어 | 기능 |
|--------|------|
| `/discover` | 프로덕트 디스커버리 사이클 (아이디어→가설→실험) |
| `/brainstorm` | 멀티 관점 브레인스토밍 |
| `/interview` | 고객 인터뷰 준비/요약 |
| `/research-users` | 사용자 리서치 종합 |
| `/analyze-feedback` | 고객 피드백 감성 분석 |
| `/triage` | 피처 요청 트리아지 |

### 실행 & 관리 명령어

| 명령어 | 기능 |
|--------|------|
| `/okrs` | OKR 수립 |
| `/prd` | PRD 작성 |
| `/roadmap` | 아웃컴 로드맵 변환 |
| `/stakeholders` | 이해관계자 맵 |
| `/sprint` | 스프린트 계획/회고/릴리즈 |
| `/pre-mortem` | 프리모텀 리스크 분석 |

### 유틸리티 명령어

| 명령어 | 기능 |
|--------|------|
| `/meeting` | 회의록 정리 |
| `/proofread` | 문법/흐름 체크 |

---

## 📁 폴더 구조

```
covernat-planning-md/
├── README.md                        # 이 파일
├── CLAUDE.md                        # FPOF 커버낫 시스템 상세 설정
├── .fpof-state.json                 # 현재 시즌/PDCA 상태
├── .gitignore
│
├── .claude/                         # Claude 훅 & 명령어
│   └── commands/                    # 슬래시 명령어 (44개)
│       ├── status.md, brief.md, review.md, next.md, team.md
│       ├── export.md, deck.md, pdf.md, sheet.md, doc.md
│       ├── market-scan.md, market-intel.md, pricing.md
│       ├── business-model.md, strategy-canvas.md, value-prop.md
│       ├── competitive.md, battlecard.md, growth.md, launch.md
│       ├── north-star.md, marketing.md, instagram.md, pinterest.md
│       ├── musinsa.md, musinsa-ranking.md, musinsa-release.md
│       ├── discover.md, brainstorm.md, interview.md
│       ├── research-users.md, analyze-feedback.md, triage.md
│       ├── okrs.md, prd.md, roadmap.md, stakeholders.md
│       ├── sprint.md, pre-mortem.md, metrics.md
│       ├── ab-test.md, cohorts.md
│       └── meeting.md, proofread.md
│
├── system/
│   ├── presets/
│   │   ├── bcave/                   # 비케이브 전사 가이드라인 (6종)
│   │   │   ├── bta-guideline.md
│   │   │   ├── business-unit-guide.md
│   │   │   ├── bcave-ax-strategy-guide.md
│   │   │   ├── bcave-rework-process-innovation-guide.md
│   │   │   ├── file-naming-convention.json
│   │   │   └── product-code.json
│   │   └── covernat/                # 커버낫 브랜드 프리셋 (6종)
│   │       ├── brand.config.json
│   │       ├── personas.json
│   │       ├── tone-manner.json
│   │       ├── visual-identity.json
│   │       ├── categories.json
│   │       └── channels.json
│   │
│   ├── skills/                      # 전체 스킬 (81개)
│   │   ├── strategy/                # 전략기획실 (4개)
│   │   ├── creative/                # 크리에이티브 스튜디오 (5개)
│   │   ├── product/                 # 프로덕트 랩 (3개)
│   │   ├── marketing/               # 마케팅 쇼룸 (4개)
│   │   ├── data/                    # 데이터 인텔리전스 (6개)
│   │   ├── quality/                 # QC 본부 (4개)
│   │   ├── design/supanova/         # Supanova 디자인 엔진 (4개)
│   │   ├── task/                    # 태스크 유틸리티 (1개)
│   │   ├── pm-strategy/             # PM 전략 프레임워크 (10개)
│   │   ├── pm-research/             # PM 리서치 스킬 (4개)
│   │   ├── pm-gtm/                  # PM GTM 스킬 (3개)
│   │   ├── pm-discovery/            # PM 디스커버리 스킬 (12개)
│   │   ├── pm-execution/            # PM 실행 관리 스킬 (13개)
│   │   ├── pm-analytics/            # PM 애널리틱스 스킬 (3개)
│   │   ├── pm-marketing/            # PM 마케팅 스킬 (1개)
│   │   └── pm-toolkit/              # PM 툴킷 스킬 (4개)
│   │
│   └── package.json
│
├── scripts/                         # 유틸리티 스크립트
│
└── workspace/
    └── 26SS/                        # 시즌별 산출물
        ├── season-strategy/         # 시즌 전략 문서
        │   ├── plan_trend-brief.md
        │   ├── plan_brand-strategy.md
        │   └── plan_md-planning.md
        ├── [item-name]/             # 아이템 프로젝트
        ├── campaign-[name]/         # 캠페인 프로젝트
        ├── weekly/                  # 주간 운영
        │   ├── data/
        │   └── wNN/
        └── dashboard/              # 대시보드
```

---

## 브랜드 프리셋 파일

### 커버낫 전용 (system/presets/covernat/)

| 파일 | 내용 | 언제 참조 |
|------|------|----------|
| `brand.config.json` | DNA, North Star, 5개년 로드맵, BAM 프레임워크, 앰버서더 | 전략/기획 시 |
| `personas.json` | UNISEX/WOMEN 페르소나, K-컬처 팬덤 세그먼트 | 타겟 의사결정 시 |
| `tone-manner.json` | 브랜드 보이스, 채널별 톤, SNS 3균형 | 카피/콘텐츠 작성 시 |
| `visual-identity.json` | 브랜드 컬러(네이비/화이트/차콜), 로고 규칙, 포토그래피 무드 | 비주얼 작업 시 |
| `categories.json` | COVERNAT/AUTHENTIC/COLLEGE 3라인 + 슈즈·ACC, BTA 분류 | 상품 기획 시 |
| `channels.json` | 국내 89개·해외 50개 매장, 온라인 12채널, KPI | 유통/마케팅 전략 시 |

### 비케이브 전사 가이드라인 (system/presets/bcave/)

| 파일 | 내용 | 언제 참조 |
|------|------|----------|
| `bta-guideline.md` | BTA 상품/컬러 구성전략, 컬러 운용, 룩북 촬영 원칙 | 상품 기획, MD 플래닝 시 **항상** |
| `business-unit-guide.md` | 3B 금지, B.A.M.P 검증, 광고컷 4유형, SNS 3균형, 콜라보 원칙 | 상품/마케팅 전 영역 **항상** |
| `bcave-ax-strategy-guide.md` | AX 전략, FPOF 전사 확장 아키텍처 | AI/자동화 기획 시 |
| `file-naming-convention.json` | 파일 네이밍 & 폴더링 규칙 | 산출물 생성·저장 시 **항상** |
| `product-code.json` | 전사 품번 체계 10자리 코드 | 품번 생성·해석 시 |

---

## 핵심 운영 원칙

- **계획이 먼저** — 반드시 계획 → 승인 → 실행 순서. "알아서 해"는 금지
- **BTA 구성 필수** — Basic(안정매출) · Trend(매출+감도) · Accent(실험/아이캐칭) 균형 유지
- **3B 착장 금지** — 베이직 아이템 + 베이직 컬러 + 베이직 로고 조합 절대 지양
- **B.A.M.P 검증** — 기획안은 Branding·Awareness·Management·Product 기준 통과 필수
- **브랜드 보이스 준수** — 고객 대면 콘텐츠는 `tone-manner.json` 기반
- **참고자료가 진실** — 브랜드 정보는 프리셋 JSON 기반으로만, 지어내기 금지
- **브랜드 격리** — 와키윌리·리 브랜드 정보와 절대 혼용 금지

---

## 📌 요약 통계

| 항목 | 수량 |
|------|------|
| **패션 실무 스킬** | 27개 |
| **Supanova 디자인 엔진** | 4개 |
| **PM 프레임워크 스킬** | 50개 |
| **슬래시 명령어** | 44개 |
| **커버낫 브랜드 프리셋** | 6종 |
| **비케이브 전사 가이드라인** | 6종 |
| **에이전시** | 6개 |
| **총 스킬** | **81개** |

---

## 🚀 빠른 시작

```
# 1. 현재 상태 확인
/status

# 2. Plan 단계 시작
"26SS 트렌드 분석해줘"
/brief trend

# 3. 데이터 수집
/musinsa-ranking
/market-intel

# 4. 전략 프레임워크 활용
/market-scan        # PESTLE + Porter's + Ansoff 종합
/discover           # 아이디어 → 가설 → 실험
/okrs               # 분기 OKR 수립

# 5. 품질 검수 & 단계 전환
/review
/next
```

---

**버전**: 2.2.0
**최종 업데이트**: 2026-04-09
**라이선스**: Copyright © 2026 Covernat. All rights reserved.
