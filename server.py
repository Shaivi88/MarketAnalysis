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

    paths = run_crew(req.industry)

    with open(paths["swot"], "r", encoding="utf-8") as f:
        swot = f.read()
    with open(paths["brief"], "r", encoding="utf-8") as f:
        brief = f.read()

    return {"swot": swot, "brief": brief}
