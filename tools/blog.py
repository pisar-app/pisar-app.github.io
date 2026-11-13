# Порядок запуска из корня сайта: 1) python3 tools/blog.py .  2) python3 tools/footer.py .  3) python3 tools/nav.py .
# Генератор статей Писаря: /ru/blog/<slug>/ и /ru/blog/. python3 blog.py <site_root>
import sys, os, json, re, html
ROOT = sys.argv[1]
SITE = 'https://pisar-app.ru'
DATE = '2026-11-13'
_home = open(os.path.join(ROOT, 'index.html')).read()
BASE_CSS = re.search(r'<style>(.*?)</style>', _home, re.S).group(1)
DEFS = re.search(r'(<svg width="0" height="0".*?</svg>)', _home, re.S).group(1)
EXTRA_CSS = '''
/* статьи */
header{position:absolute}
.post{padding:112px 0 80px}
.narrow{max-width:760px}
.crumbs{display:flex;gap:8px;font-size:14px;color:var(--muted);margin-bottom:18px}
.crumbs a:hover{color:var(--fg)}
.post h1{font-size:clamp(32px,5vw,48px);line-height:1.1;letter-spacing:-.03em;margin:0 0 16px}
.post .lead{font-size:20px;line-height:1.5;color:var(--muted);margin:0 0 32px;max-width:720px}
article{font-size:17.5px;line-height:1.7}
article h2{font-size:26px;line-height:1.2;letter-spacing:-.02em;margin:44px 0 12px}
article p{margin:0 0 16px}
article ul,article ol{margin:0 0 18px;padding-left:24px}
article li{margin:6px 0}
article ul.plain{list-style:none;padding-left:0}
article ul.plain li{padding-left:22px;position:relative}
article ul.plain li:before{content:"";position:absolute;left:2px;top:.8em;width:10px;height:2px;border-radius:1px;background:var(--muted)}
article b{font-weight:600}
.t{border-collapse:collapse;width:100%;margin:8px 0 18px;font-size:16px;background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:table}
.t th,.t td{padding:12px 14px;text-align:left;border-top:1px solid var(--line);vertical-align:top}
.t th{font-size:13px;font-weight:600;color:var(--muted);border-top:0;background:var(--chip)}
.cta{display:flex;align-items:center;gap:18px;margin-top:48px;padding:24px;border-radius:22px;background:var(--hero);border:1px solid var(--line)}
.cta .pb{width:56px;height:56px;border-radius:16.8px}
.cta-t{flex:1;display:flex;flex-direction:column;gap:4px}
.cta-t b{font-size:18px}.cta-t span{color:var(--muted);font-size:15px}
.cta-b{display:flex;flex-direction:column;align-items:center;gap:6px}
.cta-b small{color:var(--muted);font-size:12.5px}
.related{padding:48px 0 0;border-top:1px solid var(--line);margin-top:56px}
.ahead{background:var(--hero);background-origin:border-box;padding:112px 0 36px;margin-bottom:8px}
.post:has(>.ahead){padding-top:0!important}
.ahead h1{margin-bottom:12px}
.ahead .lead{margin-bottom:16px;color:var(--fg);opacity:.78}
.meta{display:flex;gap:12px;align-items:center;font-size:14px;color:var(--muted)}
.scen{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:8px 0 8px}
.sc{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px}
.sc .mi{font-size:22px;color:var(--accent)}
.sc b{display:block;margin:8px 0 4px;font-size:16px}
.sc p{margin:0;font-size:14.5px;line-height:1.5;color:var(--muted)}
.howto{display:grid;grid-template-columns:minmax(0,1fr) 240px;gap:28px;align-items:start;margin:8px 0}
.steps{list-style:none;counter-reset:st;padding:0!important;margin:0!important}
.steps li{counter-increment:st;position:relative;padding:14px 16px 14px 56px;margin:0 0 10px!important;background:var(--card);border:1px solid var(--line);border-radius:16px;font-size:16px;line-height:1.5}
.steps li:before{content:counter(st);position:absolute;left:14px;top:13px;width:28px;height:28px;border-radius:9px;background:#F5A524;color:#16161A;font-weight:800;font-size:15px;display:grid;place-items:center}
.appshot{margin:0;background:#0b0d1c;padding:7px;border-radius:30px;box-shadow:0 0 0 1px rgba(255,255,255,.18),0 24px 60px -24px rgba(60,40,160,.55)}
.appshot img{display:block;width:100%;height:auto;border-radius:24px}
.appshot figcaption{font-size:12.5px;color:#a3a2c2;text-align:center;padding:8px 4px 2px}
.ex{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px;margin:8px 0 8px}
.ex-in{display:flex;gap:10px;align-items:center}
.ex-in .mi{width:36px;height:36px;border-radius:10px;background:var(--chip);display:grid;place-items:center;font-size:20px;color:var(--accent)}
.ex-in b{display:block;font-size:15px}.ex-in small{color:var(--muted);font-size:13px}
.ex-arr{display:grid;place-items:center;color:var(--accent);padding:6px 0}
.ex-out{margin:0!important;background:var(--chip);border-radius:12px;padding:12px 14px;font-size:16px}
ul.ticks{list-style:none;padding-left:0!important}
ul.ticks li{position:relative;padding-left:28px}
ul.ticks li:before{content:"";position:absolute;left:2px;top:.45em;width:14px;height:8px;border-left:2.5px solid var(--ok);border-bottom:2.5px solid var(--ok);transform:rotate(-45deg)}
.cta{background-origin:border-box}
.art .thumb:has(img){height:150px;overflow:hidden;background:var(--chip)}
.art .thumb:has(img):after{display:none}
.art .thumb img{width:100%;height:100%;object-fit:cover;object-position:center 18%;display:block}
@media (max-width:700px){.scen{grid-template-columns:1fr}.howto{grid-template-columns:1fr}.howto .appshot{max-width:260px;margin:0 auto}.ahead{padding:104px 0 24px}}
.related h2{font-size:28px;margin:0}
.back{margin:28px 0 0;text-align:center}.back a{font-weight:600;color:var(--accent)}
.art p{margin:0;color:var(--muted);font-size:15px}
.art .thumb{display:grid;place-items:center}
.art .thumb .mi{font-size:44px;color:var(--fg);opacity:.75;position:relative;z-index:1}
.art .badge{align-self:flex-start}
.art:hover h2,.art:hover h3{text-decoration:underline;text-underline-offset:3px}
.list.grid3 .art h2{font-size:20px;margin:6px 0 0;letter-spacing:-.01em;line-height:1.25}
@media (max-width:700px){.cta{flex-direction:column;text-align:center}.post{padding-top:118px}article{font-size:16.5px}article h2{font-size:22px}}
'''

