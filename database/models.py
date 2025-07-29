# database/models.py

from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PolicyClause(Base):
    __tablename__ = "policy_clauses"

    id = Column(Integer, primary_key=True, index=True)
    clause_text = Column(String, nullable=False)
    embedding = Column(String, nullable=False)  # Stored as JSON string or pickled vector
    section = Column(String, nullable=True)
    code = Column(String, nullable=True)        # E.g., "Code-Excl03"
    confidence_threshold = Column(Float, default=0.75)
