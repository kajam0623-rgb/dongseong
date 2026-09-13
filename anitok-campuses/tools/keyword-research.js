#!/usr/bin/env node
/**
 * 지점별로 네이버 자동완성을 훑어, 그 동네에서 실제로 검색되는 말이 무엇이고
 * 그 말이 무엇을 뜻하는지 확인한다. 일산 저장소의 같은 도구를 캠퍼스용으로 옮겼다.
 *
 * 재는 것: 네이버는 사람들이 실제로 치는 말만 자동완성한다. 자동완성에 뜨면
 * 수요가 있다는 증거이고, 순위는 대략적인 서열이다.
 *
 * 재지 않는 것: 검색량과 경쟁도. 그건 네이버 검색광고 키워드도구 API 가 있어야
 * 하고 이 기계에는 자격증명이 없다. 여기 숫자를 검색량으로 읽으면 안 된다.
 *
 * 의도 검사가 생각보다 중요하다. "부천미술학원"은 자동완성이 잘 되지만 그 안에
 * 유치부·차량·채용이 섞여 있다. 이 학원은 초3부터라 유아 미술학원을 찾는 사람이
 * 들어오면 서로 손해다. 수요가 있다는 것과 우리가 노려야 한다는 것은 다르다.
 *
 * 쓰기: node tools/keyword-research.js <지점> [--out content/<지점>/keywords.json]
 *       node tools/keyword-research.js mokdong
 *
 * 주의: 이 도구는 ac.search.naver.com 을 직접 부른다. 네이버가 막힌 망에서는
 * 결과가 전부 0 으로 나오므로, 값이 전부 비면 네트워크부터 확인할 것.
 */

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.join(__dirname, '..');
const slug = process.argv[2];
if (!slug || slug.startsWith('--')) {
  console.error('지점 slug 가 필요하다. 예: node tools/keyword-research.js mokdong');
  process.exit(1);
}
const dataPath = path.join(ROOT, 'data', slug + '.json');
if (!fs.existsSync(dataPath)) {
  console.error('data/' + slug + '.json 이 없다');
  process.exit(1);
}
const d = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
const OUT = process.argv.includes('--out')
  ? process.argv[process.argv.indexOf('--out') + 1]
  : path.join(ROOT, 'content', slug, 'keywords.json');

// 조사할 지역은 지점 데이터에서 끌어온다. local.area 와 nearbyAll 의 동네,
// 그리고 주소의 시·구를 합친다. 손으로 적어 두면 지점을 늘릴 때마다 잊는다.
const loc = d.local || {};
const PLACES = [
  ...new Set(
    [
      loc.area,
      ...(loc.nearbyAll || []).map((n) => n.area),
      ...(loc.nearby || []).map((n) => n.area),
      ...String(d.address?.line1 || '').split(/\s+/).filter((w) => /(시|구)$/.test(w)),
    ].filter(Boolean)
  ),
];
const TOPICS = [
  '만화학원', '웹툰학원', '애니메이션학원', '미술학원', '그림학원', '입시미술학원',
  '만화애니학원', '디지털드로잉', '일러스트학원', '캐릭터학원', '미대입시', '예고입시',
];
// 지역과 무관하게 알아 둘 값어치가 있는 말들.
const BARE = [...TOPICS, '웹툰과', '애니메이션과', '만화과', '청강대웹툰과', '애니고', '경기예고'];

// 그 말이 학원이 아닌 다른 것을 뜻한다는 신호.
const OFF_TOPIC = {
  유아: '유아 미술학원 수요 (주니어반은 초3부터)',
  유치부: '유치부 미술학원 수요',
  채용: '구인 검색',
  차량: '학원 차량 문의',
  만화카페: '만화카페 수요',
  만화방: '만화방 수요',
  만화책: '만화책 구매/대여',
  대여: '만화 대여',
  맛집: '음식점',
};

const AC =
  'https://ac.search.naver.com/nx/ac?q=%s&con=0&frm=nv&ans=2&r_format=json&r_enc=UTF-8' +
  '&r_unicode=0&t_koreng=1&run=2&rev=4&q_enc=UTF-8&st=100';

