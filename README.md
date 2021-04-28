# LingLibre
Learn new languages by reading anything you choose.

This was inspired by other site/projects like the opensource Lwt, the closed source lingq etc...

![lingl_German](https://user-images.githubusercontent.com/6438275/116419745-a6369b00-a83d-11eb-9a88-2e6b3f23fb3f.png)
![lingl_homepage](https://user-images.githubusercontent.com/6438275/116419775-ac2c7c00-a83d-11eb-8330-e5afebda7a30.png)
![lingl_texts](https://user-images.githubusercontent.com/6438275/116419787-af276c80-a83d-11eb-8bd8-32688b606225.png)


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
