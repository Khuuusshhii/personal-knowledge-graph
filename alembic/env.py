# alembic/env.py
# Alembic migration environment.
# This file tells Alembic how to connect to the database and
# where to find the SQLAlchemy models (so it can detect schema changes).

import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Add the backend directory to the Python path so we can import our modules.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import DATABASE_URL, Base
# Import all models so that Alembic sees them in Base.metadata.
# Without this, autogenerate would produce an empty migration.
import models  # noqa: F401

# Alembic Config object — gives access to values in alembic.ini.
config = context.config

# Set the SQLAlchemy URL from our database module (overrides alembic.ini value).
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# This is the MetaData object from our Base — Alembic uses it to
# detect which tables/columns exist in the models vs. the database.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations without an active database connection."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations with an active database connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
