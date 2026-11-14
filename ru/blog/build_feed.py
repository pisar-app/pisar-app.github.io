#!/usr/bin/env python3
"""Лента блога: ru/blog/feed.json (для приложения), ru/blog/rss.xml (для Telegram-ботов)\nи ru/blog/telegram/<slug>.md (анонс для поста: заголовок, 1–2 предложения, ссылка; превью подтянет og.png).

Запуск из корня сайта после любой правки статей:  python3 ru/blog/build_feed.py
Источник: сами статьи ru/blog/<slug>/index.html:
  title: <h1>, date: "datePublished" из JSON-LD, description: <meta name="description">,
  pro: карточка статьи в ru/blog/index.html содержит метку class="badge pro".
Формат описан в ru/blog/README.md.
"""
import html
import json
import pathlib
import re
from email.utils import format_datetime
from datetime import datetime, timezone

SITE = "https://pisar-app.ru"
BLOG = pathlib.Path(__file__).resolve().parent


def pick(rx, text):
    m = re.search(rx, text, re.S)
    return html.unescape(m.group(1).strip()) if m else ""


def pro_slugs():
    index = (BLOG / "index.html").read_text(encoding="utf-8")
    cards = re.findall(r'<a class="art" href="/ru/blog/([^/"]+)/">(.*?)</a>', index, re.S)
    return {slug for slug, body in cards if 'badge pro' in body}


def articles():
    pro = pro_slugs()
    out = []
    for page in sorted(BLOG.glob("*/index.html")):
        slug = page.parent.name
        text = page.read_text(encoding="utf-8")
        out.append({
            "slug": slug,
            "title": pick(r"<h1[^>]*>(.*?)</h1>", text),
            "url": f"{SITE}/ru/blog/{slug}/",
            "date": pick(r'"datePublished":\s*"([^"]+)"', text),
            "pro": slug in pro,
            "description": pick(r'<meta name="description" content="([^"]*)"', text),
        })
    out.sort(key=lambda a: (a["date"], a["slug"]), reverse=True)
    return out


def rss(items):
    def rfc(d):
        return format_datetime(datetime.fromisoformat(d).replace(hour=9, tzinfo=timezone.utc))
    e = html.escape
    rows = "".join(
        f"<item><title>{e(a['title'])}</title><link>{a['url']}</link><guid>{a['url']}</guid>"
        f"<pubDate>{rfc(a['date'])}</pubDate><description>{e(a['description'])}</description></item>\n"
        for a in items)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>\n'
            f"<title>Писарь: статьи</title><link>{SITE}/ru/blog/</link>"
            "<description>Как пользоваться Писарем: диктовка, расшифровка голосовых, текст со скриншотов</description>"
            "<language>ru</language>\n" + rows + "</channel></rss>\n")


if __name__ == "__main__":
    items = articles()
    feed = [{k: a[k] for k in ("slug", "title", "url", "date", "pro")} for a in items]
    (BLOG / "feed.json").write_text(json.dumps(feed, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (BLOG / "rss.xml").write_text(rss(items), encoding="utf-8")
    tg = BLOG / "telegram"
    tg.mkdir(exist_ok=True)
    for a in items:
        lock = " (Pro)" if a["pro"] else ""
        (tg / f"{a['slug']}.md").write_text(f"**{a['title']}**{lock}\n\n{a['description']}\n\n👉 {a['url']}\n", encoding="utf-8")
    print(f"feed.json, rss.xml и telegram/*.md: {len(items)} статей")
