import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.database.base import Base

# Alembic's config object — gives access to values in alembic.ini
config = context.config

# Wire up Python's logging from the [loggers] section in alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Inject our DATABASE_URL so alembic.ini doesn't need to store credentials
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# This is what enables autogenerate (`alembic revision --autogenerate`).
# Alembic inspects all tables registered on Base.metadata and diffs them
# against what's in the database to produce the migration script.
target_metadata = Base.metadata


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    # NullPool disables connection pooling during migrations — each migration
    # command opens one connection, uses it, and closes it immediately.
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online():
    asyncio.run(run_async_migrations())


# Alembic calls this file and expects either run_migrations_offline()
# or run_migrations_online() to be invoked.
# We only support online mode (connected to a real DB).
run_migrations_online()
