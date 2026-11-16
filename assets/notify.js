// Форма «Сообщить о выходе» на /mac/ (чат 35): почта уходит в лист ожидания облака Pro (адрес в action формы,
// CORS там открыт только для https://pisar-app.ru). Тексты ответов на языке страницы лежат в data-* формы.
// lang — язык страницы (<html lang>, чат 40): письмо о выходе Mac напишем на нём; облако берёт только 10 кодов сайта.
// Без ответа облака (ещё не обновлено, нет сети) форма пишет «не получилось», страница работает как была.
(function () {
  var f = document.querySelector('form.notify');
  if (!f || !window.fetch) return;
  var inp = f.querySelector('input[name=email]'), hp = f.querySelector('input[name=website]');
  var btn = f.querySelector('button'), msg = f.querySelector('.nmsg');
  var RE = /^[^\s@]+@[^\s@.]+(\.[^\s@.]+)*\.[^\s@.]{2,}$/;
  function say(key, cls) {
    msg.textContent = (key && f.dataset[key]) || '';
    msg.className = 'nmsg' + (cls ? ' ' + cls : '');
  }
  function bad(key) {
    inp.setAttribute('aria-invalid', 'true');
    say(key, 'err');
    inp.focus();
  }
  inp.addEventListener('input', function () {
    inp.removeAttribute('aria-invalid');
    if (msg.classList.contains('err')) say('', '');
  });
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    if (btn.disabled) return;
    var v = inp.value.trim();
    if (!v) return bad('empty');
    if (v.length > 254 || !RE.test(v)) return bad('bad');
    btn.disabled = true;
    say('wait', '');
    var ctl = window.AbortController ? new AbortController() : null;
    var timer = ctl ? setTimeout(function () { ctl.abort(); }, 15000) : 0;
    fetch(f.action, {
      method: 'POST', mode: 'cors', credentials: 'omit', signal: ctl ? ctl.signal : undefined,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: v, website: hp ? hp.value : '', lang: document.documentElement.lang || '' })
    }).then(function (r) {
      if (r.ok) { inp.value = ''; return say('ok', 'ok'); }
      return r.json().catch(function () { return {}; }).then(function (d) {
        if (r.status === 400 && d && d.error === 'email') bad('bad');
        else say(r.status === 429 ? 'many' : 'err', 'err');
      });
    }).catch(function () {
      say('err', 'err');
    }).then(function () {
      clearTimeout(timer);
      btn.disabled = false;
    });
  });
})();