ARTS = [
 dict(slug='kak-pechatat-golosom-na-android', cover='slovar', icon='keyboard_voice',
  title='Как печатать голосом на Android: 3 способа',
  desc='Голосовой ввод на Android: микрофон в клавиатуре, приложение-блокнот и Писарь. Чем отличаются и что выбрать.',
  lead='Говорить быстрее и удобнее, чем попадать по маленьким клавишам. На Android для этого есть три пути, и они заметно отличаются.',
  body='''
<h2>Способ 1. Микрофон в клавиатуре</h2>
<p>Значок микрофона есть почти в каждой клавиатуре. Ничего не нужно ставить: коснулись, сказали, текст появился.</p>
<ul><li>Во многих клавиатурах речь распознаётся через интернет: в метро и за городом ввод не работает.</li>
<li>Знаки препинания и заглавные буквы ставятся не всегда.</li>
<li>Своих слов, имён и терминов клавиатура не знает.</li></ul>

<h2>Способ 2. Приложение-блокнот</h2>
<p>Отдельное приложение для заметок голосом: надиктовали, скопировали, перешли в мессенджер, вставили. Подходит для длинных заметок, но каждый раз это лишние шаги.</p>

<h2>Способ 3. Писарь: кнопка у любого поля</h2>
<p>Поставьте курсор в любое поле: мессенджер, почта, заметки, поиск. Рядом появится кнопка P. Коснитесь и говорите или зажмите и держите, пока говорите. Текст встанет туда, где курсор.</p>
<ul><li>Распознавание идёт на телефоне, без интернета. Звук и текст не уходят с телефона.</li>
<li>Знаки, заглавные и числа цифрами Писарь ставит сам: «двадцать пять задач» станет «25 задач».</li>
<li>Свой словарь без лимита: как писать имена и термины.</li>
<li>Клавиатура остаётся прежней: Писарь не клавиатура, а кнопка рядом с полем.</li></ul>

<h2>Как начать с Писарем</h2>
<ol><li><b>Установите</b> Писарь из RuStore. Аккаунт не нужен.</li>
<li><b>Выберите язык</b> один раз: «Только русский» или «Все языки».</li>
<li><b>Дайте разрешения:</b> микрофон и «Специальные возможности». Через эту службу Писарь видит поле ввода, показывает кнопку и вставляет текст. Поля паролей он не читает.</li>
<li><b>Коснитесь P</b> у любого поля и говорите.</li></ol>

<h2>Чтобы текст получался чище</h2>
<ul><li>Говорите целыми фразами, без долгих пауз посреди мысли.</li>
<li>Включите чистку речи: Писарь уберёт «ну», «короче», повторы и оговорки.</li>
<li>Добавьте в словарь имена и термины, которые часто пишете.</li>
<li>Заведите быстрые фразы: говорите «мой адрес», вставляется полный адрес.</li></ul>
'''),
 dict(slug='golosovoy-vvod-bez-interneta', cover='rasp', icon='wifi_off',
  title='Голосовой ввод без интернета на Android',
  desc='Как диктовать текст на Android без интернета: распознавание речи прямо на телефоне, 25 языков, голос не уходит в облако.',
  lead='Обычный голосовой ввод отправляет запись на сервер и ждёт ответа. Писарь распознаёт речь прямо на телефоне: связь не нужна, а голос остаётся у вас.',
  body='''
<h2>Когда это важно</h2>
<ul><li>В метро, в самолёте, за городом, где связь пропадает.</li>
<li>Когда мобильный интернет медленный или закончился.</li>
<li>Когда не хочется, чтобы голос и тексты уходили в чужое облако.</li></ul>

<h2>Как это устроено</h2>
<p>Язык скачивается на телефон один раз. Дальше Писарь работает без сети: звук обрабатывает сам телефон, и текст сразу встаёт в поле.</p>
<table class="t"><thead><tr><th>Язык</th><th>Для чего</th></tr></thead><tbody>
<tr><td>Только русский</td><td>Быстрее и точнее на русском</td></tr>
<tr><td>Все языки</td><td>25 европейских языков, язык Писарь определит сам</td></tr></tbody></table>
<p>Что входит в «Все языки»: русский, английский, украинский, немецкий, французский, испанский, итальянский, португальский, польский, нидерландский, чешский, словацкий, болгарский, хорватский, словенский, румынский, венгерский, греческий, шведский, датский, финский, эстонский, латышский, литовский, мальтийский.</p>

<h2>Как включить</h2>
<ol><li>Откройте Писарь: Настройки → Распознавание.</li>
<li>Скачайте «Только русский» или «Все языки». Лучше по Wi-Fi: Писарь спросит, если вы в мобильной сети.</li>
<li>Готово: кнопка P у любого поля работает и без интернета.</li></ol>

<h2>Что всё же уходит в сеть</h2>
<p>Звук, тексты, имена файлов и программ не уходят. Интернет нужен, только чтобы один раз скачать язык, расшифровать файл по ссылке и оплатить Pro. Анонимную статистику сбоев можно выключить: Настройки → Помощь и связь → О программе.</p>

<h2>Честно об ограничениях</h2>
<ul class="plain"><li>Иногда ошибается: в шуме, при быстрой речи, в редких словах. Словарь помогает.</li>
<li>Языки занимают место на телефоне.</li>
<li>На старых телефонах распознавание медленнее.</li>
<li>Нужен Android 10 и новее, 64-битный процессор.</li></ul>
'''),
 dict(slug='golosovoe-soobshchenie-v-tekst', cover='rassh', icon='graphic_eq', pro=True,
  title='Как перевести голосовое сообщение в текст',
  desc='Голосовые сообщения, аудио и видео в текст на Android: поделитесь файлом с Писарем, расшифровка идёт на телефоне, без лимитов.',
  lead='Длинное голосовое неудобно слушать в транспорте или на встрече. Его можно не слушать, а прочитать.',
  body='''
<h2>Когда это выручает</h2>
<div class="scen">
<div class="sc"><span class="mi">directions_bus</span><b>В транспорте без наушников</b><p>Голосовое пришло, а слушать негде. Открыли текст и прочитали.</p></div>
<div class="sc"><span class="mi">groups</span><b>На встрече</b><p>Звук не включишь, а ответить надо. Текст можно пробежать глазами.</p></div>
<div class="sc"><span class="mi">search</span><b>Найти адрес или время</b><p>Длинное голосовое не надо переслушивать: нужное место видно в тексте.</p></div>
</div>

<h2>Как перевести голосовое в текст</h2>
<div class="howto">
<ol class="steps">
<li><b>Зажмите голосовое</b> в Telegram или WhatsApp.</li>
<li><b>Нажмите «Поделиться»</b> и выберите Писарь.</li>
<li><b>Откройте вкладку «Расшифровка»</b>: голосовое уже там текстом. Его можно скопировать или найти по слову.</li>
</ol>
<figure class="appshot"><img src="/assets/shots/rassh.webp" alt="Вкладка «Расшифровка» в Писаре: голосовое и видео уже текстом"><figcaption>Вкладка «Расшифровка» в Писаре</figcaption></figure>
</div>

<h2>Как это выглядит</h2>
<div class="ex">
<div class="ex-in"><span class="mi">mic_none</span><div><b>Голосовое · 1:24</b><small>Telegram</small></div></div>
<div class="ex-arr"><span class="mi">south</span></div>
<p class="ex-out">Привет! По поводу субботы: собираемся в два у метро, Лёша берёт машину, с тебя мангал и уголь…</p>
</div>

<h2>Что ещё можно расшифровать</h2>
<ul class="ticks">
<li><b>Видео</b> с телефона или из соцсетей, тоже через «Поделиться».</li>
<li><b>Аудиозапись</b>: выберите файл прямо в Писаре.</li>
<li><b>Ссылку</b> на Google Диск, Яндекс Диск, Dropbox или подкаст.</li>
</ul>
<p>Длинные записи расшифровываются в фоне, ход видно в уведомлении. Распознавание идёт на самом телефоне: голосовые не уходят на чужие серверы.</p>

<h2>Сколько стоит</h2>
<div class="howto">
<div>
<p>Расшифровка входит в <b>Писарь Pro</b>: 399 ₽ один раз, без подписки. Первые 7 дней бесплатно, лимитов на длину и количество файлов нет.</p>
<p>Если после пробных дней Pro не покупать, готовые тексты останутся у вас, а диктовка, словарь и правила текста продолжат работать бесплатно.</p>
</div>
<figure class="appshot"><img src="/assets/shots/pro.webp" alt="Экран «Писарь Pro» в приложении"><figcaption>Экран Pro в приложении</figcaption></figure>
</div>
'''),
 dict(slug='tekst-so-skrinshota', cover='bufer', icon='image', pro=True,
  title='Как скопировать текст со скриншота или фото',
  desc='Как достать текст из картинки на Android: поделитесь скриншотом или фото с Писарем, текст распознается на телефоне.',
  lead='Номер заказа на скриншоте, адрес на фото вывески, текст в приложении, где он не выделяется. Перепечатывать его вручную не нужно.',
  body='''
<h2>Когда пригодится</h2>
<ul><li>Текст в приложении не выделяется и не копируется.</li>
<li>Прислали скриншот с номером заказа, адресом или реквизитами.</li>
<li>Нужно переписать объявление, расписание или страницу книги с фото.</li></ul>

<h2>Как это сделать</h2>
<ol><li>Сделайте скриншот или откройте фото в галерее.</li>
<li>Нажмите «Поделиться» и выберите Писарь.</li>
<li>Текст с картинки появится во вкладке «Расшифровка». Скопируйте его целиком или нужный кусок.</li></ol>

<h2>Без интернета</h2>
<p>Текст распознаётся на телефоне. Картинка никуда не отправляется, поэтому так можно разбирать и личные документы.</p>

<h2>Сколько стоит</h2>
<p>Текст со скриншотов и фото входит в Писарь Pro: 399 ₽ один раз, без подписки. Первые 7 дней Pro бесплатно. В Pro также расшифровка голосовых, Буфер со всем скопированным и перевод при диктовке.</p>
'''),
 dict(slug='golosovoy-vvod-dlya-pozhilyh', cover='dikt2', icon='elderly',
  title='Телефон пожилому родителю: как писать голосом',
  desc='Как настроить голосовой ввод на Android для пожилых родителей: кнопка у любого поля, без рекламы и аккаунта, работает без интернета.',
  lead='Мелкие клавиши, слабое зрение, уставшие руки: родителям часто трудно набирать сообщения. Проще сказать, а телефон напишет.',
  body='''
<h2>Почему голосом проще</h2>
<ul><li>Не нужно попадать по маленьким буквам.</li>
<li>Знаки препинания и заглавные Писарь ставит сам.</li>
<li>Одна и та же кнопка P у любого поля: в мессенджере, в почте, в поиске.</li></ul>

<h2>Настройте вместе за один раз</h2>
<ol><li>Установите Писарь из RuStore. Аккаунт не нужен.</li>
<li>Выберите язык «Только русский» и скачайте его, лучше по Wi-Fi.</li>
<li>Дайте разрешения: микрофон и «Специальные возможности». Писарь объяснит, зачем каждое.</li>
<li>Покажите кнопку P: коснуться и говорить или зажать и держать, пока говоришь. Можно выбрать то, что удобнее.</li>
<li>Если кнопка мешает, её можно передвинуть или сделать прозрачнее.</li></ol>

<h2>Чего не будет</h2>
<ul class="plain"><li>Рекламы: её в Писаре нет совсем.</li>
<li>Подписок: диктовка бесплатна навсегда.</li>
<li>Аккаунтов и паролей: ничего не нужно заводить.</li></ul>

<h2>Если кнопка пропадает</h2>
<p>На некоторых телефонах, например Xiaomi, система сама выключает фоновые программы. Откройте в Писаре Настройки → Разрешения и включите автозапуск, работу батареи без ограничений и всплывающие окна в фоне.</p>

<h2>Полезные мелочи</h2>
<ul><li>Музыка и видео приглушаются, пока человек говорит.</li>
<li>Быстрые фразы: сказать «мой адрес», и вставится полный адрес.</li>
<li>Писарь работает без интернета, в том числе на даче.</li></ul>
'''),
]

