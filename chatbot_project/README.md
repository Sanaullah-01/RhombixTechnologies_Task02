# Retrieval-Based Chatbot

A production-ready, full-stack retrieval-based AI chatbot for commercial websites. It uses machine learning (`scikit-learn`'s TF-IDF Vectorizer and Logistic Regression) to classify user intents and match them with predefined responses.

## Features
- **Machine Learning**: Uses TF-IDF and Logistic Regression for highly accurate intent matching.
- **RESTful API**: Flask backend providing a standardized `/chat` JSON endpoint.
- **Interaction Logging**: Automatic logging of all user and bot messages with confidence scores into an SQLite database.
- **Admin Logs**: View recent chat sessions natively at the `/logs` endpoint.
- **Modern UI/UX**: Professional frontend using HTML/CSS/Vanilla JS featuring typing animations, scroll-handling, smooth chat bubbles, and a modal fallback dialog to talk to a human agent.
- **Fallback Handling**: Graceful fallback capabilities triggering human support workflows when the intent confidence is too low.

## Architecture
```text
System Architecture:

Frontend (HTML/CSS/JS)
         ↓
Flask Backend API (/chat)
         ↓
Intent Classification Model (Logistic Regression + TF-IDF)
         ↓
Response Engine (intent matching via intents.json)
         ↓
SQLite Database (database.db)
```

## Folder Structure
```
chatbot_project/
│
├── app.py               # Main Flask server and APIs
├── model.py             # Machine learning model loader/predictor
├── train.py             # Script to train and save the ML model
├── intents.json         # Dataset containing predefined intents
├── database.db          # Auto-generated SQLite database (logging)
│
├── templates/
│   └── index.html       # Chatbot frontend UI
│
├── static/
│   ├── style.css        # Premium styling
│   └── script.js        # Chat handling logic
│
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- `pip` (Python package installer)

### 2. Installation
Clone the repository or navigate to the project root, then install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Model Training
Run the training script to generate the models (`model.pkl` and `vectorizer.pkl`) from the `intents.json` data:
```bash
python train.py
```

### 4. Running the Application
Start the Flask application server:
```bash
python app.py
```
The application will run on `http://127.0.0.1:5000/`. The SQLite database will be created automatically.

## Endpoints
- `GET /` - Renders the chat UI.
- `POST /chat` - Expects JSON payload `{"message": "user text"}`. Returns proper response text and intent data.
- `GET /logs` - Admin route displaying the last 100 logged interactions.

## Future Improvements
- Implement JWT or session-based authentication for the `/logs` route.
- Add multi-language intent classification using embeddings.
- Implement more granular logging and metrics (dashboards, most asked queries).
- Support multimedia messages or rich UI cards in the chat window.
