# Шапка на всех страницах всех языков: логотип, вкладки Android | Mac, меню (у Mac своё), переключатель языка, тема, «Скачать», ☰ на телефоне.
# Ещё ставит в <head>: assets/site.css, assets/site.js, hreflang/x-default по реально существующим версиям, <html lang>.
# Строки в tools/i18n.py. Запуск: python3 tools/nav.py .   (всё сразу: python3 tools/build.py)
import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18n import HEAD, SITE, FALLBACK, NAMES, t, link, versions, exists, url, pages, CODES

CHEVRON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
BARS = ('<svg class="i-bars" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
        '<svg class="i-x" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>')
THEME = ('<svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>'
         '<svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>')


def is_mac(pid):
    return pid == 'mac' or pid.startswith('mac/')


def menu_items(root, lang, pid, footer=False):
    """[(ключ строки, адрес, раздел для подсветки)]. Android: на главной якоря, с других страниц /#all.
    Mac: свои пункты, якоря на блок функций и форму на той же странице. В подвале всегда Android и ссылка на Mac."""
    if is_mac(pid) and not footer:
        return [('features', '#features', None), ('notify', '#notify', None)]
    home = link(root, lang, '')
    sec = (lambda a: '#' + a) if pid == '' else (lambda a: home + '#' + a)
    return [('features', sec('all'), None), ('pro', link(root, lang, 'pro'), 'pro'),
            ('blog', link(root, lang, 'blog'), 'blog'), ('faq', sec('faq'), None)] + \
        ([('mac', link(root, lang, 'mac'), 'mac')] if footer else [])


def tabs(root, lang, pid, s):
    """Вкладки «Android | Mac» рядом с логотипом: какая версия Писаря на странице."""
    mac = is_mac(pid)
    cur = ' class="on" aria-current="true"'
    a, m = ('', cur) if mac else (cur, '')
    return (f'<nav class="plat" aria-label="{s("plat")}"><a href="{link(root, lang, "")}"{a}>Android</a>'
            f'<a href="{link(root, lang, "mac")}"{m}>Mac<small>{s("soon")}</small></a></nav>')


def is_on(pid, key):
    return bool(key) and (pid == key or pid.startswith(key + '/'))


def lang_items(root, lang, pid, tag='li'):
    """Пункты списка языков. Настоящая версия: hreflang и data-hint; запасная (английская, для блога и оферты русская): без hreflang; нет: неактивен."""
    out = []
    for c, name, u, real in versions(root, pid):
        if c == lang:
            a = f'<a href="{url(c, pid) if exists(root, c, pid) else u}" lang="{c}" class="on" aria-current="true">{name}<small>{c.upper()}</small></a>'
        elif u and real is True:
            a = (f'<a href="{u}" hreflang="{c}" lang="{c}" data-hint="{html.escape(t(HEAD, c, "hint"))}" '
                 f'data-close="{html.escape(t(HEAD, c, "close"))}">{name}<small>{c.upper()}</small></a>')
        elif u:
            a = f'<a href="{u}" lang="{c}" title="{NAMES[real]}">{name}<small>{real.upper()}</small></a>'
        else:
            a = f'<span class="off" lang="{c}" aria-disabled="true">{name}<small>{c.upper()}</small></span>'
        out.append(f'<{tag}>{a}</{tag}>' if tag else a)
    return ''.join(out)


def header(root, lang, pid):
    s = lambda k: html.escape(t(HEAD, lang, k))
    links = ''.join(f'<a href="{h}"' + (' class="on" aria-current="page"' if is_on(pid, key) else '') + f'>{s(k)}</a>'
                    for k, h, key in menu_items(root, lang, pid))
    name = dict((c, n) for c, n, _, _ in versions(root, pid))[lang]
    # главная кнопка: на Android «Скачать», на Mac «Сообщить о выходе»; на телефоне она же первым пунктом в ☰
    btn = ('#notify', s('notify')) if is_mac(pid) else (link(root, lang, 'get'), s('get'))
    if not is_mac(pid):
        links = f'<a class="mget" href="{btn[0]}">{btn[1]}</a>' + links
    return f'''<header class="hd" data-lang="{lang}">
  <div class="wrap hd-bar">
    <a class="logo" href="{link(root, lang, '')}"><img src="/assets/icon.png" alt=""><span class="lt">{s('brand')}</span></a>
    {tabs(root, lang, pid, s)}
    <nav class="hd-menu" id="hdmenu" aria-label="{s('menu')}">{links}</nav>
    <div class="spacer"></div>
    <div class="lsw"><button class="lbtn" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="lmenu" aria-label="{s('lang')}: {name}">{lang.upper()}{CHEVRON}</button><ul class="lmenu" id="lmenu" hidden>{lang_items(root, lang, pid)}</ul></div>
    <button class="tbtn" id="tbtn" type="button" aria-label="{s('theme')}">{THEME}</button>
    <a class="getbtn" href="{btn[0]}">{btn[1]}</a>
    <button class="burger" type="button" aria-controls="hdmenu" aria-expanded="false" aria-label="{s('menu')}">{BARS}</button>
  </div>
</header>'''


def alternates(root, pid):
    have = [c for c in CODES if exists(root, c, pid)]
    if len(have) < 2:
        return ''
    xd = FALLBACK if FALLBACK in have else have[0]
    return ''.join(f'<link rel="alternate" hreflang="{c}" href="{SITE}{url(c, pid)}">\n' for c in have) + \
        f'<link rel="alternate" hreflang="x-default" href="{SITE}{url(xd, pid)}">\n'


def apply(root, s, lang, pid):
    """Шапка и служебное в <head> для одной страницы."""
    s = re.sub(r'<header\b[^>]*>.*?</header>', lambda m: header(root, lang, pid), s, count=1, flags=re.S)
    s = re.sub(r'<html lang="[^"]*"', f'<html lang="{lang}"', s, count=1)
    s = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', s)
    s = re.sub(r'<!-- lang -->.*?<!-- /lang -->\n', '', s, flags=re.S)
    s = s.replace('<link rel="stylesheet" href="/assets/site.css">\n', '').replace('<script src="/assets/site.js" defer></script>\n', '')
    block = ('<!-- lang -->\n' + alternates(root, pid) + '<link rel="stylesheet" href="/assets/site.css">\n'
             '<script src="/assets/site.js" defer></script>\n<!-- /lang -->\n')
    return s.replace('</head>', block + '</head>', 1)


if __name__ == '__main__':
    ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
    n = 0
    for f, lang, pid in pages(ROOT):
        s0 = open(f, encoding='utf-8').read()
        if '<header' not in s0:
            continue
        s = apply(ROOT, s0, lang, pid)
        if s != s0:
            open(f, 'w', encoding='utf-8').write(s); n += 1
    print('navs', n)
