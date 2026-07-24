from sqlalchemy import Column,BigInteger,String,Boolean,DateTime, text,ForeignKey
from . database import Base
from sqlalchemy.sql import func
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
    updated_at=Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    users_id=Column(BigInteger,ForeignKey("users.id", ondelete='CASCADE'))
    
class Users(Base):
    __tablename__="users"
    id=Column(BigInteger, primary_key=True, nullable=False)
    username=Column(String, nullable=False)
    email=Column(String,nullable=False,unique=True)
    google_id=Column(String,nullable=False,unique=True)
    created_at=Column(DateTime(timezone=True), nullable=False, server_default=text('now()'))

class Groups(Base):
    __tablename__="Group"
    id=Column(BigInteger, primary_key=True, nullable=False)
    name=Column(String, nullable=False)
    description=Column(String, nullable=False)
    created_at=Column(DateTime(timezone=True),nullable=False,server_default=text('now()'))
    updated_at=Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    owners_id=Column(BigInteger,ForeignKey("users.id", ondelete='CASCADE'))
    
    
