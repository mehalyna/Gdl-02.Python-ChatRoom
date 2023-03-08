# Gdl-02.Python-ChatRoom
Project ChatRoom performed by Gdl-02.Python/Zenoss group

## For contributors
### Project setup
Linux setup
Inside the project create the virtual environment 
 #+begin_src sh
python3 -m venv venv
#+end_src
Activate the environment
#+begin_src sh
source venv/bin/activaten
#+end_src
Install the requirements
#+begin_src sh
python3 -m pip install -r requirements.txt
#+end_src
Addd to the .env file the next lines
#+begin_src sh
nano .env
#+end_src
#+begin_src sh
DEBUG=True
SECRET_KEY=KBl3sX5kLrd2zxj-pAichjT0EZJKMS0cXzhWI7Cydqc
DATABASE_URL=sqlite:///db.sqlite3
#+end_src
Migrate the database
#+begin_src sh
python manage.py makemigrations
python manage.py migrate
#+end_src
Run the project
#+begin_src sh
python manage.py runserver
#+end_src
### Git Flow
We are using simpliest github flow to organize our work:
![Git Flow Ilustration](https://github.com/mehalyna/Share-images/blob/main/68747470733a2f2f7363696c6966656c61622e6769746875622e696f2f736f6674776172652d646576656c6f706d656e742f696d672f6769746875622d666c6f772e706e67.png)

### Note! Contribution rules:
1. All Pull Requests should start from prefix #xxx-yyy where xxx - task number and and yyy - short description e.g. #020-CreateAdminPanel
2. Pull request should not contain any files that is not required by task.

In case of any violations, pull request will be rejected.
