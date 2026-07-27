try:
    from transformers import pipeline
except Exception:
    pipeline = None


class EmotionService:
    def __init__(self):
        self.classifier = None

    def _ensure_classifier(self):
        if self.classifier:
            return True
        if pipeline is None:
            print("transformers.pipeline not available; emotion detection disabled.")
            return False
        try:
            print("Initializing Emotion Classifier...")
            self.classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                top_k=1,
            )
            print("Emotion Model Loaded Successfully!")
            return True
        except Exception as e:
            print("Failed to load emotion model:", e)
            return False

    def detect_emotion(self, text: str):
        if not self._ensure_classifier():
            return {"emotion": "neutral", "confidence": 0.0}

        result = self.classifier(text)[0][0]

        raw_emotion = result["label"]

        emotion_map = {
            "joy": "happy",
            "love": "happy",
            "sadness": "sad",
            "anger": "angry",
            "fear": "anxious",
            "surprise": "neutral",
            "neutral": "neutral",
        }

        return {
            "emotion": emotion_map.get(raw_emotion, "neutral"),
            "confidence": round(result["score"], 3),
        }


emotion_service = EmotionService()