import os
import cv2
import numpy as np
from datetime import datetime
from car_plate_detection import detect_car_plate
from car_log import insert_car_log, get_current_car_log, update_car_log_status
from ultralytics import YOLO
from paddleocr import PaddleOCR

def main():
    # تحميل نموذج YOLO و OCR للتعرف على الأرقام العربية
    model = YOLO('best.pt')
    ocr = PaddleOCR(lang='ar')

    # تحديد مسار الصورة
    image_path = 'imagesToTest/img34.jpg'

    # اكتشاف لوحة السيارة باستخدام YOLO و OCR
    image, detected_data, confidences = detect_car_plate(image_path, model, ocr)

    if detected_data:
        plate_text = ' '.join(detected_data)  # دمج النصوص المستخرجة إذا كان هناك أكثر من جزء
        print(f'Detected Car Plate: {plate_text}')

        # حساب دقة التعرف على النص وعرضها
        if confidences:
            accuracy = np.mean(confidences) * 100
            print(f"Accuracy: {accuracy:.2f}%")

        # التحقق مما إذا كانت السيارة مسجلة مسبقًا في قاعدة البيانات
        car_log = get_current_car_log(plate_text)

        if car_log:
            if car_log[4] == 'In':
                # تحديث وقت الخروج إذا كانت السيارة بالفعل داخل الموقف
                print(f"Car {plate_text} is currently logged in. Updating exit time.")
                update_car_log_status(plate_text, 'Out')
            else:
                print(f"Car {plate_text} has already exited.")
        else:
            # تسجيل دخول السيارة إذا لم تكن مسجلة
            print(f"Car {plate_text} is logging in.")
            insert_car_log(plate_text, 'In')

        # حفظ الصورة مع الإطار والنص
        output_path = 'outputFolder/output_image.jpg'
        cv2.imwrite(output_path, image)

        # عرض الصورة المعدلة
        cv2.imshow("Detected Car Plate", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
