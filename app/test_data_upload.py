import httpx
import asyncio
from src.core.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession

#
BUILDINGS_API_URL = "http://localhost:8000/api/v1/buildings/"
ACTIVITY_TYPES_API_URL = "http://localhost:8000/api/v1/activity-types/"
ORGANIZATIONS_API_URL = "http://localhost:8000/api/v1/organizations/"
PHONE_NUMBERS_API_URL = "http://localhost:8000/api/v1/organizations/phone_numbers"



API_KEY = "invite_me_to_work"

activity_types = [
  { "name": "Производство", "parent_name": "" },
  { "name": "Производство пищевых продуктов", "parent_name": "Производство" },
  { "name": "Производство молочной продукции", "parent_name": "Производство пищевых продуктов" },
  { "name": "Производство строительных материалов", "parent_name": "Производство" },
  { "name": "Производство металлоконструкций", "parent_name": "Производство строительных материалов" },

  { "name": "Оптовая и розничная торговля", "parent_name": "" },
  { "name": "Оптовая торговля", "parent_name": "Оптовая и розничная торговля" },
  { "name": "Оптовая торговля продуктами питания", "parent_name": "Оптовая торговля" },
  { "name": "Розничная торговля", "parent_name": "Оптовая и розничная торговля" },
  { "name": "Розничная торговля одеждой", "parent_name": "Розничная торговля" },

  { "name": "Строительство", "parent_name": "" },
  { "name": "Строительство жилых зданий", "parent_name": "Строительство" },
  { "name": "Строительство многоэтажных домов", "parent_name": "Строительство жилых зданий" },
  { "name": "Строительство инженерных сооружений", "parent_name": "Строительство" },
  { "name": "Прокладка водопроводных систем", "parent_name": "Строительство инженерных сооружений" },

  { "name": "Транспорт и логистика", "parent_name": "" },
  { "name": "Грузовые перевозки", "parent_name": "Транспорт и логистика" },
  { "name": "Междугородние перевозки", "parent_name": "Грузовые перевозки" },
  { "name": "Складская логистика", "parent_name": "Транспорт и логистика" },
  { "name": "Хранение скоропортящихся товаров", "parent_name": "Складская логистика" },

  { "name": "Информационные технологии", "parent_name": "" },
  { "name": "Разработка программного обеспечения", "parent_name": "Информационные технологии" },
  { "name": "Разработка корпоративных систем", "parent_name": "Разработка программного обеспечения" },
  { "name": "Хостинг и облачные сервисы", "parent_name": "Информационные технологии" },
  { "name": "Услуги дата-центров", "parent_name": "Хостинг и облачные сервисы" }
]
buildings = [
  { "address": "ул. Земляной Вал, 33", "latitude": 55.7575, "longitude": 37.6590 },
  { "address": "ул. Нижняя Сыромятническая, 10", "latitude": 55.7559, "longitude": 37.6643 },
  { "address": "ул. Машкова, 22", "latitude": 55.7604, "longitude": 37.6680 },
  { "address": "ул. Казакова, 18", "latitude": 55.7638, "longitude": 37.6667 },
  { "address": "ул. Покровка, 47", "latitude": 55.7570, "longitude": 37.6685 },

  { "address": "Ленинградский проспект, 39", "latitude": 55.7926, "longitude": 37.5590 },
  { "address": "ул. Кастанаевская, 45", "latitude": 55.7340, "longitude": 37.4700 },
  { "address": "ул. Профсоюзная, 109", "latitude": 55.6450, "longitude": 37.5455 },
  { "address": "ул. Перовская, 66", "latitude": 55.7412, "longitude": 37.8251 },
  { "address": "ул. Новоясеневский проспект, 9", "latitude": 55.6092, "longitude": 37.5418 },

  { "address": "ул. Дмитровское шоссе, 100", "latitude": 55.8790, "longitude": 37.5612 },
  { "address": "ул. Братиславская, 20", "latitude": 55.6601, "longitude": 37.7499 },
  { "address": "ул. Люблинская, 72", "latitude": 55.6772, "longitude": 37.7666 },
  { "address": "ул. Маршала Захарова, 12", "latitude": 55.6313, "longitude": 37.7355 },
  { "address": "ул. Алтуфьевское шоссе, 40", "latitude": 55.8814, "longitude": 37.5892 }
]
organization = [
  {
    "name": "ООО МолПром",
    "address": "ул. Земляной Вал, 33",
    "activity_types": [
        "Производство молочной продукции",
        "Производство пищевых продуктов"
    ]
  },
  {
    "name": "ЗАО Продукты XXI",
    "address": "ул. Нижняя Сыромятническая, 10",
    "activity_types": [
        "Оптовая торговля продуктами питания",
        "Оптовая торговля"
    ]
  },
  {
    "name": "ОАО МонолитСтрой",
    "address": "ул. Машкова, 22",
    "activity_types": [
        "Строительство многоэтажных домов",
        "Строительство жилых зданий"
    ]
  },
  {
    "name": "ГК Логистик-Склад",
    "address": "ул. Казакова, 18",
    "activity_types": [
        "Хранение скоропортящихся товаров",
        "Складская логистика"
    ]
  },
  {
    "name": "ООО АйТи Платформа",
    "address": "ул. Покровка, 47",
    "activity_types": [
        "Разработка корпоративных систем",
        "Услуги дата-центров"
    ]
  },
  {
    "name": "АО ЦентрМеталл",
    "address": "Ленинградский проспект, 39",
    "activity_types": [
        "Производство металлоконструкций"
    ]
  },
  {
    "name": "ТД СтройСнаб",
    "address": "ул. Кастанаевская, 45",
    "activity_types": [
        "Розничная торговля одеждой"
    ]
  },
  {
    "name": "ООО ЯсеневоСтрой",
    "address": "ул. Новоясеневский проспект, 9",
    "activity_types": [
        "Прокладка водопроводных систем",
        "Строительство жилых зданий"
    ]
  },
  {
    "name": "ООО Учебные технологии",
    "address": "ул. Профсоюзная, 109",
    "activity_types": [
        "Хостинг и облачные сервисы",
        "Услуги дата-центров"
    ]
  },
  {
    "name": "ЗАО ВостокГруз",
    "address": "ул. Перовская, 66",
    "activity_types": [
        "Междугородние перевозки",
        "Складская логистика"
    ]
  },
  {
    "name": "ООО МосФуд",
    "address": "ул. Дмитровское шоссе, 100",
    "activity_types": [
        "Производство пищевых продуктов",
        "Оптовая торговля продуктами питания"
    ]
  },
  {
    "name": "ТК Продукты Поволжья",
    "address": "ул. Братиславская, 20",
    "activity_types": [
        "Оптовая торговля"
    ]
  },
  {
    "name": "ООО ЦентрДом",
    "address": "ул. Люблинская, 72",
    "activity_types": [
        "Строительство жилых зданий"
    ]
  },
  {
    "name": "АО ЦентрЛогистик",
    "address": "ул. Маршала Захарова, 12",
    "activity_types": [
        "Складская логистика",
        "Хранение скоропортящихся товаров"
    ]
  },
  {
    "name": "ООО Хайтек Проект",
    "address": "ул. Алтуфьевское шоссе, 40",
    "activity_types": [
        "Услуги дата-центров",
        "Хостинг и облачные сервисы",
        "Складская логистика"
    ]
  }
]

