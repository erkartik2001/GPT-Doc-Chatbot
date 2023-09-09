from llama_index import load_index_from_storage, StorageContext,VectorStoreIndex
from llama_index.vector_stores import ChromaVectorStore,PineconeVectorStore
import openai
import pinecone
import os
from dotenv import load_dotenv


def query_ans(unid,query,opkey):
    load_dotenv(".env")
    openai.api_key = opkey
    api_key = os.getenv("PINECONE_API_KEY")
    pinecone.init(api_key=api_key,environment="gcp-starter")

    vector_store = PineconeVectorStore(index_name=unid,environment="gcp-starter")
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    query_engine = index.as_query_engine()
    res = query_engine.query(query)
    return res

