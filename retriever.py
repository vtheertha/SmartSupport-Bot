import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()

class Retriever:
    def __init__(self):
        """Initialize FAISS index with Google Generative AI embeddings."""
        self.docs_path = "docs/twitter_faq.txt"  # Path to your dataset file
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

        # Load existing FAISS index or create one
        if os.path.exists("faiss_index"):
            print("Loading existing FAISS index...")
            self.index, self.documents = self.load_faiss_index()
        else:
            print("FAISS index not found! Creating a new one...")
            self.index, self.documents = self.create_faiss_index()

    def load_faiss_index(self):
        """Loads FAISS index if it exists."""
        try:
            vectorstore = FAISS.load_local(
                "faiss_index", 
                self.embeddings, 
                allow_dangerous_deserialization=True  # Enable safe deserialization
            )
            return vectorstore, vectorstore.index_to_docstore_id
        except Exception as e:
            raise RuntimeError(f"Error loading FAISS index: {e}")


    def create_faiss_index(self):
        """Creates FAISS index from the Twitter FAQ text file."""
        if not os.path.exists(self.docs_path):
            raise FileNotFoundError(f"Dataset file '{self.docs_path}' not found.")

        # Read the entire text file
        with open(self.docs_path, "r", encoding="utf-8") as file:
            text_data = file.read()

        if not text_data.strip():
            raise ValueError("Dataset file is empty! Please add FAQs.")

        print("Loaded dataset. Splitting into chunks...")

        # Split text into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        split_docs = text_splitter.create_documents([text_data])  # Convert text to documents

        if not split_docs:
            raise ValueError("Text splitting failed, resulting in an empty list.")

        print(f"Generated {len(split_docs)} text chunks.")

        # Create FAISS index
        vectorstore = FAISS.from_documents(split_docs, self.embeddings)
        vectorstore.save_local("faiss_index")

        return vectorstore, vectorstore.index_to_docstore_id

    def retrieve_documents(self, query, top_k=3):
        """Finds the top_k most relevant FAQ entries using FAISS."""
        docs = self.index.similarity_search(query, k=top_k)
        return [doc.page_content for doc in docs] if docs else ["No relevant FAQs found."]











