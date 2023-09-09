from llama_index import load_index_from_storage, StorageContext,VectorStoreIndex
from llama_index.vector_stores import ChromaVectorStore,PineconeVectorStore
import openai
import pinecone
import os
from dotenv import load_dotenv


def query_ans(unid,query,opkey):
    load_dotenv(".env")
    openai.api_key = opkey
    # os.environ["PINECONE_API_KEY"] = "be40f998-7766-438a-b5af-3da192458908"
    pinecone.init(api_key="be40f998-7766-438a-b5af-3da192458908",environment="gcp-starter")

    vector_store = PineconeVectorStore(index_name=unid,environment="gcp-starter")
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    query_engine = index.as_query_engine()
    res = query_engine.query(query)
    return res

