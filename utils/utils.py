import json
import os
import pickle
import random
import string
import re
import torch

from deep_translator import GoogleTranslator
from langdetect import detect

def clean_string(s):
    s = s.lower().strip()
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'[^a-z0-9 ]', '', s)
    s = s.replace(' ', '')
    
    return s

def load_metadata(metadata_dir):
    metadata_dict = {}
    for subdir in ['uu']:
        full_dir_path = os.path.join(metadata_dir, subdir)
        for filename in os.listdir(full_dir_path):
            if filename.endswith('.json'):
                filepath = os.path.join(full_dir_path, filename)
                with open(filepath, 'r') as f:
                    metadata_list = json.load(f)
                    for item in metadata_list:
                        metadata_dict[item['id']] = item
    return metadata_dict

def ensure_metadata_fields(metadata, required_fields):
    return {field: metadata.get(field, "") for field in required_fields}

translator_en = GoogleTranslator(source='auto', target='en')
translator_id = GoogleTranslator(source='auto', target='id')

def is_language_indonesian(query):
    # This function assumes only laguage is either
    # Indonesian or English
    detected_lang = detect(query)
    return detected_lang == 'id'

def translate(lang, query):
    if lang == "id":
        return translator_id.translate(query)
    return translator_en.translate(query)

def save_to_pickle(file, filename):
    with open(f'pickles/{filename}.pkl', 'wb') as f:
        pickle.dump(file, f)

def load_from_pickle(filename):
    file = open(f'pickles/{filename}.pkl','rb')
    return pickle.load(file)

def generate_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8)).lower()

def set_gpu(gpu):
    torch.cuda.set_device(gpu)
    print(f"Set GPU to {gpu}")

# Function to extract and format subject from URI
def format_iri(uri):
    # Extract the identifier from the URI
    match = re.search(r'/data/([^/]+)$', uri)
    if not match:
        match = re.search(r'/schema/([^/]+)$', uri)
    if not match:
        return uri  # Return URI if no match found
        
    identifier = match.group(1)  # e.g., "UU_2007_40"
    
    # Format the identifier into a natural language label
    parts = identifier.split('_')  # e.g., ["UU", "2007", "40"]
    result_lst = [''] * len(parts)

    if parts[0] == "UU" or parts[0] == "UUD":
        for i, part in enumerate(parts):
            if i == 0:
                if part == "UU":
                    result_lst[i] = "Undang-Undang"
                elif part == "UUD":
                    result_lst[i] = "Undang-Undang Dasar"
                else:
                    result_lst[i] = part
            elif i == 1:
                result_lst[i] = f"Tahun {part}"
            elif i == 2:
                result_lst[i] = f"Nomor {part}"
            else:
                result_lst[i] = part
    else:
        for i, part in enumerate(parts):
            result_lst[i] = part
    
    return " ".join(result_lst)
    
# Function to extract and format predicate from URI
def format_predicate(uri):
    # Extract the last part of the predicate URI
    match = re.search(r'/schema/([^/]+)$', uri) # lexid-s
    if not match:
        match = re.search(r'/22-rdf-syntax-ns#([^/]+)$', uri) # rdf
    if not match:
        match = re.search(r'/rdf-schema#([^/]+)$', uri) # rdfs
    if not match:
        match = re.search(r'/terms/([^/]+)$', uri) # dct
    if not match:
        return uri
        
    predicate = match.group(1)  # take the first URI directory
    return predicate

# Function to verbalize triples
def verbalize_triples(triples):
    sentences = []
    for subj, pred_uri, obj in triples:
        # Format subject, predicate, and object
        subject_label = format_iri(subj)
        predicate_label = format_predicate(pred_uri)
        object_label = format_iri(obj)
        sentence = f"{subject_label} {predicate_label} {object_label}."
        sentences.append(sentence)
    return sentences
