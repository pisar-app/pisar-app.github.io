# Страницы на других языках: /xx/ (главная), /xx/pro/, /xx/get/, /xx/mac/, /xx/privacy/, /xx/terms/.
# Тексты одного языка лежат в tools/lang/<код>.py, правовые тексты в tools/lang/<код>.privacy.html и .terms.html.
# Главная собирается из русской index.html: каждый русский кусок из HOME_SRC заменяется переводом по ключу.
# Поменяли текст русской главной: сборка упадёт на ключе, которого больше нет, и его надо перевести заново.
# Остальные страницы собираются из оболочки русской Pro или политики (шапка, стили) и своего <main>.
# Запуск: python3 tools/intl.py .   (всё сразу: python3 tools/build.py; после geo, до footer и nav)
import sys, os, re, json, html, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from i18n import SITE, EMAIL, FOOT, t
import nav, footer, toc
import pages as layout

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
LANGS = ['en', 'de', 'fr', 'es', 'it', 'pt', 'pl', 'nl', 'bg']
LOCALE = {'en': 'en_US', 'de': 'de_DE', 'fr': 'fr_FR', 'es': 'es_ES', 'it': 'it_IT', 'pt': 'pt_BR', 'pl': 'pl_PL',
          'nl': 'nl_NL', 'bg': 'bg_BG'}
ORG_ID = f'{SITE}/#org'
ORG = {"@type": "Organization", "@id": ORG_ID, "name": "Pozdnekov Labs", "url": f"{SITE}/",
       "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/icon.png"}, "email": EMAIL}
LD_RE = re.compile(r'<script type="application/ld\+json">.*?</script>\n?', re.S)


def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()


def wr(p, s):
    f = os.path.join(ROOT, p)
    os.makedirs(os.path.dirname(f), exist_ok=True)
    old = open(f, encoding='utf-8').read() if os.path.exists(f) else None
    if old != s:
        open(f, 'w', encoding='utf-8').write(s)
        print('  обновлён', p)


