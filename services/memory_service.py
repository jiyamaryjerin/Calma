from datetime import datetime
from models.memory import Memory


class MemoryService:

    def __init__(self):
        self.memories = []

    def add_memory(self, memory_data: dict):

        memory = Memory(
            type=memory_data["type"],
            fact=memory_data["fact"],
            importance=memory_data["importance"],
            timestamp=datetime.now(),
        )

        self.memories.append(memory)

        return memory

    def get_memories(self):
        return self.memories

    def clear(self):
        self.memories.clear()



memory_service = MemoryService()