import openai
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAI
from langchain.schema import Document
from pinecone import Pinecone as PineconeClient
from pypdf import PdfReader
from langchain.chains.summarize import load_summarize_chain
from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv
import os
from datetime import datetime
import time

load_dotenv()

def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def create_docs(user_pdf_list, unique_id):
    docs=[]
    for filename in user_pdf_list:
        chunks = get_pdf_text(filename)

        docs.append(Document(
            page_content = chunks,
            metadata = {"name":filename.name, "type=": filename.type, "size": filename.size, "unique_id": unique_id, 'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        ))

        
    return docs


def create_embedding_instance():
    embeddings = OpenAIEmbeddings()
    return embeddings


# Function to push data to vector store - pinecone
def push_to_pinecone(embeddings,docs):
    
    pinecone_apikey = os.environ.get("PINECONE_API_KEY")
    pinecone_environment = os.environ.get("PINECONE_ENVIRONMENT")
    pinecone_index_name = os.environ.get("PINECONE_INDEX")

    

    pc = PineconeClient(
            api_key=pinecone_apikey
        )
    index = pc.Index(pinecone_index_name)
    index.delete(delete_all=True, namespace='abc')
    #print("all vector deleted.")

    index_name = pinecone_index_name
    #PineconeStore is an alias name of Pinecone class, please look at the imports section at the top :)
    index = Pinecone.from_documents(docs, embeddings, index_name=index_name, namespace = 'abc')

    return index
    
    
#Function to pull index data from Pinecone
def pull_from_pinecone(embeddings):

    print("30secs delay...")
    time.sleep(30)

    pinecone_apikey = os.environ.get("PINECONE_API_KEY")
    pinecone_environment = os.environ.get("PINECONE_ENVIRONMENT")
    pinecone_index_name = os.environ.get("PINECONE_INDEX")

    PineconeClient(
    api_key=pinecone_apikey,
    environment=pinecone_environment
    )

    index_name = pinecone_index_name
    #PineconeStore is an alias name of Pinecone class, please look at the imports section at the top :)
    index = Pinecone.from_existing_index(index_name, embeddings, namespace='abc')

    return index


def get_similar_doc(query, k, embeddings, unique_id):

    """
    print("*****"*20)
    pc = PineconeClient(
            api_key="9fe6ffcf-09a0-4f3c-9b30-e76fdf938dd5"
        )
    print(pc.Index("chatbotdb").describe_index_stats())
    """

    index = pull_from_pinecone(embeddings)
    similar_docs = index.similarity_search_with_score(query, int(k), {"unique_id": unique_id})
    
    print(len(similar_docs),"similar doc found")
    return similar_docs

# Helps us get the summary of a document
def get_summary(current_doc):
    llm = OpenAI(temperature=0)
    #llm = HuggingFaceHub(repo_id="bigscience/bloom", model_kwargs={"temperature":1e-10})
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run([current_doc])

    return summary
