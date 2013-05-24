import sys, os, json, bottle

bottle.TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), "../templates"))

app = bottle.default_app()


@app.route('/assets/:path#.+#')
def server_static(path):
    return bottle.static_file(path, root='./assets')


@app.route('/')
@app.route('/index.html')
@app.route('/home')
@app.route('/home.html')
@bottle.view('home')
def index():
    return dict(title="At your service!", menu="index")

@app.route('/projects')
@bottle.view('projects')
def projects():
    return dict(title="List of all Projects", menu="projects", path=app.config.path)



@app.route('/applications')
@bottle.view('applications')
def projects():
    query = bottle.request.params.get('q')
    if query is None:
        query = ""
    return dict(title="List of all Applications", menu="applications", path=app.config.path, query=query)


@app.route('/runs')
@bottle.view('runs')
def projects():
    query = bottle.request.params.get('q')
    if query is None:
        query = ""
    return dict(title="List of all runs", menu="runs", path=app.config.path, query=query)

