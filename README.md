# Куда пойти

Сайт о самых интересных местах в Москве.

![Главная страница](main_page.png)

## Требования проекта

- Python: 3.10–3.13
- Django: 5.1.x
- python-dotenv: 1.x
- Pillow: 11.3.x
- django-admin-sortable2: 2.2.x
- django-tinymce: 4.1.x

## Установка и настройка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/AlexKlos/DVMN_l22.git
   ```

2. Создайте виртуальное окружение в папке проекта:

   ```bash
   python -m venv venv
   source venv/bin/activate  # или venv\Scripts\activate на Windows
   ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Создайте ключ Django:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. Создайте и настройте файл `.env`:

   ```env
   DJANGO_SECRET_KEY=...                      # Ключ Django
   DJANGO_DEBUG=False                         # Режим разработки (False для продакшн)
   DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost   # Разрешённые хосты (через запятую, без пробелов)
   DJANGO_TIME_ZONE=Asia/Bangkok              # Часовой пояс проекта
   DJANGO_LANGUAGE_CODE=en-us                 # Язык интерфейса
   DJANGO_MEDIA_ROOT=media                    # Папка для пользовательских файлов (media)
   DJANGO_STATIC_ROOT=staticfiles             # Папка для собранных статических файлов (staticfiles)
   ```

7. Примените миграции:
   ```bash
   python manage.py migrate
   ```

8. Создайте суперпользователя Django:
   ```bash
   python manage.py createsuperuser
   ```

9. Запустите сервер разработки:
   ```bash
   python manage.py runserver
   ```

## Использование

- После запуска сайт будет доступен по адресу:
   ```
   http://127.0.0.1:8000
   ```

- Редактирование данных через панель администратора по адресу:
   ```
   http://127.0.0.1:8000/admin/
   ```
   Доступ по реквизитам суперпользователя Django (см. п.7.)

- Добавить новое место с помощью файла .json:

   В папке поекта выполните команду
   ```
   python manage.py load_place http://адрес/файла.json
   ```

   Пример файла .json:
   ```json
   {
    "title": "Антикафе Bizone",
    "imgs": [
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/1f09226ae0edf23d20708b4fcc498ffd.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/6e1c15fd7723e04e73985486c441e061.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/be067a44fb19342c562e9ffd815c4215.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/f6148bf3acf5328347f2762a1a674620.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/b896253e3b4f092cff47a02885450b5c.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/605da4a5bc8fd9a748526bef3b02120f.jpg"
    ],
    "description_short": "Настольные и компьютерные игры, виртуальная реальность и насыщенная программа мероприятий — новое антикафе Bizone предлагает два уровня удовольствий для вашего уединённого отдыха или радостных встреч с родными, друзьями, коллегами.",
    "description_long": "<p>Рядом со станцией метро «Войковская» открылось антикафе Bizone, в котором создание качественного отдыха стало делом жизни для всей команды. Создатели разделили пространство на две зоны, одна из которых доступна для всех посетителей, вторая — только для совершеннолетних гостей.</p><p>В Bizone вы платите исключительно за время посещения. В стоимость уже включены напитки, сладкие угощения, библиотека комиксов, большая коллекция популярных настольных и видеоигр. Также вы можете арендовать ВИП-зал для большой компании и погрузиться в мир виртуальной реальности с помощью специальных очков от топового производителя.</p><p>В течение недели организаторы проводят разнообразные встречи для меломанов и киноманов. Также можно присоединиться к английскому разговорному клубу или посетить образовательные лекции и мастер-классы. Летом организаторы запускают марафон настольных игр. Каждый день единомышленники собираются, чтобы порубиться в «Мафию», «Имаджинариум», Codenames, «Манчкин», Ticket to ride, «БЭНГ!» или «Колонизаторов». Точное расписание игр ищите в группе антикафе <a class=\"external-link\" href=\"https://vk.com/anticafebizone\" target=\"_blank\">«ВКонтакте»</a>.</p><p>Узнать больше об антикафе Bizone и забронировать стол вы можете <a class=\"external-link\" href=\"http://vbizone.ru/\" target=\"_blank\">на сайте</a> и <a class=\"external-link\" href=\"https://www.instagram.com/anticafe.bi.zone/\" target=\"_blank\">в Instagram</a>.</p>",
    "coordinates": {
        "lng": "37.50169",
        "lat": "55.816591"
    }
   }
   ```

## Цели проекта

Код написан в учебных целях — для курса по Python и веб-разработке на сайте [Devman](https://dvmn.org).

Тестовые данные взяты с сайта [KudaGo](https://kudago.com).
