import psycopg2
from psycopg2.extras import RealDictCursor

params = {'host': 'localhost', 'database': 'toxicity', 'user': 'rajat', 'password': 'toxicity'}


def conn_create():
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
    except(Exception, psycopg2.DatabaseError) as e:
        error = 'Error {0} occurred while creating connection'.format(e)
        print(error)
    finally:
        return conn, cur


def conn_close(conn):
    if conn is not None:
        conn.close()
