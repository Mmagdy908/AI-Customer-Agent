import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()


model_id = os.getenv("WATSONX_MODEL_ID")
project_id = os.getenv("WATSONX_PROJECT_ID")
space_id = os.getenv("WATSONX_SPACE_ID")  # optional
API_KEY = os.getenv("WATSONX_APIKEY")


token = requests.post(
    "https://iam.cloud.ibm.com/identity/token",
    data={"apikey": API_KEY, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"},
).json()["access_token"]

header = {
    "Content-Type": "application/json",
    "accept": "application/json",
    "Authorization": "Bearer " + token,
}
# content = input()
payload_scoring = {
    "messages": [{"content": "tell me 3 advices in life", "role": "user"}]
}

response_scoring = requests.post(
    "https://au-syd.ml.cloud.ibm.com/ml/v4/deployments/354d674f-3eb9-4308-aef2-a670992ee16a/ai_service?version=2021-05-01",
    json=payload_scoring,
    headers=header,
)


def parse_streaming_response(text):
    blocks = text.strip().split("\n\n")
    result = []
    for block in blocks:
        lines = block.strip().split("\n")
        data_line = next((line for line in lines if line.startswith("data: ")), None)
        if data_line:
            try:
                data_json = json.loads(data_line[len("data: ") :])
                result.append(data_json)
            except Exception as e:
                print("Error parsing JSON:", e)
    return result


def get_assistant_response(text):
    try:
        filtered_response = filter(
            lambda x: "choices" in x
            and "content" in x["choices"][0]["delta"]
            and x["choices"][0]["delta"]["role"] == "assistant",
            parse_streaming_response(text),
        )
        chunks = map(
            lambda x: x["choices"][0]["delta"]["content"],
            filtered_response,
        )

        return "".join(chunks)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# print(get_assistant_response(response_scoring.text))
print(response_scoring.json()["choices"][0]["message"]["content"])
