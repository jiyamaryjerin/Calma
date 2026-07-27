from fastapi import FastAPI
from pydantic import BaseModel
from services.kokoro_service import kokoro_service
from fastapi.staticfiles import StaticFiles
from services.emotion_service import emotion_service
from services.memory_filter import memory_filter
from services.memory_service import memory_service
from services.memory_extractor import memory_extractor
from services.vector_memory_service import vector_memory_service
from services.conversation_service import conversation_service
from services.llm_service import llm_service

app = FastAPI(title="Calma Backend")
app.mount("/audio", StaticFiles(directory="audio"), name="audio")

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    emotion: str
    confidence: float
    audio_url: str | None = None


@app.get("/")
def home():
    return {
        "message": "Calma Backend Running 🌿"
    }


@app.get("/memory")
def memory():
    return {
        "memories": memory_service.get_memories()
    }


@app.get("/history")
def history():
    return {
        "history": conversation_service.get_history()
    }

@app.post("/reset")
def reset():

    conversation_service.clear()
    memory_service.clear()
    vector_memory_service.clear()

    return {
        "message": "Calma reset successfully 🌿"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    # ---------------------------------
    # Save user message
    # ---------------------------------
    conversation_service.add_user_message(request.message)

    # ---------------------------------
    # Retrieve relevant semantic memories
    # ---------------------------------
    results = vector_memory_service.search_excluding_exact_match(
        request.message,
        n_results=3
    )

    print("\n===== CHROMADB RESULTS =====")
    print(results["documents"])
    print("============================\n")

    remembered_memories = []

    if (
        results["documents"]
        and len(results["documents"]) > 0
    ):
        remembered_memories = results["documents"][0]

    # ---------------------------------
    # Detect emotion
    # ---------------------------------
    emotion = emotion_service.detect_emotion(
        request.message
    )

    emotion_name = emotion["emotion"]

    # ---------------------------------
    # Recent conversation
    # ---------------------------------
    history = conversation_service.get_history()

    print("\n===== CONVERSATION HISTORY =====")
    for msg in history:
        print(f"{msg['role']}: {msg['content']}")
    print("================================\n")

    # ---------------------------------
    # Generate AI response
    # ---------------------------------
    try:

        response = llm_service.generate_response(
            message=request.message,
            emotion=emotion_name,
            memories=remembered_memories,
            history=history,
        )

    except Exception as e:

        print(e)

        response = (
            "I'm having a little trouble responding right now, "
            "but I'm still here with you. "
            "Could you try sending that again?"
        )
        # ---------------------------------
    # Generate voice response
    # ---------------------------------
    try:

        audio_url = kokoro_service.generate_audio(
            response
        )

    except Exception as e:

        print("Kokoro Error:", e)
        audio_url = None
    # ---------------------------------
    # Save assistant response
    # ---------------------------------
    conversation_service.add_assistant_message(response)

    # ---------------------------------
    # Store meaningful memories
    # ---------------------------------
    if memory_filter.should_store(request.message):

        extracted_memory = memory_extractor.extract(
            request.message
        )

        memory = memory_service.add_memory(
            extracted_memory
        )

        vector_memory_service.add_memory(
            memory
        )

    return ChatResponse(
        response=response,
        emotion=emotion_name,
        confidence=emotion["confidence"],
        audio_url=audio_url,
    )