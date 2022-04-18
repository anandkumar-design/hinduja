import sqlite3
from .models import Student,marks

class sql_execution:
    def my_custom_sql(self,query):
        connection = sqlite3.connect('db.sqlite3')
        connection.row_factory = sqlite3.Row
        c = connection.cursor()
        c.execute(query)
        # row = c.fetchall()
        result = [dict(row) for row in c.fetchall()] 
        return result