def page(title, desc, canon, body, ld, extra_css=''):
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<link rel="icon" type="image/png" href="/assets/icon.png">
<meta property="og:type" content="article">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="Писарь">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons+Outlined" rel="stylesheet">
<link rel="stylesheet" href="/assets/blog.css">
<script>(function(){{var p=new URLSearchParams(location.search).get('t');var s=null;try{{s=localStorage.getItem('theme')}}catch(e){{}}var t=p||s;if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}})();</script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
{DEFS}
<header>
  <div class="wrap bar">
    <a class="logo" href="/"><img src="/assets/icon.png" alt="">Писарь</a>
    <nav class="menu"><a href="/#all">Возможности</a><a href="/#pro">Pro</a><a href="/ru/blog/">Статьи</a><a href="/#faq">Вопросы</a></nav>
    <div class="spacer"></div>
    <button class="tbtn" id="tbtn" aria-label="Светлая или тёмная тема"><svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg><svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></button>
  </div>
</header>
{body}
<footer>
  <div class="wrap f">
    <a class="logo" href="/"><img src="/assets/icon.png" alt="" style="width:24px;height:24px;border-radius:7px">Писарь</a>
    <a href="/ru/pro/">Писарь Pro</a>
    <a href="/ru/blog/">Статьи</a>
    <a href="/ru/privacy/">Политика конфиденциальности</a>
    <a href="/ru/terms/">Пользовательское соглашение</a>
    <a href="/en/privacy/">English</a>
    <span class="spacer"></span>
    <span>© 2026 Pozdnekov Labs</span>
  </div>
