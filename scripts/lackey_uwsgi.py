#!/usr/bin/env python

#import os

#nginx_configuration = os.path.dirname(os.path.join(os.path.dirname(__file__), ".."))
#project = os.path.dirname(nginx_configuration)
#workspace = os.path.dirname(project)
#sys.path.append(workspace)

from lackey import get_app

application = get_app()

