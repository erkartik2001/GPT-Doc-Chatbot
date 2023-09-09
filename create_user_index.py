import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from langchain.vectorstores import Pinecone
import openai

# def fileDirReader(fDPath):
#     if os.path.isfile(fDPath):
#         with open(fDPath, "r") as f:
#             file = f.read()
#         return [file]
    
#     if os.path.isdir(fDPath):
#         loader = DirectoryLoader(fDPath)
#         docs = loader.load()
#         return docs
    
#     return False


def textSplitter(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=20)
    docs = splitter.create_documents(docs)
    return docs


def create_ind(ind_name):
    
    load_dotenv()
    api_key = os.getenv("PINECONE_API_KEY")
    pinecone.init(api_key=api_key,environment="gcp-starter")
    if ind_name and not ind_name in pinecone.list_indexes():
        pinecone.create_index(ind_name,dimension=1536)
    return ind_name


def store_docs(docs,ind_name,opkey):
    print("-*-*"*10)
    print(opkey)
    openai.api_key = opkey
    embedding = OpenAIEmbeddings(model="text-embedding-ada-002",openai_api_key=opkey)
    Pinecone.from_documents(documents=docs,embedding=embedding,index_name=ind_name)
    return True


def create_pinecode_ind(unid,filedata,opkey):
    docs = [filedata]
    docs = textSplitter(docs=docs)
    ind_name = create_ind(unid)
    
    res = store_docs(ind_name=ind_name,docs=docs,opkey=opkey)
    return res

    
if __name__ == "__main__":
    print("inside main")