import sqlite3
from database.queries import CREATE_TABLES
import traceback


class MAKE_CONNECTION:

    def __init__(self , connection):
        self.connection = connection

    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc, tb):  
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()

        self.cursor.close()
        return None

class Database:
        
    def __init__(self):
        self.connection = sqlite3.connect("data.db")
        self.connection.execute("PRAGMA foreign_keys = ON")

    def Initialize(self):
        with MAKE_CONNECTION(self.connection) as cursor:
            cursor.executescript(CREATE_TABLES)

    def fetch_item(self , query , *args):
        try:
            with MAKE_CONNECTION(self.connection) as cursor:
                cursor.execute(query , args)
                return cursor.fetchone()
        except sqlite3.Error:
            return None

    def fetch_all_items(self , query , *args):
        try:
            with MAKE_CONNECTION(self.connection) as cursor:
                cursor.execute(query , args)
                return cursor.fetchall()
        except sqlite3.Error:
            return None
    
    def add_item(self , query , *args):
        try:
            with MAKE_CONNECTION(self.connection) as cursor:
                cursor.execute(query , args)
                return True
        except sqlite3.Error:
            #traceback.print_exc()
            return False

    def update_item(self , query , *args):
        try: 
            with MAKE_CONNECTION(self.connection) as cursor:
                cursor.execute(query , args)
                if cursor.rowcount > 0:
                    return True
        except sqlite3.Error:
            return False