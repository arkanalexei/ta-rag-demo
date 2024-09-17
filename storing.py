
from utils.database.qdrant import QdrantIndexManager
from utils.document.split import document_splitter
from utils.llm import get_embedding_model
from utils.utils import load_from_pickle


def clean_document_content(content):
    return content.replace('\x00', '')  # Remove NUL characters
  

embed_model = get_embedding_model(model="BAAI/bge-m3")
all_documents = load_from_pickle("all_documents")


all_splits = document_splitter(docs=all_documents)
all_splits_sorted = sorted(all_splits, key=lambda x: (x.metadata['id'], x.metadata.get('page_number', '0')))
for split in all_splits_sorted:
    split.page_content = clean_document_content(split.page_content)


qdrant_index_manager = QdrantIndexManager(embed_model, index_name="uu")

qdrant_index_manager.store_vector_index(all_splits, batch_size=200)

vector_store = qdrant_index_manager.load_vector_index()

if vector_store:
    results = vector_store.similarity_search("Apa itu capital Jawa Barat?", k=50)
    for result in results:
        print(result.page_content, result.metadata)
        
