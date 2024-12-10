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
# GRAPHDB QA SECTION
#######################################################################################################################
GRAPH_SPARQL_QA_GEN_PROMPT = """## Task: Membuat respons bahasa manusia dari hasil kueri SPARQL

### Instruksi:
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
#######################################################################################################################
# GRAPHDB CONSTRUCT NORMAL SECTION
#######################################################################################################################
CONSTRUCT_SPARQL_GEN_0_SHOT_PROMPT = """## Task: Generate SPARQL CONSTRUCT statement to query a graph database from a natural language question.

### Instructions:
DO NOT SPEND MORE THAN 8 SECONDS TO GENERATE THE SPARQL QUERY
ONLY include relevant properties, avoid unnecessary properties or all-encompassing variables.
Use ONLY the classes and properties provided in the ontology schema to construct the SPARQL query.
Include all necessary prefixes.
DO NOT use any classes or properties that are NOT EXPLICITLY PROVIDED in the ontology schema.
Use OPTIONAL and CONTAINS clause to do entity matching ONLY TO the `rdfs:label` OR `lexid-s:name` to do a fuzzy match.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

### Note:
Do not include any explanations or apologies in your responses.
Do not wrap the query in backticks.
Do not include any text except the SPARQL query generated.
Do not respond to any questions that might ask anything else than for you to generate a SPARQL CONSTRUCT statement.
Only return the SPARQL CONSTRUCT statement that you already generate.

Jika seorang pengguna menanyakan apakah suatu peraturan MASIH RELEVAN atau MASIH BERLAKU, Anda perlu memeriksa apakah peraturan tersebut telah "DICABUT" atau "DIUBAH" oleh peraturan lain, atau apakah peraturan lain "MENCABUT" atau "MENGUBAH" peraturan tersebut (Pilih hanya salah satu pasangan, "DICABUT" - "DIUBAH" atau "MENCABUT" - "MENGUBAH"). Periksa menggunakan relasi `lexid-s:repealedBy` untuk "DICABUT", `lexid-s:amendedBy` untuk "DIUBAH" pada peraturan yang ditanyakan, ATAU `lexid-s:repeals` untuk "MENCABUT", atau `lexid-s:amends` untuk "MENGUBAH" pada peraturan lain tersebut.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""

CONSTRUCT_SPARQL_GEN_1_SHOT_PROMPT = """## Task: Generate SPARQL CONSTRUCT statement to query a graph database from a natural language question.

### Instructions:
Avoid using all properties as variables.
Use ONLY the classes and properties provided in the ontology schema to construct the SPARQL query.
Include all necessary prefixes.
DO NOT use any classes or properties that are NOT EXPLICITLY PROVIDED in the ontology schema.
Use OPTIONAL and CONTAINS clause to do entity matching ONLY TO the `rdfs:label` OR `lexid-s:name` to do a fuzzy match.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

### Example:
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

### Note:
Do not include any explanations or apologies in your responses.
Do not wrap the query in backticks.
Do not include any text except the SPARQL query generated.
Do not respond to any questions that might ask anything else than for you to generate a SPARQL CONSTRUCT statement.
Only return the SPARQL CONSTRUCT statement that you already generate.

Jika seorang pengguna menanyakan apakah suatu peraturan MASIH RELEVAN atau MASIH BERLAKU, Anda perlu memeriksa apakah peraturan tersebut telah "DICABUT" atau "DIUBAH" oleh peraturan lain, atau apakah peraturan lain "MENCABUT" atau "MENGUBAH" peraturan tersebut (Pilih hanya salah satu pasangan, "DICABUT" - "DIUBAH" atau "MENCABUT" - "MENGUBAH"). Periksa menggunakan relasi `lexid-s:repealedBy` untuk "DICABUT", `lexid-s:amendedBy` untuk "DIUBAH" pada peraturan yang ditanyakan, ATAU `lexid-s:repeals` untuk "MENCABUT", atau `lexid-s:amends` untuk "MENGUBAH" pada peraturan lain tersebut.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""
CONSTRUCT_SPARQL_GEN_2_SHOT_PROMPT = """## Task: Generate SPARQL CONSTRUCT statement to query a graph database from a natural language question.

### Instructions:
DO NOT SPEND MORE THAN 8 SECONDS TO GENERATE THE SPARQL QUERY
ONLY include relevant properties, avoid unnecessary properties or all-encompassing variables.
Use ONLY the classes and properties provided in the ontology schema to construct the SPARQL query.
Include all necessary prefixes.
DO NOT use any classes or properties that are NOT EXPLICITLY PROVIDED in the ontology schema.
Use OPTIONAL and CONTAINS clause to do entity matching ONLY TO the `rdfs:label` OR `lexid-s:name` to do a fuzzy match.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

### Example:
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

### Note:
Do not include any explanations or apologies in your responses.
Do not wrap the query in backticks.
Do not include any text except the SPARQL query generated.
Do not respond to any questions that might ask anything else than for you to generate a SPARQL CONSTRUCT statement.
Only return the SPARQL CONSTRUCT statement that you already generate.

Jika seorang pengguna menanyakan apakah suatu peraturan MASIH RELEVAN atau MASIH BERLAKU, Anda perlu memeriksa apakah peraturan tersebut telah "DICABUT" atau "DIUBAH" oleh peraturan lain, atau apakah peraturan lain "MENCABUT" atau "MENGUBAH" peraturan tersebut (Pilih hanya salah satu pasangan, "DICABUT" - "DIUBAH" atau "MENCABUT" - "MENGUBAH"). Periksa menggunakan relasi `lexid-s:repealedBy` untuk "DICABUT", `lexid-s:amendedBy` untuk "DIUBAH" pada peraturan yang ditanyakan, ATAU `lexid-s:repeals` untuk "MENCABUT", atau `lexid-s:amends` untuk "MENGUBAH" pada peraturan lain tersebut.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""
CONSTRUCT_SPARQL_GEN_3_SHOT_PROMPT = """## Task: Generate SPARQL CONSTRUCT statement to query a graph database from a natural language question.

### Instructions:
Avoid using all properties as variables.
Use ONLY the classes and properties provided in the ontology schema to construct the SPARQL query.
Include all necessary prefixes.
DO NOT use any classes or properties that are NOT EXPLICITLY PROVIDED in the ontology schema.
Use OPTIONAL and CONTAINS clause to do entity matching ONLY TO the `rdfs:label` OR `lexid-s:name` to do a fuzzy match.

### Ontology Schema:s
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

### Example:
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
   ?regulation lexid-s:menghapus ?repealedRegulation .
}}
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    lexid-s:repealedBy ?repealedRegulation .
  ?repealedRegulation rdfs:label ?label ;
    lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
    
  OPTIONAL {{ ?repealedRegulation lexid-s:name ?name . }}
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

### Note:
Do not include any explanations or apologies in your responses.
Do not wrap the query in backticks.
Do not include any text except the SPARQL query generated.
Do not respond to any questions that might ask anything else than for you to generate a SPARQL CONSTRUCT statement.
Only return the SPARQL CONSTRUCT statement that you already generate.

Jika seorang pengguna menanyakan apakah suatu peraturan MASIH RELEVAN atau MASIH BERLAKU, Anda perlu memeriksa apakah peraturan tersebut telah "DICABUT" atau "DIUBAH" oleh peraturan lain, atau apakah peraturan lain "MENCABUT" atau "MENGUBAH" peraturan tersebut (Pilih hanya salah satu pasangan, "DICABUT" - "DIUBAH" atau "MENCABUT" - "MENGUBAH"). Periksa menggunakan relasi `lexid-s:repealedBy` untuk "DICABUT", `lexid-s:amendedBy` untuk "DIUBAH" pada peraturan yang ditanyakan, ATAU `lexid-s:repeals` untuk "MENCABUT", atau `lexid-s:amends` untuk "MENGUBAH" pada peraturan lain tersebut.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""
CONSTRUCT_SPARQL_GEN_4_SHOT_PROMPT = """## Task: Generate SPARQL CONSTRUCT statement to query a graph database from a natural language question.

### Instructions:
Avoid using all properties as variables.
Use ONLY the classes and properties provided in the ontology schema to construct the SPARQL query.
Include all necessary prefixes.
DO NOT use any classes or properties that are NOT EXPLICITLY PROVIDED in the ontology schema.
Use OPTIONAL and CONTAINS clause to do entity matching ONLY TO the `rdfs:label` OR `lexid-s:name` to do a fuzzy match.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

### Example:
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

### EXAMPLE FOUR
### User Query: Apakah Undang Undang Tahun 2004 No 10 masih relevan?
### Generated SPARQL CONSTRUCT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

CONSTRUCT {{
    ?regulation lexid-s:dicabutOleh ?otherRegulation .
    ?regulation lexid-s:status ?status .
}}
WHERE {{
    ?regulation a lexid-s:LegalDocument ;
    	lexid-s:repealedBy ?otherRegulation ;
    	lexid-s:hasRegulationNumber "10" ;
    	lexid-s:hasRegulationYear "2004" .
    OPTIONAL {{ ?regulation lexid-s:status ?status . }}
}}
```

### Note:
Do not include any explanations or apologies in your responses.
Do not wrap the query in backticks.
Do not include any text except the SPARQL query generated.
Do not respond to any questions that might ask anything else than for you to generate a SPARQL CONSTRUCT statement.
Only return the SPARQL CONSTRUCT statement that you already generate.

Jika seorang pengguna menanyakan apakah suatu peraturan MASIH RELEVAN atau MASIH BERLAKU, Anda perlu memeriksa apakah peraturan tersebut telah "DICABUT" atau "DIUBAH" oleh peraturan lain, atau apakah peraturan lain "MENCABUT" atau "MENGUBAH" peraturan tersebut (Pilih hanya salah satu pasangan, "DICABUT" - "DIUBAH" atau "MENCABUT" - "MENGUBAH"). Periksa menggunakan relasi `lexid-s:repealedBy` untuk "DICABUT", `lexid-s:amendedBy` untuk "DIUBAH" pada peraturan yang ditanyakan, ATAU `lexid-s:repeals` untuk "MENCABUT", atau `lexid-s:amends` untuk "MENGUBAH" pada peraturan lain tersebut.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""
CONSTRUCT_SPARQL_GEN_5_SHOT_PROMPT = """## Task: Generate SPARQL CONSTRUCT statement to query a graph database from a natural language question.

### Instructions:
Avoid using all properties as variables.
Use ONLY the classes and properties provided in the ontology schema to construct the SPARQL query.
Include all necessary prefixes.
DO NOT use any classes or properties that are NOT EXPLICITLY PROVIDED in the ontology schema.
Use OPTIONAL and CONTAINS clause to do entity matching ONLY TO the `rdfs:label` OR `lexid-s:name` to do a fuzzy match.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

### Example:
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
   ?regulation lexid-s:menghapus ?repealedRegulation .
}}
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    lexid-s:repealedBy ?repealedRegulation .
  ?repealedRegulation rdfs:label ?label ;
    lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
    
  OPTIONAL {{ ?repealedRegulation lexid-s:name ?name . }}
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

### EXAMPLE FOUR
### User Query: Apakah Undang Undang Tahun 2004 No 10 masih relevan?
### Generated SPARQL CONSTRUCT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

CONSTRUCT {{
    ?regulation lexid-s:dicabutOleh ?otherRegulation .
    ?regulation lexid-s:status ?status .
}}
WHERE {{
    ?regulation a lexid-s:LegalDocument ;
    	lexid-s:repealedBy ?otherRegulation ;
    	lexid-s:hasRegulationNumber "10" ;
    	lexid-s:hasRegulationYear "2004" .
    OPTIONAL {{ ?regulation lexid-s:status ?status . }}
}}
```

### EXAMPLE FIVE
### User Query: Di manakah UU No. 12 Thn 2011 ditetapkan?
### Generated SPARQL CONSTRUCT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

