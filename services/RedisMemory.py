import redis
import json
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
load_dotenv()

r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    username=os.getenv("REDIS_USERNAME", "default"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
)


def save_message(session_id: str, role: str, message: str) -> None:
    """
    Save a chat message in Redis under a session_id.
    Role can be 'user' or 'assistant'.
    """
    r.rpush(session_id, json.dumps({"role": role, "message": message}))


def get_conversation(session_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Retrieve chat history for a session.
    Returns list of {"role": ..., "message": ...}.
    If limit is given, only the last N messages are returned.
    """
    messages = r.lrange(session_id, 0, -1)
    history = [json.loads(m) for m in messages]

    return history[-limit:] if limit else history


def clear_conversation(session_id: str) -> None:
    """
    Delete all chat history for a session.
    """
    r.delete(session_id)
