# Сайт pisar-app.ru

Статический сайт Писаря, GitHub Pages из ветки `main`. Страницы лежат готовым HTML, часть собирается скриптами из `tools/`.

## Сборка

Из корня сайта:

```bash
python3 tools/build.py
```

По порядку запускает `blog.py` (статьи, `assets/blog.css`, `sitemap.xml`, RSS), `geo.py` (разметка schema.org, `/get/`, `/mac/`, `llms.txt`), `intl.py` (страницы на 9 других языках), `footer.py` (подвал), `nav.py` (шапка, языки), `toc.py` (оглавление сбоку у политики, соглашения и оферты). Повторный запуск ничего не меняет. Обложки статей отдельно: `python3 ru/blog/_src/covers.py .`.

## Где что

| Что | Где |
|---|---|
| Языки, строки шапки, подвала и подсказки | `tools/i18n.py` (`LANGS`, `HEAD`, `FOOT`) |
| Разметка шапки, `hreflang`, подключение `site.css` и `site.js` | `tools/nav.py` |
| Разметка подвала | `tools/footer.py` |
| Стили шапки (вкладки Android и Mac), подвала, списка языков, значков магазинов | `assets/site.css` |
| Список языков, меню ☰, подсказка о языке | `assets/site.js` |
| База стилей статей и документов | `tools/base.css` (из неё и стилей статей в `blog.py` собирается `assets/blog.css`) |
| Документы | `assets/legal.css` |
| Pro в стиле главной (первый экран `.hero` с телефоном, ниже разделы), успех и ошибка оплаты | разметка `tools/pages.py` (`pro_body`; русская Pro правится прямо в `ru/pro/index.html`, другие языки собирает `intl.py`), стили `assets/pages.css` |
| Экраны Писаря в телефоне (Pro и блоки Pro на главной) | `assets/shots/app/<код>/*.webp`, вырезаны из скриншотов магазинов `pisar-android/docs` скриптом `tools/shots.py` (в сборку не входит, запускать при новых скриншотах) |
| Блоки Pro на главной: на ПК (от 1024 px) телефон справа закреплён, экран меняется под блок у середины окна | стили и скрипт внутри `index.html` (`.scrolly`, `.sphone`); без скрипта и на телефоне блоки как раньше, со своими картинками |
| «Скачать» и Mac в стиле главной (первый экран `.hero`, функции Mac сеткой `.fgrid`), значки магазинов на них и на главной | разметка `tools/pages.py`, стили `assets/pages.css` |
| Главная | свои стили внутри `index.html` |
| Тексты других языков | `tools/lang/<код>.py` (главная, Pro, Скачать, Mac), `tools/lang/<код>.privacy.html` и `.terms.html`; собирает `tools/intl.py` |

Стили главной на другие страницы больше не копируются: правка `<style>` в `index.html` меняет только главную. Общее для всех страниц править в `assets/site.css`, для статей и документов в `tools/base.css`.

## Шапка

Рядом с логотипом вкладки «Android | Mac». Страницы Android: меню Возможности, Pro, Статьи, Вопросы и кнопка «Скачать». Страница Mac: своё меню (Возможности, Сообщить о выходе: якоря `#features` и `#notify` на ней же) и кнопка «Сообщить о выходе». На телефоне (до 600 px) кнопка уходит первым пунктом в ☰. Подвал у всех страниц один: ссылки Android и «Для Mac (скоро)».

## Значки магазинов

Ставит `tools/pages.py` (`badges`): на главной в метки `<!-- stores -->` (первый экран и блок внизу), на «Скачать». Русский: RuStore со ссылкой, ниже «Скоро» и три магазина. Другие языки: «Скоро» Google Play, Xiaomi, Huawei, ниже RuStore с подписью «Россия». Значки не перекрашивать, не растягивать, не обрезать по краю рисунка.

