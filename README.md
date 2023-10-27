
**YaMDb** - собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число). Пользователи могут оставлять комментарии к отзывам.
___
## **Что внутри**:
* Поддерживает все типовые операции CRUD
* Предоставляет данные в формате JSON
* Аутентификация по Jwt-токену
* Реализованы пермишены, фильтрации, пагинация ответов от API, установлено ограничение количества запросов к API
___
## **Пользовательские роли**:
* **Anonymous** — может просматривать описания произведений, читать отзывы и комментарии.
* **Аутентифицированный пользователь (user)** — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Роль присваивается по умолчанию каждому новому пользователю.
* **Модератор (moderator)** — облаадет правами аутентифицированного пользователя + право удалять любые отзывы и комментарии.
* **Администратор (admin)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры, а так же назначать роли пользователям.

___
## **Как запустить проект**:

### **Для Windows, локально:**

* Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/STI-xa/yamdb_final

cd yamdb_final
```

* Cоздать и активировать виртуальное окружение:
```
python -m venv venv

source venv/Scripts/activate
```

* Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip

pip install -r requirements.txt
```

* Выполнить миграции:
```
python manage.py migrate
```

* Запустить проект:
```
python manage.py runserver
```

### **Запуск из контейнера:**
* Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/STI-xa/yamdb_final

cd yamdb_final
```

* Создание и запуск контейнеров:
```
docker-compose up -d --build
```

* Выполняем миграции, создаем суперпользователя, собираем статику и создаем дамп БД:
```
docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py createsuperuser

docker-compose exec web python manage.py collectstatic --no-input

docker-compose exec web python manage.py dumpdata > fixtures.json
```

## Шаблон наполнения env-файла:
```
DB_ENGINE=django.db.backends.postgresql # указывает, с какой БД работать
DB_NAME=postgres # имя БД
POSTGRES_USER=postgres # логин для подключения к БД
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```

### **Образ доступен на** [DockerHub](https://hub.docker.com/repository/docker/stixaxa/yamdb_final/general)
___
## **Примеры запросов**:
* GET-запрос возвращает список произведений:
```
http://127.0.0.1:8000/api/v1/titles/
```
```
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```
* GET-запрос возвращает комментарии к посту:
```
* http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/
```
```
[
  {
    "id": 0,
    "author": "string",
    "text": "string",
    "created": "2019-08-24T14:15:22Z",
    "post": 0
  }
]
```
* Остальные примеры запросов можно посмотреть по [ссылке](http://127.0.0.1:8000/redoc/) после запуска проекта.
___
## **Стэк технологий**:
* ![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
* ![image](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
* ![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
* ![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
* ![image](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
* ![image](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)
* ![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
* ![image](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
