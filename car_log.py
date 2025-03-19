import mysql.connector
from db_connection import create_db_connection
from datetime import datetime

def insert_or_get_user_id(letters, number):
    """Insert the car if it does not exist and return its user_id."""
    try:
        with create_db_connection() as db_connection, db_connection.cursor() as cursor:
            select_query = "SELECT id FROM users WHERE letters = %s AND number = %s"
            cursor.execute(select_query, (letters, number))
            result = cursor.fetchone()

            if result:
                return result[0]  # Return user ID if it exists

            insert_query = "INSERT INTO users (letters, number) VALUES (%s, %s)"
            cursor.execute(insert_query, (letters, number))
            db_connection.commit()
            return cursor.lastrowid  # Return the new user ID

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
        return None

def insert_entry(letters, number):
    """Register the car's entry into the parking lot."""
    user_id = insert_or_get_user_id(letters, number)
    if user_id is None:
        print(f"❌ Failed to insert car {letters}-{number} into the system.")
        return

    try:
        with create_db_connection() as db_connection, db_connection.cursor() as cursor:
            # Check if the car has already entered and hasn't exited
            check_query = "SELECT id FROM appointments WHERE user_id = %s AND exit_time IS NULL"
            cursor.execute(check_query, (user_id,))
            if cursor.fetchone():
                print(f"🚗 Car {letters}-{number} is already logged in the parking lot!")
                return

            insert_query = "INSERT INTO appointments (user_id, entry_time) VALUES (%s, %s)"
            cursor.execute(insert_query, (user_id, datetime.now()))
            db_connection.commit()
            print(f"✅ Car {letters}-{number} successfully logged in.")

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")

def update_exit(letters, number):
    """Register the car's exit from the parking lot."""
    try:
        with create_db_connection() as db_connection, db_connection.cursor() as cursor:
            select_user_query = "SELECT id FROM users WHERE letters = %s AND number = %s"
            cursor.execute(select_user_query, (letters, number))
            user = cursor.fetchone()

            if not user:
                print(f"❌ Car {letters}-{number} does not exist in the database.")
                return

            user_id = user[0]
            check_query = "SELECT id FROM appointments WHERE user_id = %s AND exit_time IS NULL"
            cursor.execute(check_query, (user_id,))
            existing_entry = cursor.fetchone()

            if not existing_entry:
                print(f"❌ Car {letters}-{number} is not registered in the parking lot or has already exited!")
                return

            update_query = "UPDATE appointments SET exit_time = %s WHERE id = %s"
            cursor.execute(update_query, (datetime.now(), existing_entry[0]))
            db_connection.commit()
            print(f"🚗 Car {letters}-{number} successfully logged out.")

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
