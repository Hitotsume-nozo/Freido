from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Optional, Dict

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
def reset(req: Optional[ResetRequest] = Body(default=None)):
    req = req or ResetRequest()
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

    obs, reward, done, info = env.step(req.action)

    if done:
        envs.pop(req.session_id, None)

    return StepResponse(
        observation=obs,
        reward=reward,
        done=done,
        info=info,
    )


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
                "description": "Investigate fraudulent expense reports",
                "difficulty": "easy",
                "max_steps": 20,
            },
            {
                "id": "medium",
                "name": "The Vendor Kickback",
                "description": "Investigate procurement fraud and hidden vendor relationships",
                "difficulty": "medium",
                "max_steps": 30,
            },
            {
                "id": "hard",
                "name": "The Quarter That Never Was",
                "description": "Investigate systematic revenue fabrication before a funding round",
                "difficulty": "hard",
                "max_steps": 40,
            },
        ]
    }


def main():
    import uvicorn

    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)


if __name__ == "__main__":
    main()
