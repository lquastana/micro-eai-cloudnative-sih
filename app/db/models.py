from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class HL7Message(Base):
    __tablename__ = "hl7_messages"

    id = Column(Integer, primary_key=True, index=True)
    message_type = Column(String(20), index=True)
    raw = Column(Text)
