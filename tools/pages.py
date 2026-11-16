# Общая разметка страниц «Скачать» и «Mac» для всех языков (русские собирает geo.py, остальные intl.py).
# Стили в assets/legal.css (блоки .stores и .mbp).


def stores(items):
    """Магазины сеткой. items: [(название, подпись, ссылка или None)]."""
    li = []
    for name, note, href in items:
        inner = f'<span class="sn">{name}</span><span class="st">{note}</span>'
        if href:
            li.append(f'<li class="on"><a href="{href}" target="_blank" rel="noopener">{inner}</a></li>')
        else:
            li.append(f'<li><div>{inner}</div></li>')
    return '<ul class="stores">\n' + '\n'.join(li) + '\n</ul>'


def get_main(intro, items, after=''):
    """Скачать: слева текст, справа магазины (на ПК), на телефоне одно под другим."""
    return f'<div class="cols">\n<div class="intro">\n{intro.strip()}\n</div>\n<div class="side">\n{stores(items)}\n</div>\n</div>\n{after}'.rstrip()


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
    """Функции Mac блоками, как «Всё, что умеет Писарь» на главной: иконка и заголовок в строку, ниже одна-две строки."""
    li = '\n'.join(f'<li><span class="ico"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">{ICONS[k]}</svg></span>'
                   f'<h3>{F[k][0]}</h3><p>{F[k][1]}</p></li>' for k in FEATS)
    return f'<section class="mfeats">\n<h2>{head}</h2>\n<p class="msub">{sub}</p>\n<ul class="feats">\n{li}\n</ul>\n</section>'


def notify(N, lang):
    """«Сообщить о выходе»: почта в лист ожидания облака Pro (cloud/pro, /waitlist, CORS только для pisar-app.ru).
    Отправляет assets/notify.js; тексты ответов в data-*. website — ловушка для роботов, людям не видна."""
    msgs = ' '.join(f'data-{k}="{N[k]}"' for k in ('empty', 'bad', 'ok', 'many', 'err', 'wait'))
    return f'''<form class="notify" action="https://api.pisar-app.ru/waitlist" method="post" novalidate {msgs}>
<label for="nm">{N['label']}</label>
<div class="nrow"><input id="nm" type="email" name="email" required maxlength="254" autocomplete="email" inputmode="email" placeholder="{N['ph']}"><button type="submit">{N['btn']}</button></div>
<div class="hp" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
<p class="nmsg" role="status" aria-live="polite"></p>
<p class="nnote">{N['note'].format(href=f'/{lang}/privacy/')}</p>
</form>'''


def mac_main(text, alt, after=''):
    """Mac: слева текст «скоро» и форма, справа MacBook с окном Писаря (снимок макета, assets/shots/mac.webp), ниже функции."""
    return f'''<div class="cols">
<div class="intro">
{text.strip()}
</div>
<figure class="mbp"><div class="mbp-lid"><div class="mbp-scr"><img src="/assets/shots/mac.webp" width="1600" height="896" alt="{alt}"></div><i class="mbp-cam"></i></div><div class="mbp-base"><i></i></div></figure>
</div>
{after}'''.rstrip()
