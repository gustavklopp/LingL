# LingL
Learn new languages by reading anything you choose

this was inspired by other site/projects like Lwt, lingq etc...

## How to use it:

### Use the online website:
Generously provided by PythonAnywhere:

It's limited in user capacity but I leave it like this for the moment.

Create a User or use the test user: `test` / password: `tst1tst1`

<https://gustavklopp.pythonanywhere.com>

### Use the executable (Standalone application):

#### Linux:

##### x86/64: 

<https://github.com/gustavklopp/LingL/releases>

### Use the built-in server inside Django:

It will need `python >=3.6` and `Django >= 1.11`

Set a virtualenv with python 3.6, then inside the virtual env:
`pip install -r requirement_LingL.txt`

Running the Django project:
```
python manage.py makemigrations
python manage.py migrate

python manage.py runserver
```


