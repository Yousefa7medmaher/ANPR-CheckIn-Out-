import os
import cv2
import numpy as np
from ultralytics import YOLO
from paddleocr import PaddleOCR

def detect_car_plate(image_path, model, ocr):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # تحميل الصورة
    image = cv2.imread(image_path)

    # تنفيذ الكشف عن اللوحة باستخدام YOLO
    results = model(image)
    boxes = results[0].boxes.data.cpu().numpy()

    detected_data = []
    confidences = []

    for box in boxes:
        x1, y1, x2, y2, conf, cls = map(int, box[:6])
        cropped_plate = image[y1:y2, x1:x2]  # قص اللوحة من الصورة الأصلية

        # التعرف على النص باستخدام OCR
        ocr_result = ocr.ocr(cropped_plate)

        plate_text = ""  # لتجميع النص بنفس الترتيب الأصلي
        
        for line in ocr_result[0]:
            text, prob = line[1]
            text = text.strip()
            if text:
                # إضافة مسافة صغيرة بين الأحرف عند التجميع
                spaced_text = " ".join(text)
                plate_text += spaced_text + "  "  # مسافتان بين الكلمات

                detected_data.append(plate_text.strip())  # إضافة النص بنفس التسلسل
                confidences.append(prob)

                # رسم الإطار حول اللوحة المكتشفة وإضافة النص المكتشف
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    image,
                    plate_text.strip(),
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 0, 0),
                    2,
                    lineType=cv2.LINE_AA,
                )

    if detected_data:
        print("end")
        print("Detected Plate Text:", detected_data[-1])  # عرض النص المكتشف بنفس الترتيب
    else:
        print("No text detected, applying image processing...")

        # تطبيق تحسينات للصورة
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
        resized_image = cv2.resize(gray_image, (640, 480))  
        processed_image = cv2.GaussianBlur(resized_image, (5, 5), 0)  

        # إعادة الكشف بعد المعالجة
        results = model(processed_image)
        boxes = results[0].boxes.data.cpu().numpy()

        plate_text = ""

        for box in boxes:
            x1, y1, x2, y2, conf, cls = map(int, box[:6])
            cropped_plate = processed_image[y1:y2, x1:x2]
            ocr_result = ocr.ocr(cropped_plate)

            for line in ocr_result[0]:
                text, prob = line[1]
                text = text.strip()
                if text:
                    # إضافة مسافة بين الأحرف بعد معالجة الصورة
                    spaced_text = " ".join(text)
                    plate_text += spaced_text + "  "

                    detected_data.append(plate_text.strip())
                    confidences.append(prob)

                    # رسم الإطار
                    cv2.rectangle(processed_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(
                        processed_image,
                        plate_text.strip(),
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 0, 0),
                        2,
                        lineType=cv2.LINE_AA,
                    )

        if detected_data:
            print("end")
            print("Detected Plate Text (after processing):", detected_data[-1])
        else:
            print("No text detected after processing.")

    # عرض الصورة
    cv2.imshow("Detected Car Plate", image if detected_data else processed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return image, detected_data, confidences
