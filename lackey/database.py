from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError


class ObjectList(object):
    @property
    def all(self):
        return self._objects
    
    def __init__(self, objects):
        super(ObjectList, self).__init__()
        self._objects = objects
    
    @property
    def json(self):
        raise NotImplementedError("Subclasses should implement this!")

    def __len__(self):
        return len(self.all)

    def __getitem__(self, index):
        return self.all[index]
            



class DatabaseManagement(object):
    
    @property
    def uri(self):
        return self._uri
    @property
    def engine(self):
        return self._engine
    
    def __init__(self, uri):
        super(DatabaseManagement, self).__init__()
        self._uri       = uri
        self._engine    = None
    
    def new_session(self):
        if self._engine is None:
            self._engine = create_engine(self.uri, echo=False)
        return DatabaseSession(sessionmaker(bind=self.engine)())
    
    def create(self, base):
        base.metadata.create_all(create_engine(self.uri, echo=False))



class DatabaseSession(object):
    
    @property
    def session(self):
        return self._session
    
    def __init__(self, session):
        super(DatabaseSession, self).__init__()
        self._session = session



class ResultList(ObjectList):
    
    @property
    def json(self):
        json = []
        
        for entry in self.all:
            json.append(entry.json)
        
        return json
    
