from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from bot_logic import get_reply

app = Flask(__name__)


@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "")
    reply_text = get_reply(incoming_msg)

    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)


@app.route("/", methods=["GET"])
def health_check():
    return "WhatsApp bot server is running."


if __name__ == "__main__":
    app.run(debug=True, port=5000)
