from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from utils.chain.rag import create_combined_answer_chain
from utils.config import get_config
from utils.database.qdrant import QdrantIndexManager
from utils.llm import get_embedding_model, get_llm
from utils.retriever.uu.embedding_uu import get_embedding_uu
from utils.retriever.uu.graph_uu import get_graph_uu

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str
    chat_history: str = ""

@asynccontextmanager
async def lifespan(app: FastAPI):
    global llm, retriever_uu, graph_chain, chain_quality

    llm = get_llm("nvidia-llama3.1")
    embed_model = get_embedding_model("BAAI/bge-m3")

    vector_store = QdrantIndexManager(embed_model=embed_model, index_name="uu").load_vector_index()
    retriever_uu = get_embedding_uu(vector_store=vector_store, llm=llm, embed_model=embed_model, with_self_query=False)

    config = get_config()
    graph_chain = get_graph_uu(llm=llm, config=config)

    chain_quality = create_combined_answer_chain(
        retriever_uu=retriever_uu,
        graph_chain=graph_chain,
        llm=llm
    )

    yield


app = FastAPI(lifespan=lifespan)

@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        result = chain_quality.invoke({
            "question": request.question,
            "chat_history": request.chat_history
        })

        return {"answer": result['answer']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
