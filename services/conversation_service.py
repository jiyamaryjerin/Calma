from collections import deque


class ConversationService:

    def __init__(self):
        # Keep the last 20 messages
        self.history = deque(maxlen=20)

    def add_user_message(self, message: str):
        self.history.append({
            "role": "user",
            "content": message
        })

    def add_assistant_message(self, message: str):
        self.history.append({
            "role": "assistant",
            "content": message
        })

    def get_history(self):
        return list(self.history)

    def clear(self):
        self.history.clear()


conversation_service = ConversationService()