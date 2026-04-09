import openpyxl, json
from collections import defaultdict

wb = openpyxl.load_workbook(r'C:\Users\bcave\Desktop\브랜드별 신발 출고 비교_분류완성.xlsx', data_only=True)
ws = wb['브랜드별 신발 출고 비교']

rows = []
for row in ws.iter_rows(min_row=3, values_only=True):
    if row[0] is None: continue
    store, item_code, brand, cat1, cat2 = row[0], row[1], row[2], row[3], row[4]
    item_name = row[5]
    cum_sale = row[8]
    bm = {'CO':'커버낫', 'LE':'리(LEE)', 'WA':'와키윌리'}
    brand_kr = bm.get(str(brand).strip(), str(brand).strip()) if brand else '기타'
    if cat2 == '뺶': cat2 = '백화점'
    item_str = str(item_name) if item_name else ''
    prod_type = '스니커즈' if any(k in item_str for k in ['스니커즈','LITE','Lite','키테','솔레보 스니커즈']) else '슬라이드'
    sale = int(cum_sale) if cum_sale and str(cum_sale) not in ('None','') else 0
    rows.append({'store':store,'brand':brand_kr,'cat1':str(cat1) if cat1 else '','cat2':str(cat2) if cat2 else '','item':item_str,'prod_type':prod_type,'sale':sale})

brands = ['커버낫','리(LEE)','와키윌리']
brand_en = {'커버낫':'COVERNAT','리(LEE)':'LEE','와키윌리':'WACKY WILLY'}
brand_color_main = {'커버낫':'#1D3557','리(LEE)':'#1B6B3A','와키윌리':'#6B21A8'}
brand_color_light = {'커버낫':'#EFF6FF','리(LEE)':'#F0FDF4','와키윌리':'#FAF5FF'}

CHANNEL_COLORS = {
    '온라인':'#3B82F6','오프라인':'#F59E0B','플래그쉽':'#8B5CF6',
    '위탁/사입':'#10B981','해외':'#EF4444','기타':'#9CA3AF'
}
PROD_COLORS = {'슬라이드':'#3B82F6','스니커즈':'#F59E0B'}

def pct(val, total):
    return round(val/total*100, 1) if total>0 else 0

def pie_js(canvas_id, labels, values, colors, legend=True):
    total = sum(values)
    pct_vals = [pct(v, total) for v in values]
    cols = json.dumps(colors[:len(labels)])
    lbls = json.dumps(labels)
    vals = json.dumps(values)
    legend_str = 'true' if legend else 'false'
    pct_json = json.dumps(pct_vals)
    return f"""
new Chart(document.getElementById('{canvas_id}'), {{
  type: 'pie',
  data: {{
    labels: {lbls},
    datasets: [{{ data: {vals}, backgroundColor: {cols}, borderWidth: 2, borderColor: '#fff' }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{
      legend: {{ display: {legend_str}, position: 'bottom', labels: {{ font: {{ size: 11, family: 'Noto Sans KR, sans-serif' }}, padding: 8, boxWidth: 12 }} }},
      tooltip: {{ callbacks: {{ label: function(ctx) {{ var p={pct_json}; return ctx.label + ': ' + ctx.parsed.toLocaleString() + '개 (' + p[ctx.dataIndex] + '%)'; }} }} }}
    }}
  }}
}});"""

# ── 데이터 집계 ──
def offline_breakdown(brand):
    sub = defaultdict(set)
    for r in rows:
        if r['brand']==brand and r['cat1'] in ('오프라인','플래그쉽') and r['sale']>0:
            sub[r['cat2']].add(r['store'])
    return {k:len(v) for k,v in sub.items()}

def offline_breakdown_by_prod(brand, prod_type):
    """product type별 오프라인 매장 수 (cat2 기준)"""
    sub = defaultdict(set)
    for r in rows:
        if r['brand']==brand and r['cat1'] in ('오프라인','플래그쉽') and r['sale']>0 and r['prod_type']==prod_type:
            sub[r['cat2']].add(r['store'])
    return {k:len(v) for k,v in sub.items()}

