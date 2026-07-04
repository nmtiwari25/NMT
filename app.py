from flask import Flask, request, jsonify
from flask_cors import CORS
from twilio.twiml.messaging_response import MessagingResponse
from bot_logic import get_reply

app = Flask(__name__)
CORS(app)


@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "")
    sender = request.values.get("From", "unknown")
    reply_text = get_reply(incoming_msg, session_id=sender)

    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)


@app.route("/chat", methods=["POST"])
def chat():
    incoming_msg = request.get_json(silent=True) or {}
    session_id = incoming_msg.get("session_id", "web-default")
    reply_text = get_reply(incoming_msg.get("message", ""), session_id=session_id)
    return jsonify({"reply": reply_text})


@app.route("/", methods=["GET"])
def health_check():
    return "WhatsApp bot server is running."


if __name__ == "__main__":
    app.run(debug=True, port=5000)
