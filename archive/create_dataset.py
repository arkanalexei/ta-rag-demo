import os
import logging
from dotenv import load_dotenv
import nest_asyncio
import pandas as pd
from tqdm import tqdm
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple

from utils.utils import load_from_pickle, save_to_pickle
from utils.llm import get_llm, get_embedding_model

# Setup loggingx
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables and apply nest_asyncio
load_dotenv()
nest_asyncio.apply()

def split_into_batches(input_list, n):
    batch_size = len(input_list) // n
    remainder = len(input_list) % n

    batches = []
    start = 0

    for i in range(n):
        end = start + batch_size + (1 if remainder > 0 else 0)
        batches.append(input_list[start:end])
        start = end
        remainder -= 1

    return batches

def get_last_processed_batch():
    try:
        with open('pickles/progress.log', 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0

def save_progress(batch_num):
    with open('pickles/progress.log', 'w') as f:
        f.write(str(batch_num))

def main():
    # Load documents
    all_documents = load_from_pickle('ya_allah')
    logging.info(f"Loaded {len(all_documents)} documents")

    # Split into batches of 1 item each
    all_documents_batches = split_into_batches(all_documents, len(all_documents))
    logging.info(f"Split into {len(all_documents_batches)} batches")

    # Setup TestsetGenerator
    generator_llm = get_llm("nvidia-llama3.1")
    critic_llm = get_llm("nvidia-llama3.1")
    embeddings = get_embedding_model("BAAI/bge-m3")
    generator = TestsetGenerator.from_langchain(generator_llm, critic_llm, embeddings)

    # Set test parameters
    test_size = 1
    distributions = {simple: 1}

    # Get the last processed batch
    last_processed_batch = get_last_processed_batch()
    logging.info(f"Resuming from batch {last_processed_batch}")

    # Load existing testset if available
    if last_processed_batch > 0:
        merged_testset = load_from_pickle(f'merged_testset_{last_processed_batch}')
        logging.info(f"Loaded existing testset with {len(merged_testset)} entries")
    else:
        merged_testset = pd.DataFrame()

      # Process batches
    for batch_index, batch in enumerate(tqdm(all_documents_batches[last_processed_batch:], initial=last_processed_batch, total=len(all_documents_batches))):
        # Calculate the actual batch number by adding the last processed batch index
        actual_batch_num = last_processed_batch + batch_index
        
        try:
            testset = generator.generate_with_langchain_docs(batch, test_size=test_size, distributions=distributions)
            batch_df = testset.to_pandas()
            merged_testset = pd.concat([merged_testset, batch_df], ignore_index=True)

            # Save progress every 5 batches
            if (actual_batch_num + 1) % 5 == 0:
                save_to_pickle(merged_testset, f'merged_testset_{actual_batch_num + 1}')
                save_progress(actual_batch_num + 1)
                logging.info(f"Saved progress: {actual_batch_num + 1}/{len(all_documents_batches)} batches processed")

        except Exception as e:
            logging.error(f"Error processing batch {actual_batch_num}: {str(e)}")
            # Save progress before exiting
            save_to_pickle(merged_testset, f'merged_testset_{actual_batch_num}')
            save_progress(actual_batch_num)
            raise

    # Save final result
    save_to_pickle(merged_testset, 'final_merged_testset')
    logging.info("Processing completed. Final testset saved as 'pickles/final_merged_testset'")

if __name__ == "__main__":
    main()
