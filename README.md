# MedBot AI: Healthcare Education Chatbot for India 🇮🇳

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)
![Twilio](https://img.shields.io/badge/Twilio-F22F46?style=for-the-badge&logo=twilio&logoColor=white)

A proof-of-concept AI chatbot designed to provide accessible healthcare information to rural and semi-urban populations in India, bridging the information gap with modern language models.

## 🎯 About The Project

This project is an AI-powered chatbot created to educate users on essential health topics. Leveraging a powerful language model running locally, it provides conversational answers to questions about preventive healthcare, disease symptoms, and vaccination schedules. The backend is a high-performance FastAPI server, and it's integrated with Twilio for WhatsApp functionality.

## ✨ Key Features

* **Conversational Q&A:** Ask health-related questions in natural language.
* **Core Knowledge Areas:**
    * Preventive healthcare practices
    * Symptoms of common diseases
    * Indian vaccination schedules
* **Multi-Platform:** Accessible via a web interface and directly through WhatsApp.
* **Locally Run Model:** Powered by the `BioMistral-7B` model running via `llama.cpp` for privacy and offline capabilities.

## 🛠️ Tech Stack

* **Language:** Python
* **AI Model:** [BioMistral-7B](https://huggingface.co/BioMistral/BioMistral-7B)
* **Model Execution:** `llama.cpp`
* **Backend Framework:** FastAPI
* **Messaging API:** Twilio
* **Translation Model:** Meta NLLB
* **Translation Model Execution:** `transformers pytorch`


## 🚀 Getting Started

Follow these instructions to get a local copy up and running for development and testing.

### Prerequisites

* Python 3.10+
* Git
* A pre-downloaded GGUF model file for BioMistral-7B, change the model_path variable in sns.py and main.py to the model you're using

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/Shivansh-Game/Web-based-Medical-AI-chatbot.git](https://github.com/Shivansh-Game/Web-based-Medical-AI-chatbot.git)
    cd Web-based-Medical-AI-chatbot
    ```
2.  **Create and activate a virtual environment:**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
4.  **Set up environment variables:**
    * Create a `.env` file in the root directory.
    * Add your Twilio credentials if you plan to use the WhatsApp functionality:
        ```env
        TWILIO_ACCOUNT_SID=your_sid
        TWILIO_AUTH_TOKEN=your_token
        ```

5.  **Run the application:**
    ```sh
    uvicorn main:app --reload -- port 8000
    ```
    The application will be available at `http://127.0.0.1:8000`.

## 🔮 Future Work

* [ ] Deploy the application to a cloud service like AWS EC2.
* [ ] Fine-tune the model on a custom dataset of Indian healthcare FAQs for higher accuracy.
* [ ] Implement a proper database (e.g., MySQL or PostgreSQL) to store conversation history.
* [ ] Expand the knowledge base to include more specialized health topics.

## 👤 Author

**Shivansh** - [Shivansh-Game](https://github.com/Shivansh-Game)
