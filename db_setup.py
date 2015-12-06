__author__ = 'brettwatanabe'

import sys
import datetime
from sqlalchemy import create_engine, Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Topic(Base):
    __tablename__ = 'topic'
    id = Column(Integer, primary_key = True)
    topic = Column(String(20), nullable = False)
    note = relationship("Note", cascade="all, delete-orphan")

class Note(Base):
    __tablename__ = 'note'
    id = Column(Integer, primary_key = True)
    title = Column(String(20), nullable = False)
    message = Column(String(200), nullable = False)
    lastUpdatedTime = Column(DateTime, default= datetime.datetime.now(), onupdate=datetime.datetime.now())
    topic_id = Column(Integer, ForeignKey('topic.id'))
########insert at end of file############

engine = create_engine('sqlite:///noted.db')

Base.metadata.create_all(engine)