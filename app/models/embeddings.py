from sqlalchemy import Column, INT, VARCHAR, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EmbeddingModel(Base):
    __tablename__ = "embeddings"

    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    embedding = Column(TEXT, nullable=True)
    user_id = Column(VARCHAR, nullable=True)
    user_name = Column(VARCHAR, nullable=True)