def load(lang):
    spec = importlib.util.spec_from_file_location('lang_' + lang, os.path.join(HERE, 'lang', lang + '.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def ld_tag(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>\n'


def esc(s): return html.escape(s, quote=True)


def plain(s): return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def sub1(s, old, new, n=1):
    """Заменить кусок, который обязан встретиться ровно n раз."""
    c = s.count(old)
    assert c == n, f'кусок встречается {c} раз вместо {n}: {old[:80]!r}'
    return s.replace(old, new)


def head(s, lang, pid, title, desc):
    """<title>, описание, canonical, og:* для страницы pid на языке lang; прежний блок geo убирается."""
    u = f'{SITE}/{lang}/' + (pid + '/' if pid else '')
    s = re.sub(r'<!-- geo -->.*?<!-- /geo -->\n', '', s, flags=re.S)
    s = re.sub(r'<meta (name="description"|property="og:[a-z_]+"|name="twitter:[a-z]+") content="[^"]*">\n', '', s)
    s = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{u}">', s, count=1)
    meta = (f'<meta name="description" content="{esc(desc)}">\n<meta property="og:type" content="website">\n'
            f'<meta property="og:locale" content="{LOCALE[lang]}">\n<meta property="og:site_name" content="Pisar">\n'
            f'<meta property="og:title" content="{esc(title)}">\n<meta property="og:description" content="{esc(desc)}">\n'
            f'<meta property="og:url" content="{u}">\n<meta property="og:image" content="{SITE}/assets/og.png">\n'
            '<meta name="twitter:card" content="summary_large_image">\n')
    return s.replace('<link rel="canonical"', '<!-- geo -->\n' + meta + '<!-- /geo -->\n<link rel="canonical"', 1)


def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def check(s, lang, where):
    """Без длинного тире, без рублей и русского текста в видимой части."""
    body = re.sub(r'<(script|style)\b[\s\S]*?</\1>', '', s)
    body = re.sub(r'<!--[\s\S]*?-->', '', body)
    body = re.sub(r'<(header|footer)\b[\s\S]*?</\1>', '', body)
    assert '—' not in body, f'{where}: длинное тире'
    for bad in ('₽', 'руб', 'СБП', 'Robokassa', 'Робокасса'):
        if where.endswith(('privacy', 'terms')) and bad == 'Robokassa':
            continue  # политика честно называет платёжный сервис
        assert bad not in body, f'{where}: {bad}'
    rus = re.findall(r'[ыэёЫЭЁ]', body) if lang == 'bg' else re.findall(r'[а-яА-ЯёЁ]+', body)
    assert not rus, f'{where}: русский текст {rus[:5]}'


# ---------- главная ----------
# Русские куски главной и ключи перевода в tools/lang/<код>.py (словарь HOME).
HOME_SRC = [
    ('h1', 'Говорите.<br>Писарь печатает.'),
    ('lead', 'Наговорите сообщение, письмо или заметку, и текст сам встанет в любое поле.<br><span>Голос не уходит с телефона.</span>'),
    ('chat_in1', 'Ты во сколько приедешь?'),
    ('chat_in2', 'Хорошо, сынок! Чайник уже ставлю, жду тебя'),
    ('f_h2', 'Говорить быстрее, чем печатать'),
    ('f1_h', '<h3>Работает без интернета</h3>'), ('f1_p', 'В метро, в самолёте, на даче. Речь распознаётся прямо на телефоне.'),
    ('f2_h', 'В любом приложении'), ('f2_p', 'Мессенджер, почта, заметки, поиск: текст встаёт туда, где курсор. Клавиатуру менять не нужно.'),
    ('f3_h', 'Бесплатно и без рекламы'), ('f3_p', 'Диктовка без подписки и без лимитов. Pro покупается один раз за 399 ₽.'),
    ('c_h2', 'Текст сразу чистый'), ('c_sub', 'Исправлять ничего не нужно: знаки, заглавные и числа Писарь ставит сам.'),
    ('c_said', '<span>Сказали</span>'), ('c_ins', '<span>Вставилось</span>'),
    ('s_h2', 'Три шага, и можно говорить'),
    ('s1_h', '1. Установите'), ('s1_p', 'Без регистрации и аккаунта.'),
    ('s2_h', '2. Выберите язык'), ('s2_p', 'Русский или сразу 24 языка. Один раз, дальше Писарь работает и без интернета.'),
    ('s3_h', '3. Говорите'), ('s3_p', 'Коснитесь кнопки P у любого поля, и текст появится сам.'),
    ('a_h2', 'Всё, что умеет Писарь'), ('a_sub', 'Всё это входит в бесплатную диктовку. Без рекламы, без аккаунта, без лимитов на диктовку.'),
    ('p_h2', 'Писарь Pro: больше, чем диктовка'), ('p_sub', 'Голосовые, видео и скриншоты в текст. 399 ₽ один раз, первые 7 дней бесплатно.'),
    ('m_voice', '<b>Голосовое</b><small>сегодня, 0:42</small>'),
    ('m_voice_t', 'Привет! Короче, в субботу собираемся у бабушки к часу, не забудь торт забрать, я заказала на твоё имя.'),
    ('m_video', '<b>Видео</b><small>вчера, 3:15</small>'),
    ('m_link', '<b>Ссылка на подкаст</b><small>расшифровывается в фоне</small>'),
    ('m_ocr', 'Номер заказа 48 213. Получение: пункт выдачи на Садовой, 12, до 20:00.'),
    ('m_pinned', '<div class="mhead">Закреплено</div>'),
    ('m_addr', '<span class="mi">push_pin</span>ул. Садовая, 12, кв. 5'),
    ('m_today', '<div class="mhead">Сегодня</div>'),
    ('m_clip1', 'Ссылка на запись к врачу'), ('m_clip2', 'Список покупок: молоко, хлеб, яблоки'),
    ('m_pair', '>RU→EN<'),
    ('m_said', '«Спасибо, всё получил, завтра отвечу»'),
    ('m_out', "Thanks, got everything, I'll reply tomorrow."),
]
# Блоки, которые на других языках устроены иначе (без цены, без кнопки RuStore, без русского блога)
HERO_CTA = re.compile(r'<div class="ctas">\n\s*<a class="store"[\s\S]*?</div>\s*<p class="note">[\s\S]*?</p>')
SAID_ROW = re.compile(r'<div class="row"><span class="s">.*?</span><span class="arr">→</span><span class="t">.*?<span class="tag">.*?</span></span></div>')
FCARD = re.compile(r'(<div class="fcard"><div class="ico"><span class="mi">\w+</span></div>)<h3>.*?</h3><p>.*?</p></div>')
SHOW_T = re.compile(r'(<div class="show-t"><h3><span class="badge pro"><span class="mi">lock</span>Pro</span> ).*?</h3><p>.*?</p></div>')
PRICE = re.compile(r'<section id="pro">[\s\S]*?</section>')
FAQ = re.compile(r'<section id="faq">[\s\S]*?</section>')
BLOG = re.compile(r'<section id="blog"[\s\S]*?</section>\n\n')
FINAL = re.compile(r'<div class="final">[\s\S]*?\n  </div>\n</div>')


def one(rx, s, new):
    assert len(rx.findall(s)) == 1, f'блок {rx.pattern[:40]!r} не найден или не один'
    return rx.sub(lambda m: new, s, count=1)


def home(lang, L):
    H = L.HOME
    s = rd('index.html')
    for key, ru in HOME_SRC:
        s = sub1(s, ru, H[key])
    # переписка в телефоне: имя, ответ (он же набранный текст) и «✓ N слов»
    s = sub1(s, '<span class="ava">М</span>Мама', f'<span class="ava">{H["chat_name"][0]}</span>{H["chat_name"]}')
    s = sub1(s, 'Мамуль, уже еду, буду через 20 минут. Поставь чайник, я с пирогом', H['chat_out'], 2)
    s = sub1(s, '<span class="ph">Сообщение</span>', f'<span class="ph">{H["chat_ph"]}</span>')
    words = H['words'].format(n=len(plain(H['chat_out']).split()))
    w = min(136, 38 + round(len(words) * 7.8) + 12)  # ширина плашки «✓ N слов» под длину подписи
    s = sub1(s, '<svg class="pw-done" width="104" height="32" viewBox="0 0 104 32"><rect x=".5" y=".5" width="103"',
             f'<svg class="pw-done" width="{w}" height="32" viewBox="0 0 {w} 32"><rect x=".5" y=".5" width="{w - 1}"')
    s = sub1(s, '>12 слов<', f'>{words}<')
    s = sub1(s, 'done:{w:104,h:32', f'done:{{w:{w},h:32')
    s = sub1(s, "Math.max(0,sl-44)", f"Math.max(0,sl-{148 - w})")
    # «Сказали → Вставилось»
    rows = iter(H['rows'])
    assert len(SAID_ROW.findall(s)) == len(H['rows']) == 4
    s = SAID_ROW.sub(lambda m: '<div class="row"><span class="s">{}</span><span class="arr">→</span><span class="t">{}<span class="tag">{}</span></span></div>'.format(*next(rows)), s)
    cards = iter(H['fcards'])
    assert len(FCARD.findall(s)) == len(H['fcards']) == 12
    s = FCARD.sub(lambda m: m.group(1) + '<h3>{}</h3><p>{}</p></div>'.format(*next(cards)), s)
    shows = iter(H['shows'])
    assert len(SHOW_T.findall(s)) == len(H['shows']) == 4
    s = SHOW_T.sub(lambda m: m.group(1) + '{}</h3><p>{}</p></div>'.format(*next(shows)), s)
    get = f'/{lang}/get/'
    s = one(HERO_CTA, s, f'<div class="ctas">\n      <a class="btn btn1" href="{get}">{H["cta"]}</a>\n    </div>\n'
                         f'    <p class="note">{H["hero_note"]}</p>')
    P = H['price']
    li = lambda xs: ''.join(f'\n          <li>{x}</li>' for x in xs)
    s = one(PRICE, s, f'''<section id="pro">
  <div class="wrap">
    <div class="center"><h2>{P["h2"]}</h2><p class="sub">{P["sub"]}</p></div>
    <div class="pro">
      <div class="card">
        <span class="badge">{P["free"]}</span>
        <ul class="list">{li(P["free_items"])}
        </ul>
        <span class="badge pro" style="margin-top:22px"><span class="mi">lock</span>{P["pro"]}</span>
        <ul class="list">{li(P["pro_items"])}
        </ul>
      </div>
      <div class="price">
        <div class="pr-row"><span class="prologo lg"><img src="/assets/icon.png" alt=""><b>PRO</b></span><div><b class="pr-name">Pisar Pro</b><span class="pr-sub">{P["pr_sub"]}</span></div></div>
        <div class="big" style="font-size:clamp(34px,5vw,44px)">{P["big"]}</div>
        <p style="margin:12px 0 0;color:var(--muted)">{P["text"]}</p>
        <a class="btn btnpro" style="margin-top:22px" href="/{lang}/pro/">{P["btn"]}</a>
      </div>
    </div>
  </div>
</section>''')
    faq = ''.join(f'      <details><summary>{q}</summary><p>{a}</p></details>\n' for q, a in L.FAQ)
    s = one(FAQ, s, f'<section id="faq">\n  <div class="wrap">\n    <div class="center"><h2>{H["faq_h2"]}</h2></div>\n'
                    f'    <div class="faq">\n{faq}    </div>\n  </div>\n</section>')
    s = one(BLOG, s, '')  # статьи пока только на русском
    s = one(FINAL, s, f'''<div class="final">
  <div class="wrap" style="position:relative">
    <h2>{H["final_h2"]}</h2>
    <p class="sub" style="margin-left:auto;margin-right:auto">{H["final_sub"]}</p>
    <div class="ctas"><a class="btn btn1" href="{get}">{H["cta"]}</a></div><p class="note">{H["soon"]}</p>
  </div>
</div>''')
    M = L.META
    s = head(s, lang, '', M['home_title'], M['home_desc'])
    app = {"@type": "MobileApplication", "@id": f"{SITE}/{lang}/#app", "name": "Pisar",
           "description": M['home_desc'], "url": f"{SITE}/{lang}/", "image": f"{SITE}/assets/icon.png",
           "operatingSystem": "Android 10+", "applicationCategory": "UtilitiesApplication", "inLanguage": lang,
           "isAccessibleForFree": True, "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID},
           "featureList": [plain(h) for h, _ in H['fcards']] + [plain(h) for h, _ in H['shows']]}
    faq_ld = {"@type": "FAQPage", "@id": f"{SITE}/{lang}/#faq", "mainEntity": [
        {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in L.FAQ]}
    s = LD_RE.sub('', s, count=1)
    s = s.replace('<link rel="preconnect"', ld_tag({"@context": "https://schema.org", "@graph": [ORG, app, faq_ld]}) + '<link rel="preconnect"', 1)
    return s


# ---------- Pro, Скачать, Mac ----------
MAIN = re.compile(r'<main>[\s\S]*?</main>')
ASIDE = re.compile(r'<aside class="pro-aside">[\s\S]*?</aside>\n?')


def pro(lang, L):
    P, M = L.PRO, L.META
    s = rd('ru/pro/index.html')
    s = LD_RE.sub('', s)
    s = head(s, lang, 'pro', M['pro_title'], M['pro_desc'])
    s = one(MAIN, s, f'<main><nav><a href="/{lang}/">Pisar</a> · Pisar Pro</nav>\n{P["main"].strip()}\n'
                     f'<p><a href="/{lang}/terms/">{t(FOOT, lang, "terms")}</a> · <a href="/{lang}/privacy/">{t(FOOT, lang, "privacy")}</a></p>\n</main>')
    s = one(ASIDE, s, f'<aside class="pro-aside"><figure class="appshot"><img src="/assets/shots/pro-{lang}.webp" alt="{esc(P["shot_alt"])}">'
                      f'<figcaption>{P["shot_cap"]}</figcaption></figure></aside>\n')
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": M['pro_title'], "url": f"{SITE}/{lang}/pro/", "inLanguage": lang,
         "description": M['pro_desc'], "about": {"@id": f"{SITE}/{lang}/#app"}, "publisher": {"@id": ORG_ID}},
        crumbs([('Pisar', f'{SITE}/{lang}/'), ('Pisar Pro', f'{SITE}/{lang}/pro/')])]}
    return s.replace('<!-- /geo -->', ld_tag(ld) + '<!-- /geo -->', 1)


