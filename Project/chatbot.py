from llama_cpp import Llama

class MedicalChatbot:
    def __init__(self, model_path, n_threads=2):
        self.llm = Llama(model_path=model_path, n_threads=n_threads, verbose=False)
        self.conversation_history = []

    def ask(self, user_input):
        
        prompt = (
            "You are a helpful and knowledgeable medical assistant who will not have access"
            "to any visual indications and must make judgements purely based on the information, avoid repeating disclaimers like 'I am not a doctor'. Use concise, helpful language."
            "you receive from the patient.\n"
        )
        for turn in self.conversation_history:
            prompt += f"Patient: {turn['user']}\nAssistant: {turn['bot']}\n"
        prompt += f"Patient: {user_input}\nAssistant:"

        # Generates a response
        response = self.llm(
            prompt=prompt,
            max_tokens=150,
            temperature=0.5,
            stop=["\nPatient:", "\nAssistant:"]
        )

        bot_reply = response['choices'][0]['text'].strip()

        # History keeper
        self.conversation_history.append({"user": user_input, "bot": bot_reply})

        return bot_reply