CONSTRUCT {{
    ?regulation lexid-s:ditetapkanDi ?enactionLocation .
}}
WHERE {{
    ?regulation a lexid-s:LegalDocument ;
    	lexid-s:hasEnactionLocation ?enactionLocation ;
    	lexid-s:hasRegulationYear "2011" ;
    	lexid-s:hasRegulationNumber "12" .
}}
```

### Note:
Do NOT include any explanations or apologies in your responses.
Do NOT wrap the query in backticks.
Do NOT return this input prompt to the output
Do NOT include any text except the SPARQL query generated.
Do NOT respond to any questions that might ask anything else than for you to generate a SPARQL CONSTRUCT statement.
Only return the SPARQL CONSTRUCT statement that you already generate.

Jika seorang pengguna menanyakan apakah suatu peraturan MASIH RELEVAN atau MASIH BERLAKU, Anda perlu memeriksa apakah peraturan tersebut telah "DICABUT" atau "DIUBAH" oleh peraturan lain, atau apakah peraturan lain "MENCABUT" atau "MENGUBAH" peraturan tersebut (Pilih hanya salah satu pasangan, "DICABUT" - "DIUBAH" atau "MENCABUT" - "MENGUBAH"). Periksa menggunakan relasi `lexid-s:repealedBy` untuk "DICABUT", `lexid-s:amendedBy` untuk "DIUBAH" pada peraturan yang ditanyakan, ATAU `lexid-s:repeals` untuk "MENCABUT", atau `lexid-s:amends` untuk "MENGUBAH" pada peraturan lain tersebut.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""

#######################################################################################################################
# GRAPHDB SELECT NORMAL SECTION
#######################################################################################################################
SELECT_SPARQL_GEN_0_SHOT_PROMPT = """## Task: Generate SPARQL SELECT statement to query a graph database from a natural language question.

### Instructions:
Avoid using all properties as variables.
Use ONLY the classes and properties provided in the ontology schema to construct the SPARQL query.
Include all necessary prefixes.
DO NOT use any classes or properties that are NOT EXPLICITLY PROVIDED in the ontology schema.
Use OPTIONAL and CONTAINS clause to do entity matching ONLY TO the `rdfs:label` OR `lexid-s:name` to do a fuzzy match.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

### Note:
Do not include any explanations or apologies in your responses.
Do not wrap the query in backticks.
Do not include any text except the SPARQL query generated.
Do not respond to any questions that might ask anything else than for you to generate a SPARQL SELECT statement.
Only return the SPARQL SELECT statement that you already generate.

Jika seorang pengguna menanyakan apakah suatu peraturan MASIH RELEVAN atau MASIH BERLAKU, Anda perlu memeriksa apakah peraturan tersebut telah "DICABUT" atau "DIUBAH" oleh peraturan lain, atau apakah peraturan lain "MENCABUT" atau "MENGUBAH" peraturan tersebut (Pilih hanya salah satu pasangan, "DICABUT" - "DIUBAH" atau "MENCABUT" - "MENGUBAH"). Periksa menggunakan relasi `lexid-s:repealedBy` untuk "DICABUT", `lexid-s:amendedBy` untuk "DIUBAH" pada peraturan yang ditanyakan, ATAU `lexid-s:repeals` untuk "MENCABUT", atau `lexid-s:amends` untuk "MENGUBAH" pada peraturan lain tersebut.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""

SELECT_SPARQL_GEN_1_SHOT_PROMPT = """## Task: Generate SPARQL SELECT statement to query a graph database from a natural language question.

### Instructions:
Avoid using all properties as variables.
Use ONLY the classes and properties provided in the ontology schema to construct the SPARQL query.
Include all necessary prefixes.
DO NOT use any classes or properties that are NOT EXPLICITLY PROVIDED in the ontology schema.
Use OPTIONAL and CONTAINS clause to do entity matching ONLY TO the `rdfs:label` OR `lexid-s:name` to do a fuzzy match.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

### Example:
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

### EXAMPLE ONE
### User Query: Peraturan apa yang dihapus oleh UU Nomor 7 Tahun 1948?
### Generated SPARQL SELECT Query:
```
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?regulation ?label ?name
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?label ;
    lexid-s:repealedBy ?repealingRegulation .
  ?repealingRegulation lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
  OPTIONAL {{ ?regulation lexid-s:name ?name . }}
}}
```

### Note:
Do not include any explanations or apologies in your responses.
Do not wrap the query in backticks.
Do not include any text except the SPARQL query generated.
Do not respond to any questions that might ask anything else than for you to generate a SPARQL SELECT statement.
Only return the SPARQL SELECT statement that you already generate.

Jika seorang pengguna menanyakan apakah suatu peraturan MASIH RELEVAN atau MASIH BERLAKU, Anda perlu memeriksa apakah peraturan tersebut telah "DICABUT" atau "DIUBAH" oleh peraturan lain, atau apakah peraturan lain "MENCABUT" atau "MENGUBAH" peraturan tersebut (Pilih hanya salah satu pasangan, "DICABUT" - "DIUBAH" atau "MENCABUT" - "MENGUBAH"). Periksa menggunakan relasi `lexid-s:repealedBy` untuk "DICABUT", `lexid-s:amendedBy` untuk "DIUBAH" pada peraturan yang ditanyakan, ATAU `lexid-s:repeals` untuk "MENCABUT", atau `lexid-s:amends` untuk "MENGUBAH" pada peraturan lain tersebut.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""
SELECT_SPARQL_GEN_2_SHOT_PROMPT = """## Task: Generate SPARQL SELECT statement to query a graph database from a natural language question.

### Instructions:
Avoid using all properties as variables.
Use ONLY the classes and properties provided in the ontology schema to construct the SPARQL query.
Include all necessary prefixes.
DO NOT use any classes or properties that are NOT EXPLICITLY PROVIDED in the ontology schema.
Use OPTIONAL and CONTAINS clause to do entity matching ONLY TO the `rdfs:label` OR `lexid-s:name` to do a fuzzy match.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

### Example:
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

### EXAMPLE ONE
### User Query: Peraturan apa yang dihapus oleh UU Nomor 7 Tahun 1948?
### Generated SPARQL SELECT Query:
```
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?regulation ?label ?name
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?label ;
    lexid-s:repealedBy ?repealingRegulation .
  ?repealingRegulation lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
  OPTIONAL {{ ?regulation lexid-s:name ?name . }}
}}
```
### EXAMPLE TWO
### User Query: Apa tujuan dari peraturan Undang-Undang Republik Indonesia Nomor 30 Tahun 2002?
### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?label ?considerant
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?label ;
    lexid-s:considers ?considerant ;
    lexid-s:hasRegulationNumber "30" ;
    lexid-s:hasRegulationYear "2002" .
}}
```

### Note:
Do not include any explanations or apologies in your responses.
Do not wrap the query in backticks.
Do not include any text except the SPARQL query generated.
Do not respond to any questions that might ask anything else than for you to generate a SPARQL SELECT statement.
Only return the SPARQL SELECT statement that you already generate.

Jika seorang pengguna menanyakan apakah suatu peraturan MASIH RELEVAN atau MASIH BERLAKU, Anda perlu memeriksa apakah peraturan tersebut telah "DICABUT" atau "DIUBAH" oleh peraturan lain, atau apakah peraturan lain "MENCABUT" atau "MENGUBAH" peraturan tersebut (Pilih hanya salah satu pasangan, "DICABUT" - "DIUBAH" atau "MENCABUT" - "MENGUBAH"). Periksa menggunakan relasi `lexid-s:repealedBy` untuk "DICABUT", `lexid-s:amendedBy` untuk "DIUBAH" pada peraturan yang ditanyakan, ATAU `lexid-s:repeals` untuk "MENCABUT", atau `lexid-s:amends` untuk "MENGUBAH" pada peraturan lain tersebut.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""
SELECT_SPARQL_GEN_3_SHOT_PROMPT = """## Task: Generate SPARQL SELECT statement to query a graph database from a natural language question.

### Instructions:
Avoid using all properties as variables.
Use ONLY the classes and properties provided in the ontology schema to construct the SPARQL query.
Include all necessary prefixes.
DO NOT use any classes or properties that are NOT EXPLICITLY PROVIDED in the ontology schema.
Use OPTIONAL and CONTAINS clause to do entity matching ONLY TO the `rdfs:label` OR `lexid-s:name` to do a fuzzy match.

### Ontology Schema:s
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

### Example:
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

### EXAMPLE ONE
### User Query: Peraturan apa yang dihapus oleh UU Nomor 7 Tahun 1948?
### Generated SPARQL SELECT Query:
```
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?regulation ?label ?name
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?label ;
    lexid-s:repealedBy ?repealingRegulation .
  ?repealingRegulation lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
  OPTIONAL {{ ?regulation lexid-s:name ?name . }}
}}
```
### EXAMPLE TWO
### User Query: Apa tujuan dari peraturan Undang-Undang Republik Indonesia Nomor 30 Tahun 2002?
### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?label ?considerant
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
### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?regulation ?legalBasis
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?regulationLabel ;
    lexid-s:hasLegalBasis ?legalBasis ;
    lexid-s:hasRegulationNumber "6" ;
    lexid-s:hasRegulationYear "1987" .
  ?legalBasis rdfs:label ?legalBasisLabel
}}
```

### Note:
Do not include any explanations or apologies in your responses.
Do not wrap the query in backticks.
Do not include any text except the SPARQL query generated.
Do not respond to any questions that might ask anything else than for you to generate a SPARQL SELECT statement.
Only return the SPARQL SELECT statement that you already generate.

Jika seorang pengguna menanyakan apakah suatu peraturan MASIH RELEVAN atau MASIH BERLAKU, Anda perlu memeriksa apakah peraturan tersebut telah "DICABUT" atau "DIUBAH" oleh peraturan lain, atau apakah peraturan lain "MENCABUT" atau "MENGUBAH" peraturan tersebut (Pilih hanya salah satu pasangan, "DICABUT" - "DIUBAH" atau "MENCABUT" - "MENGUBAH"). Periksa menggunakan relasi `lexid-s:repealedBy` untuk "DICABUT", `lexid-s:amendedBy` untuk "DIUBAH" pada peraturan yang ditanyakan, ATAU `lexid-s:repeals` untuk "MENCABUT", atau `lexid-s:amends` untuk "MENGUBAH" pada peraturan lain tersebut.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""
SELECT_SPARQL_GEN_4_SHOT_PROMPT = """## Task: Generate SPARQL SELECT statement to query a graph database from a natural language question.

### Instructions:
Avoid using all properties as variables.
Use ONLY the classes and properties provided in the ontology schema to construct the SPARQL query.
Include all necessary prefixes.
DO NOT use any classes or properties that are NOT EXPLICITLY PROVIDED in the ontology schema.
Use OPTIONAL and CONTAINS clause to do entity matching ONLY TO the `rdfs:label` OR `lexid-s:name` to do a fuzzy match.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

### Example:
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

### EXAMPLE ONE
### User Query: Peraturan apa yang dihapus oleh UU Nomor 7 Tahun 1948?
### Generated SPARQL SELECT Query:
```
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?regulation ?label ?name
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?label ;
    lexid-s:repealedBy ?repealingRegulation .
  ?repealingRegulation lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
  OPTIONAL {{ ?regulation lexid-s:name ?name . }}
}}
```

### EXAMPLE TWO
### User Query: Apa tujuan dari peraturan Undang-Undang Republik Indonesia Nomor 30 Tahun 2002?
### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?label ?considerant
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
### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?regulation ?legalBasis
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?regulationLabel ;
    lexid-s:hasLegalBasis ?legalBasis ;
    lexid-s:hasRegulationNumber "6" ;
    lexid-s:hasRegulationYear "1987" .
  ?legalBasis rdfs:label ?legalBasisLabel
}}
```

### EXAMPLE FOUR
### User Query: Apakah Undang Undang Tahun 2004 No 10 masih relevan?
### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?regulation ?repealingRegulation ?status
WHERE {{
    ?regulation a lexid-s:LegalDocument ;
    	lexid-s:repealedBy ?repealingRegulation ;
    	lexid-s:hasRegulationNumber "10" ;
    	lexid-s:hasRegulationYear "2004" .
    OPTIONAL {{ ?regulation lexid-s:status ?status . }}
}}
```

### Note:
Do not include any explanations or apologies in your responses.
Do not wrap the query in backticks.
Do not include any text except the SPARQL query generated.
Do not respond to any questions that might ask anything else than for you to generate a SPARQL SELECT statement.
Only return the SPARQL SELECT statement that you already generate.

