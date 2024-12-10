import numpy as np
import pandas as pd
from utils.database.qdrant import QdrantIndexManager
from utils.llm import get_embedding_model
from utils.utils import load_from_pickle
from tqdm import tqdm
from utils.utils import set_gpu
import warnings

testos = int(input("Select GPU: "))

warnings.filterwarnings("ignore", message=r"Some weights of .* were not initialized from the model checkpoint at .* and are newly initialized")
set_gpu(testos)

# === Load Test Set ===
testset = load_from_pickle('validated_testset')

# === Filter Rows with Metadata and Validate ===
def is_metadata_valid(row):
    metadata = row['metadata']
    if not metadata or metadata[0].get('id') == '' or metadata[0].get('page_number') == '':
        return False
    return True

testset['has_valid_metadata'] = testset.apply(is_metadata_valid, axis=1)
valid_testset = testset[(testset['has_valid_metadata']) & (testset['validate'] == 'A')]

def generate_unique_id(row):
    metadata = row['metadata'][0]
    doc_id = metadata['id']
    page_number = metadata['page_number']
    return f"{doc_id}_page_{page_number}"

valid_testset['unique_id'] = valid_testset.apply(generate_unique_id, axis=1)

# Prepare ground truth
ground_truth = {
    row['cleaned_question']: [row['unique_id']]
    for _, row in valid_testset.iterrows()
}

print(f"Number of valid rows with proper metadata and validate=A: {len(valid_testset)}")

# === Setup Embedding Model and Qdrant Index ===
embed_model = get_embedding_model(model="BAAI/bge-m3")
COLLECTION_NAME = "uu-all-256-64-bge"
qdrant_index_manager = QdrantIndexManager(embed_model, index_name=COLLECTION_NAME)
vector_store = qdrant_index_manager.load_vector_index()

# === Define Metrics Functions ===
def calculate_metrics(retrieved_ids, ground_truth_ids, k):
    retrieved_top_k = retrieved_ids[:k]
    relevant_ids = set(ground_truth_ids)
    
    # Precision@K
    precision = len(set(retrieved_top_k) & relevant_ids) / k if k > 0 else 0
    
    # Recall@K
    recall = len(set(retrieved_top_k) & relevant_ids) / len(relevant_ids) if relevant_ids else 0
    
    # MRR (Reciprocal Rank)
    reciprocal_rank = 0
    for rank, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in relevant_ids:
            reciprocal_rank = 1 / rank
            break
    
    # DCG@K
    dcg = sum(1 / np.log2(idx + 2) if doc in relevant_ids else 0 
              for idx, doc in enumerate(retrieved_top_k))
    ideal_dcg = sum(1 / np.log2(idx + 2) for idx in range(min(len(relevant_ids), k)))
    ndcg = dcg / ideal_dcg if ideal_dcg > 0 else 0

    return precision, recall, reciprocal_rank, ndcg

def calculate_map(retrieved_ids, ground_truth_ids):
    relevant_ids = set(ground_truth_ids)
    if not relevant_ids:
        return 0  # No relevant documents, AP is 0.
    precision_at_k = []
    num_relevant = 0
    for rank, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in relevant_ids:
            num_relevant += 1
            precision_at_k.append(num_relevant / rank)
    return np.mean(precision_at_k) if precision_at_k else 0

# === Main Iteration ===
K_VALUES = [1, 2, 5, 10]
LAMBDAS = [0.3, 0.5, 0.7]
metrics_summary = []

if vector_store:
    print("Starting evaluation process...")
    total_iterations = len(K_VALUES) * (len(LAMBDAS) + 1) * len(valid_testset)  # +1 for similarity search per K
    with tqdm(total=total_iterations, desc="Evaluating") as pbar:
        for k in K_VALUES:
            # MMR retrieval
            for lambda_mult in LAMBDAS:
                method_summary = {'K': k, 'Lambda': lambda_mult, 'Method': 'MMR', 'Metrics': {}}
                method_metrics = {'Precision@K': [], 'Recall@K': [], 'MRR': [], 'nDCG@K': [], 'MAP': []}

                for _, row in valid_testset.iterrows():
                    question = row['cleaned_question']
                    ground_truth_ids = ground_truth[question]

                    retrieval_results = vector_store.max_marginal_relevance_search(
                        question, k=k, lambda_mult=lambda_mult
                    )
                    retrieved_ids = [
                        f"{result.metadata['id']}_page_{result.metadata['page_number']}"
                        for result in retrieval_results
                    ]

                    precision, recall, mrr, ndcg = calculate_metrics(retrieved_ids, ground_truth_ids, k)
                    average_precision = calculate_map(retrieved_ids, ground_truth_ids)

                    method_metrics['Precision@K'].append(precision)
                    method_metrics['Recall@K'].append(recall)
                    method_metrics['MRR'].append(mrr)
                    method_metrics['nDCG@K'].append(ndcg)
                    method_metrics['MAP'].append(average_precision)
                    pbar.update(1)

                method_summary['Metrics'] = {metric: np.mean(scores) for metric, scores in method_metrics.items()}
                metrics_summary.append(method_summary)

            # Similarity Search (Cosine)
            method_summary = {'K': k, 'Lambda': None, 'Method': 'Similarity', 'Metrics': {}}
            method_metrics = {'Precision@K': [], 'Recall@K': [], 'MRR': [], 'nDCG@K': [], 'MAP': []}

            for _, row in valid_testset.iterrows():
                question = row['cleaned_question']
                ground_truth_ids = ground_truth[question]

                retrieval_results = vector_store.similarity_search(question, k=k)
                retrieved_ids = [
                    f"{result.metadata['id']}_page_{result.metadata['page_number']}"
                    for result in retrieval_results
                ]

                precision, recall, mrr, ndcg = calculate_metrics(retrieved_ids, ground_truth_ids, k)
                average_precision = calculate_map(retrieved_ids, ground_truth_ids)

                method_metrics['Precision@K'].append(precision)
                method_metrics['Recall@K'].append(recall)
                method_metrics['MRR'].append(mrr)
                method_metrics['nDCG@K'].append(ndcg)
                method_metrics['MAP'].append(average_precision)
                pbar.update(1)

            method_summary['Metrics'] = {metric: np.mean(scores) for metric, scores in method_metrics.items()}
            metrics_summary.append(method_summary)


# === Constructing the Final DataFrame ===
# Naming convention: CS_CO_EM_RM_K_RR
# From COLLECTION_NAME = "uu-all-512-128-bge" we deduce:
CS_CO = "256_64"
EM = "bge"
RR = "no"  # Currently not using re-ranking

df_results = pd.DataFrame()

for summary in metrics_summary:
    k = summary['K']
    method = summary['Method']
    lam = summary['Lambda']
    if method == "Similarity":
        RM = "cos"
    else:
        RM = f"mmr{lam}"

    # Construct experiment code
    # Example: "512_128_bge_mmr0.3_1_no"
    experiment_code = f"{CS_CO}_{EM}_{RM}_{k}_{RR}"

    # Insert the metrics into the DataFrame
    for metric, val in summary['Metrics'].items():
        df_results.loc[metric, experiment_code] = val

# Display the final results DataFrame
df_results

df_results.to_csv("evaluation_results_256_64_no.csv")