import mysql.connector
from db_connection import create_db_connection
from datetime import datetime

def insert_car_log(plate_number, status):
    db_connection = create_db_connection()
    cursor = db_connection.cursor()

    # التحقق مما إذا كانت السيارة مسجلة بالفعل في قاعدة البيانات
    current_log = get_current_car_log(plate_number)

    # إذا كانت السيارة مسجلة بالفعل ولكن بحالة مختلفة، يتم إنشاء سجل جديد بحالة "Login"
    if current_log:
        last_status = current_log[4]
        
        if last_status == 'Out' and status == 'In':
            # عند عودة السيارة بعد خروجها، نقوم بإنشاء سجل جديد بحالة "Login"
            check_in_time = datetime.now()
            check_out_time = None

            insert_query = """
            INSERT INTO car_log (plate_number, check_in_time, check_out_time, status)
            VALUES (%s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (plate_number, check_in_time, check_out_time, 'Login'))
            db_connection.commit()
            print(f"تم تسجيل دخول السيارة {plate_number} بحالة Login.")
            return  # لإنهاء الدالة بعد إنشاء السجل الجديد

        elif last_status == 'In' and status == 'In':
            print(f"السيارة {plate_number} بالفعل موجودة داخل الموقف.")
            return  # لا تسمح بإدخال السيارة مرة أخرى إذا كانت بالفعل في الداخل
        elif last_status == 'Out' and status == 'Out':
            print(f"السيارة {plate_number} قد خرجت بالفعل.")
            return  # لا تسمح بإخراج السيارة مرة أخرى إذا كانت بالفعل في الخارج

    # إذا لم تكن السيارة مسجلة مسبقًا، يتم إدخال بيانات جديدة بحالة "Login"
    if not current_log:
        check_in_time = datetime.now() if status == 'In' else None
        check_out_time = datetime.now() if status == 'Out' else None

        insert_query = """
        INSERT INTO car_log (plate_number, check_in_time, check_out_time, status)
        VALUES (%s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (plate_number, check_in_time, check_out_time, status))
        db_connection.commit()
        print(f"تم تسجيل {plate_number} بحالة {status}.")
    
    cursor.close()
    db_connection.close()

def get_current_car_log(plate_number):
    db_connection = create_db_connection()
    cursor = db_connection.cursor()

    select_query = """
    SELECT id, plate_number, check_in_time, check_out_time, status
    FROM car_log
    WHERE plate_number = %s
    ORDER BY id DESC
    LIMIT 1
    """
    
    cursor.execute(select_query, (plate_number,))
    result = cursor.fetchone()

    cursor.close()
    db_connection.close()

    return result

def update_car_log_status(plate_number, status):
    db_connection = create_db_connection()
    cursor = db_connection.cursor()

    current_log = get_current_car_log(plate_number)

    if current_log:
        last_status = current_log[4]
        
        # إذا كانت السيارة في حالة "In" ثم تم تحديد حالة "Out"، نقوم بتسجيل الخروج
        if last_status == 'In' and status == 'Out':
            update_query = """
            UPDATE car_log
            SET check_out_time = %s, status = %s
            WHERE id = %s
            """
            cursor.execute(update_query, (datetime.now(), status, current_log[0]))
            db_connection.commit()

            print(f"تم تسجيل خروج {plate_number} بنجاح.")
        
        # إذا كانت السيارة في حالة "Out" ثم تم تحديد حالة "In"، نقوم بإنشاء سجل جديد بحالة "Login"
        elif last_status == 'Out' and status == 'In':
            insert_car_log(plate_number, 'Login')  # إدخال جديد بحالة "Login"
        else:
            print(f"لا يمكن تغيير الحالة إلى {status}.")
    
    cursor.close()
    db_connection.close()