Jika seorang pengguna menanyakan apakah suatu peraturan MASIH RELEVAN atau MASIH BERLAKU, Anda perlu memeriksa apakah peraturan tersebut telah "DICABUT" atau "DIUBAH" oleh peraturan lain, atau apakah peraturan lain "MENCABUT" atau "MENGUBAH" peraturan tersebut (Pilih hanya salah satu pasangan, "DICABUT" - "DIUBAH" atau "MENCABUT" - "MENGUBAH"). Periksa menggunakan relasi `lexid-s:repealedBy` untuk "DICABUT", `lexid-s:amendedBy` untuk "DIUBAH" pada peraturan yang ditanyakan, ATAU `lexid-s:repeals` untuk "MENCABUT", atau `lexid-s:amends` untuk "MENGUBAH" pada peraturan lain tersebut.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""
SELECT_SPARQL_GEN_5_SHOT_PROMPT = """## Task: Generate SPARQL SELECT statement to query a graph database from a natural language question.

### Instructions:
Avoid using all properties as variables.
Use ONLY the classes and properties provided in the ontology schema to construct the SPARQL query.
Include all necessary prefixes.
DO NOT use any classes or properties that are NOT EXPLICITLY PROVIDED in the ontology schema.
Use OPTIONAL and CONTAINS clause to do entity matching ONLY TO the `rdfs:label` OR `lexid-s:name` to do a fuzzy match.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

### Example:
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

### EXAMPLE ONE
### User Query: Peraturan apa yang dihapus oleh UU Nomor 7 Tahun 1948?
### Generated SPARQL SELECT Query:
```
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?regulation ?label ?name
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?label ;
    lexid-s:repealedBy ?repealingRegulation .
  ?repealingRegulation lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
  OPTIONAL {{ ?regulation lexid-s:name ?name . }}
}}
```

### EXAMPLE TWO
### User Query: Apa tujuan dari peraturan Undang-Undang Republik Indonesia Nomor 30 Tahun 2002?
### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?label ?considerant
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
### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?regulation ?legalBasis
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?regulationLabel ;
    lexid-s:hasLegalBasis ?legalBasis ;
    lexid-s:hasRegulationNumber "6" ;
    lexid-s:hasRegulationYear "1987" .
  ?legalBasis rdfs:label ?legalBasisLabel
}}
```

### EXAMPLE FOUR
### User Query: Apakah Undang Undang Tahun 2004 No 10 masih relevan?
### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?regulation ?repealingRegulation ?status
WHERE {{
    ?regulation a lexid-s:LegalDocument ;
    	lexid-s:repealedBy ?repealingRegulation ;
    	lexid-s:hasRegulationNumber "10" ;
    	lexid-s:hasRegulationYear "2004" .
    OPTIONAL {{ ?regulation lexid-s:status ?status . }}
}}
```

### EXAMPLE FIVE
### User Query: Di manakah UU No. 12 Thn 2011 ditetapkan?
### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?regulation ?enactionLocation
WHERE {{
    ?regulation a lexid-s:LegalDocument ;
    	lexid-s:hasEnactionLocation ?enactionLocation ;
    	lexid-s:hasRegulationYear "2011" ;
    	lexid-s:hasRegulationNumber "12" .
}}
```

### Note:
Do NOT include any explanations or apologies in your responses.
Do NOT wrap the query in backticks.
Do NOT return this input prompt to the output
Do NOT include any text except the SPARQL query generated.
Do NOT respond to any questions that might ask anything else than for you to generate a SPARQL SELECT statement.
Only return the SPARQL SELECT statement that you already generate.

Jika seorang pengguna menanyakan apakah suatu peraturan MASIH RELEVAN atau MASIH BERLAKU, Anda perlu memeriksa apakah peraturan tersebut telah "DICABUT" atau "DIUBAH" oleh peraturan lain, atau apakah peraturan lain "MENCABUT" atau "MENGUBAH" peraturan tersebut (Pilih hanya salah satu pasangan, "DICABUT" - "DIUBAH" atau "MENCABUT" - "MENGUBAH"). Periksa menggunakan relasi `lexid-s:repealedBy` untuk "DICABUT", `lexid-s:amendedBy` untuk "DIUBAH" pada peraturan yang ditanyakan, ATAU `lexid-s:repeals` untuk "MENCABUT", atau `lexid-s:amends` untuk "MENGUBAH" pada peraturan lain tersebut.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""


#######################################################################################################################
# GRAPHDB CONSTRUCT COT SECTION
#######################################################################################################################
CONSTRUCT_SPARQL_GEN_COT_0_SHOT_PROMPT = """## Task: Generate SPARQL CONSTRUCT statement to query a graph database from a natural language question.

You are an helpful assistant for SPARQL CONSTRUCT query generation tasks. Use the context provided to answer the question. Follow these guidelines and explain your reasoning internally at each step, but only output the final answer.

### Step-by-Step Guide:

1. **Break down the user's question:**
- Identify the subject: What is the primary thing the user is asking about? This could be a legal document, a law, or a regulation.
- Identify the relationship(s): What is the user trying to know about the subject? For example, is the user asking if a regulation is amended, repealed, or still valid?
- Identify any specific entities: Look for names or numbers mentioned in the question. Are there specific laws, dates, or entities name the user refers to?

2. **Entity matching:**
- Use the classes defined in the ontology schema to determine the entities based on the previous step. 
- Use the `rdfs:label` or `lexid-s:name` properties to match entities mentioned in the question. If the user refers to a specific regulation by name or number, ensure that these are linked properly to the entities.
- You may need to use the `OPTIONAL` and `CONTAINS` clauses to do a fuzzy match or handle cases where the exact name or number may not be available in the graph.

3. **Identify relevant relationships:**
Based on the user's question, determine which relationships in the ontology schema are relevant. For example:

If the user asks about laws that were "repealed" or "amended", you will need to use relationships like:

- `lexid-s:repealedBy` (for laws repealed by other laws)
- `lexid-s:amendedBy` (for laws amended by other laws)
- `lexid-s:repeals` (for laws that repeal other laws)
- `lexid-s:amends` (for laws that amend other laws)

Use the provided ontology schema for more details of relationships.

4. **Construct the query:**
- Start by constructing the `CONSTRUCT` part of the query, indicating what entities or relationships you need to retrieve. Match the relation name with the language that used on the question.
- Then, build the `WHERE` clause to specify the conditions of the query. This will typically involve checking the relevant relationships such as `lexid-s:repealedBy` for repealed laws, or `lexid-s:hasRegulationNumber` for specific regulation number. Ensure that the subject (regulation or law) and target entities match the user's input.
- Make sure to include the appropriate `PREFIX` statements at the top of the query for the namespaces (`rdf`, `rdfs`, `lexid`, `lexid-s`). See more details of prefixes on the provided ontology schema.
- If the question includes an entity name or number, use a condition to match the label or name using the `rdfs:label` or `lexid-s:name`.

5. **If the user's question asks about whether a regulation is still relevant or still valid, think about the relationships that imply whether a regulation has been repealed or amended by another regulation.** Specifically:
- Check the `lexid-s:repealedBy` or `lexid-s:amendedBy` properties for the regulation in question.
- Alternatively, check the `lexid-s:repeals` or `lexid-s:amends` properties for other regulations.

### Important: Do not include the steps in the answer; only output the final answer directly.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

### Note:
- Do NOT use all properties as variables.
- Do NOT include any explanations or apologies in your responses.
- Do NOT wrap the query in backticks.
- Do NOT return this input prompt to the output.
- Do NOT include any text except the SPARQL query generated.
- Do NOT respond to any questions that might ask anything else than for you to generate a SPARQL CONSTRUCT statement.
- Do ONLY return the SPARQL CONSTRUCT statement you generate after thinking through the steps outlined above.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""

CONSTRUCT_SPARQL_GEN_COT_1_SHOT_PROMPT = """## Task: Generate SPARQL CONSTRUCT statement to query a graph database from a natural language question.

You are an helpful assistant for SPARQL CONSTRUCT query generation tasks. Use the context provided to answer the question. Follow these guidelines and explain your reasoning internally at each step, but only output the final answer.

### Step-by-Step Guide:

1. **Break down the user's question:**
- Identify the subject: What is the primary thing the user is asking about? This could be a legal document, a law, or a regulation.
- Identify the relationship(s): What is the user trying to know about the subject? For example, is the user asking if a regulation is amended, repealed, or still valid?
- Identify any specific entities: Look for names or numbers mentioned in the question. Are there specific laws, dates, or entities name the user refers to?

2. **Entity matching:**
- Use the classes defined in the ontology schema to determine the entities based on the previous step. 
- Use the `rdfs:label` or `lexid-s:name` properties to match entities mentioned in the question. If the user refers to a specific regulation by name or number, ensure that these are linked properly to the entities.
- You may need to use the `OPTIONAL` and `CONTAINS` clauses to do a fuzzy match or handle cases where the exact name or number may not be available in the graph.

3. **Identify relevant relationships:**
Based on the user's question, determine which relationships in the ontology schema are relevant. For example:

If the user asks about laws that were "repealed" or "amended", you will need to use relationships like:

- `lexid-s:repealedBy` (for laws repealed by other laws)
- `lexid-s:amendedBy` (for laws amended by other laws)
- `lexid-s:repeals` (for laws that repeal other laws)
- `lexid-s:amends` (for laws that amend other laws)

Use the provided ontology schema for more details of relationships.

4. **Construct the query:**
- Start by constructing the `CONSTRUCT` part of the query, indicating what entities or relationships you need to retrieve. Match the relation name with the language that used on the question.
- Then, build the `WHERE` clause to specify the conditions of the query. This will typically involve checking the relevant relationships such as `lexid-s:repealedBy` for repealed laws, or `lexid-s:hasRegulationNumber` for specific regulation number. Ensure that the subject (regulation or law) and target entities match the user's input.
- Make sure to include the appropriate `PREFIX` statements at the top of the query for the namespaces (`rdf`, `rdfs`, `lexid`, `lexid-s`). See more details of prefixes on the provided ontology schema.
- If the question includes an entity name or number, use a condition to match the label or name using the `rdfs:label` or `lexid-s:name`.

5. **If the user's question asks about whether a regulation is still relevant or still valid, think about the relationships that imply whether a regulation has been repealed or amended by another regulation.** Specifically:
- Check the `lexid-s:repealedBy` or `lexid-s:amendedBy` properties for the regulation in question.
- Alternatively, check the `lexid-s:repeals` or `lexid-s:amends` properties for other regulations.

### Important: Do not include the steps in the answer; only output the final answer directly.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

## Example
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

### EXAMPLE ONE
### User Query: Peraturan apa yang dihapus oleh UU Nomor 7 Tahun 1948?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The primary subject is UU Nomor 7 Tahun 1948, which is a regulation.
- Relationship(s): The user is asking about a repealed law, i.e., what other regulation was repealed by this law.
- Specific Entity: The law number 7 and the year 1948 are specifically mentioned.

2. **Entity matching:**
- We will match the UU Nomor 7 Tahun 1948 by its regulation number and year using properties like `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`. This will ensure we retrieve the specific law.

3. **Identifying relevant relationships:**
- The key relationship is `lexid-s:repealedBy`, which shows the law that repeals other laws.
- In this case, we are looking for other regulations that have been repealed by UU Nomor 7 Tahun 1948.

4. **Construct the query:**
- The CONSTRUCT clause will specify that we want to retrieve the law being repealed (`?repealedregulation`) and the law that repeals it (`?regulation`).
- The WHERE clause will define the conditions; we will filter by `lexid-s:repealedBy`, matching the specific regulation number and year (7, 1948), and also match the name or label of the repealed law using relationships listed in the ontology schema.

### Generated SPARQL CONSTRUCT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

CONSTRUCT {{
   ?regulation lexid-s:dihapus ?repealingRegulation .
}}
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    lexid-s:repealedBy ?repealingRegulation ;
    rdfs:label ?label .
  ?repealingRegulation lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
  OPTIONAL {{ ?repealedRegulation lexid-s:name ?name . }}
}}
```

### Note:
- Do NOT use all properties as variables.
- Do NOT include any explanations or apologies in your responses.
- Do NOT wrap the query in backticks.
- Do NOT return this input prompt to the output.
- Do NOT include any text except the SPARQL query generated.
- Do NOT respond to any questions that might ask anything else than for you to generate a SPARQL CONSTRUCT statement.
- Do ONLY return the SPARQL CONSTRUCT statement you generate after thinking through the steps outlined above.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""
CONSTRUCT_SPARQL_GEN_COT_2_SHOT_PROMPT = """## Task: Generate SPARQL CONSTRUCT statement to query a graph database from a natural language question.

You are an helpful assistant for SPARQL CONSTRUCT query generation tasks. Use the context provided to answer the question. Follow these guidelines and explain your reasoning internally at each step, but only output the final answer.

### Step-by-Step Guide:

1. **Break down the user's question:**
- Identify the subject: What is the primary thing the user is asking about? This could be a legal document, a law, or a regulation.
- Identify the relationship(s): What is the user trying to know about the subject? For example, is the user asking if a regulation is amended, repealed, or still valid?
- Identify any specific entities: Look for names or numbers mentioned in the question. Are there specific laws, dates, or entities name the user refers to?

2. **Entity matching:**
- Use the classes defined in the ontology schema to determine the entities based on the previous step. 
- Use the `rdfs:label` or `lexid-s:name` properties to match entities mentioned in the question. If the user refers to a specific regulation by name or number, ensure that these are linked properly to the entities.
- You may need to use the `OPTIONAL` and `CONTAINS` clauses to do a fuzzy match or handle cases where the exact name or number may not be available in the graph.

3. **Identify relevant relationships:**
Based on the user's question, determine which relationships in the ontology schema are relevant. For example:

If the user asks about laws that were "repealed" or "amended", you will need to use relationships like:

- `lexid-s:repealedBy` (for laws repealed by other laws)
- `lexid-s:amendedBy` (for laws amended by other laws)
- `lexid-s:repeals` (for laws that repeal other laws)
- `lexid-s:amends` (for laws that amend other laws)

Use the provided ontology schema for more details of relationships.

4. **Construct the query:**
- Start by constructing the `CONSTRUCT` part of the query, indicating what entities or relationships you need to retrieve. Match the relation name with the language that used on the question.
- Then, build the `WHERE` clause to specify the conditions of the query. This will typically involve checking the relevant relationships such as `lexid-s:repealedBy` for repealed laws, or `lexid-s:hasRegulationNumber` for specific regulation number. Ensure that the subject (regulation or law) and target entities match the user's input.
- Make sure to include the appropriate `PREFIX` statements at the top of the query for the namespaces (`rdf`, `rdfs`, `lexid`, `lexid-s`). See more details of prefixes on the provided ontology schema.
- If the question includes an entity name or number, use a condition to match the label or name using the `rdfs:label` or `lexid-s:name`.

