import json
import os
import pickle
import random
import string

from deep_translator import GoogleTranslator
from langdetect import detect


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
