from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.agents import load_tools
from model import get_llm
from model import get_chat
import streamlit as st
# from model import get_chat_model
from memory import get_memory
from prompts import sales_prompt, service_prompt
from tools.vector_tool import get_vector_tool

# memory= get_memory().clear()


def get_tools():
    tools = load_tools(
        [], 
        llm = get_llm()
        # llm=get_llm('llama2')
    )
    tools.append(get_vector_tool())

    return tools

def get_agent(category):
    model = get_chat()
    memory = get_memory()

    match category:
        case "Sales":
            system_message = sales_prompt
            print("Sales agent loaded")
        case "Service":
            system_message = service_prompt
            print("Service agent loaded")

    agent_definition = ConversationalChatAgent.from_llm_and_tools( 
        llm = model, 
        # llm=get_chat_model('llama2'),
        tools = get_tools(), 
        system_message = system_message, 
        handle_parsing_errors = True )
    agent_execution = AgentExecutor.from_agent_and_tools(
        agent = agent_definition, 
        llm = model,
        # llm=get_chat_model('llama2') ,
        tools = get_tools(),
        handle_parsing_errors = True, 
        verbose = True, 
        max_iterations = 3,
        memory = memory 
    )

    return agent_execution

# user_input="tell me about brightspeed"
# agent = get_agent()
# agent_response = agent.invoke({user_input})
# print(agent_response)

# for i in range(3):
#     user_input =input("Enter the query: ")
#     agent=get_agent()
#     agent_response = agent.invoke({user_input})
#     print(agent_response)


