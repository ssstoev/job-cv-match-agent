from fastapi import FastAPI, UploadFile, File, Form
from ai_agent import run_agent
from langchain_core.messages import HumanMessage
import uuid
# import os

app = FastAPI()
sessions = {}  # In-memory store for conversation sessions (for POC)

# WIP: Add mongoDB + vector db integration
@app.post("/upload/")
async def upload(cv: UploadFile = File(...), jd: UploadFile = File(...)):
    cv_text = (await cv.read()).decode("utf-8")
    jd_text = (await jd.read()).decode("utf-8")

    user_prompt = f"""
    You are a professional recruiter. ANSWER WITH 1 SENTENCE.

    Resume:
    {cv_text}

    Job Description:
    {jd_text}

    Evaluate the match and return:
    - Score from 0–100
    - Strengths
    - Weaknesses
    - Suggestions
    """

    session_id = str(uuid.uuid4())
    conversation = [HumanMessage(content=user_prompt)]
    messages = run_agent(conversation)

    sessions[session_id] = messages
    return {
        "session_id": session_id,
        "response": messages[-1].content
    }

@app.post("/chat/")
async def chat(session_id: str = Form(...), message: str = Form(...)):
    if session_id not in sessions:
        return {"error": "Invalid session ID"}

    conversation = sessions[session_id]
    conversation.append(HumanMessage(content=message))
    updated_messages = run_agent(conversation)

    sessions[session_id] = updated_messages
    return {
        "response": updated_messages[-1].content
    }

@app.get("/history/{session_id}")
def get_history(session_id: str):
    if session_id not in sessions:
        return {"error": "Session not found"}
    return {
        "history": [
            {"role": "user" if isinstance(m, HumanMessage) else "ai", "content": m.content}
            for m in sessions[session_id]
        ]
    }
