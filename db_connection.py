import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE

def create_db_connection():
    try:
        db_connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )
        if db_connection.is_connected():
            print("✅ Successfully connected to the database.")
            return db_connection
    except Error as e:
        print(f"❌ Database connection failed: {e}")
        return None
