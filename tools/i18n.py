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
    'en': {'brand': 'Pisar', 'features': 'Features', 'pro': 'Pro', 'blog': 'Articles (RU)', 'faq': 'FAQ',
           'mac': 'For Mac (soon)', 'get': 'Download', 'menu': 'Menu', 'lang': 'Language', 'theme': 'Light or dark theme',
           'hint': 'This page is available in English', 'close': 'Close'},
    'de': {'brand': 'Pisar', 'features': 'Funktionen', 'pro': 'Pro', 'blog': 'Artikel (RU)', 'faq': 'Fragen',
           'mac': 'Für Mac (bald)', 'get': 'Download', 'menu': 'Menü', 'lang': 'Sprache', 'theme': 'Helles oder dunkles Design',
           'hint': 'Diese Seite gibt es auf Deutsch', 'close': 'Schließen'},
    'fr': {'brand': 'Pisar', 'features': 'Fonctions', 'pro': 'Pro', 'blog': 'Articles (RU)', 'faq': 'Questions',
           'mac': 'Pour Mac (bientôt)', 'get': 'Télécharger', 'menu': 'Menu', 'lang': 'Langue', 'theme': 'Thème clair ou sombre',
           'hint': 'Cette page existe en français', 'close': 'Fermer'},
    'es': {'brand': 'Pisar', 'features': 'Funciones', 'pro': 'Pro', 'blog': 'Artículos (RU)', 'faq': 'Preguntas',
           'mac': 'Para Mac (pronto)', 'get': 'Descargar', 'menu': 'Menú', 'lang': 'Idioma', 'theme': 'Tema claro u oscuro',
           'hint': 'Esta página está disponible en español', 'close': 'Cerrar'},
    'it': {'brand': 'Pisar', 'features': 'Funzioni', 'pro': 'Pro', 'blog': 'Articoli (RU)', 'faq': 'Domande',
           'mac': 'Per Mac (presto)', 'get': 'Scarica', 'menu': 'Menu', 'lang': 'Lingua', 'theme': 'Tema chiaro o scuro',
           'hint': 'Questa pagina è disponibile in italiano', 'close': 'Chiudi'},
    'pt': {'brand': 'Pisar', 'features': 'Recursos', 'pro': 'Pro', 'blog': 'Artigos (RU)', 'faq': 'Perguntas',
           'mac': 'Para Mac (em breve)', 'get': 'Baixar', 'menu': 'Menu', 'lang': 'Idioma', 'theme': 'Tema claro ou escuro',
           'hint': 'Esta página está disponível em português', 'close': 'Fechar'},
    'pl': {'brand': 'Pisar', 'features': 'Funkcje', 'pro': 'Pro', 'blog': 'Artykuły (RU)', 'faq': 'Pytania',
           'mac': 'Na Maca (wkrótce)', 'get': 'Pobierz', 'menu': 'Menu', 'lang': 'Język', 'theme': 'Jasny lub ciemny motyw',
           'hint': 'Ta strona jest dostępna po polsku', 'close': 'Zamknij'},
    'nl': {'brand': 'Pisar', 'features': 'Functies', 'pro': 'Pro', 'blog': 'Artikelen (RU)', 'faq': 'Vragen',
           'mac': 'Voor Mac (binnenkort)', 'get': 'Downloaden', 'menu': 'Menu', 'lang': 'Taal', 'theme': 'Licht of donker thema',
           'hint': 'Deze pagina is beschikbaar in het Nederlands', 'close': 'Sluiten'},
    'bg': {'brand': 'Pisar', 'features': 'Функции', 'pro': 'Pro', 'blog': 'Статии (RU)', 'faq': 'Въпроси',
           'mac': 'За Mac (скоро)', 'get': 'Изтегляне', 'menu': 'Меню', 'lang': 'Език', 'theme': 'Светла или тъмна тема',
           'hint': 'Тази страница е достъпна на български', 'close': 'Затвори'},
}

