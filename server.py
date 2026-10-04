import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    industry: str


@app.post("/api/research")
def research(req: ResearchRequest):
    from src.crew import run_crew

    result = run_crew(req.industry)
    return {"swot": result["swot"], "brief": result["brief"]}