</footer>
<script>(function(){{var r=document.documentElement;function d(){{var t=r.getAttribute('data-theme');return t?t==='dark':matchMedia('(prefers-color-scheme: dark)').matches}}document.getElementById('tbtn').addEventListener('click',function(){{var t=d()?'light':'dark';r.setAttribute('data-theme',t);try{{localStorage.setItem('theme',t)}}catch(e){{}}}})}})();</script>
</body>
</html>
'''

STORE = '<a class="store" aria-label="Скоро в RuStore"><img class="only-light" src="/assets/rustore-color-dark.svg" alt="Скачайте из RuStore"><img class="only-dark" src="/assets/rustore-color-light.svg" alt="Скачайте из RuStore"></a>'

def card(a, h='h3'):
    tag = '<span class="badge pro">Pro</span>' if a.get('pro') else ''
    return f'<a class="art" href="/ru/blog/{a["slug"]}/"><div class="thumb"><img src="/assets/shots/{a["cover"]}.webp" alt="" style="object-position:center {a.get("pos","8%")}"></div><{h}>{a["title"]}</{h}><p>{a["desc"]}</p>{tag}</a>'

for a in ARTS:
    canon = f'{SITE}/ru/blog/{a["slug"]}/'
    others = [o for o in ARTS if o is not a][:3]
    cta_sub = 'Писарь Pro: 399 ₽ один раз, первые 7 дней бесплатно.' if a.get('pro') else 'Диктовка бесплатно навсегда. Без рекламы и аккаунта.'
    read = max(2, round(len(re.sub('<[^>]+>', '', a["body"]).split()) / 160))
    tag = '<span class="badge pro">Pro</span>' if a.get('pro') else '<span class="badge">Бесплатно</span>'
    body = f'''<main class="post">
  <section class="ahead">
    <div class="wrap narrow">
      <nav class="crumbs"><a href="/">Писарь</a><span>/</span><a href="/ru/blog/">Статьи</a></nav>
      <h1>{a["title"]}</h1>
      <p class="lead">{a["lead"]}</p>
      <div class="meta">{tag}<span>{read} мин чтения</span></div>
    </div>
  </section>
  <div class="wrap narrow">
    <article>{a["body"]}</article>
    <div class="cta">
      <span class="pb"><svg class="plogo"><use href="#plogo"/></svg></span>
      <div class="cta-t"><b>Писарь: диктовка без интернета</b><span>{cta_sub}</span></div>
      <div class="cta-b">{STORE}<small>Скоро в RuStore</small></div>
    </div>
  </div>
  <section class="related">
    <div class="wrap narrow"><h2>Ещё статьи</h2><div class="grid3">{"".join(card(o) for o in others)}</div><p class="back"><a href="/ru/blog/">← Все статьи</a></p></div>
  </section>
