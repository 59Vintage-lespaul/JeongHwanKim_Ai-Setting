---
type: skill
id: design-generator
name: AI 디자인 제너레이터
agency: creative-studio
role: 디자인 제너레이터 (Design Generator)
phase: design
triggers:
  - 디자인 시안 만들어줘
  - 디자인 아이디어 뽑아줘
  - 이 아이템 배리에이션 만들어줘
  - 그래픽 방향 잡아줘
  - 컬러웨이 매트릭스 짜줘
  - 스케치 기반으로 시안 만들어줘
  - 이번 시즌 디자인 방향성 시각화해줘
presets:
  - visual-identity.json
  - brand.config.json
  - categories.json
feeds:
  - skills/creative/moodboard.md
  - skills/creative/color-intelligence.md
  - skills/creative/design-spec.md
  - skills/creative/visual-generation.md
outputs:
  - "workspace/[시즌]/[item-name]/design_generator-sheet_YYYY-MM-DD.md"
---

# AI 디자인 제너레이터 (Design Generator)

> 텍스트 브리프, 아이템 브리프, 스케치 이미지를 입력받아
> 커버낫 브랜드 DNA에 맞는 디자인 시안 세트를 자동 생성하는 크리에이티브 엔진.
> `moodboard`(방향 설정)와 `design-spec`(상세 스펙) 사이의 비주얼라이제이션 가속기.

## 기존 스킬과의 관계

| 연계 스킬 | 관계 |
|----------|------|
| `moodboard` | 무드·방향 수신 → 구체적 배리에이션으로 전환 |
| `color-intelligence` | 컬러웨이 매트릭스 데이터 수신 |
| `design-spec` | 채택된 시안을 상세 스펙으로 연결 |
| `visual-generation` | 각 배리에이션의 이미지 생성 프롬프트 제공 |
| `visual-factory` | 최종 채택 디자인을 채널별 에셋 생산으로 연결 |

## 언제 사용

- 시즌 디자인 킥오프 — 기획 아이디어를 배리에이션으로 빠르게 시각화할 때
- 씨빅 패딩 등 히어로 아이템의 시즌 배리에이션 설계 시
- 콜라보 아이템 아이디어 탐색 시
- 트렌드 반응형 SPOT 아이템 빠른 디자인 검토 시

---

## 실행 절차

### Step 1: 브리프 입력 확인

사용자에게 다음 정보를 확인한다.

```
1. 아이템 선택:
   - COVERNAT_LINE / AUTHENTIC_LINE / COLLEGE_LINE
   - 카테고리 (상의/하의/아우터/니트웨어/슈즈/ACC)
   - 구체적 아이템명 (예: 반팔티, 씨빅 패딩, 데님 팬츠)

2. 브리프 소스:
   a. 텍스트 — 방향 설명만
   b. 아이템 브리프 파일 — 기획서/MD 플래닝 참조
   c. 스케치 이미지 — 손그림 또는 참고 이미지

3. 배리에이션 수: 3개(빠른) / 5개(표준) / 10개+(전수)

4. 우선 고려 사항:
   - 이번 시즌 컬러 팔레트 (color-intelligence 결과)
   - 무드보드 방향 (moodboard 결과)
   - BTA 포지셔닝 (Basic/Trend/Accent 중)
```

---

### Step 2: 브리프 파싱 (6요소 추출)

입력을 아래 6개 디자인 요소로 분해한다.

| 요소 | 내용 | 커버낫 참조 기준 |
|------|------|--------------|
| 아이템 유형 | 정확한 카테고리·아이템명 | categories.json |
| 핏/실루엣 | 오버사이즈/릴렉스드/레귤러/슬림 | 라인별 실루엣 가이드 |
| 소재 | 패브릭 종류, 기능성 요소 | DS-1 소재 원칙 |
| 그래픽/디테일 | 로고 기법, 프린트, 자수, 패치 | visual-identity.json 로고 규칙 |
| 컬러 | 메인·서브·포인트 컬러 | color-intelligence 팔레트 |
| 무드 | 시즌 테마와의 연결, 타겟 감성 | personas.json 코어 타겟 |

**커버낫 DNA 필터:**
- Borderless Casual 감도 — 과도한 스트릿 또는 포멀 지양
- Timeless / Authentic 무드 — 트렌디하되 시즌 후에도 입을 수 있는 디자인
- 로고 사용 원칙 — 형태 변형 절대 금지, 위치·크기·기법 변형만 허용
- 3B 착장 조합 배리에이션 금지 (베이직 아이템 + 베이직 컬러 + 베이직 로고)

---

### Step 3: 배리에이션 컨셉 설계

**5가지 축의 조합으로 배리에이션 매트릭스 생성:**

| 축 | 커버낫 주요 옵션 |
|---|--------------|
| 실루엣 | 오버사이즈 / 릴렉스드 / 레귤러 / 크롭 |
| 그래픽/디테일 | 로고 자수 / 워드마크 프린트 / 아치 로고 / 아트워크 / 클린(노 그래픽) |
| 소재 | 코튼 / 헤비 플리스 / 데님 / 울 / 테크 패브릭 |
| 컬러 | Core / Season Main / Accent 컬러 조합 |
| 라인 무드 | COVERNAT 뉴클래식 / AUTHENTIC 헤리티지 / COLLEGE 캠퍼스 |

