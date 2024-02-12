from langchain.vectorstores.pinecone import Pinecone
from langchain.agents import Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from model import get_llm
from embed import get_embed
import index

db = Pinecone(index = index.get_index('starter'), embedding = get_embed().embed_query, text_key = 'text')
prompt = PromptTemplate.from_template(template = "Use this tool to answer Brightspeed sales questions")

chain = LLMChain(prompt = prompt, llm = get_llm())

def get_vector_tool():

    tool = Tool( func = db.similarity_search, name = "Brightspeed Sales VectorDB tool", description = "Contains information about Brightspeed services and broadband plans", retriever_top_k = 3 )

    return tool