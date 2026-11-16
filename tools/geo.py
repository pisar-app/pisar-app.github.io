# Запуск всей сборки: python3 tools/build.py (blog, geo, footer, nav по порядку)
# Нейропоиск (ChatGPT, Perplexity, Claude, Google AI Overviews, Алиса): разметка schema.org,
# описания у правовых страниц и Pro (hreflang ставит nav.py), llms.txt и llms-full.txt. Повторный запуск ничего не меняет.
import sys, os, re, json, html, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nav, footer, pages
ROOT = sys.argv[1]
SITE = 'https://pisar-app.ru'
RUSTORE = 'https://www.rustore.ru/catalog/app/com.pisar.android'
ORG_ID, APP_ID, WEB_ID = f'{SITE}/#org', f'{SITE}/#app', f'{SITE}/#website'
EMAIL = 'poal0208@gmail.com'
LD_RE = re.compile(r'<script type="application/ld\+json">.*?</script>\n?', re.S)


def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()


def wr(p, s):
    f = os.path.join(ROOT, p)
    old = open(f, encoding='utf-8').read() if os.path.exists(f) else None
    if old != s:
        open(f, 'w', encoding='utf-8').write(s)
        print('  обновлён', p)


def chrome(s, pid):
    """Шапка и подвал своей страницы (get и mac собираются из копии Pro)."""
    return footer.apply(ROOT, nav.apply(ROOT, s, 'ru', pid), 'ru', pid)


def ld_tag(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>\n'


def text(s):
    s = re.sub(r'<(script|style|svg|header|footer|nav)\b[\s\S]*?</\1>', '', s)
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'<h([1-4])[^>]*>', lambda m: '\n\n' + '#' * (int(m.group(1)) + 1) + ' ', s)
    s = re.sub(r'</h[1-4]>', '\n', s)
    s = re.sub(r'<li[^>]*>', '\n- ', s)
    s = re.sub(r'<(tr)[^>]*>', '\n', s)
    s = re.sub(r'<(td|th)[^>]*>', ' | ', s)
    s = re.sub(r'<summary[^>]*>', '\n\n**', s); s = s.replace('</summary>', '**\n')
    s = re.sub(r'<(p|div|section|article|figure|figcaption|details)\b[^>]*>', '\n', s)
    s = re.sub(r'<span class="mi">[a-z_]+</span>', '', s)  # значки Material Icons
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r' *\n *', '\n', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()


# ---------- общие сущности ----------
ORG = {"@type": "Organization", "@id": ORG_ID, "name": "Pozdnekov Labs", "url": f"{SITE}/",
       "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/icon.png"}, "email": EMAIL,
       "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": EMAIL,
                        "availableLanguage": ["ru", "en"]}}
DESC = ('Писарь: диктовка в любом поле Android. Распознаёт речь прямо на телефоне, без интернета. '
        'Бесплатно, без рекламы и аккаунта.')
APP = {"@type": "MobileApplication", "@id": APP_ID, "name": "Писарь",
       "alternateName": ["Pisar", "Писарь: диктовка без интернета"],
       "description": DESC, "url": f"{SITE}/", "image": f"{SITE}/assets/icon.png",
       "screenshot": f"{SITE}/assets/og.png",
       "operatingSystem": "Android 10+", "softwareRequirements": "Android 10 и новее, 64-битный процессор",
       "applicationCategory": "UtilitiesApplication", "applicationSubCategory": "Голосовой ввод",
       "downloadUrl": RUSTORE, "installUrl": RUSTORE, "sameAs": [RUSTORE],
       "inLanguage": "ru", "isAccessibleForFree": True,
       "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID},
       "featureList": [
           "Диктовка голосом в любом поле Android: мессенджеры, почта, заметки, поиск",
           "Распознавание речи на телефоне, без интернета: звук и текст не уходят с телефона",
           "24 европейских языка, русский особенно точно",
           "Знаки препинания, заглавные буквы и числа цифрами автоматически",
           "Чистка речи: убирает «ну», «короче», повторы и оговорки",
           "Словарь имён и терминов, быстрые фразы",
           "Pro: голосовые, аудио и видео в текст, по файлу или ссылке",
           "Pro: текст со скриншотов и фото",
           "Pro: Буфер обмена с поиском и закреплением",
           "Pro: перевод при диктовке на 22 языка, без интернета"],
       "offers": [
           {"@type": "Offer", "name": "Диктовка", "price": "0", "priceCurrency": "RUB",
            "description": "Бесплатно навсегда, без рекламы, аккаунта и лимитов"},
           {"@type": "Offer", "name": "Писарь Pro", "price": "399", "priceCurrency": "RUB",
            "url": f"{SITE}/ru/pro/", "availability": "https://schema.org/InStock",
            "description": "Разовый платёж, без подписки. Первые 7 дней бесплатно"}]}