def offline_sales_by_prod(brand, prod_type):
    """product type별 오프라인 채널(1차) 판매 집계"""
    d = defaultdict(int)
    for r in rows:
        if r['brand']==brand and r['cat1'] in ('오프라인','플래그쉽') and r['prod_type']==prod_type:
            d[r['cat1']] += r['sale']
    return dict(d)

def channel_sales(brand):
    d = defaultdict(int)
    for r in rows:
        if r['brand']==brand and r['cat1'] not in ('기타',):
            d[r['cat1']] += r['sale']
    return dict(d)

def online_channels(brand):
    d = defaultdict(int)
    stores = set()
    for r in rows:
        if r['brand']==brand and r['cat1']=='온라인' and r['sale']>0:
            d[r['cat2']] += r['sale']
            stores.add(r['store'])
    return dict(d), len(stores)

def cat2_prods():
    d = defaultdict(lambda: defaultdict(int))
    for r in rows:
        if r['cat1'] not in ('기타',):
            d[r['cat2']][r['prod_type']] += r['sale']
    return {k:dict(v) for k,v in d.items() if sum(v.values())>0}

def brand_prods(brand):
    d = defaultdict(int)
    for r in rows:
        if r['brand']==brand:
            d[r['prod_type']] += r['sale']
    return dict(d)

data = {}
for b in brands:
    ob = offline_breakdown(b)
    cs = channel_sales(b)
    oc, ocnt = online_channels(b)
    bp = brand_prods(b)
    data[b] = {
        'offline_breakdown': ob,
        'offline_total': sum(ob.values()),
        'channel_sales': cs,
        'total_sale': sum(cs.values()),
        'online_channels': oc,
        'online_channel_count': ocnt,
        'brand_prods': bp,
    }
cp = cat2_prods()

scripts = []

