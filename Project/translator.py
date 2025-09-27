import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class NLLBTranslator:

    LANG_CODE_MAP = {
        'en': 'eng_Latn', 'hi': 'hin_Deva', 'bn': 'ben_Beng',
        'ta': 'tam_Taml', 'te': 'tel_Telu', 'ur': 'urd_Arab',
        'gu': 'guj_Gujr', 'mr': 'mar_Deva', 'pa': 'pan_Guru',
        'kn': 'kan_Knda', 'ml': 'mal_Mlym',
    }

    def __init__(self, model_name="facebook/nllb-200-distilled-600M"):
        
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        self.tokenizer = None
        self.model = None
        self._load_model()

    def _load_model(self):

        print(f"Loading model '{self.model_name}'...")
        print(f"Loading model '{self.model_name}' directly onto device: {self.device}...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            

            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                self.model_name,
                device_map="auto"
            )
            
            self.model.eval()
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def get_supported_languages(self):
        """Returns the dictionary of supported language codes."""
        return self.LANG_CODE_MAP

    def translate(self, text: str, src_lang: str, tgt_lang: str) -> str:
        
        if not self.model or not self.tokenizer:
            return "Error: Model is not loaded."

        src_code = self.LANG_CODE_MAP.get(src_lang)
        tgt_code = self.LANG_CODE_MAP.get(tgt_lang)

        if not src_code or not tgt_code:
            valid_codes = ", ".join(self.LANG_CODE_MAP.keys())
            return f"Error: Invalid language code. Use one of: {valid_codes}"

        with torch.no_grad():
            try:
                self.tokenizer.src_lang = src_code
                encoded_text = self.tokenizer(text, return_tensors="pt").to(self.device)

                target_lang_id = self.tokenizer.convert_tokens_to_ids(tgt_code)

                generated_tokens = self.model.generate(
                    **encoded_text,
                    forced_bos_token_id=target_lang_id,
                    max_length=256
                )
                
                translation = self.tokenizer.batch_decode(
                    generated_tokens, skip_special_tokens=True
                )[0]
                return translation
            except Exception as e:
                return f"Error during translation: {e}"

# --- FOR TESTING --- #
# This block will only run when you execute this file
if __name__ == "__main__":
    translator = NLLBTranslator()

    if translator.model:
        source_lang = "hi" 
        english_text = "आपका नाम क्या है?"
        
        print(f"\nTranslating from '{source_lang}' to 'en'...")
        english_translation = translator.translate(english_text, src_lang=source_lang, tgt_lang='en')
        print(f"Original ({source_lang}): {english_text}")
        print(f"Translated (en): {english_translation}\n")
        
        print(f"Translating from 'en' back to '{source_lang}'...")
        hindi_translation = translator.translate(english_translation, src_lang='en', tgt_lang=source_lang)
        print(f"Original (en): {english_translation}")
        print(f"Translated ({source_lang}): {hindi_translation}")
