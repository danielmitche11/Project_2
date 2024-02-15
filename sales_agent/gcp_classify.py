import os
from google.oauth2 import service_account
from google.cloud import aiplatform

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "sales_agent/theta-cell-406519-112ac0726a30.json"
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