import os
import cv2
import numpy as np
from ultralytics import YOLO
from paddleocr import PaddleOCR

def detect_car_plate(image_path, model, ocr):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(image_path)
 
    results = model(image)
    boxes = results[0].boxes.data.cpu().numpy()

    detected_data = []
    confidences = []

    for box in boxes:
        x1, y1, x2, y2, conf, cls = map(int, box[:6])

 
        if x2 - x1 < 30 or y2 - y1 < 10:
            continue  

        cropped_plate = image[y1:y2, x1:x2]
 
        gray_plate = cv2.cvtColor(cropped_plate, cv2.COLOR_BGR2GRAY)
        processed_plate = cv2.GaussianBlur(gray_plate, (3, 3), 0)

        ocr_result = ocr.ocr(processed_plate)

        plate_text = ""
        for line in ocr_result[0]:
            text, prob = line[1]
            if text.strip():
                plate_text += text.strip() + " "

        if plate_text.strip():
            detected_data.append(plate_text.strip())
            confidences.append(prob)

 
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
        print("Detected Plate Text:", detected_data[-1])
    else:
        print("No text detected. Try improving the image quality.")
 
    cv2.imwrite("output_detected_plate.jpg", image)

    return image, detected_data, confidences
