import asyncio
import os
import sys
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from app.src.core.db.base import Base
from app.src.models.activity_type import ActivityTypes
from app.src.models.building import Building
from app.src.models.organization import Organization, organization_activity_association
from geoalchemy2 import Geography


# ✅ Подключаем .env
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# ✅ Получаем строку подключения напрямую из окружения
DATABASE_URL = os.environ["DATABASE_URL"]
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Добавляем путь к проекту
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app", "src"))
)

# Метадата моделей
target_metadata = Base.metadata
print("🧠 Alembic sees tables:", Base.metadata.tables.keys())


def run_migrations_offline():
    """Запуск миграций в offline-режиме (без подключения к БД)"""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = create_async_engine(DATABASE_URL, poolclass=None)

    async with connectable.begin() as connection:
        await connection.run_sync(
            lambda sync_connection: context.configure(
                connection=sync_connection,
                target_metadata=target_metadata,
                compare_type=True,
            )
        )

        await connection.run_sync(lambda _: context.run_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
