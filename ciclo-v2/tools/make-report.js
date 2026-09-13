const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  PageBreak, LevelFormat, convertInchesToTwip,
} = require('docx');
const fs = require('fs');

const FONT = '맑은 고딕';
const NAVY = '111E6C';
const INK  = '1A1A1A';
const GREY = '5C5C5C';
const LINE = 'D8D3C8';
const CREAM = 'F4F1EA';

// A4(11906 twips) − 좌우 여백 1440씩 = 9026. 이 값을 넘기면 표가 오른쪽 여백을 침범한다.
const W = 9026;

// ── 헬퍼 ────────────────────────────────────────────────────────
const P = (text, o = {}) => new Paragraph({
  alignment: o.align,
  spacing: { before: o.before ?? 0, after: o.after ?? 120, line: o.line ?? 300 },
  indent: o.indent,
  numbering: o.numbering,
  border: o.border,
  children: (Array.isArray(text) ? text : [text]).map(t =>
    typeof t === 'string'
      ? new TextRun({ text: t, font: FONT, size: o.size ?? 20, color: o.color ?? INK, bold: o.bold })
      : new TextRun({ font: FONT, size: o.size ?? 20, color: o.color ?? INK, ...t })),
});

const H1 = t => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  spacing: { before: 400, after: 200 },
  children: [new TextRun({ text: t, font: FONT, size: 30, bold: true, color: NAVY })],
});
const H2 = t => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  spacing: { before: 300, after: 140 },
  children: [new TextRun({ text: t, font: FONT, size: 24, bold: true, color: INK })],
});
const H3 = t => new Paragraph({
  heading: HeadingLevel.HEADING_3,
  spacing: { before: 220, after: 100 },
  children: [new TextRun({ text: t, font: FONT, size: 21, bold: true, color: NAVY })],
});

const BULLET = t => P(t, { numbering: { reference: 'b', level: 0 }, after: 60 });

const NOTE = (lines) => new Paragraph({
  spacing: { before: 140, after: 180, line: 300 },
  indent: { left: 200 },
  border: { left: { style: BorderStyle.SINGLE, size: 18, color: NAVY, space: 12 } },
  children: lines.flatMap((l, i) => {
    const runs = (Array.isArray(l) ? l : [l]).map(t =>
      typeof t === 'string'
        ? new TextRun({ text: t, font: FONT, size: 19, color: GREY })
        : new TextRun({ font: FONT, size: 19, color: GREY, ...t }));
    return i ? [new TextRun({ break: 1 }), ...runs] : runs;
  }),
});

// 표: rows = [[c,c,c], ...], 첫 행은 머리글
function T(cols, rows, opt = {}) {
  const widths = cols.map(c => Math.round(W * c));
  const cell = (txt, i, head) => new TableCell({
    width: { size: widths[i], type: WidthType.DXA },
    shading: head ? { type: ShadingType.CLEAR, fill: NAVY } : (opt.zebra && opt.r % 2 ? { type: ShadingType.CLEAR, fill: 'FAF8F3' } : undefined),
    margins: { top: 80, bottom: 80, left: 110, right: 110 },
    children: [new Paragraph({
      alignment: i === 0 ? AlignmentType.LEFT : (opt.numAlign && i >= (opt.numFrom ?? 1) ? AlignmentType.RIGHT : AlignmentType.LEFT),
      spacing: { after: 0, line: 260 },
      children: (Array.isArray(txt) ? txt : [txt]).map(t => typeof t === 'string'
        ? new TextRun({ text: t, font: FONT, size: 18, bold: head, color: head ? 'FFFFFF' : INK })
        : new TextRun({ font: FONT, size: 18, bold: head, color: head ? 'FFFFFF' : INK, ...t })),
    })],
  });
  return new Table({
    columnWidths: widths,
    width: { size: W, type: WidthType.DXA },
    borders: {
      top:    { style: BorderStyle.SINGLE, size: 2, color: LINE },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: LINE },
      left:   { style: BorderStyle.NONE },
      right:  { style: BorderStyle.NONE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: LINE },
      insideVertical:   { style: BorderStyle.NONE },
    },
    rows: rows.map((r, ri) => new TableRow({
      tableHeader: ri === 0,
      children: r.map((c, ci) => { opt.r = ri; return cell(c, ci, ri === 0); }),
    })),
  });
}
const GAP = (h = 160) => new Paragraph({ spacing: { after: h }, children: [] });

