import streamlit as st
from agent import get_agent
import os
from google.oauth2 import service_account
from google.cloud import aiplatform

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "theta-cell-406519-112ac0726a30.json"
credentials = service_account.Credentials.from_service_account_file(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
project_id = 'theta-cell-406519'

def predict_text_classification_single_label_sample(project="719559140092",location="us-central1", endpoint= "398667523068788736",content="{user_input}"):

  aiplatform.init(project=project, location=location)
  endpoint = aiplatform.Endpoint(endpoint)
  response = endpoint.predict(instances=[{"content": content}], parameters={})
  print(response)
  names=response[0][0]['displayNames']
  values=response[0][0]['confidences']
  max_index=values.index(max(values))

  return names[max_index]


# Title of the page
st.title('BrightSpeed')

# Code to add the first ai message
if 'chat' not in st.session_state:
  st.session_state['chat'] = [{
    "content": "Hi, I'm a sales agent for Brightspeed. How can I help you today?",
    "role": "ai"
  }]

user_input = st.chat_input('message:', key= "user_input")
classifier = predict_text_classification_single_label_sample(content=user_input)
print(classifier)

# adding user input to session
if user_input:
  st.session_state['chat'].append({
    "content": user_input,
    "role": "user"
  })
  # calling the langchain sales agent
  agent = get_agent()

  # generating completeion for users prompt by invoking the agent
  try:
    agent_response = agent.invoke({user_input})
    # adding ai agent response to the session state
    st.session_state['chat'].append({
      "content": agent_response['output'],
      "role": "ai"})
  except :
    # handlinig any parsing errors
    st.session_state['chat'].append({
      "content": "Sorry, I'm not sure I can help with that.",
      "role":"ai"})

# rendering the messesges from chat
if st.session_state['chat']:
  for i in range(0, len(st.session_state['chat'])):
    user_message = st.session_state['chat'][i]
    st.chat_message(user_message["role"]).write(user_message["content"])