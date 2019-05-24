from sqlalchemy.orm import Session
from sqlalchemy import schema, MetaData
from src.logging import logger
from src.tables import Base, schema_name, Tweet
from colorama import Fore, Style
from typing import Dict, Iterable
from sqlalchemy.engine.base import Connection


def init_db(conn: Connection) -> None:

    """
    Configures the target schema in which the tweets data will be stored,
    creates the schema and the table if not existing yet

    :param conn: SQLAlchemy connection object
    """

    logger.info(f"{Fore.YELLOW}Initializing database ...{Style.RESET_ALL}")

    # Create specified schema if not exists
    if not conn.dialect.has_schema(conn, schema_name):
        logger.info(f"{Fore.YELLOW}Schema {schema_name} does not exist, creating it ...{Style.RESET_ALL}")
        conn.execute(schema.CreateSchema(schema_name))
        logger.info(f"{Fore.GREEN}Schema {schema_name} successfully created !{Style.RESET_ALL}")
    else:
        logger.info(f"{Fore.GREEN}Schema {schema_name} was found, continuing database initialization "
                    f"...{Style.RESET_ALL}")

    # Create tables
    Base.metadata.create_all(bind=conn)

    logger.info(f"{Fore.GREEN}Schema {schema_name} successfully configured !{Style.RESET_ALL}")


def insert_tweets(conn: Connection, fetch_data: Iterable[Dict]) -> None:

    """
    Inserts fetched tweet data to the target database table

    :param conn: SQLAlchemy connection object
    :param fetch_data: generator containing fetched tweet data
    """

    s = Session(bind=conn)
    meta = MetaData()
    meta.reflect(bind=conn)
    s.add_all([Tweet(**t) for t in fetch_data])
    s.commit()
