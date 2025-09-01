# 🤖 Agentify – Multi-Agent Customer Support System

**Agentify** is an AI-powered customer support system built with **FastAPI, PostgreSQL, and IBM Watsonx Orchestrate**.
It uses a **multi-agent architecture** to classify and respond to customer requests, create support tickets, and escalate issues when needed.

---

## 🚀 Features

* 🔑 **JWT Authentication** – User registration & login
* 🧠 **Multi-Agent System** powered by **Watsonx Orchestrate**

  * **Classifier Agent** → routes requests to the correct agent
  * **Info Agent** → answers inquiries using business knowledge base
  * **Ticket Agent** → creates Jira issues for technical requests
  * **Escalation Agent** → sends escalation emails via Gmail API
* 💬 **Threaded Conversations** – each interaction is stored and retrievable
* 📩 **3rd-party integrations** – Jira, Gmail (Google Cloud API)

---

## 🏗️ Architecture

Here’s the architecture of **Agentify** showing how the Classifier Agent orchestrates requests and delegates them to other agents:

<img width="828" height="418" alt="agentify-diagram" src="https://github.com/user-attachments/assets/5d6b9b00-08d7-475c-bd1b-354d23c07676" />

---

## 🌐 Live Demo

Frontend (Client): https://agentify-ai-customer-support-client.vercel.app

Backend (API): https://ai-customer-agent-production.up.railway.app/api/v1

---

## 🎥 Demo video



https://github.com/user-attachments/assets/0f25ec4d-ce2a-4351-9fd4-d975cce241a5


---
## 📦 Tech Stack

* **Backend:** FastAPI, PostgreSQL, SQLAlchemy
* **AI/Agents:** IBM Watsonx Orchestrate
* **Integrations:** Jira API, Gmail API (Google Cloud)

---

## 🔑 Authentication

### Register

`POST /auth/register`

**Request**

```json
{
  "full_name": "Mohamed tarek",
  "email": "test@test.com",
  "password": "test1234"
}
```

**Response**

```json
{
  "id": 2,
  "full_name": "Mohamed tarek",
  "email": "test@test.com"
}
```

---

### Login

`POST /auth/login`

**Request**

```json
{
  "email": "test@test.com",
  "password": "test1234"
}
```

**Response**

```json
{
  "id": 2,
  "full_name": "Mohamed tarek",
  "email": "test@test.com",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI..."
}
```

---

## 💬 Conversations

### Get All Threads

`GET /threads` (requires Bearer Token)

**Response**

```json
{
  "response": [
    {
      "thread_id": "c6129b43-1076-49ee-a821-9f068c2dcf5c",
      "title": "\"Refund Payment Request\"",
      "user_id": 2
    },
    {
      "thread_id": "39488b80-b6f6-4c58-b68f-3836faa0684c",
      "title": "\"Refund Payment Request\"",
      "user_id": 2
    }
  ]
}
```

---

### Get Messages in Thread

`GET /messages/:thread_id` (requires Bearer Token)

**Response**

```json
{
  "response": [
    { "role": "user", "content": "i want to refund my payment" },
    { "role": "assistant", "content": "What is your order number?" },
    { "role": "user", "content": "124124" },
    { "role": "assistant", "content": "Your refund for order 124124 has been successfully submitted. Your issue number is KAN-5." }
  ]
}
```

---

### Send Prompt (Start or Continue Thread)

`POST /threads/send_prompt` (requires Bearer Token)

**Request**

```json
{
  "content": "i want to refund my payment",
  "thread_id": "c6129b43-1076-49ee-a821-9f068c2dcf5c"  //optional
}
```

**Response**

```json
{
  "response": {
    "thread_id": "e48ab4c0-e89b-4137-9bb9-07792bb2db8a",
    "thread_title": "\"Refund Payment Request\"",
    "response": {
      "role": "assistant",
      "content": "What is your order number?"
    }
  }
}
```

---
