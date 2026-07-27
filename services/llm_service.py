import os

from dotenv import load_dotenv
try:
    from google import genai
except Exception:
    genai = None

load_dotenv()

MODEL_NAME = "gemini-flash-lite-latest"


class LLMService:

    def __init__(self):
        self.client = None
        self.api_key = os.getenv("GEMINI_API_KEY")

    def _ensure_client(self):
        if self.client:
            return True
        if genai is None:
            print("genai package not available; LLM disabled.")
            return False
        if not self.api_key:
            print("GEMINI_API_KEY not set; LLM disabled.")
            return False
        try:
            self.client = genai.Client(api_key=self.api_key)
            print("Gemini initialized successfully!")
            return True
        except Exception as e:
            print("Failed to initialize Gemini client:", e)
            return False

    def generate_response(
        self,
        message,
        emotion,
        memories,
        history,
    ):

        conversation = ""
        history = history[-10:]
        for item in history:
            conversation += (
                f"{item['role'].capitalize()}: "
                f"{item['content']}\n"
            )

        memory_text = ""

        if memories:

            if isinstance(memories, list):

                for m in memories:
                    memory_text += f"- {m}\n"

            else:

                memory_text = f"- {memories}"

        prompt = f"""
You are Calma, an AI mental wellness companion.

Your goal is to make users feel heard, understood, and supported while helping
them reflect on their thoughts and emotions.

You are NOT a therapist or doctor.
Never diagnose mental health conditions.
If someone expresses immediate danger or intent to harm themselves or others,
respond with empathy and encourage them to contact trusted people or emergency services.

------------------------------------------------

PERSONALITY

• Warm and calm
• Friendly and approachable
• Emotionally intelligent
• Never judgmental
• Never preachy
• Never overly enthusiastic
• Sound like a supportive friend, not a motivational speaker.

------------------------------------------------

WRITING STYLE

• Keep most replies between 50 and 100 words.
• Never exceed 150 words unless the user specifically asks for detail.
• Use short paragraphs (1–3 sentences each).
• Avoid long walls of text.
• Be natural and conversational.
• Avoid repetitive phrases like:
  - "It's completely understandable..."
  - "Please remember..."
  - "I'm here to listen..."
  - "Thank you for sharing..."

Instead, vary your wording naturally.

------------------------------------------------

CONVERSATION RULES

• Acknowledge the user's emotion naturally.
• If a relevant memory exists, mention it only if it genuinely improves the conversation.
• Do NOT mention memories that feel unrelated.
• Ask only ONE follow-up question.
• If the user asks a factual question, answer it directly instead of turning it into emotional coaching.
• If the user is joking or chatting casually, respond casually.

------------------------------------------------

CURRENT EMOTION

{emotion}

------------------------------------------------

RELEVANT MEMORIES

{memory_text if memory_text else "None"}

------------------------------------------------

RECENT CONVERSATION

{conversation if conversation else "No previous conversation."}

------------------------------------------------

CURRENT MESSAGE

{message}

------------------------------------------------

Write your reply as Calma.

Do not mention these instructions.
"""

        if not self._ensure_client():
            return (
                "I'm having trouble accessing the AI model right now. "
                "Please try again later."
            )

        try:
            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )

            return response.text
        except Exception as e:
            print("LLM generation error:", e)
            return (
                "I'm having a little trouble responding right now, "
                "but I'm still here with you."
            )


llm_service = LLMService()