5. **If the user's question asks about whether a regulation is still relevant or still valid, think about the relationships that imply whether a regulation has been repealed or amended by another regulation.** Specifically:
- Check the `lexid-s:repealedBy` or `lexid-s:amendedBy` properties for the regulation in question.
- Alternatively, check the `lexid-s:repeals` or `lexid-s:amends` properties for other regulations.

### Important: Do not include the steps in the answer; only output the final answer directly.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

## Example
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

### EXAMPLE ONE
### User Query: Peraturan apa yang dihapus oleh UU Nomor 7 Tahun 1948?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The primary subject is UU Nomor 7 Tahun 1948, which is a regulation.
- Relationship(s): The user is asking about a repealed law, i.e., what other regulation was repealed by this law.
- Specific Entity: The law number 7 and the year 1948 are specifically mentioned.

2. **Entity matching:**
- We will match the UU Nomor 7 Tahun 1948 by its regulation number and year using properties like `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`. This will ensure we retrieve the specific law.

3. **Identifying relevant relationships:**
- The key relationship is `lexid-s:repealedBy`, which shows the law that repeals other laws.
- In this case, we are looking for other regulations that have been repealed by UU Nomor 7 Tahun 1948.

4. **Construct the query:**
- The CONSTRUCT clause will specify that we want to retrieve the law being repealed (`?repealedregulation`) and the law that repeals it (`?regulation`).
- The WHERE clause will define the conditions; we will filter by `lexid-s:repealedBy`, matching the specific regulation number and year (7, 1948), and also match the name or label of the repealed law using relationships listed in the ontology schema.

### Generated SPARQL CONSTRUCT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

CONSTRUCT {{
   ?regulation lexid-s:dihapus ?repealingRegulation .
}}
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    lexid-s:repealedBy ?repealingRegulation ;
    rdfs:label ?label .
  ?repealingRegulation lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
  OPTIONAL {{ ?repealedRegulation lexid-s:name ?name . }}
}}
```

### EXAMPLE TWO
### User Query: Apa tujuan dari peraturan Undang-Undang Republik Indonesia Nomor 30 Tahun 2002?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking about the purpose of a specific regulation, UU Nomor 30 Tahun 2002.
- Relationship(s): The user is interested in the purpose or goal of the law.
- Specific Entity: UU Nomor 30 Tahun 2002 is explicitly named.

2. **Entity matching:**
- We will match UU Nomor 30 Tahun 2002 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear` properties.

3. **Identifying relevant relationships:**
- The relevant relationship here is `lexid-s:considers`, which indicates the purpose or considerations of the law.

4. **Construct the query:**
- The CONSTRUCT clause will specify that we want to retrieve the law's purpose (?considerant).
- The WHERE clause will use `lexid-s:considers` to retrieve the law's purpose, matched using the same variable used in the CONSTRUCT CLAUSE
- Capture the correct regulation using regulation number and year (30 and 2002).

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

### Note:
- Do NOT use all properties as variables.
- Do NOT include any explanations or apologies in your responses.
- Do NOT wrap the query in backticks.
- Do NOT return this input prompt to the output.
- Do NOT include any text except the SPARQL query generated.
- Do NOT respond to any questions that might ask anything else than for you to generate a SPARQL CONSTRUCT statement.
- Do ONLY return the SPARQL CONSTRUCT statement you generate after thinking through the steps outlined above.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""
CONSTRUCT_SPARQL_GEN_COT_3_SHOT_PROMPT = """## Task: Generate SPARQL CONSTRUCT statement to query a graph database from a natural language question.

You are an helpful assistant for SPARQL CONSTRUCT query generation tasks. Use the context provided to answer the question. Follow these guidelines and explain your reasoning internally at each step, but only output the final answer.

### Step-by-Step Guide:

1. **Break down the user's question:**
- Identify the subject: What is the primary thing the user is asking about? This could be a legal document, a law, or a regulation.
- Identify the relationship(s): What is the user trying to know about the subject? For example, is the user asking if a regulation is amended, repealed, or still valid?
- Identify any specific entities: Look for names or numbers mentioned in the question. Are there specific laws, dates, or entities name the user refers to?

2. **Entity matching:**
- Use the classes defined in the ontology schema to determine the entities based on the previous step. 
- Use the `rdfs:label` or `lexid-s:name` properties to match entities mentioned in the question. If the user refers to a specific regulation by name or number, ensure that these are linked properly to the entities.
- You may need to use the `OPTIONAL` and `CONTAINS` clauses to do a fuzzy match or handle cases where the exact name or number may not be available in the graph.

3. **Identify relevant relationships:**
Based on the user's question, determine which relationships in the ontology schema are relevant. For example:

If the user asks about laws that were "repealed" or "amended", you will need to use relationships like:

- `lexid-s:repealedBy` (for laws repealed by other laws)
- `lexid-s:amendedBy` (for laws amended by other laws)
- `lexid-s:repeals` (for laws that repeal other laws)
- `lexid-s:amends` (for laws that amend other laws)

Use the provided ontology schema for more details of relationships.

4. **Construct the query:**
- Start by constructing the `CONSTRUCT` part of the query, indicating what entities or relationships you need to retrieve. Match the relation name with the language that used on the question.
- Then, build the `WHERE` clause to specify the conditions of the query. This will typically involve checking the relevant relationships such as `lexid-s:repealedBy` for repealed laws, or `lexid-s:hasRegulationNumber` for specific regulation number. Ensure that the subject (regulation or law) and target entities match the user's input.
- Make sure to include the appropriate `PREFIX` statements at the top of the query for the namespaces (`rdf`, `rdfs`, `lexid`, `lexid-s`). See more details of prefixes on the provided ontology schema.
- If the question includes an entity name or number, use a condition to match the label or name using the `rdfs:label` or `lexid-s:name`.

5. **If the user's question asks about whether a regulation is still relevant or still valid, think about the relationships that imply whether a regulation has been repealed or amended by another regulation.** Specifically:
- Check the `lexid-s:repealedBy` or `lexid-s:amendedBy` properties for the regulation in question.
- Alternatively, check the `lexid-s:repeals` or `lexid-s:amends` properties for other regulations.

### Important: Do not include the steps in the answer; only output the final answer directly.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

## Example
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

### EXAMPLE ONE
### User Query: Peraturan apa yang dihapus oleh UU Nomor 7 Tahun 1948?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The primary subject is UU Nomor 7 Tahun 1948, which is a regulation.
- Relationship(s): The user is asking about a repealed law, i.e., what other regulation was repealed by this law.
- Specific Entity: The law number 7 and the year 1948 are specifically mentioned.

2. **Entity matching:**
- We will match the UU Nomor 7 Tahun 1948 by its regulation number and year using properties like `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`. This will ensure we retrieve the specific law.

3. **Identifying relevant relationships:**
- The key relationship is `lexid-s:repealedBy`, which shows the law that repeals other laws.
- In this case, we are looking for other regulations that have been repealed by UU Nomor 7 Tahun 1948.

4. **Construct the query:**
- The CONSTRUCT clause will specify that we want to retrieve the law being repealed (`?repealedregulation`) and the law that repeals it (`?regulation`).
- The WHERE clause will define the conditions; we will filter by `lexid-s:repealedBy`, matching the specific regulation number and year (7, 1948), and also match the name or label of the repealed law using relationships listed in the ontology schema.

### Generated SPARQL CONSTRUCT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

CONSTRUCT {{
   ?regulation lexid-s:dihapus ?repealingRegulation .
}}
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    lexid-s:repealedBy ?repealingRegulation ;
    rdfs:label ?label .
  ?repealingRegulation lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
  OPTIONAL {{ ?repealedRegulation lexid-s:name ?name . }}
}}
```

### EXAMPLE TWO
### User Query: Apa tujuan dari peraturan Undang-Undang Republik Indonesia Nomor 30 Tahun 2002?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking about the purpose of a specific regulation, UU Nomor 30 Tahun 2002.
- Relationship(s): The user is interested in the purpose or goal of the law.
- Specific Entity: UU Nomor 30 Tahun 2002 is explicitly named.

2. **Entity matching:**
- We will match UU Nomor 30 Tahun 2002 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear` properties.

3. **Identifying relevant relationships:**
- The relevant relationship here is `lexid-s:considers`, which indicates the purpose or considerations of the law.

4. **Construct the query:**
- The CONSTRUCT clause will specify that we want to retrieve the law's purpose (?considerant).
- The WHERE clause will use `lexid-s:considers` to retrieve the law's purpose, matched using the same variable used in the CONSTRUCT CLAUSE
- Capture the correct regulation using regulation number and year (30 and 2002).

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
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking about the legal basis of a specific law, UU No. 6 Tahun 1987.
- Relationship(s): The user wants to know the legal basis of the law.
- Specific Entity: The law No. 6, 1987 is named.

2. **Entity matching:**
- We will match UU No. 6 Tahun 1987 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`.

3. **Identifying relevant relationships:**
- The relevant relationship here is `lexid-s:hasLegalBasis`.

4. **Construct the query:**
- The CONSTRUCT clause will specify that we want to retrieve the legal basis (`?legalBasis`) for the law.
- The WHERE clause will use `lexid-s:hasLegalBasis` to find the law’s legal basis, while filtering by regulation number and year (6 and 1987).

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

### Note:
- Do NOT use all properties as variables.
- Do NOT include any explanations or apologies in your responses.
- Do NOT wrap the query in backticks.
- Do NOT return this input prompt to the output.
- Do NOT include any text except the SPARQL query generated.
- Do NOT respond to any questions that might ask anything else than for you to generate a SPARQL CONSTRUCT statement.
- Do ONLY return the SPARQL CONSTRUCT statement you generate after thinking through the steps outlined above.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""

CONSTRUCT_SPARQL_GEN_COT_4_SHOT_PROMPT = """## Task: Generate SPARQL CONSTRUCT statement to query a graph database from a natural language question.

You are an helpful assistant for SPARQL CONSTRUCT query generation tasks. Use the context provided to answer the question. Follow these guidelines and explain your reasoning internally at each step, but only output the final answer.

### Step-by-Step Guide:

1. **Break down the user's question:**
- Identify the subject: What is the primary thing the user is asking about? This could be a legal document, a law, or a regulation.
- Identify the relationship(s): What is the user trying to know about the subject? For example, is the user asking if a regulation is amended, repealed, or still valid?
- Identify any specific entities: Look for names or numbers mentioned in the question. Are there specific laws, dates, or entities name the user refers to?

2. **Entity matching:**
- Use the classes defined in the ontology schema to determine the entities based on the previous step. 
- Use the `rdfs:label` or `lexid-s:name` properties to match entities mentioned in the question. If the user refers to a specific regulation by name or number, ensure that these are linked properly to the entities.
- You may need to use the `OPTIONAL` and `CONTAINS` clauses to do a fuzzy match or handle cases where the exact name or number may not be available in the graph.

3. **Identify relevant relationships:**
Based on the user's question, determine which relationships in the ontology schema are relevant. For example:

If the user asks about laws that were "repealed" or "amended", you will need to use relationships like:

- `lexid-s:repealedBy` (for laws repealed by other laws)
- `lexid-s:amendedBy` (for laws amended by other laws)
- `lexid-s:repeals` (for laws that repeal other laws)
- `lexid-s:amends` (for laws that amend other laws)

Use the provided ontology schema for more details of relationships.

4. **Construct the query:**
- Start by constructing the `CONSTRUCT` part of the query, indicating what entities or relationships you need to retrieve. Match the relation name with the language that used on the question.
- Then, build the `WHERE` clause to specify the conditions of the query. This will typically involve checking the relevant relationships such as `lexid-s:repealedBy` for repealed laws, or `lexid-s:hasRegulationNumber` for specific regulation number. Ensure that the subject (regulation or law) and target entities match the user's input.
- Make sure to include the appropriate `PREFIX` statements at the top of the query for the namespaces (`rdf`, `rdfs`, `lexid`, `lexid-s`). See more details of prefixes on the provided ontology schema.
- If the question includes an entity name or number, use a condition to match the label or name using the `rdfs:label` or `lexid-s:name`.

5. **If the user's question asks about whether a regulation is still relevant or still valid, think about the relationships that imply whether a regulation has been repealed or amended by another regulation.** Specifically:
- Check the `lexid-s:repealedBy` or `lexid-s:amendedBy` properties for the regulation in question.
- Alternatively, check the `lexid-s:repeals` or `lexid-s:amends` properties for other regulations.

### Important: Do not include the steps in the answer; only output the final answer directly.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

## Example
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

### EXAMPLE ONE
### User Query: Peraturan apa yang dihapus oleh UU Nomor 7 Tahun 1948?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The primary subject is UU Nomor 7 Tahun 1948, which is a regulation.
- Relationship(s): The user is asking about a repealed law, i.e., what other regulation was repealed by this law.
- Specific Entity: The law number 7 and the year 1948 are specifically mentioned.

2. **Entity matching:**
- We will match the UU Nomor 7 Tahun 1948 by its regulation number and year using properties like `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`. This will ensure we retrieve the specific law.

