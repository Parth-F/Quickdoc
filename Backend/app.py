from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.llms import LlamaCpp
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
import warnings
import os
from get_embedding_function import get_embedding_function

warnings.filterwarnings("ignore")
CHROMA_PATH = "chroma"
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Models", "model.gguf")

PROMPT_TEMPLATE = """
You are a medical professional. Answer the question based only on the following context like a human would. It should consist of paragraph and conversational aspect rather than just a summary. Answer the asked question briefly. Answer in a professional tone:

{context}

---

Answer the question based on the above context: {question}
"""


app = Flask(__name__)
# Configure CORS to allow requests from specific origins in production
cors_origin = os.environ.get('CORS_ORIGIN', '*')
CORS(app, resources={r"/*": {"origins": cors_origin}})

def query_rag(query_text: str):
    try:
        # Prepare the DB.
        embedding_function = get_embedding_function()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

        # Search the DB.
        results = db.similarity_search_with_score(query_text, k=5)

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
        print(prompt)
        
        # Load the LLM directly from the GGUF file
        model = LlamaCpp(
            model_path=MODEL_PATH,
            temperature=0.1,
            max_tokens=1024,
            n_ctx=2048,
            verbose=False
        )
        response_text = model.invoke(prompt)

        sources = [doc.metadata.get("id", None) for doc, _score in results]
        formatted_response = f"{response_text}\n\n\nSources: {sources}"
        print(formatted_response)
        return formatted_response
    except Exception as e:
        print(f"Error in query_rag: {e}")
        return f"Error processing request: {e}"

def query_finetune(prompt: str):
    try:
        # Load the LLM directly
        model = LlamaCpp(
            model_path=MODEL_PATH,
            temperature=0.1,
            max_tokens=1024,
            n_ctx=2048,
            verbose=False
        )
        
        # First check if the query is medical-related
        gatePrompt = f"""
        I will now give you a question. This question should only be related to medical queries or advice. 
        If it is related to medical queries or advice, then reply with 'True' and nothing else. 
        If it's not related to medical info, then just say 'False' and nothing else.
        
        Question: {prompt}
        
        Answer (True/False):
        """
        
        gateResult = model.invoke(gatePrompt).strip()
        
        if gateResult.lower() == "false":
            return "This query is not related to medical field. Please ask related queries."
            
        medicalPrompt = f"""
        You are a medical professional. Answer the following question truthfully and professionally.
        If the question is not related to health, reply that you are a medical professional and cannot answer it.
        
        Question: {prompt}
        
        Answer:
        """
        
        response_text = model.invoke(medicalPrompt)
        print(response_text)
        return response_text
    except Exception as e:
        print(f"Error in query_finetune: {e}")
        return f"Error processing request: {e}"

@app.route('/api/queryRAG', methods=['POST'])
def queryRAG():
    try:
        data = request.get_json()
        query_text = data.get('query_text')
        if not query_text:
            return jsonify({"error": "No query_text provided"}), 400
        
        print(f"Received query: {query_text}")
        response_text = query_rag(query_text)
        return jsonify({"response": response_text})
    except Exception as e:
        print(f"Error in /query endpoint: {e}")
        return jsonify({"error": f"Error processing request: {e}"}), 500
    

@app.route('/api/queryFineTune', methods=['POST'])
def queryFinetune():
    try:
        data = request.get_json()
        query_text = data.get('query_text')
        if not query_text:
            return jsonify({"error": "No query_text provided"}), 400
        
        print(f"Received query: {query_text}")
        response_text = query_finetune(query_text)
        return jsonify({"response": response_text})
    except Exception as e:
        print(f"Error in /query endpoint: {e}")
        return jsonify({"error": f"Error processing request: {e}"}), 500

if __name__ == '__main__':
    # Get port from environment variable or use 5000 as default
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
