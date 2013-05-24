# lackey <small>(at your service)</small>

> someone who is too willing to do whatever they are told to do, especially when the person, organization etc being obeyed is much more important or powerful
> -- <cite>[Macmillan Dictionary][1]</cite>

I'm helping you to run project specific tasks, in particular by running your simulation which your are too lazy to do manually.

Nevertheless I ask you to adhere some guidlines. Here they are:

TODO

## registration
When scheduling a new run, a unique token is assigned to it. Every change on such a run, is authenticated over this unique token.

An application can register a start using the follwoing command

    curl -i -H "Accept: application/json" -X PUT -d "token=99ee72e2-764d-42a9-b3a1-5c38d1647f28&ts=1369312595" http://localhost:8000/api/run/start/1

and stopping it as follow

    curl -i -H "Accept: application/json" -X PUT -d "token=99ee72e2-764d-42a9-b3a1-5c38d1647f28&ts=1369322595&log=asdf%20123" http://localhost:8000/api/run/stop/1

where ``ts`` is a **unix UTC timestamp**.


## installation

(1) installaling software

    > sudo apt-get install samba
    > sudo apt-get install python-virtualenv
    > sudo apg-get install uwsgi uwsgi-plugin-python
    > sudo apt-get install nginx


(2a) preparing environment

    > sudo mkdir -p /opt/virtualenv
    > cd /opt/virtualenv
    > virtualenv lackey
    > source lackey/bin/activate
    > pip install sqlalchemy
    > pip install bottle

(2b) preparing web application folder

    > sudo mkdir -p /var/www/lackey
    > sudo chown -R www-data:www-data /var/www/lackey/

(2c) preparing uwsgi vassals

    > sudo mkdir /etc/uwsgi/vassals


(3) preparing uWSGI Emperor

> If you need to deploy a big number of apps on a single server, or a group of servers, the Emperor mode is just the ticket.

> It is a special uWSGI instance that will monitor specific events and will spawn/stop/reload instances (known as vassals, when managed by an Emperor) on demand.

> By default the Emperor will scan specific directories for supported (.ini, .xml, .yml, .json, etc.) uWSGI configuration files, but you it is extensible using imperial monitor plugins
> -- <cite>[The uWSGI Emperor – multi-app deployment][2]</cite>

create for each application a new vassal in ``/etc/uwsgi/vassals/``

    > sudo vim /var/www/vassals/lackey.xml
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
        <virtualenv>/opt/virtualenv/lackey</virtualenv>
        <pythonpath>%d../%n</pythonpath>
        <chdir>%d../%n</chdir>
        <module>scripts.%n_uwsgi</module>
        <!-- <wsgi-file>%d../%n/scripts/lackey_wsgi.py</wsgi-file> -->
    </uwsgi>

spawn the Emperor

    > uwsgi --emperor /var/www/vassals

uWSGI does not automatically start. Use the startup manager of your system e.g ``upstart``

    > sudo vim /etc/init/uwsgi.conf
    # uWSGI - manage uWSGI application server                                                                                                                                                                
    #                                                                                                                                                                                                    
    
    description     "uWSGI Emperor"
    
    start on (filesystem and net-device-up IFACE=lo)
    stop on runlevel [!2345]
    
    respawn
    
    env LOGTO=/var/log/uwsgi.log
    env BINPATH=/usr/bin/uwsgi
    
    exec $BINPATH --emperor /var/www/vassals/ --logto $LOGTO

refrefsh servcies

    > sudo initctl reload-configuration


(4) preparing web server (add the following lines)

    > sudo vim /etc/nginx/sites-available/lackey_plus_dev.conf
    server {
            listen      80;
            charset     utf-8;
            server_name lackey.plus.dev.ethz.ch;
            root        /var/www/lackey;
            
            location /  {
                    include     uwsgi_params;
                    uwsgi_pass  unix:/tmp/uwsgi.lackey.socket;
            }
    }
    > cd /etc/nginx/sites-enabled
    > sudo ln -s ../sites-available/lackey_plus_dev.conf .

preparing exhange folder (samba)

    > sudo mkdir -p /opt/exchange


## restarting everything

    > sudo service nginx {start|stop|status|try-restart|restart|force-reload|reload|probe}
    > sudo service uwsgi {start|stop|status|try-restart|restart|force-reload|reload|probe}
    > sudo service smbd {start|stop|status|try-restart|restart|force-reload|reload|probe}


[1]:http://www.macmillandictionary.com/dictionary/british/lackey
[2]:http://uwsgi-docs.readthedocs.org/en/latest/Emperor.html
