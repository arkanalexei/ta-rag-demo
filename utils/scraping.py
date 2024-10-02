import re
import random
import requests
import string

def slugify(input_string):
    if isinstance(input_string, float):
        return "unknown"
    normalized_string = re.sub(r'\W+', '_', input_string)
    normalized_string = normalized_string.lower()
    return normalized_string

def generate_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8)).lower()

def download_file(url, filepath):
    response = requests.get(url)
    response.raise_for_status()
    with open(filepath, 'wb') as file:
        file.write(response.content)

def create_metadata(row, doc_url, unique_id, new_filename):
    metadata = {
            "title": row['title'],
            "jenis_bentuk_peraturan": row['jenis_bentuk_peraturan'],
            "pemrakarsa": row['pemrakarsa'],
            "nomor": row['nomor'],
            "tahun": row['tahun'],
            "tentang": row['tentang'],
            "tempat_penetapan": row['tempat_penetapan'],
            "ditetapkan_tanggal": row['ditetapkan_tanggal'],
            "status": row['status'],
            "dokumen_peraturan": doc_url,
            "id": unique_id,
            "filename": new_filename
        }
    return metadata