| Магазин | Файл | Откуда | Условия |
|---|---|---|---|
| RuStore | `assets/rustore-color-dark.svg`, `-light.svg` | в репозитории с 13.11 (коммит cb6222b), официальный значок RuStore | официальный значок, на светлом фоне тёмный, на тёмном светлый |
| Google Play | `assets/badges/google-play-<код>.png`, 10 языков | `https://play.google.com/intl/en_us/badges/static/images/badges/<код>_badge_web_generic.png` (16.11.2026), обрезаны только прозрачные поля | правила Google Play Partner Marketing Hub («Lockups, icons, & badges»): значок не меняем и не перекрашиваем, высота не меньше 28 px, рядом со значками других магазинов Google Play не меньше их (поэтому все значки одной высоты), язык значка как язык страницы, вокруг свободное место в четверть высоты. Значок предназначен для продвижения приложения в Google Play: до публикации он стоит без ссылки, с подписью «Скоро». После публикации добавить ссылку на карточку |
| Xiaomi GetApps | `assets/badges/xiaomi-getapps.svg` | официальный архив значков Xiaomi: сайт GetApps отдаёт его по `https://global.app.mi.com/intl/web/api/index/badge` → `https://fgb0.market.xiaomi.com/download/AppStore/0e467c9c5422945f0ab2ce31710b1d2609422a77b/badge.zip` (16.11.2026; внутри `GetApps_Dark` и `GetApps_Light`, SVG и PNG). Взят `GetApps_Dark.svg` без изменений | правил использования Xiaomi не публикует; значок не меняем. Надпись на значке «GET IT ON Mi App Mall» (так Xiaomi называет магазин в значке, логотип тот же, что у GetApps), есть только на английском |
| Huawei AppGallery | `assets/badges/huawei-appgallery.png` | официальный значок «Download on AppGallery» с сайта Huawei Mobile Services: `https://huaweimobileservices.com/wp-content/uploads/2019/12/AppGallery_DownlaodBadge_ENG.png` (сайт больше не открывается, файл взят из Wayback Machine, снимок 09.08.2021), обрезаны только прозрачные поля | публичных правил Huawei нет; значок не меняем. Есть только на английском. Свежий значок на всех языках (PNG, SVG, AI) выдаёт AppGallery Connect после публикации (Distribute, AppGallery Download, Badge links): тогда заменить файл |

Когда приложение выйдет в магазине: ссылку добавить и значок при надобности поменять в `tools/pages.py` (`_soon`, `badges`), тексты «скоро» в `tools/geo.py`, `tools/lang/*.py`.

## Адреса

Русский: главная `/`, `/get/`, `/mac/`, остальное под `/ru/` (`/ru/pro/`, `/ru/privacy/`, `/ru/blog/…`).
Другие языки: `/en/`, `/de/`, `/fr/`, `/es/`, `/it/`, `/pt/`, `/pl/`, `/nl/`, `/bg/` с той же структурой: `/en/` главная, `/en/get/`, `/en/mac/`, `/en/pro/`, `/en/privacy/`, `/en/terms/`, `/en/blog/…`.

Одна и та же страница на разных языках имеет один путь после кода языка. По нему скрипты находят версии.

## Как работают языки

- Переключатель в шапке и список в подвале строятся по файлам на диске. Есть `/de/pro/index.html`: пункт Deutsch на странице Pro ведёт туда.
- Нет немецкой версии, но есть английская: пункт ведёт на английскую (в списке помечен EN).
- Нет и английской, но есть русская (блог, оферта): пункт ведёт на русскую (помечен RU). Нет никакой: язык серый.
- `hreflang` и `x-default` (английская, если есть, иначе первая из имеющихся) ставятся только на существующие версии и только если версий две и больше.
- Ссылки меню ведут на версию своего языка, если её нет, на английскую, иначе на русскую. «Возможности» и «Вопросы» на главной это якоря `#all`, `#faq`, с других страниц `/#all`, `/#faq` (или `/en/#all` и т. д.).
- Язык браузера сам ничего не переключает. Если он не совпадает с языком страницы и версия на нём есть, сверху тонкая строка «This page is available in English» на языке браузера, с крестиком. Закрытие запоминается в `localStorage` (`pisar-lang-hint`).