def simple(lang, L, pid, main, title, desc, crumb):
    s = rd(f'{lang}/pro/index.html')
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\n', '', s)
    s = head(s, lang, pid, title, desc)
    s = s.replace('<div class="legal is-pro">', '<div class="legal is-wide">', 1)  # на ПК две колонки внутри карточки
    s = one(ASIDE, s, '')
    s = one(MAIN, s, f'<main><nav><a href="/{lang}/">Pisar</a> · {crumb}</nav>\n{main.strip()}\n</main>')
    s = s.replace(' class="on" aria-current="page"', '')
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": title, "url": f"{SITE}/{lang}/{pid}/", "inLanguage": lang, "description": desc,
         "about": {"@id": f"{SITE}/{lang}/#app"}, "publisher": {"@id": ORG_ID}},
        crumbs([('Pisar', f'{SITE}/{lang}/'), (crumb, f'{SITE}/{lang}/{pid}/')])]}
    return s.replace('<!-- /geo -->', ld_tag(ld) + '<!-- /geo -->', 1)


RUSTORE = 'https://www.rustore.ru/catalog/app/com.pisar.android'


def get(lang, L):
    G = L.GET
    intro = f'<h1>{G["h1"]}</h1>\n<p>{G["p"]}</p>\n<p>{G["req"]} <a href="/{lang}/">{G["what"]}</a></p>'
    items = [(n, G['soon'], None) for n in ('Google Play', 'Xiaomi GetApps', 'Huawei AppGallery')] + [('RuStore', G['rustore'], RUSTORE)]
    return simple(lang, L, 'get', layout.get_main(intro, items), L.META['get_title'], L.META['get_desc'], G['crumb'])


