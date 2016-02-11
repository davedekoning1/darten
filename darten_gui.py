# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 22:39:23 2016

@author: konin_de

New update 09-02-2016:
    Database issue is fixed, however it was found that the statistics for first 9 darts do not match yet.
    Furthermore the code can possibly be cleaned a fair bit.
    
    ** Still to be added **
    1. Possible finishes
    2. View of previous matches
    3. More stats/ custom stats
    4. Maybe add a menu for the settings of the match
    6. Nicer playername input fields
    7. Better layout of the gui
    10. Pop-up screen/save to excel/pdf with match overview
    11. Pop-ups when doing something wrong

"""

""" darten """

import pickle
import os
import numpy as np
from Tkinter import *
import ttk

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
        self.count_180 = 0
        self.count_140 = 0
        self.count_100 = 0
        self.count_60 = 0
        self.finish_130up = 0
        self.finish_130 = 0
        self.finish_80 = 0
        self.matches = matches
        self.average = average
        
class Match():
    
    def __init__(self, match_id, bo_legs, bo_sets):
        self.match_id = match_id
        self.bo_legs = bo_legs
        self.bo_sets = bo_sets
        self.is_finished = False
        self.won_by = None
        self.lost_by = None
        self.match_throws = {}
        
    def save_match_throws(self, players):
        for player in players:
            self.match_throws[player.name] = []

class Set():
    
    def __init__(self, set_id, bo_legs):
        self.set_id = set_id
        self.bo_legs = bo_legs
        self.is_finished = False
        self.won_by = None
        self.lost_by = None
        self.set_throws = {}
        
    def save_set_throws(self, players):
        for player in players:
            self.set_throws[player.name] = []

class Leg():
    def __init__(self, leg_id):
        self.leg_id = leg_id
        self.is_finished = False
        self.won_by = None
        self.lost_by = None
        self.leg_throws = {}
        self.finish = 0
        self.twentysix = []
    
    def save_leg_throws(self, players):
        for player in players:
            self.leg_throws[player.name] = []

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

def dart_match(players, bo_legs, bo_sets, data):    
    match_id = data['match_counter'] + 1
    data['match_counter'] += 1

    data['matches'][match_id] = Match(match_id, bo_legs, bo_sets)
    data['matches'][match_id].save_match_throws(players)

    set_id = 1
    set_id_db = str(match_id) + '.' + str(set_id)

    data['sets'][set_id_db] = Set(set_id_db, bo_legs)
    data['sets'][set_id_db].save_set_throws(players)

    leg_id = 1
    leg_id_db = str(match_id) + '.' + str(set_id) + '.' + str(leg_id)
    
    data['legs'][leg_id_db] = Leg(leg_id_db)
    data['legs'][leg_id_db].save_leg_throws(players)
    
    score_reset(players)
    legs_reset(players)
    sets_reset(players)

    match_ongoing = True
    leg_counter = 0
    set_counter = 0
    
    imp_throws = [163, 166, 169, 172, 173, 175, 176, 178, 179]
    
    return [match_id, data, set_id, set_id_db, leg_id, leg_id_db, leg_counter, set_counter, match_ongoing, imp_throws]

class MyGUI:
    
    def __init__(self):
        self.__mainWindow = Tk()
        # self.__mainWindow.after(1, lambda:self.__mainWindow.focus_force())
        #self.fram1 = Frame(self.__mainWindow)
        
        self.button1 = ttk.Button(self.__mainWindow, text = "Start new match",command = self.start_dart_match2, takefocus = 1)
        self.button1.bind('<Return>', self.start_dart_match)
        # self.button1.bind('<Button-1>', self.start_dart_match)
        
        self.labelText = 'User name player 1'
        self.label1 = Label(self.__mainWindow, text = self.labelText)
        self.labelText2 = 'User name player 2'
        self.label2 = Label(self.__mainWindow, text = self.labelText2)
    
        self.depositlabel1 = Label(self.__mainWindow, text = 'Player 1')
        self.depositlabel2 = Label(self.__mainWindow, text = 'Player 2')
        
        self.label_text12 = StringVar()
        self.label_text12.set("Throw!")
        self.label12 = Label(self.__mainWindow, textvariable=self.label_text12)
        self.label_text13 = StringVar()
        self.label_text13.set("Wait for it!")
        self.label13 = Label(self.__mainWindow, textvariable=self.label_text13)
        
        self.depositlabel3 = Listbox(self.__mainWindow, width = 10)
        self.depositlabel4 = Listbox(self.__mainWindow, width = 10)
    
        self.depositEntry1 = Entry(self.__mainWindow, width = 10)
        self.depositEntry1.focus_set()
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
        
        self.label12.grid(row = 4, column = 1, columnspan = 2)
        self.label13.grid(row = 4, column = 3, columnspan = 2)
        
        self.depositlabel3.grid(row = 5,column = 1)
        self.depositlabel4.grid(row = 5,column = 3)
        self.depositEntry3.grid(row = 5,column = 2, sticky=E)
        self.depositEntry4.grid(row = 5,column = 4, sticky=E)
        
        self.button1.grid(row = 4, column = 5, columnspan = 2, sticky=N)
        
        ###################
        ### Score frame ###
        ###################
        self.score_frame = Frame(self.__mainWindow)
        self.score_frame.grid(row = 1, rowspan = 3, column = 6)
        
        self.label_sets = Label(self.score_frame, text = 'Sets: ')
        self.label_legs = Label(self.score_frame, text = 'Legs: ')
        
        self.label_player1 = Label(self.score_frame, text = 'Player 1')
        self.label_player2 = Label(self.score_frame, text = 'Player 2')
        
        self.label_player1_sets = Label(self.score_frame, text = "0")
        self.label_player1_legs = Label(self.score_frame, text = "0")
        self.label_player2_sets = Label(self.score_frame, text = "0")
        self.label_player2_legs = Label(self.score_frame, text = "0")
        
        self.label_sets.grid(row = 1, column = 3)
        self.label_legs.grid(row = 1, column = 2)
        
        self.label_player1.grid(row = 2, column = 1)
        self.label_player2.grid(row = 3, column = 1)
        
        self.label_player1_sets.grid(row = 2, column = 3)
        self.label_player1_legs.grid(row = 2, column = 2)
        self.label_player2_sets.grid(row = 3, column = 3)
        self.label_player2_legs.grid(row = 3, column = 2)
        
        ###################
        ### Stats frame ###
        ###################
        self.stats_frame = Frame(self.__mainWindow)
        self.stats_frame.grid(row = 5, rowspan = 3, column = 6)
        
        self.average_frame = Frame(self.stats_frame)
        self.average_frame.grid(row = 1,column = 1)
        self.high_frame = Frame(self.stats_frame)
        self.high_frame.grid(row = 2,column = 1)
        self.finish_frame = Frame(self.stats_frame)
        self.finish_frame.grid(row = 3,column = 1)
        
        self.lp1_average = Label(self.average_frame, text = 'Player 1')
        self.lp2_average = Label(self.average_frame, text = 'Player 2')
        self.label_average_match = Label(self.average_frame, text = "Match average")
        self.label_average_first9 = Label(self.average_frame, text = "First 9 darts")
        
        self.label_average_match_p1 = Label(self.average_frame, text = "0")
        self.label_average_first9_p1 = Label(self.average_frame, text = "0")
        self.label_average_match_p2 = Label(self.average_frame, text = "0")
        self.label_average_first9_p2 = Label(self.average_frame, text = "0")

        self.lp1_high = Label(self.high_frame, text = 'Player 1')
        self.lp2_high = Label(self.high_frame, text = 'Player 2')
        self.label_throw60 = Label(self.high_frame, text = "60-100")
        self.label_throw100 = Label(self.high_frame, text = "100-140")
        self.label_throw140 = Label(self.high_frame, text = "140-180")
        self.label_throw180 = Label(self.high_frame, text = "180")
        
        self.label_throw60_p1 = Label(self.high_frame, text = "0")
        self.label_throw100_p1 = Label(self.high_frame, text = "0")
        self.label_throw140_p1 = Label(self.high_frame, text = "0")
        self.label_throw180_p1 = Label(self.high_frame, text = "0")
        self.label_throw60_p2 = Label(self.high_frame, text = "0")
        self.label_throw100_p2 = Label(self.high_frame, text = "0")
        self.label_throw140_p2 = Label(self.high_frame, text = "0")
        self.label_throw180_p2 = Label(self.high_frame, text = "0")
        
        self.lp1_finish = Label(self.finish_frame, text = 'Player 1')
        self.lp2_finish = Label(self.finish_frame, text = 'Player 2')
        self.label_finish80 = Label(self.finish_frame, text = "0-80")
        self.label_finish130 = Label(self.finish_frame, text = "80-130")
        self.label_finish130up = Label(self.finish_frame, text = "130+")
        
        self.label_finish80_p1 = Label(self.finish_frame, text = "0")
        self.label_finish130_p1 = Label(self.finish_frame, text = "0")
        self.label_finish130up_p1 = Label(self.finish_frame, text = "0")
        self.label_finish80_p2 = Label(self.finish_frame, text = "0")
        self.label_finish130_p2 = Label(self.finish_frame, text = "0")
        self.label_finish130up_p2 = Label(self.finish_frame, text = "0")
        
        self.lp1_average.grid(row = 2, column = 1)
        self.lp2_average.grid(row = 3, column = 1)
        self.label_average_match.grid(row = 1, column = 3)
        self.label_average_first9.grid(row = 1, column = 2)
        
        self.label_average_match_p1.grid(row = 2, column = 3)
        self.label_average_first9_p1.grid(row = 2, column = 2)
        self.label_average_match_p2.grid(row = 3, column = 3)
        self.label_average_first9_p2.grid(row = 3, column = 2)

        self.lp1_high.grid(row = 2, column = 1)
        self.lp2_high.grid(row = 3, column = 1)
        self.label_throw60.grid(row = 1, column = 2)
        self.label_throw100.grid(row = 1, column = 3)
        self.label_throw140.grid(row = 1, column = 4)
        self.label_throw180.grid(row = 1, column = 5)
        
        self.label_throw60_p1.grid(row = 2, column = 2)
        self.label_throw100_p1.grid(row = 2, column = 3)
        self.label_throw140_p1.grid(row = 2, column = 4)
        self.label_throw180_p1.grid(row = 2, column = 5)
        self.label_throw60_p2.grid(row = 3, column = 2)
        self.label_throw100_p2.grid(row = 3, column = 3)
        self.label_throw140_p2.grid(row = 3, column = 4)
        self.label_throw180_p2.grid(row = 3, column = 5)
        
        self.lp1_finish.grid(row = 2, column = 1)
        self.lp2_finish.grid(row = 3, column = 1)
        self.label_finish80.grid(row = 1, column = 2)
        self.label_finish130.grid(row = 1, column = 3)
        self.label_finish130up.grid(row = 1, column = 4)
        
        self.label_finish80_p1.grid(row = 2, column = 2)
        self.label_finish130_p1.grid(row = 2, column = 3)
        self.label_finish130up_p1.grid(row = 2, column = 4)
        self.label_finish80_p2.grid(row = 3, column = 2)
        self.label_finish130_p2.grid(row = 3, column = 3)
        self.label_finish130up_p2.grid(row = 3, column = 4)
        
        mainloop()

    def change_number_label(self, text, label):
        label.config(text = str(text))
        
    def check_throw_stats_p1(self, throw, player):
        if throw == 180:
            player.count_180 += 1
            self.label_throw180_p1.config(text = str(player.count_180))
        elif throw >= 140:
            player.count_140 += 1
            self.label_throw140_p1.config(text = str(player.count_140))
        elif throw >= 100:
            player.count_100 += 1
            self.label_throw100_p1.config(text = str(player.count_100))
        elif throw >= 60:
            player.count_60 += 1
            self.label_throw60_p1.config(text = str(player.count_60))
            
    def check_finish_stats_p1(self, throw, player):
        if throw >= 130:
            player.finish_130up += 1
            self.label_finish130up_p1.config(text = str(player.finish_130up))
        elif throw >= 80:
            player.finish_130 += 1
            self.label_finish130_p1.config(text = str(player.finish_130))
        else:
            player.finish_80 += 1
            self.label_finish80_p1.config(text = str(player.finish_80))
    
    def check_throw_stats_p2(self, throw, player):
        if throw == 180:
            player.count_180 += 1
            self.label_throw180_p2.config(text = str(player.count_180))
        elif throw >= 140:
            player.count_140 += 1
            self.label_throw140_p2.config(text = str(player.count_140))
        elif throw >= 100:
            player.count_100 += 1
            self.label_throw100_p2.config(text = str(player.count_100))
        elif throw >= 60:
            player.count_60 += 1
            self.label_throw60_p2.config(text = str(player.count_60))
            
    def check_finish_stats_p2(self, throw, player):
        if throw >= 130:
            player.finish_130up += 1
            self.label_finish130up_p2.config(text = str(player.finish_130up))
        elif throw >= 80:
            player.finish_130 += 1
            self.label_finish130_p2.config(text = str(player.finish_130))
        else:
            player.finish_80 += 1
            self.label_finish80_p2.config(text = str(player.finish_80))
    def calculate_averages(self, Leg, Set, Match, player):
        Leg_average = np.mean(Leg.leg_throws[player.name])
        Set_average = np.mean(Set.set_throws[player.name])
        Match_average = np.mean(Match.match_throws[player.name])
        
        if player.no_throws == 3:
            First_9 = np.mean(Leg.leg_throws[player.name])
        
    def update_averages_p1(self, data, Leg, Set, Match, player):
        Leg_average = np.mean(Leg.leg_throws[player.name])
        Set_average = np.mean(Set.set_throws[player.name])
        Match_average = np.mean(Match.match_throws[player.name])
        if player.no_throws == 3:
            First_9 = []
            for key in data['legs'].keys():
                match_counter = data['match_counter']
                len_match_count = len(str(match_counter))
                if key[:len_match_count] == str(match_counter):
                    First_9.append(data['legs'][key].leg_throws[player.name][:3])
            First_9_mean = np.mean(First_9)
            self.label_average_first9_p1.config(text = '{:.2f}'.format(First_9_mean))
        
        self.label_average_match_p1.config(text = '{:.2f}'.format(Match_average))
    
    def update_averages_p2(self, data, Leg, Set, Match, player):
        Leg_average = np.mean(Leg.leg_throws[player.name])
        Set_average = np.mean(Set.set_throws[player.name])
        Match_average = np.mean(Match.match_throws[player.name])
        
        if player.no_throws == 3:
            First_9 = []
            for key in data['legs'].keys():
                match_counter = data['match_counter']
                len_match_count = len(str(match_counter))
                if key[:len_match_count] == str(match_counter):
                    First_9.append(data['legs'][key].leg_throws[player.name][:3])
            First_9_mean = np.mean(First_9)
            self.label_average_first9_p2.config(text = '{:.2f}'.format(First_9_mean))
        
        self.label_average_match_p2.config(text = '{:.2f}'.format(Match_average))

    def cycle_label_text(self):
        self.LABEL_TEXT = ["Throw!", "Wait for it!"]
        self.label_index -= 1
        if self.label_index < -1:
            self.label_index = 0
        self.label_text12.set(self.LABEL_TEXT[self.label_index])
        self.label_text13.set(self.LABEL_TEXT[self.label_index+1])

    def depositCallBack1(self,event):
        self.labelText = self.depositEntry1.get()
        self.depositlabel1.config(text = self.labelText)
        self.label_player1.config(text = self.labelText)
        
    	self.lp1_average.config(text = self.labelText)
    	self.lp1_high.config(text = self.labelText)
    	self.lp1_finish.config(text = self.labelText)
        
        self.player1 = Darters(self.depositEntry1.get())
        print(self.labelText)
        
        self.depositEntry2.focus_set()
    
    def depositCallBack2(self,event):
        self.labelText = self.depositEntry2.get()
        self.depositlabel2.config(text = self.labelText)
        self.label_player2.config(text = self.labelText)

    	self.lp2_average.config(text = self.labelText)
    	self.lp2_high.config(text = self.labelText)
    	self.lp2_finish.config(text = self.labelText)
        
        self.player2 = Darters(self.depositEntry2.get())
        print(self.labelText)
        
        self.button1.focus_set()
        
    def depositCallBack3(self,event):
        if self.match_ongoing == False:
            print "Start a new match"
            return
        
        if self.player1.no_throws > self.player2.no_throws:
            print "It's not your turn!"
            return
        
        throw = int(event.widget.get())
        if throw < 0 or throw > 180 or throw in self.imp_throws:
            print 'No!'
        else:
            self.cycle_label_text()
            self.player1.score, throw = score_keeper(self.player1.score, throw)
            self.labelText = str(self.player1.score) + "    " + str(throw)
            self.depositlabel3.insert(END, self.labelText)
            event.widget.delete(0, 'end')
            
            self.data['legs'][self.leg_id_db].leg_throws[self.player1.name].append(throw)
            self.data['sets'][self.set_id_db].set_throws[self.player1.name].append(throw)
            self.data['matches'][self.match_id].match_throws[self.player1.name].append(throw)
            
            if self.player1.score != 0:
                self.player1.no_throws += 1
                self.calculate_averages(self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player1)
                self.depositEntry4.focus_set()
                self.check_throw_stats_p1(throw, self.player1)
                self.update_averages_p1(self.data, self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player1)
            
            else:
                self.check_finish_stats_p1(throw, self.player1)
                self.check_throw_stats_p1(throw, self.player1)
                self.player2.no_throws = 0
                self.player1.no_throws = 0
                self.calculate_averages(self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player1)
                self.update_averages_p1(self.data, self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player1)
                self.data['legs'][self.leg_id_db].finish = throw
                self.data['legs'][self.leg_id_db].is_finished = True
                self.data['legs'][self.leg_id_db].won_by = self.player1.name
                self.data['legs'][self.leg_id_db].lost_by = [loser.name for loser in self.players if loser != self.player1]
            
                save_data(self.data,fname)
            
                self.leg_counter += 1
                self.player1.legs += 1
            
                if self.player1.legs == bo_legs:
                
                    self.data['sets'][self.set_id_db].is_finished = True
                    self.data['sets'][self.set_id_db].won_by = self.player1.name
                    self.data['sets'][self.set_id_db].lost_by = [loser.name for loser in self.players if loser != self.player1]
                
                    save_data(self.data,fname)
                
                    self.leg_counter = 0
                    self.leg_id = 1
                    self.set_counter += 1
                    self.player1.sets += 1
                    
                    self.change_number_label(self.player1.sets, self.label_player1_sets)
                
                    if self.player1.sets == bo_sets:
                    
                        self.data['matches'][self.match_id].is_finished = True
                        self.data['matches'][self.match_id].won_by = self.player1.name
                        self.data['matches'][self.match_id].lost_by = [loser.name for loser in self.players if loser != self.player1]
                    
                        save_data(self.data,fname)
                    
                        self.match_ongoing = False
                        print '%s has won the game!' % self.player1.name
                        
                        self.button1.focus_set()
                        ## Hier moet misschien nog iets van een break!
                    else:
                        score_reset(self.players)
                        self.depositlabel3.delete(0,END)
                        self.depositlabel4.delete(0,END)
                        self.depositlabel3.insert(END, "501")
                        self.depositlabel4.insert(END, "501")
                    
                        self.set_id += 1
                        self.set_id_db = str(self.match_id) + '.' + str(self.set_id)

                        self.data['sets'][self.set_id_db] = Set(self.set_id_db, bo_legs)
                        self.data['sets'][self.set_id_db].save_set_throws(self.players)
                    
                        self.leg_id_db = str(self.match_id) + '.' + str(self.set_id) + '.' + str(self.leg_id)
            
                        self.data['legs'][self.leg_id_db] = Leg(self.leg_id_db)
                        self.data['legs'][self.leg_id_db].save_leg_throws(self.players)
                    
                        legs_reset(self.players)
                        
                        self.depositEntry4.focus_set()
                        
                        self.change_number_label(self.player1.legs, self.label_player1_legs)
                        self.change_number_label(self.player2.legs, self.label_player2_legs)
                        
                        print '%s has won the set %s!' % (self.player1.name, self.set_counter)
                else:
                    
                    self.leg_id += 1
                    self.leg_id_db = str(self.match_id) + '.' + str(self.set_id) + '.' + str(self.leg_id)
            
                    self.data['legs'][self.leg_id_db] = Leg(self.leg_id_db)
                    self.data['legs'][self.leg_id_db].save_leg_throws(self.players)
                
                    score_reset(self.players)
                    self.change_number_label(self.player1.legs, self.label_player1_legs)

                    self.depositEntry4.focus_set()
                    
                    self.depositlabel3.delete(0,END)
                    self.depositlabel4.delete(0,END)
                    self.depositlabel3.insert(END, "501")
                    self.depositlabel4.insert(END, "501")
                    print '%s has won the leg %s!' % (self.player1.name, self.leg_counter)
    
    def depositCallBack4(self,event):
        if self.match_ongoing == False:
            print "Start a new match"
            return
        
        if self.player2.no_throws > self.player1.no_throws:
            print "It's not your turn!"
            return
        
        throw = int(event.widget.get())
        if throw < 0 or throw > 180 or throw in self.imp_throws:
            print 'No!'
        else:
            self.cycle_label_text()
            self.player2.score, throw = score_keeper(self.player2.score, throw)
            self.labelText = str(self.player2.score) + "    " + str(throw)
            self.depositlabel4.insert(END, self.labelText)
            event.widget.delete(0, 'end')
            
            self.data['legs'][self.leg_id_db].leg_throws[self.player2.name].append(throw)
            self.data['sets'][self.set_id_db].set_throws[self.player2.name].append(throw)
            self.data['matches'][self.match_id].match_throws[self.player2.name].append(throw)
            
            if self.player2.score != 0:
                self.player2.no_throws += 1
                self.depositEntry3.focus_set()
                self.check_throw_stats_p2(throw, self.player2)
                self.calculate_averages(self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player2)
                self.update_averages_p2(self.data, self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player2)
            
            else:
                self.check_finish_stats_p2(throw, self.player2)
                self.check_throw_stats_p2(throw, self.player2)
                self.calculate_averages(self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player2)
                self.update_averages_p2(self.data, self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player2)
                self.player2.no_throws = 0
                self.player1.no_throws = 0
                self.data['legs'][self.leg_id_db].finish = throw
                self.data['legs'][self.leg_id_db].is_finished = True
                self.data['legs'][self.leg_id_db].won_by = self.player2.name
                self.data['legs'][self.leg_id_db].lost_by = [loser.name for loser in self.players if loser != self.player2]
            
                save_data(self.data,fname)

                self.leg_counter += 1
                self.player2.legs += 1
            
                if self.player2.legs == bo_legs:
                
                    self.data['sets'][self.set_id_db].is_finished = True
                    self.data['sets'][self.set_id_db].won_by = self.player2.name
                    self.data['sets'][self.set_id_db].lost_by = [loser.name for loser in self.players if loser != self.player2]
                    
                    save_data(self.data,fname)
                
                    self.leg_counter = 0
                    self.leg_id = 1
                    self.set_counter += 1
                    self.player2.sets += 1
                    
                    self.change_number_label(self.player2.sets, self.label_player2_sets)
                
                    if self.player2.sets == bo_sets:
                    
                        self.data['matches'][self.match_id].is_finished = True
                        self.data['matches'][self.match_id].won_by = self.player2.name
                        self.data['matches'][self.match_id].lost_by = [loser.name for loser in self.players if loser != self.player2]

                        save_data(self.data,fname)
                    
                        self.match_ongoing = False
                        print '%s has won the game!' % self.player2.name
                        
                        self.button1.focus_set()
                        ## Hier moet misschien nog iets van een break!
                    else:
                        score_reset(self.players)
                        self.depositlabel3.delete(0,END)
                        self.depositlabel4.delete(0,END)
                        self.depositlabel3.insert(END, "501")
                        self.depositlabel4.insert(END, "501")
                    
                        self.set_id += 1
                        self.set_id_db = str(self.match_id) + '.' + str(self.set_id)

                        self.data['sets'][self.set_id_db] = Set(self.set_id_db, bo_legs)
                        self.data['sets'][self.set_id_db].save_set_throws(self.players)
                    
                        self.leg_id_db = str(self.match_id) + '.' + str(self.set_id) + '.' + str(self.leg_id)
            
                        self.data['legs'][self.leg_id_db] = Leg(self.leg_id_db)
                        self.data['legs'][self.leg_id_db].save_leg_throws(self.players)
                    
                        legs_reset(self.players)

                        self.depositEntry3.focus_set()
                        
                        self.change_number_label(self.player2.legs, self.label_player2_legs)
                        self.change_number_label(self.player1.legs, self.label_player1_legs)
                        
                        print '%s has won the set %s!' % (self.player2.name, self.set_counter)
                else:
                    
                    self.leg_id += 1
                    self.leg_id_db = str(self.match_id) + '.' + str(self.set_id) + '.' + str(self.leg_id)
            
                    self.data['legs'][self.leg_id_db] = Leg(self.leg_id_db)
                    self.data['legs'][self.leg_id_db].save_leg_throws(self.players)
                
                    score_reset(self.players)
                    self.change_number_label(self.player2.legs, self.label_player2_legs)

                    self.depositEntry3.focus_set()
                    
                    self.depositlabel3.delete(0,END)
                    self.depositlabel4.delete(0,END)
                    self.depositlabel3.insert(END, "501")
                    self.depositlabel4.insert(END, "501")
                    print '%s has won the leg %s!' % (self.player2.name, self.leg_counter)
    
        
    def start_dart_match(self, event):
        self.depositlabel3.delete(0,END)
        self.depositlabel4.delete(0,END)
        self.depositlabel3.insert(END, "501")
        self.depositlabel4.insert(END, "501")
        
        self.depositEntry3.delete(0,END)
        self.depositEntry4.delete(0,END)
        self.depositEntry3.focus_set()
        
        self.label_index = 0
        self.label_text12.set("Throw!")
        self.label_text13.set("Wait for it!")
        
        self.players = [self.player1,self.player2]
        [self.match_id, self.data, self.set_id, self.set_id_db, self.leg_id, self.leg_id_db, self.leg_counter, self.set_counter, self.match_ongoing, self.imp_throws] = dart_match(self.players, bo_legs, bo_sets, data_load)
        for player in self.players:
            player.__init__(name = player.name, matches = player.matches)
        
        self.labels_changing = [
        	[self.label_player1_sets, self.player1.legs],
        	[self.label_player1_legs, self.player1.sets],
        	[self.label_player2_sets, self.player2.legs],
        	[self.label_player2_legs, self.player2.sets],
        	[self.lp1_average, self.player1.name],
        	[self.lp1_high, self.player1.name],
        	[self.lp1_finish, self.player1.name],
        	[self.lp2_average, self.player2.name],
        	[self.lp2_high, self.player2.name],
        	[self.lp2_finish, self.player2.name],
        	[self.label_throw60_p1, self.player1.count_60],
        	[self.label_throw100_p1, self.player1.count_100],
        	[self.label_throw140_p1, self.player1.count_140],
        	[self.label_throw180_p1, self.player1.count_180],
        	[self.label_throw60_p2, self.player2.count_60],
        	[self.label_throw100_p2, self.player2.count_100],
        	[self.label_throw140_p2, self.player2.count_140],
        	[self.label_throw180_p2, self.player2.count_180],
        	[self.label_finish80_p1, self.player1.finish_80],
        	[self.label_finish130_p1, self.player1.finish_130],
        	[self.label_finish130up_p1, self.player1.finish_130up],
        	[self.label_finish80_p2, self.player2.finish_80],
        	[self.label_finish130_p2, self.player2.finish_130],
        	[self.label_finish130up_p2, self.player2.finish_130up],
        	[self.label_average_match_p1, "0"],
        	[self.label_average_first9_p1, "0"],
        	[self.label_average_match_p2, "0"],
        	[self.label_average_first9_p2,  "0"]
        ]
        
        for item in self.labels_changing:
            self.change_number_label(item[1], item[0])
        
        # self.change_number_label(self.player1.legs, self.label_player1_legs)
#         self.change_number_label(self.player1.sets, self.label_player1_sets)
#         self.change_number_label(self.player2.legs, self.label_player2_legs)
#         self.change_number_label(self.player2.sets, self.label_player2_sets)

    def start_dart_match2(self):
        self.depositlabel3.delete(0,END)
        self.depositlabel4.delete(0,END)
        self.depositlabel3.insert(END, "501")
        self.depositlabel4.insert(END, "501")
        
        self.depositEntry3.delete(0,END)
        self.depositEntry4.delete(0,END)
        self.depositEntry3.focus_set()
        
        self.label_index = 0
        self.label_text12.set("Throw!")
        self.label_text13.set("Wait for it!")
        
        self.players = [self.player1,self.player2]
        [self.match_id, self.data, self.set_id, self.set_id_db, self.leg_id, self.leg_id_db, self.leg_counter, self.set_counter, self.match_ongoing, self.imp_throws] = dart_match(self.players, bo_legs, bo_sets, data_load)
        for player in self.players:
            player.__init__(name = player.name, matches = player.matches)
        
        self.labels_changing = [
        	[self.label_player1_sets, self.player1.legs],
        	[self.label_player1_legs, self.player1.sets],
        	[self.label_player2_sets, self.player2.legs],
        	[self.label_player2_legs, self.player2.sets],
        	[self.lp1_average, self.player1.name],
        	[self.lp1_high, self.player1.name],
        	[self.lp1_finish, self.player1.name],
        	[self.lp2_average, self.player2.name],
        	[self.lp2_high, self.player2.name],
        	[self.lp2_finish, self.player2.name],
        	[self.label_throw60_p1, self.player1.count_60],
        	[self.label_throw100_p1, self.player1.count_100],
        	[self.label_throw140_p1, self.player1.count_140],
        	[self.label_throw180_p1, self.player1.count_180],
        	[self.label_throw60_p2, self.player2.count_60],
        	[self.label_throw100_p2, self.player2.count_100],
        	[self.label_throw140_p2, self.player2.count_140],
        	[self.label_throw180_p2, self.player2.count_180],
        	[self.label_finish80_p1, self.player1.finish_80],
        	[self.label_finish130_p1, self.player1.finish_130],
        	[self.label_finish130up_p1, self.player1.finish_130up],
        	[self.label_finish80_p2, self.player2.finish_80],
        	[self.label_finish130_p2, self.player2.finish_130],
        	[self.label_finish130up_p2, self.player2.finish_130up],
        	[self.label_average_match_p1, "0"],
        	[self.label_average_first9_p1, "0"],
        	[self.label_average_match_p2, "0"],
        	[self.label_average_first9_p2,  "0"]
        ]
        
        for item in self.labels_changing:
            self.change_number_label(item[1], item[0])
        
        # self.change_number_label(self.player1.legs, self.label_player1_legs)
#         self.change_number_label(self.player1.sets, self.label_player1_sets)
#         self.change_number_label(self.player2.legs, self.label_player2_legs)
#         self.change_number_label(self.player2.sets, self.label_player2_sets)

if __name__ == "__main__":

    bo_legs = int(raw_input("Best of legs: "))
    bo_sets = int(raw_input("Best of sets: "))

    fname = 'database.pkl'

    if os.path.isfile(fname):
        with open(fname, 'rb') as fp:
            data_load = pickle.load(fp)
    else:
        data_load = AutoVivification()
        data_load['match_counter'] = 0
    
    myGUI = MyGUI()
