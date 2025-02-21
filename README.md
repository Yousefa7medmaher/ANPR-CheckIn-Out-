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

## Installation & Setup

### Prerequisites:
- Download and install **Anaconda** [here](https://www.anaconda.com/products/distribution)
- Install **MySQL** [here](https://dev.mysql.com/downloads/installer/)
- Install **Node.js** and **npm** [here](https://nodejs.org/)
- Install **VS Code** [here](https://code.visualstudio.com/)

### Steps:

#### 1. Clone this repository:
```sh
git clone https://github.com/Yousefa7medmaher/ANPR-System.git
cd ANPR-System
```

#### 2. Create and Activate Anaconda Virtual Environment:
```sh
conda create --name anpr_env python=3.8
conda activate anpr_env
```

#### 3. Install Required Python Packages:
```sh
pip install opencv-python numpy ultralytics paddleocr mysql-connector-python flask
```

#### 4. Setup Web Application:
```sh
cd server
npm install
node server.js
```

#### 5. Create MySQL Database:
```sql
CREATE DATABASE anpr_db;
USE anpr_db;

CREATE TABLE car_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plate_number VARCHAR(20) NOT NULL,
    check_in_time DATETIME NOT NULL,
    check_out_time DATETIME NULL,
    status VARCHAR(10) NOT NULL DEFAULT 'IN'
);
```

#### 6. Setup Database Connection in `.env` file:
Create a `.env` file in the root directory and add:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=anpr_db
```

#### 7. Open Project in VS Code:
```sh
code .
```

#### 8. Run ANPR System:
```sh
python main.py
```

## Usage
1. **Run the Python script** to capture and process images:
   ```sh
   python main.py
   ```
2. **Check the web application** to view vehicle check-in and check-out history:
   ```sh
   cd server
   node server.js
   ```
3. Open `http://localhost:3000` in your browser to access the web interface.

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

