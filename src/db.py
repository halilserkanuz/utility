
import os
import psycopg2
import psycopg2.extras
from typing import Dict, Tuple


class DBHelper(object):

    def __init__(self, db_name="TRACK"):
        self.db_name = db_name

    def create_connection(self):
        cnx = psycopg2.connect(
                        host=os.getenv("PG_HOST"),
                        database=os.getenv("PG_DB_" + self.db_name),
                        user=os.getenv("PG_USER_" + self.db_name),
                        password=os.getenv("PG_PASSWORD_" + self.db_name)
                    )
        cnx.autocommit = True
        return cnx

    
    def fetch(self, query: str) -> Dict:
        cnx = self.create_connection()
        cur = cnx.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        cnx.close()
        return rows

    def execute(self, query: str, data: Tuple) -> None:
        cnx = self.create_connection()
        cur = cnx.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(query, data)
        cur.close()
        cnx.close()

    def query(self, query: str) -> None:
        cnx = self.create_connection()
        cur = cnx.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(query)
        cur.close()
        cnx.close()


    
