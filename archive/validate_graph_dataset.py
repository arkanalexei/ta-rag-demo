import pandas as pd
import openai
import concurrent.futures
import time
from utils.utils import load_from_pickle, save_to_pickle

# Set your OpenAI API key
api_key = "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" # Replace with your actual API key

client = openai.OpenAI(
    api_key=api_key,  # This is the default and can be omitted
)

# Load the DataFrame
data = load_from_pickle("filtered_testset_2_ttl")

# Function to construct the prompt and get the validation result
def get_validation(row):
    question = row['cleaned_question']
    context = ' '.join(row['contexts'])  # Combine context if it's a list
    ground_truth = row['ground_truth']
    
    # Construct a concise prompt
    prompt = f"""
Based on the context below, classify the answer as one of the choices (A, B, C, or D):

Context:
{context}

Question:
{question}

Answer:
{ground_truth}

Choices:
A. Correct answer (answers the question) and matches the given context
B. Correct answer (answers the question) but does NOT match the given context
C. Incorrect answer (does not answer the question) but the question matches the context
D. Incorrect answer (does not answer the question) and the question does NOT match the context

Provide only the letter corresponding to the correct choice (A, B, C, or D).
"""
    max_retries = 5
    retry_delay = 5  # seconds
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "user", "content": prompt,}
                        ],
                        max_tokens=1,  # Limit to 1 token since the expected output is a single character
                        temperature=0.0  # Use deterministic output
                    )
            # Extract the assistant's reply
            validation = response.choices[0].message.content.strip()
            return validation
        except openai.RateLimitError as e:
            if attempt < max_retries - 1:
                print(f"Rate limit reached. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Error processing row {row.name}: {e}")
                return None
        except Exception as e:
            print(f"Error processing row {row.name}: {e}")
            return None

# Apply the function to the DataFrame using parallel processing
def process_dataframe(df):
    results = []
    max_workers = 5  # Adjust this number based on your rate limit and performance needs
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(get_validation, row): idx for idx, row in df.iterrows()}
        for future in concurrent.futures.as_completed(futures):
            idx = futures[future]
            try:
                validation = future.result()
            except Exception as e:
                print(f"Error at index {idx}: {e}")
                validation = None
            results.append((idx, validation))
    return results

example_row = data.iloc[0]
result = get_validation(example_row)

# Run the processing function
validation_results = process_dataframe(data)
validation_dict = dict(validation_results)
data['validate'] = data.index.map(validation_dict)

# Save the updated DataFrame
filename = "validated_graph_testset"
save_to_pickle(data, filename)

print(f"Validation complete. The updated DataFrame has been saved as '{filename}'.")