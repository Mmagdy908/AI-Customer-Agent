from fastapi import HTTPException
from dotenv import load_dotenv
import os
import requests
from sqlalchemy.orm import Session
from app.repositories.thread_repository import ThreadRepository

load_dotenv()


# TODO
# need refactoring
def send_agent_prompt(db: Session, prompt: str, thread_id: str | None = None) -> any:
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

    thread_repository = ThreadRepository(db)

    chat_messages = []
    user_message = {"role": "user", "content": prompt}
    thread_title = None

    # load thread title and messages if it exists
    if thread_id:
        thread = thread_repository.get_thread_by_id(thread_id)
        if not thread:
            raise HTTPException(404, "This thread is not found")
        chat_messages = thread.messages
        thread_title = thread.title

    # sending new prompt to agent
    chat_messages.append(user_message)

    response = requests.post(
        f"{os.getenv('ORCHESTRATE_URL')}/v1/orchestrate/{os.getenv('ORCHESTRATE_AGENT_ID')}/chat/completions",
        json={
            "model": os.getenv("ORCHESTRATE_MODEL_ID"),
            "messages": chat_messages,
            "stream": False,
        },
        headers=headers,
    )

    responseData = response.json()

    # generate thread title if new thread is created
    if not thread_id:
        res = requests.post(
            f"{os.getenv('ORCHESTRATE_URL')}/v1/orchestrate/{os.getenv('ORCHESTRATE_AGENT_ID')}/chat/completions",
            json={
                "model": os.getenv("ORCHESTRATE_MODEL_ID"),
                "messages": [
                    {
                        "role": "user",
                        "content": f"generate a suitable thread title depending on the user input. Respond with just the title. this is user prompt:{prompt}",
                    },
                ],
                "stream": False,
            },
            headers=headers,
        ).json()

        thread_id = responseData["thread_id"]
        thread_title = res["choices"][0]["message"]["content"]
        thread_repository.create_thread(thread_id, thread_title)

    # save new user message & response to the thread in DB
    assistant_message = responseData["choices"][0]["message"]
    thread_repository.add_messages(thread_id, [user_message, assistant_message])

    return {
        "thread_id": thread_id,
        "thread_title": thread_title,
        "response": assistant_message,
    }
