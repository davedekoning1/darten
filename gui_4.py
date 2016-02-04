from Tkinter import *

number_of_players = range(1,3)

players = {}


    
top = Tk()
L1 = Label(top, text="User Name player 1")
L1.pack( side = LEFT)
L1.grid()

L2 = Label(top, text="User name player 2")
L2.pack( side = RIGHT)
L2.grid()

E1 = Entry(top, bd =5)
E1.pack(side = LEFT)
E1.grid()

E2 = Entry(top, bd =5)
E2.pack(side = RIGHT)
E2.grid()

def get_input():
    players['player' + str(player_num)] = E1.get()

B1 = Button(top, text = "submit", command = get_input)
B1.pack( side = RIGHT)
B1.grid()

top.mainloop()

print players