# Общая разметка «Скачать» и «Mac» для всех языков (русские собирает geo.py, остальные intl.py) и значки магазинов
# (их ставит и intl.py на главную других языков). Обе страницы в стиле главной: первый экран с градиентом .hero,
# ниже секции; общие стили главной берутся из assets/blog.css, свои в assets/pages.css, значки в assets/site.css.
import re

RUSTORE = 'https://www.rustore.ru/catalog/app/com.pisar.android'
GP_LANGS = {'ru', 'en', 'de', 'fr', 'es', 'it', 'pt', 'pl', 'nl', 'bg'}  # есть assets/badges/google-play-<код>.png


def _rustore(alt):
    """Официальный значок RuStore (assets/rustore-color-dark.svg) в обеих темах: все значки одинаковые чёрные плитки."""
    return (f'<a class="sb-rs" href="{RUSTORE}" target="_blank" rel="noopener">'
            f'<img src="/assets/rustore-color-dark.svg" width="111" height="40" alt="{alt}"></a>')


def _soon(lang):
    """Магазины, где Писаря ещё нет: официальные значки без ссылок, одной высоты, не перекрашены. Источники и условия в README.md.
    Google Play на языке страницы; Xiaomi (архив значков с сайта GetApps) и Huawei (сайт Huawei Mobile Services) есть только на английском."""
    gp = lang if lang in GP_LANGS else 'en'
    return [f'<span class="sb-gp"><img src="/assets/badges/google-play-{gp}.png" width="646" height="192" alt="Google Play"></span>',
            '<span class="sb-gp"><img src="/assets/badges/xiaomi-getapps.svg" width="255" height="80" alt="Xiaomi GetApps"></span>',
            '<span class="sb-gp"><img src="/assets/badges/huawei-appgallery.png" width="570" height="170" alt="Huawei AppGallery"></span>']


def badges(lang, soon, russia='', alt='RuStore'):
    """Значки магазинов группами. Русский: RuStore со ссылкой, ниже «Скоро» и три магазина.
    Другие языки: «Скоро» Google Play, Xiaomi, Huawei; ниже RuStore с подписью «Россия»."""
    if lang == 'ru':
        groups = [('', [_rustore(alt)]), (soon, _soon(lang))]
    else:
        groups = [(soon, _soon(lang)), (russia, [_rustore(alt)])]
    out = []
    for cap, items in groups:
        c = f'<span class="sb-cap">{cap}</span>' if cap else ''
        out.append(f'<div class="sb-group">{c}<div class="sb-row">{"".join(items)}</div></div>')
    return f'<div class="sbadges">{"".join(out)}</div>'


STORES = re.compile(r'<!-- stores -->[\s\S]*?<!-- /stores -->')


def fill_stores(s, block):
    """Главная: значки в метки <!-- stores --> (первый экран и блок внизу). Повторный запуск ничего не меняет."""
    assert len(STORES.findall(s)) == 2, 'на главной нет двух меток <!-- stores -->'
    return STORES.sub(lambda m: f'<!-- stores -->{block}<!-- /stores -->', s)


def shell(s, body):
    """Страница из копии Pro: вместо карточки документа своё тело, вместо legal.css стили страниц."""
    s = re.sub(r'<div class="legal[^"]*"><div class="wrap">[\s\S]*?\n(?=<footer)', lambda m: body.strip() + '\n', s, count=1)
    return s.replace('<link rel="stylesheet" href="/assets/legal.css">', '<link rel="stylesheet" href="/assets/pages.css">', 1)


def get_body(h1, lead, stores, note):
    """Скачать: первый экран как на главной, по центру: заголовок, строка, значки, требования."""
    return f'''<main class="hero phero">
  <div class="wrap" style="position:relative">
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    {stores}
    <p class="note">{note}</p>
  </div>
</main>'''