3. **Identifying relevant relationships:**
- The key relationship is `lexid-s:repealedBy`, which shows the law that repeals other laws.
- In this case, we are looking for other regulations that have been repealed by UU Nomor 7 Tahun 1948.

4. **Construct the query:**
- The CONSTRUCT clause will specify that we want to retrieve the law being repealed (`?repealedregulation`) and the law that repeals it (`?regulation`).
- The WHERE clause will define the conditions; we will filter by `lexid-s:repealedBy`, matching the specific regulation number and year (7, 1948), and also match the name or label of the repealed law using relationships listed in the ontology schema.

### Generated SPARQL CONSTRUCT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

CONSTRUCT {{
   ?regulation lexid-s:dihapus ?repealingRegulation .
}}
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    lexid-s:repealedBy ?repealingRegulation ;
    rdfs:label ?label .
  ?repealingRegulation lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
  OPTIONAL {{ ?repealedRegulation lexid-s:name ?name . }}
}}
```

### EXAMPLE TWO
### User Query: Apa tujuan dari peraturan Undang-Undang Republik Indonesia Nomor 30 Tahun 2002?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking about the purpose of a specific regulation, UU Nomor 30 Tahun 2002.
- Relationship(s): The user is interested in the purpose or goal of the law.
- Specific Entity: UU Nomor 30 Tahun 2002 is explicitly named.

2. **Entity matching:**
- We will match UU Nomor 30 Tahun 2002 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear` properties.

3. **Identifying relevant relationships:**
- The relevant relationship here is `lexid-s:considers`, which indicates the purpose or considerations of the law.

4. **Construct the query:**
- The CONSTRUCT clause will specify that we want to retrieve the law's purpose (?considerant).
- The WHERE clause will use `lexid-s:considers` to retrieve the law's purpose, matched using the same variable used in the CONSTRUCT CLAUSE
- Capture the correct regulation using regulation number and year (30 and 2002).

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
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking about the legal basis of a specific law, UU No. 6 Tahun 1987.
- Relationship(s): The user wants to know the legal basis of the law.
- Specific Entity: The law No. 6, 1987 is named.

2. **Entity matching:**
- We will match UU No. 6 Tahun 1987 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`.

3. **Identifying relevant relationships:**
- The relevant relationship here is `lexid-s:hasLegalBasis`.

4. **Construct the query:**
- The CONSTRUCT clause will specify that we want to retrieve the legal basis (`?legalBasis`) for the law.
- The WHERE clause will use `lexid-s:hasLegalBasis` to find the law’s legal basis, while filtering by regulation number and year (6 and 1987).

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

### EXAMPLE FOUR
### User Query: Apakah Undang Undang Tahun 2004 No 10 masih relevan?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking if UU No. 10 Tahun 2004 is still relevant.
- Relationship(s): The user wants to know if this law is still valid or has been repealed or amended.
- Specific Entity: UU No. 10 Tahun 2004 is the regulation in question.

2. **Entity matching:**
- We will match UU No. 10 Tahun 2004 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`.

3. **Identifying relevant relationships:**
- The relevant relationships here are `lexid-s:repealedBy` and `lexid-s:amendedBy`, which indicate whether the law has been repealed or amended, respectively.

4. **Construct the query:**
- The CONSTRUCT clause will specify that we want to retrieve the law’s status (whether it’s been repealed or amended) and its relationship with other regulations.
- The WHERE clause will check for the `lexid-s:repealedBy` and `lexid-s:amendedBy` relationships, filtering by the law number and year (10 and 2004).

### Generated SPARQL CONSTRUCT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

CONSTRUCT {{
    ?regulation lexid-s:dicabutOleh ?otherRegulation .
    ?regulation lexid-s:status ?status .
}}
WHERE {{
    ?regulation a lexid-s:LegalDocument ;
    	lexid-s:repealedBy ?otherRegulation ;
    	lexid-s:hasRegulationNumber "10" ;
    	lexid-s:hasRegulationYear "2004" .
    OPTIONAL {{ ?regulation lexid-s:status ?status . }}
}}
```

### Note:
- Do NOT use all properties as variables.
- Do NOT include any explanations or apologies in your responses.
- Do NOT wrap the query in backticks.
- Do NOT return this input prompt to the output.
- Do NOT include any text except the SPARQL query generated.
- Do NOT respond to any questions that might ask anything else than for you to generate a SPARQL CONSTRUCT statement.
- Do ONLY return the SPARQL CONSTRUCT statement you generate after thinking through the steps outlined above.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""

CONSTRUCT_SPARQL_GEN_COT_5_SHOT_PROMPT = """## Task: Generate SPARQL CONSTRUCT statement to query a graph database from a natural language question.

You are an helpful assistant for SPARQL CONSTRUCT query generation tasks. Use the context provided to answer the question. Follow these guidelines and explain your reasoning internally at each step, but only output the final answer.

### Step-by-Step Guide:

1. **Break down the user's question:**
- Identify the subject: What is the primary thing the user is asking about? This could be a legal document, a law, or a regulation.
- Identify the relationship(s): What is the user trying to know about the subject? For example, is the user asking if a regulation is amended, repealed, or still valid?
- Identify any specific entities: Look for names or numbers mentioned in the question. Are there specific laws, dates, or entities name the user refers to?

2. **Entity matching:**
- Use the classes defined in the ontology schema to determine the entities based on the previous step. 
- Use the `rdfs:label` or `lexid-s:name` properties to match entities mentioned in the question. If the user refers to a specific regulation by name or number, ensure that these are linked properly to the entities.
- You may need to use the `OPTIONAL` and `CONTAINS` clauses to do a fuzzy match or handle cases where the exact name or number may not be available in the graph.

3. **Identify relevant relationships:**
Based on the user's question, determine which relationships in the ontology schema are relevant. For example:

If the user asks about laws that were "repealed" or "amended", you will need to use relationships like:

- `lexid-s:repealedBy` (for laws repealed by other laws)
- `lexid-s:amendedBy` (for laws amended by other laws)
- `lexid-s:repeals` (for laws that repeal other laws)
- `lexid-s:amends` (for laws that amend other laws)

Use the provided ontology schema for more details of relationships.

4. **Construct the query:**
- Start by constructing the `CONSTRUCT` part of the query, indicating what entities or relationships you need to retrieve. Match the relation name with the language that used on the question.
- Then, build the `WHERE` clause to specify the conditions of the query. This will typically involve checking the relevant relationships such as `lexid-s:repealedBy` for repealed laws, or `lexid-s:hasRegulationNumber` for specific regulation number. Ensure that the subject (regulation or law) and target entities match the user's input.
- Make sure to include the appropriate `PREFIX` statements at the top of the query for the namespaces (`rdf`, `rdfs`, `lexid`, `lexid-s`). See more details of prefixes on the provided ontology schema.
- If the question includes an entity name or number, use a condition to match the label or name using the `rdfs:label` or `lexid-s:name`.

5. **If the user's question asks about whether a regulation is still relevant or still valid, think about the relationships that imply whether a regulation has been repealed or amended by another regulation.** Specifically:
- Check the `lexid-s:repealedBy` or `lexid-s:amendedBy` properties for the regulation in question.
- Alternatively, check the `lexid-s:repeals` or `lexid-s:amends` properties for other regulations.

### Important: Do not include the steps in the answer; only output the final answer directly.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

## Example
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

### EXAMPLE ONE
### User Query: Peraturan apa yang dihapus oleh UU Nomor 7 Tahun 1948?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The primary subject is UU Nomor 7 Tahun 1948, which is a regulation.
- Relationship(s): The user is asking about a repealed law, i.e., what other regulation was repealed by this law.
- Specific Entity: The law number 7 and the year 1948 are specifically mentioned.

2. **Entity matching:**
- We will match the UU Nomor 7 Tahun 1948 by its regulation number and year using properties like `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`. This will ensure we retrieve the specific law.

3. **Identifying relevant relationships:**
- The key relationship is `lexid-s:repealedBy`, which shows the law that repeals other laws.
- In this case, we are looking for other regulations that have been repealed by UU Nomor 7 Tahun 1948.

4. **Construct the query:**
- The CONSTRUCT clause will specify that we want to retrieve the law being repealed (`?repealedregulation`) and the law that repeals it (`?regulation`).
- The WHERE clause will define the conditions; we will filter by `lexid-s:repealedBy`, matching the specific regulation number and year (7, 1948), and also match the name or label of the repealed law using relationships listed in the ontology schema.

### Generated SPARQL CONSTRUCT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

CONSTRUCT {{
   ?regulation lexid-s:dihapus ?repealedRegulation .
}}
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    lexid-s:repealedBy ?repealedRegulation .
  ?repealedRegulation rdfs:label ?label ;
    lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
    
  OPTIONAL {{ ?repealedRegulation lexid-s:name ?name . }}
}}

### EXAMPLE TWO
### User Query: Apa tujuan dari peraturan Undang-Undang Republik Indonesia Nomor 30 Tahun 2002?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking about the purpose of a specific regulation, UU Nomor 30 Tahun 2002.
- Relationship(s): The user is interested in the purpose or goal of the law.
- Specific Entity: UU Nomor 30 Tahun 2002 is explicitly named.

2. **Entity matching:**
- We will match UU Nomor 30 Tahun 2002 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear` properties.

3. **Identifying relevant relationships:**
- The relevant relationship here is `lexid-s:considers`, which indicates the purpose or considerations of the law.

4. **Construct the query:**
- The CONSTRUCT clause will specify that we want to retrieve the law's purpose (?considerant).
- The WHERE clause will use `lexid-s:considers` to retrieve the law's purpose, matched using the same variable used in the CONSTRUCT CLAUSE
- Capture the correct regulation using regulation number and year (30 and 2002).

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
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking about the legal basis of a specific law, UU No. 6 Tahun 1987.
- Relationship(s): The user wants to know the legal basis of the law.
- Specific Entity: The law No. 6, 1987 is named.

2. **Entity matching:**
- We will match UU No. 6 Tahun 1987 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`.

3. **Identifying relevant relationships:**
- The relevant relationship here is `lexid-s:hasLegalBasis`.

4. **Construct the query:**
- The CONSTRUCT clause will specify that we want to retrieve the legal basis (`?legalBasis`) for the law.
- The WHERE clause will use `lexid-s:hasLegalBasis` to find the law’s legal basis, while filtering by regulation number and year (6 and 1987).

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

### EXAMPLE FOUR
### User Query: Apakah Undang Undang Tahun 2004 No 10 masih relevan?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking if UU No. 10 Tahun 2004 is still relevant.
- Relationship(s): The user wants to know if this law is still valid or has been repealed or amended.
- Specific Entity: UU No. 10 Tahun 2004 is the regulation in question.

2. **Entity matching:**
- We will match UU No. 10 Tahun 2004 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`.

3. **Identifying relevant relationships:**
- The relevant relationships here are `lexid-s:repealedBy` and `lexid-s:amendedBy`, which indicate whether the law has been repealed or amended, respectively.

4. **Construct the query:**
- The CONSTRUCT clause will specify that we want to retrieve the law’s status (whether it’s been repealed or amended) and its relationship with other regulations.
- The WHERE clause will check for the `lexid-s:repealedBy` and `lexid-s:amendedBy` relationships, filtering by the law number and year (10 and 2004).

### Generated SPARQL CONSTRUCT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

CONSTRUCT {{
    ?regulation lexid-s:dicabutOleh ?otherRegulation .
    ?regulation lexid-s:status ?status .
}}
WHERE {{
    ?regulation a lexid-s:LegalDocument ;
    	lexid-s:repealedBy ?otherRegulation ;
    	lexid-s:hasRegulationNumber "10" ;
    	lexid-s:hasRegulationYear "2004" .
    OPTIONAL {{ ?regulation lexid-s:status ?status . }}
}}
```

### EXAMPLE FIVE
### User Query: Di manakah UU No. 12 Thn 2011 ditetapkan?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking about the location where UU No. 12 Tahun 2011 was established.
- Relationship(s): The user is looking for the enaction location of the law.
- Specific Entity: UU No. 12 Tahun 2011 is specified.

2. **Entity matching:**
- We will match UU No. 12 Tahun 2011 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`.

3. **Identifying relevant relationships:**
- The relevant relationship here is `lexid-s:enactionLocation` (established in), which will give us the location where the law was enacted.

4. **Construct the query:**
- The CONSTRUCT clause will specify that we want to retrieve the location of the law's enactment (?enactionLocation).
- The WHERE clause will filter for the law's enactment location using `lexid-s:enactionLocation`, while matching the law number and year (12 and 2011).

### Generated SPARQL CONSTRUCT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

