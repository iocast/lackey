from datetime import datetime

from sqlalchemy import or_, and_

from .orm import Project, Application, Run
from .database import DatabaseSession, ResultList


class ProjectSession(DatabaseSession):

    @property
    def all(self):
        return ResultList(self.session.query(Project).all())

    def get(self, id):
        return ResultList([self.session.query(Project).filter(Project.id == id).one()])
    
    def edit(self, project):
        self.session.add(project)
        self.session.flush()
        return project

    def add(self, project):
        self.session.add(project)
        self.session.flush()
        return project

    def delete(self, id):
        project = self.session.query(Project).filter(Project.id == id).one()
        self.session.delete(project)

    def search(self, search):
        q = self.session.query(Project)
        clauses = []
        
        for column in search:
            if column['key'] == "text":
                q = q.filter(or_(*map(lambda n: Project.description.like("%%%s%%" % n), column['values'])))
            else:
                q = q.filter(or_(*map(lambda n: getattr(Project, column["key"]).ilike("%%%s%%" % n), column['values'])))
        
        return ResultList(q.distinct())

    def applications(self, id):
        return ResultList(self.session.query(Application).filter(Application.project_id == id).all())



class ApplicationSession(DatabaseSession):
    
    @property
    def all(self):
        return ResultList(self.session.query(Application).all())
    
    def get(self, id):
        return ResultList([self.session.query(Application).filter(Application.id == id).one()])

    def edit(self, application):
        self.session.add(application)
        self.session.flush()
        return application

    def add(self, application):
        self.session.add(application)
        self.session.flush()
        return application

    def delete(self, id):
        application = self.session.query(Application).filter(Application.id == id).one()
        self.session.delete(application)


    def search(self, search):
        q = self.session.query(Application)
        clauses = []
        
        for column in search:
            if column['key'] == "text":
                q = q.filter(or_(*map(lambda n: Application.description.like("%%%s%%" % n), column['values'])))
            else:
                q = q.filter(or_(*map(lambda n: getattr(Application, column["key"]).ilike("%%%s%%" % n), column['values'])))
        
        return ResultList(q.distinct())

    def runs(self, id):
        return ResultList(self.session.query(Run).filter(Run.application_id == id).all())


class RunSession(DatabaseSession):

    @property
    def all(self):
        return ResultList(self.session.query(Run).all())
    
    @property
    def jobs(self):
        return ResultList(self.session.query(Run).filter(and_(Run.schedule <= datetime.now(), Run.start == None)).all())
    
    @property
    def running(self):
        return ResultList(self.session.query(Run).filter(and_(Run.start != None, Run.end == None)).all())

    def get(self, id):
        return ResultList([self.session.query(Run).filter(Run.id == id).one()])
    
    def add(self, run):
        run.application = self.session.query(Application).filter(Application.id == run.application_id).one()
        run.directory = run.application.project.directory + run.application.directory
        run.command = run.application.command
        
        self.session.add(run)
        self.session.flush()
        return run
    
    def edit(self, run):
        self.session.add(run)
        self.session.flush()
        return run
    
    def start(self, id, ts):
        run = self.get(id)[0]
        run.start = datetime.fromtimestamp(ts)
        return self.edit(run)
    
    def stop(self, id, ts, log):
        run = self.get(id)[0]
        run.end = datetime.fromtimestamp(ts)
        run.raw_log = log
        return self.edit(run)

    def search(self, search):
        q = self.session.query(Run)
        clauses = []
    
        for column in search:
            if column['key'] == "text":
                q = q.filter(or_(*map(lambda n: Run.raw_log.like("%%%s%%" % n), column['values'])))
            else:
                q = q.filter(or_(*map(lambda n: getattr(Run, column["key"]).ilike("%%%s%%" % n), column['values'])))
        
        return ResultList(q.distinct())

