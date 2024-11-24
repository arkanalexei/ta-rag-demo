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
MATCH (p:Peraturan {{nomor: XXXX, tahun: YYYY, jenis_peraturan: 'UNDANG-UNDANG'}})
MATCH (p)-[:MENCABUT]->(revoked:Peraturan)
RETURN 
  p AS revokingRegulation, 
  revoked AS revokedRegulation

Example two:
User Query: Undang Undang No XXXX Tahun YYYY dicabut peraturan apa saja?
Generated Cypher Query:

```cypher
MATCH (p:Peraturan {{nomor: XXXX, tahun: YYYY, jenis_peraturan: 'UNDANG-UNDANG'}})
MATCH (p)-[:DICABUT]->(revoked:Peraturan)
RETURN 
  p AS revokedRegulation, 
  revoked AS revokingRegulation

Note: the relationship could either be "MENCABUT", "MENGUBAH", "DIUBAH", or "DICABUT". It depends on the user query.

Lastly, ALWAYS end the generated Cypher statement with a RETURN clause, a FINISH clause, an update clause, a unit subquery call, or a procedure call with no YIELD. Do NOT conclude the Cypher statement with a MATCH clause.

The question is:
{question}
"""
#######################################################################################################################
# GRAPHDB SECTION
#######################################################################################################################

GRAPH_SPARQL_QA_GEN_PROMPT = """##Task: Membuat respons bahasa manusia dari hasil kueri SPARQL

## Instruksi:
Anda adalah asisten yang mengambil hasil dari kueri SPARQL 
dan membentuk respons yang dapat mudah dibaca manusia. Bagian hasil kueri berisi hasil kueri SPARQL
yang dihasilkan berdasarkan pertanyaan bahasa alami pengguna. Informasi yang diberikan bersifat
otoritatif, Anda tidak boleh meragukannya atau mencoba menggunakan pengetahuan internal Anda untuk 
memperbaikinya. Jadikan jawabannya terdengar seperti respons terhadap pertanyaan.

Jika informasi yang diberikan kosong, katakanlah Anda tidak tahu jawabannya.
Informasi kosong terlihat seperti ini: []

Jika informasinya tidak kosong, Anda harus memberikan jawaban menggunakan hasilnya. 
Informasi yang diberikan harusnya adalah jawaban dari pertanyaan yang ditanyakan.
Jika ada peraturan yang berasal dari relasi `lexid-s:amends`, `lexid-s:amendedBy`, `lexid-s:repeals`, ATAU `lexid-s:repealedBy`
TOLONG masukkan informasi seperti nomor ketentuan dan informasi lainnya yang relevan sebagai bukti dari jawaban anda.

Never say you don't have the right information if there is data in
the query results. Always use the data in the query results.

WRITE YOUR ANSWER IN INDONESIAN LANGUAGE.

### Pertanyaan:
{prompt}

### Jawaban dari pertanyaan di atas:
{context}

### Jawaban bahasa manusia:
"""

GRAPH_SPARQL_GEN_0_SHOT_PROMPT = """Task: Generate SPARQL CONSTRUCT statement to query a graph database from a natural language question.

Instructions:
Use ONLY the classes and properties provided in the ontology schema to construct the SPARQL query.
Include all necessary prefixes.
DO NOT use any classes or properties that are NOT EXPLICITLY PROVIDED in the ontology schema.
Use OPTIONAL and CONTAINS clause to do entity matching ONLY against the `rdfs:label` OR `lexid-s:name` to anticipate a fuzzy match.

The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

Note:
Do not include any explanations or apologies in your responses.
Do not wrap the query in backticks.
Do not include any text except the SPARQL query generated.
Do not respond to any questions that might ask anything else than for you to construct a SPARQL CONSTRUCT statement.
Only return the SPARQL CONSTRUCT statement that you already generate.

Jika seorang pengguna menanyakan apakah suatu peraturan MASIH RELEVAN atau MASIH BERLAKU, Anda perlu memeriksa apakah peraturan tersebut telah "DICABUT" atau "DIUBAH" oleh peraturan lain, atau apakah peraturan lain "MENCABUT" atau "MENGUBAH" peraturan tersebut (Pilih hanya salah satu pasangan, "DICABUT" - "DIUBAH" atau "MENCABUT" - "MENGUBAH"). Periksa menggunakan relasi `lexid-s:repealedBy` untuk "DICABUT", `lexid-s:amendedBy` untuk "DIUBAH" pada peraturan yang ditanyakan, ATAU `lexid-s:repeals` untuk "MENCABUT", atau `lexid-s:amends` untuk "MENGUBAH" pada peraturan lain tersebut.

The question delimited by triple backticks is:
```
{prompt}
```
"""

GRAPH_SPARQL_GEN_1_SHOT_PROMPT = """Task: Generate SPARQL CONSTRUCT statement to query a graph database from a natural language question.

Instructions:
Use ONLY the classes and properties provided in the ontology schema to construct the SPARQL query.
Include all necessary prefixes.
DO NOT use any classes or properties that are NOT EXPLICITLY PROVIDED in the ontology schema.
Use OPTIONAL and CONTAINS clause to do entity matching ONLY against the `rdfs:label` OR `lexid-s:name` to anticipate a fuzzy match.

The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

Example:
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

### EXAMPLE ONE
### User Query: Peraturan apa yang dihapus oleh UU Nomor 7 Tahun 1948?
### Generated SPARQL CONSTRUCT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

CONSTRUCT {{
   ?regulation lexid-s:menghapus ?repealingRegulation .
}}
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    lexid-s:repealedBy ?repealingRegulation .
  ?repealingRegulation rdfs:label ?label ;
    lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
  OPTIONAL {{ ?repealingRegulation lexid-s:name ?name . }}
}}
```

