from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.llms import OpenAI

load_dotenv()

def get_chat():
    model = ChatOpenAI(model = "gpt-3.5-turbo")
    return model

def get_llm():
    llm = OpenAI(model = "gpt-3.5-turbo")
    return llm