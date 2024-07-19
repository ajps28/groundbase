import logging
import logging.config
import importlib.util

from alembic.config import Config
from alembic import command

from dependency_injector import containers, providers

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class MainContainer(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)

    def get_logger():
        logging.config.fileConfig("log_config.ini", disable_existing_loggers=False)
        return logging.getLogger("groundbase")  # change logger name as you will

    logger = providers.Factory(get_logger)

    db_engine = providers.Singleton(
        create_async_engine,
        config.db_connection_string,
        echo=bool(config.db_sql_logging),
    )

    db_session_factory = providers.Factory(async_sessionmaker, db_engine, expire_on_commit=False)


def check_dependencies():
    # here add dependencies as needed
    deps = ["fastapi", "dependency_injector", "sqlalchemy", "alembic", "sqlmodel", "aiosqlite"]
    for dep in deps:
        if not importlib.util.find_spec(dep):
            raise RuntimeError(f"check that {dep} is installed!")


def initialize_database():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


def initialize_dependency_injection():
    container = MainContainer()

    container.config.db_connection_string.from_env("DB_CONNECTION_STRING")
    container.config.db_sql_logging.from_env("DB_SQL_LOGGING")

    container.init_resources()

    container.wire(
        packages=[
            "groundbase",
            # here add all packages as needed
        ]
    )
