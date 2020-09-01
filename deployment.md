#Flask Deployment
------------------

**Create a Virtual Environment**
```
apt install virtualenv
cd {project_folder}
source .venv/bin/activate
```
**Install Requirements**
```
pip install -r requirements.txt
```

##Setup & configure ```gunicorn```
**Install gunicorn**
```
pip install gunicorn
gunicorn -b localhost:8880 -w 4 wsgi:app
```

**dotenv environment variables loading**
```
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from main import app as application

if __name__ == '__main__':
    application.run()
```
**gunicorn config file**
```
# file gunicorn.conf.py
# coding=utf-8
# Reference: https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py
import os
import multiprocessing

_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..'))
_VAR = os.path.join(_ROOT, 'var')
_ETC = os.path.join(_ROOT, 'etc')

loglevel = 'info'
# errorlog = os.path.join(_VAR, 'log/api-error.log')
# accesslog = os.path.join(_VAR, 'log/api-access.log')
errorlog = "-"
accesslog = "-"

# bind = 'unix:%s' % os.path.join(_VAR, 'run/gunicorn.sock')
bind = '0.0.0.0:5000'
# workers = 3
workers = multiprocessing.cpu_count() * 2 + 1

timeout = 3 * 60  # 3 minutes
keepalive = 24 * 60 * 60  # 1 day

capture_output = True
```
Then start gunicorn app with -c option
```
gunicorn -c etc/gunicorn.conf.py wsgi
```

#Supervisor
```
sudo apt install supervisor
```
**Check if supervisor service is running**
```
service supervisor status
```
**Create a configuration file for our API project**
```
sudo nano /etc/supervisor/conf.d/pythonbot.conf
```
```
;/etc/supervisor/conf.d/pythonbot.conf
[program:pythonbot]
user = wolfmann911
directory = /home/wolfmann911/project/pythonbot
command = /home/wolfmann911/project/pythonbot/run.sh gunicorn -c etc/gunicorn.conf.py wsgi
priority = 900
autostart = true
autorestart = true
stopsignal = TERM
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/pythonbot/pythonbot.err.log
stdout_logfile=/var/log/pythonbot/pythonbot.out.log
```
The run.sh script above is just a simple wrapper to activate Python virtual environment before actually execute the upcoming command. 
```
#!/bin/bash -e

if [ -f pythonbotenv/bin/activate ]; then
    echo   "Load Python virtualenv from 'pythonbotenv/bin/activate'"
    source pythonbotenv/bin/activate
fi
exec "$@"
```
Add permisison if needed
```
chmod +x run.sh
```
**Start gunicorn app with supervisor**
```
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl avail
sudo supervisorctl restart pythonbot
```
Reload whole supervisor service
```
sudo service supervisor restart
```

**Install nginx**
```
sudo apt install nginx
```
**Configure nginx**
* Remove default
- sudo rm /etc/nginx/sites-enabled/default
```
sudo touch /etc/nginx/sites-available/pythonbot
sudo ln -s /etc/nginx/sites-available/pythonbot /etc/nginx/sites-enabled/api_project
sudo nano /etc/nginx/sites-available/pythonbot
```
```
server {
    listen 80;
    server_name http://192.99.186.16/;
    location / {
        proxy_pass "http://localhost:8000";
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        fastcgi_read_timeout 300s;
        proxy_read_timeout 300;
    }
    location /static {
        alias  /home/wolfmann911/project/pythonbot/static/;
    }
    error_log  /var/log/nginx/api-error.log;
    access_log /var/log/nginx/api-access.log;
}
```
Check config and restart
```
sudo nginx -t
sudo service nginx restart
```

Open firewall (If needed)
```
sudo ufw allow htt/tcp
sudo ufw enable
```

Log check
```
sudo less /var/log/nginx/error.log: checks the Nginx error logs.
sudo less /var/log/nginx/access.log: checks the Nginx access logs.
sudo journalctl -u nginx: checks the Nginx process logs.
sudo journalctl -u pythonbot: checks your Flask app’s Gunicorn logs.
```



The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.
```
mkdir /tmp/.X11-unix
sudo chmod 1777 /tmp/.X11-unix
sudo chown root /tmp/.X11-unix
```

It can also happen that Xvfb crashed but still blocking the display port. It is then not possible to restart Xvfb on the same display port:
Fatal server error:
Server is already active for display 1337
    If this server is no longer running, remove /tmp/.X1337-lock
    and start again.
As suggested from the message the lock file needs to be removed:
rm /tmp/.X1337-lock
Afterwards it is possible to start Xvfb again on display port 1337.



export DISPLAY=:0 XAUTHORITY=/etc/X11/host-Xauthority
Xephyr :1 -fullscreen


less /var/log/pythonbot/pythonbot.err.log
less /var/log/pythonbot/pythonbot.out.log


less /var/www/html/python-services/pythonbot/logs/nginx/access.log
less /var/www/html/python-services/pythonbot/logs/nginx/error.log
