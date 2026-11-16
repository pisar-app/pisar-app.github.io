# Оглавление сбоку у документов (политика, соглашение, оферта) на всех языках.
# Ставит якоря s-1, s-2… на <h2> внутри <main> и блок <aside class="toc"> после </main>.
# На экране от 1100 px оглавление справа и едет со страницей, уже скрыто (assets/legal.css).
# Запуск: python3 tools/toc.py .   (всё сразу: python3 tools/build.py). Повторный запуск ничего не меняет.
import sys, os, re, glob

LABEL = {'ru': 'Содержание', 'en': 'Contents', 'de': 'Inhalt', 'fr': 'Sommaire', 'es': 'Índice', 'it': 'Indice',
         'pt': 'Índice', 'pl': 'Spis treści', 'nl': 'Inhoud', 'bg': 'Съдържание'}
TOC_RE = re.compile(r'<aside class="toc"[\s\S]*?</aside>\n?')
ID_RE = re.compile(r'<h2 id="s-\d+">')


def strip(s):
    """Страница без оглавления и якорей (intl.py берёт русскую политику как основу для перевода)."""
    s = TOC_RE.sub('', s)
    s = ID_RE.sub('<h2>', s)
    return s.replace('<div class="legal has-toc">', '<div class="legal">', 1)


def apply(s, lang=None):
    s = strip(s)
    lang = lang or re.search(r'<html lang="(\w+)"', s).group(1)
    a, b = s.index('<main>'), s.index('</main>')
    main, n, items = s[a:b], 0, []

    def anchor(m):
        nonlocal n
        n += 1
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        items.append(f'<li><a href="#s-{n}">{title}</a></li>')
        return f'<h2 id="s-{n}">{m.group(1)}</h2>'
    main = re.sub(r'<h2>([\s\S]*?)</h2>', anchor, main)
    if n < 3:
        return s
    aside = (f'<aside class="toc" aria-label="{LABEL[lang]}"><p>{LABEL[lang]}</p><ol>\n'
             + '\n'.join(items) + '\n</ol></aside>\n')
    s = s[:a] + main + s[b:b + len('</main>')] + '\n' + aside + s[b + len('</main>'):].lstrip('\n')
    return s.replace('<div class="legal">', '<div class="legal has-toc">', 1)


if __name__ == '__main__':
    ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
    files = sorted(glob.glob(os.path.join(ROOT, '*/privacy/index.html')) + glob.glob(os.path.join(ROOT, '*/terms/index.html'))
                   + glob.glob(os.path.join(ROOT, 'ru/pro/offer/index.html')))
    for f in files:
        old = open(f, encoding='utf-8').read()
        new = apply(old)
        if new != old:
            open(f, 'w', encoding='utf-8').write(new)
            print('  обновлён', os.path.relpath(f, ROOT))
    print('toc: ok,', len(files), 'страниц')
