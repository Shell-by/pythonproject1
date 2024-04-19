import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Date
from database import Base
from uuid import UUID, uuid4


class Users(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, index=True, default=str(uuid4()))
    name = Column(String, unique=False)
    token = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)


class Tel(Base):
    __tablename__ = 'tel'

    id = Column(String, primary_key=True, index=True, default=str(uuid4()))
    users_id = Column(String, ForeignKey('users.id'))
    name = Column(String, unique=False)
    tel = Column(String, unique=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)


class Check_Date(Base):
    __tablename__ = 'check_date'

    id = Column(String, primary_key=True, index=True, default=str(uuid4()))
    name = Column(String, unique=False)
    is_korean_luna = Column(Boolean, unique=False, default=False)
    date = Column(Date)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)
