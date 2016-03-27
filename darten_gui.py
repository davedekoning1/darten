# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 22:39:23 2016

@author: konin_de

New update 09-02-2016:
    Database issue is fixed, however it was found that the statistics for first 9 darts do not match yet.
    Furthermore the code can possibly be cleaned a fair bit.
    
    ** Still to be added **
    1. combine the 2 screens in one gui!
    2. combine the callbacks for the two players!
    3. continue match button
    4. Maybe add a menu for the settings of the match
    5. Better setup of match, use enters/but perhaps also just check when a new match is started
    6. Nicer playername input fields
    7. Better layout of the gui
    10. Pop-up screen/save to excel/pdf with match overview
    11. Pop-ups when doing something wrong

"""
def check_bull(value, mult):
    if value == 50:
        val = 'Bullseye'
    elif value == 25:
        val = 'Bull'
    elif mult == 'D':
        val = mult + str(value/2)
    elif mult == 'T':
        val = mult + str(value/3)
    elif mult == 'S':
        val = str(value)
    return val

def find_finishes(score):
    preference = [40, 32, 16, 8, 4, 2]
    diction = AutoVivification()
    singles = []
    doubles = []
    triples = []
    for mult in ['S', 'D', 'T']:
        for num in range(1,21):
            key = mult + str(num)
            if mult == 'S':
                diction[str(num)] = num
                singles.append(num)
            elif mult == 'D':
                diction[key] = num * 2
                doubles.append(num*2)
            elif mult == 'T':
                diction[key] = num * 3
                triples.append(num*3)
    doubles.append(50)
    singles = [50, 25] + singles
    all_throws =  singles + triples

    if score in doubles:
        key = check_bull(score, 'D')
        return key
        
    top_val = 0
    top_num = 0
    top_key = None
    for value in reversed(all_throws):
        for num in doubles:
            val2 = check_bull(num, 'D')
            if score == value + num:
                if value in singles:
                    val1 = check_bull(value, 'S')
                    key = val1 + ', ' + val2
                elif value in triples:
                    val1 = check_bull(value, 'T')
                    key = val1 + ', ' + val2
                if (val1 > top_val and top_num not in preference) or (num in preference and num > top_num):
                    top_val = val1
                    top_key = key
                    if num in preference:
                        top_num = num
    
    if top_key == None:
        top_val1 = 0
        top_val2 = 0
        top_num = 0
        for value1 in reversed(all_throws):
            for value2 in reversed(all_throws):
                for num in doubles:
                    val3 = check_bull(num, 'D')
                    if score == value1 + value2 + num:
                        if value1 in triples:
                            val1 = check_bull(value1, 'T')
                            if value2 in singles:
                                val2 = check_bull(value2, 'S')
                                key = val1 + ', ' + val2 + ', ' + val3
                            elif value2 in triples:
                                val2 = check_bull(value2, 'T')
                                key = val1 + ', ' + val2 + ', ' + val3
                            if (value1 > top_val1 and value2 > top_val2 and top_num not in preference) or (num in preference and num > top_num):
                                top_val1 = value1
                                top_val2 = value2
                                if num in preference:
                                    top_num = num
                                top_key = key
    
    if top_key == None:
        top_key = "Not yet"                            
    return top_key

""" darten """

import pickle
import os
import numpy as np
from datetime import datetime
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
        self.players = []
        self.set_counter = 0
        #self.date_tag = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M")
        self.date_tag = datetime.now()
        self.twentysix = 0
        
    def save_match_throws(self, players):
        for player in players:
            self.players.append(player.name)
            self.match_throws[player.name] = []

class Set():
    
    def __init__(self, set_id, bo_legs):
        self.set_id = set_id
        self.bo_legs = bo_legs
        self.is_finished = False
        self.won_by = None
        self.lost_by = None
        self.set_throws = {}
        self.leg_counter = 0
        
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
    
    imp_throws = [163, 166, 169, 172, 173, 175, 176, 178, 179]
    
    return [match_id, data, set_id, set_id_db, leg_id, leg_id_db, match_ongoing, imp_throws]

class MyGUI:
                        
    def __init__(self):            
        self.__mainWindow = Tk()
        
        self.mainframes = dict()
        self.subframes = dict()
        
        self.listboxes = dict()
        self.labels = AutoVivification()
        self.buttons = dict()
        self.entries = dict()
        self.optionmenus = AutoVivification()
        
        ### Frames ###
        self.define_main_frames_dict()
        for name, frame in self.MainFrames.items():
            self.mainframes[name] = self.create_frame(**frame)
            
        self.define_sub_frames_dict()
        for name, frame in self.SubFrames.items():
            self.subframes[name] = self.create_frame(**frame)
        
        ### Listboxes ###        
        self.define_listboxes_dict()
        for name, listbox in self.Listboxes.items():
            self.listboxes[name] = self.create_listbox(**listbox)
        
        ### Menus ###
        # self.define_optionmenus_dict()
        # for optionmenu in self.Optionmenus.values():
            # self.optionmenus[optionmenu['name']]['menu'], self.optionmenus[optionmenu['name']]['variable'] = self.create_optionmenu(**optionmenu)
        
        ### Buttons ###
        self.define_buttons_dict()
        for name, button in self.Buttons.items():
            self.buttons[name] = self.create_button(**button)
        
        ### Labels ###
        self.define_labels_dict()
        for name, label in self.Labels.items():
            self.labels[name]['label'] = self.create_labels(self.labels, name=name, **label)
        
        ### Entry boxes ###
        self.define_entries_dict()
        for name, entry in self.Entries.items():
            self.entries[name] = self.create_entry(**entry)
        
        ### Initialization ###
        self.entries['no_of_legs_input'].focus_set()
        
        mainloop()
    
    def define_main_frames_dict(self):
        self.MainFrames = {}
        self.add_to_frame_dict(self.MainFrames, 'settings_frame', self.__mainWindow, row=1, col=1)
        self.add_to_frame_dict(self.MainFrames, 'score_keeper_frame', self.__mainWindow, row=3, col=1)
        self.add_to_frame_dict(self.MainFrames, 'score_frame', self.__mainWindow, row=1, col=3)
        self.add_to_frame_dict(self.MainFrames, 'stats_frame', self.__mainWindow, row=3, col=3)
    
    def define_sub_frames_dict(self):
        self.SubFrames = {}
        self.add_to_frame_dict(self.SubFrames, 'average_frame', self.mainframes['stats_frame'], row=1, col=1)
        self.add_to_frame_dict(self.SubFrames, 'high_frame', self.mainframes['stats_frame'], row=2, col=1)
        self.add_to_frame_dict(self.SubFrames, 'finish_frame', self.mainframes['stats_frame'], row=3, col=1)
        self.add_to_frame_dict(self.SubFrames, 'twentysix_frame', self.mainframes['stats_frame'], row=4, col=1)        
    
    def define_entries_dict(self):
        self.Entries = {}
        self.add_to_entry_dict(self.Entries, 'name_p1_input', self.mainframes['settings_frame'], row=3, col=1, bindings={'<Return>': self.CallBack1}, width=10)
        self.add_to_entry_dict(self.Entries, 'name_p2_input', self.mainframes['settings_frame'], row=3, col=4, bindings={'<Return>': self.CallBack2}, width=10)
        self.add_to_entry_dict(self.Entries, 'no_of_legs_input', self.mainframes['settings_frame'], row=1, col=3, bindings={'<Return>': self.CallBack5}, width=10)
        self.add_to_entry_dict(self.Entries, 'no_of_sets_input', self.mainframes['settings_frame'], row=2, col=3, bindings={'<Return>': self.CallBack6}, width=10)
        
        self.add_to_entry_dict(self.Entries, 'score_input_p1', self.mainframes['score_keeper_frame'], row=2, col=2, bindings={'<Return>': self.CallBack3}, width=10, sticky=E)
        self.add_to_entry_dict(self.Entries, 'score_input_p2', self.mainframes['score_keeper_frame'], row=2, col=4, bindings={'<Return>': self.CallBack4}, width=10, sticky=E)
        
    def define_listboxes_dict(self):
        self.Listboxes = {}
        self.add_to_listbox_dict(self.Listboxes, 'score_keeper_p1', self.mainframes['score_keeper_frame'], row=2, col=1, rowspan=2, width=10)
        self.add_to_listbox_dict(self.Listboxes, 'score_keeper_p2', self.mainframes['score_keeper_frame'], row=2, col=3, rowspan=2, width=10)
    
    def define_buttons_dict(self):
        self.Buttons = {}
        self.add_to_button_dict(self.Buttons, 'start_new_match', self.mainframes['settings_frame'], text='Start new match', row=3, col=2, columnspan=2, bindings={'<Return>':self.start_dart_match, '<Button-1>':self.start_dart_match}, sticky=N, takefocus=1)
        self.add_to_button_dict(self.Buttons, 'Undo_p1', self.mainframes['score_keeper_frame'], text='Undo', row=3, col=2, callback=self.delete_entry1)
        self.add_to_button_dict(self.Buttons, 'Undo_p2', self.mainframes['score_keeper_frame'], text='Undo', row=3, col=4, callback=self.delete_entry2)        
        
    def define_labels_dict(self):        
        self.Labels = {}
        
        """Settings frame"""
        self.add_to_label_dict(self.Labels, 'topname_desc_p1', self.mainframes['settings_frame'], row=1, col=1, text='User name player 1', sticky=W)
        self.add_to_label_dict(self.Labels, 'topname_desc_p2', self.mainframes['settings_frame'], row=1, col=4, text='User name player 2', sticky=E)
        self.add_to_label_dict(self.Labels, 'topname_p1', self.mainframes['settings_frame'], row=2, col=1, text='Player 1', sticky=W)
        self.add_to_label_dict(self.Labels, 'topname_p2', self.mainframes['settings_frame'], row=2, col=4, text='Player 2', sticky=E)
        
        self.add_to_label_dict(self.Labels, 'no_of_legs', self.mainframes['settings_frame'], row=1, col=2, text='Number of legs: ', var=True)
        self.add_to_label_dict(self.Labels, 'no_of_sets', self.mainframes['settings_frame'], row=2, col=2, text='Number of sets: ', var=True)
        
        """Score keeper frame"""
        self.add_to_label_dict(self.Labels, 'turn_msg_p1', self.mainframes['score_keeper_frame'], row=1, col=1, columnspan=2, text='Throw! ', var=True)
        self.add_to_label_dict(self.Labels, 'turn_msg_p2', self.mainframes['score_keeper_frame'], row=1, col=3, columnspan=2, text='Wait for it! ', var=True)
        
        self.add_to_label_dict(self.Labels, 'fin_msg_p1', self.mainframes['score_keeper_frame'], row=4, col=1, columnspan=2, text='Not yet', var=True)
        self.add_to_label_dict(self.Labels, 'fin_msg_p2', self.mainframes['score_keeper_frame'], row=4, col=3, columnspan=2, text='Not yet', var=True)
        
        """Score frame"""
        self.add_to_label_dict(self.Labels, 'label_legs', self.mainframes['score_frame'], row=1, col=2, text='Legs: ')
        self.add_to_label_dict(self.Labels, 'label_sets', self.mainframes['score_frame'], row=1, col=3, text='Sets: ')

        self.add_to_label_dict(self.Labels, 'label_p1_name', self.mainframes['score_frame'], row=2, col=1, text='Player 1')
        self.add_to_label_dict(self.Labels, 'label_p2_name', self.mainframes['score_frame'], row=3, col=1, text='Player 2')

        self.add_to_label_dict(self.Labels, 'leg_count_p1', self.mainframes['score_frame'], row=2, col=2, text='0')
        self.add_to_label_dict(self.Labels, 'set_count_p1', self.mainframes['score_frame'], row=2, col=3, text='0')
        self.add_to_label_dict(self.Labels, 'leg_count_p2', self.mainframes['score_frame'], row=3, col=2, text='0')
        self.add_to_label_dict(self.Labels, 'set_count_p2', self.mainframes['score_frame'], row=3, col=3, text='0')

        """Stats frames"""
        
        """Average frame"""
        self.add_to_label_dict(self.Labels, 'frame_desc_average', self.subframes['average_frame'], col=1, row=1, text="Averages")
        self.add_to_label_dict(self.Labels, 'lp1_average', self.subframes['average_frame'], row=2, col=1, text='Player 1')
        self.add_to_label_dict(self.Labels, 'lp2_average', self.subframes['average_frame'], row=3, col=1, text='Player 2')
        self.add_to_label_dict(self.Labels, 'label_average_first9', self.subframes['average_frame'], row=1, col=2, text='First 9 darts')
        self.add_to_label_dict(self.Labels, 'label_average_match', self.subframes['average_frame'], row=1, col=3, text='Match average')

        self.add_to_label_dict(self.Labels, 'first9_average_p1', self.subframes['average_frame'], row=2, col=2, text='0')
        self.add_to_label_dict(self.Labels, 'match_average_p1', self.subframes['average_frame'], row=2, col=3, text='0')
        self.add_to_label_dict(self.Labels, 'first9_average_p2', self.subframes['average_frame'], row=3, col=2, text='0')
        self.add_to_label_dict(self.Labels, 'match_average_p2', self.subframes['average_frame'], row=3, col=3, text='0')
        
        """High frame"""
        self.add_to_label_dict(self.Labels, 'frame_desc_high', self.subframes['high_frame'], col=1, row=1, text="High throws")
        self.add_to_label_dict(self.Labels, 'lp1_high', self.subframes['high_frame'], row=2, col=1, text='Player 1')
        self.add_to_label_dict(self.Labels, 'lp2_high', self.subframes['high_frame'], row=3, col=1, text='Player 2')
        self.add_to_label_dict(self.Labels, 'label_throw60', self.subframes['high_frame'], row=1, col=2, text='60-100')
        self.add_to_label_dict(self.Labels, 'label_throw100', self.subframes['high_frame'], row=1, col=3, text='100-140')
        self.add_to_label_dict(self.Labels, 'label_throw140', self.subframes['high_frame'], row=1, col=4, text='140-180')
        self.add_to_label_dict(self.Labels, 'label_throw180', self.subframes['high_frame'], row=1, col=5, text='180')
        
        self.add_to_label_dict(self.Labels, 'throw60_count_p1', self.subframes['high_frame'], row=2, col=2, text='0')
        self.add_to_label_dict(self.Labels, 'throw100_count_p1', self.subframes['high_frame'], row=2, col=3, text='0')
        self.add_to_label_dict(self.Labels, 'throw140_count_p1', self.subframes['high_frame'], row=2, col=4, text='0')
        self.add_to_label_dict(self.Labels, 'throw180_count_p1', self.subframes['high_frame'], row=2, col=5, text='0')
        self.add_to_label_dict(self.Labels, 'throw60_count_p2', self.subframes['high_frame'], row=3, col=2, text='0')
        self.add_to_label_dict(self.Labels, 'throw100_count_p2', self.subframes['high_frame'], row=3, col=3, text='0')
        self.add_to_label_dict(self.Labels, 'throw140_count_p2', self.subframes['high_frame'], row=3, col=4, text='0')
        self.add_to_label_dict(self.Labels, 'throw180_count_p2', self.subframes['high_frame'], row=3, col=5, text='0')
        
        """Finish frame"""
        self.add_to_label_dict(self.Labels, 'frame_desc_finish', self.subframes['finish_frame'], col=1, row=1, text="Finishes")
        self.add_to_label_dict(self.Labels, 'lp1_finish', self.subframes['finish_frame'], row=2, col=1, text='Player 1')
        self.add_to_label_dict(self.Labels, 'lp2_finish', self.subframes['finish_frame'], row=3, col=1, text='Player 2')
        self.add_to_label_dict(self.Labels, 'label_finish80', self.subframes['finish_frame'], row=1, col=2, text='0-80')
        self.add_to_label_dict(self.Labels, 'label_finish130', self.subframes['finish_frame'], row=1, col=3, text='80-130')
        self.add_to_label_dict(self.Labels, 'label_finish130up', self.subframes['finish_frame'], row=1, col=4, text='130+')
        self.add_to_label_dict(self.Labels, 'finish80_count_p1', self.subframes['finish_frame'], row=2, col=2, text='0')
        self.add_to_label_dict(self.Labels, 'finish130_count_p1', self.subframes['finish_frame'], row=2, col=3, text='0')
        self.add_to_label_dict(self.Labels, 'finish130up_count_p1', self.subframes['finish_frame'], row=2, col=4, text='0')
        self.add_to_label_dict(self.Labels, 'finish80_count_p2', self.subframes['finish_frame'], row=3, col=2, text='0')
        self.add_to_label_dict(self.Labels, 'finish130_count_p2', self.subframes['finish_frame'], row=3, col=3, text='0')
        self.add_to_label_dict(self.Labels, 'finish130up_count_p2', self.subframes['finish_frame'], row=3, col=4, text='0')
        
        """26!!!"""
        self.add_to_label_dict(self.Labels, 'label_26', self.subframes['twentysix_frame'], col=1, row=1, text="TWENTYSIX!!!")
        self.add_to_label_dict(self.Labels, 'count_26', self.subframes['twentysix_frame'], col=2, row=1, text="0")
    
    def create_entry(self, parent, row, column, rowspan, columnspan, width, bindings, callback, sticky):
        new_entry = Entry(parent, width=width)
        if callback is None:
            for binding, callback in bindings.items():
                new_entry.bind(binding, callback)
        else:
            new_entry.config(command=callback)
        new_entry.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)
        return new_entry
    
    def create_button(self, parent, text, row, column, rowspan, columnspan, bindings, callback, width, sticky, takefocus):
        new_button = ttk.Button(parent, text=text, takefocus=takefocus)
        if callback is None:
            for binding, callback in bindings.items():
                new_button.bind(binding, callback)
        else:
            new_button.config(command=callback)
        
        new_button.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)
        return new_button
    
    def create_frame(self, parent, row, column, rowspan, columnspan):
        new_frame = Frame(parent)
        new_frame.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
        return new_frame
    
    def create_listbox(self, parent, row, column, rowspan, columnspan, width, bindings):
        new_listbox = Listbox(parent, width = width)
        new_listbox.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
        if bindings is not None:
            for binding, callback in bindings.items():
                new_listbox.bind(binding, callback)
        return new_listbox
        
    def create_labels(self, dct, name, parent, row, column, rowspan, columnspan, width, var, text, sticky):
        if var == True:
            dct[name]['textvar'] = StringVar()
            dct[name]['textvar'].set(text)
            new_label = Label(parent, textvariable=dct[name]['textvar'])
            
        else:
            new_label = Label(parent, text=text)
    
        new_label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)
    
        return new_label

    def add_to_entry_dict(self, dct, name, frame, row, col, rowspan=1, columnspan=1, bindings=None, callback=None, width=10, sticky=None):
        dct[name] = dict(parent=frame, row=row, column=col, rowspan=rowspan, columnspan=columnspan, bindings=bindings, callback=callback, width=width, sticky=sticky)
        return dct
        
    def add_to_label_dict(self, dct, name, frame, row, col, rowspan=1, columnspan=1, width=10, text=None, var=False, sticky=None):
        dct[name] = dict(parent=frame, row=row, column=col, rowspan=rowspan, columnspan=columnspan, width=width, text=text, var=var, sticky=sticky)
        return dct
        
    def add_to_frame_dict(self, dct, name, frame, row, col, rowspan=1, columnspan=1):
        dct[name] = dict(parent=frame, row=row, column=col, rowspan=rowspan, columnspan=columnspan)
        return dct
        
    def add_to_button_dict(self, dct, name, frame, text, row, col, rowspan=1, columnspan=1, bindings=None, callback=None, width=10, sticky=None, takefocus=1):
        dct[name] = dict(parent=frame, text=text, row=row, column=col, rowspan=rowspan, columnspan=columnspan, bindings=bindings, callback=callback, width=width, sticky=sticky, takefocus=takefocus)
        return dct
        
    def add_to_listbox_dict(self, dct, name, frame, row, col, rowspan=1, columnspan=1, width=10, bindings=None):
        dct[name] = dict(parent=frame, row=row, column=col, rowspan=rowspan, columnspan=columnspan, width=width, bindings=bindings)
        return dct
        
    def delete_entry1(self):
        throw = int(self.listboxes['score_keeper_p1'].get(END).split()[-1])
        self.listboxes['score_keeper_p1'].delete(END)
        self.cycle_label_text()
        self.player1.no_throws -= 1
        
        del self.data['legs'][self.leg_id_db].leg_throws[self.player1.name][-1]
        del self.data['sets'][self.set_id_db].set_throws[self.player1.name][-1]
        del self.data['matches'][self.match_id].match_throws[self.player1.name][-1]
        
        self.entries['score_input_p1'].focus_set()
        self.check_throw_stats_p1(throw, self.player1, 'remove')
        self.update_averages_p1(self.data, self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player1, 'N')
        self.player1.score += throw
        
    def delete_entry2(self):
        throw = int(self.listboxes['score_keeper_p2'].get(END).split()[-1])
        self.listboxes['score_keeper_p2'].delete(END)
        self.cycle_label_text()
        self.player2.no_throws -= 1
        
        del self.data['legs'][self.leg_id_db].leg_throws[self.player2.name][-1]
        del self.data['sets'][self.set_id_db].set_throws[self.player2.name][-1]
        del self.data['matches'][self.match_id].match_throws[self.player2.name][-1]
        
        self.entries['score_input_p2'].focus_set()
        self.check_throw_stats_p2(throw, self.player2, 'remove')
        self.update_averages_p2(self.data, self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player2, 'N')
        self.player2.score += throw
    
    def change_number_label(self, text, label):
        label.config(text = str(text))
        
    def check_throw_stats_p1(self, throw, player, remove=None):
        if remove == 'remove':
            if throw == 180:
                player.count_180 -= 1
                self.labels['throw180_count_p1']['label'].config(text = str(player.count_180))
            elif throw >= 140:
                player.count_140 -= 1
                self.labels['throw140_count_p1']['label'].config(text = str(player.count_140))
            elif throw >= 100:
                player.count_100 -= 1
                self.labels['throw100_count_p1']['label'].config(text = str(player.count_100))
            elif throw >= 60:
                player.count_60 -= 1
                self.labels['throw60_count_p1']['label'].config(text = str(player.count_60))
            elif throw == 26:
                self.data['matches'][self.match_id].twentysix -= 1
                self.labels['count_26']['label'].config(text = str(self.data['matches'][self.match_id].twentysix))
                
        else:
            if throw == 180:
                player.count_180 += 1
                self.labels['throw180_count_p1']['label'].config(text = str(player.count_180))
            elif throw >= 140:
                player.count_140 += 1
                self.labels['throw140_count_p1']['label'].config(text = str(player.count_140))
            elif throw >= 100:
                player.count_100 += 1
                self.labels['throw100_count_p1']['label'].config(text = str(player.count_100))
            elif throw >= 60:
                player.count_60 += 1
                self.labels['throw60_count_p1']['label'].config(text = str(player.count_60))
            elif throw == 26:
                self.data['matches'][self.match_id].twentysix += 1
                self.labels['count_26']['label'].config(text = str(self.data['matches'][self.match_id].twentysix))
            
    def check_finish_stats_p1(self, throw, player):
        if throw >= 130:
            player.finish_130up += 1
            self.labels['finish130up_count_p1']['label'].config(text = str(player.finish_130up))
        elif throw >= 80:
            player.finish_130 += 1
            self.labels['finish130_count_p1']['label'].config(text = str(player.finish_130))
        else:
            player.finish_80 += 1
            self.labels['finish80_count_p1']['label'].config(text = str(player.finish_80))
    
    def check_throw_stats_p2(self, throw, player, remove=None):
        if remove == 'remove':
            if throw == 180:
                player.count_180 -= 1
                self.labels['throw180_count_p2']['label'].config(text = str(player.count_180))
            elif throw >= 140:
                player.count_140 -= 1
                self.labels['throw140_count_p2']['label'].config(text = str(player.count_140))
            elif throw >= 100:
                player.count_100 -= 1
                self.labels['throw100_count_p2']['label'].config(text = str(player.count_100))
            elif throw >= 60:
                player.count_60 -= 1
                self.labels['throw60_count_p2']['label'].config(text = str(player.count_60))
            elif throw == 26:
                self.data['matches'][self.match_id].twentysix -= 1
                self.labels['count_26']['label'].config(text = str(self.data['matches'][self.match_id].twentysix))
                
        else:
            if throw == 180:
                player.count_180 += 1
                self.labels['throw180_count_p2']['label'].config(text = str(player.count_180))
            elif throw >= 140:
                player.count_140 += 1
                self.labels['throw140_count_p2']['label'].config(text = str(player.count_140))
            elif throw >= 100:
                player.count_100 += 1
                self.labels['throw100_count_p2']['label'].config(text = str(player.count_100))
            elif throw >= 60:
                player.count_60 += 1
                self.labels['throw60_count_p2']['label'].config(text = str(player.count_60))
            elif throw == 26:
                self.data['matches'][self.match_id].twentysix += 1
                self.labels['count_26']['label'].config(text = str(self.data['matches'][self.match_id].twentysix))
            
    def check_finish_stats_p2(self, throw, player):
        if throw >= 130:
            player.finish_130up += 1
            self.labels['finish130up_count_p2']['label'].config(text = str(player.finish_130up))
        elif throw >= 80:
            player.finish_130 += 1
            self.labels['finish130_count_p2']['label'].config(text = str(player.finish_130))
        else:
            player.finish_80 += 1
            self.labels['finish80_count_p2']['label'].config(text = str(player.finish_80))
    
    def calculate_averages(self, Leg, Set, Match, player):
        Leg_average = np.mean(Leg.leg_throws[player.name])
        Set_average = np.mean(Set.set_throws[player.name])
        Match_average = np.mean(Match.match_throws[player.name])
        
        if player.no_throws == 3:
            First_9 = np.mean(Leg.leg_throws[player.name])
        
    def update_averages_p1(self, data, Leg, Set, Match, player, BelowNine):
        Leg_average = np.mean(Leg.leg_throws[player.name])
        Set_average = np.mean(Set.set_throws[player.name])
        Match_average = np.mean(Match.match_throws[player.name])
        
        if player.no_throws == 3 or BelowNine == 'Y':
            First_9 = []
            for key in data['legs'].keys():
                match_counter = data['match_counter']
                len_match_count = len(str(match_counter))
                if key[:len_match_count] == str(match_counter):
                    First_9 += data['legs'][key].leg_throws[player.name][:3]
            
            First_9_mean = np.mean(First_9)
            self.labels['first9_average_p1']['label'].config(text = '{:.2f}'.format(First_9_mean))
        
        self.labels['match_average_p1']['label'].config(text = '{:.2f}'.format(Match_average))
    
    def update_averages_p2(self, data, Leg, Set, Match, player, BelowNine):
        Leg_average = np.mean(Leg.leg_throws[player.name])
        Set_average = np.mean(Set.set_throws[player.name])
        Match_average = np.mean(Match.match_throws[player.name])
        
        if player.no_throws == 3 or BelowNine == 'Y':
            First_9 = []
            for key in data['legs'].keys():
                match_counter = data['match_counter']
                len_match_count = len(str(match_counter))
                if key[:len_match_count] == str(match_counter):
                    First_9 += data['legs'][key].leg_throws[player.name][:3]
            
            First_9_mean = np.mean(First_9)
            self.labels['first9_average_p2']['label'].config(text = '{:.2f}'.format(First_9_mean))
        
        self.labels['match_average_p2']['label'].config(text = '{:.2f}'.format(Match_average))

    def cycle_label_text(self):
        self.LABEL_TEXT = ["Throw!", "Wait for it!"]
        self.label_index -= 1
        if self.label_index < -1:
            self.label_index = 0
        self.labels['turn_msg_p1']['textvar'].set(self.LABEL_TEXT[self.label_index])
        self.labels['turn_msg_p2']['textvar'].set(self.LABEL_TEXT[self.label_index+1])

    def CallBack1(self, event):
        self.labelText = self.entries['name_p1_input'].get()
        self.labels['topname_p1']['label'].config(text = self.labelText)
        self.labels['label_p1_name']['label'].config(text = self.labelText)
        
    	self.labels['lp1_average']['label'].config(text = self.labelText)
    	self.labels['lp1_high']['label'].config(text = self.labelText)
    	self.labels['lp1_finish']['label'].config(text = self.labelText)
        
        self.player1 = Darters(self.labelText)
        
        self.entries['name_p2_input'].focus_set()
    
    def CallBack2(self, event):
        self.labelText = self.entries['name_p2_input'].get()
        self.labels['topname_p2']['label'].config(text = self.labelText)
        self.labels['label_p2_name']['label'].config(text = self.labelText)

    	self.labels['lp2_average']['label'].config(text = self.labelText)
    	self.labels['lp2_high']['label'].config(text = self.labelText)
    	self.labels['lp2_finish']['label'].config(text = self.labelText)
        
        self.player2 = Darters(self.labelText)
        
        self.buttons['start_new_match'].focus_set()
        
    def CallBack5(self, event):
        self.labels['no_of_legs']['textvar'].set("Number of legs: %s" % event.widget.get())
        self.bo_legs = int(event.widget.get())
        event.widget.delete(0,END)
        self.entries['no_of_sets_input'].focus_set()
        
    def CallBack6(self, event):
        self.labels['no_of_sets']['textvar'].set("Number of sets: %s" % event.widget.get())
        self.bo_sets = int(event.widget.get())
        event.widget.delete(0,END)
        self.entries['name_p1_input'].focus_set()
        
    def CallBack3(self, event):
        if self.match_ongoing == False:
            print "Start a new match"
            return
        
        if self.player1.no_throws > self.player2.no_throws:
            print "It's not your turn!"
            return
        
        throw = int(event.widget.get())
        if throw < 0 or throw > 180 or throw in self.imp_throws:
            print 'No!'
            event.widget.delete(0,END)
        else:
            self.cycle_label_text()
            self.player1.score, throw = score_keeper(self.player1.score, throw)
            self.labelText = str(self.player1.score) + "    " + str(throw)
            self.listboxes['score_keeper_p1'].insert(END, self.labelText)
            self.listboxes['score_keeper_p1'].yview(END)
            event.widget.delete(0, 'end')
            
            self.data['legs'][self.leg_id_db].leg_throws[self.player1.name].append(throw)
            self.data['sets'][self.set_id_db].set_throws[self.player1.name].append(throw)
            self.data['matches'][self.match_id].match_throws[self.player1.name].append(throw)
            
            if self.player1.score != 0:
                self.player1.no_throws += 1
                self.calculate_averages(self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player1)
                self.entries['score_input_p2'].focus_set()
                self.check_throw_stats_p1(throw, self.player1)
                self.update_averages_p1(self.data, self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player1, 'N')
                self.labels['fin_msg_p1']['textvar'].set(find_finishes(self.player1.score))
            
            else:
                self.player1.no_throws += 1
                self.check_finish_stats_p1(throw, self.player1)
                self.check_throw_stats_p1(throw, self.player1)
                self.calculate_averages(self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player1)
                self.update_averages_p1(self.data, self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player1, 'N')
                if self.player2.no_throws < 9:
                    self.update_averages_p2(self.data, self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player2, 'Y')

                self.data['legs'][self.leg_id_db].finish = throw
                self.data['legs'][self.leg_id_db].is_finished = True
                self.data['legs'][self.leg_id_db].won_by = self.player1.name
                self.data['legs'][self.leg_id_db].lost_by = [loser.name for loser in self.players if loser != self.player1]
            
                save_data(self.data,fname)
                
                self.player2.no_throws = 0
                self.player1.no_throws = 0
            
                self.data['sets'][self.set_id_db].leg_counter += 1
                self.player1.legs += 1
            
                if self.player1.legs == self.bo_legs:
                
                    self.data['sets'][self.set_id_db].is_finished = True
                    self.data['sets'][self.set_id_db].won_by = self.player1.name
                    self.data['sets'][self.set_id_db].lost_by = [loser.name for loser in self.players if loser != self.player1]
                
                    save_data(self.data,fname)
                
                    self.data['sets'][self.set_id_db].leg_counter = 0
                    self.leg_id = 1
                    self.data['matches'][self.match_id].set_counter += 1
                    self.player1.sets += 1
                    
                    self.change_number_label(self.player1.sets, self.labels['set_count_p1']['label'])
                
                    if self.player1.sets == self.bo_sets:
                        
                        legs_reset(self.players)
                        
                        self.change_number_label(self.player1.legs, self.labels['leg_count_p1']['label'])
                        self.change_number_label(self.player2.legs, self.labels['leg_count_p2']['label'])
                    
                        self.data['matches'][self.match_id].is_finished = True
                        self.data['matches'][self.match_id].won_by = self.player1.name
                        self.data['matches'][self.match_id].lost_by = [loser.name for loser in self.players if loser != self.player1]
                    
                        save_data(self.data,fname)
                    
                        self.match_ongoing = False
                        print '%s has won the game!' % self.player1.name
                        
                        self.buttons['start_new_match'].focus_set()
                        ## Hier moet misschien nog iets van een break!
                    else:
                        score_reset(self.players)
                        self.listboxes['score_keeper_p1'].delete(0,END)
                        self.listboxes['score_keeper_p2'].delete(0,END)
                        self.listboxes['score_keeper_p1'].insert(END, "501")
                        self.listboxes['score_keeper_p2'].insert(END, "501")
                        
                        self.labels['fin_msg_p1']['textvar'].set("Not yet")
                        self.labels['fin_msg_p2']['textvar'].set("Not yet")
                    
                        self.set_id += 1
                        self.set_id_db = str(self.match_id) + '.' + str(self.set_id)

                        self.data['sets'][self.set_id_db] = Set(self.set_id_db, self.bo_legs)
                        self.data['sets'][self.set_id_db].save_set_throws(self.players)
                    
                        self.leg_id_db = str(self.match_id) + '.' + str(self.set_id) + '.' + str(self.leg_id)
            
                        self.data['legs'][self.leg_id_db] = Leg(self.leg_id_db)
                        self.data['legs'][self.leg_id_db].save_leg_throws(self.players)
                    
                        legs_reset(self.players)
                        
                        self.entries['score_input_p2'].focus_set()
                        
                        self.change_number_label(self.player1.legs, self.labels['leg_count_p1']['label'])
                        self.change_number_label(self.player2.legs, self.labels['leg_count_p2']['label'])
                        
                        print '%s has won the set %s!' % (self.player1.name, self.data['matches'][self.match_id].set_counter)
                else:
                    
                    self.leg_id += 1
                    self.leg_id_db = str(self.match_id) + '.' + str(self.set_id) + '.' + str(self.leg_id)
            
                    self.data['legs'][self.leg_id_db] = Leg(self.leg_id_db)
                    self.data['legs'][self.leg_id_db].save_leg_throws(self.players)
                
                    score_reset(self.players)
                    self.change_number_label(self.player1.legs, self.labels['leg_count_p1']['label'])
                    self.labels['fin_msg_p1']['textvar'].set("Not yet")
                    self.labels['fin_msg_p2']['textvar'].set("Not yet")

                    self.entries['score_input_p2'].focus_set()
                    
                    self.listboxes['score_keeper_p1'].delete(0,END)
                    self.listboxes['score_keeper_p2'].delete(0,END)
                    self.listboxes['score_keeper_p1'].insert(END, "501")
                    self.listboxes['score_keeper_p2'].insert(END, "501")
                    print '%s has won the leg %s!' % (self.player1.name, self.data['sets'][self.set_id_db].leg_counter)
    
    def CallBack4(self, event):
        if self.match_ongoing == False:
            print "Start a new match"
            return
        
        if self.player2.no_throws > self.player1.no_throws:
            print "It's not your turn!"
            return
        
        throw = int(event.widget.get())
        if throw < 0 or throw > 180 or throw in self.imp_throws:
            print 'No!'
            event.widget.delete(0,END)
            
        else:
            self.cycle_label_text()
            self.player2.score, throw = score_keeper(self.player2.score, throw)
            self.labelText = str(self.player2.score) + "    " + str(throw)
            self.listboxes['score_keeper_p2'].insert(END, self.labelText)
            self.listboxes['score_keeper_p2'].yview(END)
            event.widget.delete(0, 'end')
            
            self.data['legs'][self.leg_id_db].leg_throws[self.player2.name].append(throw)
            self.data['sets'][self.set_id_db].set_throws[self.player2.name].append(throw)
            self.data['matches'][self.match_id].match_throws[self.player2.name].append(throw)
            
            if self.player2.score != 0:
                self.player2.no_throws += 1
                self.entries['score_input_p1'].focus_set()
                self.check_throw_stats_p2(throw, self.player2)
                self.calculate_averages(self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player2)
                self.update_averages_p2(self.data, self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player2, 'N')
                self.labels['fin_msg_p2']['textvar'].set(find_finishes(self.player2.score))
            
            else:
                self.player2.no_throws += 1
                self.check_finish_stats_p2(throw, self.player2)
                self.check_throw_stats_p2(throw, self.player2)
                self.calculate_averages(self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player2)
                self.update_averages_p2(self.data, self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player2, 'N')
                if self.player1.no_throws < 9:
                    self.update_averages_p1(self.data, self.data['legs'][self.leg_id_db], self.data['sets'][self.set_id_db], self.data['matches'][self.match_id], self.player1, 'Y')
                
                self.data['legs'][self.leg_id_db].finish = throw
                self.data['legs'][self.leg_id_db].is_finished = True
                self.data['legs'][self.leg_id_db].won_by = self.player2.name
                self.data['legs'][self.leg_id_db].lost_by = [loser.name for loser in self.players if loser != self.player2]
            
                save_data(self.data,fname)

                self.player2.no_throws = 0
                self.player1.no_throws = 0

                self.data['sets'][self.set_id_db].leg_counter += 1
                self.player2.legs += 1
            
                if self.player2.legs == self.bo_legs:
                
                    self.data['sets'][self.set_id_db].is_finished = True
                    self.data['sets'][self.set_id_db].won_by = self.player2.name
                    self.data['sets'][self.set_id_db].lost_by = [loser.name for loser in self.players if loser != self.player2]
                    
                    save_data(self.data,fname)
                
                    self.data['sets'][self.set_id_db].leg_counter = 0
                    self.leg_id = 1
                    self.data['matches'][self.match_id].set_counter += 1
                    self.player2.sets += 1
                    
                    self.change_number_label(self.player2.sets, self.labels['set_count_p2']['label'])
                
                    if self.player2.sets == self.bo_sets:
                        
                        legs_reset(self.players)
                        
                        self.change_number_label(self.player1.legs, self.labels['leg_count_p1']['label'])
                        self.change_number_label(self.player2.legs, self.labels['leg_count_p2']['label'])
                                                
                        self.data['matches'][self.match_id].is_finished = True
                        self.data['matches'][self.match_id].won_by = self.player2.name
                        self.data['matches'][self.match_id].lost_by = [loser.name for loser in self.players if loser != self.player2]

                        save_data(self.data,fname)
                    
                        self.match_ongoing = False
                        print '%s has won the game!' % self.player2.name
                        
                        self.buttons['start_new_match'].focus_set()
                        ## Hier moet misschien nog iets van een break!
                    else:
                        score_reset(self.players)
                        self.listboxes['score_keeper_p1'].delete(0,END)
                        self.listboxes['score_keeper_p2'].delete(0,END)
                        self.listboxes['score_keeper_p1'].insert(END, "501")
                        self.listboxes['score_keeper_p2'].insert(END, "501")
                        
                        self.labels['fin_msg_p1']['textvar'].set("Not yet")
                        self.labels['fin_msg_p2']['textvar'].set("Not yet")
                    
                        self.set_id += 1
                        self.set_id_db = str(self.match_id) + '.' + str(self.set_id)

                        self.data['sets'][self.set_id_db] = Set(self.set_id_db, self.bo_legs)
                        self.data['sets'][self.set_id_db].save_set_throws(self.players)
                    
                        self.leg_id_db = str(self.match_id) + '.' + str(self.set_id) + '.' + str(self.leg_id)
            
                        self.data['legs'][self.leg_id_db] = Leg(self.leg_id_db)
                        self.data['legs'][self.leg_id_db].save_leg_throws(self.players)
                    
                        legs_reset(self.players)

                        self.entries['score_input_p1'].focus_set()
                        
                        self.change_number_label(self.player2.legs, self.labels['leg_count_p2']['label'])
                        self.change_number_label(self.player1.legs, self.labels['leg_count_p1']['label'])
                        
                        print '%s has won the set %s!' % (self.player2.name, self.data['matches'][self.match_id].set_counter)
                else:
                    
                    self.leg_id += 1
                    self.leg_id_db = str(self.match_id) + '.' + str(self.set_id) + '.' + str(self.leg_id)
            
                    self.data['legs'][self.leg_id_db] = Leg(self.leg_id_db)
                    self.data['legs'][self.leg_id_db].save_leg_throws(self.players)
                
                    score_reset(self.players)
                    self.change_number_label(self.player2.legs, self.labels['leg_count_p2']['label'])

                    self.labels['fin_msg_p1']['textvar'].set("Not yet")
                    self.labels['fin_msg_p2']['textvar'].set("Not yet")
                    
                    self.entries['score_input_p1'].focus_set()
                    
                    self.listboxes['score_keeper_p1'].delete(0,END)
                    self.listboxes['score_keeper_p2'].delete(0,END)
                    self.listboxes['score_keeper_p1'].insert(END, "501")
                    self.listboxes['score_keeper_p2'].insert(END, "501")
                    print '%s has won the leg %s!' % (self.player2.name, self.data['sets'][self.set_id_db].leg_counter)
    
        
    def start_dart_match(self, event):
        for attr in ['bo_legs', 'bo_sets', 'player1', 'player2']:
            if not hasattr(self, attr):
                print "%s is not defined yet!, make sure to press enter after filling in an entrybox" % (attr)
                return
        
        self.listboxes['score_keeper_p1'].delete(0,END)
        self.listboxes['score_keeper_p2'].delete(0,END)
        self.listboxes['score_keeper_p1'].insert(END, '501')
        self.listboxes['score_keeper_p2'].insert(END, '501')
        
        self.entries['score_input_p1'].delete(0,END)
        self.entries['score_input_p2'].delete(0,END)
        self.entries['score_input_p1'].focus_set()
        
        self.label_index = 0
        self.labels['turn_msg_p1']['textvar'].set('Throw!')
        self.labels['turn_msg_p2']['textvar'].set('Wait for it!')
        self.labels['fin_msg_p1']['textvar'].set('Not yet')
        self.labels['fin_msg_p2']['textvar'].set('Not yet')
        
        self.players = [self.player1,self.player2]
        [self.match_id, self.data, self.set_id, self.set_id_db, self.leg_id, self.leg_id_db, self.match_ongoing, self.imp_throws] = dart_match(self.players, self.bo_legs, self.bo_sets, data_load)
        for player in self.players:
            player.__init__(name = player.name, matches = player.matches)
            if player.name not in self.data['player_list']:
                self.data['player_list'].append(player.name)
        
        self.labels_changing = [
        ['leg_count_p1', self.player1.legs],
        ['set_count_p1', self.player1.sets],
        ['leg_count_p2', self.player2.legs],
        ['set_count_p2', self.player2.sets],
        ['lp1_average', self.player1.name],
        ['lp2_average', self.player2.name],
        ['lp1_high', self.player1.name],
        ['lp2_high', self.player2.name],
        ['lp1_finish', self.player1.name],
        ['lp2_finish', self.player2.name],
        ['throw60_count_p1', self.player1.count_60],
        ['throw100_count_p1', self.player1.count_100],
        ['throw140_count_p1', self.player1.count_140],
        ['throw180_count_p1', self.player1.count_180],
        ['throw60_count_p2', self.player2.count_60],
        ['throw100_count_p2', self.player2.count_100],
        ['throw140_count_p2', self.player2.count_140],
        ['throw180_count_p2', self.player2.count_180],
        ['finish80_count_p1', self.player1.finish_80],
        ['finish130_count_p1', self.player1.finish_130],
        ['finish130up_count_p1', self.player1.finish_130up],
        ['finish80_count_p2', self.player2.finish_80],
        ['finish130_count_p2', self.player2.finish_130],
        ['finish130up_count_p2', self.player2.finish_130up],
        ['count_26', '0'],
        ['first9_average_p1', '0'],
        ['match_average_p1', '0'],
        ['first9_average_p2', '0'],
        ['match_average_p2', '0']
        ]
        
        for item in self.labels_changing:
            self.change_number_label(item[1], self.labels[item[0]]['label'])

if __name__ == "__main__":

    fname = 'database.pkl'

    if os.path.isfile(fname):
        with open(fname, 'rb') as fp:
            data_load = pickle.load(fp)
    else:
        data_load = AutoVivification()
        data_load['match_counter'] = 0
        data_load['player_list'] = []
    
    myGUI = MyGUI()
