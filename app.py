import streamlit as st
import requests
import google.auth
from google.oauth2 import service_account
import google.auth.transport.requests
from dotenv import load_dotenv
import os
import json
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
SERVICE_ACCOUNT_INFO = {
    "type": os.getenv("type"),
    "project_id": os.getenv("project_id"),
    "private_key_id": os.getenv("private_key_id"),
    "private_key": os.getenv("private_key"),
    "client_email": os.getenv("client_email"),
    "client_id": os.getenv("client_id"),
    "auth_uri": os.getenv("auth_uri"),
    "token_uri": os.getenv("token_uri"),
    "auth_provider_x509_cert_url": os.getenv("auth_provider_x509_cert_url"),
    "client_x509_cert_url": os.getenv("client_x509_cert_url"),
    "universe_domain": os.getenv("universe_domain")
}

# Create credentials using the loaded service account info
credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)


base_url = "https://us-central1-aiplatform.googleapis.com/v1beta1/projects/{project_id}/locations/us-central1/endpoints/{endpoint_id}:predict"
# base_url = "https://us-central1-aiplatform.googleapis.com/v1/projects/{project_id}/locations/us-central1/endpoints/{endpoint_id}:predict"
project_id = os.getenv("project_id")
endpoint_id = os.getenv("endpoint_id")

def send_prediction(prompt, max_token, top_k):
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    bearer_token = credentials.token

    request_body = {
        "instances": [
            {
                "prompt": prompt,
                "max_tokens": max_token,
                "top_k": top_k
            }
        ]
    }

    full_url = base_url.format(project_id=project_id, endpoint_id=endpoint_id)
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }

    resp = requests.post(full_url, json=request_body, headers=headers)
    print(resp)
    response_data = resp.json()
    
    return response_data

def main():
    st.title('Llama2 Chatbot')

    prompt = st.text_input('Enter your message:')
    max_token = st.slider('Max Length', min_value=50, max_value=500, value=200)
    top_k = st.slider('Top K', min_value=1, max_value=20, value=10)

    if st.button('Send'):
        response_data = send_prediction(prompt, max_token, top_k)

        # print(response_data)
        if 'predictions' in response_data and response_data['predictions']:
            response_text = response_data['predictions'][0]
            ans = ""
            
            if "Output:\n" in response_text:
                ans = response_text.split("Output:\n")[1].strip()
                ans = ans[0].upper() + ans[1:] if ans else ans
            
            st.write(ans)
        else:
            st.write('No response received from the bot.')

if __name__ == '__main__':
    main()
