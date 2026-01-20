from flask import Flask, request, jsonify, render_template
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import pipeline
import os

app = Flask(__name__, template_folder="../templates", static_folder="../static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "db")

# Load embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load vector database
db = Chroma(
    persist_directory=DB_PATH,
    embedding_function=embeddings
)

# Load LLM
llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    max_length=256
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question")

    if not user_question:
        return jsonify({"answer": "Please enter a question."})

    # Retrieve documents
    docs = db.similarity_search(user_question, k=3)

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
    Answer the question using the context below.

    Context:
    {context}

    Question:
    {user_question}
    """

    response = llm(prompt)[0]["generated_text"]

    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(debug=True)
