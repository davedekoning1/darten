from Tkinter import *

number_of_players = range(1,3)

players = {}
    
root = Tk()
L1 = Label(root, text="User Name player 1")
L1.place(x = 20, y = 20)

L2 = Label(root, text="User name player 2")
L2.place(x = 250, y = 20)

E1 = Entry(root, bd =5)
E1.place(x = 20, y = 50)

E2 = Entry(root, bd =5)
E2.place(x = 250, y = 50)

L3 = Label(root, text="Player 1: %s" % E1.get())
L3.place(x = 20, y = 100)

def Button1():
	listbox.insert(END, "button1 pressed")

button1 = Button(root, text="button1", command = Button1)

scrollbar = Scrollbar(root, orient=VERTICAL)
listbox = Listbox(root, yscrollcommand=scrollbar.set)
scrollbar.configure(command=listbox.yview)

root.mainloop()