## Как добавить язык

1. В `tools/i18n.py` заполнить `HEAD['xx']` (все ключи как у `ru`/`en`) и `FOOT['xx']`. Ключ `offer` только у русского: оферта есть только на русском.
2. Положить страницы в `/xx/…` с той же структурой, что у английских: `<html lang="xx">`, внутри пустые `<header></header>` и `<footer></footer>` (или скопированные с другой страницы, скрипты их заменят).
3. `python3 tools/build.py`. Шапка, подвал, переключатель, `hreflang` обновятся на всех страницах сами.
4. Добавить новые адреса в `sitemap.xml` (список в конце `tools/blog.py`).

Новый язык в список (`LANGS`) добавлять не нужно, там уже все 10. Строки, которых нет в `HEAD['xx']`, берутся из английского.

## Другие языки

Главная, Pro, `/get/`, `/mac/`, политика и соглашение на en de fr es it pt pl nl bg собираются `tools/intl.py`. Главная берётся из русской `index.html`: каждый русский кусок из `HOME_SRC` заменяется переводом по ключу из `tools/lang/<код>.py`. Поменяли текст русской главной: сборка упадёт на изменённом куске, его надо перевести во всех 9 файлах. Без цены и рублей (Pro покупается в приложении), RuStore не главная кнопка; сборка падает, если на странице другого языка есть «₽», «СБП», длинное тире или русский текст. Правовые страницы: перевод для удобства, сверху ссылка на русскую версию, она и действует. Блог и оферта только на русском.

## Тексты

Без длинного тире, без «лучший», «единственный», «уникальный». Цифры только замеренные.

### Свои кнопки магазинов (16.11)

По решению владельца вместо официальных значков стоят свои кнопки одного вида: чёрная плитка, логотип магазина (вырезан из официального значка, `assets/badges/icons/`), две строки одним шрифтом. Код: `tools/pages.py` (`_btn`, `GET_ON`, `SOON_ON`), стили: `assets/site.css` (`.sbtn`). Правила Google Play требуют официальный значок без изменений: когда Писарь выйдет в Google Play, кнопку Google Play стоит заменить на официальный значок.

## Вычитка переводов 16.11 (чат 39)

Вычитаны тексты главной, Pro, «Скачать», Mac, шапки и подвала на 9 языках, пункт 11.4 соглашения на всех языках, типографика политики и соглашения. Обращение проверено: de Sie, fr vous, bg вие, es it pt pl nl на «ты» (как в карточках магазинов). Термины сверены с `pisar-android/docs/stores-listing-i18n.md`. Длинного тире нет нигде. В таблице только значимые правки; мелкие (порядок слов, «für immer», «Bitte versuchen Sie es…», прямой апостроф в I’ll) не перечислены.

