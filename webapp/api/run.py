import sys, os, json, re, bottle, uuid
from datetime import datetime


from lackey.database import DatabaseManagement
from lackey.base import RunSession
from lackey.orm import Run

api = bottle.Bottle();

config = json.load(open('./config/lackey.json', 'r'))
database = DatabaseManagement("%(dialect)s://%(uri)s" % {'dialect' : config['database']['dialect'], 'uri' : config['database']['uri'] % {'app': ''}})


@api.route('/list')
def api_runs():
    session = database.new_session()
    session.__class__ = RunSession
    return json.dumps(session.all.json)

@api.route('/jobs')
def api_runs():
    session = database.new_session()
    session.__class__ = RunSession
    return json.dumps(session.jobs.json)

@api.get('/<id>.raw')
def api_run(id):
    session = database.new_session()
    session.__class__ = RunSession
    return session.get(id)[0].raw_log

@api.get('/<id>')
def api_run(id):
    session = database.new_session()
    session.__class__ = RunSession
    return json.dumps(session.get(id).json)


@api.post('/application/<application_id>') # insert
def api_run_insert(application_id):
    out = {}
    
    session = database.new_session()
    session.__class__ = RunSession
    
    #JavaScript:    'MM/dd/yyyy HH:mm:ss PP',
    #Python:        '%m/%d/%Y %I:%M:%S %p'
    schedule = datetime.strptime(bottle.request.forms.get('schedule'), '%m/%d/%Y %I:%M:%S %p')
    

    try:
        entry = session.add(Run(
                                token = str(uuid.uuid4()),
                                schedule = schedule,
                                application_id = application_id
                                ))
        
        session.session.commit()
        
        out['status'] = "ok"
        out['entry'] = entry.json
    except Exception as  e:
        out["status"] = "error"
        out["message"] = e.message
        session.session.rollback()
    
    return json.dumps(out)


@api.post('/start/<id>') # update to cause of mordern browsers
@api.put('/start/<id>') # update
def api_project_update(id):
    session = database.new_session()
    session.__class__ = RunSession
    
    out = {}
    
    if bottle.request.forms.get('token') == session.get(id)[0].token:
        ts = bottle.request.forms.get('ts')
        if ts is not None:
            try:
                entry = session.start(id, float(ts))
                session.session.commit()
        
                out['status'] = "ok"
                out['entry'] = entry.json
            except Exception as  e:
                out["status"] = "error"
                out["message"] = e.message
                session.session.rollback()
        else:
            bottle.response.status = 400
            out["status"] = "error"
            out["message"] = "missing parameters"

    else:
        bottle.response.status = 401
        out["status"] = "error"
        out["message"] = "you are not authorized"
    
    return json.dumps(out)


@api.post('/stop/<id>') # update to cause of mordern browsers
@api.put('/stop/<id>') # update
def api_project_update(id):
    session = database.new_session()
    session.__class__ = RunSession
    
    out = {}
    
    if bottle.request.forms.get('token') == session.get(id)[0].token:
        ts = bottle.request.forms.get('ts')
        log = bottle.request.forms.get('log')
        
        if ts is not None and log is not None:
            try:
                entry = session.stop(id, float(ts), log)
                session.session.commit()
            
                out['status'] = "ok"
                out['entry'] = entry.json
            except Exception as  e:
                out["status"] = "error"
                out["message"] = e.message
                session.session.rollback()
        else:
            bottle.response.status = 400
            out["status"] = "error"
            out["message"] = "missing parameters"
    else:
        bottle.response.status = 401
        out["status"] = "error"
        out["message"] = "you are not authorized"
    
    return json.dumps(out)



@api.route('/search')
def api_runs_search():
    session = database.new_session()
    session.__class__ = RunSession
    
    out = []
    
    QUOTES_RE   = "('[^']+'|\"[^\"]+\")"
    FREETEXT_RE = "('[^']+'|\"[^\"]+\"|[^'\"\\s]\\S*)"
    CATEGORY_RE = FREETEXT_RE +                     ':\\s*'
    ALL_FIELDS  = re.compile(CATEGORY_RE + FREETEXT_RE)
    
    query = bottle.request.query.get('q')
    kvps = re.findall(ALL_FIELDS, query)
    
    values = []
    for kvp in kvps:
        category = kvp[0]
        value    = kvp[1]
        
        values.append({'category' : category.strip().strip('"').strip(), 'value' : value.strip().strip('"').strip()})
        kvp_re   = re.compile(category + ":\s*" + value)
        query = re.sub(kvp_re, '', query).strip()
    
    category = "text"
    value = re.sub(' +',' ', query)
    if len(value) > 0:
        values.append({'category' : category.strip().strip('"').strip(), 'value' : value.strip().strip('"').strip()})
    
    # sort by category
    values = sorted(values, key=lambda k: k['category'])
    
    # get distinct keys
    keys = set(map(lambda x:x['category'], values))
    
    # group by keys
    grouped = [{'key' : x, 'values' : [y["value"] for y in values if y["category"]==x] }for x in keys]
    
    return json.dumps(session.search(grouped).json)


