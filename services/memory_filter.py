class MemoryFilter:

    def __init__(self):
        self.ignore_messages = {
            "hi",
            "hello",
            "hey",
            "thanks",
            "thank you",
            "ok",
            "okay",
            "yes",
            "no",
            "good morning",
            "good night",
            "bye",
        }

    def should_store(self, text: str) -> bool:

        text = text.strip().lower()

        if text in self.ignore_messages:
            return False

        if len(text.split()) < 4:
            return False

        return True


memory_filter = MemoryFilter()