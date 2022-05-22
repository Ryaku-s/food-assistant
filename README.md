# Food Assistant
## Описание
Учебный проект кулинарного сайта на Django
### Инструменты
- Python 3.8
- Django
- JavaScript
- JQuery
- PostgreSQL
- Bootstrap 5
### Функционал
- Создание / Изменение / Удаление своих рецептов любым пользователем
- Сортировка каталога рецептов, и поиск по нему
- Каждый рецепт до публикации является черновиком и не будет виден другим пользователям
- Добавление рецептов в избранное
- Система подписок между пользователями
- Настройка профиля (аватар, отображаемое имя и т. д.)
### Интересное
- Зависимые выпадающие списки
- Unit-тесты
- Оптимизированные SQL-запросы через `select_realed()`, `prefetch_related()`
- Сервисы бизнес-логики и запросы к базе данных в отдельных модулях
## Начало работы
1) Виртуальное окружение
    ```
    python -m venv venv
    ```
2) Установить зависимости
    ```
    pip install -r requirements.txt
    ```
3) В корне проекта создать файл .env и прописать свои переменные окружения, в том числе подключение к базе данных.
 Образец из .env.example:
    ```
    DEBUG=1
    SECRET_KEY=your_secret_key

    # Database
    POSTGRES_ENGINE=engine
    POSTGRES_NAME=name
    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    POSTGRES_HOST=host
    POSTGRES_PORT=port
    ```
4) Выполнить миграции
    ```
    python manage.py migrate
    ```
5) Создать суперпользователя
    ```
    python manage.py createsuperuser
    ```
6) Запустить сервер
    ```
    python manage.py runserver
    ```
