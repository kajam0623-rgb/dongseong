(function(){
var rm = matchMedia('(prefers-reduced-motion: reduce)').matches;
document.addEventListener('error', function(e){
var img = e.target;
if (!img || img.tagName !== 'IMG' || img.dataset.fellBack) return;
img.dataset.fellBack = '1';
if (img.classList.contains('hero-bg')) {
var d = document.createElement('div');
d.className = 'hero-bg hero-bg--none';
img.replaceWith(d);
return;
}
var ph = document.createElement('div');
ph.className = 'ph';
ph.setAttribute('role', 'img');
ph.setAttribute('aria-label', img.alt || '사진 준비 중');
ph.innerHTML = '<span class="ph-mark">ANITALK</span><span class="ph-cap"></span>';
ph.querySelector('.ph-cap').textContent = img.alt || '사진 준비 중';
var btn = img.closest('button.shot');
(btn || img).replaceWith(ph);
}, true);
var bar = document.querySelector('[data-progress]');
if (bar) {
var tick = false;
addEventListener('scroll', function(){
if (tick) return; tick = true;
requestAnimationFrame(function(){
var h = document.documentElement.scrollHeight - innerHeight;
bar.style.width = (h > 0 ? (scrollY / h) * 100 : 0) + '%';
tick = false;
});
}, { passive: true });
}
var h1 = document.querySelector('.hero h1');
if (h1 && !rm) {
var n = 0;
var split = function(node){
Array.prototype.slice.call(node.childNodes).forEach(function(ch){
if (ch.nodeType === 3) {
var parts = ch.textContent.split(/(\s+)/).filter(function(t){ return t.length; });
if (!parts.length) return;
var frag = document.createDocumentFragment();
parts.forEach(function(p){
if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
var w = document.createElement('span');
w.className = 'w';
w.textContent = p;
w.style.setProperty('--d', (80 + n++ * 38) + 'ms');
frag.appendChild(w);
});
node.replaceChild(frag, ch);
} else if (ch.nodeType === 1 && ch.tagName !== 'BR') {
split(ch);
}
});
};
split(h1);
}
var pending = [];
var targets = document.querySelectorAll('[data-reveal]');
var play = function(el){
var d = parseInt(el.getAttribute('data-reveal'), 10) || 0;
setTimeout(function(){ el.classList.add('is-in'); }, d);
};
if (rm || !('IntersectionObserver' in window)) {
targets.forEach(function(el){ el.classList.add('is-in'); });
} else {
var io = new IntersectionObserver(function(entries){
entries.forEach(function(e){
if (!e.isIntersecting) return;
io.unobserve(e.target);
var i = pending.indexOf(e.target);
if (i > -1) pending.splice(i, 1);
play(e.target);
});
}, { rootMargin: '0px 0px -12% 0px', threshold: 0.01 });
targets.forEach(function(el){ pending.push(el); io.observe(el); });
}
if (!rm && 'IntersectionObserver' in window) {
var cio = new IntersectionObserver(function(entries){
entries.forEach(function(e){
if (!e.isIntersecting) return;
cio.unobserve(e.target);
var node = e.target.firstChild;
var target = parseInt(node.textContent, 10);
var dur = 1200, t0 = performance.now();
var tick = function(t){
var p = Math.min(1, (t - t0) / dur);
node.textContent = String(Math.round(target * (1 - Math.pow(1 - p, 3))));
if (p < 1) requestAnimationFrame(tick);
};
requestAnimationFrame(tick);
});
}, { threshold: 0.4 });
document.querySelectorAll('.stat-value').forEach(function(el){
var f = el.firstChild;
if (f && f.nodeType === 3 && /^\d+$/.test(f.textContent.trim())) cio.observe(el);
});
}
if (!rm && matchMedia('(hover:hover)').matches) {
document.querySelectorAll('.card, .stat, .vcard').forEach(function(card){
var img = card.querySelector('img');
var S = { v: 0, x: 0, tx: 0, rx: 0, ry: 0, trx: 0, try_: 0, raf: null };
var K = 0.13, D = 0.78;
var frame = function(){
S.v += (S.tx - S.x) * K; S.v *= D; S.x += S.v;
S.rx += (S.trx - S.rx) * 0.16; S.ry += (S.try_ - S.ry) * 0.16;
var lift = S.x;
card.style.transform = 'perspective(900px) translate3d(0,' + (-lift * 12).toFixed(2) + 'px,0) rotateX(' + S.rx.toFixed(3) + 'deg) rotateY(' + S.ry.toFixed(3) + 'deg) scale(' + (1 + lift * 0.022).toFixed(4) + ')';
card.style.boxShadow = lift > 0.004 ? '0 ' + (lift * 26).toFixed(1) + 'px ' + (lift * 52).toFixed(1) + 'px rgba(0,0,0,' + (lift * 0.5).toFixed(3) + ')' : 'none';
if (img) img.style.transform = 'scale(' + (1 + lift * 0.075).toFixed(4) + ')';
var settled = Math.abs(S.tx - S.x) < 0.0012 && Math.abs(S.v) < 0.0012 && Math.abs(S.trx - S.rx) < 0.01 && Math.abs(S.try_ - S.ry) < 0.01;
S.raf = settled ? null : requestAnimationFrame(frame);
};
var kick = function(){ if (S.raf == null) S.raf = requestAnimationFrame(frame); };
card.addEventListener('mouseenter', function(){ S.tx = 1; kick(); });
card.addEventListener('mousemove', function(ev){
var r = card.getBoundingClientRect();
var px = (ev.clientX - r.left) / r.width - 0.5;
var py = (ev.clientY - r.top) / r.height - 0.5;
S.try_ = px * 7; S.trx = -py * 7; kick();
});
card.addEventListener('mouseleave', function(){ S.tx = 0; S.trx = 0; S.try_ = 0; kick(); });
});
}
var bgw = document.querySelector('[data-parallax]');
var heroIn = document.querySelector('.hero-in');
if (!rm && bgw) {
var ys = scrollY, idle = 0, raf = null;
var paint = function(y){
var vh = innerHeight || 1;
var p = Math.min(1, y / vh);
bgw.style.transform = 'translate3d(0,' + (y * 0.25).toFixed(1) + 'px,0)';
bgw.style.filter = 'brightness(' + (1 - p * 0.35).toFixed(3) + ')';
if (heroIn) {
heroIn.style.transform = 'translate3d(0,' + (y * 0.18).toFixed(1) + 'px,0)';
heroIn.style.opacity = String(Math.max(0, 1 - p * 1.3).toFixed(3));
}
};
var loop = function(){
var y = scrollY;
ys += (y - ys) * 0.14;
if (Math.abs(y - ys) < 0.15) ys = y;
paint(ys);
if (pending.length) {
var vh = innerHeight;
pending.slice().forEach(function(el){
var r = el.getBoundingClientRect();
if (r.top < vh * 0.94 && r.bottom > 0) { pending.splice(pending.indexOf(el), 1); play(el); }
});
}
idle = Math.abs(y - ys) > 0.15 ? 0 : idle + 1;
raf = idle > 90 ? null : requestAnimationFrame(loop);
};
var kickLoop = function(){ idle = 0; if (raf == null) raf = requestAnimationFrame(loop); };
addEventListener('scroll', kickLoop, { passive: true });
addEventListener('resize', kickLoop);
raf = requestAnimationFrame(loop);
}
var burger = document.querySelector('[data-burger]');
var mnav = document.querySelector('[data-mnav]');
if (burger && mnav) {
burger.addEventListener('click', function(){
var open = mnav.classList.toggle('is-open');
burger.setAttribute('aria-expanded', open ? 'true' : 'false');
});
mnav.addEventListener('click', function(e){
if (e.target.closest('a')) {
mnav.classList.remove('is-open');
burger.setAttribute('aria-expanded', 'false');
}
});
}
document.addEventListener('click', function(e){
var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
if (!a) return;
var id = a.getAttribute('href');
if (!id || id === '#') return;
var el = document.querySelector(id);
if (!el) return;
e.preventDefault();
var y = el.getBoundingClientRect().top + scrollY - 76;
scrollTo({ top: y, behavior: rm ? 'auto' : 'smooth' });
if (history.replaceState) history.replaceState(null, '', id);
});
var lb = document.querySelector('[data-lb]');
if (lb) {
var lbImg = lb.querySelector('img');
var last = null;
document.addEventListener('click', function(e){
var b = e.target.closest ? e.target.closest('button.shot') : null;
if (!b) return;
var img = b.querySelector('img');
if (!img) return;
last = b;
lbImg.src = img.currentSrc || img.src;
lbImg.alt = img.alt || '';
lb.classList.add('is-open');
document.body.style.overflow = 'hidden';
lb.querySelector('.lb-close').focus();
});
function close(){
lb.classList.remove('is-open');
lbImg.removeAttribute('src');
document.body.style.overflow = '';
if (last) last.focus();
}
lb.addEventListener('click', function(e){
if (e.target === lb || e.target.closest('.lb-close')) close();
});
addEventListener('keydown', function(e){
if (e.key === 'Escape' && lb.classList.contains('is-open')) close();
});
}
})();