from Tkinter import *

root = Tk()
nameLabel = Label(root, text="Name")
ent = Entry(root, bd=5)

def getName():
    print ent.get()
    root.destroy()

submit = Button(root, text ="Submit", command = getName)

nameLabel.pack()
ent.pack()

submit.pack(side = BOTTOM) 
root.mainloop()

print "Rest of the code goes here" 