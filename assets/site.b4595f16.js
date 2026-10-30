(function () {
  'use strict';
  var d = document, w = window, root = d.documentElement;
  var reduce = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function ev(name, params) { try { if (w.gtag) w.gtag('event', name, params || {}); } catch (e) {} }
  function store(k, v) { try { if (v === undefined) return sessionStorage.getItem(k); sessionStorage.setItem(k, v); } catch (e) {} return null; }
  var yr = d.getElementById('year'); if (yr) yr.textContent = new Date().getFullYear();
  var dds = [].slice.call(d.querySelectorAll('.dd'));
  function closeDD() { dds.forEach(function (x) { x.classList.remove('open'); x.querySelector('.dd-btn').setAttribute('aria-expanded', 'false'); }); }
  dds.forEach(function (dd) {
    var b = dd.querySelector('.dd-btn');
    b.addEventListener('click', function (e) {
      var was = dd.classList.contains('open'); closeDD();
      if (!was) { dd.classList.add('open'); b.setAttribute('aria-expanded', 'true'); }
      e.stopPropagation();
    });
  });
  d.addEventListener('click', function (e) { if (!e.target.closest('.dd')) closeDD(); });
  var mb = d.querySelector('.menu-btn'), mm = d.getElementById('mmenu');
  function closeMenu() { if (!mb) return; mb.setAttribute('aria-expanded', 'false'); mb.setAttribute('aria-label', 'Open menu'); mm.hidden = true; }
  if (mb && mm) {
    mb.addEventListener('click', function () {
      var open = mb.getAttribute('aria-expanded') === 'true';
      if (open) { closeMenu(); } else { mb.setAttribute('aria-expanded', 'true'); mb.setAttribute('aria-label', 'Close menu'); mm.hidden = false; }
    });
    mm.addEventListener('click', function (e) { if (e.target.closest('a')) closeMenu(); });
  }
  d.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeDD(); closeMenu(); } });
  root.classList.add('rv-ok');
  function countUp(el) {
    var end = parseFloat(el.getAttribute('data-count')), pre = el.getAttribute('data-prefix') || '', suf = el.getAttribute('data-suffix') || '';
    if (reduce) return;
    var t0 = null, dur = 1300;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - p, 3);
      el.textContent = pre + Math.round(end * e) + suf;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var rv = [].slice.call(d.querySelectorAll('.reveal'));
  if ('IntersectionObserver' in w) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('in'); io.unobserve(e.target);
        var c = e.target.querySelector('[data-count]'); if (c) countUp(c);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    rv.forEach(function (el) { io.observe(el); });
  } else { rv.forEach(function (el) { el.classList.add('in'); }); }
  var sc = d.getElementById('stickycta');
  if (sc && 'IntersectionObserver' in w) {
    var inview = {}, targets = [].slice.call(d.querySelectorAll('.fitcard, .site-footer'));
    var upd = function () {
      var any = false; for (var k in inview) { if (inview[k]) any = true; }
      var show = w.scrollY > 520 && !any;
      sc.classList.toggle('show', show);
    };
    var io2 = new IntersectionObserver(function (es) { es.forEach(function (e) { inview[targets.indexOf(e.target)] = e.isIntersecting; }); upd(); });
    targets.forEach(function (t) { io2.observe(t); });
    w.addEventListener('scroll', upd, { passive: true });
  }
  var q = new URLSearchParams(w.location.search);
  ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'gclid'].forEach(function (k) { if (q.get(k)) store('dt_' + k, q.get(k)); });
  if (!store('dt_landing')) { store('dt_landing', w.location.pathname); store('dt_ref', d.referrer || ''); }
  [].slice.call(d.querySelectorAll('.fitform')).forEach(function (f) {
    var card = f.closest('.fitcard'), started = false;
    function set(n, v) { var i = f.elements[n]; if (i) i.value = v || ''; }
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'gclid'].forEach(function (k) { set(k, store('dt_' + k)); });
    set('landing_page', store('dt_landing') || w.location.pathname);
    set('referrer', store('dt_ref') || d.referrer);
    var dots = card.querySelectorAll('.steps-dots span'), num = card.querySelector('[data-stepnum]');
    function go(n) {
      card.classList.toggle('is-step2', n === 2);
      if (dots.length) { dots[0].className = 'on'; dots[1].className = n === 2 ? 'on' : ''; }
      if (num) num.textContent = n;
      var focusEl = f.querySelector(n === 2 ? 'input[name=name]' : 'input[name=need]:checked');
      if (focusEl && n === 2) focusEl.focus({ preventScroll: true });
    }
    f.addEventListener('focusin', function () {
      if (started) return; started = true;
      ev('form_start', { form_location: f.getAttribute('data-form') });
    });
    var nx = f.querySelector('[data-next]'), bk = f.querySelector('[data-back]');
    if (nx) nx.addEventListener('click', function () {
      ev('form_step_complete', { form_location: f.getAttribute('data-form'), need: (f.elements.need || {}).value });
      go(2);
    });
    if (bk) bk.addEventListener('click', function () { go(1); });
    f.addEventListener('submit', function () {
      var need = (f.querySelector('input[name=need]:checked') || {}).value || '';
      var spend = (f.elements.spend || {}).value || '';
      set('_subject', 'New DigiTradie fit check: ' + need + ' | ' + spend + ' | ' + (f.elements.business || {}).value);
      ev('form_submit', { form_location: f.getAttribute('data-form'), need: need, spend: spend });
    });
  });
  d.addEventListener('click', function (e) {
    var a = e.target.closest('[data-cta],[data-track]'); if (!a) return;
    var c = a.getAttribute('data-cta'), t = a.getAttribute('data-track');
    if (c) ev('cta_click', { cta_location: c, link_url: a.getAttribute('href') });
    if (t === 'phone') ev('phone_click', { link_url: a.getAttribute('href') });
    if (t === 'email') ev('email_click', { link_url: a.getAttribute('href') });
  });
})();