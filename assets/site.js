/* Шапка: список языков, меню на телефоне, подсказка о версии на языке браузера. Ставит tools/nav.py. */
(function () {
  var h = document.querySelector('header.hd'); if (!h) return;
  var lb = h.querySelector('.lbtn'), lm = h.querySelector('.lmenu'), bg = h.querySelector('.burger');
  function closeL() { if (lm && !lm.hidden) { lm.hidden = true; lb.setAttribute('aria-expanded', 'false'); } }
  function closeM() { if (h.classList.contains('open')) { h.classList.remove('open'); bg.setAttribute('aria-expanded', 'false'); } }
  if (lb) lb.addEventListener('click', function (e) {
    e.stopPropagation(); var open = lm.hidden; closeM();
    lm.hidden = !open; lb.setAttribute('aria-expanded', String(open));
    if (open) { var a = lm.querySelector('a.on') || lm.querySelector('a'); if (a) a.focus(); }
  });
  if (bg) bg.addEventListener('click', function (e) {
    e.stopPropagation(); var open = !h.classList.contains('open'); closeL();
    h.classList.toggle('open', open); bg.setAttribute('aria-expanded', String(open));
  });
  h.querySelector('.hd-menu').addEventListener('click', function (e) { if (e.target.closest('a')) closeM(); });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.lsw')) closeL();
    if (!e.target.closest('.hd-menu')) closeM();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { if (lm && !lm.hidden) { closeL(); lb.focus(); } closeM(); }
  });

  // Подсказка: язык браузера не совпадает с языком страницы, а версия на нём есть. Сама не перебрасывает.
  var KEY = 'pisar-lang-hint';
  try { if (localStorage.getItem(KEY)) return; } catch (e) {}
  if (!lm) return;
  var page = h.getAttribute('data-lang'), want = null;
  var have = [].map.call(lm.querySelectorAll('[lang]'), function (x) { return x.getAttribute('lang'); });
  var nav = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ''];
  for (var i = 0; i < nav.length; i++) {
    var c = String(nav[i]).slice(0, 2).toLowerCase();
    if (have.indexOf(c) >= 0) { want = c; break; }
  }
  if (!want || want === page) return;
  var a = lm.querySelector('a[hreflang="' + want + '"][data-hint]'); if (!a) return;
  function remember() { try { localStorage.setItem(KEY, '1'); } catch (e) {} }
  var bar = document.createElement('div'); bar.className = 'lhint'; bar.setAttribute('lang', want);
  var w = document.createElement('div'); w.className = 'wrap';
  var link = document.createElement('a'); link.href = a.getAttribute('href'); link.textContent = a.getAttribute('data-hint');
  link.addEventListener('click', remember);
  var x = document.createElement('button'); x.type = 'button'; x.textContent = '×';
  x.setAttribute('aria-label', a.getAttribute('data-close') || 'Close');
  x.addEventListener('click', function () { bar.remove(); remember(); });
  w.appendChild(link); w.appendChild(x); bar.appendChild(w); h.insertBefore(bar, h.firstChild);
})();
