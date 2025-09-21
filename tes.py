import os
from dotenv import load_dotenv
from services.RedisMemory import get_conversation

load_dotenv() 

print(os.getenv("REDIS_PORT"))
print(get_conversation(session_id="user123"))