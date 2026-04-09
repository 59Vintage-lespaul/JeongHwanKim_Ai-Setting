/**
 * 모자 기획방식 변경 — 비즈니스 보고 프레젠테이션 리빌드
 * run: node build_hat_pptx.js
 */
const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");

const IMG = "C:/Users/bcave/work/product-planning-md/scripts/matrix-convert/hat_images/";
const OUT = "C:/Users/bcave/Desktop/모자 기획방식 변경_리빌드.pptx";

// ── Design System ──────────────────────────────────────────────────────────
const C = {
  dark:      "0F172A",
  navy:      "1E3A5F",
  gold:      "C8952A",
  goldLight: "F0C155",
  white:     "FFFFFF",
  light:     "F7F8FA",
  grayBg:    "EEF0F3",
  grayLine:  "D1D5DB",
  gray:      "6B7280",
  grayDark:  "374151",
  basic:     "1E3A5F",
  trend:     "1B6340",
  accent:    "7B2131",
};

const F = { title: "Arial Black", head: "Calibri", body: "Calibri" };
const shadow = () => ({ type:"outer", color:"000000", blur:8, offset:2, angle:135, opacity:0.1 });

function img(n, ext="png") {
  return IMG + `image${n}.${ext}`;
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.3" × 7.5"
pres.title = "모자 기획방식 변경";
pres.author = "BKV MD";

// ── Shared Components ───────────────────────────────────────────────────────
function addSlideFrame(slide, num, title) {
  // Background
  slide.background = { color: C.light };

  // Header band
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0, y:0, w:13.3, h:0.82,
    fill:{ color:C.dark }, line:{ color:C.dark }
  });
  // Gold left strip
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0, y:0, w:0.07, h:7.5,
    fill:{ color:C.gold }, line:{ color:C.gold }
  });
  // Slide number (gold)
  slide.addText(String(num).padStart(2,"0"), {
    x:0.16, y:0, w:0.52, h:0.82,
    fontSize:22, fontFace:F.title, bold:true,
    color:C.goldLight, valign:"middle", margin:0
  });
  // Title
  slide.addText(title, {
    x:0.78, y:0, w:10.5, h:0.82,
    fontSize:22, fontFace:F.title, bold:true,
    color:C.white, valign:"middle", margin:0
  });
  // Footer label
  slide.addText("모자 기획방식 변경  ·  26SS", {
    x:10.5, y:0.28, w:2.7, h:0.25,
    fontSize:7, fontFace:F.body, color:C.gray, align:"right"
  });
  // Bottom line
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0, y:7.42, w:13.3, h:0.08,
    fill:{ color:C.gold }, line:{ color:C.gold }
  });
}

function addInsightCard(slide, x, y, w, h, num, label, body, color) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h, fill:{ color:C.white },
    line:{ color:C.grayLine, width:0.8 },
    shadow: shadow()
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w:0.06, h,
    fill:{ color:color }, line:{ color:color }
  });
  slide.addText(num, {
    x:x+0.12, y:y+0.08, w:0.6, h:0.28,
    fontSize:9, fontFace:F.body, bold:true, color:color, margin:0
  });
  slide.addText(label, {
    x:x+0.12, y:y+0.34, w:w-0.18, h:0.34,
    fontSize:11, fontFace:F.head, bold:true, color:C.dark, margin:0
  });
  slide.addText(body, {
    x:x+0.12, y:y+0.68, w:w-0.2, h:h-0.82,
    fontSize:9, fontFace:F.body, color:C.grayDark, margin:0, wrap:true
  });
}

