# Подвал на всех страницах всех языков, включая главную: колонки и список языков.
# Строки в tools/i18n.py (FOOT). Свой CSS каждой страницы не трогает: стили подвала в assets/site.css и базе.
# Запуск: python3 tools/footer.py .   (всё сразу: python3 tools/build.py)
import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18n import HEAD, FOOT, EMAIL, t, link, pages, boosty_badge
from nav import menu_items, lang_items


def footer(root, lang, pid):
    f = lambda k: html.escape(t(FOOT, lang, k))
    h = lambda k: html.escape(t(HEAD, lang, k))
    app = ''.join(f'<a href="{u}">{f("pro_long") if k == "pro" else h(k)}</a>' for k, u, _ in menu_items(root, lang, pid))
    docs = f'<a href="{link(root, lang, "privacy")}">{f("privacy")}</a><a href="{link(root, lang, "terms")}">{f("terms")}</a>'
    if FOOT.get(lang, {}).get('offer'):
        docs += f'<a href="{link(root, lang, "pro/offer")}">{f("offer")}</a>'
    return f'''<footer>
  <div class="wrap fcols">
    <div class="fbrand"><a class="logo" href="{link(root, lang, '')}"><img src="/assets/icon.png" alt="" style="width:28px;height:28px;border-radius:8px">{h('brand')}</a><p>{f('tagline')}</p><p class="copy">© 2026 Pozdnekov Labs</p></div>
    <nav><h4>{f('col_app')}</h4>{app}</nav>
    <nav><h4>{f('col_docs')}</h4>{docs}</nav>
    <nav><h4>{f('col_contact')}</h4><a href="mailto:{EMAIL}">{EMAIL}</a>{boosty_badge(lang)}</nav>
  </div>
  <div class="wrap"><nav class="flangs" aria-label="{f('col_lang')}"><h4>{f('col_lang')}</h4>{re.sub(r'<small>.*?</small>', '', lang_items(root, lang, pid, tag=''))}</nav></div>
</footer>'''


def apply(root, s, lang, pid):
    return re.sub(r'<footer\b[^>]*>.*?</footer>', lambda m: footer(root, lang, pid), s, count=1, flags=re.S)


if __name__ == '__main__':
    ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
    n = 0
    for fn, lang, pid in pages(ROOT):
        s0 = open(fn, encoding='utf-8').read()
        if '<footer' not in s0:
            continue
        s = apply(ROOT, s0, lang, pid)
        if s != s0:
            open(fn, 'w', encoding='utf-8').write(s); n += 1
    print('footers', n)
