from fastapi import HTTPException
from dotenv import load_dotenv
import os
import requests
from sqlalchemy.orm import Session
from app.repositories.thread_repository import ThreadRepository
from app.repositories.message_repository import MessageRepository
from app.models.user import UserInDb

load_dotenv()

ORCHESTRATE_URL = f"{os.getenv('ORCHESTRATE_URL')}/v1/orchestrate/{os.getenv('ORCHESTRATE_AGENT_ID')}/chat/completions"


class AgentService:
    def __init__(self, db: Session):
        self.thread_repository = ThreadRepository(db)
        self.mesaage_repository = MessageRepository(db)

    def _send_agent_message(
        self, chat_messages: list[dict[str, str]], thread_id: str | None = None
    ):
        # define headers
        headers = {
            # "Authorization": f"Bearer {os.getenv("ORCHESTRATE_APIKEY")}",
            "IAM-API_KEY": os.getenv("ORCHESTRATE_APIKEY"),
            "X-IBM-THREAD-ID": thread_id,
            "content-type": "application/json",
            "accept": "application/json",
        }

        response = requests.post(
            ORCHESTRATE_URL,
            json={
                "model": os.getenv("ORCHESTRATE_MODEL_ID"),
                "messages": chat_messages,
                "stream": False,
            },
            headers=headers,
        )

        return response.json()

    def _generate_thread_title(self, prompt: str) -> str:
        title_messages = [
            {
                "role": "user",
                "content": f"generate a suitable thread title depending on the user input. Respond with just the title. this is user prompt:{prompt}",
            },
        ]

        return self._send_agent_message(title_messages)["choices"][0]["message"][
            "content"
        ]

    def get_all_threads(self, user_id: int):
        return self.thread_repository.get_all_threads(user_id)

    def send_agent_prompt(
        self, prompt: str, current_user: UserInDb, thread_id: str | None = None
    ) -> any:
        """
        Process the agent prompt and return a response.
        This is a placeholder function that simulates sending a prompt to an agent.
        """

        chat_messages = []
        user_message = {"role": "user", "content": prompt}
        thread_title = None

        # load thread title and messages if it exists
        if thread_id:
            thread = self.thread_repository.get_thread_by_id(thread_id)

            if not thread:
                raise HTTPException(404, "This thread is not found")
            if thread.user_id != current_user.id:
                raise HTTPException(403, "You are not authorized to access this thread")

            chat_messages = self.mesaage_repository.get_all_messages(thread_id)
            thread_title = thread.title
        else:
            # send system message as first message
            system_message = {
                "role": "system",
                "content": f"You are chatting with user with full name: {current_user.full_name}, email: {current_user.email} and id: {current_user.id}",
            }

            chat_messages.append(system_message)

        # sending new prompt to agent
        chat_messages.append(user_message)

        responseData = self._send_agent_message(chat_messages, thread_id)

        # if thread is new
        if not thread_id:
            thread_id = responseData["thread_id"]
            thread_title = self._generate_thread_title(prompt)
            self.thread_repository.create_thread(
                thread_id, thread_title, user_id=current_user.id
            )
            self.mesaage_repository.create_message(
                thread_id,
                role=system_message["role"],
                content=system_message["content"],
            )

        # save new user message & response to the thread in DB
        assistant_message = responseData["choices"][0]["message"]
        self.mesaage_repository.create_message(
            thread_id, role=user_message["role"], content=user_message["content"]
        )
        self.mesaage_repository.create_message(
            thread_id,
            role=assistant_message["role"],
            content=assistant_message["content"],
        )

        return {
            "thread_id": thread_id,
            "thread_title": thread_title,
            "response": assistant_message,
        }
