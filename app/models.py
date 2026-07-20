from sqlalchemy import Column,BigInteger,String,Boolean,DateTime, text
from . database import Base
# from sqlalchemy.ext.declarative import declarative_base

# Base=declarative_base()
# metadata=Base.metadata
class tasks(Base):
    __tablename__="Tasks"
    id=Column(BigInteger, primary_key=True, nullable=False)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False)
    completed=Column(Boolean, nullable=False, server_default="False")
    created_at=Column(DateTime(timezone=True),nullable=False, server_default=text('now()'))
    
class Users(Base):
    __tablename__="users"
    id=Column(BigInteger, primary_key=True, nullable=False)
    username=Column(String, nullable=False)
    email=Column(String,nullable=False)
    password=Column(String,nullable=False)
    created_at=Column(DateTime(timezone=True), nullable=False, server_default=text('now()'))
    
