# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 22:39:23 2016

@author: konin_de
"""

""" darten """

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

class Darters():
    def __init__(self, name, score = 501, no_throws = 0, legs = 0, sets = 0, matches = 0, average = 0):
        self.name = name
        self.score = score
        self.no_throws = no_throws
        self.legs = legs
        self.sets = sets
        self.matches = matches
        self.average = average
        
class Match():
    is_finished = False
    won_by = None
    lost_by = None
    
    def __init__(self, match_id, bo_legs, bo_sets):
        self.match_id = match_id
        self.bo_legs = bo_legs
        self.bo_sets = bo_sets

class Set():
    is_finished = False
    won_by = None
    lost_by = None
    
    def __init__(self, set_id, bo_legs):
        self.set_id = set_id
        self.bo_legs = bo_legs
    
class Leg():
    is_finished = False
    won_by = None
    lost_by = None
    throws = {}
    finish = 0
    twentysix = []
    
    def __init__(self, leg_id):
        self.leg_id = leg_id
    
    def save_throws(self, players):
        for player in players:
            self.throws[player.name] = []

def score_keeper(score, throw):
    if score - throw < 2 and score - throw != 0:
        throw = 0
    else:
        score -= throw
    return score, throw
    
def score_reset(players):
    for player in players:
        player.score = 501
        
def legs_reset(players):
    for player in players:
        player.legs = 0
        
def sets_reset(players):
    for player in players:
        player.sets = 0
        
def save_data(data, fname):
    with open(fname, 'wb') as fp:
        pickle.dump(data, fp)

def retag(tag, *args):
    '''Add the given tag as the first bindtag for every widget passed in'''
    for widget in args:
        widget.bindtags((tag,) + widget.bindtags())

def dart_match(players, bo_legs, bo_sets):
    match_id = data['match_counter'] + 1
    data['match_counter'] += 1

    Current_match = Match(match_id, bo_legs, bo_sets)

    set_id = 1
    set_id_db = str(match_id) + '.' + str(set_id)

    Current_set = Set(set_id_db, bo_legs)

    leg_id = 1
    leg_id_db = str(match_id) + '.' + str(set_id) + '.' + str(leg_id)

    Current_leg = Leg(leg_id_db)
    Current_leg.save_throws(players)

    score_reset(players)
    legs_reset(players)
    sets_reset(players)

    match_ongoing = True
    leg_counter = 0
    set_counter = 0
    
    return [match_id, data, Current_match, set_id, set_id_db, Current_set, leg_id, leg_id_db, Current_leg, leg_counter, set_counter]

    # while match_ongoing:
#         for player in players:
#
#
#
#             if player.score != 0:
#                 player.no_throws += 1
#
#             else:
#                 player.no_throws += 1
#                 Current_leg.finish = throw
#                 Current_leg.is_finished = True
#                 Current_leg.won_by = player.name
#                 Current_leg.lost_by = [loser.name for loser in players if loser != player]
#
#                 data['legs'][leg_id_db] = Current_leg
#
#                 save_data(data,fname)
#
#                 leg_counter += 1
#                 player.legs += 1
#
#                 if player.legs == bo_legs:
#
#                     Current_set.is_finished = True
#                     Current_set.won_by = player.name
#                     Current_set.lost_by = [loser.name for loser in players if loser != player]
#
#                     data['sets'][set_id_db] = Current_set
#
#                     save_data(data,fname)
#
#                     leg_counter = 0
#                     leg_id = 1
#                     set_counter += 1
#                     player.sets += 1
#
#                     if player.sets == bo_sets:
#
#                         Current_match.is_finished = True
#                         Current_match.won_by = player.name
#                         Current_match.lost_by = [loser.name for loser in players if loser != player]
#
#                         data['matches'][match_id] = Current_match
#
#                         save_data(data,fname)
#
#                         match_ongoing = False
#                         print '%s has won the game!' % player.name
#                         break
#                     else:
#                         score_reset(players)
#
#                         set_id += 1
#                         set_id_db = str(match_id) + '.' + str(set_id)
#
#                         Current_set = Set(set_id_db, bo_legs)
#
#                         leg_id_db = str(match_id) + '.' + str(set_id) + '.' + str(leg_id)
#
#                         Current_leg = Leg(leg_id_db)
#                         Current_leg.save_throws(players)
#
#                         legs_reset(players)
#                         print '%s has won the set %s!' % (player.name, set_counter)
#                 else:
#
#                     leg_id_db = str(match_id) + '.' + str(set_id) + '.' + str(leg_id)
#
#                     Current_leg = Leg(leg_id_db)
#                     Current_leg.save_throws(players)
#
#                     score_reset(players)
#                     print '%s has won the leg %s!' % (player.name, leg_counter)
#

import pickle
import os
from Tkinter import *

class MyGUI:
    
    def __init__(self):
        self.__mainWindow = Tk()
        #self.fram1 = Frame(self.__mainWindow)
        
        self.button1 = Button(self.__mainWindow, text = "Start new match", command=self.start_dart_match)
        
        self.labelText = 'User name player 1'
        self.label1 = Label(self.__mainWindow, text = self.labelText)
        self.labelText2 = 'User name player 2'
        self.label2 = Label(self.__mainWindow, text = self.labelText2)
    
        self.depositlabel1 = Label(self.__mainWindow, text = 'Player 1')
        self.depositlabel2 = Label(self.__mainWindow, text = 'Player 2')
        
        self.label_sets = Label(self.__mainWindow, text = 'Sets: ')
        self.label_legs = Label(self.__mainWindow, text = 'Legs: ')
        
        
        # self.label_text12 = StringVar()
#         self.label_text12.set("Throw!")
#         self.label12 = Label(self.__mainWindow, textvariable=self.label_text12)
#         self.label12.bind("<Button-1>", self.cycle_label_text)
#         self.label_text13 = StringVar()
#         self.label_text13.set("Wait for it!")
#         self.label13 = Label(self.__mainWindow, textvariable=self.label_text13)
#         self.label13.bind("<Button-1>", self.cycle_label_text)
        
        self.depositlabel3 = Listbox(self.__mainWindow, width = 10)
        self.depositlabel4 = Listbox(self.__mainWindow, width = 10)
    
        self.depositEntry1 = Entry(self.__mainWindow, width = 10)
        self.depositEntry1.bind('<Return>', self.depositCallBack1)
        self.depositEntry2 = Entry(self.__mainWindow, width = 10)
        self.depositEntry2.bind('<Return>', self.depositCallBack2)
        
        self.depositEntry3 = Entry(self.__mainWindow, width = 10)
        self.depositEntry3.bind('<Return>', lambda widget=self.depositEntry3: self.depositCallBack3(widget))
        self.depositEntry4 = Entry(self.__mainWindow, width = 10)
        self.depositEntry4.bind('<Return>', lambda widget=self.depositEntry4: self.depositCallBack4(widget))
    
        self.depositlabel1.grid(row = 1, column = 1, columnspan=2, sticky=W)
        self.depositlabel2.grid(row = 1, column = 3, columnspan=2, sticky=E)
        self.label1.grid(row = 2, column = 1, columnspan=2, sticky=W)
        self.label2.grid(row = 2, column = 3, columnspan=2, sticky=E)
        self.depositEntry1.grid(row = 3,column = 1)
        self.depositEntry2.grid(row = 3,column = 4)

        self.depositlabel3.grid(row = 4,column = 1)
        self.depositlabel4.grid(row = 4,column = 3)
        self.depositEntry3.grid(row = 4,column = 2, sticky=E)
        self.depositEntry4.grid(row = 4,column = 4, sticky=E)
        
        self.button1.grid(row = 5,columnspan = 4, sticky=N)

        mainloop()

    def depositCallBack1(self,event):
        self.labelText = self.depositEntry1.get()
        self.depositlabel1.config(text = self.labelText)
        
        self.player1 = Darters(self.depositEntry1.get())
        print(self.labelText)
    
    def depositCallBack2(self,event):
        self.labelText = self.depositEntry2.get()
        self.depositlabel2.config(text = self.labelText)
        
        self.player2 = Darters(self.depositEntry2.get())
        print(self.labelText)
        
    def depositCallBack3(self,event):
        throw = int(event.widget.get())
        if throw < 0 or throw > 180:
            print 'No!'
        else:
            self.player1.score, throw = score_keeper(self.player1.score, throw)
            self.labelText = str(self.player1.score) + "    " + str(throw)
            self.depositlabel3.insert(END, self.labelText)
            event.widget.delete(0, 'end')
            
            self.Current_leg.throws[self.player1.name].append(throw)
            
            if self.player1.score != 0:
                self.player1.no_throws += 1
            
            else:
                self.player1.no_throws += 1
                self.Current_leg.finish = throw
                self.Current_leg.is_finished = True
                self.Current_leg.won_by = self.player1.name
                self.Current_leg.lost_by = [loser.name for loser in self.players if loser != self.player1]
            
                self.data['legs'][self.leg_id_db] = self.Current_leg
            
                save_data(self.data,fname)
            
                self.leg_counter += 1
                self.player1.legs += 1
            
                if self.player1.legs == bo_legs:
                
                    self.Current_set.is_finished = True
                    self.Current_set.won_by = self.player1.name
                    self.Current_set.lost_by = [loser.name for loser in self.players if loser != self.player1]
                
                    self.data['sets'][self.set_id_db] = self.Current_set
                
                    save_data(self.data,fname)
                
                    self.leg_counter = 0
                    self.leg_id = 1
                    self.set_counter += 1
                    self.player1.sets += 1
                
                    if self.player1.sets == bo_sets:
                    
                        self.Current_match.is_finished = True
                        self.Current_match.won_by = self.player1.name
                        self.Current_match.lost_by = [loser.name for loser in self.players if loser != self.player1]
                    
                        self.data['matches'][self.match_id] = self.Current_match
                    
                        save_data(self.data,fname)
                    
                        match_ongoing = False
                        print '%s has won the game!' % self.player1.name
                        ## Hier moet misschien nog iets van een break!
                    else:
                        score_reset(self.players)
                        self.depositlabel3.delete(0,END)
                        self.depositlabel4.delete(0,END)
                        self.depositlabel3.insert(END, "501")
                        self.depositlabel4.insert(END, "501")
                    
                        self.set_id += 1
                        self.set_id_db = str(self.match_id) + '.' + str(self.set_id)

                        self.Current_set = Set(self.set_id_db, bo_legs)
                    
                        self.leg_id_db = str(self.match_id) + '.' + str(self.set_id) + '.' + str(self.leg_id)
            
                        self.Current_leg = Leg(self.leg_id_db)
                        self.Current_leg.save_throws(self.players)
                    
                        legs_reset(self.players)
                        print '%s has won the set %s!' % (self.player1.name, self.set_counter)
                else:
                
                    self.leg_id_db = str(self.match_id) + '.' + str(self.set_id) + '.' + str(self.leg_id)
            
                    self.Current_leg = Leg(self.leg_id_db)
                    self.Current_leg.save_throws(self.players)
                
                    score_reset(self.players)
                    self.depositlabel3.delete(0,END)
                    self.depositlabel4.delete(0,END)
                    self.depositlabel3.insert(END, "501")
                    self.depositlabel4.insert(END, "501")
                    print '%s has won the leg %s!' % (self.player1.name, self.leg_counter)
    
    def depositCallBack4(self,event):
        throw = int(event.widget.get())
        if throw < 0 or throw > 180:
            print 'No!'
        else:
            self.player2.score, throw = score_keeper(self.player2.score, throw)
            self.labelText = str(self.player2.score) + "    " + str(throw)
            self.depositlabel4.insert(END, self.labelText)
            event.widget.delete(0, 'end')
            
            self.Current_leg.throws[self.player2.name].append(throw)
            
            if self.player2.score != 0:
                self.player2.no_throws += 1
            
            else:
                self.player2.no_throws += 1
                self.Current_leg.finish = throw
                self.Current_leg.is_finished = True
                self.Current_leg.won_by = self.player2.name
                self.Current_leg.lost_by = [loser.name for loser in self.players if loser != self.player2]
            
                self.data['legs'][self.leg_id_db] = self.Current_leg
            
                save_data(self.data,fname)
            
                self.leg_counter += 1
                self.player2.legs += 1
            
                if self.player2.legs == bo_legs:
                
                    self.Current_set.is_finished = True
                    self.Current_set.won_by = self.player2.name
                    self.Current_set.lost_by = [loser.name for loser in self.players if loser != self.player2]
                
                    self.data['sets'][self.set_id_db] = self.Current_set
                
                    save_data(self.data,fname)
                
                    self.leg_counter = 0
                    self.leg_id = 1
                    self.set_counter += 1
                    self.player2.sets += 1
                
                    if self.player2.sets == bo_sets:
                    
                        self.Current_match.is_finished = True
                        self.Current_match.won_by = self.player2.name
                        self.Current_match.lost_by = [loser.name for loser in self.players if loser != self.player2]
                    
                        self.data['matches'][self.match_id] = self.Current_match
                    
                        save_data(self.data,fname)
                    
                        match_ongoing = False
                        print '%s has won the game!' % self.player2.name
                        ## Hier moet misschien nog iets van een break!
                    else:
                        score_reset(self.players)
                        self.depositlabel3.delete(0,END)
                        self.depositlabel4.delete(0,END)
                        self.depositlabel3.insert(END, "501")
                        self.depositlabel4.insert(END, "501")
                    
                        self.set_id += 1
                        self.set_id_db = str(self.match_id) + '.' + str(self.set_id)

                        self.Current_set = Set(self.set_id_db, bo_legs)
                    
                        self.leg_id_db = str(self.match_id) + '.' + str(self.set_id) + '.' + str(self.leg_id)
            
                        self.Current_leg = Leg(self.leg_id_db)
                        self.Current_leg.save_throws(self.players)
                    
                        legs_reset(self.players)
                        print '%s has won the set %s!' % (self.player2.name, self.set_counter)
                else:
                
                    self.leg_id_db = str(self.match_id) + '.' + str(self.set_id) + '.' + str(self.leg_id)
            
                    self.Current_leg = Leg(self.leg_id_db)
                    self.Current_leg.save_throws(self.players)
                
                    score_reset(self.players)
                    self.depositlabel3.delete(0,END)
                    self.depositlabel4.delete(0,END)
                    self.depositlabel3.insert(END, "501")
                    self.depositlabel4.insert(END, "501")
                    print '%s has won the leg %s!' % (self.player2.name, self.leg_counter)
    
    # def depositCallBack4(self,event):
#         throw = int(event.widget.get())
#         if throw < 0 or throw > 180:
#             print 'No!'
#         else:
#             self.player2.score, throw = score_keeper(self.player2.score, throw)
#             self.labelText = str(self.player2.score) + "    " + str(throw)
#             self.depositlabel4.insert(END, self.labelText)
#             event.widget.delete(0, 'end')
#
#             Current_leg.throws[player2.name].append(throw)
        
    def start_dart_match(self):
        self.depositlabel3.delete(0,END)
        self.depositlabel4.delete(0,END)
        self.depositlabel3.insert(END, "501")
        self.depositlabel4.insert(END, "501")
        
        self.players = [self.player1,self.player2]
        [self.match_id, self.data, self.Current_match, self.set_id, self.set_id_db, self.Current_set, self.leg_id, self.leg_id_db, self.Current_leg, self.leg_counter, self.set_counter] = dart_match([self.player1,self.player2], bo_legs, bo_sets)

if __name__ == "__main__":
    #player1 = Darters(raw_input("Player1: "))
    #player2 = Darters(raw_input("Player2: "))

    bo_legs = int(raw_input("Best of legs: "))
    bo_sets = int(raw_input("Best of sets: "))

    fname = 'database.pkl'

    if os.path.isfile(fname):
        with open(fname, 'rb') as fp:
            data = pickle.load(fp)
    else:
        data = AutoVivification()
        data['match_counter'] = 0
    
    myGUI = MyGUI()