CONSTRUCT {{
    ?regulation lexid-s:ditetapkanDi ?enactionLocation .
}}
WHERE {{
    ?regulation a lexid-s:LegalDocument ;
    	lexid-s:hasEnactionLocation ?enactionLocation ;
    	lexid-s:hasRegulationYear "2011" ;
    	lexid-s:hasRegulationNumber "12" .
}}
```

### Note:
- Do NOT use all properties as variables.
- Do NOT include any explanations or apologies in your responses.
- Do NOT wrap the query in backticks.
- Do NOT return this input prompt to the output.
- Do NOT include any text except the SPARQL query generated.
- Do NOT respond to any questions that might ask anything else than for you to generate a SPARQL CONSTRUCT statement.
- Do ONLY return the SPARQL CONSTRUCT statement you generate after thinking through the steps outlined above.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""

#######################################################################################################################
# GRAPHDB SELECT COT SECTION
#######################################################################################################################
SELECT_SPARQL_GEN_COT_0_SHOT_PROMPT = """## Task: Generate SPARQL SELECT statement to query a graph database from a natural language question.

You are an helpful assistant for SPARQL SELECT query generation tasks. Use the context provided to answer the question. Follow these guidelines and explain your reasoning internally at each step, but only output the final answer.

### Step-by-Step Guide:

1. **Break down the user's question:**
- Identify the subject: What is the primary thing the user is asking about? This could be a legal document, a law, or a regulation.
- Identify the relationship(s): What is the user trying to know about the subject? For example, is the user asking if a regulation is amended, repealed, or still valid?
- Identify any specific entities: Look for names or numbers mentioned in the question. Are there specific laws, dates, or entities name the user refers to?

2. **Entity matching:**
- Use the classes defined in the ontology schema to determine the entities based on the previous step. 
- Use the `rdfs:label` or `lexid-s:name` properties to match entities mentioned in the question. If the user refers to a specific regulation by name or number, ensure that these are linked properly to the entities.
- You may need to use the `OPTIONAL` and `CONTAINS` clauses to do a fuzzy match or handle cases where the exact name or number may not be available in the graph.

3. **Identify relevant relationships:**
Based on the user's question, determine which relationships in the ontology schema are relevant. For example:

If the user asks about laws that were "repealed" or "amended", you will need to use relationships like:

- `lexid-s:repealedBy` (for laws repealed by other laws)
- `lexid-s:amendedBy` (for laws amended by other laws)
- `lexid-s:repeals` (for laws that repeal other laws)
- `lexid-s:amends` (for laws that amend other laws)

Use the provided ontology schema for more details of relationships.

4. **Construct the query:**
- Start by constructing the `SELECT` part of the query, indicating what entities or relationships you need to retrieve. Match the relation name with the language that used on the question.
- Then, build the `WHERE` clause to specify the conditions of the query. This will typically involve checking the relevant relationships such as `lexid-s:repealedBy` for repealed laws, or `lexid-s:hasRegulationNumber` for specific regulation number. Ensure that the subject (regulation or law) and target entities match the user's input.
- Make sure to include the appropriate `PREFIX` statements at the top of the query for the namespaces (`rdf`, `rdfs`, `lexid`, `lexid-s`). See more details of prefixes on the provided ontology schema.
- If the question includes an entity name or number, use a condition to match the label or name using the `rdfs:label` or `lexid-s:name`.

5. **If the user's question asks about whether a regulation is still relevant or still valid, think about the relationships that imply whether a regulation has been repealed or amended by another regulation.** Specifically:
- Check the `lexid-s:repealedBy` or `lexid-s:amendedBy` properties for the regulation in question.
- Alternatively, check the `lexid-s:repeals` or `lexid-s:amends` properties for other regulations.

### Important: Do not include the steps in the answer; only output the final answer directly.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

### Note:
- Do NOT use all properties as variables.
- Do NOT include any explanations or apologies in your responses.
- Do NOT wrap the query in backticks.
- Do NOT return this input prompt to the output.
- Do NOT include any text except the SPARQL query generated.
- Do NOT respond to any questions that might ask anything else than for you to generate a SPARQL SELECT statement.
- Do ONLY return the SPARQL SELECT statement you generate after thinking through the steps outlined above.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""

SELECT_SPARQL_GEN_COT_1_SHOT_PROMPT = """## Task: Generate SPARQL SELECT statement to query a graph database from a natural language question.

You are an helpful assistant for SPARQL SELECT query generation tasks. Use the context provided to answer the question. Follow these guidelines and explain your reasoning internally at each step, but only output the final answer.

### Step-by-Step Guide:

1. **Break down the user's question:**
- Identify the subject: What is the primary thing the user is asking about? This could be a legal document, a law, or a regulation.
- Identify the relationship(s): What is the user trying to know about the subject? For example, is the user asking if a regulation is amended, repealed, or still valid?
- Identify any specific entities: Look for names or numbers mentioned in the question. Are there specific laws, dates, or entities name the user refers to?

2. **Entity matching:**
- Use the classes defined in the ontology schema to determine the entities based on the previous step. 
- Use the `rdfs:label` or `lexid-s:name` properties to match entities mentioned in the question. If the user refers to a specific regulation by name or number, ensure that these are linked properly to the entities.
- You may need to use the `OPTIONAL` and `CONTAINS` clauses to do a fuzzy match or handle cases where the exact name or number may not be available in the graph.

3. **Identify relevant relationships:**
Based on the user's question, determine which relationships in the ontology schema are relevant. For example:

If the user asks about laws that were "repealed" or "amended", you will need to use relationships like:

- `lexid-s:repealedBy` (for laws repealed by other laws)
- `lexid-s:amendedBy` (for laws amended by other laws)
- `lexid-s:repeals` (for laws that repeal other laws)
- `lexid-s:amends` (for laws that amend other laws)

Use the provided ontology schema for more details of relationships.

4. **Construct the query:**
- Start by constructing the `SELECT` part of the query, indicating what entities or relationships you need to retrieve. Match the relation name with the language that used on the question.
- Then, build the `WHERE` clause to specify the conditions of the query. This will typically involve checking the relevant relationships such as `lexid-s:repealedBy` for repealed laws, or `lexid-s:hasRegulationNumber` for specific regulation number. Ensure that the subject (regulation or law) and target entities match the user's input.
- Make sure to include the appropriate `PREFIX` statements at the top of the query for the namespaces (`rdf`, `rdfs`, `lexid`, `lexid-s`). See more details of prefixes on the provided ontology schema.
- If the question includes an entity name or number, use a condition to match the label or name using the `rdfs:label` or `lexid-s:name`.

5. **If the user's question asks about whether a regulation is still relevant or still valid, think about the relationships that imply whether a regulation has been repealed or amended by another regulation.** Specifically:
- Check the `lexid-s:repealedBy` or `lexid-s:amendedBy` properties for the regulation in question.
- Alternatively, check the `lexid-s:repeals` or `lexid-s:amends` properties for other regulations.

### Important: Do not include the steps in the answer; only output the final answer directly.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

## Example
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

### EXAMPLE ONE
### User Query: Peraturan apa yang dihapus oleh UU Nomor 7 Tahun 1948?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The primary subject is UU Nomor 7 Tahun 1948, which is a regulation.
- Relationship(s): The user is asking about a repealed law, i.e., what other regulation was repealed by this law.
- Specific Entity: The law number 7 and the year 1948 are specifically mentioned.

2. **Entity matching:**
- We will match the UU Nomor 7 Tahun 1948 by its regulation number and year using properties like `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`. This will ensure we retrieve the specific law.

3. **Identifying relevant relationships:**
- The key relationship is `lexid-s:repealedBy`, which shows the law that repeals other laws.
- In this case, we are looking for other regulations that have been repealed by UU Nomor 7 Tahun 1948.

4. **Construct the query:**
- The SELECT part will look for the regulation(s) repealed by UU Nomor 7 Tahun 1948 (?regulation) and the label of it (?label). Optionally, we will use the if the regulation has it's official name we will return it also (?name).
- The WHERE clause will define the conditions; we will filter by `lexid-s:repealedBy`, matching the specific regulation number and year (7, 1948), and also match the name or label of the repealed law using relationships listed in the ontology schema.

### Generated SPARQL SELECT Query:
```
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?regulation ?label ?name
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?label ;
    lexid-s:repealedBy ?repealingRegulation .
  ?repealingRegulation lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
  OPTIONAL {{ ?regulation lexid-s:name ?name . }}
}}
```

### Note:
- Do NOT use all properties as variables.
- Do NOT include any explanations or apologies in your responses.
- Do NOT wrap the query in backticks.
- Do NOT return this input prompt to the output.
- Do NOT include any text except the SPARQL query generated.
- Do NOT respond to any questions that might ask anything else than for you to generate a SPARQL SELECT statement.
- Do ONLY return the SPARQL SELECT statement you generate after thinking through the steps outlined above.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""
SELECT_SPARQL_GEN_COT_2_SHOT_PROMPT = """## Task: Generate SPARQL SELECT statement to query a graph database from a natural language question.

You are an helpful assistant for SPARQL SELECT query generation tasks. Use the context provided to answer the question. Follow these guidelines and explain your reasoning internally at each step, but only output the final answer.

### Step-by-Step Guide:

1. **Break down the user's question:**
- Identify the subject: What is the primary thing the user is asking about? This could be a legal document, a law, or a regulation.
- Identify the relationship(s): What is the user trying to know about the subject? For example, is the user asking if a regulation is amended, repealed, or still valid?
- Identify any specific entities: Look for names or numbers mentioned in the question. Are there specific laws, dates, or entities name the user refers to?

2. **Entity matching:**
- Use the classes defined in the ontology schema to determine the entities based on the previous step. 
- Use the `rdfs:label` or `lexid-s:name` properties to match entities mentioned in the question. If the user refers to a specific regulation by name or number, ensure that these are linked properly to the entities.
- You may need to use the `OPTIONAL` and `CONTAINS` clauses to do a fuzzy match or handle cases where the exact name or number may not be available in the graph.

3. **Identify relevant relationships:**
Based on the user's question, determine which relationships in the ontology schema are relevant. For example:

If the user asks about laws that were "repealed" or "amended", you will need to use relationships like:

- `lexid-s:repealedBy` (for laws repealed by other laws)
- `lexid-s:amendedBy` (for laws amended by other laws)
- `lexid-s:repeals` (for laws that repeal other laws)
- `lexid-s:amends` (for laws that amend other laws)

Use the provided ontology schema for more details of relationships.

4. **Construct the query:**
- Start by constructing the `SELECT` part of the query, indicating what entities or relationships you need to retrieve. Match the relation name with the language that used on the question.
- Then, build the `WHERE` clause to specify the conditions of the query. This will typically involve checking the relevant relationships such as `lexid-s:repealedBy` for repealed laws, or `lexid-s:hasRegulationNumber` for specific regulation number. Ensure that the subject (regulation or law) and target entities match the user's input.
- Make sure to include the appropriate `PREFIX` statements at the top of the query for the namespaces (`rdf`, `rdfs`, `lexid`, `lexid-s`). See more details of prefixes on the provided ontology schema.
- If the question includes an entity name or number, use a condition to match the label or name using the `rdfs:label` or `lexid-s:name`.

5. **If the user's question asks about whether a regulation is still relevant or still valid, think about the relationships that imply whether a regulation has been repealed or amended by another regulation.** Specifically:
- Check the `lexid-s:repealedBy` or `lexid-s:amendedBy` properties for the regulation in question.
- Alternatively, check the `lexid-s:repeals` or `lexid-s:amends` properties for other regulations.

### Important: Do not include the steps in the answer; only output the final answer directly.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

## Example
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

### EXAMPLE ONE
### User Query: Peraturan apa yang dihapus oleh UU Nomor 7 Tahun 1948?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The primary subject is UU Nomor 7 Tahun 1948, which is a regulation.
- Relationship(s): The user is asking about a repealed law, i.e., what other regulation was repealed by this law.
- Specific Entity: The law number 7 and the year 1948 are specifically mentioned.

2. **Entity matching:**
- We will match the UU Nomor 7 Tahun 1948 by its regulation number and year using properties like `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`. This will ensure we retrieve the specific law.

3. **Identifying relevant relationships:**
- The key relationship is `lexid-s:repealedBy`, which shows the law that repeals other laws.
- In this case, we are looking for other regulations that have been repealed by UU Nomor 7 Tahun 1948.

4. **Construct the query:**
- The SELECT part will look for the regulation(s) repealed by UU Nomor 7 Tahun 1948 (?regulation) and the label of it (?label). Optionally, we will use the if the regulation has it's official name we will return it also (?name).
- The WHERE clause will define the conditions; we will filter by `lexid-s:repealedBy`, matching the specific regulation number and year (7, 1948), and also match the name or label of the repealed law using relationships listed in the ontology schema.

### Generated SPARQL SELECT Query:
```
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?regulation ?label ?name
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?label ;
    lexid-s:repealedBy ?repealingRegulation .
  ?repealingRegulation lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
  OPTIONAL {{ ?regulation lexid-s:name ?name . }}
}}
```

### EXAMPLE TWO
### User Query: Apa tujuan dari peraturan Undang-Undang Republik Indonesia Nomor 30 Tahun 2002?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking about the purpose of a specific regulation, UU Nomor 30 Tahun 2002.
- Relationship(s): The user is interested in the purpose or goal of the law.
- Specific Entity: UU Nomor 30 Tahun 2002 is explicitly named.

2. **Entity matching:**
- We will match UU Nomor 30 Tahun 2002 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear` properties.

