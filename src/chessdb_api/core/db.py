"""This module sets up Gino to talk with our PostgreSQL database

"""
from chessdb_api.core import config_loader
from gino.ext import starlette  # pylint: disable=no-name-in-module
from sqlalchemy.dialects import postgresql

DB = starlette.Gino(
    dsn=config_loader.DB_DSN,
    pool_min_size=config_loader.DB_POOL_MIN_SIZE,
    pool_max_size=config_loader.DB_POOL_MAX_SIZE,
    echo=config_loader.DB_ECHO,
    ssl=config_loader.DB_SSL,
    use_connection_for_request=config_loader.DB_USE_CONNECTION_FOR_REQUEST,
    retry_limit=config_loader.DB_RETRY_LIMIT,
    retry_interval=config_loader.DB_RETRY_INTERVAL,
)

DB.UUID = (postgresql.UUID)
