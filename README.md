# chat_api (AndroZDI_Chat)
=======================================================================================================================

Chat API which is able to provide capabilities to chat between individuals or groups.
Integrated with Jinja2 for a cool user interface and that would use the API to allow users
to communicate with others via one on one or group mode in real-time.

This uses python Socket.IO Library to open a connection.
Allowing a users to send and recieve messages

# How to install ?
There are two ways to install.

# You can install manually intall library that are requied to run this APP


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

Postgresql must be installed.

if not, install postgres and its server-side extensions

Run app by
 
```
python chat.py
```
### 
