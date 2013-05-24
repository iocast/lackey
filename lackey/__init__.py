

def get_app():
    from webapp import web
    from webapp.api import api
    #from webapp.api import application, project
    
    web.app.config.id = "lackey"
    web.app.config.prefix = ""
    web.app.config.path= ""
    
    
    api.api.config.path = lambda: web.app.config.path + api.api.config.prefix
    web.app.mount(app=api.api, prefix="/api")

    return web.app
    