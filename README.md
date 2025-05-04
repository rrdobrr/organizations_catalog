

# OrganizationCatalog
## Асинхронное REST API приложение

### Запуск проекта через Docker
    - git clone https://github.com/yourname/organization_catalog.git
    - cd organization_catalog
    - docker-compose up --build


### Особенности:
    - автомиграции при запуске контейнера;
    - автозаполнение БД тестовыми данными после запуска контейнера;
    - Вложенность видов деятельности ограничена 3-мя уровнями;
        (можно регулировать в app/src/constants/activity_type)

### Функционал:
    - Фильтрация
        - по форме организации (ООО, ЗАО и т.д.);
        - по названию;
        - по виду деятельности;
        - по вложенным видам деятельности;
        - организаций и зданий в заданном радиусе от любой геоточки;

### Проверка фукнционала:
    - Эндпоинты: http://localhost:8000/docs#/
    - API_KEY: invite_me_to_work

### Примеры координат проверки метода geo-radius:
  - "latitude": 55.7575, "longitude": 37.6590
  - "latitude": 55.7340, "longitude": 37.4700 
  - "latitude": 55.6450, "longitude": 37.5455


### Стек:
  - Python 3.12-slim
  - FastAPI
  - PostgreSQL (через asyncpg)
  - SQLAlchemy (Async)
  - geoalchemy2
  - alembic
  - Poetry
  - Docker / Docker Compose


