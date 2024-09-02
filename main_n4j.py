# main_n4j.py
from llama_index.core import (
    PropertyGraphIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings,
)
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import timeit
import datetime
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
import os

'''
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
'''

# load LLM and embeddings model
llm = LlamaCPP(
    model_path='./models/mistral-7b-instruct-v0.3.Q2_K.gguf',
    temperature=0.1,
    max_new_tokens=256,
    context_window=4096,
    model_kwargs={"n_gpu_layers": 1},
    verbose=False
)
embed_model = HuggingFaceEmbedding()
Settings.llm = llm
Settings.embed_model = embed_model
Settings.chunk_size = 512

# setup neo4j graph store
url = "bolt://localhost:7687"
username = "neo4j"
password = "password"
database = "neo4j"
graph_store = Neo4jPropertyGraphStore(
    username=username,
    password=password,
    url=url,
    database=database,
)

try:
    # attempt to load index from file and graph from database
    gstorage_context = StorageContext.from_defaults(persist_dir='./storage_n4')
    kg_index = PropertyGraphIndex.from_existing(property_graph_store=graph_store)
except FileNotFoundError as e:
    gstorage_context = StorageContext.from_defaults(graph_store=graph_store)
    documents = SimpleDirectoryReader("./pdf/").load_data()
    start = timeit.default_timer()
    # perform kg generation
    kg_index = PropertyGraphIndex.from_documents(
        documents,
        storage_context=gstorage_context,
        max_triplets_per_chunk=10,
        include_embeddings=True,
        property_graph_store=graph_store,
    )
    kg_gen_time = timeit.default_timer() - start # seconds
    gstorage_context.persist(persist_dir="./storage_n4")
    print(f'KG generation completed in: {datetime.timedelta(seconds=kg_gen_time)}')

kg_keyword_query_engine = kg_index.as_query_engine(
    # setting to false uses the raw triplets instead of adding the text from the corresponding nodes
    include_text=True,
    similarity_top_k=2,
)

# read questions from file and ask one at a time
with open('qa_list_doc1.txt') as qfile:
    for query in qfile:
        # KG query
        start = timeit.default_timer()
        response = kg_keyword_query_engine.query(query.rstrip())
        kg_qa_resp_time = timeit.default_timer() - start # seconds
        print(f'Query: {query}\nResponse: {response.response}\nTime: {kg_qa_resp_time:.2f}\n{"="*80}')

