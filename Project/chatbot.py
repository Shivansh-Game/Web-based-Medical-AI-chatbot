from llama_cpp import Llama

'''
Disclaimer: The first output from the bot takes a lot longer than subsequent ones.
'''



class MedicalChatbot:
    def __init__(self, model_path, n_threads=2):
        self.llm = Llama(model_path=model_path, n_threads=n_threads, verbose=False)
        self.conversation_history = []

    def ask(self, user_input):
        
        max_context_tokens = 512

        system_prompt = (
            "You are 'Baymax', a helpful and knowledgeable AI medical assistant for rural and semi-urban Indian communities. "
            "Your primary goal is to provide clear, concise, and helpful information about preventive healthcare, disease symptoms, and vaccination schedules. "
            "You must make judgments purely based on the information you receive, as users do not have access to visual tools.\n\n"
            "CRITICAL SAFETY RULE: You are an informational tool, NOT a doctor. You must NEVER give a diagnosis or prescribe medicine. "
            "For any query that asks for a diagnosis, treatment, or seems like a medical emergency, you MUST decline to answer and strongly advise the user to consult a real doctor or go to the nearest hospital immediately.\n\n"
            "RESPONSE STYLE: Avoid repeating generic disclaimers like 'I am not a doctor' in every message. Use simple, to-the-point language.\n\n"
            "CONTEXT RULE: When provided with specific CONTEXT, base your answer STRICTLY on that information to ensure accuracy."
        )

        # Builds history
        managed_history = []
        current_token_count = len(self.llm.tokenize(system_prompt.encode('utf-8')))
        

        for turn in reversed(self.conversation_history):
            turn_text = f"Patient: {turn['user']}\nAssistant: {turn['bot']}\n"
            turn_tokens = self.llm.tokenize(turn_text.encode('utf-8'))

            # Checks if next prompt add will go over the limit
            if current_token_count + len(turn_tokens) <= max_context_tokens:
                managed_history.insert(0, turn_text) 
                current_token_count += len(turn_tokens)
            else:
                break

        history_string = "".join(managed_history)
        final_prompt = f"{system_prompt}\n\n{history_string}Patient: {user_input}\nAssistant:"
        

        response = self.llm(
            prompt=final_prompt,
            max_tokens=200,
            temperature=0.5,
            stop=["\nPatient:", "\nAssistant:"]
        )

        bot_reply = response['choices'][0]['text'].strip()

        # Updates the full conversation history
        self.conversation_history.append({"user": user_input, "bot": bot_reply})
        # Trims history
        if len(self.conversation_history) > 20:
            self.conversation_history.pop(0)

        return bot_reply
