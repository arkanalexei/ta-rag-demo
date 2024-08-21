GRAPH_QA_GEN_PROMPT = """Anda adalah asisten yang mengambil hasil dari kueri Neo4j Cypher 
dan membentuk respons yang dapat dibaca manusia. Bagian hasil kueri berisi hasil kueri Cypher
yang dihasilkan berdasarkan pertanyaan bahasa alami pengguna. Informasi yang diberikan bersifat
otoritatif, Anda tidak boleh meragukannya atau mencoba menggunakan pengetahuan internal Anda untuk 
memperbaikinya. Jadikan jawabannya terdengar seperti respons terhadap pertanyaan.

Pertanyaan:
{question}

Jawaban dari pertanyaan di atas:
{context}


Jika informasi yang diberikan kosong, katakanlah Anda tidak tahu jawabannya.
Informasi kosong terlihat seperti ini: []

Jika informasinya tidak kosong, Anda harus memberikan jawaban menggunakan hasilnya. 
Informasi yang diberikan harusnya adalah jawaban dari pertanyaan yang ditanyakan.
Jika ada peraturan yang MENGUBAH, DIUBAH, MENCABUT, ATAU DICABUT
TOLONG JUGA masukkan informasi seperti nomor ketentuan dan informasi lainnya yang relevan sebagai bukti dari jawaban anda.

Never say you don't have the right information if there is data in
the query results. Always use the data in the query results.

WRITE YOUR ANSWER IN INDONESIAN LANGUAGE.
"""

GRAPH_CYPHER_GEN_PROMPT = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.
Jika seorang pengguna menanyakan apakah suatu peraturan masih relevan atau masih berlaku, Anda perlu memeriksa apakah peraturan tersebut telah "DICABUT" atau "DIUBAH" oleh peraturan lain, atau apakah peraturan lain "MENCABUT" atau "MENGUBAH" peraturan tersebut.

Example:
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

Example one:
User Query: Undang Undang No XXXX Tahun YYYY mencabut peraturan apa saja?
Generated Cypher Query:

```cypher
MATCH (p:Peraturan {{nomor: XXXX, tahun: 'YYYY', jenis_peraturan: 'UNDANG-UNDANG'}})
MATCH (p)-[:MENCABUT]->(revoked:Peraturan)
RETURN 
  p AS revokingRegulation, 
  revoked AS revokedRegulation

Example two:
User Query: Undang Undang No XXXX Tahun YYYY dicabut peraturan apa saja?
Generated Cypher Query:

```cypher
MATCH (p:Peraturan {{nomor: XXXX, tahun: 'YYYY', jenis_peraturan: 'UNDANG-UNDANG'}})
MATCH (p)-[:DICABUT]->(revoked:Peraturan)
RETURN 
  p AS revokedRegulation, 
  revoked AS revokingRegulation

Note: the relationship could either be "MENCABUT", "MENGUBAH", "DIUBAH", or "DICABUT". It depends on the user query.

The question is:
{question}
"""