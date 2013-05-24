import os, sys, bottle


nginx_configuration = os.path.dirname(os.path.join(os.path.dirname(__file__), ".."))
project = os.path.dirname(nginx_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)


from lackey import get_app

def application(environment, response):
    return get_app().wsgi(environment, response)

