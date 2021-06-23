#!/usr/bin/env python
'''Create a simple GUI to launch the server Waitress and a button to
    open the browser. Done with tkinter '''
from waitress import serve
from LingL.wsgi import application
import webbrowser
import threading
import os
import platform
import wx



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

# window = Tk()
app = wx.App()
#window.title("LingLibre")
frm = wx.Frame(None, title='LingLibre', style=wx.DEFAULT_FRAME_STYLE, size=(250, 100))
# window.title(thispath)
# window.geometry('250x100')
cwd = os.getcwd()
system = platform.system().lower()
if system == 'windows' or system == 'linux':
    loc = wx.IconLocation('LingL_app.ico')
    loc = wx.IconLocation('LingL_app.ico')
    frm.SetIcon(wx.Icon(loc))

else: # MacOS: BUG... not working
    loc = wx.IconLocation('LingL_app.icns')
#     loc = wx.IconLocation('LingL_app.ico')
#     frm.SetIcon(wx.Icon(loc))
# photo = PhotoImage(file = lingl_image_path)
# window.iconphoto(False, photo)

def clicked(event):
    webbrowser.open('http://'+page)

main_sizer = wx.BoxSizer(wx.VERTICAL)
# btn = Button(window, text="Launch LingLibre \n(A tab will open in your browser)", command=clicked)
btn = wx.Button(frm, label="Launch LingLibre \n(A tab will open in your browser)")
btn.Bind(wx.EVT_BUTTON, clicked)
main_sizer.AddStretchSpacer()
main_sizer.Add(btn, 0, wx.CENTER)
main_sizer.AddStretchSpacer()
frm.SetSizer(main_sizer)
# btn.place(relx=0.5, rely=0.5, anchor=CENTER)

frm.Show()
# window.mainloop()
app.MainLoop()
