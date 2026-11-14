# Порядок запуска из корня сайта: 1) python3 tools/blog.py .  2) python3 tools/footer.py .  3) python3 tools/nav.py .
# Одинаковая шапка с настоящими ссылками и активным пунктом на всех русских страницах. python3 nav.py <site_root>
import sys, os, re, glob
ROOT = sys.argv[1]
ITEMS = [('/#all', 'Возможности', None), ('/ru/blog/', 'Статьи', 'ru/blog'), ('/ru/pro/', 'Pro', 'ru/pro'), ('/#faq', 'Вопросы', None)]
n = 0
for f in glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True):
    rel = os.path.relpath(os.path.dirname(f), ROOT).replace(os.sep, '/')
    s = open(f).read()
    if '<html lang="en"' in s or '<header>' not in s: continue
    links = ''.join(f'<a href="{h}"' + (' class="on" aria-current="page"' if key and (rel == key or rel.startswith(key + '/')) else '') + f'>{t}</a>' for h, t, key in ITEMS)
    nav = f'<nav class="menu">{links}</nav>'
    if '<nav class="menu">' in s:
        s2 = re.sub(r'<nav class="menu">.*?</nav>', nav, s, count=1)
    else:  # правовые страницы без меню: вставить после логотипа
        s2 = re.sub(r'(<header>\s*<div class="wrap bar">\s*<a class="logo"[^>]*>.*?</a>)\s*', r'\1\n    ' + nav + '\n    ', s, count=1, flags=re.S)
    if s2 != s: open(f, 'w').write(s2); n += 1
print('navs', n)
