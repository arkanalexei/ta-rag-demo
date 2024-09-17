from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.llm import get_llm, get_embedding_model
from utils.database.qdrant import QdrantIndexManager
from utils.retriever.uu.embedding_uu import get_embedding_uu
from utils.retriever.uu.graph_uu import get_graph_uu
from utils.config import get_config
from utils.chain.rag import create_combined_answer_chain

# FastAPI app
app = FastAPI()

# Define a request model
class QuestionRequest(BaseModel):
    question: str
    chat_history: str = ""

# Load models and retrievers at startup
@app.on_event("startup")
def load_resources():
    global llm, retriever_uu, graph_chain, chain_quality

    # Load the LLM and the embedding model
    llm = get_llm("nvidia-llama3.1")
    embed_model = get_embedding_model("BAAI/bge-m3")

    # Initialize the vector store and retriever
    vector_store = QdrantIndexManager(embed_model=embed_model, index_name="uu").load_vector_index()
    retriever_uu = get_embedding_uu(vector_store=vector_store, llm=llm, embed_model=embed_model, with_self_query=False)

    # Load the graph chain
    config = get_config()
    graph_chain = get_graph_uu(llm=llm, config=config)

    # Create the final RAG chain
    chain_quality = create_combined_answer_chain(
        retriever_uu=retriever_uu,
        graph_chain=graph_chain,
        llm=llm
    )

# Define an API endpoint
@app.post("/ask")
def ask_question(request: QuestionRequest):
    print("start ask quuestion")
    try:
        # Invoke the RAG pipeline
        result = chain_quality.invoke({
            "question": request.question,
            "chat_history": request.chat_history
        })

        print("result", result)
        answer = json.dumps(result['answer'], default=str)
        return {"answer": answer}

        # Return the answer from the RAG pipeline
        return {"answer": result['answer']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app with: uvicorn main:app --reload
