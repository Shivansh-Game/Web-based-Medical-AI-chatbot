from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import MedicalChatbot

# Port must be 8000 for the program to run
# Run By running this python file and then enter uvicorn main:app --port 8000 --reload in the terminal

app = FastAPI()

model_path = "Models\\BioMistral-7B.Q4_K_M.gguf"
bot = MedicalChatbot(model_path=model_path, n_threads=2)


# Lets the backend and frontend communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Input format (JSON)
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    user_message = request.message.lower()

    bot_reply = bot.ask(user_message)

    return {"reply": bot_reply}

