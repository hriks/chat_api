# Chat_api (AndroZDI_Chat)
================================================================

Chat API which is able to provide, chat between individuals or groups.
Integrated with Jinja2 for a cool user interface and that would use the API to allow users
to communicate with others via one on one or group mode in real-time.

This uses python Socket.IO Library to open a connection.
Allowing a users to send and recieve messages

# How to install ?
There are two ways to install.

# You can install manually install library that are requied to run this APP


### The pythonista way

Ensure that you have an updated version of pip

```
pip --version
```
Should atleast be 1.5.4

If pip version is less than 1.5.4 upgrade it
```
pip install -U pip
```

This will install latest pip

Ensure that you are in virtualenv
if not install virtual env
```
sudo pip install virtualenv
```
This will make install all dependencies to the virtualenv
not on your root

From the module folder install the dependencies. This also installs
the module itself in a very pythonic way.

```
pip install -r requirements.txt
```
## NOTE

You also have to export SECKET_KEY and CHAT_DATABASE_URI and DB_NAME

in your environment to run this app

Postgresql must be installed to use postgresql as a DATABASE
Any RDBMS canbe used to run this app.

if not, install postgres and its server-side extensions
USE ANY DATABASE BUT MAKE SURE YOU CHANGE CHAT_DATABASE_URI

```
export SECRET_KEY='YOUR SECRET KEY'

export CHAT_DATABASE_URI='postgresql://username:password@localhost:5432'
```
```
export SECRET_KEY='YOUR SECRET KEY'
```
```
export DB_NAME="Your DB_NAME"
```

Run app by

```
python chat.py
```

## Common Isuues

```
KEY_ERROR
```
This can be as you had not export environment variables like SECRET_KEY
or DB_NAME

```
OperationalError: (psycopg2.OperationalError) FATAL:  database "/chat_api" does not exist
```

This can be due to added '/' at the end of CHAT_DATABASE_URI
Correct format for URI
```
export CHAT_DATABASE_URI='postgresql://username:password@localhost:5432'
```
To run on locally first, have to setup database
open python in terminal
```
from app import db
```
This will import models, then
```
db.create_all()
```
call create_all function.
This will create tables requied to run.
Happy coding