3. **Identifying relevant relationships:**
- The relevant relationship here is `lexid-s:considers`, which indicates the purpose or considerations of the law.

4. **Construct the query:**
- The SELECT clause will specify that we want to retrieve the law's purpose (?considerant).
- The WHERE clause will use `lexid-s:considers` to retrieve the law's purpose, matched using the same variable used in the SELECT CLAUSE
- Capture the correct regulation using regulation number and year (30 and 2002).

### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?label ?considerant
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?label ;
    lexid-s:considers ?considerant ;
    lexid-s:hasRegulationNumber "30" ;
    lexid-s:hasRegulationYear "2002" .
}}
```

### Note:
- Do NOT use all properties as variables.
- Do NOT include any explanations or apologies in your responses.
- Do NOT wrap the query in backticks.
- Do NOT return this input prompt to the output.
- Do NOT include any text except the SPARQL query generated.
- Do NOT respond to any questions that might ask anything else than for you to generate a SPARQL SELECT statement.
- Do ONLY return the SPARQL SELECT statement you generate after thinking through the steps outlined above.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""
SELECT_SPARQL_GEN_COT_3_SHOT_PROMPT = """## Task: Generate SPARQL SELECT statement to query a graph database from a natural language question.

You are an helpful assistant for SPARQL SELECT query generation tasks. Use the context provided to answer the question. Follow these guidelines and explain your reasoning internally at each step, but only output the final answer.

### Step-by-Step Guide:

1. **Break down the user's question:**
- Identify the subject: What is the primary thing the user is asking about? This could be a legal document, a law, or a regulation.
- Identify the relationship(s): What is the user trying to know about the subject? For example, is the user asking if a regulation is amended, repealed, or still valid?
- Identify any specific entities: Look for names or numbers mentioned in the question. Are there specific laws, dates, or entities name the user refers to?

2. **Entity matching:**
- Use the classes defined in the ontology schema to determine the entities based on the previous step. 
- Use the `rdfs:label` or `lexid-s:name` properties to match entities mentioned in the question. If the user refers to a specific regulation by name or number, ensure that these are linked properly to the entities.
- You may need to use the `OPTIONAL` and `CONTAINS` clauses to do a fuzzy match or handle cases where the exact name or number may not be available in the graph.

3. **Identify relevant relationships:**
Based on the user's question, determine which relationships in the ontology schema are relevant. For example:

If the user asks about laws that were "repealed" or "amended", you will need to use relationships like:

- `lexid-s:repealedBy` (for laws repealed by other laws)
- `lexid-s:amendedBy` (for laws amended by other laws)
- `lexid-s:repeals` (for laws that repeal other laws)
- `lexid-s:amends` (for laws that amend other laws)

Use the provided ontology schema for more details of relationships.

4. **Construct the query:**
- Start by constructing the `SELECT` part of the query, indicating what entities or relationships you need to retrieve. Match the relation name with the language that used on the question.
- Then, build the `WHERE` clause to specify the conditions of the query. This will typically involve checking the relevant relationships such as `lexid-s:repealedBy` for repealed laws, or `lexid-s:hasRegulationNumber` for specific regulation number. Ensure that the subject (regulation or law) and target entities match the user's input.
- Make sure to include the appropriate `PREFIX` statements at the top of the query for the namespaces (`rdf`, `rdfs`, `lexid`, `lexid-s`). See more details of prefixes on the provided ontology schema.
- If the question includes an entity name or number, use a condition to match the label or name using the `rdfs:label` or `lexid-s:name`.

5. **If the user's question asks about whether a regulation is still relevant or still valid, think about the relationships that imply whether a regulation has been repealed or amended by another regulation.** Specifically:
- Check the `lexid-s:repealedBy` or `lexid-s:amendedBy` properties for the regulation in question.
- Alternatively, check the `lexid-s:repeals` or `lexid-s:amends` properties for other regulations.

### Important: Do not include the steps in the answer; only output the final answer directly.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

## Example
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

### EXAMPLE ONE
### User Query: Peraturan apa yang dihapus oleh UU Nomor 7 Tahun 1948?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The primary subject is UU Nomor 7 Tahun 1948, which is a regulation.
- Relationship(s): The user is asking about a repealed law, i.e., what other regulation was repealed by this law.
- Specific Entity: The law number 7 and the year 1948 are specifically mentioned.

2. **Entity matching:**
- We will match the UU Nomor 7 Tahun 1948 by its regulation number and year using properties like `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`. This will ensure we retrieve the specific law.

3. **Identifying relevant relationships:**
- The key relationship is `lexid-s:repealedBy`, which shows the law that repeals other laws.
- In this case, we are looking for other regulations that have been repealed by UU Nomor 7 Tahun 1948.

4. **Construct the query:**
- The SELECT part will look for the regulation(s) repealed by UU Nomor 7 Tahun 1948 (?regulation) and the label of it (?label). Optionally, we will use the if the regulation has it's official name we will return it also (?name).
- The WHERE clause will define the conditions; we will filter by `lexid-s:repealedBy`, matching the specific regulation number and year (7, 1948), and also match the name or label of the repealed law using relationships listed in the ontology schema.

### Generated SPARQL SELECT Query:
```
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?regulation ?label ?name
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?label ;
    lexid-s:repealedBy ?repealingRegulation .
  ?repealingRegulation lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
  OPTIONAL {{ ?regulation lexid-s:name ?name . }}
}}
```

### EXAMPLE TWO
### User Query: Apa tujuan dari peraturan Undang-Undang Republik Indonesia Nomor 30 Tahun 2002?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking about the purpose of a specific regulation, UU Nomor 30 Tahun 2002.
- Relationship(s): The user is interested in the purpose or goal of the law.
- Specific Entity: UU Nomor 30 Tahun 2002 is explicitly named.

2. **Entity matching:**
- We will match UU Nomor 30 Tahun 2002 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear` properties.

3. **Identifying relevant relationships:**
- The relevant relationship here is `lexid-s:considers`, which indicates the purpose or considerations of the law.

4. **Construct the query:**
- The SELECT clause will specify that we want to retrieve the law's purpose (?considerant).
- The WHERE clause will use `lexid-s:considers` to retrieve the law's purpose, matched using the same variable used in the SELECT CLAUSE
- Capture the correct regulation using regulation number and year (30 and 2002).

### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?label ?considerant
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
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking about the regulation Undang Undang No. 6 Tahun 1987.
- Relationship: The user is asking about the legal basis of the regulation.
- Entity: The regulation Undang Undang No. 6 Tahun 1987 is explicitly mentioned.

2. **Entity matching:**
- We will match UU No. 6 Tahun 1987 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`.

3. **Identifying relevant relationships:**
- The relevant relationship is `lexid-s:hasLegalBasis`, which links a regulation to its legal basis.

4. **Construct the query:**
- The SELECT clause will specify that we want to retrieve the legal basis (`?legalBasis`) for the law (`?regulation`).
- The WHERE clause will use `lexid-s:hasLegalBasis` to find the law's legal basis, while matching it by regulation number and year (6 and 1987).

### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?regulation ?legalBasis
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?regulationLabel ;
    lexid-s:hasLegalBasis ?legalBasis ;
    lexid-s:hasRegulationNumber "6" ;
    lexid-s:hasRegulationYear "1987" .
  ?legalBasis rdfs:label ?legalBasisLabel
}}
```

### Note:
- Do NOT use all properties as variables.
- Do NOT include any explanations or apologies in your responses.
- Do NOT wrap the query in backticks.
- Do NOT return this input prompt to the output.
- Do NOT include any text except the SPARQL query generated.
- Do NOT respond to any questions that might ask anything else than for you to generate a SPARQL SELECT statement.
- Do ONLY return the SPARQL SELECT statement you generate after thinking through the steps outlined above.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""

SELECT_SPARQL_GEN_COT_4_SHOT_PROMPT = """## Task: Generate SPARQL SELECT statement to query a graph database from a natural language question.

You are an helpful assistant for SPARQL SELECT query generation tasks. Use the context provided to answer the question. Follow these guidelines and explain your reasoning internally at each step, but only output the final answer.

### Step-by-Step Guide:

1. **Break down the user's question:**
- Identify the subject: What is the primary thing the user is asking about? This could be a legal document, a law, or a regulation.
- Identify the relationship(s): What is the user trying to know about the subject? For example, is the user asking if a regulation is amended, repealed, or still valid?
- Identify any specific entities: Look for names or numbers mentioned in the question. Are there specific laws, dates, or entities name the user refers to?

2. **Entity matching:**
- Use the classes defined in the ontology schema to determine the entities based on the previous step. 
- Use the `rdfs:label` or `lexid-s:name` properties to match entities mentioned in the question. If the user refers to a specific regulation by name or number, ensure that these are linked properly to the entities.
- You may need to use the `OPTIONAL` and `CONTAINS` clauses to do a fuzzy match or handle cases where the exact name or number may not be available in the graph.

3. **Identify relevant relationships:**
Based on the user's question, determine which relationships in the ontology schema are relevant. For example:

If the user asks about laws that were "repealed" or "amended", you will need to use relationships like:

- `lexid-s:repealedBy` (for laws repealed by other laws)
- `lexid-s:amendedBy` (for laws amended by other laws)
- `lexid-s:repeals` (for laws that repeal other laws)
- `lexid-s:amends` (for laws that amend other laws)

Use the provided ontology schema for more details of relationships.

4. **Construct the query:**
- Start by constructing the `SELECT` part of the query, indicating what entities or relationships you need to retrieve. Match the relation name with the language that used on the question.
- Then, build the `WHERE` clause to specify the conditions of the query. This will typically involve checking the relevant relationships such as `lexid-s:repealedBy` for repealed laws, or `lexid-s:hasRegulationNumber` for specific regulation number. Ensure that the subject (regulation or law) and target entities match the user's input.
- Make sure to include the appropriate `PREFIX` statements at the top of the query for the namespaces (`rdf`, `rdfs`, `lexid`, `lexid-s`). See more details of prefixes on the provided ontology schema.
- If the question includes an entity name or number, use a condition to match the label or name using the `rdfs:label` or `lexid-s:name`.

5. **If the user's question asks about whether a regulation is still relevant or still valid, think about the relationships that imply whether a regulation has been repealed or amended by another regulation.** Specifically:
- Check the `lexid-s:repealedBy` or `lexid-s:amendedBy` properties for the regulation in question.
- Alternatively, check the `lexid-s:repeals` or `lexid-s:amends` properties for other regulations.

### Important: Do not include the steps in the answer; only output the final answer directly.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

## Example
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

### EXAMPLE ONE
### User Query: Peraturan apa yang dihapus oleh UU Nomor 7 Tahun 1948?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The primary subject is UU Nomor 7 Tahun 1948, which is a regulation.
- Relationship(s): The user is asking about a repealed law, i.e., what other regulation was repealed by this law.
- Specific Entity: The law number 7 and the year 1948 are specifically mentioned.

2. **Entity matching:**
- We will match the UU Nomor 7 Tahun 1948 by its regulation number and year using properties like `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`. This will ensure we retrieve the specific law.

3. **Identifying relevant relationships:**
- The key relationship is `lexid-s:repealedBy`, which shows the law that repeals other laws.
- In this case, we are looking for other regulations that have been repealed by UU Nomor 7 Tahun 1948.

4. **Construct the query:**
- The SELECT part will look for the regulation(s) repealed by UU Nomor 7 Tahun 1948 (?regulation) and the label of it (?label). Optionally, we will use the if the regulation has it's official name we will return it also (?name).
- The WHERE clause will define the conditions; we will filter by `lexid-s:repealedBy`, matching the specific regulation number and year (7, 1948), and also match the name or label of the repealed law using relationships listed in the ontology schema.

### Generated SPARQL SELECT Query:
```
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?regulation ?label ?name
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?label ;
    lexid-s:repealedBy ?repealingRegulation .
  ?repealingRegulation lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
  OPTIONAL {{ ?regulation lexid-s:name ?name . }}
}}
```

### EXAMPLE TWO
### User Query: Apa tujuan dari peraturan Undang-Undang Republik Indonesia Nomor 30 Tahun 2002?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking about the purpose of a specific regulation, UU Nomor 30 Tahun 2002.
- Relationship(s): The user is interested in the purpose or goal of the law.
- Specific Entity: UU Nomor 30 Tahun 2002 is explicitly named.

2. **Entity matching:**
- We will match UU Nomor 30 Tahun 2002 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear` properties.

3. **Identifying relevant relationships:**
- The relevant relationship here is `lexid-s:considers`, which indicates the purpose or considerations of the law.

4. **Construct the query:**
- The SELECT clause will specify that we want to retrieve the law's purpose (?considerant).
- The WHERE clause will use `lexid-s:considers` to retrieve the law's purpose, matched using the same variable used in the SELECT CLAUSE
- Capture the correct regulation using regulation number and year (30 and 2002).

### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?label ?considerant
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
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking about the regulation Undang Undang No. 6 Tahun 1987.
- Relationship: The user is asking about the legal basis of the regulation.
- Entity: The regulation Undang Undang No. 6 Tahun 1987 is explicitly mentioned.

2. **Entity matching:**
- We will match UU No. 6 Tahun 1987 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`.

3. **Identifying relevant relationships:**
- The relevant relationship is `lexid-s:hasLegalBasis`, which links a regulation to its legal basis.

4. **Construct the query:**
- The SELECT clause will specify that we want to retrieve the legal basis (`?legalBasis`) for the law (`?regulation`).
- The WHERE clause will use `lexid-s:hasLegalBasis` to find the law’s legal basis, while matching it by regulation number and year (6 and 1987).

### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?regulation ?legalBasis
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?regulationLabel ;
    lexid-s:hasLegalBasis ?legalBasis ;
    lexid-s:hasRegulationNumber "6" ;
    lexid-s:hasRegulationYear "1987" .
  ?legalBasis rdfs:label ?legalBasisLabel
}}
```

### EXAMPLE FOUR
### User Query: Apakah Undang Undang Tahun 2004 No 10 masih relevan?
### Step-by-Step Thoughts:
1. **Break down the user's question:**
- Subject: The user is asking about the regulation Undang Undang Tahun 2004 No 10.
- Relationship: The user is wants to know whether the regulation is still relevant, that is, whether the regulation has been repealed or amended.
- Entity: The regulation Undang Undang Tahun 2004 No 10 is explicitly mentioned.

2. **Entity matching:**
- We will match UU No. 10 Tahun 2004 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear` by its number and year.

3. **Identifying relevant relationships:**
- The relevant relationships here are `lexid-s:repealedBy` and `lexid-s:amendedBy`, which indicate whether the law has been repealed or amended, respectively.

4. **Construct the query:**
- The SELECT part will retrieve the status of Undang Undang Tahun 2004 No 10 (`?status`), checking if it has been repealed or amended. This part also retrieve the regulation (`?regulation`) and the repealing regulation counterpart (`?repealingRegulation`).
- The WHERE clause will check for the `lexid-s:repealedBy` and `lexid-s:amendedBy` relationships to find its current relevance. Also we need to do filtering by the law number and year (10 and 2004).

### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?regulation ?repealingRegulation ?status
WHERE {{
    ?regulation a lexid-s:LegalDocument ;
    	lexid-s:repealedBy ?repealingRegulation ;
    	lexid-s:hasRegulationNumber "10" ;
    	lexid-s:hasRegulationYear "2004" .
    OPTIONAL {{ ?regulation lexid-s:status ?status . }}
}}
```

### Note:
- Do NOT use all properties as variables.
- Do NOT include any explanations or apologies in your responses.
- Do NOT wrap the query in backticks.
- Do NOT return this input prompt to the output.
- Do NOT include any text except the SPARQL query generated.
- Do NOT respond to any questions that might ask anything else than for you to generate a SPARQL SELECT statement.
- Do ONLY return the SPARQL SELECT statement you generate after thinking through the steps outlined above.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""

SELECT_SPARQL_GEN_COT_5_SHOT_PROMPT = """## Task: Generate SPARQL SELECT statement to query a graph database from a natural language question.