WEBSITE = {"@type": "WebSite", "@id": WEB_ID, "url": f"{SITE}/", "name": "Писарь",
           "alternateName": "Pisar", "inLanguage": "ru", "publisher": {"@id": ORG_ID}, "about": {"@id": APP_ID}}


def faq_from(s):
    items = re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', s, re.S)
    return {"@type": "FAQPage", "@id": f"{SITE}/#faq", "mainEntity": [
        {"@type": "Question", "name": html.unescape(re.sub('<[^>]+>', '', q)).strip(),
         "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub('<[^>]+>', '', a)).strip()}}
        for q, a in items]}


# ---------- главная: вопросы для нейропоиска + разметка из видимого текста ----------
home = rd('index.html')
NEW_FAQ = [
    ('Писарь работает без интернета?',
     'Да. Речь распознаётся прямо на телефоне, звук и текст никуда не отправляются. Интернет нужен один раз, '
     'чтобы скачать язык, а потом только для расшифровки файла по ссылке и оплаты Pro.'),
    ('Сколько стоит Писарь?',
     'Диктовка бесплатна навсегда: без рекламы, аккаунта и лимитов. Писарь Pro (голосовые и видео в текст, '
     'текст со скриншотов, Буфер, перевод при диктовке) стоит 399 ₽ один раз, без подписки. Первые 7 дней Pro бесплатно.'),
    ('Где скачать Писарь?',
     'В RuStore. Скоро в Xiaomi GetApps, Huawei AppGallery и Google Play.'),
]
anchor = '<div class="faq">\n'
for q, a in NEW_FAQ:
    if f'<summary>{q}</summary>' not in home:
        i = home.index(anchor) + len(anchor)
        home = home[:i] + f'      <details><summary>{q}</summary><p>{a}</p></details>\n' + home[i:]
graph = {"@context": "https://schema.org", "@graph": [ORG, WEBSITE, APP, faq_from(home)]}
home = LD_RE.sub('', home, count=1) if LD_RE.search(home) else home
home = home.replace('<link rel="preconnect"', ld_tag(graph) + '<link rel="preconnect"', 1)
wr('index.html', home)

# ---------- Pro и правовые страницы: описание, hreflang, разметка ----------
def head_add(s, extra):
    """Вставить блок перед первым preconnect; прежний блок geo убрать."""
    s = re.sub(r'<!-- geo -->.*?<!-- /geo -->\n', '', s, flags=re.S)
    return s.replace('<link rel="preconnect"', '<!-- geo -->\n' + extra + '<!-- /geo -->\n<link rel="preconnect"', 1)



def meta(desc, title, url, lang):
    loc = 'ru_RU' if lang == 'ru' else 'en_US'
    name = 'Писарь' if lang == 'ru' else 'Pisar'
    return (f'<meta name="description" content="{html.escape(desc)}">\n'
            f'<meta property="og:type" content="website">\n<meta property="og:locale" content="{loc}">\n'
            f'<meta property="og:site_name" content="{name}">\n<meta property="og:title" content="{html.escape(title)}">\n'
            f'<meta property="og:description" content="{html.escape(desc)}">\n<meta property="og:url" content="{url}">\n'
            f'<meta property="og:image" content="{SITE}/assets/og.png">\n')


def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


PRO_DESC = ('Писарь Pro: голосовые, аудио и видео в текст, текст со скриншотов, Буфер и перевод при диктовке. '
            '399 ₽ один раз, без подписки, первые 7 дней бесплатно.')
p = 'ru/pro/index.html'
s = rd(p)
title = re.search(r'<title>(.*?)</title>', s).group(1)
pro = {"@context": "https://schema.org", "@graph": [
    {"@type": "Product", "@id": f"{SITE}/ru/pro/#product", "name": "Писарь Pro", "description": PRO_DESC,
     "image": f"{SITE}/assets/icon.png", "brand": {"@type": "Brand", "name": "Писарь"},
     "isRelatedTo": {"@id": APP_ID},
     "offers": {"@type": "Offer", "price": "399", "priceCurrency": "RUB", "url": f"{SITE}/ru/pro/",
                "availability": "https://schema.org/InStock", "seller": {"@id": ORG_ID},
                "hasMerchantReturnPolicy": {"@type": "MerchantReturnPolicy", "applicableCountry": "RU",
                                            "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
                                            "merchantReturnDays": 14}}},
    {**ORG},
    crumbs([('Писарь', f'{SITE}/'), ('Писарь Pro', f'{SITE}/ru/pro/')])]}
wr(p, head_add(s, meta(PRO_DESC, title, f'{SITE}/ru/pro/', 'ru') + ld_tag(pro)))

# ---------- /get/: одна ссылка на установку (для «Поделиться» и подписи в приложении) ----------
STORE_BTN = re.search(r'<a class="store"[^>]*>.*?</a>', rd('index.html'), re.S).group(0)
GET_DESC = ('Скачать Писарь: офлайн-диктовка для Android. Сейчас в RuStore, скоро в Xiaomi GetApps, '
            'Huawei AppGallery и Google Play.')
GET_MAIN = ('<main><nav><a href="/">Писарь</a> · Скачать</nav>\n' + pages.get_main(f"""
<h1>Скачать Писарь</h1>
<p>Писарь: офлайн-диктовка для Android. Кнопка голосового ввода у любого поля, речь распознаётся на телефоне без интернета. Диктовка бесплатна, без рекламы и аккаунта.</p>
<p>{STORE_BTN}</p>
<p>Нужен Android 10 и новее, 64-битный процессор. <a href="/">Что умеет Писарь</a></p>""",
    [('RuStore', 'Установить', RUSTORE), ('Xiaomi GetApps', 'Скоро', None), ('Huawei AppGallery', 'Скоро', None),
     ('Google Play', 'Скоро', None)]) + '\n</main>')
g = rd('ru/pro/index.html')
g = re.sub(r'<title>.*?</title>', '<title>Скачать Писарь · Писарь</title>', g, count=1)
g = g.replace(f'href="{SITE}/ru/pro/"', f'href="{SITE}/get/"', 1)
g = g.replace(' class="on" aria-current="page"', '')
g = re.sub(r'<main>[\s\S]*?</main>', lambda m: GET_MAIN, g, count=1)
g = g.replace('<div class="legal is-pro">', '<div class="legal is-wide">', 1)  # на ПК две колонки внутри карточки
g = re.sub(r'<aside class="pro-aside">[\s\S]*?</aside>\n?', '', g, count=1)  # скриншот Pro здесь не нужен
get_ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "name": "Скачать Писарь", "url": f"{SITE}/get/", "inLanguage": "ru", "description": GET_DESC,
     "about": {"@id": APP_ID}, "publisher": {"@id": ORG_ID}},
    crumbs([('Писарь', f'{SITE}/'), ('Скачать', f'{SITE}/get/')])]}