</main>'''
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"],
           "datePublished": DATE, "dateModified": DATE, "inLanguage": "ru", "mainEntityOfPage": canon,
           "image": f"{SITE}/assets/og.png",
           "author": {"@type": "Organization", "name": "Pozdnekov Labs"},
           "publisher": {"@type": "Organization", "name": "Pozdnekov Labs", "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/icon.png"}}},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Писарь", "item": f"{SITE}/"},
              {"@type": "ListItem", "position": 2, "name": "Статьи", "item": f"{SITE}/ru/blog/"},
              {"@type": "ListItem", "position": 3, "name": a["title"], "item": canon}]}]
    d = os.path.join(ROOT, 'ru', 'blog', a['slug']); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w').write(page(a['title'] + ' | Писарь', a['desc'], canon, body, ld))

open(os.path.join(ROOT, 'assets', 'blog.css'), 'w').write(BASE_CSS + EXTRA_CSS)
# список статей
body = f'''<main class="post">
  <section class="ahead"><div class="wrap">
    <nav class="crumbs"><a href="/">Писарь</a><span>/</span><span>Статьи</span></nav>
    <h1>Как писать голосом</h1>
    <p class="lead">Короткие инструкции: голосовой ввод на Android, диктовка без интернета, голосовые и скриншоты в текст.</p>
  </div></section>
  <div class="wrap">
    <div class="grid3 list">{"".join(card(a, 'h2') for a in ARTS)}</div>
  </div>
