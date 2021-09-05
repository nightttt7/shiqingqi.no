# log

| date                 | log                                                                        | detail                                                                                                                                                                |
| -------------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2017/9/14            | start project                                                              | Set up github project; sync readme to Netease cloud notes; plan to make dicts v1.0 first                                                                              |
| 2017/9/15            |                                                                            | Add template folder, add template file base and index                                                                                                                 |
| 2017/9/16            | Shutdown                                                                   | Supplementary knowledge                                                                                                                                               |
| 2017/9/17            | Add the complete structure                                                 | Add multiple folders, change templates location, transfer readme files to Youdao Cloud Notes link for easy modification                                               |
| 2017/9/18            | add chop folder                                                            | add chop folder                                                                                                                                                       |
| 2017/9/19            | add dicts folder                                                           | Added dicts folder and modified other details                                                                                                                         |
| 2017/9/20-23         | Shutdown                                                                   | Supplementary knowledge                                                                                                                                               |
| 2017/9/24            | add login function                                                         | Joined login and modified other files                                                                                                                                 |
| 2017/9/25            | add dicts function                                                         | Corrected the login error, went online successfully, added the dictionary set dicts, and can perform custom word queries                                              |
| 2017/9/26            | Use mysql database instead and migrate the working environment to windows7 | /                                                                                                                                                                     |
| 2017/9/27-2018/3/9   | Shutdown                                                                   | Put on hold                                                                                                                                                           |
| 2018/3/10            | Modify plan                                                                | Change the project name to nightttt7, no longer use Netease Cloud Notes as a readme, adjust some web page structure and file structure plans, and start a slow update |
| 2018/3/11-2019/12/11 | Shutdown                                                                   | Started work, failed to modify plan, shelved                                                                                                                          |
| 2019/12/12           | new start                                                                  | change develop evironment to windows10, change structures                                                                                                             |
| 2019/12/15           | basic edition                                                              | have index, login, CV and Blog                                                                                                                                        |
| 2019/12/20           | add post                                                                   | add post related part                                                                                                                                                 |
| 2019/12/20           | add comment                                                                | add post comment part                                                                                                                                                 |
| 2019/12/22           | add register                                                               | add post register part, this web "could in use" now                                                                                                                   |
| 2019/12/23           | pause                                                                      | next plan: change the front-end, try to use React and Primer                                                                                                          |
| 2019/12/30           | ready to production environment                                            | next: deploy in a linux server                                                                                                                                        |
| 2020/3/15            | deploy                                                                     | deploy in linux server. Addon Domain                                                                                                                                  |
| 2020/7/4             | start to use Primer CSS                                                    | base and markdown                                                                                                                                                     |
| 2020/7/5             | change front-end to Primer CSS                                             | all to Primer CSS                                                                                                                                                     |
| 2020/7/6             | change and adapt                                                           | change login and reg page, adapt for cellphone                                                                                                                        |
| 2020/8/7             | add timesheet page                                                         | something new and javascript                                                                                                                                          |
| 2021/1/22            | change server to AWS                                                       | change server                                                                                                                                                         |
| 2021/7/19            | change name and fine tune contents                                         | change server                                                                                                                                                         |
| 2021/8/31            | add new features                                                           | change server                                                                                                                                                         |

# environment

- development: windows10, python3.8, VSCode

# pip freeze

```
pip3 freeze > requirements.txt
pip3 install -r requirements.txt
```

# before everything

```
cd my-project-directory
```

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

User.giveblog('a@b.com')
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

- for local access
```
flask run -h 0.0.0.0 -p 5000
```

# run production server

- environment setting (example)

```
export FLASK_APP=filename.py
export FLASK_CONFIG=production
export FLASK_DEBUG=0
export FLASK_ADMIN=xxx@xxx.com
export SECRET_KEY='xxxxxxx'
DATABASE_URL=mysql+pymysql://username:password@host/database
```

- change dir

```
cd qingqi.no
```

- git pull

```
git pull
```

- run Gunicorn only

```
pkill gunicorn
gunicorn --bind 0.0.0.0:443 nightttt7:app
```

- run Gunicorn and Nginx
```
pkill gunicorn
gunicorn --bind 127.0.0.1:7777 nightttt7:app &
```

- if more workers supported
```
pkill gunicorn
gunicorn --workers 2 --bind 127.0.0.1:7777 nightttt7:app &
```

- file /etc/nginx/sites-available/default

```
server {
    listen                 443;
    server_name            nightttt7.no www.nightttt7.no;

    ssl                    on;
    ssl_certificate        /etc/letsencrypt/live/shiqingqi.no/fullchain.pem;
    ssl_certificate_key    /etc/letsencrypt/live/shiqingqi.no/privkey.pem;

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

- about firewall

```
ufw allow 'Nginx Full'
```

- renew SSL

```
certbot renew
```