os.makedirs(os.path.join(ROOT, 'get'), exist_ok=True)
wr('get/index.html', chrome(head_add(g, meta(GET_DESC, 'Скачать Писарь', f'{SITE}/get/', 'ru') + ld_tag(get_ld)), 'get'))

# ---------- /mac/: заглушка раздела «Писарь для Mac» ----------
MAC_DESC = 'Писарь для Mac: скоро здесь. Это отдельное приложение для Mac со своими функциями.'
MAC_F = {  # функции Мак-Писаря, сверены с кодом pisar-mac (чат 35): (заголовок, строка); порядок и иконки в tools/pages.py
    'rec': ('Запись экрана, камеры и звука', 'Экран вместе с камерой и звуком, только камера или только звук. Весь экран, область или окно; микрофон и собеседники в одном файле.'),
    'reel': ('Ролики 9:16', 'Вертикальное видео: экран сверху и вы снизу, кружок камеры или только экран. Кадр может ехать за мышкой.'),
    'tr': ('Расшифровка аудио и видео', 'Файл или своя запись становится текстом по спикерам: кто что сказал. По желанию конспект и перевод.'),
    'dict': ('Диктовка в любом приложении', 'Нажмите клавишу и говорите: текст встанет туда, где курсор, в любой программе.'),
    'clip': ('Буфер обмена', 'Лента всего, что вы копировали: найдите нужное и вставьте в любую программу, ⇧⌘V.'),
    'scr': ('Текст с экрана', 'Обведите текст на картинке, в видео или в окне, где его не выделить, и он уже в буфере обмена.'),
}
MAC_N = {  # «Сообщить о выходе»: почта в лист ожидания облака Pro (pisar-android cloud/pro, /waitlist)
    'label': 'Оставьте почту, и мы напишем, когда выйдет версия для Mac.', 'ph': 'Ваша почта', 'btn': 'Сообщить о выходе',
    'empty': 'Впишите почту.', 'bad': 'Проверьте почту: похоже, в ней ошибка.', 'ok': 'Готово, напишем, когда выйдет.',
    'many': 'Слишком много попыток. Попробуйте через час.', 'err': 'Не получилось отправить. Попробуйте позже.', 'wait': 'Отправляю…',
    'note': 'Одно письмо о выходе, без рассылок. <a href="{href}">Политика конфиденциальности</a>',
}
MAC_MAIN = ('<main><nav><a href="/">Писарь</a> · Mac</nav>\n' + pages.mac_main(f"""
<h1>Писарь для Mac</h1>
<p>Скоро здесь.</p>
<p>Это отдельное приложение для Mac, со своими функциями.</p>
{pages.notify(MAC_N, 'ru')}
<p><a href="/">Писарь для Android</a></p>""", 'Окно Писаря для Mac: раздел «Запись»',
    pages.feats('Что умеет Писарь для Mac', 'Запись, расшифровка и диктовка работают прямо на Маке.', MAC_F)) + '\n</main>')
