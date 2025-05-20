import logging
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from .cathegory import Cathegory, Order, OrderProduct, Product
from .user import Admin
from .base import Base

__all__ = [
    "Cathegory",
    "Order",
    "OrderProduct",
    "Product",
    "Admin",
]

from config import DATABASE_URL

logger = logging.getLogger(__name__)


def create_metadata():
    logger.debug("create_metadata")

    if not database_exists(DATABASE_URL.replace("+asyncpg", "")):
        create_database(DATABASE_URL.replace("+asyncpg", ""))
    sync_engine = create_engine(DATABASE_URL.replace("+asyncpg", ""))
    Base.metadata.create_all(bind=sync_engine)