function addBtaSection(slide, x, y, w, h, label, color, lines) {
  // Section background
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h, fill:{ color:C.white },
    line:{ color:C.grayLine, width:0.8 }, shadow:shadow()
  });
  // Top color band
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h:0.35, fill:{ color:color }, line:{ color:color }
  });
  // Label
  slide.addText(label, {
    x, y, w, h:0.35,
    fontSize:11, fontFace:F.title, bold:true,
    color:C.white, align:"center", valign:"middle", margin:0
  });
  // Content lines
  if (lines && lines.length > 0) {
    const items = lines.map((l, i) => ({
      text: l,
      options: { bullet:true, breakLine: i < lines.length - 1 }
    }));
    slide.addText(items, {
      x:x+0.1, y:y+0.42, w:w-0.18, h:h-0.5,
      fontSize:9, fontFace:F.body, color:C.grayDark, wrap:true, valign:"top"
    });
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// Slide 1 — 현황분석
// ═══════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  addSlideFrame(slide, 1, "현황분석");

  // ── Left panel: Observation Matrix ──────────────────────────────────────
  const panelW = 8.7;
  const rowY = [0.9, 2.5, 4.75];
  const rowH = [1.52, 2.1, 1.5];
  const rowLabels = ["외부시점", "제 품", "내부인원"];
  const rowColors = [C.navy, C.dark, C.grayDark];

  rowLabels.forEach((lbl, i) => {
    // Row background
    slide.addShape(pres.shapes.RECTANGLE, {
      x:0.12, y:rowY[i], w:panelW, h:rowH[i],
      fill:{ color:i===1?C.white:C.grayBg }, line:{ color:C.grayLine, width:0.6 }
    });
    // Row label tag
    slide.addShape(pres.shapes.RECTANGLE, {
      x:0.12, y:rowY[i], w:1.1, h:rowH[i],
      fill:{ color:rowColors[i] }, line:{ color:rowColors[i] }
    });
    slide.addText(lbl, {
      x:0.12, y:rowY[i], w:1.1, h:rowH[i],
      fontSize:11, fontFace:F.head, bold:true, color:C.white,
      align:"center", valign:"middle", margin:0
    });
  });

  // ── Row 0: 외부시점 — customer perception bubble ─────────────────────────
  // Speech bubble rect
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x:1.35, y:1.02, w:3.8, h:0.85,
    fill:{ color:"FEF9ED" }, line:{ color:C.gold, width:1.2 }, rectRadius:0.08,
    shadow:shadow()
  });
  slide.addText('"여긴 이걸 많이 파는 브랜드구나"', {
    x:1.42, y:1.08, w:3.7, h:0.75,
    fontSize:10.5, fontFace:F.body, italic:true,
    color:C.grayDark, valign:"middle", margin:0
  });
  slide.addText("소비자 시점", {
    x:1.35, y:1.02, w:1.2, h:0.28,
    fontSize:7, fontFace:F.body, bold:true, color:C.gold, margin:0
  });

  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x:5.4, y:1.0, w:3.15, h:0.9,
    fill:{ color:"FEF9ED" }, line:{ color:C.gold, width:1.2 }, rectRadius:0.08,
    shadow:shadow()
  });
  slide.addText('"소비자가 직관적으로 느낄 수 있는 변화 부족  →  재미없음  →  이탈"', {
    x:5.47, y:1.04, w:3.05, h:0.82,
    fontSize:9, fontFace:F.body, italic:true,
    color:C.grayDark, valign:"middle", wrap:true, margin:0
  });

  // ── Row 1: 제품 — 5 cap images ──────────────────────────────────────────
  const capImages = [1, 2, 3, 4, 5];
  const capLabels = ["스탠핏", "뉴스탠핏", "스탠슬림핏", "코지핏", "뉴코지핏"];
  const capX0 = 1.35;
  const capW = 1.4;
  const capGap = 0.05;
  capImages.forEach((n, i) => {
    const cx = capX0 + i * (capW + capGap);
    // Product image
    slide.addImage({
      path:img(n), x:cx, y:2.62, w:capW, h:1.5,
      sizing:{ type:"contain", w:capW, h:1.5 }
    });
    // Label
    slide.addShape(pres.shapes.RECTANGLE, {
      x:cx, y:2.56, w:capW, h:0.27,
      fill:{ color:C.dark }, line:{ color:C.dark }
    });
    slide.addText(capLabels[i], {
      x:cx, y:2.56, w:capW, h:0.27,
      fontSize:8.5, fontFace:F.body, bold:true, color:C.white,
      align:"center", valign:"middle", margin:0
    });
  });

  // Speech bubbles below product row
  const bubbles = [
    { x:1.35, text:"다팔았습니다\n리오더해주세요", color:"E8F5E9", border:C.trend },
    { x:4.25, text:"챙을 3mm 늘린\n신규 디자인입니다", color:C.grayBg, border:C.gray },
  ];
  bubbles.forEach(b => {
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x:b.x, y:4.2, w:2.6, h:0.48,
      fill:{ color:b.color }, line:{ color:b.border, width:0.8 }, rectRadius:0.06
    });
    slide.addText(b.text, {
      x:b.x+0.06, y:4.2, w:2.52, h:0.48,
      fontSize:8, fontFace:F.body, color:C.grayDark,
      valign:"middle", wrap:true, margin:0
    });
  });

  // ── Row 2: 내부인원 ──────────────────────────────────────────────────────
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x:1.35, y:4.87, w:4.8, h:0.75,
    fill:{ color:"FEF2F2" }, line:{ color:C.accent, width:1.2 }, rectRadius:0.08, shadow:shadow()
  });
  slide.addText('→  반성을 통해 \'개선\'을 해야 한다', {
    x:1.44, y:4.87, w:4.65, h:0.75,
    fontSize:11, fontFace:F.body, bold:true, italic:true,
    color:C.accent, valign:"middle", margin:0
  });

  // ── Right panel: Core Problems ───────────────────────────────────────────
  const rx = 8.95;
  addInsightCard(slide, rx, 0.9, 4.25, 1.55, "ISSUE 01",
    "핏(Fit) · 쉐입(Shape) 용어 혼용",
    "핏 = 볼캡의 착용 구조 (스탠/코지 등)\n쉐입 = 실루엣 형태 변화\n→ 개념 미분리로 기획 중복 발생",
    C.basic);

  addInsightCard(slide, rx, 2.55, 4.25, 1.6, "ISSUE 02",
    "신규 핏 개발 → 소비자 인식 한계",
    "변화를 개발해도 소비자가\n시각적으로 체감 불가능\n→ 소통 방식 개선 필요",
    C.trend);

  addInsightCard(slide, rx, 4.25, 4.25, 1.6, "ISSUE 03",
    "캐리오버 반복 → 중복 유형 누적",
    "판매 BEST → 캐리오버 → 부분 수정 반복\n→ 동일 유형 지속 누적\n→ 재미없음 → 소비자 이탈",
    C.accent);

  // ── 핏 vs 쉐입 개념 정의 박스 ───────────────────────────────────────────
  slide.addShape(pres.shapes.RECTANGLE, {
    x:rx, y:5.95, w:4.25, h:1.4,
    fill:{ color:C.dark }, line:{ color:C.dark }, shadow:shadow()
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x:rx, y:5.95, w:4.25, h:0.32,
    fill:{ color:C.gold }, line:{ color:C.gold }
  });
  slide.addText("핏 vs 쉐입  개념 정의", {
    x:rx, y:5.95, w:4.25, h:0.32,
    fontSize:9, fontFace:F.head, bold:true, color:C.dark,
    align:"center", valign:"middle", margin:0
  });
  slide.addText([
    { text:"핏(Fit)  ", options:{ bold:true, color:C.goldLight } },
    { text:"볼캡의 착용 구조 유형  (스탠 / 코지 계열)", options:{ color:C.white } },
    { text:"\n쉐입(Shape)  ", options:{ bold:true, color:C.goldLight } },
    { text:"실루엣 형태 변화  (캠프 / 5패널 / 뉴스보이 등)", options:{ color:C.white } },
  ], {
    x:rx+0.15, y:6.3, w:4.1, h:0.98,
    fontSize:9, fontFace:F.body, wrap:true, valign:"top", margin:0
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// Slide 2 — 기획 방식 구조화
// ═══════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  addSlideFrame(slide, 2, "기획 방식 구조화");

  // AS-IS block (left)
  const asX = 0.18, toX = 7.0;
  const panelY = 0.9, panelH = 5.9;

  // AS-IS panel
  slide.addShape(pres.shapes.RECTANGLE, {
    x:asX, y:panelY, w:6.5, h:panelH,
    fill:{ color:C.white }, line:{ color:C.grayLine, width:0.8 }, shadow:shadow()
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x:asX, y:panelY, w:6.5, h:0.42,
    fill:{ color:C.grayDark }, line:{ color:C.grayDark }
  });
  slide.addText("AS-IS  ·  현재 기획 방식", {
    x:asX, y:panelY, w:6.5, h:0.42,
    fontSize:12, fontFace:F.head, bold:true, color:C.white,
    align:"center", valign:"middle", margin:0
  });

  // AS-IS image (slide 2 main diagram image)
  slide.addImage({
    path:img("16_img"), x:asX+0.15, y:panelY+0.52, w:6.2, h:3.2,
    sizing:{ type:"contain", w:6.2, h:3.2 }
  });

  // AS-IS problems
  const asProblems = [
    "전년도 판매 확인 → BEST 캐리오버 or 부분 수정 반복",
    "기획 단계에서 BTA 비율 통제 불가",
    "어느 유형을 진행하지 않았는지 확인 불가",
  ];
  const asItems = asProblems.map((t, i) => ({
    text:`${t}`,
    options: { bullet:true, breakLine: i < asProblems.length-1, color:C.accent }
  }));
  slide.addText(asItems, {
    x:asX+0.15, y:panelY+3.85, w:6.2, h:1.95,
    fontSize:10, fontFace:F.body, color:C.grayDark, wrap:true, valign:"top"
  });

  // Arrow
  slide.addShape(pres.shapes.RECTANGLE, {
    x:6.74, y:3.2, w:0.26, h:0.5,
    fill:{ color:C.gold }, line:{ color:C.gold }
  });
  slide.addText("→", {
    x:6.58, y:3.1, w:0.5, h:0.7,
    fontSize:22, fontFace:F.title, bold:true, color:C.gold,
    align:"center", valign:"middle", margin:0
  });

  // TO-BE panel
  slide.addShape(pres.shapes.RECTANGLE, {
    x:toX, y:panelY, w:6.15, h:panelH,
    fill:{ color:C.white }, line:{ color:C.grayLine, width:0.8 }, shadow:shadow()
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x:toX, y:panelY, w:6.15, h:0.42,
    fill:{ color:C.navy }, line:{ color:C.navy }
  });
  slide.addText("TO-BE  ·  개선 기획 방식", {
    x:toX, y:panelY, w:6.15, h:0.42,
    fontSize:12, fontFace:F.head, bold:true, color:C.white,
    align:"center", valign:"middle", margin:0
  });

  // TO-BE image
  slide.addImage({
    path:img("17_img"), x:toX+0.15, y:panelY+0.52, w:5.85, h:3.2,
    sizing:{ type:"contain", w:5.85, h:3.2 }
  });

  // TO-BE improvements
  const improvements = [
    "기획 단계에서 전체 구조 파악 후 스타일 가부 판단",
    "BTA 비율 실시간 통제 가능 (놓치는 유형 → 의도적 미진행)",
    "핏 · 쉐입 용어 구분 사용 → 중복 스타일 방지",
  ];
  const toItems = improvements.map((t, i) => ({
    text:t,
    options: { bullet:true, breakLine: i < improvements.length-1, color:C.trend }
  }));
  slide.addText(toItems, {
    x:toX+0.15, y:panelY+3.85, w:5.85, h:1.95,
    fontSize:10, fontFace:F.body, color:C.grayDark, wrap:true, valign:"top"
  });

  // Bottom summary bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0.12, y:6.88, w:13.1, h:0.5,
    fill:{ color:C.dark }, line:{ color:C.dark }
  });
  slide.addText("핵심 원칙:  핏 확장은 신중하게  ·  쉐입 확장은 유동적으로  |  기획 단계 BTA 비율 실시간 점검", {
    x:0.12, y:6.88, w:13.1, h:0.5,
    fontSize:10, fontFace:F.head, bold:true, color:C.goldLight,
    align:"center", valign:"middle", margin:0
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// Slide 3 — 전면 로고 표현
// ═══════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  addSlideFrame(slide, 3, "전면 로고 표현");

  // Context box
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0.18, y:0.92, w:13.0, h:0.62,
    fill:{ color:C.white }, line:{ color:C.grayLine, width:0.8 }
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0.18, y:0.92, w:0.06, h:0.62,
    fill:{ color:C.gold }, line:{ color:C.gold }
  });
  slide.addText("모자 전면 로고 표현방식 지속 업데이트  ·  연도별 신규 공정 및 표현방식 아카이빙", {
    x:0.32, y:0.92, w:12.8, h:0.62,
    fontSize:11, fontFace:F.head, color:C.grayDark, valign:"middle", margin:0
  });

  // Two images side by side
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0.18, y:1.65, w:6.35, h:5.6,
    fill:{ color:C.white }, line:{ color:C.grayLine, width:0.8 }, shadow:shadow()
  });
  slide.addImage({
    path:img(19), x:0.3, y:1.72, w:6.1, h:5.4,
    sizing:{ type:"contain", w:6.1, h:5.4 }
  });

  slide.addShape(pres.shapes.RECTANGLE, {
    x:6.65, y:1.65, w:6.5, h:5.6,
    fill:{ color:C.white }, line:{ color:C.grayLine, width:0.8 }, shadow:shadow()
  });
  slide.addImage({
    path:img(20), x:6.78, y:1.72, w:6.24, h:5.4,
    sizing:{ type:"contain", w:6.24, h:5.4 }
  });

  // Caption
  slide.addText("좌: 연도별 표현방식 아카이브     우: 신규 공정 개발 레퍼런스", {
    x:0.18, y:7.25, w:13.0, h:0.2,
    fontSize:8, fontFace:F.body, color:C.gray, align:"center", margin:0
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// Slide 4 — 시장 상황 및 경쟁사 분석
// ═══════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  addSlideFrame(slide, 4, "시장 상황 및 경쟁사 분석");

  // Key insight banner
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0.18, y:0.92, w:13.0, h:0.62,
    fill:{ color:C.navy }, line:{ color:C.navy }
  });
  slide.addText("트렌드 키워드:  언스트럭처 볼캡 핏 세분화  →  다양한 쉐입 · 로고표현 · 소재 다양화 트렌드로 이동", {
    x:0.3, y:0.92, w:12.85, h:0.62,
    fontSize:11, fontFace:F.head, bold:true, color:C.white, valign:"middle", margin:0
  });

  // Main competitor image
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0.18, y:1.65, w:13.0, h:5.65,
    fill:{ color:C.white }, line:{ color:C.grayLine, width:0.8 }, shadow:shadow()
  });
  slide.addImage({
    path:img(21), x:0.22, y:1.68, w:12.92, h:5.6,
    sizing:{ type:"contain", w:12.92, h:5.6 }
  });

  // Caption
  slide.addText("경쟁사 언스트럭처드 볼캡 라인업 분석  |  쉐입 다양화 · 소재 실험 · 로고 그래픽 업데이트", {
    x:0.18, y:7.26, w:13.0, h:0.18,
    fontSize:8, fontFace:F.body, color:C.gray, align:"center", margin:0
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// Slide 5 — 커버낫 기획 방식
// ═══════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  addSlideFrame(slide, 5, "커버낫 기획 방식");

  // Summary bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0.18, y:0.92, w:13.0, h:0.62,
    fill:{ color:C.white }, line:{ color:C.grayLine, width:0.8 }
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0.18, y:0.92, w:0.06, h:0.62,
    fill:{ color:C.gold }, line:{ color:C.gold }
  });
  slide.addText("기존 베이직캡 3~4개 → 2개 압축 (재고소진 우선)  ·  시즌별 4~5개 쉐입 전개  ·  쉐입별 최적 C로고 표현방식 개발", {
    x:0.32, y:0.92, w:12.8, h:0.62,
    fontSize:10, fontFace:F.body, color:C.grayDark, valign:"middle", margin:0
  });

  // 핏/쉐입 axis labels
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0.18, y:1.64, w:1.0, h:5.6,
    fill:{ color:C.dark }, line:{ color:C.dark }
  });
  slide.addText(["핏\n(FIT)"].join(""), {
    x:0.18, y:2.8, w:1.0, h:1.2,
    fontSize:13, fontFace:F.title, bold:true, color:C.white,
    align:"center", valign:"middle", margin:0
  });
  slide.addText("축소·압축", {
    x:0.18, y:4.1, w:1.0, h:0.55,
    fontSize:8, fontFace:F.body, color:C.goldLight, align:"center", margin:0
  });
  slide.addText("↓", {
    x:0.18, y:4.6, w:1.0, h:0.4,
    fontSize:14, fontFace:F.body, color:C.goldLight, align:"center", margin:0
  });

  // BTA columns
  const colX = [1.28, 5.18, 9.02];
  const colW = 3.78;
  const btaData = [
    {
      label:"BASIC", color:C.basic,
      lines:["볼캡 2개 핏으로 압축", "재고소진 우선 전략", "안정 매출 유지"],
      imgNums:[22, 22],
    },
    {
      label:"TREND", color:C.trend,
      lines:["시즌별 4~5개 쉐입 전개", "캠프캡 / 5패널 / 뉴스보이", "쉐입별 최적 C로고 표현"],
      imgNums:[23, 24],
    },
    {
      label:"ACCENT", color:C.accent,
      lines:["아이캐칭 실험적 쉐입", "한정 수량 / 콜라보 연계", "시즌 임팩트 강화"],
      imgNums:[25, 26],
    },
  ];

  btaData.forEach((d, i) => {
    const cx = colX[i];
    // Section box
    slide.addShape(pres.shapes.RECTANGLE, {
      x:cx, y:1.64, w:colW, h:5.6,
      fill:{ color:C.white }, line:{ color:C.grayLine, width:0.8 }, shadow:shadow()
    });
    // Header
    slide.addShape(pres.shapes.RECTANGLE, {
      x:cx, y:1.64, w:colW, h:0.42,
      fill:{ color:d.color }, line:{ color:d.color }
    });
    slide.addText(d.label, {
      x:cx, y:1.64, w:colW, h:0.42,
      fontSize:13, fontFace:F.title, bold:true, color:C.white,
      align:"center", valign:"middle", margin:0
    });
    // Images
    d.imgNums.forEach((n, j) => {
      const iw = (colW - 0.2) / 2;
      slide.addImage({
        path:img(n), x:cx+0.05+(j*(iw+0.1)), y:2.12, w:iw, h:2.05,
        sizing:{ type:"contain", w:iw, h:2.05 }
      });
    });
    // Text lines
    const textItems = d.lines.map((l, k) => ({
      text:l, options:{ bullet:true, breakLine: k < d.lines.length-1 }
    }));
    slide.addText(textItems, {
      x:cx+0.1, y:4.26, w:colW-0.18, h:2.9,
      fontSize:9.5, fontFace:F.body, color:C.grayDark, wrap:true, valign:"top"
    });
  });

  // 쉐입 arrow label (horizontal)
  slide.addShape(pres.shapes.RECTANGLE, {
    x:1.28, y:7.18, w:11.52, h:0.2,
    fill:{ color:C.gold }, line:{ color:C.gold }
  });
  slide.addText("← BASIC (안정매출)          TREND (매출+감도)          ACCENT (아이캐칭·실험) →     쉐입(SHAPE) 확장 →", {
    x:1.28, y:7.2, w:11.52, h:0.22,
    fontSize:8, fontFace:F.body, color:C.grayDark, align:"center", margin:0
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// Slide 6 — 리(LEE) 기획 방식
// ═══════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  addSlideFrame(slide, 6, "리(LEE) 기획 방식");

  // Summary bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0.18, y:0.92, w:13.0, h:0.62,
    fill:{ color:C.white }, line:{ color:C.grayLine, width:0.8 }
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0.18, y:0.92, w:0.06, h:0.62,
    fill:{ color:C.gold }, line:{ color:C.gold }
  });
  slide.addText("기본 볼캡 3개 핏 → 2개 핏 압축  ·  트렌드 NEW 고정 쉐입 전개  ·  LEE 아카이브 제품 구성", {
    x:0.32, y:0.92, w:12.8, h:0.62,
    fontSize:10, fontFace:F.body, color:C.grayDark, valign:"middle", margin:0
  });

  // 핏 axis label
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0.18, y:1.64, w:1.0, h:5.6,
    fill:{ color:C.dark }, line:{ color:C.dark }
  });
  slide.addText("핏\n(FIT)", {
    x:0.18, y:2.8, w:1.0, h:1.2,
    fontSize:13, fontFace:F.title, bold:true, color:C.white,
    align:"center", valign:"middle", margin:0
  });
  slide.addText("축소·압축", {
    x:0.18, y:4.1, w:1.0, h:0.55,
    fontSize:8, fontFace:F.body, color:C.goldLight, align:"center", margin:0
  });

  const colX = [1.28, 5.18, 9.02];
  const colW = 3.78;
  const btaData = [
    {
      label:"BASIC", color:C.basic,
      lines:["볼캡 3개 → 2개 핏 압축", "기본 실루엣 안정화", "안정 매출 기반 유지"],
      imgs:[27, 28],
    },
    {
      label:"TREND", color:C.trend,
      lines:["NEW 고정 쉐입 시즌별 전개", "트렌드 반영 실루엣 업데이트", "매출+감도 동시 달성"],
      imgs:[29, 30],
    },
    {
      label:"ACCENT\n+ Archive", color:C.accent,
      lines:["LEE 아카이브 제품 구성 필요", "브랜드 헤리티지 강조", "한정 수량 · 팬덤 대상"],
      imgs:[31, 32],
    },
  ];

  btaData.forEach((d, i) => {
    const cx = colX[i];
    slide.addShape(pres.shapes.RECTANGLE, {
      x:cx, y:1.64, w:colW, h:5.6,
      fill:{ color:C.white }, line:{ color:C.grayLine, width:0.8 }, shadow:shadow()
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x:cx, y:1.64, w:colW, h:0.42,
      fill:{ color:d.color }, line:{ color:d.color }
    });
    slide.addText(d.label, {
      x:cx, y:1.64, w:colW, h:0.42,
      fontSize:12, fontFace:F.title, bold:true, color:C.white,
      align:"center", valign:"middle", margin:0
    });
    d.imgs.forEach((n, j) => {
      const iw = (colW - 0.2) / 2;
      slide.addImage({
        path:img(n), x:cx+0.05+(j*(iw+0.1)), y:2.12, w:iw, h:2.05,
        sizing:{ type:"contain", w:iw, h:2.05 }
      });
    });
    const textItems = d.lines.map((l, k) => ({
      text:l, options:{ bullet:true, breakLine: k < d.lines.length-1 }
    }));
    slide.addText(textItems, {
      x:cx+0.1, y:4.26, w:colW-0.18, h:2.9,
      fontSize:9.5, fontFace:F.body, color:C.grayDark, wrap:true, valign:"top"
    });
  });

  // LEE archive highlight
  slide.addShape(pres.shapes.RECTANGLE, {
    x:9.02, y:5.8, w:3.78, h:1.3,
    fill:{ color:"FEF9ED" }, line:{ color:C.gold, width:1.2 }
  });
  slide.addImage({
    path:img(33, "jpeg"), x:9.1, y:5.85, w:1.4, h:1.15,
    sizing:{ type:"contain", w:1.4, h:1.15 }
  });
  slide.addText("Archive\n아카이브 제품: LEE 헤리티지 기반\n팬덤 · 콜라보 · 리미티드", {
    x:10.6, y:5.85, w:2.1, h:1.1,
    fontSize:8.5, fontFace:F.body, color:C.grayDark, wrap:true, valign:"top", margin:0
  });

  // 쉐입 arrow
  slide.addShape(pres.shapes.RECTANGLE, {
    x:1.28, y:7.18, w:11.52, h:0.2,
    fill:{ color:C.gold }, line:{ color:C.gold }
  });
  slide.addText("← BASIC (안정매출)          TREND (매출+감도)          ACCENT + Archive (실험·헤리티지) →     쉐입(SHAPE) 확장 →", {
    x:1.28, y:7.2, w:11.52, h:0.22,
    fontSize:8, fontFace:F.body, color:C.grayDark, align:"center", margin:0
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// Slide 7 — 와키윌리 기획 방식
// ═══════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  addSlideFrame(slide, 7, "와키윌리 기획 방식");

  // Summary bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0.18, y:0.92, w:13.0, h:0.62,
    fill:{ color:C.white }, line:{ color:C.grayLine, width:0.8 }
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0.18, y:0.92, w:0.06, h:0.62,
    fill:{ color:C.gold }, line:{ color:C.gold }
  });
  slide.addText("기본볼캡 2개 핏 → 1개 핏 축소  ·  트렌드/악센트 쉐입 가장 적극적 확장  ·  트렌디·키치 브랜드 인식 변화 1순위", {
    x:0.32, y:0.92, w:12.8, h:0.62,
    fontSize:10, fontFace:F.body, color:C.grayDark, valign:"middle", margin:0
  });

  // 핏 axis label
  slide.addShape(pres.shapes.RECTANGLE, {
    x:0.18, y:1.64, w:1.0, h:5.6,
    fill:{ color:C.dark }, line:{ color:C.dark }
  });
  slide.addText("핏\n(FIT)", {
    x:0.18, y:2.8, w:1.0, h:1.2,
    fontSize:13, fontFace:F.title, bold:true, color:C.white,
    align:"center", valign:"middle", margin:0
  });
  slide.addText("최소화", {
    x:0.18, y:4.1, w:1.0, h:0.55,
    fontSize:8, fontFace:F.body, color:C.goldLight, align:"center", margin:0
  });

  // BTA columns - WW has narrower BASIC, wider ACCENT
  const colDefs = [
    { label:"BASIC", color:C.basic, x:1.28, w:2.9,
      lines:["볼캡 1개 핏으로 최소화", "안정 매출 기반만 유지", "불필요한 중복 정리"],
      imgs:[35] },
    { label:"TREND", color:C.trend, x:4.28, w:3.6,
      lines:["트렌디 쉐입 적극 전개", "시즌별 뉴 쉐입 2~3개 추가", "매출+브랜드 감도 동시 달성"],
      imgs:[36, 37] },
    { label:"ACCENT", color:C.accent, x:7.98, w:5.2,
      lines:["키치·실험적 쉐입 최대 확장", "트렌디 모자 브랜드 인식 변화 1순위", "표현방식 다양화 (소재·그래픽·공정)", "콜라보·캡슐 연계"],
      imgs:[38, 39, 35] },
  ];

  colDefs.forEach(d => {
    slide.addShape(pres.shapes.RECTANGLE, {
      x:d.x, y:1.64, w:d.w, h:5.6,
      fill:{ color:C.white }, line:{ color:C.grayLine, width:0.8 }, shadow:shadow()
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x:d.x, y:1.64, w:d.w, h:0.42,
      fill:{ color:d.color }, line:{ color:d.color }
    });
    slide.addText(d.label, {
      x:d.x, y:1.64, w:d.w, h:0.42,
      fontSize:12, fontFace:F.title, bold:true, color:C.white,
      align:"center", valign:"middle", margin:0
    });
    const perImg = (d.w - 0.15) / d.imgs.length;
    d.imgs.forEach((n, j) => {
      slide.addImage({
        path:img(n), x:d.x+0.05+j*(perImg+0.05), y:2.12, w:perImg, h:2.1,
        sizing:{ type:"contain", w:perImg, h:2.1 }
      });
    });
    const textItems = d.lines.map((l, k) => ({
      text:l, options:{ bullet:true, breakLine: k < d.lines.length-1 }
    }));
    slide.addText(textItems, {
      x:d.x+0.1, y:4.3, w:d.w-0.18, h:2.85,
      fontSize:9.5, fontFace:F.body, color:C.grayDark, wrap:true, valign:"top"
    });
  });

  // WW main image (brand mood image)
  slide.addImage({
    path:img(40), x:1.28, y:6.5, w:11.9, h:0.6,
    sizing:{ type:"cover", w:11.9, h:0.6 }
  });

  // 쉐입 arrow
  slide.addShape(pres.shapes.RECTANGLE, {
    x:1.28, y:7.18, w:11.52, h:0.22,
    fill:{ color:C.gold }, line:{ color:C.gold }
  });
  slide.addText("← BASIC (최소)     TREND (적극 확장)     ACCENT (최대 확장 · 키치 브랜드 차별화) →     쉐입(SHAPE) →", {
    x:1.28, y:7.2, w:11.52, h:0.22,
    fontSize:8, fontFace:F.body, color:C.grayDark, align:"center", margin:0
  });
}

// ─── Save ──────────────────────────────────────────────────────────────────
pres.writeFile({ fileName: OUT })
  .then(() => console.log("Saved: " + OUT))
  .catch(e => console.error("Error:", e));
