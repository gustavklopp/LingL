'''Create a simple GUI to launch the server Waitress and a button to
    open the browser. Done with tkinter '''
from waitress import serve
from LingL.wsgi import application
import webbrowser
from tkinter import Button, Tk, CENTER, PhotoImage
import threading
import os
import platform


page = '127.0.0.1:8000'

'''the Waitress server is run in the background'''
class waitress_thread(object):
    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
#         self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()   
        
    def run(self):
        serve(application, listen=page)

waitress_thr = waitress_thread()

# serve(application, listen=page)

window = Tk()
window.title("LingLibre")
window.geometry('250x100')
cwd = os.getcwd()
system = platform.system()
is_Mac = True if system != 'Windows' or system != 'Linux' else False
if is_Mac:
    lingl_image_path = os.path.join(cwd,'lib','lwt','static','lwt','img','site_icon_16x16.png')
else:
    lingl_image_path = os.path.join(cwd,'LingL','lwt','static','lwt','img','site_icon_16x16.png')
photo = PhotoImage(file = lingl_image_path)
window.iconphoto(False, photo)

def clicked():
    webbrowser.open('http://'+page)

btn = Button(window, text="Launch LingLibre \n(A tab will open in your browser)", command=clicked)
btn.place(relx=0.5, rely=0.5, anchor=CENTER)

window.mainloop()
