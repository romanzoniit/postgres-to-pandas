import pandas as pd
import psycopg2
from psycopg2 import Error
import os
import logging
from dotenv import load_dotenv
import time
load_dotenv()

FORMAT = '%(asctime)s: %(levelname)s: %(name)s %(module)s: %(message)s'
filename_log = str(os.getenv('LOGS_PATH') + os.getenv('LOGS'))


def get_logger(name, level=logging.INFO) -> logging.Logger:
    logging.basicConfig(format=FORMAT,
                        level=level,
                        filename=filename_log,
                        encoding='utf-8')
    logger = logging.getLogger(name)
    return logger


logger = get_logger(__name__)


def select_query():
    query = """
            select t.filename, 
            max(t.duration) as duration,
            max(t.count_words) as count_words,
            max(t.time_recognition) as time_recognition
            from ui.tstats_recognition t
            where t.id > 167 and count_words > 0 
            group by t.filename 
            order by duration
            """
    return query


def db_connection():
    connection = None
    try:
        # Подключиться к существующей базе данных
        connection = psycopg2.connect(user=os.getenv('DATABASE_USER'),
                                      # пароль, который указали при установке PostgreSQL
                                      password=os.getenv('DATABASE_PASSWORD'),
                                      host=os.getenv('DATABASE_HOST'),
                                      port=os.getenv('DATABASE_PORT'),
                                      database=os.getenv('DATABASE_NAME')
                                      )
        logger.info("Connection to PostgreSQL DB successful")
    except (Exception, Error) as e:
        logger.error(f"The error '{e}' occurred")
    return connection


def db_close(connection):
    if connection:
        connection.close()
        logger.info("Connection to PostgreSQL closed")


def get_data_from_sql_to_pd(connection, column_names):
    df = None
    try:
        with connection:
            try:
                with connection.cursor() as cursor:
                    start = time.time()
                    cursor.execute(select_query())
                    end = time.time()
                    logger.info(f"Execute time: {round(end - start, 3)}")
                    logger.info(f"Select query successfully")
                    tuples = cursor.fetchall()
                    df = pd.DataFrame(tuples, columns=column_names)
            except (Exception, Error) as e:
                logger.error(f"The error '{e}' occurred")
    finally:
        db_close(connection)
    return df
