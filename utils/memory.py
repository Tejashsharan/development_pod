from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import RedisChatMessageHistory

def get_memory(session_id="default"):
    history = RedisChatMessageHistory(url="redis://localhost:6379", session_id=session_id)
    memory = ConversationBufferMemory(chat_memory=history, return_messages=True)
    return memory
