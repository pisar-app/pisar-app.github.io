# Общая разметка «Скачать» и «Mac» для всех языков (русские собирает geo.py, остальные intl.py) и значки магазинов
# (их ставит и intl.py на главную других языков). Обе страницы в стиле главной: первый экран с градиентом .hero,
# ниже секции; общие стили главной берутся из assets/blog.css, свои в assets/pages.css, значки в assets/site.css.
import re

RUSTORE = 'https://www.rustore.ru/catalog/app/com.pisar.android'
GP_LANGS = {'ru', 'en', 'de', 'fr', 'es', 'it', 'pt', 'pl', 'nl', 'bg'}  # есть assets/badges/google-play-<код>.png


# Свои кнопки магазинов одного вида (решение владельца 16.11): чёрная плитка, логотип магазина слева, две строки одним шрифтом.
# Логотипы вырезаны из официальных значков (assets/badges/icons/), источники значков в README.md.
GET_ON = {'ru': 'Скачайте в', 'en': 'Get it on', 'de': 'Jetzt bei', 'fr': 'Disponible sur', 'es': 'Disponible en',
          'it': 'Disponibile su', 'pt': 'Disponível no', 'pl': 'Pobierz z', 'nl': 'Ontdek het op', 'bg': 'Изтеглете от'}
SOON_ON = {'ru': 'Скоро в', 'en': 'Soon on', 'de': 'Bald bei', 'fr': 'Bientôt sur', 'es': 'Pronto en',
           'it': 'Presto su', 'pt': 'Em breve no', 'pl': 'Wkrótce w', 'nl': 'Binnenkort op', 'bg': 'Скоро в'}
STORE_ICONS = {'RuStore': 'rustore.svg', 'Google Play': 'google-play.png', 'GetApps': 'xiaomi.svg', 'AppGallery': 'huawei.png'}


def _btn(name, top, href=None, alt=''):
    inner = (f'<img class="sbi" src="/assets/badges/icons/{STORE_ICONS[name]}" width="30" height="30" alt="">'
             f'<span class="sbt"><small>{top}</small><b>{name}</b></span>')
    if href:
        return f'<a class="sbtn" href="{href}" target="_blank" rel="noopener" aria-label="{alt or top + " " + name}">{inner}</a>'
    return f'<span class="sbtn soon">{inner}</span>'


def _rustore(alt, lang='ru'):
    return _btn('RuStore', GET_ON.get(lang, GET_ON['en']), RUSTORE, alt)


def _soon(lang):
    top = SOON_ON.get(lang, SOON_ON['en'])
    return [_btn(n, top) for n in ('Google Play', 'GetApps', 'AppGallery')]


def badges(lang, soon, russia='', alt='RuStore'):
    """Кнопки магазинов. Русский: RuStore со ссылкой, ниже три «Скоро в». Другие языки: три «Скоро», ниже RuStore с подписью «Россия».
    Подпись «Скоро» над рядом не нужна: она есть на самих кнопках."""
    if lang == 'ru':
        groups = [('', [_rustore(alt, lang)]), ('', _soon(lang))]
    else:
        groups = [('', _soon(lang)), (russia, [_rustore(alt, lang)])]
    out = []
    for cap, items in groups:
        c = f'<span class="sb-cap">{cap}</span>' if cap else ''
        out.append(f'<div class="sb-group">{c}<div class="sb-row">{"".join(items)}</div></div>')
    return f'<div class="sbadges">{"".join(out)}</div>'


STORES = re.compile(r'<!-- stores -->[\s\S]*?<!-- /stores -->')


def fill_stores(s, block):
    """Главная: значки в метки <!-- stores --> (первый экран и блок внизу). Повторный запуск ничего не меняет."""
    assert len(STORES.findall(s)) == 2, 'на главной нет двух меток <!-- stores -->'
    n = [0]

    def one(m):
        n[0] += 1  # первый блок (первый экран) — цель кнопки «Скачать» в шапке
        b = block.replace('<div class="sbadges">', '<div class="sbadges" id="download">', 1) if n[0] == 1 else block
        return f'<!-- stores -->{b}<!-- /stores -->'
    return STORES.sub(one, s)


def shell(s, body):
    """Страница из копии Pro: всё между шапкой и подвалом заменяется своим телом, вместо legal.css стили страниц."""
    s, n = re.subn(r'(?<=</header>\n)[\s\S]*?\n(?=<footer)', lambda m: body.strip() + '\n', s, count=1)
    assert n == 1, 'нет места между </header> и <footer>'
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


def pro_body(main, shot, alt):
    """Pro (чат 38) в стиле главной. main: текст Pro как был (h1, вступление, p.price и строка под ним, дальше разделы h2).
    Всё до первого h2 уходит на первый экран с градиентом .hero: слева заголовок, вступление и цена, справа телефон
    с экраном Pro (assets/shots/app/<код>/pro.webp, корпус и свечение телефона главной); разделы ниже обычным текстом."""
    main = re.sub(r'^\s*<nav>[\s\S]*?</nav>\s*', '', main.strip())  # хлебные крошки: на странице в стиле главной не нужны
    i = main.index('<h2>')
    top, rest = main[:i].strip(), main[i:].strip()
    h1 = re.match(r'<h1>[\s\S]*?</h1>', top).group(0)
    top = top[len(h1):].strip()
    j = top.index('<p class="price">')
    intro, price = top[:j].strip(), top[j:].strip()
    return f'''<main class="ppage">
<div class="hero prohero">
  <div class="wrap" style="position:relative">
    {h1}
    <div class="lead">{intro}</div>
    <div class="pprice">{price}</div>
    <div class="stage pstage"><div class="phone"><div class="screen"><img src="{shot}" width="552" height="1197" alt="{alt}"></div></div></div>
  </div>
</div>
<section class="pdoc">
  <div class="wrap">
{rest}
  </div>
</section>
</main>'''