// ── 문서 ────────────────────────────────────────────────────────
const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 20, color: INK } } } },
  numbering: {
    config: [{
      reference: 'b',
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: '•',
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 340, hanging: 200 } } },
      }],
    }],
  },
  sections: [{
    properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    children: [

// ══ 표지 ══
GAP(1400),
new Paragraph({
  spacing: { after: 80 },
  children: [new TextRun({ text: 'CICLO', font: FONT, size: 56, bold: true, color: INK })],
}),
new Paragraph({
  spacing: { after: 400 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: NAVY, space: 10 } },
  children: [new TextRun({ text: '홈페이지 v2 작업 보고서', font: FONT, size: 32, bold: true, color: NAVY })],
}),
P('238LAB 벤치마킹 반영 · 실측 진단 · 남은 작업 · 배포 순서', { size: 22, color: GREY, after: 600 }),
T([0.28, 0.72], [
  ['항목', '내용'],
  ['작성일', '2026년 9월 13일'],
  ['대상', 'ciclo.kr — 홈 및 서브페이지 9개, 치과 랜딩 1개'],
  ['산출물', 'global.css · ciclo-effects.js · wpcode-head.html · 페이지 마크업 12개'],
  ['벤치마크', '238lab.kr (실측 대조)'],
  ['검증 환경', '헤드리스 크롬 · 1440 / 768 / 390 / 360px'],
]),
new Paragraph({ children: [new PageBreak()] }),

// ══ 요약 ══
H1('요약'),
P('씨클로 홈페이지를 238LAB 수준의 콘텐츠 구성으로 다시 짜고, 그 과정에서 라이브 사이트에 실제로 나고 있던 버그를 찾아 고쳤습니다. 디자인 시스템(크림·네이비·옐로, Archivo)은 그대로 두고 내용 구성·문체·타이포·모션만 바꿨습니다.'),

H2('핵심은 세 가지입니다'),
BULLET(['증거가 생겼습니다. ', { text: '치과 여덟 곳을 직접 채점한 실태조사', bold: true }, '와 맡은 사이트의 실측값을 숫자 그대로 열었습니다. 이전에는 목업 화면 한 장이 전부였습니다.']),
BULLET(['말투가 바뀌었습니다. ', { text: '못 하는 것과 한계를 같은 문단에서 밝히는', bold: true }, ' 238LAB 문법을 가져왔습니다. 증가율 옆에 분모를 같이 적고, 100점 옆에 "빠르다는 뜻이지 잘 팔린다는 뜻이 아니다"를 붙였습니다.']),
BULLET(['라이브에 나고 있던 버그 세 개를 찾았습니다. ', { text: 'JavaScript 스니펫 전체가 죽어 있고, 홈이 설계 폭의 64%로 눌려 있고, 로고 이미지 5개가 404', bold: true }, '입니다. 성능 이전에 기능 문제입니다.']),

NOTE([
  [{ text: '이 보고서에 PageSpeed 점수는 없습니다.', bold: true, color: INK }],
  '로컬 환경은 프록시가 폰트 CDN을 막아 FCP가 12초로 찍힙니다. 실제 점수는 배포 후 PageSpeed Insights에서 재야 합니다. 아래 수치는 전부 헤드리스 크롬 실측이거나 정적 분석 값입니다.',
]),

new Paragraph({ children: [new PageBreak()] }),

// ══ 1장 ══
H1('1. 벤치마킹 — 238LAB 실측 대조'),
P('감으로 비교하지 않고 두 사이트의 계산된 스타일을 같은 조건에서 읽어 표로 만들었습니다.'),
GAP(100),
T([0.22, 0.39, 0.39], [
  ['역할', '씨클로 (전)', '238LAB'],
  ['h1', '168px / 900 / 행간 0.92 / Archivo', '60px / 700 / 행간 1.25 / 한글'],
  ['h2', '80px / 900 / 영문', '36px / 700 / 한글 문장'],
  ['본문 기본', '16px / 행간 1.50 / weight 500', '16px / 행간 1.70 / weight 400'],
  ['섹션 리드', '없음', '18px / 400 / 행간 1.556'],
  ['섹션 패딩', '140 / 140', '160 / 160'],
  ['버튼 라운드', '20px (알약)', '4px'],
  ['알약 배지', '18개', '0개'],
  ['스크롤 리빌', '22개 노드', '0개'],
]),
GAP(),

H3('가장 중요한 발견 — weight 500 문제'),
P('씨클로는 본문을 전부 500으로 깔고 있었습니다. 부제도 500, 카드 본문도 500. 그래서 본문 안에 위계가 없었습니다. 238LAB은 400을 기본으로 두고 600·700을 위계에만 씁니다.'),
P([{ text: 'body를 400으로 내리는 한 줄', bold: true }, '만으로 체감이 가장 크게 달라지는 항목이었습니다.']),

H3('가져온 것과 가져오지 않은 것'),
P([{ text: '가져온 것 — ', bold: true }, '섹션 구성 문법(눈썹 → 한글 문장형 h2 → 리드 → 근거 → 출처 캡션), FAQ 답변의 4요소(단정 첫문장 / 실무 근거 / 자사 한계 고백 / 판별 기준), 타이포 토큰, 모션 최소화.']),
P([{ text: '가져오지 않은 것 — ', bold: true }, '문체 자체입니다. 씨클로의 칼럼 문체가 238LAB보다 낫다고 판단했습니다. 구조 규칙만 빌리고 목소리는 씨클로 것을 유지했습니다.']),

new Paragraph({ children: [new PageBreak()] }),

// ══ 2장 ══
H1('2. 라이브 사이트 진단'),
P('성능을 재려고 열었다가 먼저 발견한 것들입니다. v2 적용과 별개로 지금 고쳐야 합니다.'),

H2('버그 1 — JavaScript 스니펫이 통째로 죽어 있습니다'),
P([ '라이브 콘솔에 ', { text: 'SyntaxError: Unexpected token \':\'', bold: true }, ' 가 뜹니다. WPCode JavaScript 스니펫 하나의 끝에 JSON-LD 스키마가 ', { text: '<script>', bold: true }, ' 태그 없이 붙어 있습니다. JS 문맥에서는 문법 오류라 ', { text: '스니펫 전체가 파싱 단계에서 실행되지 못합니다.', bold: true }]),
P('그 스니펫이 하려던 일 — body에 ciclo-live 클래스 부여, 테마 헤더·푸터 숨기기, max-width 해제 — 이 전부 작동하지 않고 있습니다.'),
P([{ text: '조치: ', bold: true }, '그 스니펫에서 JSON-LD 블록을 삭제하십시오. 구조화 데이터는 이미 SEO 플러그인이 9.6KB 규모로 정상 출력 중이라 중복입니다. 지워도 손실이 없습니다.']),

H2('버그 2 — 홈이 820px로 눌려 있습니다'),
P('1280px로 설계된 홈이 라이브에서 820px로 렌더링됩니다. 설계 폭의 64%입니다.'),
BULLET('커스터마이저 추가 CSS의 max-width:820px 규칙에 body 조건이 없습니다.'),
BULLET('이를 풀어주려고 넣은 body.ciclo-live 규칙은 버그 1 때문에 클래스가 안 붙어 발동하지 않습니다.'),
BULLET('.ciclo-page에 max-width:none을 줬지만, 제약이 걸린 건 부모인 .page-content라 효과가 없습니다.'),

H2('버그 3 — 로고 이미지 5개가 전부 404'),
P('업로드 경로와 마크업이 가리키는 경로가 다릅니다. 눈에 안 보였던 이유는 CSS가 content:url()로 실제 로고를 덮어 그리고 있기 때문입니다. 화면은 멀쩡한데 요청은 5번 실패합니다.'),
P([{ text: '조치: ', bold: true }, 'v2에서 src를 투명 1×1 GIF로 바꿔 요청 자체를 없앴습니다. 업로드가 필요 없습니다.']),

H2('그리고 — CSS가 두 벌 돌고 있습니다'),
GAP(80),
T([0.46, 0.16, 0.38], [
  ['스타일', '크기', '정체'],
  ['(no-id)', '49.1KB', 'WPCode global.css'],
  ['(no-id)', '25.0KB', 'global.css를 #ciclo-home으로 스코프한 복사본'],
  ['global-styles-inline', '10.9KB', '워드프레스 theme.json (77% 미사용)'],
  ['wp-block-library', '4.2KB', '구텐베르크 — 페이지에 블록 0개'],
  ['wp-emoji-styles', '0.3KB', '이모지 — 페이지에 이모지 0개'],
]),
GAP(),
NOTE([
  [{ text: '이것 때문에 global.css만 v2로 바꾸면 거의 아무 변화가 없습니다.', bold: true, color: INK }],
  '#ciclo-home은 특정성 (1,1,0)이라 원본 global.css의 (0,1,0)을 모든 공통 규칙에서 이깁니다. 즉 라이브가 실제로 그리고 있는 값은 global.css가 아니라 그 25KB 복사본입니다. 복사본을 먼저 지워야 합니다.',
]),

new Paragraph({ children: [new PageBreak()] }),

// ══ 3장 ══
H1('3. v2에서 한 작업'),

H2('3-1. 콘텐츠 구성 — 홈 섹션을 다시 짰습니다'),
GAP(80),
T([0.1, 0.32, 0.58], [
  ['#', '섹션', '내용'],
  ['1', '히어로', 'CICLO + "GEO 웹사이트, 랜딩페이지 제작"'],
  ['2', '마퀴', '유지 (26s → 40s)'],
  ['3', '증거 밴드 (신설)', '81점 → 20점 대비, 열 항목 막대, 30초 자가 점검'],
  ['4', '서비스', 'h2 한글 문장형 + 리드'],
  ['5', '사례', '진단 카드 6장 — 익명 처리한 실측 점수'],
  ['6', '실적 밴드 (신설)', '맡은 사이트의 유입·속도 실측'],
  ['7', '프로세스', 'h2 한글화 + 리드'],
  ['8', 'Why now (신설)', '지금인 이유 3가지, 전부 실측 근거'],
  ['9', '소개', 'h2 한글화 + 1단 전환'],
  ['10', 'FAQ', '5 → 7문항, 금액 밴드 공개'],
]),
GAP(),

H3('증거 밴드 — 사이트에서 가장 중요한 자리'),
P('치과 홈페이지 여덟 곳을 열 항목·쉰 개 체크포인트로 채점했습니다. 사람이 보는 화면은 81점인데 기계가 읽는 자리는 20점이라는 격차를 한 화면에 넣었습니다.'),
P('"30초 자가 점검"을 같이 넣었습니다. 페이지 소스 보기 → Ctrl+F → ld+json. 읽는 분이 직접 확인할 수 있어야 증거가 됩니다.'),

H3('실적 밴드 — 진단에서 멈추지 않는다는 증명'),
P('지금까지 사이트가 하던 말은 "남의 사이트를 채점했다"까지였습니다. 제공해 주신 실측 캡처로 "맡은 뒤 숫자가 어디로 갔다"를 처음 붙였습니다.'),
GAP(80),
T([0.26, 0.15, 0.15, 0.15, 0.29], [
  ['대상', '클릭', '노출', '클릭률', '직전 90일 대비'],
  ['치과 ① 수도권·종합', '740', '6.4만', '1.2%', '+12,300%'],
  ['치과 ② 인천·사랑니', '110', '1.9만', '0.6%', '+1,733%'],
  ['치과 ③ 수도권·개원초기', '74', '1.4만', '0.5%', '+7,300%'],
], { numAlign: true }),
GAP(80),
NOTE([
  [{ text: '증가율만 크게 쓰지 않았습니다.', bold: true, color: INK }],
  '세 곳 모두 직전 90일 클릭이 한 자리였습니다. 740클릭은 6클릭에서 온 값이고, 74클릭은 1클릭에서 온 값입니다. 카드 안에 "직전 90일 클릭" 행을 따로 두어 배수의 분모를 숨기지 않았고, 캡션에 "클릭률 1.2%는 업계 평균을 넘는 값이 아닙니다"를 넣었습니다.',
]),

H3('금액 밴드 — 지어내지 않고 자사 공개값을 옮겼습니다'),
P('FAQ의 TODO 다섯 칸을 채웠습니다. 출처는 패키지 안에 이미 있었습니다 — /dental 랜딩의 패키지 표가 정상가를 공개하고 있었습니다.'),
GAP(80),
T([0.34, 0.18, 0.14, 0.14, 0.2], [
  ['패키지', '정상가', '기간', '페이지', '무상수정'],
  ['STANDARD · 단일 페이지', '150만원', '2주', '1', '2회'],
  ['DELUXE · 진료과목 분리', '200만원', '3주', '7', '3회'],
  ['PREMIUM · 콘텐츠 구조까지', '320만원', '4주', '15', '5회'],
], { numAlign: true }),
GAP(80),
P('월 이용료 0원, 도메인·서버 실비 연 20~40만원, 오픈 후 3개월 무상 점검도 함께 적었습니다. 런칭 특별가는 지우지 않고 밴드 아래 한 줄로 /dental에 안내합니다.'),

new Paragraph({ children: [new PageBreak()] }),

H2('3-2. 타이포와 여백'),
P('섹션 사이 여백(160/160)은 238LAB 실측치와 같아 건드리지 않았습니다. 빽빽한 것은 섹션 안쪽이었습니다.'),
GAP(80),
T([0.46, 0.27, 0.27], [
  ['항목', '전', '후 (1440px)'],
  ['진단 카드 패딩', '24 / 22', '32 / 28'],
  ['실적 카드 패딩', '22 / 22 / 20', '30 / 28 / 26'],
  ['프로세스 카드 패딩', '28 / 24', '36 / 30'],
  ['카드 그리드 간격', '14~24', '26~30'],
  ['눈썹 → h2', '18', '26'],
  ['h2 → 리드', '18', '24'],
  ['FAQ 답변 문단 간격', '12', '18'],
  ['리드 행간', '1.55', '1.68'],
], { numAlign: true }),
GAP(80),
P('한글은 글자에 속공간이 없어 같은 수치라도 라틴 문자보다 빽빽하게 읽힙니다. 모바일은 clamp() 하한을 종전 값 근처에 두어 세로로 더 길어지지 않게 했습니다.'),

H3('제목 줄바꿈 버그 (전 페이지 48곳)'),
P('420px 이하에서 제목의 강제 개행을 푸는 규칙이 있는데, 마크업이 "않았습니다,<br>고친" 이라 br이 사라지면 "않았습니다,고친"으로 붙었습니다.'),
P('CSS로는 해결되지 않는 것을 먼저 확인했습니다 — br::after{content:" "}는 렌더되지 않고, br{display:inline;content:" "}는 br이 그대로 개행합니다. 마크업에 공백을 넣는 방법만 동작했고, 데스크톱 줄 폭은 변하지 않았습니다.'),

H2('3-3. 성능'),
GAP(80),
T([0.42, 0.29, 0.29], [
  ['항목', '전', '후'],
  ['global.css (gzip)', '26,361B', '19,427B (−26%)'],
  ['로고 인라인 payload', 'PNG base64 23,962B', 'WebP 6,023B (−75%)'],
  ['폰트 로딩', '@import ×2 (직렬 3왕복)', 'head <link> + preconnect (병렬)'],
  ['will-change 노드', '1', '0'],
  ['무한 애니메이션', '3', '1 (마퀴)'],
  ['스크롤 리빌', '22 노드', '0'],
  ['이미지 404', '5건', '0건'],
  ['이미지 치수 명시', '0 / 5', '5 / 5'],
], { numAlign: true }),
GAP(80),
NOTE([
  [{ text: '압축 전 바이트는 오히려 13% 늘었습니다.', bold: true, color: INK }],
  '섹션을 다섯 개 새로 만들어 규칙이 290 → 501개가 됐기 때문입니다. 다만 인라인 <style>은 HTML과 함께 압축돼 나가므로 회선을 타는 값은 gzip 쪽이고, 그 기준으로는 26% 줄었습니다. 파싱 비용은 규칙 수에 비례하므로 +211개가 공짜는 아니라는 점도 적어 둡니다.',
]),

H2('3-4. 접근성'),
P('"PageSpeed 100점" 목표에는 접근성 100점도 들어가고, 라이트하우스가 대비를 자동 검사합니다. 텍스트를 가진 요소를 전수 대조했더니 27곳이 WCAG AA 미달이었습니다.'),
GAP(80),
T([0.3, 0.34, 0.18, 0.18], [
  ['배경', '색', '대비', '기준'],
  ['패널 #ECE7DC', 'rgba(18,18,18,.48)', '3.16', '4.5'],
  ['크림·패널', 'rgba(18,18,18,.5)', '3.35~3.43', '4.5'],
  ['크림·패널', 'rgba(18,18,18,.55)', '3.90~4.00', '4.5'],
  ['네이비 #111E6C', 'rgba(255,255,255,.35)', '2.96', '4.5'],
  ['흰 카드', 'rgba(17,30,108,.6)', '4.26', '4.5'],
], { numAlign: true, numFrom: 2 }),
GAP(80),
P('임계값을 계산해 color: 선언 39곳을 올렸습니다. 가장 눈에 띄는 개선은 증거 밴드 차트의 축 눈금(0·20·40·60·80·100)으로, 2.96:1이라 실제로 거의 보이지 않았습니다.'),
P('그 밖에 포커스 트랩·스크롤 잠금·aria 상태·포커스 복원을 사이드바에 넣었고, 키보드로 직접 구동해 확인했습니다(Tab 25회로 닫힌 사이드바에 닿지 않고, 열린 상태에서 Tab 30회가 안에 갇히며, ESC로 버거 버튼에 포커스가 돌아옵니다).'),

H2('3-5. 치과 랜딩 페이지 수리'),
P('홈 Featured 카드가 가리키는 가장 큰 페이지(76.7KB)인데 상태가 가장 나빴습니다.'),
GAP(80),
T([0.34, 0.33, 0.33], [
  ['항목', '전', '후'],
  ['가로 오버플로 (390px)', '470px', '0'],
  ['뷰포트보다 넓은 노드', '276개', '0'],
  ['최대 제목 크기 (390px)', '88px', '38px'],
  ['will-change 노드', '33', '0'],
  ['무한 애니메이션', '3', '0'],
  ['Pretendard 로드', '2벌', '1벌'],
  ['카카오 플로팅 버튼', '2개', '1개'],
], { numAlign: true }),
GAP(80),
P('고정폭 860px에 미디어쿼리가 카카오 버튼용 두 개뿐이었습니다. 휴대폰에서 페이지 전체가 옆으로 밀리고 글이 잘렸습니다.'),
P('작동한 적 없는 코드도 두 개 찾았습니다. 스크롤 스냅 규칙이 html을 div의 자손으로 지정해 한 번도 적용된 적이 없었고, 스코프 없는 스타일 블록이 한 벌 더 있었습니다.'),

new Paragraph({ children: [new PageBreak()] }),

// ══ 4장 ══
H1('4. 남은 작업'),
P('전부 제가 할 수 없는 것들입니다. 값을 알 수 없거나, 사실 확인이 필요합니다.'),
GAP(100),
T([0.06, 0.3, 0.64], [
  ['#', '항목', '내용'],
  ['1', 'PSI 캡처 2장', '대화에는 있으나 파일로 받지 못했습니다. assets/psi/에 넣고 python3 build-psi-shots.py 한 줄이면 변환·모자이크·마크업 교체가 끝납니다.'],
  ['2', 'About 회사정보', '대표 · 사업자등록번호 · 소재지 3칸이 비어 있습니다. 빨간 TODO 배지로 표시해 두었습니다.'],
  ['3', '실적 밴드 귀속 표현', '"저희가 맡은 / 만든 사이트"가 다섯 곳 전부에 맞는지 확인이 필요합니다. 유지보수만 맡은 곳이 섞여 있으면 "운영 중인"이 정확합니다.'],
  ['4', '치과 랜딩 전화번호', '010-8817-2001이었는데 나머지 네 곳 정본(010-8017-2001)으로 맞췄습니다. 8817이 맞다면 알려주십시오.'],
]),
GAP(),
NOTE([
  [{ text: '배포 전에 2번은 반드시 채워야 합니다.', bold: true, color: INK }],
  '사업자 정보를 적어두지 않은 에이전시는 거르셔도 된다고 About에 써 두었는데, 정작 저희 것이 비어 있으면 앞뒤가 맞지 않습니다.',
]),

// ══ 5장 ══
H1('5. 배포 순서'),
NOTE([
  [{ text: 'global.css만 바꾸면 거의 아무 변화가 없습니다.', bold: true, color: INK }],
  '라이브에 #ciclo-home으로 스코프된 25KB 복사본이 특정성으로 원본을 이기고 있습니다. 그것을 먼저 지워야 v2가 먹습니다.',
]),
GAP(100),
T([0.08, 0.42, 0.5], [
  ['순서', '작업', '위치'],
  ['1', '25KB 중복 CSS 스니펫 삭제', 'WPCode — .ciclo-page{max-width:none!important로 시작하는 것'],
  ['2', 'JS 스니펫의 JSON-LD 블록 삭제', 'WPCode — SyntaxError를 내는 스니펫'],
  ['3', 'max-width:820px 규칙에 body 조건 부여', '커스터마이저 추가 CSS'],
  ['4', 'global.css 교체', 'WPCode CSS 스니펫'],
  ['5', 'ciclo-effects.js 교체', 'WPCode JS 스니펫 (Site Wide Footer)'],
  ['6', 'wpcode-head.html 추가', 'WPCode HTML 스니펫 (Site Wide Header)'],
  ['7', '페이지 마크업 교체', 'Elementor 텍스트 에디터 위젯'],
]),
GAP(),
P([{ text: '주의: ', bold: true }, '4번과 5번은 세트입니다. CSS만 바꾸고 JS를 그대로 두면 구버전 JS가 .reveal을 주입해 콘텐츠가 보이지 않습니다. 6번을 넣지 않으면 폰트가 적용되지 않습니다.']),
P('불필요한 CSS(wp-block-library · global-styles · 이모지) 제거용 PHP 스니펫은 PERFORMANCE.md에 적어 두었습니다. 15.4KB 규모이고 대부분 이 사이트에서 쓰지 않는 규칙입니다.'),

new Paragraph({ children: [new PageBreak()] }),

// ══ 부록 ══
H1('부록. 검증과 도구'),
H2('검증 결과 (9개 페이지 × 1440 / 390px)'),
GAP(80),
T([0.5, 0.5], [
  ['항목', '결과'],
  ['페이지당 h1', '전부 정확히 1개'],
  ['제목 단계 건너뜀', '0'],
  ['죽은 내부 링크', '0 (11개 경로 전부 실재)'],
  ['alt 없는 이미지', '0'],
  ['제목 단어 붙음', '0'],
  ['가로 오버플로', '0'],
  ['요소 겹침 (1440/768/390/360)', '0'],
  ['로고 비율 오차', '0 (5개 인스턴스 전부 488:566)'],
  ['CLS', '0'],
  ['JS 에러', '0'],
  ['WCAG AA 대비 미달', '0'],
]),
GAP(),

H2('만든 도구'),
GAP(80),
T([0.3, 0.7], [
  ['파일', '용도'],
  ['make-preview.py', '워드프레스 출력 구조를 재현한 로컬 프리뷰 생성'],
  ['tools/img2webp.js', '크로미움 캔버스 기반 모자이크·리사이즈·WebP 변환'],
  ['build-psi-shots.py', 'PSI 캡처 변환 + 마크업 교체 자동화'],
  ['build-*.py (30여 개)', '변경 하나당 스크립트 하나. 각 파일 상단에 왜 고쳤는지와 실측값이 적혀 있습니다.'],
]),
GAP(),
P('모든 build 스크립트는 대상 문자열을 정확히 1회만 찾도록 단언합니다. 못 찾으면 조용히 틀리지 않고 멈춥니다.'),

GAP(300),
new Paragraph({
  border: { top: { style: BorderStyle.SINGLE, size: 8, color: LINE, space: 12 } },
  spacing: { before: 200 },
  children: [new TextRun({ text: 'CICLO · 2026', font: FONT, size: 17, color: GREY })],
}),

    ],
  }],
});

Packer.toBuffer(doc).then(b => {
  fs.writeFileSync(process.argv[2] || 'report.docx', b);
  console.log('생성 완료:', process.argv[2], (b.length / 1024).toFixed(1) + 'KB');
});
