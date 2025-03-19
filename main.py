import os
import cv2
import numpy as np
from datetime import datetime
from car_plate_detection import detect_car_plate
from car_log import insert_entry, update_exit
from ultralytics import YOLO
from paddleocr import PaddleOCR

def main():
    try:
        # Load car plate detection model
        model = YOLO('best.pt')
        ocr = PaddleOCR(lang='ar')

        # Define test image
        image_path = 'imagesToTest/img34.jpg'
        
        # Perform plate detection
        image, detected_data, confidences = detect_car_plate(image_path, model, ocr)

        if detected_data:
            plate_text = ' '.join(detected_data).strip()
            print(f'🔍 Recognized Plate: {plate_text}')

            if confidences:
                accuracy = np.mean(confidences) * 100
                print(f"✅ Recognition Accuracy: {accuracy:.2f}%")

            # Separate letters and numbers in the plate
            letters = ''.join([char for char in plate_text if char.isalpha()])
            numbers = ''.join([char for char in plate_text if char.isdigit()])

            # Check if the car is already logged in
            if is_car_logged_in(letters, numbers):
                print(f"🚗 Car {plate_text} is already logged in. Logging out now...")
                update_exit(letters, numbers)
            else:
                print(f"🚗 Car {plate_text} is not logged in yet. Logging in now...")
                insert_entry(letters, numbers)

            # Save the processed image
            output_path = 'outputFolder/output_image.jpg'
            cv2.imwrite(output_path, image)
            print(f"📸 Processed image saved at: {output_path}")

            # Display the image
            cv2.imshow("Detected Car Plate", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("❌ No license plate detected in the image.")

    except Exception as e:
        print(f"⚠️ Error occurred while running the program: {e}")

def is_car_logged_in(letters, numbers):
    """Check if the car has entered the parking lot and hasn't exited yet."""
    import mysql.connector
    from db_connection import create_db_connection

    try:
        with create_db_connection() as db_connection, db_connection.cursor() as cursor:
            check_query = """
                SELECT id FROM appointments 
                WHERE user_id = (SELECT id FROM users WHERE letters = %s AND number = %s) 
                AND exit_time IS NULL
            """
            cursor.execute(check_query, (letters, numbers))
            return cursor.fetchone() is not None
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
        return False

if __name__ == '__main__':
    main()
