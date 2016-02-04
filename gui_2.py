from Tkinter import*

def valueGET(val1, val2):
    print val1 + "  " + val2

class ContentUI():
    def showLogin(self, frame):

        self.contentUI = ContentUI()    

        L1 = Label(frame, text="Name")
        L1.pack( side = LEFT)
        L1.grid()

        E1 = Entry(frame, bd =5)
        E1.pack(side = RIGHT)
        E1.grid()

        L2 = Label(frame, text="Secret")
        L2.pack( side = LEFT)
        L2.grid()       

        E2 = Entry(frame, bd =5, show="*")
        E2.pack(side = RIGHT)
        E2.grid()

        submit = Button(frame, text="Enter", width=15, command=lambda: valueGET(E1.get(), E2.get()))
        submit.grid()

class UIDisplay():
    def play(self):
        root = Tk()

        root.title(title)
        root.geometry(dimension)

        app = Frame(root)
        
        contentUI = ContentUI()
        contentUI.showLogin(app)

        app.grid()

        root.mainloop()

adkooPlay = UIDisplay()
adkooPlay.play()