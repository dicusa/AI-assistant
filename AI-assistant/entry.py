from flask import Flask, request, jsonify
from assistant.speech import SpeechEngine
from assistant.commands import handle_query
from assistant.utils import get_greeting
from assistant.plugins import reminders

app = Flask(__name__)

speech_engine = SpeechEngine()
reminders.start_scheduler_thread()

@app.route("/")
def home():
    return "Zara AI Assistant is running!"

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    user_query = data.get("query")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Handle the query and get a response (simulate speaking)
    flag,response = handle_query(user_query, speech_engine)
    # If handle_query returns True/False, you may want to capture actual text output
    # For now, let's assume it returns a response string
    return jsonify({"response": response})

if __name__ == "__main__":
    # Use host="0.0.0.0" to allow connections from other devices on your network
    app.run(host="0.0.0.0", port=5000, debug=True)