# Иконки функций Mac (24×24, заливка цветом текста): своё SVG, без шрифта иконок, которого на этих страницах нет
ICONS = {
    'rec': '<path d="M20 3H4a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2h5v2H7v2h10v-2h-2v-2h5a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2Zm0 13H4V5h16v11Z"/><circle cx="12" cy="10.5" r="3"/>',
    'reel': '<path d="M16 1H8a3 3 0 0 0-3 3v16a3 3 0 0 0 3 3h8a3 3 0 0 0 3-3V4a3 3 0 0 0-3-3Zm1 19a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v16Z"/><path d="M10 8.5v7l5.5-3.5z"/>',
    'tr': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6Zm4 18H6V4h7v5h5v11Z"/><path d="M8 12h8v2H8zm0 4h5v2H8z"/>',
    'dict': '<path d="M12 14a3 3 0 0 0 3-3V5a3 3 0 0 0-6 0v6a3 3 0 0 0 3 3Zm5-3a5 5 0 0 1-10 0H5a7 7 0 0 0 6 6.92V21h2v-3.08A7 7 0 0 0 19 11h-2Z"/>',
    'clip': '<path d="M19 3h-4.18a3 3 0 0 0-5.64 0H5a2 2 0 0 0-2 2v15a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2Zm-7 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2Zm7 17H5V5h2v3h10V5h2v15Z"/>',
    'scr': '<path d="M3 3h6v2H5v4H3V3Zm12 0h6v6h-2V5h-4V3ZM3 15h2v4h4v2H3v-6Zm16 4v-4h2v6h-6v-2h4Z"/><path d="M7 7h10v3h-2V9h-2v7h1.5v2h-5v-2H11V9H9v1H7V7Z"/>',
}
FEATS = ('rec', 'reel', 'tr', 'dict', 'clip', 'scr')  # порядок блоков; тексты в F[ключ] = (заголовок, строка)


def feats(head, sub, F):
    """Функции Mac секцией «Всё, что умеет Писарь» главной: те же .fgrid, .fcard и .ico (сетка 3 колонки)."""
    cards = '\n'.join(f'      <div class="fcard"><div class="ico"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">{ICONS[k]}</svg></div>'
                      f'<h3>{F[k][0]}</h3><p>{F[k][1]}</p></div>' for k in FEATS)
    return f'''<section id="features" class="sec2">
  <div class="wrap">
    <div class="center"><h2>{head}</h2><p class="sub">{sub}</p></div>
    <div class="fgrid mgrid">
{cards}
    </div>
  </div>
</section>'''


def notify(N, lang):
    """«Сообщить о выходе»: почта в лист ожидания облака Pro (cloud/pro, /waitlist, CORS только для pisar-app.ru).
    Отправляет assets/notify.js; тексты ответов в data-*. website: ловушка для роботов, людям не видна."""
    msgs = ' '.join(f'data-{k}="{N[k]}"' for k in ('empty', 'bad', 'ok', 'many', 'err', 'wait'))
    return f'''<form class="notify" id="notify" action="https://api.pisar-app.ru/waitlist" method="post" novalidate {msgs}>
<label for="nm">{N['label']}</label>
<div class="nrow"><input id="nm" type="email" name="email" required maxlength="254" autocomplete="email" inputmode="email" placeholder="{N['ph']}"><button type="submit">{N['btn']}</button></div>
<div class="hp" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
<p class="nmsg" role="status" aria-live="polite"></p>
<p class="nnote">{N['note'].format(href=f'/{lang}/privacy/')}</p>
</form>'''


def mac_body(h1, soon, p, form, alt, after):
    """Mac: первый экран как у главной (слева заголовок, «Скоро» и форма, справа MacBook с окном assets/shots/mac.webp
    в корпусе и со свечением телефона главной), ниже функции."""
    return f'''<main>
<div class="hero mhero">
  <div class="wrap" style="position:relative">
    <h1>{h1}</h1>
    <p class="lead"><b>{soon}</b> <span>{p}</span></p>
    {form}
    <figure class="mbp"><div class="mbp-lid"><div class="mbp-scr"><img src="/assets/shots/mac.webp" width="1600" height="896" alt="{alt}"></div><i class="mbp-cam"></i></div><div class="mbp-base"><i></i></div></figure>
  </div>
</div>
{after}
</main>'''
