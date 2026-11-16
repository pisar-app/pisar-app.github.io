# Блог pisar-app.ru/ru/blog/

## Лента статей

После любой правки статей из корня сайта: `python3 ru/blog/build_feed.py`. Скрипт пересобирает два файла.

### `ru/blog/feed.json`: для приложения

https://pisar-app.ru/ru/blog/feed.json: массив, новые статьи сверху (по `date`, затем по `slug`).

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

### `ru/blog/rss.xml`: RSS 2.0 для Telegram-ботов

https://pisar-app.ru/ru/blog/rss.xml: `title`, `link`, `guid`, `pubDate`, `description` (из `<meta name="description">`).

## Статьи

Тексты: `ru/blog/_src/free.py` (бесплатные функции), `pro.py` (Писарь Pro), `scen.py` (сценарии); помощники разметки в `_lib.py`. Шаблон, стили, шапка и подвал: `tools/blog.py`, `tools/footer.py`, `tools/nav.py` (чат «Сайт»).

Сборка из корня сайта, по порядку:

1. `python3 ru/blog/_src/covers.py .`: обложки `ru/blog/<slug>/og.png` (1200×630, превью ссылки) и `thumb.webp` (карточка).
2. `python3 tools/blog.py .`: страницы, `assets/blog.css`, `sitemap.xml`; в конце сам вызывает `build_feed.py`.
3. `python3 tools/footer.py .`
4. `python3 tools/nav.py .`

`ru/blog/telegram/<slug>.md`: анонс для поста в Telegram (заголовок, 1–2 предложения, ссылка). Картинку Telegram подтянет из og.png.

## Проверка 16.11

Сверено с `pisar-android` (main, `strings_help.xml`, `strings_pro.xml`, `PisarAccessibilityService.kt`, `Fillers.kt`), `docs/rustore-listing.md` §1, `docs/dictation-quality.md`. Во всех статьях: `seo` (тег `<title>`) с запросом в начале, до 62 знаков; запрос в первом абзаце (`lead`); `dateModified` 2026-11-16 (`MOD` в `tools/blog.py`); JSON-LD HowTo из первого списка шагов; sitemap и llms.txt пересобраны. Один H1, canonical, description до 160 у всех. Адреса не менял.

| Статья | Запрос | Что не так | Что правлю |
|---|---|---|---|
| kak-pechatat-golosom-na-android | как печатать голосом на андроид | запроса нет в первом абзаце; «вставляется через буфер в части программ» неточно; нет честного сравнения с клавиатурами | lead с запросом; по коду: в поле с текстом вставка через буфер; ссылка на сравнение |
| golosovoy-vvod-bez-interneta | голосовой ввод без интернета андроид | H1 без запроса; «обновлять не нужно» без основания; нет сравнения | H1, desc, lead; убрал «обновлять»; раздел «Чем ещё можно диктовать без интернета»: Google, Яндекс, Говорун, SweetWhisper, минусы Писаря |
| pravila-teksta-i-chistka-rechi | голосовой ввод знаки препинания | каннибализация с bez-slov-parazitov (обе про «ну, короче»); «чистка только для русского» устарело (с 15.11 10 языков) | развёл: эта про знаки и цифры, чистка коротко со ссылкой; 10 языков |
| knopka-diktovki-nastroyka | кнопка диктовки настройка (справка) | title 73 знака | seo короче |
| istoriya-diktovok | история диктовок (справка) | title 63 | seo короче |
| slovar-i-bystrye-frazy | голосовой ввод путает имена | title 70, запроса нет; нет пути «Учиться на правках» | seo, lead; путь «Настройки → Словарь» |
| chto-vhodit-v-pisar-pro | писарь pro что платно | «зачёркнуто 499 ₽: это цена на старте» наоборот (на старте 399); нет условий пробного срока | цена; «срок идёт с первой Pro-функции, нужен интернет» |
| golosovoe-soobshchenie-v-tekst | голосовое сообщение в текст | «не слушать, а прочитать»; запроса нет в lead | lead |
| rasshifrovka-po-ssylke | расшифровка аудио по ссылке / с Яндекс Диска | title 74 | seo, lead |
| tekst-so-skrinshota | скопировать текст со скриншота андроид | запроса нет в lead | lead |
| bufer-obmena | история буфера обмена андроид | title без запроса | seo, lead |
| perevod-pri-diktovke | голосовой ввод с переводом на английский | title 78; нет данных о качестве | seo, lead; раздел «Насколько хорошо переводит» по замеру (30 фраз ru→en: 9/16/5) |
| hranenie-zapisey | сколько хранятся записи (справка) | title 62 | seo |
| golosovoe-na-soveshchanii | прочитать голосовое не включая звук | title ситуативный | seo, lead |
| otvet-v-telegram-na-parkovke | надиктовать сообщение в Telegram | title без запроса | seo, lead |
| nomer-zakaza-so-skrinshota | скопировать текст, который не выделяется | близко к tekst-so-skrinshota | развёл по запросу; кандидат на слияние (решение владельца) |
| golosovoy-vvod-dlya-pozhilyh | голосовой ввод для пожилых | «за 10 минут» без замера | убрал из H1, seo, lead |
| bez-slov-parazitov | убрать слова-паразиты голосовой ввод | каннибализация с pravila; «только русский» устарело | главная по паразитам: seo, desc, lead; 10 языков; ссылка на правила |
| pismo-inostrancu | письмо на английском не зная языка | близко к perevod-pri-diktovke | развёл по запросу; ссылка на оценку качества |
| lekciya-v-konspekt | расшифровка лекции в текст | title без запроса | seo, lead |
| xiaomi-propala-knopka | xiaomi пропала кнопка | title 60 | seo короче |
| odnoy-rukoy-s-kolyaskoy | писать одной рукой | title без запроса | seo, lead |
| spisok-pokupok-golosom | список покупок голосом | title без запроса | seo, lead |
| otchet-klientu-s-obekta | надиктовать сообщение в WhatsApp | title без запроса | seo, lead |
| otvety-pokupatelyam | отвечать на отзывы покупателей | title без запроса | seo, lead |
| itogi-vstrechi | надиктовать заметку голосом | хранение (Pro) не помечено | seo, lead; «(Pro)» у продления хранения |
| slayd-v-tekst | текст с фото слайда | «Уже не надо» рекламно | seo, lead |
| bumazhnyy-dokument-v-tekst | распознать текст с фото документа | title без запроса | seo, lead |
| poisk-po-golosovym | найти слово в голосовых | title без запроса | seo, lead |
| dlinnyy-post-golosom | надиктовать пост ВК голосом | title без запроса | seo, lead |

Слова «лучший», «единственный», «уникальный» и длинного тире нет (тире проверяет `tools/blog.py`). Концовки «Плюсы и минусы» и «Что ещё поможет» одинаковые по структуре, тексты в них разные.

Открыто:
- Слить `nomer-zakaza-so-skrinshota` в `tekst-so-skrinshota`? Пока разведены по запросу.
- Сравнение с Яндекс Клавиатурой («голосовой ввод через интернет») и Google («русский офлайн на многих телефонах») не проверено на телефоне.
- `strings_help.xml` в приложении: «Чистка речи… пока только для русской речи» устарело после `cebdc4a`.
- `tools/geo.py` (llms.txt): «часовая запись расшифровывается несколько минут» без замера.
- `tools/footer.py` и `blog.py` при сборке переносят подвал и CSS главной (после 6e2dad3) на get, mac, privacy, terms, pro: в этой ветке откатил, это работа чата шапки.
