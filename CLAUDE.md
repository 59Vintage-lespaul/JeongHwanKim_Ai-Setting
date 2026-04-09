# FPOF — 커버낫 패션 하우스 오케스트레이션

> AI가 커버낫 브랜드의 시즌 기획부터 런칭까지를 함께 운영하는 시스템입니다.
> 패션 실무자가 자연어로 지시하면, AI가 브랜드 지식을 기반으로 실무 산출물을 만듭니다.
> **이 프로젝트는 와키윌리(product-planning-md), 리(leekorea-planning-md)와 완전 분리된 독립 인스턴스입니다.**

## 세션 시작 시 반드시
1. `.fpof-state.json` 읽기 — 현재 시즌, PDCA 단계, 진행 상황 파악
2. `system/presets/bcave/` 전사 가이드라인 숙지 — 경로: `system/presets/bcave/`
3. `system/presets/covernat/` 브랜드 프리셋 참조 — 현재 단계에 맞는 파일 로드

## 핵심 원칙
1. **계획이 먼저** — "알아서 해"는 금지. 반드시 계획 → 승인 → 실행 순서.
2. **브랜드 보이스 준수** — 고객 대면 콘텐츠는 반드시 `tone-manner.json` 참조.
3. **한 번에 하나씩** — 큰 작업은 쪼개서 진행. 완료 후 상태 업데이트.
4. **완료 전 셀프 체크** — 작업 완료 선언 전에 누락/오류 스스로 점검.
5. **상태 기록** — 의미 있는 진전이 있으면 `.fpof-state.json` 업데이트.
6. **참고자료가 진실** — 브랜드 정보를 지어내지 말 것. 프리셋 JSON 기반으로만.
7. **브랜드 격리** — 와키윌리·리 브랜드 정보와 절대 혼용하지 말 것.
8. **토큰 비용 절감** — 에이전트 팀/서브에이전트 사용 시 아래 "에이전트 팀 운영 규칙" 반드시 준수.

## 비케이브 전사 가이드라인 — 브랜드 공통 필수 준수

> 아래 파일들은 `system/presets/bcave/`에 위치합니다.
> 커버낫을 포함한 **모든 비케이브 브랜드**에 공통 적용되는 상위 지침입니다.

| 파일 | 내용 | 언제 참조 |
|------|------|----------|
| `bta-guideline.md` | BTA 상품/컬러 구성전략, 부서별 액션, 컬러 운용, 룩북 촬영 원칙 | 상품 기획, MD 플래닝, 디자인 스펙, 컬러 전략 시 **항상** |
| `business-unit-guide.md` | 대표이사 보고 원칙, 스케줄링, CAD맵 7대 항목, 품평 운영(3B 금지), B.A.M.P 검증, 광고컷 4유형, 셀럽 체크리스트, SNS 3균형, 콜라보 원칙, VM | 상품/마케팅/유통 전 영역 **항상** |
| `bcave-ax-strategy-guide.md` | AX 전략, FPOF 전사 확장 아키텍처, AI 사용 5대 원칙 | AI/자동화 기획 시 |
| `bcave-rework-process-innovation-guide.md` | 전사 방향성, 브랜드 감도 강화, 히트상품 프로세스 | 전사 방향성 관련 시 |
| `file-naming-convention.json` | 파일 네이밍 & 폴더링 규칙 | **산출물 생성·저장 시 항상** |
| `product-code.json` | 전사 품번 체계 10자리 코드 | 품번 생성·해석 시 **항상** |