const cache = new Map();
function suggest(q) {
  if (cache.has(q)) return cache.get(q);
  let items = [];
  try {
    const raw = execFileSync('curl', ['-sS', '--max-time', '12', '-A', 'Mozilla/5.0', AC.replace('%s', encodeURIComponent(q))], {
      encoding: 'utf8',
    });
    items = ((JSON.parse(raw).items || [])[0] || []).map((a) => a[0]);
  } catch {
    items = [];
  }
  cache.set(q, items);
  return items;
}

const norm = (s) => s.replace(/\s+/g, '');

function assess(term) {
  const items = suggest(term);
  const flat = items.map(norm);
  const self = flat.indexOf(norm(term));

  const noise = [];
  for (const [word, why] of Object.entries(OFF_TOPIC)) {
    const hits = items.filter((i) => norm(i).includes(word)).length;
    if (hits) noise.push({ word, hits, why });
  }
  const offTopicShare = items.length ? noise.reduce((n, x) => n + x.hits, 0) / items.length : 0;

  return {
    term,
    suggested: items.length,
    selfRank: self < 0 ? null : self + 1, // 1-based; null = Naver does not complete to it
    siblings: items.slice(0, 8),
    offTopic: noise,
    offTopicShare: Math.round(offTopicShare * 100),
  };
}

const results = [];
const seen = new Set();
const add = (t) => {
  const k = norm(t);
  if (seen.has(k)) return;
  seen.add(k);
  results.push(assess(t));
};

console.log('probing…');
for (const p of PLACES) for (const t of TOPICS) add(p + t);
for (const t of BARE) add(t);

// Second pass: whatever Naver itself suggested that we had not thought to ask about,
// as long as it is still about learning to draw somewhere near here.
const discovered = new Set();
for (const r of results) {
  for (const s of r.siblings) {
    const n = norm(s);
    if (seen.has(n)) continue;
    if (!/(학원|입시|과|드로잉|일러스트)/.test(n)) continue;
    if (Object.keys(OFF_TOPIC).some((w) => n.includes(w))) continue;
    discovered.add(s);
  }
}
for (const d of [...discovered].slice(0, 40)) add(d);

// Ranked by: Naver completes to it at all, how near the top, and how clean the intent.
const scored = results
  .map((r) => ({
    ...r,
    score: (r.selfRank ? 100 - (r.selfRank - 1) * 8 : 0) + (r.suggested ? 10 : 0) - r.offTopicShare,
  }))
  .sort((a, b) => b.score - a.score);

// 망이 막혀 있으면 모든 질의가 조용히 빈 배열로 돌아온다. 그대로 쓰면
// "수요 없음"이 가득한 파일이 남아, 실제로는 수요가 있는 말까지 버리게 된다.
// 실제로 이 컨테이너에서 한 번 그렇게 나왔다. 하나도 못 받았으면 쓰지 않는다.
if (results.every((r) => r.suggested === 0)) {
  console.error(
    '모든 질의가 빈 응답이다. ac.search.naver.com 에 닿지 못했을 가능성이 크다.\n' +
      '결과를 쓰지 않고 멈춘다. 네이버가 열린 망에서 다시 돌릴 것.'
  );
  process.exit(1);
}

const usable = scored.filter((r) => r.selfRank && r.offTopicShare < 40);
const noDemand = scored.filter((r) => !r.suggested);
const mismatched = scored.filter((r) => r.offTopicShare >= 40);

fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify({ probedAt: new Date().toISOString().slice(0, 10), results: scored }, null, 2));

console.log('\n검색 수요 확인됨 (네이버가 자동완성하는 것) — ' + usable.length + '개');
usable.slice(0, 25).forEach((r) => console.log('  ' + String(r.selfRank).padStart(2) + '위  ' + r.term));

if (mismatched.length) {
  console.log('\n검색 의도가 다름 — 쓰면 안 되는 키워드');
  mismatched.slice(0, 10).forEach((r) => console.log('  ' + r.term + '  (' + r.offTopic.map((o) => o.why).join(', ') + ')'));
}

console.log('\n자동완성 없음 (수요 거의 없음) — ' + noDemand.length + '개');
console.log('  ' + noDemand.slice(0, 14).map((r) => r.term).join(', '));
console.log('\n→ ' + OUT);
