# LingLibre
Learn new languages by reading anything you choose.

This was inspired by other site/projects like the opensource Lwt, the closed source lingq etc...

![lingl_German_800px](https://user-images.githubusercontent.com/6438275/116420467-47bdec80-a83e-11eb-8023-4f67974223ad.png)
![lingl_homepage_600px](https://user-images.githubusercontent.com/6438275/116420494-4d1b3700-a83e-11eb-9570-ef473cba9777.png)


## 1. How to use it:

### 1.1 Use the executable (Standalone application):

Available for Linux/Windows/Max:

the executable is `Linglibre`.

<https://github.com/gustavklopp/LingL/releases>

After launching the app, you will need to create an account (this way, the app allows multi-accounts).

### 1.2. Use the built-in server inside Django:

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

After launching the app, you will need to create an account (this way, the app allows multi-accounts).
There's also a `superuser` account for Django admin use: it's : username: `lingl` / password: `lingl`.

### 1.3. (future) Use the online website:
Maybe later if people interested.

## 2. Developers:

To build `LingLibre`, use CX_Freeze with the suitable platform:

`python setup_LINUX.py build` on Linux

`python setup_WIN32.py build` on Windows

`python setup_MACOS.py build` on Mac

The build results (with the `LingLibre` executable) will be in the `build` folder.
