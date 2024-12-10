import os
from utils.llm import get_embedding_model
from utils.utils import load_from_pickle
from utils.document.split import document_splitter
from utils.database.qdrant import QdrantIndexManager

def clean_document_content(content):
    """
    Cleans the document content by removing unwanted characters.
    """
    return content.replace('\x00', '')

def split_documents(documents, chunk_sizes, chunk_overlaps):
    """
    Splits documents into chunks based on specified chunk sizes and overlaps.
    Preserves metadata in the process.
    """
    all_splits = []
    for size in chunk_sizes:
        for overlap in chunk_overlaps:
            if overlap < size:  # Valid overlap
                print(f"Splitting documents with chunk size {size} and overlap {overlap}...")
                splits = document_splitter(docs=documents, chunk_size=size, chunk_overlap=overlap)
                for split in splits:
                    split.page_content = clean_document_content(split.page_content)
                all_splits.append((size, overlap, splits))
    return all_splits

def configure_qdrant_params(vector_size, distance_metric, use_hnsw=False):
    """
    Configures Qdrant index parameters for storing embeddings.
    Includes optional HNSW configuration.
    """
    params = {
        "vectors": {
            "size": vector_size,
            "distance": distance_metric
        },
        "shard_number": 1,
        "on_disk_payload": True
    }
    if use_hnsw:
        params["hnsw_config"] = {
            "m": 16,
            "ef_construct": 200,
            "ef": 50,
            "full_scan_threshold": 10000
        }
    print(f"Configuring Qdrant with vector size={vector_size}, distance={distance_metric}, HNSW={use_hnsw}...")
    return params

def store_embeddings(embed_model, splits, index_name, use_hnsw=False):
    """
    Stores embeddings into Qdrant, handling metadata and optional HNSW configuration.
    """
    qdrant_index_manager = QdrantIndexManager(embed_model, index_name=index_name)

    # Configure Qdrant index parameters
    vector_size = 1024  # Adjust based on embedding model output size
    params = configure_qdrant_params(vector_size, "Cosine", use_hnsw)

    # Create index in Qdrant
    if not qdrant_index_manager.check_index_exists():
        print(f"Creating index '{index_name}' in Qdrant...")
        qdrant_index_manager.create_index(**params)

    # Store embeddings with metadata
    for size, overlap, chunks in splits:
        print(f"Storing embeddings for chunk size {size} and overlap {overlap}...")
        qdrant_index_manager.store_vector_index(chunks, batch_size=20000)

    return qdrant_index_manager

def perform_query(qdrant_manager, query, k=5):
    """
    Performs a similarity search query on the stored embeddings in Qdrant.
    """
    vector_store = qdrant_manager.load_vector_index()
    if vector_store:
        results = vector_store.similarity_search(query, k=k)
        for result in results:
            print("Page Content:", result.page_content)
            print("Metadata:", result.metadata)
            print("=" * 50)
    else:
        print("Vector store not found.")


# Example usage
if __name__ == "__main__":
    # Load documents
    all_documents = load_from_pickle("all_documents")

    # Define chunk sizes and overlaps
    chunk_sizes = [128, 256, 512, 1024]
    chunk_overlaps = [0, 64, 128, 256, 512]

    # Split documents
    splits = split_documents(all_documents, chunk_sizes, chunk_overlaps)

    # Embedding model
    embed_model_bge = get_embedding_model(model="BAAI/bge-m3")

    # Store embeddings (without HNSW)
    store_embeddings(embed_model_bge, splits, index_name="dense-bge-m3", use_hnsw=False)

    # Store embeddings (with HNSW)
    store_embeddings(embed_model_bge, splits, index_name="hnsw-bge-m3", use_hnsw=True)
