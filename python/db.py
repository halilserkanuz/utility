# -*- coding: utf-8 -*-
import  pymysql
import os
from . import filesystem
import os.path
import psycopg2
import psycopg2.extras
import json

class DbOps(object):

    fs = filesystem.FileSystemOps()
    def __init__(self, db="default_db"):
        self.config = self.fs.read_json_from_file(os.path.dirname(__file__) + '/../config.json')
        self.db_settings = self.config[db]
    
    def create_connection(self):
        db_settings = self.db_settings
        if db_settings["db_type"]=="mysql":
            return pymysql.connect(
                host=db_settings["host"], 
                user=db_settings["user_name"], 
                passwd=db_settings["password"], 
                db=db_settings["db_name"],
                port=db_settings["port"], 
                autocommit=True, 
                charset='utf8mb4',
                connect_timeout=315360)
        elif db_settings["db_type"]=="postgresql":
            con = psycopg2.connect(
                host=db_settings["host"],
                database=db_settings["db_name"],
                user=db_settings["user_name"],
                password=db_settings["password"])
            con.autocommit = True
            return con
            print("Connected to mysql server")

    def execute_sp(self, spname, parameter, parameterCount):
        print("SP Name: ",spname)
        cnx = self.create_connection()
        cur = cnx.cursor()
        select_statement = "call "+spname+" ("
        for i in range(parameterCount):
            if i == parameterCount-1:
                select_statement = select_statement + "'{0}')".format(parameter[i])
            else:
                select_statement = select_statement +"'{0}',".format(parameter[i])
        
        cur.execute(select_statement)
        cnx.commit()
        cur.close()
        cnx.close()
        

    def execute_sp_return_results(self, spname, parameter, parameterCount):
        print("SP Name: ",spname)
        cnx = self.create_connection()
        cur = cnx.cursor()
        select_statement = "call "+spname+" ("
        for i in range(parameterCount):
            if i == parameterCount-1:
                select_statement = select_statement+"%s"
            else:
                select_statement = select_statement + "%s,"
        cur.execute(select_statement+")", parameter)
        rows = cur.fetchall()
        cnx.commit()
        cur.close()
        cnx.close()
        return rows

    def execute_sql(self, sql, params=None):
        cnx = self.create_connection()
        cur = cnx.cursor()
        select_statement = sql
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(select_statement)
        cnx.commit()
        cur.close()
        cnx.close()

        print("Completed ", sql)
    
    

    def execute_sql_return_results(self, sql):
        cnx = self.create_connection()
        cur = cnx.cursor()
        select_statement = sql
        cur.execute(select_statement, ())
        rows = cur.fetchall()
        
        cur.close()
        cnx.close()
        return rows


    def execute_sql_return_json(self, sql="", returns=()):
        cnx = self.create_connection()
        cur = cnx.cursor()

        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        results = {"results": []}
        for row in rows:
            i=0
            res = {}
            for ret in returns:
                res[ret]=row[i]
                i=i+1
            results.get("results").append(res)

        return results

    def query(self, query, dictCursor=True):
        cnx = self.create_connection()
        cur = cnx.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        cnx.close()
        return json.loads(json.dumps(rows))