You are an helpful assistant for SPARQL SELECT query generation tasks. Use the context provided to answer the question. Follow these guidelines and explain your reasoning internally at each step, but only output the final answer.

### Step-by-Step Guide:

1. **Break down the user's question:**
- Identify the subject: What is the primary thing the user is asking about? This could be a legal document, a law, or a regulation.
- Identify the relationship(s): What is the user trying to know about the subject? For example, is the user asking if a regulation is amended, repealed, or still valid?
- Identify any specific entities: Look for names or numbers mentioned in the question. Are there specific laws, dates, or entities name the user refers to?

2. **Entity matching:**
- Use the classes defined in the ontology schema to determine the entities based on the previous step. 
- Use the `rdfs:label` or `lexid-s:name` properties to match entities mentioned in the question. If the user refers to a specific regulation by name or number, ensure that these are linked properly to the entities.
- You may need to use the `OPTIONAL` and `CONTAINS` clauses to do a fuzzy match or handle cases where the exact name or number may not be available in the graph.

3. **Identify relevant relationships:**
Based on the user's question, determine which relationships in the ontology schema are relevant. For example:

If the user asks about laws that were "repealed" or "amended", you will need to use relationships like:

- `lexid-s:repealedBy` (for laws repealed by other laws)
- `lexid-s:amendedBy` (for laws amended by other laws)
- `lexid-s:repeals` (for laws that repeal other laws)
- `lexid-s:amends` (for laws that amend other laws)

Use the provided ontology schema for more details of relationships.

4. **Construct the query:**
- Start by constructing the `SELECT` part of the query, indicating what entities or relationships you need to retrieve. Match the relation name with the language that used on the question.
- Then, build the `WHERE` clause to specify the conditions of the query. This will typically involve checking the relevant relationships such as `lexid-s:repealedBy` for repealed laws, or `lexid-s:hasRegulationNumber` for specific regulation number. Ensure that the subject (regulation or law) and target entities match the user's input.
- Make sure to include the appropriate `PREFIX` statements at the top of the query for the namespaces (`rdf`, `rdfs`, `lexid`, `lexid-s`). See more details of prefixes on the provided ontology schema.
- If the question includes an entity name or number, use a condition to match the label or name using the `rdfs:label` or `lexid-s:name`.

5. **If the user's question asks about whether a regulation is still relevant or still valid, think about the relationships that imply whether a regulation has been repealed or amended by another regulation.** Specifically:
- Check the `lexid-s:repealedBy` or `lexid-s:amendedBy` properties for the regulation in question.
- Alternatively, check the `lexid-s:repeals` or `lexid-s:amends` properties for other regulations.

### Important: Do not include the steps in the answer; only output the final answer directly.

### Ontology Schema:
The ontology schema delimited by triple backticks in Turtle format is:
```turtle
{schema}
```

## Example
PLEASE USE THIS EXAMPLE FOR YOUR THINKING AND NEVER USE IT TO ANSWER ANY QUESTIONS.

### EXAMPLE ONE
### User Query: Peraturan apa yang dihapus oleh UU Nomor 7 Tahun 1948?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The primary subject is UU Nomor 7 Tahun 1948, which is a regulation.
- Relationship(s): The user is asking about a repealed law, i.e., what other regulation was repealed by this law.
- Specific Entity: The law number 7 and the year 1948 are specifically mentioned.

2. **Entity matching:**
- We will match the UU Nomor 7 Tahun 1948 by its regulation number and year using properties like `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`. This will ensure we retrieve the specific law.

3. **Identifying relevant relationships:**
- The key relationship is `lexid-s:repealedBy`, which shows the law that repeals other laws.
- In this case, we are looking for other regulations that have been repealed by UU Nomor 7 Tahun 1948.

4. **Construct the query:**
- The SELECT part will look for the regulation(s) repealed by UU Nomor 7 Tahun 1948 (?regulation) and the label of it (?label). Optionally, we will use the if the regulation has it's official name we will return it also (?name).
- The WHERE clause will define the conditions; we will filter by `lexid-s:repealedBy`, matching the specific regulation number and year (7, 1948), and also match the name or label of the repealed law using relationships listed in the ontology schema.

### Generated SPARQL SELECT Query:
```
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?regulation ?label ?name
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?label ;
    lexid-s:repealedBy ?repealingRegulation .
  ?repealingRegulation lexid-s:hasRegulationNumber "7" ;
    lexid-s:hasRegulationYear "1948" .
  OPTIONAL {{ ?regulation lexid-s:name ?name . }}
}}
```

### EXAMPLE TWO
### User Query: Apa tujuan dari peraturan Undang-Undang Republik Indonesia Nomor 30 Tahun 2002?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking about the purpose of a specific regulation, UU Nomor 30 Tahun 2002.
- Relationship(s): The user is interested in the purpose or goal of the law.
- Specific Entity: UU Nomor 30 Tahun 2002 is explicitly named.

2. **Entity matching:**
- We will match UU Nomor 30 Tahun 2002 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear` properties.

3. **Identifying relevant relationships:**
- The relevant relationship here is `lexid-s:considers`, which indicates the purpose or considerations of the law.

4. **Construct the query:**
- The SELECT clause will specify that we want to retrieve the law's purpose (?considerant).
- The WHERE clause will use `lexid-s:considers` to retrieve the law's purpose, matched using the same variable used in the SELECT CLAUSE
- Capture the correct regulation using regulation number and year (30 and 2002).

### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?label ?considerant
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
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking about the regulation Undang Undang No. 6 Tahun 1987.
- Relationship: The user is asking about the legal basis of the regulation.
- Entity: The regulation Undang Undang No. 6 Tahun 1987 is explicitly mentioned.

2. **Entity matching:**
- We will match UU No. 6 Tahun 1987 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`.

3. **Identifying relevant relationships:**
- The relevant relationship is `lexid-s:hasLegalBasis`, which links a regulation to its legal basis.

4. **Construct the query:**
- The SELECT clause will specify that we want to retrieve the legal basis (`?legalBasis`) for the law (`?regulation`).
- The WHERE clause will use `lexid-s:hasLegalBasis` to find the law’s legal basis, while matching it by regulation number and year (6 and 1987).

### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?regulation ?legalBasis
WHERE {{
  ?regulation a lexid-s:LegalDocument ;
    rdfs:label ?regulationLabel ;
    lexid-s:hasLegalBasis ?legalBasis ;
    lexid-s:hasRegulationNumber "6" ;
    lexid-s:hasRegulationYear "1987" .
  ?legalBasis rdfs:label ?legalBasisLabel
}}
```

### EXAMPLE FOUR
### User Query: Apakah Undang Undang Tahun 2004 No 10 masih relevan?
### Step-by-Step Thoughts:
1. **Break down the user's question:**
- Subject: The user is asking about the regulation Undang Undang Tahun 2004 No 10.
- Relationship: The user is wants to know whether the regulation is still relevant, that is, whether the regulation has been repealed or amended.
- Entity: The regulation Undang Undang Tahun 2004 No 10 is explicitly mentioned.

2. **Entity matching:**
- We will match UU No. 10 Tahun 2004 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear` by its number and year.

3. **Identifying relevant relationships:**
- The relevant relationships here are `lexid-s:repealedBy` and `lexid-s:amendedBy`, which indicate whether the law has been repealed or amended, respectively.

4. **Construct the query:**
- The SELECT part will retrieve the status of Undang Undang Tahun 2004 No 10 (`?status`), checking if it has been repealed or amended. This part also retrieve the regulation (`?regulation`) and the repealing regulation counterpart (`?repealingRegulation`).
- The WHERE clause will check for the `lexid-s:repealedBy` and `lexid-s:amendedBy` relationships to find its current relevance. Also we need to do filtering by the law number and year (10 and 2004).

### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?regulation ?repealingRegulation ?status
WHERE {{
    ?regulation a lexid-s:LegalDocument ;
    	lexid-s:repealedBy ?repealingRegulation ;
    	lexid-s:hasRegulationNumber "10" ;
    	lexid-s:hasRegulationYear "2004" .
    OPTIONAL {{ ?regulation lexid-s:status ?status . }}
}}
```

### EXAMPLE FIVE
### User Query: Di manakah UU No. 12 Thn 2011 ditetapkan?
### Step-by-Step Thoughts:
1. **Break down the user's question:** 
- Subject: The user is asking about the location where UU No. 12 Tahun 2011 was established.
- Relationship(s): The user is looking for the enaction location of the law.
- Entity: The regulation UU No. 12 Thn 2011 is explicitly mentioned.

2. **Entity matching:**
- We will match UU No. 12 Tahun 2011 using `lexid-s:hasRegulationNumber` and `lexid-s:hasRegulationYear`.

3. **Identifying relevant relationships:**
- The relevant relationship here is `lexid-s:enactionLocation` (established in), which will give us the location where the law was enacted.

4. **Construct the query:**
- The SELECT part will retrieve the location of enactment for UU No. 12 Thn 2011 (`?enactionLocation`) and also the regulation itself (`?regulation`).
- The WHERE clause will filter for the law's enactment location using `lexid-s:enactionLocation`, while matching the law number and year (12 and 2011).

### Generated SPARQL SELECT Query:
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX lexid: <https://w3id.org/lex-id/data/>
PREFIX lexid-s: <https://w3id.org/lex-id/schema/>

SELECT ?regulation ?enactionLocation
WHERE {{
    ?regulation a lexid-s:LegalDocument ;
    	lexid-s:hasEnactionLocation ?enactionLocation ;
    	lexid-s:hasRegulationYear "2011" ;
    	lexid-s:hasRegulationNumber "12" .
}}
```

### Note:
- Do NOT use all properties as variables.
- Do NOT include any explanations or apologies in your responses.
- Do NOT wrap the query in backticks.
- Do NOT return this input prompt to the output.
- Do NOT include any text except the SPARQL query generated.
- Do NOT respond to any questions that might ask anything else than for you to generate a SPARQL SELECT statement.
- Do ONLY return the SPARQL SELECT statement you generate after thinking through the steps outlined above.

### Question
The question delimited by triple backticks is:
```
{prompt}
```
"""