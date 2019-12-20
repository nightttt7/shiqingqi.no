# 工作日志

| tag  | 日期                 | 事项                           | 详细                                                         |
| ---- | ------------------ | ---------------------------- | ---------------------------------------------------------- |
| a1   | 2017/9/14          | 立项                           | 建立github项目；将readme同步到网易云笔记；计划优先作出dicts v1.0                |
| a2   | 2017/9/15          | 见详细                          | 加入template文件夹，增加模板文件base和index                             |
| None | 2017/9/16          | 停工                           | 补充相关知识                                                     |
| a3   | 2017/9/17          | 加入完整结构                       | 加入多个文件夹，更改templates位置，readme文件转移至有道云笔记链接方便修改               |
| None | 2017/9/18          | 加入chop文件夹                    | 加入chop文件夹                                                  |
| None | 2017/9/19          | 加入dicts文件夹                   | 加入dicts文件夹，并做了其他细节的修改                                      |
| None | 2017/9/20-23       | 停工                           | 补充相关知识                                                     |
| None | 2017/9/24          | 加入login                      | 加入login并修改了其他文件                                            |
| b1   | 2017/9/25          | 加入dicts                      | 修改了login的错误，上线成功，加入了词典集合dicts，可以进行自定义单词查询                  |
| None | 2017/9/26          | 改为使用mysql数据库，工作环境迁移至windows7 |         /                                                  |
| None | 2017/9/27-2018/3/9 | 停工                           | 搁置                                                         |
| None | 2018/3/10          | 修改计划                         | 更改项目名为nightttt7,不再使用网易云笔记作为readme,调整一些网页结构和文件结构的计划,开始缓慢的更新 |
| None | 2019/12/12         | new start                    | change develop evironment to windows10, change structures  |
| None | 2019/12/15         | basic edition                | have index, login, CV and Blog                             |
| None | 2019/12/20         | add post                     | /                                                          |
| None | 2019/12/20         | add comment                  | /                                                          |

# web structure

- homepage[Nightttt7's Blog]
    - .CV
    - (.Post Blog *if Bloger)
- Tool
    - ...
- Game
    - ...
- (Timesheet *if log in)
- (Keep *if log in)
- (profile [your email] *if log in)
- login (logout *if log in)
- (manage *if is Administrator)

# run development server

```
$env:FLASK_APP = "nightttt7.py"
$env:FLASK_DEBUG=1
flask run -h 127.0.0.1 -p 5000
```

# database

```
flask shell
db.drop_all()
db.create_all()
db.session.add(u)
db.session.delete(u)
db.session.commit()
Role.insert_roles()
User.giveblog('a@b.com')
```

```
flask db init
flask db migrate -m "comments"
flask db upgrade
```