Note:
Do not include any explanations or apologies in your responses.
Do not wrap the query in backticks.
Do not include any text except the SPARQL query generated.
Do not respond to any questions that might ask anything else than for you to construct a SPARQL CONSTRUCT statement.
Only return the SPARQL CONSTRUCT statement that you already generate.

Jika seorang pengguna menanyakan apakah suatu peraturan MASIH RELEVAN atau MASIH BERLAKU, Anda perlu memeriksa apakah peraturan tersebut telah "DICABUT" atau "DIUBAH" oleh peraturan lain, atau apakah peraturan lain "MENCABUT" atau "MENGUBAH" peraturan tersebut (Pilih hanya salah satu pasangan, "DICABUT" - "DIUBAH" atau "MENCABUT" - "MENGUBAH"). Periksa menggunakan relasi `lexid-s:repealedBy` untuk "DICABUT", `lexid-s:amendedBy` untuk "DIUBAH" pada peraturan yang ditanyakan, ATAU `lexid-s:repeals` untuk "MENCABUT", atau `lexid-s:amends` untuk "MENGUBAH" pada peraturan lain tersebut.

The question delimited by triple backticks is:
```
{prompt}
```
"""

GRAPH_SPARQL_GEN_3_SHOT_PROMPT = """Task: Generate SPARQL CONSTRUCT statement to query a graph database from a natural language question.

Instructions:
Use ONLY the classes and properties provided in the ontology schema to construct the SPARQL query.
Include all necessary prefixes.
DO NOT use any classes or properties that are NOT EXPLICITLY PROVIDED in the ontology schema.
Use OPTIONAL and CONTAINS clause to do entity matching ONLY against the `rdfs:label` OR `lexid-s:name` to anticipate a fuzzy match.

The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

Example:
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

### EXAMPLE ONE
### User Query: Peraturan apa yang dihapus oleh UU Nomor 7 Tahun 1948?
### Generated SPARQL CONSTRUCT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

CONSTRUCT {{
   ?regulation lexid-s:menghapus ?repealingRegulation .
}}
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    lexid-s:repealedBy ?repealingRegulation .
  ?repealingRegulation rdfs:label ?label ;
    lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
  OPTIONAL {{ ?repealingRegulation lexid-s:name ?name . }}
}}
```
### EXAMPLE TWO
### User Query: Apa tujuan dari peraturan Undang-Undang Republik Indonesia Nomor 30 Tahun 2002?
### Generated SPARQL CONSTRUCT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

CONSTRUCT {{
    ?regulation lexid-s:mempertimbangkan ?considerant .
}}
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?label ;
    lexid-s:considers ?considerant ;
    lexid-s:hasRegulationNumber "30" ;
    lexid-s:hasRegulationYear "2002" .
}}
```

### EXAMPLE THREE
### User Query: Apa dasar hukum dari Undang Undang No. 6 Tahun 1987?
### Generated SPARQL CONSTRUCT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

CONSTRUCT {{
    ?regulation lexid-s:memilikiDasarHukum ?legalBasis
}}
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?regulationLabel ;
    lexid-s:hasLegalBasis ?legalBasis ;
    lexid-s:hasRegulationNumber "6" ;
    lexid-s:hasRegulationYear "1987" .
  ?legalBasis rdfs:label ?legalBasisLabel
}}
```

Note:
Do not include any explanations or apologies in your responses.
Do not wrap the query in backticks.
Do not include any text except the SPARQL query generated.
Do not respond to any questions that might ask anything else than for you to construct a SPARQL CONSTRUCT statement.
Only return the SPARQL CONSTRUCT statement that you already generate.

Jika seorang pengguna menanyakan apakah suatu peraturan MASIH RELEVAN atau MASIH BERLAKU, Anda perlu memeriksa apakah peraturan tersebut telah "DICABUT" atau "DIUBAH" oleh peraturan lain, atau apakah peraturan lain "MENCABUT" atau "MENGUBAH" peraturan tersebut (Pilih hanya salah satu pasangan, "DICABUT" - "DIUBAH" atau "MENCABUT" - "MENGUBAH"). Periksa menggunakan relasi `lexid-s:repealedBy` untuk "DICABUT", `lexid-s:amendedBy` untuk "DIUBAH" pada peraturan yang ditanyakan, ATAU `lexid-s:repeals` untuk "MENCABUT", atau `lexid-s:amends` untuk "MENGUBAH" pada peraturan lain tersebut.

The question delimited by triple backticks is:
```
{prompt}
```
"""