m = re.sub(r'<main>[\s\S]*?</main>', lambda _: MAC_MAIN, g, count=1)
m = re.sub(r'<title>.*?</title>', '<title>Писарь для Mac · Писарь</title>', m, count=1)
m = m.replace(f'href="{SITE}/get/"', f'href="{SITE}/mac/"', 1)
os.makedirs(os.path.join(ROOT, 'mac'), exist_ok=True)
m = m if 'assets/notify.js' in m else m.replace('</head>', '<script src="/assets/notify.js" defer></script>\n</head>', 1)  # форма «Сообщить о выходе»
wr('mac/index.html', chrome(head_add(m, meta(MAC_DESC, 'Писарь для Mac', f'{SITE}/mac/', 'ru')), 'mac'))

LEGAL = {  # другие языки собирает tools/intl.py
    ('privacy', 'ru'): 'Политика конфиденциальности Писаря: звук и тексты распознаются на телефоне и никуда не отправляются. Что и когда уходит в сеть.',
    ('terms', 'ru'): 'Пользовательское соглашение Писаря: лицензионная оферта на использование приложения.',
}
for (kind, lang), desc in LEGAL.items():
    p = f'{lang}/{kind}/index.html'
    s = rd(p)
    title = re.search(r'<title>(.*?)</title>', s).group(1)
    url = f'{SITE}/{lang}/{kind}/'
    page_ld = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": url,
               "inLanguage": lang, "description": desc, "publisher": {"@id": ORG_ID}, "about": {"@id": APP_ID}}
    wr(p, head_add(s, meta(desc, title, url, lang) + ld_tag(page_ld)))