# Строки подвала. offer только у русского: оферта есть только на русском (оплата в рублях).
FOOT = {
    'ru': {'tagline': 'Диктовка в любом приложении на Android.', 'col_app': 'Писарь', 'pro_long': 'Писарь Pro',
           'col_docs': 'Документы', 'privacy': 'Политика конфиденциальности', 'terms': 'Пользовательское соглашение',
           'offer': 'Оферта', 'col_contact': 'Связь', 'col_lang': 'Язык'},
    'en': {'tagline': 'Voice typing in any Android app. Your voice stays on your phone.', 'col_app': 'Pisar',
           'pro_long': 'Pisar Pro', 'col_docs': 'Documents', 'privacy': 'Privacy Policy', 'terms': 'Terms of Use',
           'col_contact': 'Contact', 'col_lang': 'Language'},
    'de': {'tagline': 'Spracheingabe in jeder Android-App. Ihre Stimme bleibt auf dem Handy.', 'col_app': 'Pisar',
           'pro_long': 'Pisar Pro', 'col_docs': 'Rechtliches', 'privacy': 'Datenschutzerklärung', 'terms': 'Nutzungsbedingungen',
           'col_contact': 'Kontakt', 'col_lang': 'Sprache'},
    'fr': {'tagline': 'La saisie vocale dans toutes les applis Android. Votre voix reste sur le téléphone.', 'col_app': 'Pisar',
           'pro_long': 'Pisar Pro', 'col_docs': 'Documents', 'privacy': 'Politique de confidentialité', 'terms': "Conditions d'utilisation",
           'col_contact': 'Contact', 'col_lang': 'Langue'},
    'es': {'tagline': 'Dictado por voz en cualquier app de Android. Tu voz no sale del teléfono.', 'col_app': 'Pisar',
           'pro_long': 'Pisar Pro', 'col_docs': 'Documentos', 'privacy': 'Política de privacidad', 'terms': 'Condiciones de uso',
           'col_contact': 'Contacto', 'col_lang': 'Idioma'},
    'it': {'tagline': 'Dettatura vocale in ogni app Android. La tua voce resta sul telefono.', 'col_app': 'Pisar',
           'pro_long': 'Pisar Pro', 'col_docs': 'Documenti', 'privacy': 'Informativa sulla privacy', 'terms': "Condizioni d'uso",
           'col_contact': 'Contatti', 'col_lang': 'Lingua'},
    'pt': {'tagline': 'Digitação por voz em qualquer app Android. Sua voz fica no celular.', 'col_app': 'Pisar',
           'pro_long': 'Pisar Pro', 'col_docs': 'Documentos', 'privacy': 'Política de privacidade', 'terms': 'Termos de uso',
           'col_contact': 'Contato', 'col_lang': 'Idioma'},
    'pl': {'tagline': 'Pisanie głosem w każdej aplikacji na Androida. Twój głos zostaje na telefonie.', 'col_app': 'Pisar',
           'pro_long': 'Pisar Pro', 'col_docs': 'Dokumenty', 'privacy': 'Polityka prywatności', 'terms': 'Warunki korzystania',
           'col_contact': 'Kontakt', 'col_lang': 'Język'},
    'nl': {'tagline': 'Spraakinvoer in elke Android-app. Je stem blijft op je telefoon.', 'col_app': 'Pisar',
           'pro_long': 'Pisar Pro', 'col_docs': 'Documenten', 'privacy': 'Privacybeleid', 'terms': 'Gebruiksvoorwaarden',
           'col_contact': 'Contact', 'col_lang': 'Taal'},
    'bg': {'tagline': 'Гласово въвеждане във всяко приложение за Android. Гласът ви остава на телефона.', 'col_app': 'Pisar',
           'pro_long': 'Pisar Pro', 'col_docs': 'Документи', 'privacy': 'Политика за поверителност', 'terms': 'Условия за ползване',
           'col_contact': 'Контакт', 'col_lang': 'Език'},
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
    """Для переключателя: [(код, название, адрес или None, True если версия своя, иначе код запасной (en, ru) или False)]."""
    out = []
    for c, name in LANGS:
        if exists(root, c, pid):
            out.append((c, name, url(c, pid), True))
        elif exists(root, FALLBACK, pid):
            out.append((c, name, url(FALLBACK, pid), FALLBACK))
        elif exists(root, 'ru', pid):  # блог и оферта есть только на русском
            out.append((c, name, url('ru', pid), 'ru'))
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

BOOSTY = 'https://boosty.to/pozdnekov'
# Плашка Boosty в подвале: подпись на языке страницы
SUPPORT = {'ru': 'Поддержать на Boosty', 'en': 'Support on Boosty', 'de': 'Auf Boosty unterstützen',
           'fr': 'Soutenir sur Boosty', 'es': 'Apoyar en Boosty', 'it': 'Sostieni su Boosty', 'pt': 'Apoiar no Boosty',
           'pl': 'Wesprzyj na Boosty', 'nl': 'Steun op Boosty', 'bg': 'Подкрепете в Boosty'}
HEART = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3 5 6.4 5c2 0 3.6 1.1 4.4 2.6h2.4C14 6.1 15.6 5 17.6 5 21 5 23.1 8.4 21.6 11.8 19.5 16.4 12 21 12 21z"/></svg>'
def boosty_badge(lang):
    import html as _h
    txt = _h.escape(SUPPORT.get(lang, SUPPORT['en']))
    return f'<a class="boosty" href="{BOOSTY}" target="_blank" rel="noopener">{HEART}<span>{txt}</span></a>'
