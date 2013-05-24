#!/usr/bin/env python

"""
lackey daemon process
    
runs in the background and checks the database for new jobs to be run
"""

import os, sys
import urllib, urllib2, json
import threading, subprocess
from datetime import datetime


config = json.load(open('./config/lackey.json', 'r'))



def popenAndCall(onExit, job, *popenArgs, **popenKWArgs):
    """
        Runs a subprocess.Popen, and then calls the function onExit when the
        subprocess completes.
        
        Use it exactly the way you'd normally use subprocess.Popen, except include a
        callable to execute as the first argument. onExit is a callable object, and
        *popenArgs and **popenKWArgs are simply passed up to subprocess.Popen.
        """
    def runInThread(onExit, job, popenArgs, popenKWArgs):
        proc = subprocess.Popen(*popenArgs, **popenKWArgs)
        #proc.wait()
        proc.communicate()
        onExit(job, popenKWArgs.get('stdout'), popenKWArgs.get('stderr'))
        return
    
    thread = threading.Thread(target=runInThread, args=(onExit, job, popenArgs, popenKWArgs))
    thread.start()
    
    return thread # returns immediately after the thread starts


# Even threading is pretty easy in Python, but note that if onExit() is computationally expensive, you'll want to put this in a separate process instead using multiprocessing (so that the GIL doesn't slow your program down). It's actually very simple - you can basically just replace all calls to threading.Thread with multiprocessing.Process since they follow (almost) the same API.

def preExec(job):
    headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
    
    now = datetime.now()
    
    form_data = {'token': job['token'], 'ts':now.strftime('%s')}
    data = urllib.urlencode(form_data)
    
    url = config['application']['host'] + "api/run/start/" + str(job["id"])
    
    req = urllib2.Request(url, data, headers)

    f = urllib2.urlopen(req)
    response = f.read()
    f.close()



def postExec(job, stdout, stderr):
    headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
    
    now = datetime.now()
    
    stdout.seek(0)
    log = stdout.read()
    
    if stdout is not stderr:
        stderr.seek(0)
        log += stderr.read()
        stderr.close()
    
    stdout.close()
    
    form_data = {'token':job['token'], 'ts':now.strftime('%s'), 'log':log}
    data = urllib.urlencode(form_data)
    
    url = config['application']['host'] + "api/run/stop/" + str(job["id"])
    
    req = urllib2.Request(url, data, headers)
    
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    




url = config['application']['host'] + config['application']['jobs']
headers = {'Content-type': 'application/json'}
params = {}


request = urllib2.Request(url, None, {'Content-Type': 'application/json'})
f = urllib2.urlopen(request)
jobs = json.loads(f.read())
f.close()


for job in jobs:
    try:
        preExec(job)
        
        workdir = config['application']['workdir'] + job['directory']
        
        logfile = '%(dir)s/lackey.log' % {'dir':workdir}
        if os.path.isfile(logfile):
            os.remove(logfile)
        open(logfile, 'w').close()
        
        f = open(logfile, 'r+')
        
        popenAndCall(postExec, job, "cd %(dir)s; %(command)s " % {'dir' : workdir, 'command': job['command']}, cwd=workdir, stdout = f, stderr = f, shell=True)
    
    except urllib2.URLError, e:
        print 'you got an error with the code', e
