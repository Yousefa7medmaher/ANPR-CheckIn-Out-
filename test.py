import mysql.connector
from db_connection import create_db_connection
from datetime import datetime

def test_db_connection():
    try:
        # محاولة الاتصال بقاعدة البيانات
        db_connection = create_db_connection()
        cursor = db_connection.cursor()
        
        # اختبار الاتصال عن طريق إظهار الجداول الموجودة
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("Tables in database:")
        for table in tables:
            print(table)

        # إدخال بيانات اختبار في جدول car_log
        plate_number = "ر د ص م ١ ٢ ٣"
        check_in_time = datetime.now()  # تاريخ ووقت الدخول
        check_out_time = None  # لم يتم الخروج بعد
        status = 'In'  # الحالة هي "In" حالياً

        insert_query = """
            INSERT INTO car_log (plate_number, check_in_time, check_out_time, status)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(insert_query, (plate_number, check_in_time, check_out_time, status))
        db_connection.commit()  # تأكيد التغييرات في قاعدة البيانات
        
        print(f"Inserted data: {plate_number} with status {status}.")

        # إغلاق الاتصال
        cursor.close()
        db_connection.close()

        print("Connection test successful!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
# تشغيل الاختبار
if __name__ == "__main__":
    test_db_connection()