| язык | было | стало | почему |
| --- | --- | --- | --- |
| en | The last text once more, with one button. | Paste your last text again with one tap. | неполное предложение |
| en | it goes in as Spanish | it’s typed in Spanish | калька |
| en | Transcription and Clips stop, the texts… | …stop working, but the texts… | склейка двух предложений запятой |
| en | the trial starts with the first Pro feature you use, and only once | starts the first time you use a Pro feature and is available only once | неясно |
| en | Pisar offers to leave your email so you hear… | Pisar lets you leave your email so we can tell you… | калька |
| en | "Share", "Agreement" | “Share”, “Agreement” | в политике и соглашении стояли прямые кавычки (108 пар) |
| de | Das Wasser kocht gleich, bis gleich | Super, ich setze gleich Wasser auf. Bis dann! | повтор «gleich» |
| de | Der Text ist gleich sauber | Sofort sauberer Text | неестественно для заголовка |
| de | Sprache laden | Sprachpaket laden | «Sprache» читается как «речь» |
| de | Wo herunterladen | Zum Download | обрывок фразы на кнопке |
| de | Probieren Sie es auf Ihrem Handy | …auf Ihrem Handy aus | нет отделяемой приставки |
| de | Transkription und Ablage halten an | …sind dann gesperrt, fertige Texte bleiben Ihnen erhalten | калька «останавливаются» |
| de | Wo sind die Grenzen? | Gibt es Einschränkungen? | калька |
| de | Der Test beginnt mit der ersten Pro-Funktion | Der Testzeitraum beginnt, sobald Sie zum ersten Mal eine Pro-Funktion nutzen | неясно |
| de | Bitte in einer Stunde erneut. | Bitte versuchen Sie es in einer Stunde erneut. | обрывок фразы |
| de | 11.4: schränkt nichts in dieser Vereinbarung … ein | schränkt diese Vereinbarung … nicht ein | естественнее для юридического немецкого |
| fr | Marche sans Internet | Fonctionne sans Internet | разговорно для заголовка |
| fr | Ça s’écrit | Pisar écrit | неестественно |
| fr | Coller encore / Le dernier texte à nouveau | Coller à nouveau / Recollez le dernier texte d’une seule touche | калька, неполное предложение |
| fr | Tout le gratuit | Tout ce qui est gratuit | так не говорят |
| fr | …s’arrêtent, les textes déjà prêts restent chez vous | …ne sont plus disponibles, mais les textes déjà transcrits restent chez vous | калька |
| fr | Pourquoi l’« Accessibilité » ? | Pourquoi Pisar a-t-il besoin de l’Accessibilité ? | обрывок вопроса |
| fr | l’e-mail qui a reçu le reçu | l’adresse e-mail où le reçu a été envoyé | тавтология и ошибка смысла |
| fr | `Tu viens samedi ?` (обычный пробел) | неразрывный узкий пробел перед ? ! ; и неразрывный перед : и внутри « » | по правилам французской типографики, перенос не отрывает знак (fr.py, политика, соглашение) |
| es | Más bajo mientras hablas / La música y los vídeos bajan el volumen | Baja el volumen mientras hablas / …suenan más bajo | музыка сама не «убавляет громкость» |
| es | …se detienen, los textos… | …dejan de estar disponibles, pero los textos… | калька |
| es | La que vale es la versión rusa | Prevalece la versión rusa | разговорно для юридической оговорки |
| it | Nomi scritti giusti | Nomi scritti correttamente | разговорно, грамматически небрежно |
| it | Tutto il gratuito | Tutto quello che è gratis | так не говорят |
| it | …si fermano, i testi già pronti restano a te | …non sono più disponibili, ma i testi già trascritti restano tuoi | калька |
| it | …e come pagare prima del pagamento | …e il metodo di pagamento prima che tu paghi | тавтология |
| pt | …param, os textos prontos ficam com você | …deixam de funcionar, mas os textos já transcritos continuam com você | калька |
| pt | Para que serve a “Acessibilidade”? | Por que o Pisar precisa da Acessibilidade? | вопрос звучал как «зачем вообще нужна» |
| pt | o Pisar oferece deixar seu e-mail para avisar | o Pisar sugere que você deixe seu e-mail para ser avisado | грамматика |
| pt | Vale a versão em russo | Prevalece a versão em russo | разговорно для юридической оговорки |
| pt | 11.4: onde se aplicam | onde se apliquem | нужен сослагательный |
| pl | Imiona zapisane poprawnie | Nazwy zapisane poprawnie | «imiona» только имена людей, а речь о названиях и терминах |
| pl | Wszystko, co skopiowałeś | Wszystko, co skopiujesz | мужской род, обращение без рода |
| pl | …się zatrzymują, gotowe teksty… | …przestają działać, ale gotowe teksty… | калька |
| pl | Godzinne nagranie przepisuje się kilka minut. | Transkrypcja godzinnego nagrania trwa kilka minut. | грамматическая ошибка |
| pl | paragon | potwierdzenie zakupu | «paragon» это бумажный чек из кассы |
| pl | 11.4: Wielkiej Brytanii lub innym kraju | Zjednoczonym Królestwie lub innym państwie | юридическое название |
| nl | “eh” … ‘Muziek en video’ | везде ‘…’ | на главной были одни кавычки, на Pro другие |
| nl | het komt erin in het Engels | het verschijnt in het Engels | неуклюже |
| nl | …stoppen, de teksten… | …werken dan niet meer, maar de teksten… | калька |
| nl | De app toont de prijs en hoe je betaalt voordat je betaalt. | Voordat je betaalt, toont de app de prijs en de betaalmethode. | тавтология |
| nl | „…” в политике и соглашении, “…” на главной | везде ‘…’ | одни кавычки по всему языку; „…” в нидерландском устарели |
| nl | 11.4: de rechten die dat recht hem geeft | de rechten die hij aan dat recht ontleent | юридический оборот |
| bg | Да говориш е по-бързо… | Говоренето е по-бързо от писането | обращение на «ты» при «вы» по всему сайту |
| bg | Поправите дума веднъж… | Поправете дума веднъж… | грамматическая ошибка |
| bg | Гласови, видео… в текст | Гласови съобщения, видео… | прилагательное без существительного |
| bg | Всичко безплатно / Текст от екранни снимки и снимки | Всичко от безплатната версия / …и фотографии | двусмысленно, повтор |
| bg | касовата бележка | разписката | «касова бележка» это бумажный чек |
| bg | 11.4: Ако Потребителят е потребител | Ако Потребителят има качеството на потребител | тавтология |