</main>'''
ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Статьи Писаря", "url": f"{SITE}/ru/blog/",
      "hasPart": [{"@type": "Article", "headline": a["title"], "url": f"{SITE}/ru/blog/{a['slug']}/"} for a in ARTS]}
os.makedirs(os.path.join(ROOT, 'ru', 'blog'), exist_ok=True)
open(os.path.join(ROOT, 'ru', 'blog', 'index.html'), 'w').write(page('Статьи: как писать голосом | Писарь', 'Инструкции по голосовому вводу на Android: диктовка без интернета, голосовые и скриншоты в текст, телефон для пожилых.', f'{SITE}/ru/blog/', body, ld))

# карточки для главной
open(os.path.join(os.path.dirname(__file__), 'home_cards.html'), 'w').write(''.join(card(a) for a in ARTS[:3]))
# sitemap
urls = [('/', '1.0'), ('/ru/blog/', '0.7')] + [(f'/ru/blog/{a["slug"]}/', '0.7') for a in ARTS] + [('/ru/pro/', '0.8'), ('/ru/privacy/', '0.3'), ('/ru/terms/', '0.3')]
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{DATE}</lastmod><priority>{p}</priority></url>\n' for u, p in urls) + '</urlset>\n')
# проверка текстов
for dp, _, fs in os.walk(os.path.join(ROOT, 'ru', 'blog')):
    for f in fs:
        t = open(os.path.join(dp, f)).read()
        assert '—' not in t, (dp, 'long dash')
        assert 'GitHub' not in t and 'гитхаб' not in t.lower(), dp
        assert not re.search(r'\d+\s*секунд', t), dp
        assert 'МБ' not in t, (dp, 'megabytes')
print('ok', len(ARTS))
