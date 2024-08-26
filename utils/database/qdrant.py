import os
import time
from abc import ABC, abstractmethod

from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient


class VectorIndexManager(ABC):
    def __init__(self, embed_model, index_name="uu"):
        self.embed_model = embed_model
        self.index_name = index_name
        self.vector_store = None

    @abstractmethod
    def delete_index(self):
        pass

    @abstractmethod
    def store_vector_index(self, docs=None, delete=False):
        pass

    @abstractmethod
    def load_vector_index(self):
        pass
    
class QdrantIndexManager(VectorIndexManager):
    def __init__(self, embed_model: Embeddings, index_name="uu", url="http://localhost:6333"):
        super().__init__(embed_model, index_name)
        self.url = url
        self.client = QdrantClient(url=url)
        self.base_log_path = './database/store_logs'
        self.log_path = os.path.join(self.base_log_path, f'start_store_idx_{self.index_name}.txt')

    def delete_index(self):
        try:
            self.client.delete_collection(collection_name=self.index_name)
            print(f"Deleted index '{self.index_name}'.")
            if os.path.exists(self.log_path):
                os.remove(self.log_path)
        except Exception as e:
            print(f"Error deleting index: {e}")

    def store_vector_index(self, docs, batch_size=200):
        # Determine the start index from log file
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r') as f:
                start_split_idx = int(f.read())
            print(f"Start loading from idx: {start_split_idx}")
        else:
            with open(self.log_path, 'w') as f:
                f.write(str(0))
            start_split_idx = 0

        # Load or create the vector store in Qdrant
        if start_split_idx < batch_size:
            self.vector_store = Qdrant.from_texts(
                texts=[doc.page_content for doc in docs[0:batch_size]],
                embedding=self.embed_model,
                metadatas=[doc.metadata for doc in docs[0:batch_size]],
                collection_name=self.index_name,
                url=self.url
            )
            time.sleep(4)

            last_split_idx = min(batch_size, len(docs))
            with open(self.log_path, 'w') as f:
                f.write(str(last_split_idx))
            print(f"Loaded 1-{last_split_idx} documents")
            start_split_idx = batch_size
        else:
            self.vector_store = Qdrant.from_existing_collection(
                collection_name=self.index_name,
                embedding=self.embed_model,
                url=self.url
            )

        # Add documents in batches
        for i in range(start_split_idx, len(docs), batch_size):
            batch_docs = docs[i:i+batch_size]
            self.vector_store.add_texts(
                texts=[doc.page_content for doc in batch_docs],
                metadatas=[doc.metadata for doc in batch_docs]
            )
            time.sleep(4)
            last_split_idx = min(i+batch_size, len(docs))
            with open(self.log_path, 'w') as f:
                f.write(str(last_split_idx))
            print(f"Loaded {i+1}-{last_split_idx} documents")

    def load_vector_index(self):
        try:
            # Load the existing vector index from Qdrant
            self.vector_store = Qdrant.from_existing_collection(
                path=None,
                collection_name=self.index_name,
                embedding=self.embed_model,
                url=self.url
            )
            print(f"Loaded index '{self.index_name}'.")
            return self.vector_store
        except Exception as e:
            print(f"Error loading index: {e}")
            return None