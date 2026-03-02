import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template

from model import chatbot_model

app = Flask(__name__)

DB_FILE = "database.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def log_interaction(user_message, bot_response, confidence):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        timestamp = datetime.now().isoformat()
        c.execute("""
            INSERT INTO interactions (user_message, bot_response, confidence, timestamp)
            VALUES (?, ?, ?, ?)
        """, (user_message, bot_response, confidence, timestamp))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging interaction: {e}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data["message"].strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    intent, confidence = chatbot_model.predict_intent(user_message)
    response_text = chatbot_model.get_response(intent)
    
    # Format precision
    confidence_formatted = round(float(confidence), 2)

    log_interaction(user_message, response_text, confidence_formatted)

    return jsonify({
        "response": response_text,
        "confidence": confidence_formatted,
        "intent": intent
    })

@app.route("/logs")
def view_logs():
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM interactions ORDER BY timestamp DESC LIMIT 100")
        rows = c.fetchall()
        conn.close()
        
        # Super basic HTML for the bonus /logs endpoint
        html = "<html><head><title>Chat Logs</title><style>body{font-family:sans-serif;padding:20px;} table{border-collapse:collapse;width:100%;} th,td{border:1px solid #ddd;padding:8px;text-align:left;} th{background-color:#f2f2f2;}</style></head><body><h1>Recent Interactions</h1><table><tr><th>ID</th><th>User Message</th><th>Bot Response</th><th>Confidence</th><th>Timestamp</th></tr>"
        for row in rows:
            html += f"<tr><td>{row['id']}</td><td>{row['user_message']}</td><td>{row['bot_response']}</td><td>{row['confidence']}</td><td>{row['timestamp']}</td></tr>"
        html += "</table></body></html>"
        
        return html
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    init_db()
    # Create required directories for frontend
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    app.run(debug=True, port=5000)
