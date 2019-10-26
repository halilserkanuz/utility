# -*- coding: utf-8 -*-
import mysql.connector as pymysql
import os
from . import filesystem
import os.path

class DbOps(object):

    fs = filesystem.FileSystemOps()
    def __init__(self, db="default_db"):
        self.config = self.fs.read_json_from_file(os.path.dirname(__file__) + '/../config.json')
        if self.config[db]["db_type"]=="mysql":
            self.db_settings = self.config[db]
            print("Running on mysql server")
    
    def create_connection(self):
        db_settings = self.db_settings
        if db_settings["db_type"]=="mysql":
            return pymysql.connect(
                host=db_settings["host"], 
                user=db_settings["user_name"], 
                passwd=db_settings["password"], 
                db=db_settings["db_name"],
                port=db_settings["port"], 
                charset='utf8',
                autocommit=True, 
                connect_timeout=315360)
            print("Connected to mysql server")

    def execute_sp(self, spname, parameter, parameterCount):
        cnx = self.create_connection()
        cur = cnx.cursor()
        cur.callproc(spname, (parameter,))
        cur.close()
        cnx.close()
        

    def execute_sp_return_results(self, spname, parameter, parameterCount):
        cnx = self.create_connection()
        cur = cnx.cursor(buffered=True)
        select_statement = "call "+spname+" ("
        for i in range(parameterCount):
            if i == parameterCount-1:
                select_statement = select_statement+"%s"
            else:
                select_statement = select_statement + "%s,"
        cur.execute(select_statement+")", parameter, multi=True)
        rows = cur.fetchall()
        cur.close()
        cnx.close()
        return rows

    def execute_sql(self, sql):
        cnx = self.create_connection()
        cur = cnx.cursor()
        select_statement = sql
        cur.execute(select_statement, ())
        cur.close()
        cnx.close()



    def execute_sql_return_results(self, sql):
        cnx = self.create_connection()
        cur = cnx.cursor()
        select_statement = sql
        cur.execute(select_statement, ())
        rows = cur.fetchall()
        cur.close()
        cnx.close()
        return rows


