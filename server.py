# server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from environment import FraudInvestigationEnv
from models import Action, Observation, Reward

app = FastAPI(
    title="Forensic Fraud Investigation - OpenEnv",
    description="AI agent environment for corporate fraud investigation",
    version="1.0.0",
)

envs: Dict[str, FraudInvestigationEnv] = {}


class ResetRequest(BaseModel):
    task_id: str = "easy"
    session_id: str = "default"


class StepRequest(BaseModel):
    session_id: str = "default"
    action: Action


class StepResponse(BaseModel):
    observation: Observation
    reward: Reward
    done: bool
    info: dict


class ResetResponse(BaseModel):
    observation: Observation


class StateResponse(BaseModel):
    state: dict


@app.get("/")
def health():
    return {
        "status": "ok",
        "environment": "forensic-fraud-investigation",
        "version": "1.0.0",
    }


@app.post("/reset", response_model=ResetResponse)
def reset(req: ResetRequest):
    try:
        env = FraudInvestigationEnv(task_id=req.task_id)
        obs = env.reset()
        envs[req.session_id] = env
        return ResetResponse(observation=obs)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/step", response_model=StepResponse)
def step(req: StepRequest):
    env = envs.get(req.session_id)
    if env is None:
        raise HTTPException(
            status_code=400,
            detail="No active environment. Call /reset first.",
        )
    try:
        obs, reward, done, info = env.step(req.action)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if done:
        envs.pop(req.session_id, None)

    return StepResponse(observation=obs, reward=reward, done=done, info=info)


@app.get("/state", response_model=StateResponse)
def get_state(session_id: str = "default"):
    env = envs.get(session_id)
    if env is None:
        raise HTTPException(
            status_code=400,
            detail="No active environment.",
        )
    return StateResponse(state=env.state())


@app.get("/tasks")
def list_tasks():
    return {
        "tasks": [
            {
                "id": "easy",
                "name": "The Expense Report",
                "description": "Investigate fraudulent expense reports - single perpetrator, clear paper trail",
                "difficulty": "easy",
                "max_steps": 20,
            },
            {
                "id": "medium",
                "name": "The Vendor Kickback",
                "description": "Investigate procurement fraud with hidden vendor relationships and pressured approvals",
                "difficulty": "medium",
                "max_steps": 30,
            },
            {
                "id": "hard",
                "name": "The Quarter That Never Was",
                "description": "Investigate systematic revenue fabrication across departments ahead of a funding round",
                "difficulty": "hard",
                "max_steps": 40,
            },
        ]
    }
