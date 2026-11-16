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


def mac_main(text, alt, cap):
    """Mac: слева текст «скоро», справа MacBook с окном Писаря (снимок макета, assets/shots/mac.webp)."""
    return f'''<div class="cols">
<div class="intro">
{text.strip()}
</div>
<figure class="mbp"><div class="mbp-lid"><div class="mbp-scr"><img src="/assets/shots/mac.webp" width="1600" height="896" alt="{alt}"></div><i class="mbp-cam"></i></div><div class="mbp-base"><i></i></div><figcaption>{cap}</figcaption></figure>
</div>'''
