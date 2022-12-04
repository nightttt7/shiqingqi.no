# log
- 2017-09-14: start project 
- 2017-09-16: shut down
- 2017-09-18: add 2 simple folder
- 2017-09-20: shut down
- 2017-09-24: add login function
- 2017-09-26: change database to mysql
- 2017-09-27: shut down
- 2018-03-10: change the project name to nightttt7
- 2018-03-11: shut down
- 2019-12-12: new start
- 2019-12-15: basic edition (have index, login and Blog)
- 2019-12-20: add post (add post related part)
- 2019-12-20: add comment (add post comment part)
- 2019-12-22: add register (add post register part, this web "could in use" now)
- 2019-12-23: pause
- 2019-12-30: ready to production environment
- 2020-03-15: deploy
- 2020-07-04: start to use Primer CSS (base and markdown)
- 2020-07-05: change front-end to Primer CSS (all to Primer CSS)
- 2020-07-06: change and adapt (change login and reg page, adapt for cellphone)
- 2020-08-07: add timesheet page (something new and javascript)
- 2021-01-22: change server to AWS
- 2021-07-19: change name and fine tune contents
- 2021-08-31: add new features
- 2022-01-28: start to REST API and React

# requirements
```
pip freeze > requirements.txt
pip install -r requirements.txt
```

# manual installation
- ARM Linux: pandas (apt install python3-pandas)
- Linux python: gunicorn
- Linux: nginx

# database
```
flask shell
db.drop_all()
db.create_all()
Role.insert_roles()

u = User(email='xxx', username='xxx', password='xxx')
db.session.add(u)
db.session.delete(u)
db.session.commit()
```

# upgrade database
```
# flask db init
flask db migrate -m "comment"
flask db upgrade
```

# run development server
- environment setting
    - file .env
    - this file should not exist in production environment

- run (after start venv)
```
flask run -h 127.0.0.1 -p 5000
```

- for local access (after start venv) (may need to open the port)
```
flask run -h 0.0.0.0 -p 5000
```

# run production server
- environment setting
```
export FLASK_APP=run.py
export FLASK_CONFIG=production
export FLASK_DEBUG=0
export FLASK_ADMIN=xxx@xxx.com
export SECRET_KEY='xxxxxxx'
DATABASE_URL=mysql+pymysql://username:password@host/database
```

- change dir
```
cd lovecatcat.com
```

- run Gunicorn only

```
pkill gunicorn
gunicorn --bind 0.0.0.0:443 run:app
```

- run Gunicorn and Nginx
```
pkill gunicorn
gunicorn --bind 127.0.0.1:7777 run:app &
```

- if more workers supported
```
pkill gunicorn
gunicorn --workers 2 --bind 127.0.0.1:7777 run:app &
```

- nginx setting (only https): /etc/nginx/sites-available/default
```
server {
    listen                 443;
    server_name            lovecatcat.com www.lovecatcat.com;

    ssl                    on;
    ssl_certificate        /etc/letsencrypt/live/lovecatcat.com/fullchain.pem;
    ssl_certificate_key    /etc/letsencrypt/live/lovecatcat.com/privkey.pem;

    location / {
        include            proxy_params;
        proxy_pass         http://127.0.0.1:7777/;
    }
}
```

- restart nginx
```
systemctl restart nginx
```

- firewall setting
```
ufw allow 'Nginx Full'
```
