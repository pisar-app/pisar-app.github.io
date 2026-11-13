# Блог pisar-app.ru/ru/blog/

## Лента статей

После любой правки статей из корня сайта: `python3 ru/blog/build_feed.py`. Скрипт пересобирает два файла.

### `ru/blog/feed.json` — для приложения

https://pisar-app.ru/ru/blog/feed.json — массив, новые статьи сверху (по `date`, затем по `slug`).

| Поле | Тип | Что это |
|---|---|---|
| `slug` | строка | адрес статьи, папка `ru/blog/<slug>/` |
| `title` | строка | заголовок `<h1>` |
| `url` | строка | полный адрес `https://pisar-app.ru/ru/blog/<slug>/` |
| `date` | строка `ГГГГ-ММ-ДД` | `datePublished` статьи |
| `pro` | bool | статья про функцию Pro (в списке статей у неё метка Pro) |

```json
[{"slug": "tekst-so-skrinshota", "title": "Как скопировать текст со скриншота или фото",
  "url": "https://pisar-app.ru/ru/blog/tekst-so-skrinshota/", "date": "2026-11-13", "pro": true}]
```

Поля только добавляются, старые не переименовываются и не удаляются.

### `ru/blog/rss.xml` — RSS 2.0 для Telegram-ботов

https://pisar-app.ru/ru/blog/rss.xml — `title`, `link`, `guid`, `pubDate`, `description` (из `<meta name="description">`).
