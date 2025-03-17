import os
import mysql.connector as connector
from mysql.connector import MySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_DATABASE")

class DatabaseConnection:
    def __init__(self):
        self.connection: PooledMySQLConnection | MySQLConnectionAbstract  = connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            #ssl_disabled=True,
        )
        self.cursor: Cursor = self.connection.cursor()

    def find(self, query:str,args:list=None):
        if args is None:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        else:
            self.cursor.execute(query,args)
            return self.cursor.fetchall()
    def execute(self, query:str,args:list=None):
        if args is None:
            self.cursor.execute(query)
            return self.cursor.rowcount
        else:
            self.cursor.execute(query,args)
            return self.cursor.rowcount

    def add(self,query:str,args:list):
        self.cursor.execute(query,args)
        return self.cursor.lastrowid

    def complete(self):
        self.connection.commit()
        self.connection.close()

    def undo(self):
        self.connection.close()