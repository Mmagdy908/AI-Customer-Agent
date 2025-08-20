# import http.client
from dotenv import load_dotenv
import os
import requests

load_dotenv()

orchestrate_url = os.getenv("ORCHESTRATE_URL")

# res = requests.post(
#     "https://iam.cloud.ibm.com/identity/token",
#     data={
#         "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
#         "apikey": os.getenv("ORCHESTRATE_IAM_APIKEY"),
#     },
#     headers={"Content-Type": "application/x-www-form-urlencoded"},
# )

# token = res.json()["access_token"]
headers = {
    # "Authorization": f"Bearer {os.getenv("ORCHESTRATE_APIKEY")}",
    "IAM-API_KEY": os.getenv("ORCHESTRATE_APIKEY"),
    "content-type": "application/json",
    "accept": "application/json",
}

res = requests.post(
    f"{orchestrate_url}/v1/orchestrate/{os.getenv('ORCHESTRATE_AGENT_ID')}/chat/completions",
    json={
        "model": os.getenv("meta-llama/llama-3-2-90b-vision-instruct"),
        "messages": [
            {
                "role": "user",
                "content": "I want to refund my order",
            }
        ],
        "stream": False,
    },
    headers=headers,
)

print(res.json())
