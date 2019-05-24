import fire
from sqlalchemy import create_engine, MetaData
from configparser import ConfigParser
from pathlib import Path
from src.twitter import fetch_tweets
from src.logging import with_logging
from src.postgres import init_db, insert_data


class TwitterFetcher(object):

    @with_logging
    def fetch(self, user: str, n: int=5) -> None:

        """
        Fetches last N tweets for the specified user and stores them in Postgres

        :param user: name of the specified user on Twitter
        :param n: number of last tweets to fetch
        """

        # Parse configuration file
        cfg = ConfigParser()
        cfg.read(f'{Path(__file__).parent}/config.ini')

        # Split config sections for readability
        db_cfg, api_cfg = cfg['postgres'], cfg['twitter']

        # Create connection string and database engine
        conn_string = f"{db_cfg['driver']}://{db_cfg['user']}:{db_cfg['pw']}" \
                      f"@{db_cfg['host']}:{db_cfg['port']}/{db_cfg['db']}"
        engine = create_engine(conn_string)

        # Initialize database and insert records fetched
        with engine.connect() as conn:
            init_db(conn)
            insert_data(conn, fetch_tweets(user, n, api_cfg))


if __name__ == '__main__':
    fire.Fire(TwitterFetcher)
