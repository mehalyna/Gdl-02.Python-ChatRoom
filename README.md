# Gdl-02.Python-ChatRoom
Project ChatRoom performed by Gdl-02.Python/Zenoss group

## For contributors
### Project setup

Inside the project create the virtual environment \
Linux command
```
python3 -m venv venv
```
Windows command
```
py -3.10 -m venv .venv
```
Activate the environment\
Linux command
```
source venv/bin/activate
```
Windows command
```
.venv\Scripts\activate
```
Install the requirements
```
python3 -m pip install -r requirements.txt
```
Addd to the .env file the next lines, or create the file if it does not exits
```
nano .env
```
```
DEBUG=True
SECRET_KEY=KBl3sX5kLrd2zxj-pAichjT0EZJKMS0cXzhWI7Cydqc
DATABASE_URL=sqlite:///db.sqlite3
```
Migrate the database
```
python manage.py makemigrations
python manage.py migrate
```
Enable a channel layer
```
docker run -p 6379:6379 -d redis:5
```
Run the project
```
python manage.py runserver
```
### Git Flow
We are using simpliest github flow to organize our work:
![Git Flow Ilustration](https://github.com/mehalyna/Share-images/blob/main/68747470733a2f2f7363696c6966656c61622e6769746875622e696f2f736f6674776172652d646576656c6f706d656e742f696d672f6769746875622d666c6f772e706e67.png)

### Note! Contribution rules:
1. All Pull Requests should start from prefix #xxx-yyy where xxx - task number and and yyy - short description e.g. #020-CreateAdminPanel
2. Pull request should not contain any files that is not required by task.

In case of any violations, pull request will be rejected.
