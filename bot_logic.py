import groq
from dotenv import load_dotenv

load_dotenv()

client = groq.Groq()  # reads GROQ_API_KEY from env
MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = (
    "You are a friendly, helpful assistant chatting with a user over WhatsApp. "
    "Keep replies short (1-3 sentences) and conversational, since this is a "
    "WhatsApp chat, not a document."
)

MAX_HISTORY_MESSAGES = 20  # trim to keep the prompt bounded

# In-memory per-sender conversation history. Not persisted across restarts —
# fine for a single-process dev bot; swap for a real store before scaling out.
_conversations: dict[str, list[dict]] = {}

RULE_REPLIES = {
    "hi": "Hello! Welcome to our WhatsApp bot. Type 'help' to see what I can do.",
    "hello": "Hello! Welcome to our WhatsApp bot. Type 'help' to see what I can do.",
    "hey": "Hello! Welcome to our WhatsApp bot. Type 'help' to see what I can do.",
    "help": "Here's what I can do:\n- Type 'hi' to greet me\n- Type 'about' to learn about this project\n- Type 'bye' to end the chat\n- Ask me anything else and I'll do my best to answer!",
    "about": "This is a WhatsApp chatbot built by nmtiwari25 and a friend, using Flask + Twilio + Llama (via Groq).",
    "bye": "Goodbye! Have a great day.",
}


def get_reply(message: str, session_id: str = "default") -> str:
    text = message.strip().lower()

    if text in RULE_REPLIES:
        return RULE_REPLIES[text]

    return _call_groq(session_id, message)


def _call_groq(session_id: str, message: str) -> str:
    history = _conversations.setdefault(session_id, [])
    history.append({"role": "user", "content": message})
    del history[:-MAX_HISTORY_MESSAGES]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *history],
        )
    except groq.RateLimitError:
        history.pop()
        return "I'm getting a lot of requests right now — please try again in a moment."
    except groq.APIStatusError as e:
        history.pop()
        return f"Sorry, I hit an error talking to my brain (status {e.status_code}). Please try again."
    except groq.APIConnectionError:
        history.pop()
        return "I couldn't reach my AI service just now. Please check your connection and try again."

    reply_text = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply_text})
    return reply_text
