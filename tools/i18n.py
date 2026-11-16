# Языки сайта и строки шапки, подвала и подсказки о языке. Чтобы добавить язык, хватит правок в этом файле
# (словари HEAD и FOOT) и самих страниц /xx/...; подробно в README.md в корне сайта.
import os

SITE = 'https://pisar-app.ru'
EMAIL = 'poal0208@gmail.com'

# Порядок как в переключателе: код, название на своём языке
LANGS = [('ru', 'Русский'), ('en', 'English'), ('de', 'Deutsch'), ('fr', 'Français'), ('es', 'Español'),
         ('it', 'Italiano'), ('pt', 'Português'), ('pl', 'Polski'), ('nl', 'Nederlands'), ('bg', 'Български')]
CODES = [c for c, _ in LANGS]
NAMES = dict(LANGS)
FALLBACK = 'en'  # если страницы на языке нет, пункт ведёт сюда; если и её нет, язык неактивен
RU_ROOT = {'get', 'mac'}  # русские страницы без /ru/ в адресе (кроме главной)

# Строки шапки. Нет языка или ключа: берётся английский.
# hint: подсказка на языке браузера, показывается на странице другого языка, если версия на этом языке есть.
HEAD = {
    'ru': {'brand': 'Писарь', 'features': 'Возможности', 'pro': 'Pro', 'blog': 'Статьи', 'faq': 'Вопросы',
           'mac': 'Для Mac (скоро)', 'get': 'Скачать', 'menu': 'Меню', 'lang': 'Язык', 'theme': 'Светлая или тёмная тема',
           'hint': 'Эта страница есть на русском', 'close': 'Закрыть'},
    'en': {'brand': 'Pisar', 'features': 'Features', 'pro': 'Pro', 'blog': 'Articles', 'faq': 'FAQ',
           'mac': 'For Mac (soon)', 'get': 'Download', 'menu': 'Menu', 'lang': 'Language', 'theme': 'Light or dark theme',
           'hint': 'This page is available in English', 'close': 'Close'},
    'de': {'hint': 'Diese Seite gibt es auf Deutsch', 'close': 'Schließen'},
    'fr': {'hint': 'Cette page existe en français', 'close': 'Fermer'},
    'es': {'hint': 'Esta página está disponible en español', 'close': 'Cerrar'},
    'it': {'hint': 'Questa pagina è disponibile in italiano', 'close': 'Chiudi'},
    'pt': {'hint': 'Esta página está disponível em português', 'close': 'Fechar'},
    'pl': {'hint': 'Ta strona jest dostępna po polsku', 'close': 'Zamknij'},
    'nl': {'hint': 'Deze pagina is beschikbaar in het Nederlands', 'close': 'Sluiten'},
    'bg': {'hint': 'Тази страница е налична на български', 'close': 'Затвори'},
}

# Строки подвала. offer только у русского: оферта есть только на русском (оплата в рублях).
FOOT = {
    'ru': {'tagline': 'Диктовка в любом приложении на Android.', 'col_app': 'Писарь', 'pro_long': 'Писарь Pro',
           'col_docs': 'Документы', 'privacy': 'Политика конфиденциальности', 'terms': 'Пользовательское соглашение',
           'offer': 'Оферта', 'col_contact': 'Связь', 'col_lang': 'Язык'},
    'en': {'tagline': 'Voice typing in any Android app. Your voice stays on your phone.', 'col_app': 'Pisar',
           'pro_long': 'Pisar Pro', 'col_docs': 'Documents', 'privacy': 'Privacy Policy', 'terms': 'Terms of Use',
           'col_contact': 'Contact', 'col_lang': 'Language'},
}


def t(table, lang, key):
    """Строка на языке lang, иначе английская."""
    return table.get(lang, {}).get(key) or table['en'].get(key, '')


def url(lang, pid):
    """Адрес страницы pid ('' главная, 'pro', 'blog/slug' ...) на языке lang."""
    if lang == 'ru':
        if not pid:
            return '/'
        return f'/{pid}/' if pid.split('/')[0] in RU_ROOT else f'/ru/{pid}/'
    return f'/{lang}/' + (pid + '/' if pid else '')


def exists(root, lang, pid):
    return os.path.isfile(os.path.join(root, url(lang, pid).strip('/'), 'index.html'))


def page_of(rel):
    """Путь папки страницы от корня ('' , 'get', 'ru/pro', 'en/privacy') -> (язык, pid)."""
    parts = [p for p in rel.split('/') if p and p != '.']
    if parts and parts[0] in CODES:
        return parts[0], '/'.join(parts[1:])
    return 'ru', '/'.join(parts)


def link(root, lang, pid):
    """Ссылка на pid для страницы языка lang: своя версия, иначе английская, иначе русская."""
    for l in (lang, FALLBACK, 'ru'):
        if exists(root, l, pid):
            return url(l, pid)
    return url('ru', pid)


def versions(root, pid):
    """Для переключателя: [(код, название, адрес или None, настоящая ли версия)]."""
    out = []
    for c, name in LANGS:
        if exists(root, c, pid):
            out.append((c, name, url(c, pid), True))
        elif exists(root, FALLBACK, pid):
            out.append((c, name, url(FALLBACK, pid), False))
        else:
            out.append((c, name, None, False))
    return out


def pages(root):
    """Все страницы сайта: [(файл, язык, pid)]."""
    skip = {'.git', '.worktrees', 'tools', 'assets', '_src', 'node_modules'}
    res = []
    for dp, dns, fs in os.walk(root):
        dns[:] = sorted(d for d in dns if d not in skip and not d.startswith('.'))
        if 'index.html' in fs:
            rel = os.path.relpath(dp, root).replace(os.sep, '/')
            lang, pid = page_of('' if rel == '.' else rel)
            res.append((os.path.join(dp, 'index.html'), lang, pid))
    return res