# ---------- llms.txt и llms-full.txt ----------
arts = []
for f in sorted(glob.glob(os.path.join(ROOT, 'ru', 'blog', '*', 'index.html'))):
    s = open(f, encoding='utf-8').read()
    slug = os.path.basename(os.path.dirname(f))
    h1 = html.unescape(re.sub('<[^>]+>', '', re.search(r'<h1>(.*?)</h1>', s, re.S).group(1))).strip()
    d = html.unescape(re.search(r'<meta name="description" content="(.*?)">', s).group(1))
    body = re.search(r'<main[\s\S]*?</main>', s).group(0)
    body = re.sub(r'<section class="related">[\s\S]*?</section>', '', body)
    body = re.sub(r'<div class="cta">[\s\S]*?</div>\s*</div>', '', body)
    body = re.sub(r'<p class="support">[\s\S]*?</p>', '', body)
    arts.append((slug, h1, d, text(body)))
# порядок как в разделах блога (бесплатные, Pro, сценарии)
order = re.findall(r'href="/ru/blog/([a-z0-9-]+)/"', rd('ru/blog/index.html'))
rank = {s: i for i, s in reversed(list(enumerate(order)))}
arts.sort(key=lambda a: rank.get(a[0], 999))

FACTS_RU = '''- Что это: приложение для Android. Добавляет кнопку диктовки P у любого поля ввода; сказанное печатается туда, где курсор. Это не клавиатура: ваша клавиатура остаётся прежней.
- Без интернета: речь распознаётся на самом телефоне, звук и текст никуда не отправляются. Интернет нужен один раз, чтобы скачать язык, и ещё для расшифровки файла по ссылке и оплаты Pro.
- Языки распознавания: 24 европейских, русский особенно точно; можно выбрать «Только русский» (быстрее и точнее).
- Текст сразу чистый: знаки препинания, заглавные, числа цифрами, «?» у вопроса; по желанию убирает слова-паразиты, повторы, оговорки и мат.
- Бесплатно навсегда: диктовка без лимитов, без рекламы и без аккаунта. Записи хранятся 1 день.
- Писарь Pro, 399 ₽ один раз (без подписки, первые 7 дней бесплатно): голосовые, аудио и видео в текст (файл или ссылка), текст со скриншотов и фото, Буфер скопированного с поиском, перевод при диктовке на 22 языка, хранение записей неделю, месяц или всегда. Оплата картой или СБП, возврат в течение 14 дней.
- Требования: Android 10 и новее, 64-битный процессор. Нужно разрешение «Специальные возможности»: через него Писарь видит поле, показывает кнопку и вставляет текст; поля паролей не читает.
- Ограничения: иногда ошибается в шуме, при быстрой речи и в редких словах (помогает словарь); языки занимают место на телефоне; на старых телефонах медленнее.
- Где скачать: RuStore ({rustore}). Скоро в Xiaomi GetApps, Huawei AppGallery и Google Play.
- Разработчик: Pozdnekov Labs. Поддержка: {email}.'''.format(rustore=RUSTORE, email=EMAIL)

FACTS_EN = '''Pisar is an offline voice typing app for Android by Pozdnekov Labs. It adds a dictation button next to any text field (messengers, email, notes, search) and types what you say where the cursor is. It is not a keyboard: your keyboard stays the same.
- Speech recognition runs entirely on the phone. Audio and text never leave the device; internet is needed only once to download a language, plus for transcribing a file by link and paying for Pro.
- 24 European recognition languages, Russian is the most accurate.
- Punctuation, capital letters and numbers as digits are added automatically; filler words and repetitions can be removed.
- Dictation is free forever: no ads, no account, no limits.
- Pisar Pro is a one-time purchase, no subscription, 7-day free trial: voice messages, audio and video to text, text from screenshots and photos, clipboard history with search, translation while dictating into 22 languages.
- Requires Android 10+ and a 64-bit CPU. Uses the Android Accessibility Service to see the text field and insert text; never reads password fields.
- Available on RuStore: {rustore}. Coming to Xiaomi GetApps, Huawei AppGallery and Google Play.
- Support: {email}. Privacy policy: {site}/en/privacy/'''.format(rustore=RUSTORE, email=EMAIL, site=SITE)

