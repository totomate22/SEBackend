# 1. Dependencies

Python<br>
PIP<br>
PostgreSQL<br>

pipenv<br>
django<br>
psycopg2<br>
Pillow<br><br>

# 2. Installation (Windows 11)

In the following, “Terminal” refers to the Windows Powershell.<br>

## 2.1 Install Dependencies

First, install the following programms:<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;[python](https://www.python.org/downloads/)<br>

&nbsp;&nbsp;&nbsp;&nbsp;[PIP](https://pip.pypa.io/en/stable/installation/) 
*(usually, pip is automatically installed when installing python downloaded 
from [python.org](https://www.python.org/downloads/))*<br>

&nbsp;&nbsp;&nbsp;&nbsp;[PostgreSQL](https://sbp.enterprisedb.com/getfile.jsp?fileid=1259363)<br>

## 2.2 Prerequisites

**Since this project uses django as the main framework and a PostgreSQL database:**<br>
We have to create a PostgreSQL database accessible by django, <br> instead of the django-default SQLite database.<br>
To do this, just open a terminal anywhere and follow the next steps.<br>
By default, for this app you can use the following commands to create the PostgreSQL database:<br>

**2.2.1** Create the database with the default psql superuser (in this case the superuser is called `postgres`)<br>
  `psql -U PostgreSQL db`<br>
* *after hitting Enter, the command prompt should change and show `db=#` before the cursor*<br>

**2.2.2** Create the User "django_user" and give it all necessary privileges for the DB.<br>
Please copy and paste the following commands behind `db=#` to your terminal, one after one:<br><br>
  `CREATE USER django_user WITH PASSWORD 'IchLiebeGA;'`<br>
  `GRANT USAGE ON SCHEMA public TO django_user;`<br>
  `GRANT CREATE ON SCHEMA public TO django_user;`<br>
  `GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO django_user;`<br>
  `GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO django_user;`<br>
  `GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO django_user;`<br>

## 2.3 Install the Project Files

There are multiple ways to get the project files from our GitHub repository.

Here are 2 examples:<br>

&nbsp;&nbsp;&nbsp;&nbsp;a) Please open your terminal at the place where you want to install the projekt files.<br>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Clone the repo:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`git clone https://github.com/totomate22/SEBackend`<br>

&nbsp;&nbsp;&nbsp;&nbsp;**OR**

&nbsp;&nbsp;&nbsp;&nbsp;b) Download it as a .ZIP from https://github.com/totomate22/SEBackend.<br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Afterwards extract the archive to the desired location on your PC.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Then please open a terminal at the folder you extracted the .ZIP to and go on to the next step.

If you followed the steps before, you should now have a directory with the project files.

## 2.4 Create a Python virtual environment

Inside SEBackend there should be a folder called DigiDish.<br>
Please open this folder in a terminal (or `cd` into it, if your terminal session from the steps before is still active).

**Inside** DigiDish folder:<br>
&nbsp;&nbsp;&nbsp;&nbsp;Install pipenv for simply creating a virtual environment:<br>
&nbsp;&nbsp;&nbsp;&nbsp;`pip install pipenv`

&nbsp;&nbsp;&nbsp;&nbsp;Install the project dependencies in the virtual environment with the following command:<br>
&nbsp;&nbsp;&nbsp;&nbsp;`pipenv install qrcode django psycopg2 Pillow`<br><br>


# 3. Getting started

### Important!<br>
To run the project, 
it is required to have the virtual environment with the dependencies installed ***active***<br>

Please open a terminal **inside** DigiDish folder or (`cd` into it)
and activate the virtual environment with the following command<br> `pipenv shell`<br>

### Final Steps - inside **active** Virtual Envrionment <br>

&nbsp;&nbsp;&nbsp;&nbsp;Create your django-admin login credentials:<br>
&nbsp;&nbsp;&nbsp;&nbsp;`python manage.py createsuperuser`

&nbsp;&nbsp;&nbsp;&nbsp;Migrate the database:<br>
&nbsp;&nbsp;&nbsp;&nbsp;`python manage.py migrate`

&nbsp;&nbsp;&nbsp;&nbsp;Run the server:<br>
&nbsp;&nbsp;&nbsp;&nbsp;`python manage.py runserver`

**You are now ready to go**

The server runs at port http://127.0.0.1:8000/<br>
Visit [this address](http://127.0.0.1:8000/) in your browser to get to the starting page.

To go to the admin site, use the following link:<br>http://127.0.0.1:8000/admin/.<br>
To login there, use the username and password we defined earlier.




### Links

&nbsp;&nbsp;&nbsp;&nbsp;[django](https://www.djangoproject.com/download/)<br>

**Backend vom Softwaretechnikpraktikum:**
https://github.com/20SEBastian03/PraktikumSoftwaretechnik2024_25

**Link zum GoogleDoc**
https://docs.google.com/document/u/0/d/1FzFdH04_WFbqNceWN6JbWwkEn3PPtvXhIoQiQIEPI8E/mobilebasic
