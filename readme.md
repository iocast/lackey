# lackey <small>(at your service)</small>

> someone who is too willing to do whatever they are told to do, especially when the person, organization etc being obeyed is much more important or powerful
> -- <cite>[Macmillan Dictionary][1]</cite>

I'm helping you to run project specific tasks, in particular by running your simulation which you are too lazy to do manually.

Nevertheless I ask you to adhere some guidlines. Here they are:


## registration
When scheduling a new run, a unique token is assigned to it. Every change on such a run, is authenticated over this unique token.

An application can register a start using the follwoing command

    curl -i -H "Accept: application/json" -X PUT -d "token=99ee72e2-764d-42a9-b3a1-5c38d1647f28&ts=1369312595" http://localhost:8000/api/run/start/1

and stopping it as follow

    curl -i -H "Accept: application/json" -X PUT -d "token=99ee72e2-764d-42a9-b3a1-5c38d1647f28&ts=1369322595&log=asdf%20123" http://localhost:8000/api/run/stop/1

where ``ts`` is a **unix UTC timestamp**.


## prerequisites

* samba >= 3.6.3
* Python >= 2.7.3

### Python libraries

* SQLAlchemy >= 0.8.1
* argparse >= 1.2.1
* bottle >= 0.11.6
* distribute >= 0.6.24
* wsgiref >= 0.1.2

## installation

following variables are used in the following instruction

* `<path-to-www>`
* `<path-to-virtualenv>`


**(1) installation**

download latest release from [GitHub/iocast/lackey](https://github.com/iocast/lackey).

create a new folder in your www root folder

    sudo mkdir -p /<path-to-www>/lackey
	sudo chwon -R www-data:www-data /<path-to-www>/lackey/

copy all the files into the folder ``/<path-to-www>/lackey/``


**(2) configuration virtualenv**

go to your ``virtualenv`` environment folder or create a new folder in your application

    cd /<path-to-virtualenv>
	virtualenv lackey
	source lackey/bin/activate
	pip install sqlalchemy
	pip install bottle


### uwsgi

**(3a) vassal**

this is needed if you are using the `--emperor` when starting `uwsgi`

	sudo vim /<path-to-vassals>/lackey.xml

and add the following lines

	<uwsgi>
	    <vhost>true</vhost>
	    <plugins>python</plugins>
	    <master>true</master>
	    <processes>1</processes>
	    <vaccum>true</vaccum>
	    <chmod-socket>666</chmod-socket>
	    <socket>/tmp/uwsgi.%n.socket</socket>
	    <uid>www-data</uid>
	    <gid>www-data</gid>
	    <virtualenv>/<path-to-virtualenv>/lackey</virtualenv>
	    <pythonpath>%d../%n</pythonpath>
	    <chdir>%d../%n</chdir>
	    <module>scripts.%n_uwsgi</module>
	    <!-- <wsgi-file>%d../%n/scripts/lackey_wsgi.py</wsgi-file> -->
	</uwsgi>

### nginx

**(3b) enabling site**

	sudo vim /etc/nginx/sites-available/lackey.conf


	and add the following lines:
	<code javascript >
	server {
	    listen      80;
	    charset     utf-8;
	    server_name lackey.localhost;
	    root        /<path-to-www>/lackey;
    
	    location /  {
	        include     uwsgi_params;
	        uwsgi_pass  unix:/tmp/uwsgi.lackey.socket;
	    }
	}
	</code>

enable it as follow:

	cd /etc/nginx/sites-enabled
	sudo ln -s ../sites-available/lackey.conf .



## TODO

* TODO: [ ] run imediately
* TODO: [ ] list of active runs / jobs


[1]:http://www.macmillandictionary.com/dictionary/british/lackey
[2]:http://uwsgi-docs.readthedocs.org/en/latest/Emperor.html
