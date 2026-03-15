from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True)
    hcp_name = Column(String)
    interaction_type = Column(String)
    date = Column(String)
    attendees = Column(String)
    topics = Column(String)
    sentiment = Column(String)
    outcomes = Column(String)
    followup = Column(String)