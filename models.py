from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    research_data = Column(Text)      # JSON string — Sai's output
    outline = Column(Text)            # JSON string — Vishnu's output
    draft_content = Column(Text)      # Abilasha's output
    final_content = Column(Text)      # Jitendra's output
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())