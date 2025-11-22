from google.genai import Client
from config import Config

def list_models():
    client = Client(api_key=Config.GOOGLE_API_KEY)

    print("\n📌 Available Gemini Models:\n")
    models = client.models.list()

    for model in models:
        print(f"- {model.name}")

if __name__ == "__main__":
    list_models()
