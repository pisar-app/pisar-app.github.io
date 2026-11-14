# Порядок запуска из корня сайта: 1) python3 tools/blog.py .  2) python3 tools/footer.py .  3) python3 tools/nav.py .
# Новый подвал по колонкам на все страницы, кроме главной (её подвал ставит round2.py). python3 footer.py <site_root>
import sys, os, re, glob
ROOT = sys.argv[1]
home = open(os.path.join(ROOT, 'index.html')).read()
RU = re.search(r'<footer>.*?</footer>', home, re.S).group(0)
EN = '''<footer>
  <div class="wrap fcols">
    <div class="fbrand"><a class="logo" href="/"><img src="/assets/icon.png" alt="" style="width:28px;height:28px;border-radius:8px">Pisar</a><p>Voice typing in any Android app. Your voice stays on your phone.</p><p class="copy">© 2026 Pozdnekov Labs</p></div>
    <nav><h4>Documents</h4><a href="/en/privacy/">Privacy Policy</a><a href="/en/terms/">Terms of Use</a><a href="/ru/privacy/">Русский</a></nav>
    <nav><h4>Contact</h4><a href="mailto:poal0208@gmail.com">poal0208@gmail.com</a></nav>
  </div>
</footer>'''
n = 0
for f in glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True):
    if os.path.samefile(f, os.path.join(ROOT, 'index.html')) or '/.git/' in f: continue
    s = open(f).read()
    if '<footer>' not in s: continue
    new = EN if '<html lang="en"' in s else RU
    s2 = re.sub(r'<footer>.*?</footer>', lambda m: new, s, count=1, flags=re.S)
    if s2 != s: open(f, 'w').write(s2); n += 1
print('footers', n)
