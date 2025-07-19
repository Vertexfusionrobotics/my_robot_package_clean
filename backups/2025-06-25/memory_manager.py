from datetime import datetime

class MemoryManager:
    def __init__(self):
        self.memories = []

    def remember(self, user_input):
        # Very simple extraction rule — customize later
        if "i like" in user_input.lower():
            topic = user_input.lower().split("i like")[-1].strip().rstrip(".")
            self.memories.append({
                "fact": f"You said you like {topic}.",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    def recall(self):
        if self.memories:
            last = self.memories[-1]
            return f"{last['fact']} (noted on {last['timestamp']})"
        return None
