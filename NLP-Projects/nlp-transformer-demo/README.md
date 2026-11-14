# NLP Transformer Project

## 📌 Project Title

**Text Classification using Transformer (DistilBERT) with Flask Web Application**

## 📖 Introduction

This project implements an NLP-based text classification system using a Transformer architecture. A pre-trained DistilBERT model is fine-tuned on a text dataset to classify user input text.

The trained Transformer model is integrated with a Flask web application that allows users to enter text and get real-time predictions with confidence scores.

## 🎯 Objectives

* Understand Transformer-based NLP workflow
* Fine-tune a pre-trained DistilBERT model
* Perform text classification using deep learning
* Build a web interface using Flask
* Generate predictions from the trained model

## 🛠 Technologies Used

* Python
* PyTorch
* Hugging Face Transformers
* DistilBERT
* Flask
* Natural Language Processing (NLP)
* Machine Learning
* HTML/CSS

## 🔄 Project Workflow

```
Dataset Loading
        ↓
Text Preprocessing
        ↓
Tokenization
        ↓
DistilBERT Fine-Tuning
        ↓
Model Training
        ↓
Model Evaluation
        ↓
Flask Web Application
        ↓
User Text Prediction
```

## 📂 Project Structure

```
NLP-Transformer-Project/

│── app.py                 # Flask web application
│── predict.py             # Prediction script
│── train.py               # Model training
│── evaluate.py            # Model evaluation
│── tokenizer.py           # Tokenization utilities
│── model.py               # Model definition
│── dataset_loader.py      # Dataset handling
│── requirements.txt       # Required libraries
│── README.md              # Project documentation

│── templates/
│     └── index.html       # Web interface

│── models/
│     └── fine_tuned_model # Trained Transformer model
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Muneeba-Asjad/NLP-Transformer-Project.git
```

Navigate to project folder:

```bash
cd NLP-Transformer-Project
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Run Flask Web Application

Start the application:

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

## 💡 Example

Input:

```
This movie was amazing and I really enjoyed it.
```

Output:

```
Label: POSITIVE

Confidence: 99%
```

## ✨ Features

* Transformer-based text classification
* Fine-tuned DistilBERT model
* Real-time prediction
* Confidence score generation
* User-friendly Flask interface

## 👩‍💻 Author

Muneeba Asjad