### Вторая часть (чат 39b)

Целиком вычитаны политика конфиденциальности на 9 языках и соглашение на en fr es it pt pl nl (de и bg прочитаны в первой части). Смысл не менялся, кроме одного места: в политике на 8 языках не было пункта о моделях PaddleOCR, теперь он есть, как в русской. Неиспользуемый ключ `cta` («Где скачать») удалён из `tools/lang/*.py`: в сборке он нигде не подставлялся.

| язык | было | стало | почему |
| --- | --- | --- | --- |
| en | 11.2: a claim must be sent… | A pre-trial claim procedure is mandatory… | потеряно «обязателен претензионный порядок» |
| en | Settings → Text from images | “Settings → Text from pictures” | в приложении пункт называется Text from pictures |
| fr | Store d’applications | Boutique d’applications | англицизм в юридическом тексте |
| fr | store | boutique d’applications | англицизм |
| fr | Cela ne se fait que sur votre appui. | Cela n’a lieu que lorsque vous appuyez sur le bouton. | калька |
| es | no está de acuerdo con el Acuerdo | no acepta el Acuerdo | тавтология |
| es | Si activas tú mismo | Si activas | мужской род в обращении |
| it | far cessare l’Accordo | recedere dall’Accordo | юридический оборот |
| it | quali dati ti riguardano vengono trattati | quali dati che ti riguardano… | грамматическая ошибка |
| pt | Antes de ir à justiça | Antes de recorrer à Justiça | разговорно для юридического текста |
| pt | se você mesmo… | se você… | мужской род в обращении (4 места) |
| pl | rozwiązać licencję | wypowiedzieć licencję | юридический термин |
| pl | sam zostawiłeś, podałeś, włączyłeś, połączyłeś… | безличные формы | мужской род в обращении (9 мест) |
| nl | beperkingen … beperken niet | doen geen afbreuk aan | тавтология |
| nl | de bon | het betaalbewijs | «bon» это кассовый чек в магазине |
| de fr es it pt pl nl bg | в политике нет пункта о моделях PaddleOCR для фото документов | пункт добавлен (раздел 2.1), как в русской и английской | пропуск при переводе, политика расходилась с русской |
| en | App's, Don't (прямой апостроф) | App’s, Don’t | типографика, как в 11.4 |
| nl | кнопка RuStore «Download via» | «Ontdek het op» | как на значке Google Play и в паре с «Binnenkort op» |
