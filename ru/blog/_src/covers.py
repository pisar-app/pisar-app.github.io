#!/usr/bin/env python3
"""Обложки статей: ru/blog/<slug>/og.png (1200×630, превью ссылки в Telegram и соцсетях)
и ru/blog/<slug>/thumb.webp (карточка в списке статей).

Запуск из корня сайта:  python3 ru/blog/_src/covers.py .
Нужен Pillow. Шрифт Roboto (как в Android): /Library/Fonts/Roboto-*.ttf.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
SRC = os.path.join(ROOT, 'ru', 'blog', '_src')
W, H = 1200, 630
FONT_DIRS = ['/Library/Fonts', os.path.expanduser('~/Library/Fonts'), '/usr/share/fonts/truetype/roboto']


def font(name, size):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default(size)


def load_arts():
    arts = []
    for sec in ('free', 'pro', 'scen'):
        ns = {'ROOT': ROOT}
        exec(open(os.path.join(SRC, '_lib.py'), encoding='utf-8').read(), ns)
        exec(open(os.path.join(SRC, sec + '.py'), encoding='utf-8').read(), ns)
        for a in ns['ARTS']:
            a['sec'] = sec
            arts.append(a)
    return arts


def background():
    # тот же градиент, что в полосе-заголовке сайта (тёмная тема), по диагонали
    stops = [(0, (2, 2, 16)), (.30, (11, 15, 58)), (.55, (42, 42, 122)), (.78, (106, 84, 176)), (1, (184, 150, 212))]
    grad = Image.new('RGB', (1, 256))
    for y in range(256):
        t = y / 255
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t0 <= t <= t1:
                k = (t - t0) / (t1 - t0)
                grad.putpixel((0, y), tuple(int(c0[i] + (c1[i] - c0[i]) * k) for i in range(3)))
                break
    big = grad.resize((W * 3, H * 3)).rotate(-28, resample=Image.BICUBIC, expand=False)
    cx, cy = big.width // 2, big.height // 2 - 60
    return big.crop((cx - W // 2, cy - H // 2, cx + W // 2, cy + H // 2))


def wrap(draw, text, fnt, width):
    lines, line = [], ''
    for w in text.split():
        t = (line + ' ' + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            line = t
        else:
            lines.append(line)
            line = w
    lines.append(line)
    return lines


def phone(shot):
    img = Image.open(shot).convert('RGB')
    w = 330
    img = img.resize((w, int(img.height * w / img.width)), Image.LANCZOS)
    pad, r = 10, 38
    frame = Image.new('RGBA', (w + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(frame).rounded_rectangle((0, 0, frame.width - 1, frame.height - 1), r, fill=(11, 13, 28, 255), outline=(255, 255, 255, 60), width=2)
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, img.width - 1, img.height - 1), r - 8, fill=255)
    frame.paste(img, (pad, pad), mask)
    return frame


def cover(a, out_png, out_thumb):
    im = background().convert('RGBA')
    d = ImageDraw.Draw(im)
    # телефон справа, уходит за нижний край
    ph = phone(os.path.join(ROOT, 'assets', 'shots', a['cover'] + '.webp'))
    shadow = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((812, 78, 812 + ph.width, 78 + ph.height), 40, fill=(20, 10, 60, 150))
    im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(28)))
    im.alpha_composite(ph, (800, 60))
    # метка раздела
    label, fill, ink = {'free': ('Бесплатно', (255, 255, 255, 40), (255, 255, 255)),
                        'pro': ('Pro', (245, 165, 36, 255), (22, 22, 26)),
                        'scen': ('Сценарий', (255, 255, 255, 40), (255, 255, 255))}[a['sec']]
    if a['sec'] == 'scen' and a.get('pro'):
        label, fill, ink = 'Сценарий · Pro', (245, 165, 36, 255), (22, 22, 26)
    f_lab = font('Roboto-Bold.ttf', 26)
    lw = d.textlength(label, font=f_lab)
    d.rounded_rectangle((72, 72, 72 + lw + 36, 72 + 46), 23, fill=fill)
    d.text((72 + 18, 72 + 8), label, font=f_lab, fill=ink)
    # заголовок: подбираем размер, чтобы влез в 4 строки
    title = a.get('cover_title', a['title'])
    for size in (62, 56, 50, 46, 42):
        f_t = font('Roboto-Bold.ttf', size)
        lines = wrap(d, title, f_t, 660)
        if len(lines) <= 4:
            break
    y = 160
    for ln_ in lines:
        d.text((72, y), ln_, font=f_t, fill=(255, 255, 255))
        y += int(size * 1.16)
    # подпись: логотип и сайт
    icon = Image.open(os.path.join(ROOT, 'assets', 'icon.png')).convert('RGBA').resize((56, 56), Image.LANCZOS)
    m = Image.new('L', icon.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, 55, 55), 16, fill=255)
    im.paste(icon, (72, H - 72 - 56), m)
    d.text((72 + 72, H - 72 - 52), 'Писарь', font=font('Roboto-Bold.ttf', 30), fill=(255, 255, 255))
    d.text((72 + 72, H - 72 - 16), 'pisar-app.ru', font=font('Roboto-Regular.ttf', 22), fill=(220, 220, 245))
    rgb = im.convert('RGB')
    rgb.save(out_png, optimize=True)
    rgb.resize((600, 315), Image.LANCZOS).save(out_thumb, quality=82)


if __name__ == '__main__':
    arts = load_arts()
    for a in arts:
        d = os.path.join(ROOT, 'ru', 'blog', a['slug'])
        os.makedirs(d, exist_ok=True)
        cover(a, os.path.join(d, 'og.png'), os.path.join(d, 'thumb.webp'))
    print('covers', len(arts))
