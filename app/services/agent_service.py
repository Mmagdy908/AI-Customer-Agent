from dotenv import load_dotenv
import os
import requests

load_dotenv()


def send_agent_prompt(prompt: str) -> str:
    """
    Process the agent prompt and return a response.
    This is a placeholder function that simulates sending a prompt to an agent.
    """
    # define headers
    headers = {
        "Authorization": f"Bearer {os.getenv('ORCHESTRATE_API_KEY')}",
        "IAM-API_KEY": os.getenv("ORCHESTRATE_IAM_API_KEY"),
        # "ZenApiKey": "REPLACE_THIS_VALUE",
        "content-type": "text/plain",
        "accept": "text/plain",
    }
    response = requests.post(
        f"{os.getenv('ORCHESTRATE_URL')}/v1/runs?stream=my_stream&stream_timeout=30",
        data=prompt,
        headers=headers,
    )
    print(f"Response: {response}")
    return "Prompt sent successfully"
