# LingLibre
Learn new languages by reading anything you choose.

This was inspired by other site/projects like the opensource Lwt, the closed source lingq etc...

## How to use it:

### 1. Use the executable (Standalone application):

#### 1.2 Linux/Windows:
the executable `Linglibre` is in the folder `LingL/`.

<https://github.com/gustavklopp/LingL/releases>

#### 1.2 (future) Mac:
Maybe later if people interested.

### 2. Use the built-in server inside Django:

It will need `python >=3.8` and `Django >= 3.2`

Set a virtualenv with python 3.8, then inside the virtual env:
`pip install -r requirements.txt`

Running the Django project:

move inside the LingL folder (where `manage.py` is) and:
	
```
python manage.py migrate
python manage.py runserver
```
then open your browser to <http://127.0.0.1:8000>

### 3. (future) Use the online website:
Maybe later if people interested.