### 전사 핵심 규칙 요약
- **BTA 구성 필수**: Basic(안정매출/신뢰) · Trend(매출+감도) · Accent(실험/아이캐칭)
- **3B 착장 금지**: 베이직 아이템 + 베이직 컬러 + 베이직 로고 조합 절대 지양
- **로고 형태 변형 금지**: 위치/크기/기법 변형만 허용
- **기획안 B.A.M.P 검증**: Branding·Awareness·Management·Product 기준
- **셀럽 파워셀럽 4대 체크리스트** 통과 필수
- **SNS 3균형**: 뉴스(상품) / 스타일링 / 로고-아이덴티티
- **콜라보 연 2회 원칙** (4시즌, 2콜라보, 2캡슐)
- **VM**: 소비자 관점 3원칙 (보기 좋게 / 집기 좋게 / 사기 좋게)

---

## 브랜드: 커버낫 (Covernat)
- **컨셉**: Borderless Casual
- **코어 타겟**: UNISEX 20-27세(core)/19-45세(range) · WOMEN 23-27세(core)/19-45세(range)
- **비전**: K-컬처 기반 창조적 글로벌 캐주얼 브랜드
- **North Star**: "현시대의 소비자를 위해, 과거를 존중하며 미래의 가치를 제안한다"
- **앰버서더**: 추영우(국내) · TXT 수빈(아시아) · 최윤지(글로벌)
- **매출**: ~1,500억원 (2024), 슈즈 신규 카테고리 런칭 중

## 브랜드 지식 베이스 (system/presets/covernat/)

| 파일 | 내용 | 언제 참조 |
|------|------|----------|
| `brand.config.json` | DNA, North Star, 5개년 로드맵, BAM 프레임워크, 시그니처 상품, 앰버서더 | 전략/기획 작업 시 |
| `personas.json` | UNISEX/WOMEN 페르소나, K-컬처 팬덤 세그먼트, 앰버서더 후보 평가 | 타겟 관련 의사결정 시 |
| `tone-manner.json` | 브랜드 보이스, 채널별 톤, 콘텐츠 프레임워크(Core/Fashion/B.I), SNS 3균형 | 카피/콘텐츠 작성 시 |
| `visual-identity.json` | 브랜드 컬러(네이비/화이트/차콜), 로고 규칙, 포토그래피 무드, 룩북 연출 | 비주얼 작업 시 |
| `categories.json` | COVERNAT/AUTHENTIC/COLLEGE 3라인 + 슈즈·ACC 신규 카테고리, BTA 분류, 콜라보 | 상품 기획 시 |
| `channels.json` | 국내 89개·해외 50개 매장, 온라인 12채널, 채널별 전략·KPI | 유통/마케팅 전략 시 |

## 스킬 시스템
> 스킬 파일 위치: `system/skills/`
> 커버낫 FPOF는 독립 인스턴스로 모든 스킬을 자체 보유합니다.

## 패션 하우스 에이전시

| 에이전시 | 팀원 (역할 → 스킬) |
|----------|-------------------|
| **전략기획실** | 시장 리서처→`trend-research` · 브랜드 전략가→`brand-strategy` · 수석 MD→`md-planning` · 컬렉션 플래너→`line-sheet` · 전략 컨설턴트→`pestle-analysis`·`porters-five-forces`·`ansoff-matrix`·`business-model-canvas`·`lean-canvas`·`value-proposition`·`product-strategy-canvas`·`product-vision` · 경쟁 분석가→`competitive-battlecard` · GTM 전략가→`beachhead-segment` · 디스커버리 리드→`opportunity-solution-tree`·`brainstorm-ideas-*`·`brainstorm-experiments-*`·`identify-assumptions-*`·`prioritize-*`·`analyze-feature-requests` · PM→`create-prd`·`user-stories` · OKR 코치→`brainstorm-okrs` · 이해관계자 매니저→`stakeholder-map` · 로드맵 설계자→`outcome-roadmap` |
| **크리에이티브 스튜디오** | 크리에이티브 디렉터→`moodboard`·`pinterest-crawl` · 패션 디자이너→`design-spec` · 아트 디렉터→`visual-generation` |
| **프로덕트 랩** | 프로덕션 매니저→`techpack`·`costing-ve`·`qr-process` |
| **마케팅 쇼룸** | 마케팅 디렉터→`imc-strategy` · 콘텐츠 디렉터→`visual-content` · 패션 에디터→`copywriting` · 소셜 전략 디렉터→`social-viral` · CX 디자이너→`customer-journey-map` · 브랜드 네이밍 전문가→`product-name` · 릴리즈 매니저→`release-notes` |
| **데이터 인텔리전스** | 트렌드 애널리스트→`sales-analysis` · 인사이트 아키텍트→`insight-archiving` · 데이터 애널리스트→`ab-test-analysis`·`cohort-analysis`·`sql-queries` · 리서치 애널리스트→`user-personas`·`user-segmentation`·`market-segments` · 고객 분석가→`ideal-customer-profile` · 데이터 엔지니어→`dummy-dataset` |
| **QC 본부** | 품질 검증관→`quality-gate` · 갭 디텍터→`gap-analysis` · 리포트 제너레이터→`completion-report` · PDCA 이터레이터→`pdca-iteration` · 회고 퍼실리테이터→`retro` · 에디터→`grammar-check` |

