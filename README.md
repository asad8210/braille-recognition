# 📘 Braille Assistive Vision

**Braille Assistive Vision** is an AI-powered assistive technology system designed to empower visually impaired users. It processes Braille script images, segments and recognizes characters, converts them into English text, and provides real-time audio feedback — all through an intuitive web interface.

---

## 🎯 Objective

To develop an AI-integrated, user-friendly tool for visually impaired individuals that:
- Recognizes Braille characters from scanned or uploaded images.
- Translates the recognized Braille into readable English text.
- Converts the translated text into speech for seamless auditory feedback.

---

## 🧩 System Modules

### 1. User-Friendly Interface
An accessible and responsive interface built using **Flask** that allows users to:
- Upload Braille script images.
- View recognized English text.
- Listen to real-time audio output.

### 2. Braille Image Acquisition
Users can upload images of Braille documents directly through the web interface for processing.

### 3. Image Processing with OpenCV
Utilizes the **OpenCV** library for:
- Preprocessing Braille images.
- Segmenting Braille cells.
- Identifying dot patterns using custom logic, bitwise operations, and **Tesseract OCR** in combination with a trained AI model.

### 4. AI-Based Braille Character Classification
A custom-trained neural network model (`BrailleModel.keras`) is used to classify segmented Braille characters into their corresponding English alphabet.

### 5. Text-to-Speech Conversion
- Converts recognized text to speech using **gTTS** and **pyttsx3** libraries.
- Enables reading comprehension via auditory feedback, supporting the visually impaired.

---

## 🚀 Features

- 📷 Image Upload for Braille Script
- 🧠 AI Character Classification using `.keras` model
- 🧩 Braille Segmentation Engine (OpenCV)
- 🔠 Translation from Braille to English
- 🔊 Real-Time Text-to-Speech Output
- 🌐 Web App Interface (Flask)
- 🐳 Docker Support for Easy Deployment

---

## 🗂 Project Structure
braille-recognition/
├── AI_integrated_Model/
│ ├── BrailleCharacter.py
│ ├── BrailleClassifier.py
│ ├── BrailleImage.py
│ ├── SegmentationEngine.py
│ └── hello.py
├── model/
│ └── BrailleModel.keras
├── samples/
├── templates/
│ └── index.html
├── app.py
├── digest.py
├── favicon.ico
├── requirements.txt
└── Dockerfile

yml
---

## ⚙️ Installation & Running

### 📦 Local Setup

```bash
pip install -r requirements.txt
python app.py
Open your browser at: http://localhost:5000

🐳 Docker Deployment
Build Docker Image:
docker build -t braille-recognition .

Run Docker Container:
docker run -p 5000:5000 braille-recognition

👨‍💻 Author
Asad – @asad8210
email-beingasad47@gmail.com

🤝 Contributions
Contributions are welcome!
Feel free to fork this repository, open issues, or submit pull requests to enhance the functionality and performance of this assistive technology system.

📜 License
This project is licensed under the MIT License.

MIT License Summary
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:



