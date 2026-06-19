# Disease-Prediction

Disease Prediction is an application that predicts possible diseases based on patient symptoms using a Machine Learning model. The system generates a professional medical-style diagnostic report containing AI predictions, confidence analysis, and detailed meta knowledge.

> ⚠ **Disclaimer:** This project is developed for educational and research purposes only. It is not intended to replace professional medical advice, diagnosis, or treatment.

---

## 📌 Features

### 🩺 Patient Symptom Analysis

* Search and select symptoms using an intelligent autocomplete system.
* Record multiple symptoms for disease prediction.
* Generate a structured clinical diagnostic report.

### 🤖 Machine Learning Disease Prediction

* Uses a trained Random Forest classifier for disease prediction.
* Predicts the top 3 most probable diseases.
* Displays confidence scores for each prediction.
* Provides a differential diagnosis table.

### 📊 Clinical Report Generation

* Hospital-style medical report interface.
* Unique report ID generation.
* Timestamped diagnostic report.
* Diagnostic confidence visualization using Plotly charts.
* Print or save the complete medical report as PDF.

### 📚 Medical Knowledge Integration

* Displays disease information including:

  * Overview
  * Symptoms
  * Causes
  * Risk Factors
  * Complications
  * Prevention
  * Diagnosis
  * Treatment
  * Lifestyle and home remedies
* Includes references and additional medical resources.

### 🔐 Security Features

* API rate limiting using Flask-Limiter.
* Input validation and error handling.
* Controlled access to prediction endpoints.

---

# 🧠 Machine Learning Model

The prediction engine is built using a **Random Forest Classifier** trained on symptom-disease data.

The model analyzes a patient's symptoms using a binary symptom vector and predicts the most likely diseases along with their probability scores.

---

# 📂 Datasets

## 1. Disease Prediction Dataset (Model Training)

Source:
https://www.kaggle.com/datasets/kaushil268/disease-prediction-using-machine-learning

Dataset Details:

* 132 symptom features.
* 42 disease classes.
* Training and testing CSV files.
* Binary symptom representation.

This dataset is used to train the Random Forest disease prediction model.

The dataset contains 132 symptom parameters that can be used to predict 42 different diseases. The data includes training and testing CSV files where symptoms are represented as features and the prognosis column represents the disease label.

---

## 2. Healthcare Disease Knowledge Dataset (Metadata)

Source:
https://huggingface.co/datasets/harmesh95/healthcare-disease-knowledge

This dataset provides additional medical information used to enrich the generated clinical report.

It contains medical knowledge such as:

* Disease overview.
* Symptoms.
* Causes.
* Risk factors.
* Diagnosis.
* Treatment.
* Prevention.
* Additional healthcare references.

---

# 🏗️ System Architecture

```
User
 │
 ▼
Symptom Selection UI
 │
 ▼
Flask Backend API
 │
 ▼
Random Forest Prediction Model
 │
 ├── Top 3 Disease Predictions
 │
 ├── Confidence Scores
 │
 └── Medical Knowledge Lookup
        │
        ▼
Clinical Diagnostic Report
```

---

# 🛠️ Technology Stack

## Backend

* Python
* Flask
* Scikit-learn
* NumPy
* Pandas
* Joblib
* Flask-Limiter

## Frontend

* HTML5
* CSS3
* JavaScript
* Plotly.js

## Machine Learning

* Random Forest Classifier

---

# 📁 Project Structure

```
Disease-Prediction/
│
├── app.py                     # Flask application
│
├── Pickle Files/
│   ├── disease_rf_model.pkl   # Trained Random Forest model
│   ├── label_encoder.pkl      # Disease label encoder
│   ├── training_dataset.pkl   # Processed training dataset
│   └── healthcare_dataset.pkl # Medical knowledge dataset
│
├── templates/
│   └── index.html             # HealthAI clinical report UI
│
├── static/
│   ├── style.css              # Medical report styling
│   └── script.js              # Frontend logic
│
├── requirements.txt
│
└── README.md
```

---

# 🚀 Installation and Setup

## 1. Clone Repository

```bash
git clone https://github.com/Lightning-President-9/Disease-Prediction.git

cd Disease-Prediction
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```
---

# 📜 License

This project is created for educational and research purposes.

---
