from waitress import serve

from LingL.wsgi import application

import webbrowser

if __name__ == '__main__':
    page = '127.0.0.1:8000'
    webbrowser.open('http://'+page)
    serve(application, listen=page)