phone_numbers = [
    # Организация 1 — 3 номера
    {"number": "8-923-111-11-11", "organization_id": 1},
    {"number": "8-923-111-22-22", "organization_id": 1},
    {"number": "8-923-111-33-33", "organization_id": 1},

    # Организация 2 — 1 номер
    {"number": "8-923-222-44-44", "organization_id": 2},

    # Организация 3 — 2 номера
    {"number": "8-923-333-55-55", "organization_id": 3},
    {"number": "8-923-333-66-66", "organization_id": 3},

    # Организация 4 — 1 номер
    {"number": "8-923-444-77-77", "organization_id": 4},

    # Организация 5 — 3 номера
    {"number": "8-923-555-88-88", "organization_id": 5},
    {"number": "8-923-555-99-99", "organization_id": 5},
    {"number": "8-923-555-00-00", "organization_id": 5},

    # Организация 6 — 1 номер
    {"number": "8-923-666-11-22", "organization_id": 6},

    # Организация 7 — 2 номера
    {"number": "8-923-777-33-44", "organization_id": 7},
    {"number": "8-923-777-55-66", "organization_id": 7},

    # Организация 8 — 1 номер
    {"number": "8-923-888-77-88", "organization_id": 8},

    # Организация 9 — 2 номера
    {"number": "8-923-999-99-11", "organization_id": 9},
    {"number": "8-923-999-88-22", "organization_id": 9},

    # Организация 10 — 1 номер
    {"number": "8-923-000-33-44", "organization_id": 10},
]


data_for_add = {ACTIVITY_TYPES_API_URL:activity_types,
                BUILDINGS_API_URL:buildings,
                ORGANIZATIONS_API_URL:organization,
                PHONE_NUMBERS_API_URL:phone_numbers
                }




headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}



async def if_table_empty_add_data(session: AsyncSession):
    from app.src.models.organization import Organization
    result = await session.execute(select(Organization))
    count = len(result.scalars().all())
    if count == 0:
        await populate()

async def run_check_and_add_data():
    async for session in get_session():
        await if_table_empty_add_data(session)


async def populate():
    async with httpx.AsyncClient() as client:
        for url, data in data_for_add.items():
            for item in data:
                print(f'Попытка добавить {item}')
                response = await client.post(url, json=item, headers=headers)
                if response.status_code == 201 or response.status_code == 200:
                    print(f"[+] Добавлено: {response}")
                else:
                    print(f"[!] Ошибка ({response.status_code}): {response.text}")



if __name__ == "__main__":
    asyncio.run(populate())