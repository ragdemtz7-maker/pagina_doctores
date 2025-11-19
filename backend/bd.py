import pymysql
import os

def get_connection():
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "database-proyecto-final.c7qoq2es4loe.us-east-2.rds.amazonaws.com"),
        user=os.environ.get("DB_USER", "admin"),
        password=os.environ.get("DB_PASSWORD", "#Citasmedicas123"),
        database=os.environ.get("DB_NAME", "citas_medicas"),
        cursorclass=pymysql.cursors.Cursor
    )
