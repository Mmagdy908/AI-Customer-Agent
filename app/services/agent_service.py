from dotenv import load_dotenv
import os
import requests

load_dotenv()


def send_agent_prompt(prompt: str, thread_id: str | None = None) -> any:
    """
    Process the agent prompt and return a response.
    This is a placeholder function that simulates sending a prompt to an agent.
    """
    # define headers
    headers = {
        # "Authorization": f"Bearer {os.getenv("ORCHESTRATE_APIKEY")}",
        "IAM-API_KEY": os.getenv("ORCHESTRATE_APIKEY"),
        "X-IBM-THREAD-ID": thread_id,
        "content-type": "application/json",
        "accept": "application/json",
    }

    # TODO
    # load all chat messages from the thread
    # For now, we will just send a static message
    # In a real application, you would fetch messages from a database or another source
    # chat_messages = get_chat_messages(thread_id) if thread_id else []
    messages = []
    print(f"Prompt: {prompt}")
    messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    response = requests.post(
        f"{os.getenv('ORCHESTRATE_URL')}/v1/orchestrate/{os.getenv('ORCHESTRATE_AGENT_ID')}/chat/completions",
        json={
            "model": os.getenv("ORCHESTRATE_MODEL_ID"),
            "messages": messages,
            "stream": False,
        },
        headers=headers,
    )

    # TODO
    # save new user message & response to the thread in DB

    print(f"Response: {response.json()}")
    return response.json()
