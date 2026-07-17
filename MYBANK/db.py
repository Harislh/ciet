import mysql.connector

def getConnection():
     con = mysql.connector.connect(
          host="localhost",
          user="root",
          password="root",
          database = "mybank"
     )
     
     return con