## 자연어 → 스킬 라우팅

### 시즌 기획 & 전략
| 이렇게 말하면 | 스킬 |
|-------------|------|
| "요즘 뭐가 유행이야?", "경쟁사 뭐 하고 있어?" | `trend-research` |
| "시즌 테마 잡아줘", "브랜드 방향 정리해줘" | `brand-strategy` |
| "SKU 어떻게 짜?", "카테고리 믹스 해줘" | `md-planning` |
| "라인시트 만들어줘", "물량 얼마나 잡아?" | `line-sheet` |
| "슈즈 경쟁사 분석해줘" | `competitive-battlecard` |
| "외부 환경 봐줘" | `pestle-analysis` |
| "업계 경쟁 상황" | `porters-five-forces` |

### 디자인 & 비주얼
| 이렇게 말하면 | 스킬 |
|-------------|------|
| "무드보드 만들어줘", "시즌 비주얼 톤은?" | `moodboard` |
| "핀터레스트에서 이미지 수집해줘" | `pinterest-crawl` |
| "디자인 스펙 잡아줘" | `design-spec` |
| "이미지 만들어줘" | `visual-generation` |

### 생산 & 원가
| 이렇게 말하면 | 스킬 |
|-------------|------|
| "원가 맞아?", "마진 계산해줘", "VE 해줘" | `costing-ve` |
| "테크팩 만들어줘" | `techpack` |
| "리오더 진행해줘" | `qr-process` |

### 마케팅 & 콘텐츠
| 이렇게 말하면 | 스킬 |
|-------------|------|
| "마케팅 전략 짜줘", "BAM 기획해줘", "IMC 계획" | `imc-strategy` |
| "화보 기획해줘", "숏폼 기획" | `visual-content` |
| "상품 설명 써줘", "인스타 캡션 써줘" | `copywriting` |
| "인플루언서 찾아줘", "런칭 시퀀스" | `social-viral` |
| "이름 뭐로 하지?", "상품명 후보 뽑아줘" | `product-name` |

### 데이터 & 분석
| 이렇게 말하면 | 스킬 |
|-------------|------|
| "매출 분석해줘", "채널별 비교" | `sales-analysis` |
| "인사이트 뽑아줘" | `insight-archiving` |
| "무신사 랭킹 가져와" | `musinsa-ranking` |
| "무신사 발매 뭐 있어?" | `musinsa-release` |
| "주간 대시보드 만들어줘" | `weekly-sales-dashboard` |

### 품질 & 검수
| 이렇게 말하면 | 스킬 |
|-------------|------|
| "검수해줘", "다음 단계 갈 수 있어?" | `quality-gate` |
| "갭 분석해줘" | `gap-analysis` |
| "시즌 끝! 리포트 만들어줘" | `completion-report` |
| "시즌 회고 해보자" | `retro` |
| "문법 틀린 데 없어?" | `grammar-check` |