**라인별 스타일 프리셋:**
| 라인 | 실루엣 방향 | 그래픽 방향 | 소재 방향 |
|------|-----------|-----------|---------|
| COVERNAT_LINE | 릴렉스드~오버사이즈 | 워드마크 중심, 아트워크 악센트 | 코튼 코어, 시즌 소재 |
| AUTHENTIC_LINE | 레귤러~릴렉스드 | 최소화, 품질 강조 디테일 | 고급 소재, 봉제 퀄리티 |
| COLLEGE_LINE | 오버사이즈, 크롭 믹스 | 아치 로고, 그래픽 강함 | 헤비 코튼, 플리스 |

---

### Step 4: 이미지 생성 프롬프트 작성

각 배리에이션에 대해 `visual-generation` 스킬에 전달할 프롬프트를 작성한다.

**플랫 스케치 프롬프트 구조:**
```
flat lay fashion design sketch, [아이템명], [핏/실루엣],
[소재/텍스처 묘사], [그래픽/로고 위치 및 기법],
[컬러: HEX 또는 컬러명], front and back view, clean white background,
technical fashion illustration, professional apparel design,
Covernat brand aesthetic, timeless casual, Korean streetwear
```

**착장 룩 프롬프트 구조:**
```
fashion lookbook photo, [아이템명] styled outfit,
Korean youth culture, natural lighting, urban casual setting,
[시즌 무드 키워드], real person wearing, authentic street style,
Stussy/Lemaire inspired mood, clean and effortless,
[컬러 조합], [스타일링 포인트]
```

---

### Step 5: 컬러웨이 매트릭스

각 배리에이션에 대해 BTA 기준으로 3가지 이상 컬러 조합을 제시한다.

**컬러웨이 포맷:**
```
[배리에이션 #N] 컬러웨이

Basic CW:   메인 [Navy/#1a2a3a] × 서브 [White/#FFFFFF] — 스테디셀러 대응
Trend CW:   메인 [Season Main 컬러] × 서브 [Core] — 시즌 매출 견인
Accent CW:  메인 [Accent 컬러] × 서브 [Core] — 컬렉터블, 아이캐칭
```

**씨빅 패딩 배리에이션 예시:**
- Basic CW: Navy × White (시그니처, 리오더 대상)
- Trend CW: Season Main 컬러 (시즌 신규)
- Accent CW: 시즌 악센트 컬러 (한정, 컬렉터블)

---

## 산출물 포맷

```markdown
# [시즌] [아이템명] 디자인 제너레이터 시트 — YYYY-MM-DD

## 브리프 요약
- 아이템: [라인] / [카테고리] / [아이템명]
- BTA 포지셔닝: [Basic/Trend/Accent]
- 브리프 소스: [텍스트/파일/스케치]
- 시즌 무드: [moodboard 연결]
- 컬러 팔레트: [color-intelligence 연결]

## 6요소 파싱 결과
| 요소 | 내용 |
|------|------|
| 아이템 유형 | |
| 핏/실루엣 | |
| 소재 | |
| 그래픽/디테일 | |
| 컬러 | |
| 무드 | |

## 배리에이션 [N개]

### V1: [배리에이션명]
- 컨셉: [1줄 설명]
- 차별점: [다른 배리에이션과의 차이]
- 플랫 스케치 프롬프트: [Step 4 형식]
- 착장 룩 프롬프트: [Step 4 형식]
- 컬러웨이: [Step 5 형식]
- design-spec 연동 데이터: [소재/기법/로고 위치 등]

[V2 ~ VN 동일 구조]

## 채택 권고
- 1순위: [V?] — [이유]
- 2순위: [V?] — [이유]

## 연결 스킬
- `visual-generation` → 채택 배리에이션 이미지 생성
- `design-spec` → 채택 시안 상세 스펙 작성
- `visual-factory` → 최종 채택 디자인 채널별 에셋 생산
```

---

## 완료 조건

- [ ] 6요소 파싱 완료 (아이템/핏/소재/그래픽/컬러/무드)
- [ ] 커버낫 DNA 필터 통과 확인 (형태 변형 없는 로고, 3B 금지)
- [ ] 배리에이션 사용자 요청 수만큼 생성
- [ ] 각 배리에이션에 플랫·착장 프롬프트 모두 작성
- [ ] 컬러웨이 매트릭스 (Basic/Trend/Accent) 완성
- [ ] design-spec 연동 데이터 포함

## 체크리스트

- [ ] 로고 형태 변형 없이 위치·크기·기법 변형만 적용되었는가?
- [ ] 3B 착장 조합 배리에이션이 포함되어 있지 않은가?
- [ ] 라인(COVERNAT/AUTHENTIC/COLLEGE)별 무드 차별화가 반영되었는가?
- [ ] 씨빅 등 히어로 아이템이면 시즌 악센트 컬러 배리에이션 포함?
- [ ] BTA 가이드라인에 맞는 컬러웨이 구성인가?
- [ ] 페르소나 코어 타겟(UNISEX 20-27세, WOMEN 23-27세) 감성에 맞는가?
