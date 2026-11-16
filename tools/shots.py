# Экраны Писаря для телефона на главной (прокрутка блоков Pro) и на Pro: вырезаны из скриншотов магазинов
# репозитория pisar-android (docs/rustore-screens для русского, docs/store-screens/<код> для остальных), только экран
# телефона без рамки и подписи. Результат: assets/shots/app/<код>/<имя>.webp. В сборку (build.py) не входит:
# запускать, когда в pisar-android обновились скриншоты: python3 tools/shots.py [путь к pisar-android]
import os, sys
from PIL import Image

ANDROID = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/Documents/Project/pisar-android')
LANGS = ['ru', 'en', 'de', 'fr', 'es', 'it', 'pt', 'pl', 'nl', 'bg']
NAMES = {'tr': 5, 'voice': 6, 'ocr': 7, 'clip': 8, 'pro': 9}  # номер скриншота в магазине
BOX = (194, 330, 885, 1829)  # экран внутри рамки телефона на скриншоте 1080×1920
W = 552  # ширина файла: телефон на сайте около 270 px, вдвое для плотных экранов

out_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'shots', 'app')
for lang in LANGS:
    src = os.path.join(ANDROID, 'docs', 'rustore-screens' if lang == 'ru' else f'store-screens/{lang}')
    os.makedirs(os.path.join(out_root, lang), exist_ok=True)
    for name, n in NAMES.items():
        im = Image.open(os.path.join(src, f'{n}.png')).convert('RGB')
        assert im.size == (1080, 1920), (lang, n, im.size)
        im = im.crop(BOX)
        im = im.resize((W, round(W * im.height / im.width)), Image.LANCZOS)
        im.save(os.path.join(out_root, lang, name + '.webp'), 'WEBP', quality=84, method=6)
print('shots: ok')