# справка на остальных 8 языках карточек (термины как в карточках магазинов)
INTL = [
('Deutsch', 'de', '''Pisar ist eine Offline-App für Spracheingabe auf Android von Pozdnekov Labs. Neben jedem Textfeld (Messenger, E-Mail, Notizen, Suche) erscheint eine Diktiertaste, und das Gesagte steht dort, wo der Cursor ist. Pisar ist keine Tastatur: Ihre Tastatur bleibt.
- Die Spracherkennung läuft komplett auf dem Handy. Ton und Text verlassen das Gerät nicht; Internet braucht man nur einmal zum Herunterladen einer Sprache.
- 24 europäische Sprachen, darunter Deutsch und Englisch.
- Satzzeichen, Großschreibung und Zahlen als Ziffern kommen automatisch; Füllwörter und Wiederholungen können entfernt werden.
- Diktieren ist dauerhaft kostenlos: ohne Werbung, ohne Konto, ohne Limits. Pisar Pro ist ein Einmalkauf ohne Abo, 7 Tage gratis testen: Sprachnachrichten, Audio und Video als Text, Text aus Screenshots, Zwischenablage-Verlauf, Übersetzung beim Diktieren.
- Android 10 oder neuer, 64-Bit-Prozessor. Nutzt den Bedienungshilfen-Dienst von Android, um das Feld zu erkennen und Text einzufügen; Passwortfelder werden nie gelesen.'''),
('Français', 'fr', '''Pisar est une application de saisie vocale hors ligne pour Android, par Pozdnekov Labs. Un bouton de dictée apparaît à côté de chaque champ de texte (messagerie, e-mail, notes, recherche) et ce que vous dites s'écrit là où se trouve le curseur. Ce n'est pas un clavier : votre clavier reste le même.
- La reconnaissance vocale fonctionne entièrement sur le téléphone. Le son et le texte ne quittent pas l'appareil ; Internet sert une seule fois, pour télécharger une langue.
- 24 langues européennes, dont le français et l'anglais.
- Ponctuation, majuscules et nombres en chiffres sont ajoutés automatiquement ; les mots de remplissage et répétitions peuvent être supprimés.
- La dictée est gratuite pour toujours : sans publicité, sans compte, sans limite. Pisar Pro est un achat unique sans abonnement, 7 jours d'essai gratuit : messages vocaux, audio et vidéo en texte, texte depuis une capture d'écran, historique du presse-papiers, traduction pendant la dictée.
- Android 10 ou plus récent, processeur 64 bits. Utilise le service d'accessibilité d'Android pour voir le champ et insérer le texte ; ne lit jamais les champs de mot de passe.'''),
('Español', 'es', '''Pisar es una app de escritura por voz sin conexión para Android, de Pozdnekov Labs. Junto a cualquier campo de texto (mensajería, correo, notas, búsqueda) aparece un botón de dictado, y lo que dices se escribe donde está el cursor. No es un teclado: tu teclado sigue igual.
- El reconocimiento de voz funciona por completo en el teléfono. El audio y el texto no salen del dispositivo; internet solo hace falta una vez, para descargar un idioma.
- 24 idiomas europeos, entre ellos español e inglés.
- Signos de puntuación, mayúsculas y números en cifras se ponen solos; se pueden quitar muletillas y repeticiones.
- El dictado es gratis para siempre: sin anuncios, sin cuenta, sin límites. Pisar Pro es un pago único sin suscripción, con 7 días de prueba gratis: notas de voz, audio y vídeo a texto, texto de capturas de pantalla, historial del portapapeles, traducción al dictar.
- Android 10 o posterior, procesador de 64 bits. Usa el servicio de accesibilidad de Android para ver el campo e insertar el texto; nunca lee campos de contraseña.'''),
('Italiano', 'it', '''Pisar è un'app di dettatura vocale offline per Android, di Pozdnekov Labs. Accanto a ogni campo di testo (messaggi, email, note, ricerca) compare un pulsante di dettatura e ciò che dici viene scritto dove si trova il cursore. Non è una tastiera: la tua tastiera resta la stessa.
- Il riconoscimento vocale funziona interamente sul telefono. Audio e testo non lasciano il dispositivo; internet serve solo una volta, per scaricare una lingua.
- 24 lingue europee, tra cui italiano e inglese.
- Punteggiatura, maiuscole e numeri in cifre vengono inseriti da soli; intercalari e ripetizioni si possono eliminare.
- La dettatura è gratuita per sempre: senza pubblicità, senza account, senza limiti. Pisar Pro è un acquisto unico senza abbonamento, con 7 giorni di prova gratuita: vocali, audio e video in testo, testo dagli screenshot, cronologia degli appunti, traduzione durante la dettatura.
- Android 10 o successivo, processore a 64 bit. Usa il servizio di accessibilità di Android per vedere il campo e inserire il testo; non legge mai i campi password.'''),
('Português', 'pt', '''Pisar é um app de digitação por voz offline para Android, da Pozdnekov Labs. Ao lado de qualquer campo de texto (mensageiro, e-mail, notas, busca) aparece um botão de ditado, e o que você fala é escrito onde está o cursor. Não é um teclado: seu teclado continua o mesmo.
- O reconhecimento de voz funciona inteiramente no celular. O áudio e o texto não saem do aparelho; a internet só é necessária uma vez, para baixar um idioma.
- 24 idiomas europeus, incluindo português e inglês.
- Pontuação, maiúsculas e números em algarismos entram sozinhos; vícios de linguagem e repetições podem ser removidos.
- O ditado é grátis para sempre: sem anúncios, sem conta, sem limites. O Pisar Pro é uma compra única, sem assinatura, com 7 dias grátis: áudios, gravações e vídeos em texto, texto de capturas de tela, histórico da área de transferência, tradução ao ditar.
- Android 10 ou mais recente, processador de 64 bits. Usa o serviço de acessibilidade do Android para ver o campo e inserir o texto; nunca lê campos de senha.'''),
('Polski', 'pl', '''Pisar to aplikacja do pisania głosem offline na Androida od Pozdnekov Labs. Obok każdego pola tekstowego (komunikator, poczta, notatki, wyszukiwarka) pojawia się przycisk dyktowania, a to, co powiesz, trafia tam, gdzie jest kursor. To nie klawiatura: Twoja klawiatura zostaje bez zmian.
- Rozpoznawanie mowy działa w całości na telefonie. Dźwięk i tekst nie opuszczają urządzenia; internet jest potrzebny tylko raz, by pobrać język.
- 24 języki europejskie, w tym polski i angielski.
- Interpunkcja, wielkie litery i liczby cyframi wstawiają się same; można usuwać wtrącenia i powtórzenia.
- Dyktowanie jest darmowe na zawsze: bez reklam, bez konta, bez limitów. Pisar Pro to jednorazowy zakup bez subskrypcji, 7 dni za darmo: głosówki, audio i wideo na tekst, tekst ze zrzutów ekranu, historia schowka, tłumaczenie podczas dyktowania.
- Android 10 lub nowszy, procesor 64-bitowy. Korzysta z usługi ułatwień dostępu Androida, by widzieć pole i wstawiać tekst; nigdy nie czyta pól haseł.'''),
('Nederlands', 'nl', '''Pisar is een offline app voor spraakinvoer op Android, van Pozdnekov Labs. Naast elk tekstveld (messenger, mail, notities, zoekbalk) verschijnt een dicteerknop, en wat je zegt komt waar de cursor staat. Het is geen toetsenbord: je eigen toetsenbord blijft.
- Spraakherkenning draait volledig op de telefoon. Geluid en tekst verlaten het toestel niet; internet is maar één keer nodig, om een taal te downloaden.
- 24 Europese talen, waaronder Nederlands en Engels.
- Leestekens, hoofdletters en getallen in cijfers komen er vanzelf in; stopwoorden en herhalingen kunnen worden weggelaten.
- Dicteren is voor altijd gratis: zonder advertenties, zonder account, zonder limieten. Pisar Pro is een eenmalige aankoop zonder abonnement, 7 dagen gratis: spraakberichten, audio en video naar tekst, tekst uit screenshots, klembordgeschiedenis, vertalen tijdens het dicteren.
- Android 10 of nieuwer, 64-bit processor. Gebruikt de toegankelijkheidsservice van Android om het veld te zien en tekst in te voegen; leest nooit wachtwoordvelden.'''),
('Български', 'bg', '''Pisar е приложение за гласово въвеждане офлайн за Android от Pozdnekov Labs. До всяко текстово поле (месинджър, поща, бележки, търсене) се появява бутон за диктовка и казаното се изписва там, където е курсорът. Не е клавиатура: вашата клавиатура остава същата.
- Разпознаването на реч работи изцяло на телефона. Звукът и текстът не напускат устройството; интернет трябва само веднъж, за да изтеглите език.
- 24 европейски езика, сред тях български и английски.
- Препинателните знаци, главните букви и числата с цифри се поставят сами; думите паразити и повторенията могат да се махат.
- Диктовката е безплатна завинаги: без реклами, без акаунт, без ограничения. Pisar Pro е еднократна покупка без абонамент, 7 дни безплатно: гласови съобщения, аудио и видео в текст, текст от екранни снимки, история на клипборда, превод при диктовка.
- Android 10 или по-нов, 64-битов процесор. Използва услугата за достъпност на Android, за да вижда полето и да вмъква текст; никога не чете полета за пароли.'''),
]
TAIL = f'\n- RuStore: {RUSTORE} · Xiaomi GetApps, Huawei AppGallery, Google Play: soon · {EMAIL}'
INTL_MD = ''.join(f'\n\n## {name} ({code})\n\n{body}{TAIL}' for name, code, body in INTL)

