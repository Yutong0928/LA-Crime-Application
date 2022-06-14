"""
coding: utf-8
author: tianqi
email: tianqixie98@gmail.com
"""
import mysql.connector
import sys

config = {
    "host": "localhost",
    "user": "dsci551",
    "password": "dsci551",
    "database": "dsci551"
}


class SearchData:
    # initial the database
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )

    @staticmethod
    # convert tuple to list
    def tupleToList(tuples):
        res = []
        for tuple in tuples:
            res.append(list(tuple))
        return res

    def fetchData(self, sql):
        myresult = []
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
        except:
            print("can not find the data")
        return SearchData.tupleToList(myresult)


    def __del__(self):
        self.mydb.close()


