import os
import psycopg2
from psycopg2.extras import RealDictCursor
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="students_db",
        user="postgres",
        password="1111", 
        cursor_factory=RealDictCursor
    )
    return conn
    return conn