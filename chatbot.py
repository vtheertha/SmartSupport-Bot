import os
import google.generativeai as genai
from langchain.memory import ConversationBufferMemory
from retriever import Retriever
from dotenv import load_dotenv

load_dotenv()  # Load API keys

class Chatbot:
    def __init__(self):
        """Initialize Gemini API & RAG retriever"""
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Load API Key
        self.model = genai.GenerativeModel("gemini-1.5-flash")  # Use Gemini-Pro
        self.retriever = Retriever()
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def get_response(self, user_query):
        """Retrieve relevant context & generate response with Gemini"""
        retrieved_docs = self.retriever.retrieve_documents(user_query)
        retrieved_context = "\n".join(retrieved_docs)

        # Construct conversation history
        chat_history = self.memory.load_memory_variables({})["chat_history"]
        conversation_context = f"Previous Chat:\n{chat_history}\n\nUser: {user_query}\nRelevant Info:\n{retrieved_context}\nAssistant:"

        # Get Gemini response
        gemini_response = self.model.generate_content(conversation_context).text

        # Save chat history
        self.memory.save_context({"User": user_query}, {"Assistant": gemini_response})

        return gemini_response



