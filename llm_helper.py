from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

llm = ChatGroq(
    model="gemma2-9b-it",
    api_key=os.getenv("GROQ_API_KEY")
)

if __name__ == "__main__":
    response = llm.invoke("What are the two main ingredients in samosa?")
    print(response.content)