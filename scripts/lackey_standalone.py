#!/usr/bin/env python
import sys, os, argparse, json

# add packages
try:
    import bottle
except:
    sys.path.append(os.path.join(os.path.dirname(__file__), "../packages"))
    import bottle


sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from lackey import get_app


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="platform management")
    parser.add_argument('-p', '--port', help="port", required=False, default=8000)
    parser.add_argument('-g', '--debug', help="enables debugging (boolean switch to trueI)", action='store_true', required=False, default=False)
    parser.add_argument('-i', '--init', help="initialize application (removes everything)", action='store_true', required=False, default=False)
    
    args = parser.parse_args()
    
    
    config = json.load(open('./config/lackey.json', 'r'))
    
    if args.init:
        if os.path.isfile(config['database']['uri'] % {'app': "."}):
            os.remove(config['database']['uri'] % {'app': "."})
    
    if not os.path.isfile(config['database']['uri'] % {'app': "."}):
        from lackey.database import DatabaseManagement
        from lackey.orm import Base
        
        database = DatabaseManagement("%(dialect)s://%(uri)s" % {'dialect' : config['database']['dialect'], 'uri' : config['database']['uri'] % {'app': ""}})
        database.create(Base)
    
    
    
    bottle.debug(args.debug)
    bottle.run(app=get_app(), host='localhost', port=args.port, quiet=False, reloader=True)