def mac(lang, L):
    G = L.MAC
    text = f'<h1>{G["h1"]}</h1>\n<p>{G["soon"]}</p>\n<p>{G["p"]}</p>\n<p><a href="/{lang}/">{G["android"]}</a></p>'
    return simple(lang, L, 'mac', layout.mac_main(text, G['alt'], G['cap']), L.META['mac_title'], L.META['mac_desc'], 'Mac')


# ---------- политика и соглашение: перевод для удобства, действует русская версия ----------
def legal(lang, L, kind):
    s = toc.strip(rd(f'ru/{kind}/index.html'))  # оглавление ставит toc.py уже по своему языку
    s = LD_RE.sub('', s)
    M = L.META
    s = head(s, lang, kind, M[kind + '_title'], M[kind + '_desc'])
    body = open(os.path.join(HERE, 'lang', f'{lang}.{kind}.html'), encoding='utf-8').read().strip()
    note = '<p class="tnote">' + L.LEGAL_NOTE.format(href=f'/ru/{kind}/') + '</p>'  # ссылка на русскую версию
    s = one(MAIN, s, f'<main>{note}\n{body}</main>')
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": M[kind + '_title'], "url": f"{SITE}/{lang}/{kind}/",
          "inLanguage": lang, "description": M[kind + '_desc'], "publisher": {"@id": ORG_ID}, "about": {"@id": f"{SITE}/{lang}/#app"}}
    return toc.apply(s.replace('<!-- /geo -->', ld_tag(ld) + '<!-- /geo -->', 1), lang)


if __name__ == '__main__':
    have = [l for l in LANGS if os.path.exists(os.path.join(HERE, 'lang', l + '.py'))]
    if have != LANGS:
        print('intl: нет текстов для', ', '.join(l for l in LANGS if l not in have))
    for lang in have:
        L = load(lang)
        pages = [('', home), ('pro', pro), ('get', get), ('mac', mac),
                 ('privacy', lambda l, m: legal(l, m, 'privacy')), ('terms', lambda l, m: legal(l, m, 'terms'))]
        for pid, fn in pages:
            out = fn(lang, L)
            out = footer.apply(ROOT, nav.apply(ROOT, out, lang, pid), lang, pid)  # как в geo.py: повторная сборка ничего не меняет
            check(out, lang, f'{lang}/{pid}')
            wr(f'{lang}/{pid}/index.html'.replace('//', '/'), out)
    print('intl: ok,', len(have), 'языков')
