# Сборка сайта целиком, по порядку. Запуск из корня сайта: python3 tools/build.py
# blog: статьи и assets/blog.css; geo: разметка и llms.txt; footer и nav: подвал, шапка, языки на всех страницах.
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
for step in ('blog', 'geo', 'footer', 'nav'):
    subprocess.run([sys.executable, os.path.join(HERE, step + '.py'), ROOT], check=True)
