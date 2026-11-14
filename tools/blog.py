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
@media(max-width:520px){.t{font-size:14px}.t th,.t td{padding:10px 8px;overflow-wrap:anywhere}}
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
.badge.pro{margin:0 6px 0 0;vertical-align:.12em}
.badge .mi{font-size:13px;margin-right:3px;vertical-align:-2px}
.bnav{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
.bnav a{padding:8px 14px;border-radius:999px;background:var(--card);border:1px solid var(--line);font-size:14px;font-weight:600}
.bsec{margin:40px 0 0;scroll-margin-top:90px}
.bsec>h2{font-size:28px;letter-spacing:-.02em;margin:0 0 6px}
.bsec>p{color:var(--muted);margin:0 0 18px}
.list.grid3 .art h3{font-size:19px;margin:6px 0 0;letter-spacing:-.01em;line-height:1.25}
article a:not(.art){color:var(--accent);text-decoration:underline;text-underline-offset:2px}
.ex-out.said{margin-top:10px!important;opacity:.75;font-style:italic}
.note{background:var(--chip);border-left:3px solid #F5A524;border-radius:10px;padding:12px 14px;margin:8px 0 18px;font-size:16px}
.pm{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:8px 0 18px}
.pm>div{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px 16px}
.pm h3{font-size:16px;margin:0 0 6px}
.pm ul{margin:0;padding-left:20px;font-size:16px}
@media (max-width:700px){.pm{grid-template-columns:1fr}}
.art:hover h2,.art:hover h3{text-decoration:underline;text-underline-offset:3px}
.list.grid3 .art h2{font-size:20px;margin:6px 0 0;letter-spacing:-.01em;line-height:1.25}
@media (max-width:700px){.cta{flex-direction:column;text-align:center}.post{padding-top:118px}article{font-size:16.5px}article h2{font-size:22px}}
'''

# Обложки og.png и thumb.webp: python3 ru/blog/_src/covers.py . (до этого скрипта).
# Тексты статей — ru/blog/_src/{free,pro,scen}.py (ведёт чат «Блог»), шаблон и стили — здесь.
SECTIONS = [('free', 'Бесплатные функции', 'Как устроена диктовка и всё, что работает без покупки.'),
            ('pro', 'Писарь Pro', 'Голосовые и скриншоты в текст, Буфер, перевод: 399 ₽ один раз.'),
            ('scen', 'Сценарии', 'Живые ситуации: что нажать и что получится.')]
ARTS = []
for _sec, _t, _d in SECTIONS:
    _ns = {'ROOT': ROOT}
    exec(open(os.path.join(ROOT, 'ru', 'blog', '_src', '_lib.py'), encoding='utf-8').read(), _ns)
    exec(open(os.path.join(ROOT, 'ru', 'blog', '_src', _sec + '.py'), encoding='utf-8').read(), _ns)
    for _a in _ns['ARTS']:
        _a['sec'] = _sec
        ARTS.append(_a)
BY = {a['slug']: a for a in ARTS}
PRO_TAG = '<span class="badge pro"><span class="mi">lock</span>Pro</span>'

def page(title, desc, canon, body, ld, extra_css='', og=None):
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
<meta property="og:image" content="{og or SITE + '/assets/og.png'}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{og or SITE + '/assets/og.png'}">
{extra_css}
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
    tag = PRO_TAG if a.get('pro') else ''
    return f'<a class="art" href="/ru/blog/{a["slug"]}/"><div class="thumb"><img src="/ru/blog/{a["slug"]}/thumb.webp" alt="" loading="lazy" style="object-position:center"></div><{h}>{tag}{a["title"]}</{h}><p>{a["desc"]}</p></a>'

for a in ARTS:
    canon = f'{SITE}/ru/blog/{a["slug"]}/'
    _rel = [x for x in a.get('rel', []) if x in BY and x != a['slug']]
    _rel += [o['slug'] for o in ARTS if o is not a and o['sec'] == a['sec']]
    others = [BY[x] for x in dict.fromkeys(_rel)][:3]
    cta_sub = 'Писарь Pro: 399 ₽ один раз, первые 7 дней бесплатно.' if a.get('pro') else 'Диктовка бесплатно навсегда. Без рекламы и аккаунта.'
    read = max(2, round(len(re.sub('<[^>]+>', '', a["body"]).split()) / 160))
    tag = PRO_TAG if a.get('pro') else '<span class="badge">Бесплатно</span>'
    date = a.get('date', DATE)
    og = f'{SITE}/ru/blog/{a["slug"]}/og.png'
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
           "datePublished": date, "dateModified": date, "inLanguage": "ru", "mainEntityOfPage": canon,
           "image": og,
           "author": {"@type": "Organization", "name": "Pozdnekov Labs"},
           "publisher": {"@type": "Organization", "name": "Pozdnekov Labs", "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/icon.png"}}},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Писарь", "item": f"{SITE}/"},
              {"@type": "ListItem", "position": 2, "name": "Статьи", "item": f"{SITE}/ru/blog/"},
              {"@type": "ListItem", "position": 3, "name": a["title"], "item": canon}]}]
    d = os.path.join(ROOT, 'ru', 'blog', a['slug']); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w').write(page(a.get('seo', a['title']) + ' | Писарь', a['desc'], canon, body, ld, og=og))

open(os.path.join(ROOT, 'assets', 'blog.css'), 'w').write(BASE_CSS + EXTRA_CSS)
# список статей
body = f'''<main class="post">
  <section class="ahead"><div class="wrap">
    <nav class="crumbs"><a href="/">Писарь</a><span>/</span><span>Статьи</span></nav>
    <h1>Как писать голосом</h1>
    <p class="lead">Как пользоваться каждой функцией Писаря, честно о плюсах и минусах, и живые сценарии: что нажать и что получится.</p>
    <nav class="bnav"><a href="#free">Бесплатные функции</a><a href="#pro">Писарь Pro</a><a href="#scen">Сценарии</a></nav>
  </div></section>
  <div class="wrap">
    {"".join(f'<section class="bsec" id="{k}"><h2>{t}</h2><p>{d}</p><div class="grid3 list">' + "".join(card(a, 'h3') for a in ARTS if a['sec'] == k) + '</div></section>' for k, t, d in SECTIONS)}
  </div>
</main>'''
ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Статьи Писаря", "url": f"{SITE}/ru/blog/",
      "hasPart": [{"@type": "Article", "headline": a["title"], "url": f"{SITE}/ru/blog/{a['slug']}/"} for a in ARTS]}
os.makedirs(os.path.join(ROOT, 'ru', 'blog'), exist_ok=True)
open(os.path.join(ROOT, 'ru', 'blog', 'index.html'), 'w').write(page('Статьи: как писать голосом | Писарь', 'Инструкции по голосовому вводу на Android: диктовка без интернета, голосовые и скриншоты в текст, телефон для пожилых.', f'{SITE}/ru/blog/', body, ld))

# карточки для главной
open(os.path.join(os.path.dirname(__file__), 'home_cards.html'), 'w').write(''.join(card(a) for a in ([a for a in ARTS if a.get('home')] or ARTS)[:3]))
# sitemap
LAST = max([DATE] + [a.get('date', DATE) for a in ARTS])
urls = [('/', '1.0', LAST), ('/ru/blog/', '0.7', LAST)] + [(f'/ru/blog/{a["slug"]}/', '0.7', a.get('date', DATE)) for a in ARTS] + [('/ru/pro/', '0.8', DATE), ('/ru/privacy/', '0.3', DATE), ('/ru/terms/', '0.3', DATE)]
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{m}</lastmod><priority>{p}</priority></url>\n' for u, p, m in urls) + '</urlset>\n')
# проверка текстов
for dp, _, fs in os.walk(os.path.join(ROOT, 'ru', 'blog')):
    for f in [x for x in fs if x.endswith((".html", ".py", ".md", ".json", ".xml"))]:
        t = open(os.path.join(dp, f)).read()
        assert '—' not in t, (dp, 'long dash')
        assert 'GitHub' not in t and 'гитхаб' not in t.lower(), dp
        assert not re.search(r'\d+\s*секунд', t), dp
        assert 'МБ' not in t, (dp, 'megabytes')
import subprocess
subprocess.run([sys.executable, os.path.join(ROOT, 'ru', 'blog', 'build_feed.py')], check=True)
print('ok', len(ARTS))