## 시즌 PDCA 단계

| 단계 | 에이전시 | 스킬 |
|------|---------|------|
| **Plan** | 전략기획실 | `trend-research` → `brand-strategy` → `md-planning` → `line-sheet` |
| **Design** | 크리에이티브 스튜디오 + 프로덕트 랩 | `moodboard` → `design-spec` → `visual-generation` + `costing-ve` |
| **Do** | 프로덕트 랩 + 마케팅 쇼룸 | `techpack` · `qr-process` + `imc-strategy` → `visual-content` → `copywriting` → `social-viral` |
| **Check** | 데이터 인텔리전스 + QC 본부 | `sales-analysis` → `insight-archiving` + `gap-analysis` → `completion-report` |
| **Act** | QC 본부 | `pdca-iteration` |

## 산출물 저장 규칙

```
workspace/26SS/
├── season-strategy/          ← 시즌 전략
│   ├── plan_trend-brief.md
│   ├── plan_brand-strategy.md
│   └── plan_md-planning.md
├── [item-name]/              ← 아이템 프로젝트
├── campaign-[name]/          ← 캠페인 프로젝트
├── weekly/                   ← 주간 운영
│   ├── data/
│   └── wNN/
└── dashboard/
```

**파일명 규칙:**
- PDCA: `[pdca]_[description][_YYYY-MM-DD][_vN].[ext]`
- 운영: `[type]_[description][_YYYY-MM-DD][_vN].[ext]`
- PDCA 접두사: `plan` | `design` | `do` | `check` | `act`
- 운영 접두사: `review` | `meeting` | `deck` | `board` | `sheet` | `report` | `data`

## 에이전트 팀 운영 규칙

### 핵심 3원칙
1. **계획 승인 모드** — 팀원은 Plan Mode로 시작, 리드 승인 후 구현
2. **모델 믹싱** — "팀원 모두 Sonnet을 사용해" 지시 필수 (토큰 4~5배 절감)
3. **최소 인원** — 3~5명 제한, 완료 팀원 즉시 종료

### 자동 거절 기준
- 전사 가이드라인(BTA, 3B 금지, B.A.M.P) 미준수 계획
- 커버낫 브랜드 프리셋 미참조 계획
- 현재 PDCA 단계와 무관한 작업
- `.fpof-state.json` 업데이트 계획 누락

## 슬래시 명령어
> 슬래시 명령어 위치: `.claude/commands/`

| 명령어 | 기능 |
|--------|------|
| `/status` | 현재 시즌·PDCA 단계·산출물 현황 확인 |
| `/brief [유형]` | 산출물 템플릿 기반 문서 작성 |
| `/review` | Quality Gate 검수 |
| `/next` | 다음 PDCA 단계 전환 |
| `/musinsa-ranking` | 무신사 랭킹 수집 |
| `/musinsa-release` | 무신사 발매판 수집 |
| `/dashboard weekly` | 주간 판매 대시보드 생성 |
| `/deck [유형]` | PPTX 프레젠테이션 생성 |
| `/pdf [유형]` | PDF 보고서 생성 |
| `/sheet [유형]` | 엑셀 시트 생성 |

## 5대 경영목표 (2026)
1. **브랜드 아이덴티티 강화** — 코어타겟 매출 비중, 인지도/선호도 상승
2. **히트상품 + IMC 강화** — 씨빅 빅IMC 성과, ROAS 목표 달성
3. **슈즈 카테고리 안착** — 2026년 30억 달성, 캐주얼슈즈 포지셔닝 확립
4. **K-컬처 앰버서더 전략** — 신규 S급 셀럽, 아시아 인지도 확대
5. **글로벌 대응 강화** — 중국·일본·동남아 채널 확장, 해외 재구매 비중 증가
