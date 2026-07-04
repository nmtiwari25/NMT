def get_reply(message: str) -> str:
    text = message.strip().lower()

    if text in ("hi", "hello", "hey"):
        return "Hello! Welcome to our WhatsApp bot. Type 'help' to see what I can do."
    elif text == "help":
        return "Here's what I can do:\n- Type 'hi' to greet me\n- Type 'about' to learn about this project\n- Type 'bye' to end the chat"
    elif text == "about":
        return "This is a WhatsApp chatbot built by nmtiwari25 and a friend, using Flask + Twilio."
    elif text == "bye":
        return "Goodbye! Have a great day."
    else:
        return "Sorry, I didn't understand that. Type 'help' to see available commands."
