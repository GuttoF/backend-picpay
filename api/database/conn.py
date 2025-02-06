from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP, DECIMAL, func
from sqlalchemy.orm import Session, relationship, sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

db_url = "url" # view later

try:
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except SQLAlchemyError as e:
    print("Error", e) # view later


Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id  = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(200), nullable=False)
    cpf_cnpj = Column(String(14), nullable=False, unique=True)
    email = Column(String(200), nullable=False, unique=True)
    balance = Column(DECIMAL(10,2), default=0.00)
    phone =  Column(String(11), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    origin_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    origin = relationship("User", foreign_keys=[origin_id])
    destination = relationship("User", foreign_keys=[destination_id])

class CreateTransaction(BaseModel):
    origin_cpf_cnpj: str
    destination_cpf_cnpj: str
    amount: float

class PushBalance(BaseModel):
    origin_cpf_cnpj: str
    amount: float
