from Tkinter import *

number_of_players = range(1,3)

players = {}

for player_num in number_of_players:
    
    top = Tk()
    L1 = Label(top, text="User Name player " + str(player_num))
    L1.pack( side = LEFT)
    L1.grid()
    E1 = Entry(top, bd =5)

    E1.pack(side = RIGHT)
    E1.grid()

    def get_input():
        players['player' + str(player_num)] = E1.get()
        top.destroy()

    B1 = Button(top, text = "submit", command = get_input)
    B1.pack( side = RIGHT)
    B1.grid()

    top.mainloop()
    
print players