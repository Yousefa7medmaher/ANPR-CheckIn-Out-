# ANPR System for Vehicle Check-in and Check-out

## Overview
This project implements an **Automated Number Plate Recognition (ANPR)** system to automate vehicle check-in and check-out processes using deep learning and computer vision techniques. The system captures license plate images, processes them to extract text, and stores the data for future reference. A web interface is also developed to track vehicle history.

## Features
- Manual image collection using mobile and camera
- Dataset creation using **Roboflow** (bounding box labeling)
- **YOLO11 Algorithm** for license plate detection
- **PaddleOCR & OpenCV (cv2)** for text extraction and image processing
- **Anaconda virtual environment** for package management
- **Python-based backend** for processing real-time and static images
- **Database integration** for storing and managing records
- **Web application using Express.js, HTML, CSS, and JavaScript** for vehicle history tracking

## Technologies Used
- **Python** (OpenCV, PaddleOCR, YOLO11)
- **Roboflow** (Dataset preparation and annotation)
- **Anaconda** (Environment management)
- **MySQL, Express.js, HTML, CSS, Node.js** (Web interface for history tracking)

## Installation
### Prerequisites:
- Python (>=3.8)
- Anaconda
- Node.js & npm
- MySQL

### Steps:
1. Clone this repository:
   ```sh
   git clone https://github.com/Yousefa7medmaher/ANPR-System.git
   cd ANPR-System
   ```
2. Setup Python environment:
   ```sh
   conda create --name anpr_env python=3.8
   conda activate anpr_env
   pip install -r requirements.txt
   ```
3. Setup Web Application:
   ```sh
   cd server
   npm install
   node server.js
   ```

## Usage
- Run the Python script to capture and process images.
- Use the web application to view check-in and check-out history.

## Future Improvements
- Optimize the model for faster inference.
- Implement automatic dataset expansion.
- Deploy the system on cloud servers for real-time accessibility.

## License
This project is licensed under the MIT License.

## Contact
- **Author:** Yousef Ahmed Maher
- **GitHub:** [@Yousefa7medmaher](https://github.com/Yousefa7medmaher)
- **Email:** ya1770620@gmail.com

