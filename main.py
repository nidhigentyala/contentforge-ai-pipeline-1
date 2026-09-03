import json
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import engine, get_db, Base
import models
from chains.researcher_chain import research_topic
from chains.outliner_chain import create_outline
from chains.writer_chain import write_draft
from chains.Editor_chain import edit_content

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ContentForge AI — Multi-Agent Content Pipeline",
    description="Researcher → Outliner → Writer → Editor pipeline. Built by Sai, Vishnu, Abilasha, Jitendra. Orchestrated by Nidhii.",
    version="1.0.0",
)

class TopicRequest(BaseModel):
    topic: str

@app.post("/generate-content", tags=["Pipeline"], summary="Run the full 4-agent content pipeline on a topic")
def generate_content(request: TopicRequest, db: Session = Depends(get_db)):
    run = models.PipelineRun(topic=request.topic, status="researching")
    db.add(run)
    db.commit()
    db.refresh(run)

    research = research_topic(request.topic)
    run.research_data = json.dumps(research)
    run.status = "outlining"
    db.commit()

    outline = create_outline(research)
    run.outline = json.dumps(outline)
    run.status = "writing"
    db.commit()

    draft = write_draft(outline)
    run.draft_content = draft["draft_content"]
    run.status = "editing"
    db.commit()

    edited = edit_content(draft)
    run.final_content = edited["final_content"]
    run.status = "completed"
    db.commit()
    db.refresh(run)

    return {
        "run_id": run.id,
        "topic": run.topic,
        "final_content": run.final_content,
        "status": run.status,
    }

@app.get("/runs/{run_id}", tags=["Pipeline"], summary="See every stage's output for one run (great for debugging)")
def get_run(run_id: int, db: Session = Depends(get_db)):
    run = db.query(models.PipelineRun).filter(models.PipelineRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run

@app.get("/runs", tags=["Pipeline"], summary="List every pipeline run ever generated")
def list_runs(db: Session = Depends(get_db)):
    return db.query(models.PipelineRun).all()

@app.get("/health", tags=["System"], summary="Check the API is alive")
def health_check():
    return {"status": "ok"}