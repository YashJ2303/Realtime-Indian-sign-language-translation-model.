# VoiceForAll: A Realtime Indian Sign Language Translator

This is a **Realtime Indian Sign Language (ISL) Translator** built using **Machine Learning** and **Computer Vision**.

It supports:

- 🔍 Static ISL character prediction (A–Z, 1–9).
- 📹 Realtime gesture prediction using webcam.
- ✍ Text → ISL step-by-step instructions (via Groq API).
- 🧠 Scripts for dataset capture, model training and testing.



## Salient Features:

### Predict from Image:
Upload an image of a hand gesture to get the predicted ISL character.

### Realtime Gesture Recognition:
Use your webcam to perform gestures and see them recognized in realtime.

### Convert Text to ISL Steps:
Provide a phrase and get step-by-step ISL gesture instructions.

### Training Support:
Includes code to:
- Capture custom gesture dataset
- Train a basic CNN gesture classifier
- Test realtime OpenCV-based gesture prediction



## 📥 Clone the Repository

```bash
git clone https://github.com/Jayesh251203/Realtime-Indian-sign-language-translation-model.-.git
cd Realtime-Indian-sign-language-translation-model.-
```
🛠️ Installation
1. Create a virtual environment (recommended)
```
python -m venv isl_env
```

Activate it:

⚡ Windows
```
isl_env\Scripts\activate
```

🐧 Linux / macOS
```
source isl_env/bin/activate
```
2. Install dependencies
```
pip install -r requirements.txt
```
🚀 Run the Web App

Start the Streamlit application:
```
streamlit run app/app.py
```

The app will open in your browser.

📦 Models (Download & Setup)

Model files are not included in the repo due to size limits.

Create a folder named models/ at the root and place your .h5 models inside:

models/
│── isl_model_new.h5
│── hand_gesture_model.h5

📊 Dataset Reference

The static ISL classifier model was trained on:
```
🔗 https://www.kaggle.com/datasets/prathumarikeri/indian-sign-language-isl
```
🧠 Kaggle Notebook (Training Reference)

Static ISL model training notebook:
```
🔗 https://www.kaggle.com/code/jayeshkawale25/indian-sign-language-isl-prediction-creation/edit
```
🎥 Capture Your Own Dataset

To capture gestures from your webcam:
```
python training/capture_images/capture.py
```

This script generates folders for each gesture class as images.

🏋️ Train Gesture Model

To train a gesture classifier:
```
python training/train/train.py
```

This saves:

hand_gesture_model.h5

best_hand_gesture_model.h5

▶️ Test OpenCV Realtime Prediction

Run:
```
python training/predict/predict.py
```

Press q to quit.

🌍 Groq API Setup (Text → ISL)

To use text-to-ISL:

Create a .env file in the root:

GROQ_API_KEY=your_api_key_here


Do not commit your .env file.

⚠️ Notes

Static predictions support letters & digits only.

Realtime accuracy depends on lighting and framing.

Full sentence-level recognition is future work.

## Credits

#### Nishit Jain

#### Pragati Thawkar 

#### Yash Joshi

#### Gaurav Saini

#### Jayesh Kawale
