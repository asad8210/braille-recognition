# Braille Assistive Vision

# Braille Assistive Reader – AI Integrated Model

An AI-powered assistive technology project designed to help visually impaired users by recognizing Braille characters from images, converting them into readable English text, and providing real-time audio feedback.

---

## 🔍 Features

- 📷 Image input for Braille script
- 🧠 AI model for character classification (`.keras`)
- 🧩 Braille segmentation engine using OpenCV
- 🔠 Translation of Braille to English
- 🔊 Text-to-Speech conversion
- 🌐 Web interface built with Flask
- 🐳 Docker-ready deployment

---

## 📁 Project Structure

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

yaml


---

## 🚀 Run Locally

### 🧰 Setup

```bash
pip install -r requirements.txt
python app.py
Open your browser at http://localhost:5000

🐳 Docker Support
🛠️ Build the Docker image

docker build -t braille-recognition .
▶️ Run the container
bash

docker run -p 5000:5000 braille-recognition
👨‍💻 Author
Asad– @asad8210

🤝 Contributions
Feel free to fork, raise issues, and submit pull requests to improve this assistive technology system.

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

The design/programming methodologies include the following modules:
1.	Creating an user friendly interface: The user would be able to convert Braille into Text and Speech here.
2.	Braille image acquisition: The user can directly upload braille scripts of their choice for conversion.
3.	Image processing using OpenCV: The Braille input image should be processed in the way that is convenient to read and it is done by using methods in OpenCV (Open Source Computer Vision) library which is primarily aimed toward a real-time PC vision. To identify the braille letters, we will use an model, ocr , bitwise and tesserect with our dataset. 
4.	Text to Speech: The Braille script to Text conversion explores a python module that translates braille script input images into text which is in turn converted to speech and vice-versa, using gTTS API and pyttsx3 library. The principal objective of this task is to set up a means of reading comprehension for specially-abled people.
