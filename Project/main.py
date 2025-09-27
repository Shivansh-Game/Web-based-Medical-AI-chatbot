from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import MedicalChatbot
from translator import NLLBTranslator

# Port must be 8000 for the program to run

# Run By running this python file and then enter py -3.13 -m uvicorn main:app --port 8000 --reload in the terminal

app = FastAPI()

print("Initializing models...")

model_path = "Models\\BioMistral-7B.Q3_K_S.gguf"
bot = MedicalChatbot(model_path=model_path, n_threads=2)


translator = NLLBTranslator()
print("All models initialized successfully.")


# remembers the chosen language.
# defaults to 'en'.
conversation_state = {
    "language": "en"
}

supported_langs = translator.get_supported_languages().keys()
# creates list of lang codes

# Allows the frontend and backend to communicate.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Lets it know we're expecting an input in the format of {'message' : str}
class ChatRequest(BaseModel):
    message: str 

@app.post("/chat")
def chat(request: ChatRequest):
    user_message = request.message.strip()
    current_lang = conversation_state["language"]

    # Check if lang code was the input
    if user_message.lower() in supported_langs:
        new_lang = user_message.lower()
        conversation_state["language"] = new_lang
        
        confirmation_text_en = f"Language has been set to {new_lang}. How can I assist you?"
        final_reply = translator.translate(confirmation_text_en, src_lang='en', tgt_lang=new_lang)
        
        return {"reply": final_reply}

    
    if current_lang != "en":

        print(f"Translating from '{current_lang}' to 'en': \"{user_message}\"")
        message_for_bot = translator.translate(user_message, src_lang=current_lang, tgt_lang='en')
        print(f"Bot receives: \"{message_for_bot}\"")
        

        bot_reply_en = bot.ask(message_for_bot)
        print(f"Bot replies (in English): \"{bot_reply_en}\"")
        

        final_reply = translator.translate(bot_reply_en, src_lang='en', tgt_lang=current_lang)
        print(f"Final translated reply: \"{final_reply}\"")
    else:
        print(f"Processing in English: \"{user_message}\"")
        final_reply = bot.ask(user_message)
        print(f"Bot replies: \"{final_reply}\"")

    return {"reply": final_reply}
