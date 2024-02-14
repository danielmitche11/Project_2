from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.agents import load_tools
from model import get_llm
from model import get_chat
# from model import get_chat_model
from memory import get_memory
from prompts import sales_prompt
from tools.vector_tool import get_vector_tool

# memory= get_memory().clear()

def get_tools():
    tools = load_tools(
        [], 
        llm = get_llm
        # llm=get_llm('llama2')
    )
    tools.append(get_vector_tool())

    return tools

def get_agent():
    agent_definition = ConversationalChatAgent.from_llm_and_tools( 
        llm = get_chat(), 
        # llm=get_chat_model('llama2'),
        tools = get_tools(), 
        system_message = sales_prompt, 
        handle_parsing_errors = True )
    agent_execution = AgentExecutor.from_agent_and_tools(
        agent = agent_definition, 
        llm = get_chat(),
        # llm=get_chat_model('llama2') ,
        tools = get_tools(),
        handle_parsing_errors = True, 
        verbose = True, 
        max_iterations = 3,
        memory = get_memory() 
    )

    return agent_execution

# user_input="tell me about brightspeed"
# agent = get_agent()
# agent_response = agent.invoke({user_input})
# print(agent_response)

