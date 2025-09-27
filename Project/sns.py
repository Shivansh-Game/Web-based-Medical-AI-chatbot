from fastapi import FastAPI, Request, Response
import twilio
from twilio.twiml.messaging_response import MessagingResponse
from chatbot import MedicalChatbot
from translator import NLLBTranslator


"""
THIS CURRENTLY WORKs INCONSISTENTLY, IT IS NOT DUE TO A PROBLEM WITH THE PROGRAM BUT RATHER THE HARDWARE IT'S RUNNING ON.

DETAILS: The twilio webhook that is trying to get the output from our bot expires within 15 seconds (seems to be a HTTP limit), but on slower hardware 
it can take upto 30 seconds to generate an output leading to an output being generated but not being caught by the twilio webhook.
This means the output is generated but the user does not recieve it. The problem can simply be solved using a faster system, The website and hosting
the bot locally still work perfectly fine.
""" 


# py -3.13 -m uvicorn sns:app --port 7000 --reload
# then run ngrok http 7000
# then put the forwarding link into the sandbox from twilio

app = FastAPI()

print("Initializing models for WhatsApp bot...")

model_path = "Models\\BioMistral-7B.Q3_K_S.gguf"
bot = MedicalChatbot(model_path=model_path, n_threads=2)

translator = NLLBTranslator()
print("All models initialized successfully.")



# This dictionary will store the chosen language for each number. A key:value pair would look like
# Key: 'whatsapp:+xxxxxxxxx'
# Value: {'language': 'en'}
conversation_state = {}

supported_langs = translator.get_supported_languages()

def get_language_list_text():

    lang_options = [
        f"• Send '{code}' for {name.split('_')[0].title()}" 
        for code, name in supported_langs.items() if code != 'en'
    ]
    return "\n".join(lang_options)


@app.post("/whatsapp")
async def whatsapp_reply(request: Request):


    form_data = await request.form()
    incoming_msg = form_data.get('Body', '').strip().lower()
    sender_number = form_data.get('From', '')

    resp = MessagingResponse()


    # If it's a new number give them the introduction
    if sender_number not in conversation_state:
        conversation_state[sender_number] = {"language": "en"}
        
        welcome_text = (
            "Hello! I am Baymax, your personal healthcare companion. How can I help you today?\n\n"
            "To chat in another language, please reply with one of the following codes:"
        )
        language_list = get_language_list_text()
        full_message = f"{welcome_text}\n{language_list}"
        
        resp.message(full_message)
        return Response(content=str(resp), media_type="application/xml")

    # gets current lang
    current_lang = conversation_state[sender_number]["language"]


    # Check if lang code was the input
    if incoming_msg in supported_langs:
        new_lang = incoming_msg
        conversation_state[sender_number]["language"] = new_lang
        
        lang_full_name = supported_langs[new_lang].split('_')[0].title()
        confirmation_text_en = f"Language has been set to {lang_full_name}. How can I assist you?"
        
        final_reply = translator.translate(confirmation_text_en, src_lang='en', tgt_lang=new_lang)
        
        resp.message(final_reply)
        return Response(content=str(resp), media_type="application/xml")


    final_reply = ""
    if current_lang != "en":
        
        print("Got to trans")
        message_for_bot = translator.translate(incoming_msg, src_lang=current_lang, tgt_lang='en')

        print("Asked bot")
        bot_reply_en = bot.ask(message_for_bot)

        print("got answer")
        final_reply = translator.translate(bot_reply_en, src_lang='en', tgt_lang=current_lang)
    else:
        print("waiting for bot")
        print(incoming_msg)
        final_reply = bot.ask(incoming_msg)

    print("Sent message")
    print(final_reply)
    resp.message(final_reply)

    # response is sent to twilio
    print(str(resp))
    return Response(content=str(resp), media_type="application/xml")