# ── HTML 빌드 ──
html = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>브랜드별 신발 출고판매 비교 보고서</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Noto Sans KR',sans-serif;background:#F8FAFC;color:#1E293B;font-size:14px;line-height:1.5}
.page{max-width:1200px;margin:0 auto;padding:32px 24px 64px}
.report-header{background:#1D3557;color:#fff;border-radius:12px;padding:36px 40px;margin-bottom:32px;display:flex;justify-content:space-between;align-items:flex-end}
.report-header h1{font-size:22px;font-weight:700;letter-spacing:-.5px;margin-bottom:6px}
.report-header .subtitle{font-size:13px;opacity:.75}
.report-header .meta{text-align:right;font-size:12px;opacity:.7;line-height:2}
.summary-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:32px}
.s-card{background:#fff;border-radius:10px;padding:20px 24px;border-top:4px solid var(--c);box-shadow:0 1px 4px rgba(0,0,0,.06)}
.s-card .brand{font-size:11px;font-weight:700;color:var(--c);text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px}
.s-card .big{font-size:26px;font-weight:700;color:#0F172A;margin-bottom:4px}
.s-card .label{font-size:11px;color:#64748B}
.s-card .metrics{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:14px;padding-top:14px;border-top:1px solid #F1F5F9}
.s-card .m-item .val{font-size:15px;font-weight:600;color:#1E293B}
.s-card .m-item .lbl{font-size:10px;color:#94A3B8;margin-top:1px}
.section{margin-bottom:40px}
.section-title{font-size:15px;font-weight:700;color:#0F172A;margin-bottom:4px;display:flex;align-items:center;gap:8px}
.section-title::before{content:'';display:inline-block;width:4px;height:18px;background:#1D3557;border-radius:2px}
.section-desc{font-size:12px;color:#64748B;margin-bottom:16px;padding-left:12px}
.brand-row{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:16px}
.brand-card{background:#fff;border-radius:10px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,.06)}
.b-header{display:flex;align-items:center;gap:8px;margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid #F1F5F9}
.b-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.b-name{font-size:13px;font-weight:700;color:#0F172A}
.b-en{font-size:10px;color:#94A3B8;margin-left:auto}
.chart-wrap{position:relative;height:180px;margin-bottom:8px}
.tbl-wrap{overflow-x:auto;margin-bottom:16px}
table{width:100%;border-collapse:collapse;font-size:13px}
th{background:#F8FAFC;padding:8px 12px;text-align:left;font-weight:600;color:#475569;border-bottom:2px solid #E2E8F0;white-space:nowrap}
td{padding:8px 12px;border-bottom:1px solid #F1F5F9;color:#1E293B}
tr:last-child td{border-bottom:none}
.num{text-align:right;font-variant-numeric:tabular-nums}
.ch-grid{display:grid;gap:12px;margin-bottom:16px}
.ch-card{background:#fff;border-radius:10px;padding:16px 14px;box-shadow:0 1px 4px rgba(0,0,0,.06)}
.ch-title{font-size:12px;font-weight:700;color:#475569;margin-bottom:10px;text-align:center}
.chart-sm{position:relative;height:150px;margin-bottom:6px}
.legend-list{font-size:11px;color:#475569}
.legend-list .li{display:flex;justify-content:space-between;padding:2px 0}
.legend-list .li .dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:5px;flex-shrink:0}
.legend-list .li .lname{flex:1}
.legend-list .li .lpct{font-weight:600;color:#1E293B}
.insight{background:#EFF6FF;border-left:4px solid #3B82F6;border-radius:0 8px 8px 0;padding:12px 16px;margin-top:12px;font-size:12px;color:#1E40AF;line-height:1.9}
.divider{height:1px;background:#E2E8F0;margin:32px 0}
</style>
</head>
<body>
<div class="page">
"""

# HEADER
html += """<div class="report-header">
  <div>
    <div class="subtitle">브랜드별 신발 출고판매 분석</div>
    <h1>신발 채널별 판매 비중 &amp; 제품 구성 보고서</h1>
    <div class="subtitle" style="margin-top:6px">커버낫 &middot; 리(LEE) &middot; 와키윌리 — 누계 실판매수량 기준</div>
  </div>
  <div class="meta">
    <div>기준: 누계 실판매수량</div>
    <div>분석 범위: 브랜드별 신발 출고 비교 시트</div>
    <div>작성일: 2026년 4월 1일</div>
  </div>
</div>
"""

# SUMMARY CARDS
html += '<div class="summary-grid">\n'
for b in brands:
    d = data[b]
    total = d['total_sale']
    offline_t = d['offline_total']
    online_cnt = d['online_channel_count']
    c = brand_color_main[b]
    bp = d['brand_prods']
    slide_r = pct(bp.get('슬라이드',0), total)
    sneak_r = pct(bp.get('스니커즈',0), total)
    cs = d['channel_sales']
    top_ch = max(cs, key=cs.get) if cs else '-'
    top_p = pct(cs.get(top_ch,0), total)
    html += f"""<div class="s-card" style="--c:{c}">
  <div class="brand">{b} &nbsp;&middot;&nbsp; {brand_en[b]}</div>
  <div class="big">{total:,}<span style="font-size:14px;font-weight:400;color:#64748B"> 개</span></div>
  <div class="label">누계 실판매 총수량</div>
  <div class="metrics">
    <div class="m-item"><div class="val">{offline_t}</div><div class="lbl">오프라인 운영 매장</div></div>
    <div class="m-item"><div class="val">{online_cnt}개</div><div class="lbl">온라인 채널 수</div></div>
    <div class="m-item"><div class="val">{slide_r}%</div><div class="lbl">슬라이드 비중</div></div>
    <div class="m-item"><div class="val">{sneak_r}%</div><div class="lbl">스니커즈 비중</div></div>
  </div>
</div>\n"""
html += '</div>\n<div class="divider"></div>\n'

# ── SEC 1: 오프라인 현황 ──
html += """<div class="section">
<div class="section-title">오프라인 운영 현황</div>
<div class="section-desc">1차분류 오프라인 + 플래그쉽 기준. 실판매 발생 매장만 집계. 스니커즈 운영 / 슬라이드 포함 운영으로 구분.</div>
"""

cat_order_off = ['백화점','아울렛','면세점','플래그쉽','로드샵','무신사']
SNEAKER_COLOR = '#F59E0B'
SLIDE_COLOR   = '#3B82F6'

for prod_type, prod_label, prod_color, prod_desc in [
    ('스니커즈', '스니커즈 운영 매장 현황', SNEAKER_COLOR, '스니커즈(키테·솔레보 스니커즈 등) 실판매 발생 오프라인 매장'),
    ('슬라이드', '슬라이드 포함 운영 매장 현황', SLIDE_COLOR,  '슬라이드(슬라이드·플립플랍·메리제인 등) 실판매 발생 오프라인 매장'),
]:
    html += f'<h3 style="font-size:13px;font-weight:700;color:#fff;background:{prod_color};display:inline-block;padding:4px 12px;border-radius:20px;margin-bottom:10px">{prod_label}</h3>\n'
    html += f'<p style="font-size:12px;color:#64748B;margin-bottom:10px">{prod_desc}</p>\n'
    html += '<div class="tbl-wrap"><table>\n'
    html += '<tr><th>브랜드</th><th class="num">백화점</th><th class="num">아울렛</th><th class="num">면세점</th><th class="num">플래그쉽</th><th class="num">로드샵</th><th class="num">무신사</th><th class="num">합계</th></tr>\n'
    for b in brands:
        ob = offline_breakdown_by_prod(b, prod_type)
        total_off = sum(ob.values())
        c = brand_color_main[b]
        def cell_val(n):
            return str(n) if n>0 else '<span style="color:#CBD5E1">—</span>'
        cells = ''.join(f'<td class="num">{cell_val(ob.get(cat,0))}</td>' for cat in cat_order_off)
        total_cell = f'<strong>{total_off}</strong>' if total_off>0 else '<span style="color:#CBD5E1">—</span>'
        html += f'<tr><td><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:{c};margin-right:6px"></span><strong>{b}</strong></td>{cells}<td class="num">{total_cell}</td></tr>\n'
    html += '</table></div>\n'

    # 파이차트 (브랜드별 오프라인 채널 판매 비중 — 해당 품목)
    html += '<div class="brand-row" style="margin-bottom:24px">\n'
    for bi, b in enumerate(brands):
        # 해당 prod_type의 오프라인 2차분류별 판매
        sub_sale = defaultdict(int)
        for r in rows:
            if r['brand']==b and r['cat1'] in ('오프라인','플래그쉽') and r['prod_type']==prod_type and r['sale']>0:
                sub_sale[r['cat2']] += r['sale']
        if not sub_sale:
            html += f'<div class="brand-card"><div class="b-header"><div class="b-dot" style="background:{brand_color_main[b]}"></div><div class="b-name">{b}</div></div><p style="color:#94A3B8;font-size:12px;text-align:center;padding:30px 0">데이터 없음</p></div>\n'
            continue
        s_total = sum(sub_sale.values())
        labels = list(sub_sale.keys())
        vals = list(sub_sale.values())
        off_pal = ['#F59E0B','#FB923C','#A78BFA','#8B5CF6','#34D399','#111827']
        cols_c = off_pal[:len(labels)]
        cid = f'pie_off_{prod_type}_{bi}'
        legend_rows = ''.join(
            f'<div class="li"><span><span class="dot" style="background:{off_pal[i%len(off_pal)]}"></span><span class="lname">{l}</span></span><span class="lpct">{pct(v,s_total)}%</span></div>'
            for i,(l,v) in enumerate(sorted(sub_sale.items(), key=lambda x:-x[1]))
        )
        html += f"""<div class="brand-card">
  <div class="b-header"><div class="b-dot" style="background:{brand_color_main[b]}"></div>
    <div class="b-name">{b}</div><div class="b-en">{prod_type} 오프라인 채널</div></div>
  <div class="chart-wrap"><canvas id="{cid}"></canvas></div>
  <div class="legend-list">{legend_rows}</div>
</div>\n"""
        scripts.append(pie_js(cid, labels, vals, cols_c, legend=False))
    html += '</div>\n'

# 전체 채널 구성 파이차트 (1차분류, 참고용)
html += '<h3 style="font-size:13px;font-weight:600;color:#475569;margin:4px 0 12px;padding-left:12px">&#9658; 전체 채널 판매 비중 (1차분류 기준, 참고)</h3>\n'
html += '<div class="brand-row">\n'
for bi, b in enumerate(brands):
    cs = data[b]['channel_sales']
    total = data[b]['total_sale']
    labels = list(cs.keys())
    vals = list(cs.values())
    cols_c = [CHANNEL_COLORS.get(l,'#CBD5E1') for l in labels]
    cid = f'pie_ch_{bi}'
    legend_rows = ''.join(
        f'<div class="li"><span><span class="dot" style="background:{CHANNEL_COLORS.get(l,"#CBD5E1")}"></span><span class="lname">{l}</span></span><span class="lpct">{pct(v,total)}%</span></div>'
        for l,v in sorted(cs.items(), key=lambda x:-x[1])
    )
    html += f"""<div class="brand-card">
  <div class="b-header"><div class="b-dot" style="background:{brand_color_main[b]}"></div>
    <div class="b-name">{b}</div><div class="b-en">전체 채널 비중</div></div>
  <div class="chart-wrap"><canvas id="{cid}"></canvas></div>
  <div class="legend-list">{legend_rows}</div>
</div>\n"""
    scripts.append(pie_js(cid, labels, vals, cols_c, legend=False))
html += '</div>\n'

# 인사이트
co_cs = data['커버낫']['channel_sales']
co_total = data['커버낫']['total_sale']
co_consign = pct(co_cs.get('위탁/사입',0), co_total)
wa_cs = data['와키윌리']['channel_sales']
wa_total = data['와키윌리']['total_sale']
wa_over = pct(wa_cs.get('해외',0), wa_total)
le_cs = data['리(LEE)']['channel_sales']
le_total = data['리(LEE)']['total_sale']
le_off = pct(le_cs.get('오프라인',0), le_total)

# 와키윌리 스니커즈 오프라인 집계
wa_sneak_off = sum(v for r in rows if r['brand']=='와키윌리' and r['cat1'] in ('오프라인','플래그쉽') and r['prod_type']=='스니커즈' for v in [r['sale']])
wa_slide_off  = sum(v for r in rows if r['brand']=='와키윌리' and r['cat1'] in ('오프라인','플래그쉽') and r['prod_type']=='슬라이드' for v in [r['sale']])
wa_sneak_stores = len(set(r['store'] for r in rows if r['brand']=='와키윌리' and r['cat1'] in ('오프라인','플래그쉽') and r['prod_type']=='스니커즈' and r['sale']>0))

html += f"""<div class="insight">
<strong>&#128204; 오프라인 운영 핵심 요약</strong><br>
&bull; <strong>커버낫·리(LEE)</strong>는 오프라인 전 매장이 슬라이드 단일 운영 — 스니커즈 오프라인 입점 없음.<br>
&bull; <strong>와키윌리</strong>만 스니커즈 오프라인 운영 중: {wa_sneak_stores}개 매장. 슬라이드 병행 매장과 스니커즈 전용 매장 채널 분포 확인 필요.<br>
&bull; <strong>커버낫</strong>은 위탁/사입(쿠팡 B2B) 집중도 <strong>{co_consign}%</strong> — 단일 도매 채널 편중.<br>
&bull; <strong>리(LEE)</strong>는 오프라인 비중 <strong>{le_off}%</strong> — 입점 매장 수 대비 온라인 확장 여지 있음.<br>
&bull; <strong>와키윌리</strong>는 해외 비중 <strong>{wa_over}%</strong> — 글로벌 채널 성장세 지속 주목.
</div></div>
<div class="divider"></div>
"""

# ── SEC 2: 온라인 채널 ──
html += """<div class="section">
<div class="section-title">온라인 채널 현황</div>
<div class="section-desc">1차분류 = 온라인 채널(자사몰·무신사·29CM 등) 운영 현황 및 채널별 판매 비중.</div>
"""

html += '<div class="tbl-wrap"><table>\n'
html += '<tr><th>브랜드</th><th>운영 채널</th><th class="num">채널 수</th><th class="num">온라인 판매</th><th class="num">전체 대비 비중</th></tr>\n'
online_pal = ['#1E40AF','#2563EB','#3B82F6','#60A5FA','#93C5FD']
for b in brands:
    d = data[b]
    oc = d['online_channels']
    ocnt = d['online_channel_count']
    o_total = sum(oc.values())
    o_pct = pct(o_total, d['total_sale'])
    ch_names = ' &middot; '.join(oc.keys())
    c = brand_color_main[b]
    html += f'<tr><td><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:{c};margin-right:6px"></span><strong>{b}</strong></td><td>{ch_names}</td><td class="num">{ocnt}개</td><td class="num">{o_total:,}개</td><td class="num"><strong>{o_pct}%</strong></td></tr>\n'
html += '</table></div>\n'

html += '<div class="brand-row">\n'
for bi, b in enumerate(brands):
    oc = data[b]['online_channels']
    if not oc:
        continue
    o_total = sum(oc.values())
    labels = list(oc.keys())
    vals = list(oc.values())
    cols_c = online_pal[:len(labels)]
    cid = f'pie_oc_{bi}'
    legend_rows = ''.join(
        f'<div class="li"><span><span class="dot" style="background:{online_pal[i%len(online_pal)]}"></span><span class="lname">{l}</span></span><span class="lpct">{pct(v,o_total)}%</span></div>'
        for i,(l,v) in enumerate(sorted(oc.items(), key=lambda x:-x[1]))
    )
    html += f"""<div class="brand-card">
  <div class="b-header"><div class="b-dot" style="background:{brand_color_main[b]}"></div>
    <div class="b-name">{b}</div><div class="b-en">온라인 {len(labels)}채널</div></div>
  <div class="chart-wrap"><canvas id="{cid}"></canvas></div>
  <div class="legend-list">{legend_rows}</div>
</div>\n"""
    scripts.append(pie_js(cid, labels, vals, cols_c, legend=False))
html += '</div>\n'

html += """<div class="insight">
<strong>&#128204; 온라인 채널 분석</strong><br>
&bull; 리(LEE)&middot;와키윌리는 <strong>무신사 의존도</strong> 1위. 커버낫은 자사몰이 64.5%로 강한 D2C 기반 보유.<br>
&bull; <strong>29CM</strong>은 리(LEE)의 핵심 온라인 채널(19.8%). 커버낫 신발은 29CM 미운영 상태.<br>
&bull; 3개 브랜드 모두 온라인 채널 3~4개 수준 — 에이블리&middot;지그재그 등 추가 플랫폼 확장 여지 존재.
</div></div>
<div class="divider"></div>
"""

# ── SEC 3: 슬라이드 vs 스니커즈 ──
html += """<div class="section">
<div class="section-title">슬라이드 vs 스니커즈 판매 비율</div>
<div class="section-desc">슬라이드(슬라이드·플립플랍·메리제인 등) vs 스니커즈(키테·솔레보 스니커즈 등) 구성 비중.</div>
"""

html += '<div class="brand-row">\n'
for bi, b in enumerate(brands):
    bp = data[b]['brand_prods']
    if not bp: continue
    b_total = sum(bp.values())
    labels = list(bp.keys())
    vals = list(bp.values())
    cols_c = [PROD_COLORS.get(l,'#CBD5E1') for l in labels]
    cid = f'pie_bp_{bi}'
    legend_rows = ''.join(
        f'<div class="li"><span><span class="dot" style="background:{PROD_COLORS.get(l,"#CBD5E1")}"></span><span class="lname">{l}</span></span><span class="lpct">{pct(v,b_total)}%</span></div>'
        for l,v in sorted(bp.items(), key=lambda x:-x[1])
    )
    html += f"""<div class="brand-card">
  <div class="b-header"><div class="b-dot" style="background:{brand_color_main[b]}"></div>
    <div class="b-name">{b}</div><div class="b-en">총 {b_total:,}개</div></div>
  <div class="chart-wrap"><canvas id="{cid}"></canvas></div>
  <div class="legend-list">{legend_rows}</div>
</div>\n"""
    scripts.append(pie_js(cid, labels, vals, cols_c, legend=False))
html += '</div>\n'

# 채널별 파이
html += '<h3 style="font-size:13px;font-weight:600;color:#475569;margin:20px 0 12px;padding-left:12px">&#9658; 채널(2차분류)별 슬라이드 / 스니커즈 비율</h3>\n'
ch_order = ['백화점','아울렛','플래그쉽','무신사','자사몰','쿠팡','29CM','에스마켓','면세점','해외','로드샵','카카오톡']
active_chs = [c for c in ch_order if c in cp and sum(cp[c].values())>0]
extra_chs = [c for c in cp if c not in ch_order and sum(cp[c].values())>0]
active_chs += extra_chs

cols_per_row = 4
for i in range(0, len(active_chs), cols_per_row):
    chunk = active_chs[i:i+cols_per_row]
    pad = cols_per_row - len(chunk)
    html += f'<div style="display:grid;grid-template-columns:repeat({cols_per_row},1fr);gap:12px;margin-bottom:12px">\n'
    for ch in chunk:
        prods = cp[ch]
        ch_total = sum(prods.values())
        s_val = prods.get('슬라이드',0)
        k_val = prods.get('스니커즈',0)
        slide_pct = pct(s_val, ch_total)
        sneak_pct = pct(k_val, ch_total)
        cid = f'pie_cp_{ch.replace("/","_").replace("(","").replace(")","")}'

        parts = []
        if s_val>0: parts.append(f'<span style="color:#3B82F6;font-weight:600">슬라이드 {slide_pct}%</span>')
        if k_val>0: parts.append(f'<span style="color:#F59E0B;font-weight:600">스니커즈 {sneak_pct}%</span>')
        legend_html = ' <span style="color:#CBD5E1">|</span> '.join(parts)
        legend_html += f'<br><span style="color:#94A3B8">{ch_total:,}개</span>'

        html += f"""<div class="ch-card">
  <div class="ch-title">{ch}</div>
  <div class="chart-sm"><canvas id="{cid}"></canvas></div>
  <div style="font-size:11px;text-align:center;margin-top:4px">{legend_html}</div>
</div>\n"""
        lbls = []; vls = []; cls = []
        if s_val>0: lbls.append('슬라이드'); vls.append(s_val); cls.append('#3B82F6')
        if k_val>0: lbls.append('스니커즈'); vls.append(k_val); cls.append('#F59E0B')
        scripts.append(pie_js(cid, lbls, vls, cls, legend=False))
    for _ in range(pad):
        html += '<div></div>\n'
    html += '</div>\n'

html += """<div class="insight">
<strong>&#128204; 슬라이드 / 스니커즈 구성 인사이트</strong><br>
&bull; <strong>커버낫&middot;리(LEE)</strong>는 현재 슬라이드 단일 구성 &mdash; 스니커즈 라인 미출고 상태.<br>
&bull; <strong>와키윌리</strong>만 슬라이드&middot;스니커즈 병행 운영. 특히 <strong>해외 채널</strong>에서 스니커즈 비중 57% 역전 &mdash; 글로벌 시장에서 스니커즈 선호 확인.<br>
&bull; <strong>플래그쉽</strong>은 슬라이드 49.6% : 스니커즈 50.4%로 균형 &mdash; 브랜드 체험 공간에서 스니커즈 노출 효과 유효.<br>
&bull; <strong>로드샵</strong>도 스니커즈 52.9% 우위 &mdash; 소규모 단독 채널에서 스니커즈 구매 의향 높음.
</div></div>
</div>
<script>
"""
html += '\n'.join(scripts)
html += '\n</script>\n</body>\n</html>'

OUT = r'C:\Users\bcave\work\product-planning-md\workspace\26SS\dashboard\report_shoes-channel-analysis_2026-04-01.html'
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'저장: {OUT}')