llms = f'''# Писарь (Pisar)

> {DESC} Диктовка бесплатна навсегда; Писарь Pro покупается один раз за 399 ₽. Разработчик: Pozdnekov Labs.

## Коротко о Писаре

{FACTS_RU}

## In English

{FACTS_EN}{INTL_MD}

## Главные страницы

- [Писарь: диктовка без интернета]({SITE}/): что умеет, цены, частые вопросы
- [Писарь Pro]({SITE}/ru/pro/): что входит в Pro, как купить, восстановить покупку и вернуть деньги
- [Статьи: как писать голосом]({SITE}/ru/blog/): инструкции к каждой функции и сценарии
- [Скачать Писарь]({SITE}/get/): RuStore, скоро Xiaomi GetApps, Huawei AppGallery, Google Play

## Статьи

''' + '\n'.join(f'- [{h1}]({SITE}/ru/blog/{slug}/): {d}' for slug, h1, d, _ in arts) + f'''

## Other languages

''' + '\n'.join(f'- {n}: [{SITE}/{c}/]({SITE}/{c}/) · [Pisar Pro]({SITE}/{c}/pro/) · [Privacy]({SITE}/{c}/privacy/)'
                for n, c in [('English', 'en')] + [(n, c) for n, c, _ in INTL]) + f'''

## Документы

- [Политика конфиденциальности]({SITE}/ru/privacy/) ([English]({SITE}/en/privacy/))
- [Пользовательское соглашение]({SITE}/ru/terms/) ([English]({SITE}/en/terms/))
- [Оферта Писарь Pro]({SITE}/ru/pro/offer/)

## Optional

- [Полный текст сайта одним файлом]({SITE}/llms-full.txt)
'''
assert '—' not in llms, 'длинное тире в llms.txt'
wr('llms.txt', llms)

