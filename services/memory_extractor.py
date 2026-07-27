class MemoryExtractor:

    family_keywords = [
        "mother", "father", "mom", "dad",
        "parents", "parent",
        "brother", "sister", "siblings",
        "grandmother", "grandfather",
        "grandma", "grandpa",
        "uncle", "aunt", "cousin",
        "nephew", "niece",
        "wife", "husband", "partner",
        "girlfriend", "boyfriend",
        "fiance", "fiancée",
        "spouse",
        "son", "daughter",
        "child", "children",
        "family"
    ]

    def extract(self, text: str):

        text = text.strip()
        lower = text.lower()

        # Career
        if (
            "interview" in lower or
            "placement" in lower or
            "job" in lower or
            "career" in lower
        ):
            return {
                "type": "career",
                "fact": text,
                "importance": 0.95,
            }

        # Education
        if (
            "exam" in lower or
            "college" in lower or
            "study" in lower or
            "school" in lower or
            "university" in lower
        ):
            return {
                "type": "education",
                "fact": text,
                "importance": 0.90,
            }

        # Family
        if any(word in lower for word in self.family_keywords):
            return {
                "type": "family",
                "fact": text,
                "importance": 0.95,
            }

        # Mental Health
        if (
            "anxiety" in lower or
            "stress" in lower or
            "depression" in lower or
            "mental health" in lower or
            "therapy" in lower
        ):
            return {
                "type": "mental_health",
                "fact": text,
                "importance": 1.0,
            }

        return {
            "type": "general",
            "fact": text,
            "importance": 0.5,
        }


memory_extractor = MemoryExtractor()