from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Sequence, String, Text, Unicode, Integer, Float, DateTime
from sqlalchemy.orm import backref, relationship
from sqlalchemy.types import TypeDecorator

import json

Base = declarative_base()


###############################
# Types

class JsonType(TypeDecorator):
    impl = String
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value
    
    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


###############################
# Schema
class Project(Base):
    __tablename__ = 'project'
    
    id = Column(Integer, Sequence('project_id_seq'), primary_key=True)
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    directory = Column(String, nullable=False)
    
    # One-To-Many type
    applications = relationship('Application', cascade='all,delete,save-update')
    
    
    @property
    def json(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "title" : self.title,
            "description" : self.description,
            "directory" : self.directory
        }
        

class Application(Base):
    __tablename__ = 'application'
    
    id = Column(Integer, Sequence('application_id_seq'), primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    directory = Column(String, nullable=False)
    command = Column(String, nullable=False)
    
    #One-To-Many relationship type
    project_id = Column(Integer, ForeignKey('project.id'))
    project = relationship('Project')
    
    # One-To-Many type
    runs = relationship('Run', cascade='all,delete,save-update')


    @property
    def json(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "description" : self.description,
            "directory" : self.directory,
            "command" : self.command,
            "project_id" : self.project.id,
            "project_name" : self.project.name,
            "project_directory" : self.project.directory
        }

class Run(Base):
    __tablename__ = 'run'

    id = Column(Integer, Sequence('run_id_seq'), primary_key=True)
    directory = Column(String, nullable=False)
    command = Column(String, nullable=False)
    schedule = Column(DateTime, nullable=False)
    token = Column(String, nullable=False)
    raw_log = Column(String, nullable=True)
    start = Column(DateTime, nullable=True)
    end = Column(DateTime, nullable=True)

    #One-To-Many relationship type
    application_id = Column(Integer, ForeignKey('application.id'))
    application = relationship('Application')
    
    
    @property
    def json(self):
        #JavaScript:    'MM/dd/yyyy HH:mm:ss PP',
        #Python:        '%m/%d/%Y %I:%M:%S %p'
        return {
            "id" : self.id,
            "directory" : self.directory,
            "command" : self.command,
            "token" : self.token,
            "raw_log" : self.raw_log if self.raw_log is not None else "",
            "schedule" : self.schedule.strftime('%m/%d/%Y %I:%M:%S %p'),
            "start" : self.start.strftime('%m/%d/%Y %I:%M:%S %p') if self.start is not None else "",
            "end" : self.end.strftime('%m/%d/%Y %I:%M:%S %p') if self.end is not None else "",
            
            "duration" : (self.end - self.start).total_seconds() if self.start is not None and self.end is not None else "",
            "application_id" : self.application.id,
            "application_name" : self.application.name,
            "project_id" : self.application.project.id,
            "project_name" : self.application.project.name,
        }
