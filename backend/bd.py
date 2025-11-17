import pymysql

def get_connection():
    return pymysql.connect(
        host="database-proyecto-final.c7qoq2es4loe.us-east-2.rds.amazonaws.com",
        user="admin",
        password="#Citasmedicas123",
        database="citas_medicas"
    )
