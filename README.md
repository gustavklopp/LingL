# LingLibre
Learn new languages by reading anything you choose.

This was inspired by other site/projects like the opensource Lwt, the closed source lingq etc...

![lingl_German_800px](https://user-images.githubusercontent.com/6438275/116420467-47bdec80-a83e-11eb-8023-4f67974223ad.png)
![lingl_homepage_600px](https://user-images.githubusercontent.com/6438275/116420494-4d1b3700-a83e-11eb-9570-ef473cba9777.png)


## How to use it:

### 1. Use the executable (Standalone application):

Available for Linux/Windows/Mac:

the executable is `Linglibre`.

<https://github.com/gustavklopp/LingL/releases>


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
