from tkinter import *
import keyboard
import pyautogui
import ftplib
import datetime
import pyperclip
import time
import os
from time import gmtime, strftime

#FTP Details for your website
filepath = "https://your.site.com/screenshots"
localpath = "C:\snips\\"
host = "site.com"
user = "user"
passw = "password"
#hotkey = 'ctrl+shift+q'

if not os.path.exists(localpath):
    os.makedirs(localpath)



class Application():
    
    def __init__(self, master):
        self.master = master
        self.rect = None
        self.x = self.y = 0
        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None
        keyboard.add_hotkey('ctrl+shift', self.createScreenCanvas)
        root.bind("<Control-Shift-KeyPress>", self.capture_keyboard_shortcut)
        # root.configure(background = 'red')
        # root.attributes("-transparentcolor","red")

        #root.withdraw()
        root.attributes("-transparent", "blue")
        root.geometry('300x80+200+200')  # set new geometry
        root.title('Snipping Tool Rewritten')
        self.menu_frame = Frame(master, bg="blue")
        self.menu_frame.pack(fill=BOTH, expand=YES)

        self.buttonBar = Frame(self.menu_frame,bg="")
        self.buttonBar.pack(fill=BOTH,expand=YES)

        self.snipButton = Button(self.buttonBar, width=42, height=5, command=self.createScreenCanvas, background="white", text="Click to take Screenshot!", fg="black")
        self.snipButton.pack(expand=YES)
        self.snipButton.place(x=0, y=0)


        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "blue")
        self.picture_frame = Frame(self.master_screen, background = "blue")
        self.picture_frame.pack(fill=BOTH, expand=YES)

    #if pyautogui.hotkey('ctrl', 'shift'):    
    
    def capture_keyboard_shortcut(self, event):
        self.createScreenCanvas()

    def takeBoundedScreenShot(self, x1, y1, x2, y2):
         im = pyautogui.screenshot(region=(x1, y1, x2, y2))
         x = datetime.datetime.now()
         fileName = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
         im.save(localpath + fileName + ".png")
         uploadName = (localpath + fileName + ".png")
         session = ftplib.FTP(host,user,passw)
         file = open(uploadName,'rb')                  # file to send
         session.storbinary('STOR ' + fileName + '.png', file)     # send the file
         file.close()                                    # close file and FTP
         session.quit()
         pyperclip.copy(filepath + fileName + '.png')
        

    def createScreenCanvas(self):
        self.master_screen.deiconify()
        root.withdraw()

        self.screenCanvas = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.screenCanvas.pack(fill=BOTH, expand=YES)

        self.screenCanvas.bind("<ButtonPress-1>", self.on_button_press)
        self.screenCanvas.bind("<B1-Motion>", self.on_move_press)
        self.screenCanvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):
        self.recPosition()

        if self.start_x <= self.curX and self.start_y <= self.curY:
            print("right down")
            self.takeBoundedScreenShot(self.start_x, self.start_y, self.curX - self.start_x, self.curY - self.start_y)

        elif self.start_x >= self.curX and self.start_y <= self.curY:
            print("left down")
            self.takeBoundedScreenShot(self.curX, self.start_y, self.start_x - self.curX, self.curY - self.start_y)

        elif self.start_x <= self.curX and self.start_y >= self.curY:
            print("right up")
            self.takeBoundedScreenShot(self.start_x, self.curY, self.curX - self.start_x, self.start_y - self.curY)

        elif self.start_x >= self.curX and self.start_y >= self.curY:
            print("left up")
            self.takeBoundedScreenShot(self.curX, self.curY, self.start_x - self.curX, self.start_y - self.curY)

        self.exitScreenshotMode()
        return event

    def exitScreenshotMode(self):
        print("Screenshot mode exited")
        self.screenCanvas.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def exit_application(self):
        print("Application exit")
        root.quit()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.screenCanvas.canvasx(event.x)
        self.start_y = self.screenCanvas.canvasy(event.y)

        self.rect = self.screenCanvas.create_rectangle(self.x, self.y, 1, 1, outline='red', width=0, fill="blue")

    def on_move_press(self, event):
        self.curX, self.curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.screenCanvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

    def recPosition(self):
        print(self.start_x)
        print(self.start_y)
        print(self.curX)
        print(self.curY)


        


if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()
