import sys, os, json, re, bottle


from lackey.database import DatabaseManagement
from lackey.base import ProjectSession
from lackey.orm import Project

api = bottle.Bottle();

config = json.load(open('./config/lackey.json', 'r'))
database = DatabaseManagement("%(dialect)s://%(uri)s" % {'dialect' : config['database']['dialect'], 'uri' : config['database']['uri'] % {'app': ''}})

@api.route('/list')
def api_projects():
    session = database.new_session()
    session.__class__ = ProjectSession
    return json.dumps(session.all.json)

@api.get('/<id>')
def api_project_get(id):
    session = database.new_session()
    session.__class__ = ProjectSession
    return json.dumps(session.get(id).json)

@api.post('/') # insert
def api_project_insert():
    out = {}
    
    session = database.new_session()
    session.__class__ = ProjectSession

    try:
        entry = session.add(Project(
                                    name = bottle.request.forms.get('name'),
                                    title = bottle.request.forms.get('title'),
                                    description = bottle.request.forms.get('description'),
                                    directory = bottle.request.forms.get('directory')
                            ))
    
        session.session.commit()

        out['status'] = "ok"
        out['entry'] = entry.json
    except Exception as  e:
        out["status"] = "error"
        out["message"] = e.message
        session.session.rollback()

    return json.dumps(out)


@api.post('/<id>') # update to cause of mordern browsers
@api.put('/<id>') # update
def api_project_update(id):
    out = {}

    session = database.new_session()
    session.__class__ = ProjectSession

    try:
        entry = session.session.query(Project).filter(Project.id == id).one()
    
        entry.name = bottle.request.forms.get('name')
        entry.title = bottle.request.forms.get('title')
        entry.description = bottle.request.forms.get('description')
        entry.directory = bottle.request.forms.get('directory')
    
        entry = session.edit(entry)
        session.session.commit()
    
        out['status'] = "ok"
        out['entry'] = entry.json
    except Exception as e:
        out["status"] = "error"
        out["message"] = e.message
        session.session.rollback()
    
    return json.dumps(out)

@api.delete('/<id>')
def api_project_delete(id):
    session = database.new_session()
    session.__class__ = ProjectSession

    session.delete(id)
    session.session.commit()


@api.route('/search')
def api_projects_search():
    session = database.new_session()
    session.__class__ = ProjectSession

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

