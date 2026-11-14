# Помощники разметки статей. Подключается tools/blog.py перед free.py, pro.py, scen.py.
# Классы: из шаблона статьи (EXTRA_CSS в tools/blog.py).
import os as _os

SHOT_CAP = {
    'dikt2': 'Вкладка «Диктовка»', 'rasp': 'Настройки → Распознавание', 'slovar': 'Вкладка «Словарь»',
    'bufer': 'Вкладка «Буфер»', 'rassh': 'Вкладка «Расшифровка»', 'pro': 'Экран «Писарь Pro»',
}


def has_shot(name):
    return bool(name) and _os.path.exists(_os.path.join(ROOT, 'assets', 'shots', name + '.webp'))


def fig(name, cap=None):
    cap = cap or SHOT_CAP.get(name, '')
    return f'<figure class="appshot"><img src="/assets/shots/{name}.webp" alt="{cap}" loading="lazy"><figcaption>{cap}</figcaption></figure>'


def scen(*cards):
    """Карточки «когда выручает»: (значок Material, заголовок, текст)."""
    return '<div class="scen">' + ''.join(f'<div class="sc"><span class="mi">{i}</span><b>{t}</b><p>{p}</p></div>' for i, t, p in cards) + '</div>'


def steps(items, shot=None, cap=None):
    """Шаги «нажал → получил»; со скриншотом справа, если он есть в assets/shots."""
    ol = '<ol class="steps">' + ''.join(f'<li>{x}</li>' for x in items) + '</ol>'
    return f'<div class="howto">{ol}{fig(shot, cap)}</div>' if has_shot(shot) else ol


def side(html, shot, cap=None):
    """Абзацы со скриншотом справа."""
    return f'<div class="howto"><div>{html}</div>{fig(shot, cap)}</div>' if has_shot(shot) else html


def ex(icon, title, small, out, before=None):
    """Пример до → после. before: что сказали голосом (кавычки ставятся тут)."""
    head = f'<div class="ex-in"><span class="mi">{icon}</span><div><b>{title}</b><small>{small}</small></div></div>'
    if before:
        head += f'<p class="ex-out said">«{before}»</p>'
    return f'<div class="ex">{head}<div class="ex-arr"><span class="mi">south</span></div><p class="ex-out">{out}</p></div>'


def pm(plus, minus):
    """Плюсы и минусы двумя колонками."""
    li = lambda xs: ''.join(f'<li>{x}</li>' for x in xs)
    return (f'<div class="pm"><div><h3>Плюсы</h3><ul class="ticks">{li(plus)}</ul></div>'
            f'<div><h3>Минусы и ограничения</h3><ul>{li(minus)}</ul></div></div>')


def table(head, rows):
    th = ''.join(f'<th>{h}</th>' for h in head)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="t"><tr>{th}</tr>{tr}</table>'


def note(html):
    return f'<p class="note">{html}</p>'


def ln(slug, text):
    return f'<a href="/ru/blog/{slug}/">{text}</a>'
