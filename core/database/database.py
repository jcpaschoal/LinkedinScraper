from loguru import logger
import typing as t
import pymysql
import sys


def create_database_connection(db: str, user: str, password: str, host: str):
    if db:
        try:
            logger.info("[+] Inserting into Database: " + str(db))
            conn = pymysql.connect(
                user=user,
                password=password,
                host=host,
                db=db,
                cursorclass=pymysql.cursos.DictCursor,
            )

            if isinstance(conn, str):
                logger.error("Unable to connect to database : ", conn)
                sys.exit(1)
            return conn

        except Exception as err:
            logger.exception(err)


def get_accounts(db_conn: pymysql.Connection):
    pass