home_txt = text(re.search(r'<body[\s\S]*</body>', rd('index.html')).group(0))
pro_txt = text(re.search(r'<main[\s\S]*?</main>', rd('ru/pro/index.html')).group(0)) if '<main' in rd('ru/pro/index.html') \
    else text(re.search(r'<body[\s\S]*</body>', rd('ru/pro/index.html')).group(0))
pro_txt = re.split(r'\n#+ Продавец', pro_txt)[0]  # реквизиты продавца остаются только на странице
full = (f'# Писарь (Pisar): полный текст сайта {SITE}\n\n> {DESC}\n\n## Коротко о Писаре\n\n{FACTS_RU}\n\n## In English\n\n{FACTS_EN}{INTL_MD}\n\n'
        f'---\n\n# Главная: {SITE}/\n\n{home_txt}\n\n---\n\n# Писарь Pro: {SITE}/ru/pro/\n\n{pro_txt}\n\n'
        + ''.join(f'---\n\n# {h1}\n\nАдрес: {SITE}/ru/blog/{slug}/\n\n{body}\n\n' for slug, h1, _, body in arts))
full = full.replace('—', ':')  # правило сайта: без длинного тире
wr('llms-full.txt', full)
print('geo: ok,', len(arts), 'статей в llms.txt;', round(len(full.encode()) / 1024), 'КБ в llms-full.txt')
