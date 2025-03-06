from flask import Flask, jsonify, request
from routes.chat import ai_chat
from routes.history import fetch_history

app = Flask(__name__)

# Routes
app.register_blueprint(ai_chat, url_prefix="/chat")
app.register_blueprint(fetch_history, url_prefix="/history")

@app.route("/")
def home():
    return jsonify({"message": "AI History Tutor API is running!"})

if __name__ == "__main__":
    app.run(debug=True)
