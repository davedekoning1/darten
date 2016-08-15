# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 22:39:23 2016

@author: konin_de

New update 09-02-2016:
    Database issue is fixed, however it was found that the statistics for
    first 9 darts do not match yet.
    Furthermore the code can possibly be cleaned a fair bit.

    ** Still to be added **
    1. combine the 2 screens in one gui!
    3. continue match button
    4. Maybe add a menu for the settings of the match
    6. Nicer playername input fields
    7. Better layout of the gui
    10. Pop-up screen/save to excel/pdf with match overview
    11. Pop-ups when doing something wrong

"""
import os
import sys

import pickle
import numpy as np
from datetime import datetime

if sys.version[0] == str(2):
    import Tkinter as tkinter
    import ttk
else:
    import tkinter
    from tkinter import ttk


def check_bull(value, mult):
    if value == 50:
        val = 'Bullseye'
    elif value == 25:
        val = 'Bull'
    elif mult == 'D':
        val = mult + str(int(value/2))
    elif mult == 'T':
        val = mult + str(int(value/3))
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
        for num in range(1, 21):
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
    all_throws = singles + triples

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
                if (value > top_val and top_num not in preference) or \
                        (num in preference and num > top_num):
                    top_val = value
                    top_key = key
                    if num in preference:
                        top_num = num

    if top_key is None:
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
                            if (value1 > top_val1 and value2 > top_val2 and
                                    top_num not in preference) or \
                                    (num in preference and num > top_num):
                                top_val1 = value1
                                top_val2 = value2
                                if num in preference:
                                    top_num = num
                                top_key = key

    if top_key is None:
        top_key = "Not yet"
    return top_key


class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


class Darters():
    def __init__(self, name, number, score=501, no_throws=0, legs=0,
                 sets=0, matches=0, average=0):
        self.name = name
        self.number = number
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
        # self.date_tag = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M")
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


def scoreKeeper(score, throw):
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
    match_id = data[b'match_counter'] + 1
    data[b'match_counter'] += 1

    data[b'matches'][match_id] = Match(match_id, bo_legs, bo_sets)
    data[b'matches'][match_id].save_match_throws(players)

    set_id = 1
    set_id_db = str(match_id) + '.' + str(set_id)

    data[b'sets'][set_id_db] = Set(set_id_db, bo_legs)
    data[b'sets'][set_id_db].save_set_throws(players)

    leg_id = 1
    leg_id_db = str(match_id) + '.' + str(set_id) + '.' + str(leg_id)

    data[b'legs'][leg_id_db] = Leg(leg_id_db)
    data[b'legs'][leg_id_db].save_leg_throws(players)

    score_reset(players)
    legs_reset(players)
    sets_reset(players)

    match_ongoing = True

    imp_throws = [163, 166, 169, 172, 173, 175, 176, 178, 179]

    return [match_id, data, set_id, set_id_db, leg_id, leg_id_db,
            match_ongoing, imp_throws]


class MyGUI:

    def __init__(self):
        self.__mainWindow = tkinter.Tk()

        self.mainframes = dict()
        self.subframes = dict()

        self.listboxes = dict()
        self.labels = AutoVivification()
        self.buttons = dict()
        self.entries = dict()
        self.optionmenus = AutoVivification()

        self.no_players = 2  # TODO dit moet een invulvak worden in scherm
        self.players = []

        """ Frames """
        self.define_main_frames_dict()
        for name, frame in self.MainFrames.items():
            self.mainframes[name] = self.create_frame(**frame)

        self.define_sub_frames_dict()
        for name, frame in self.SubFrames.items():
            self.subframes[name] = self.create_frame(**frame)

        """ Listboxes """
        self.define_listboxes_dict()
        for name, listbox in self.Listboxes.items():
            self.listboxes[name] = self.create_listbox(**listbox)

        """ Menus """
#         self.define_optionmenus_dict()
#         for optionmenu in self.Optionmenus.values():
#             self.optionmenus[optionmenu['name']]['menu'], \
#             self.optionmenus[optionmenu['name']]['variable'] = \
#             self.create_optionmenu(**optionmenu)

        """ Buttons """
        self.define_buttons_dict()
        for name, button in self.Buttons.items():
            self.buttons[name] = self.create_button(**button)

        """ Labels """
        self.define_labels_dict()
        for name, label in self.Labels.items():
            self.labels[name]['label'] = self.create_labels(self.labels,
                                                            name=name, **label)

        """ Entry boxes """
        self.define_entries_dict()
        for name, entry in self.Entries.items():
            self.entries[name] = self.create_entry(**entry)

        """ Initialization """
        self.entries['no_of_legs_input'].focus_set()

        tkinter.mainloop()

    def define_main_frames_dict(self):
        self.MainFrames = {}
        self.add_to_frame_dict(self.MainFrames, 'settings_frame',
                               self.__mainWindow, row=1, col=1)
        self.add_to_frame_dict(self.MainFrames, 'score_keeper_frame',
                               self.__mainWindow, row=3, col=1)
        self.add_to_frame_dict(self.MainFrames, 'score_frame',
                               self.__mainWindow, row=1, col=3)
        self.add_to_frame_dict(self.MainFrames, 'stats_frame',
                               self.__mainWindow, row=3, col=3)

    def define_sub_frames_dict(self):
        self.SubFrames = {}
        self.add_to_frame_dict(self.SubFrames, 'average_frame',
                               self.mainframes['stats_frame'], row=1, col=1)
        self.add_to_frame_dict(self.SubFrames, 'high_frame',
                               self.mainframes['stats_frame'], row=2, col=1)
        self.add_to_frame_dict(self.SubFrames, 'finish_frame',
                               self.mainframes['stats_frame'], row=3, col=1)
        self.add_to_frame_dict(self.SubFrames, 'twentysix_frame',
                               self.mainframes['stats_frame'], row=4, col=1)

    def define_entries_dict(self):
        self.Entries = {}
        self.add_to_entry_dict(self.Entries, 'name_input_p1',
                               self.mainframes['settings_frame'], row=3, col=1,
                               bindings={'<Return>': self.CallBack1}, width=10)
        self.add_to_entry_dict(self.Entries, 'name_input_p2',
                               self.mainframes['settings_frame'], row=3, col=4,
                               bindings={'<Return>': self.CallBack1}, width=10)
        self.add_to_entry_dict(self.Entries, 'no_of_legs_input',
                               self.mainframes['settings_frame'], row=1, col=3,
                               bindings={'<Return>': self.CallBack2}, width=10)
        self.add_to_entry_dict(self.Entries, 'no_of_sets_input',
                               self.mainframes['settings_frame'], row=2, col=3,
                               bindings={'<Return>': self.CallBack3}, width=10)

        self.add_to_entry_dict(self.Entries, 'score_input_p1',
                               self.mainframes['score_keeper_frame'], row=2,
                               col=2, bindings={'<Return>': self.CallBack4},
                               width=10, sticky=tkinter.E)
        self.add_to_entry_dict(self.Entries, 'score_input_p2',
                               self.mainframes['score_keeper_frame'],
                               row=2, col=4,
                               bindings={'<Return>': self.CallBack4},
                               width=10, sticky=tkinter.E)

    def define_listboxes_dict(self):
        self.Listboxes = {}
        self.add_to_listbox_dict(self.Listboxes, 'score_keeper_p1',
                                 self.mainframes['score_keeper_frame'], row=2,
                                 col=1, rowspan=2, width=10)
        self.add_to_listbox_dict(self.Listboxes, 'score_keeper_p2',
                                 self.mainframes['score_keeper_frame'], row=2,
                                 col=3, rowspan=2, width=10)

    def define_buttons_dict(self):
        self.Buttons = {}
        self.add_to_button_dict(self.Buttons, 'start_new_match',
                                self.mainframes['settings_frame'],
                                text='Start new match', row=3, col=2,
                                bindings={'<Return>': self.start_dart_match,
                                          '<Button-1>': self.start_dart_match},
                                sticky=tkinter.N, takefocus=1, columnspan=2)
        self.add_to_button_dict(self.Buttons, 'Undo_p1',
                                self.mainframes['score_keeper_frame'],
                                text='Undo', row=3, col=2,
                                bindings={'<Return>': self.delete_entry,
                                          '<Button-1>': self.delete_entry})
        self.add_to_button_dict(self.Buttons, 'Undo_p2',
                                self.mainframes['score_keeper_frame'],
                                text='Undo', row=3, col=4,
                                bindings={'<Return>': self.delete_entry,
                                          '<Button-1>': self.delete_entry})

    def define_labels_dict(self):
        self.Labels = {}

        """Settings frame"""
        self.add_to_label_dict(self.Labels, 'top_name_desc_p1',
                               self.mainframes['settings_frame'], row=1, col=1,
                               text='User name player 1', sticky=tkinter.W)
        self.add_to_label_dict(self.Labels, 'top_name_desc_p2',
                               self.mainframes['settings_frame'], row=1, col=4,
                               text='User name player 2', sticky=tkinter.E)
        self.add_to_label_dict(self.Labels, 'top_name_p1',
                               self.mainframes['settings_frame'], row=2, col=1,
                               text='Player 1', sticky=tkinter.W)
        self.add_to_label_dict(self.Labels, 'top_name_p2',
                               self.mainframes['settings_frame'], row=2, col=4,
                               text='Player 2', sticky=tkinter.E)

        self.add_to_label_dict(self.Labels, 'no_of_legs',
                               self.mainframes['settings_frame'], row=1, col=2,
                               text='Number of legs: ', var=True)
        self.add_to_label_dict(self.Labels, 'no_of_sets',
                               self.mainframes['settings_frame'], row=2, col=2,
                               text='Number of sets: ', var=True)

        """Score keeper frame"""
        self.add_to_label_dict(self.Labels, 'turn_msg_p1',
                               self.mainframes['score_keeper_frame'], row=1,
                               col=1, columnspan=2, text='Throw! ', var=True)
        self.add_to_label_dict(self.Labels, 'turn_msg_p2',
                               self.mainframes['score_keeper_frame'], row=1,
                               col=3, columnspan=2, text='Wait for it! ',
                               var=True)

        self.add_to_label_dict(self.Labels, 'fin_msg_p1',
                               self.mainframes['score_keeper_frame'], row=4,
                               col=1, columnspan=2, text='Not yet', var=True)
        self.add_to_label_dict(self.Labels, 'fin_msg_p2',
                               self.mainframes['score_keeper_frame'], row=4,
                               col=3, columnspan=2, text='Not yet', var=True)

        """Score frame"""
        self.add_to_label_dict(self.Labels, 'label_legs',
                               self.mainframes['score_frame'], row=1, col=2,
                               text='Legs: ')
        self.add_to_label_dict(self.Labels, 'label_sets',
                               self.mainframes['score_frame'], row=1, col=3,
                               text='Sets: ')

        self.add_to_label_dict(self.Labels, 'label_name_p1',
                               self.mainframes['score_frame'], row=2, col=1,
                               text='Player 1')
        self.add_to_label_dict(self.Labels, 'label_name_p2',
                               self.mainframes['score_frame'], row=3, col=1,
                               text='Player 2')

        self.add_to_label_dict(self.Labels, 'leg_count_p1',
                               self.mainframes['score_frame'], row=2, col=2,
                               text='0')
        self.add_to_label_dict(self.Labels, 'set_count_p1',
                               self.mainframes['score_frame'], row=2, col=3,
                               text='0')
        self.add_to_label_dict(self.Labels, 'leg_count_p2',
                               self.mainframes['score_frame'], row=3, col=2,
                               text='0')
        self.add_to_label_dict(self.Labels, 'set_count_p2',
                               self.mainframes['score_frame'], row=3, col=3,
                               text='0')

        """Stats frames"""

        """Average frame"""
        self.add_to_label_dict(self.Labels, 'frame_desc_average',
                               self.subframes['average_frame'], col=1, row=1,
                               text="Averages")
        self.add_to_label_dict(self.Labels, 'l_average_p1',
                               self.subframes['average_frame'], row=2, col=1,
                               text='Player 1')
        self.add_to_label_dict(self.Labels, 'l_average_p2',
                               self.subframes['average_frame'], row=3, col=1,
                               text='Player 2')
        self.add_to_label_dict(self.Labels, 'label_average_first9',
                               self.subframes['average_frame'], row=1, col=2,
                               text='First 9 darts')
        self.add_to_label_dict(self.Labels, 'label_average_match',
                               self.subframes['average_frame'], row=1, col=3,
                               text='Match average')

        self.add_to_label_dict(self.Labels, 'first9_average_p1',
                               self.subframes['average_frame'], row=2, col=2,
                               text='0')
        self.add_to_label_dict(self.Labels, 'match_average_p1',
                               self.subframes['average_frame'], row=2, col=3,
                               text='0')
        self.add_to_label_dict(self.Labels, 'first9_average_p2',
                               self.subframes['average_frame'], row=3, col=2,
                               text='0')
        self.add_to_label_dict(self.Labels, 'match_average_p2',
                               self.subframes['average_frame'], row=3, col=3,
                               text='0')

        """High frame"""
        self.add_to_label_dict(self.Labels, 'frame_desc_high',
                               self.subframes['high_frame'], col=1, row=1,
                               text="High throws")
        self.add_to_label_dict(self.Labels, 'l_high_p1',
                               self.subframes['high_frame'], row=2, col=1,
                               text='Player 1')
        self.add_to_label_dict(self.Labels, 'l_high_p2',
                               self.subframes['high_frame'], row=3, col=1,
                               text='Player 2')
        self.add_to_label_dict(self.Labels, 'label_throw60',
                               self.subframes['high_frame'], row=1, col=2,
                               text='60-100')
        self.add_to_label_dict(self.Labels, 'label_throw100',
                               self.subframes['high_frame'], row=1, col=3,
                               text='100-140')
        self.add_to_label_dict(self.Labels, 'label_throw140',
                               self.subframes['high_frame'], row=1, col=4,
                               text='140-180')
        self.add_to_label_dict(self.Labels, 'label_throw180',
                               self.subframes['high_frame'], row=1, col=5,
                               text='180')

        self.add_to_label_dict(self.Labels, 'throw60_count_p1',
                               self.subframes['high_frame'], row=2, col=2,
                               text='0')
        self.add_to_label_dict(self.Labels, 'throw100_count_p1',
                               self.subframes['high_frame'], row=2, col=3,
                               text='0')
        self.add_to_label_dict(self.Labels, 'throw140_count_p1',
                               self.subframes['high_frame'], row=2, col=4,
                               text='0')
        self.add_to_label_dict(self.Labels, 'throw180_count_p1',
                               self.subframes['high_frame'], row=2, col=5,
                               text='0')
        self.add_to_label_dict(self.Labels, 'throw60_count_p2',
                               self.subframes['high_frame'], row=3, col=2,
                               text='0')
        self.add_to_label_dict(self.Labels, 'throw100_count_p2',
                               self.subframes['high_frame'], row=3, col=3,
                               text='0')
        self.add_to_label_dict(self.Labels, 'throw140_count_p2',
                               self.subframes['high_frame'], row=3, col=4,
                               text='0')
        self.add_to_label_dict(self.Labels, 'throw180_count_p2',
                               self.subframes['high_frame'], row=3, col=5,
                               text='0')

        """Finish frame"""
        self.add_to_label_dict(self.Labels, 'frame_desc_finish',
                               self.subframes['finish_frame'], col=1, row=1,
                               text="Finishes")
        self.add_to_label_dict(self.Labels, 'l_finish_p1',
                               self.subframes['finish_frame'], row=2, col=1,
                               text='Player 1')
        self.add_to_label_dict(self.Labels, 'l_finish_p2',
                               self.subframes['finish_frame'], row=3, col=1,
                               text='Player 2')
        self.add_to_label_dict(self.Labels, 'label_finish80',
                               self.subframes['finish_frame'], row=1, col=2,
                               text='0-80')
        self.add_to_label_dict(self.Labels, 'label_finish130',
                               self.subframes['finish_frame'], row=1, col=3,
                               text='80-130')
        self.add_to_label_dict(self.Labels, 'label_finish130up',
                               self.subframes['finish_frame'], row=1, col=4,
                               text='130+')
        self.add_to_label_dict(self.Labels, 'finish80_count_p1',
                               self.subframes['finish_frame'], row=2, col=2,
                               text='0')
        self.add_to_label_dict(self.Labels, 'finish130_count_p1',
                               self.subframes['finish_frame'], row=2, col=3,
                               text='0')
        self.add_to_label_dict(self.Labels, 'finish130up_count_p1',
                               self.subframes['finish_frame'], row=2, col=4,
                               text='0')
        self.add_to_label_dict(self.Labels, 'finish80_count_p2',
                               self.subframes['finish_frame'], row=3, col=2,
                               text='0')
        self.add_to_label_dict(self.Labels, 'finish130_count_p2',
                               self.subframes['finish_frame'], row=3, col=3,
                               text='0')
        self.add_to_label_dict(self.Labels, 'finish130up_count_p2',
                               self.subframes['finish_frame'], row=3, col=4,
                               text='0')

        """26!!!"""
        self.add_to_label_dict(self.Labels, 'label_26',
                               self.subframes['twentysix_frame'], col=1, row=1,
                               text="TWENTYSIX!!!")
        self.add_to_label_dict(self.Labels, 'count_26',
                               self.subframes['twentysix_frame'], col=2, row=1,
                               text="0")

    def create_entry(self, parent, row, column, rowspan, columnspan, width,
                     bindings, callback, sticky):
        new_entry = tkinter.Entry(parent, width=width)
        if callback is None:
            for binding, callback in bindings.items():
                new_entry.bind(binding, callback)
        else:
            new_entry.config(command=callback)
        new_entry.grid(row=row, column=column, rowspan=rowspan,
                       columnspan=columnspan, sticky=sticky)
        return new_entry

    def create_button(self, parent, text, row, column, rowspan, columnspan,
                      bindings, callback, width, sticky, takefocus):
        new_button = ttk.Button(parent, text=text, takefocus=takefocus)
        if callback is None:
            for binding, callback in bindings.items():
                new_button.bind(binding, callback)
        else:
            new_button.config(command=callback)

        new_button.grid(row=row, column=column, rowspan=rowspan,
                        columnspan=columnspan, sticky=sticky)
        return new_button

    def create_frame(self, parent, row, column, rowspan, columnspan):
        new_frame = tkinter.Frame(parent)
        new_frame.grid(row=row, column=column, rowspan=rowspan,
                       columnspan=columnspan)
        return new_frame

    def create_listbox(self, parent, row, column, rowspan, columnspan, width,
                       bindings):
        new_listbox = tkinter.Listbox(parent, width=width)
        new_listbox.grid(row=row, column=column, rowspan=rowspan,
                         columnspan=columnspan)
        if bindings is not None:
            for binding, callback in bindings.items():
                new_listbox.bind(binding, callback)
        return new_listbox

    def create_labels(self, dct, name, parent, row, column, rowspan,
                      columnspan, width, var, text, sticky):
        if var:
            dct[name]['textvar'] = tkinter.StringVar()
            dct[name]['textvar'].set(text)
            new_label = tkinter.Label(parent,
                                      textvariable=dct[name]['textvar'])

        else:
            new_label = tkinter.Label(parent, text=text)

        new_label.grid(row=row, column=column, rowspan=rowspan,
                       columnspan=columnspan, sticky=sticky)

        return new_label

    def add_to_entry_dict(self, dct, name, frame, row, col, rowspan=1,
                          columnspan=1, bindings=None, callback=None,
                          width=10, sticky=None):
        dct[name] = dict(parent=frame, row=row, column=col, rowspan=rowspan,
                         columnspan=columnspan, bindings=bindings,
                         callback=callback, width=width, sticky=sticky)
        return dct

    def add_to_label_dict(self, dct, name, frame, row, col, rowspan=1,
                          columnspan=1, width=10, text=None, var=False,
                          sticky=None):
        dct[name] = dict(parent=frame, row=row, column=col, rowspan=rowspan,
                         columnspan=columnspan, width=width, text=text,
                         var=var, sticky=sticky)
        return dct

    def add_to_frame_dict(self, dct, name, frame, row, col, rowspan=1,
                          columnspan=1):
        dct[name] = dict(parent=frame, row=row, column=col, rowspan=rowspan,
                         columnspan=columnspan)
        return dct

    def add_to_button_dict(self, dct, name, frame, text, row, col, rowspan=1,
                           columnspan=1, bindings=None, callback=None,
                           width=10, sticky=None, takefocus=1):
        dct[name] = dict(parent=frame, text=text, row=row, column=col,
                         rowspan=rowspan, columnspan=columnspan,
                         bindings=bindings, callback=callback, width=width,
                         sticky=sticky, takefocus=takefocus)
        return dct

    def add_to_listbox_dict(self, dct, name, frame, row, col, rowspan=1,
                            columnspan=1, width=10, bindings=None):
        dct[name] = dict(parent=frame, row=row, column=col, rowspan=rowspan,
                         columnspan=columnspan, width=width, bindings=bindings)
        return dct

    def delete_entry(self, event):
        caller = event.widget
        ind = list(self.buttons.values()).index(caller)
        player_number = list(self.buttons.keys())[ind].split('_')[-1]
        for player in self.players:
            if player.number == player_number:
                break
        score_keeper = 'score_keeper_{:s}'.format(player_number)
        score_input = 'score_input_{:s}'.format(player_number)
        fin_msg = 'fin_msg_{:s}'.format(player_number)

        throw = int(self.listboxes[score_keeper].get(tkinter.END).split()[-1])
        self.listboxes[score_keeper].delete(tkinter.END)
        self.cycle_label_text()
        player.no_throws -= 1

        del self.data[b'legs'][self.leg_id_db].leg_throws[player.name][-1]
        del self.data[b'sets'][self.set_id_db].set_throws[player.name][-1]
        del self.data[b'matches'][self.match_id].match_throws[player.name][-1]

        self.entries[score_input].focus_set()
        self.check_throw_stats(throw, player, 'remove')
        self.update_averages(self.data, self.data[b'legs'][self.leg_id_db],
                             self.data[b'sets'][self.set_id_db],
                             self.data[b'matches'][self.match_id],
                             player, 'N')
        player.score += throw
        msg = find_finishes(player.score)
        self.labels[fin_msg]['textvar'].set(msg)

    def change_number_label(self, text, label):
        label.config(text=str(text))

    def get_correct_names_widgets(self, player_number):
        score_keeper = 'score_keeper_{:s}'.format(player_number)
        score_input = 'score_input_{:s}'.format(player_number)
        leg_count = 'leg_count_{:s}'.format(player_number)
        set_count = 'set_count_{:s}'.format(player_number)
        fin_msg = 'fin_msg_{:s}'.format(player_number)
        return [score_keeper, score_input, leg_count, set_count, fin_msg]

    def check_throw_stats(self, throw, player, remove=None):
        throw180 = 'throw180_count_{:s}'.format(player.number)
        throw140 = 'throw140_count_{:s}'.format(player.number)
        throw100 = 'throw100_count_{:s}'.format(player.number)
        throw60 = 'throw60_count_{:s}'.format(player.number)
        if remove == 'remove':
            if throw == 180:
                player.count_180 -= 1
                text = str(player.count_180)
                self.labels[throw180]['label'].config(text=text)
            elif throw >= 140:
                player.count_140 -= 1
                text = str(player.count_140)
                self.labels[throw140]['label'].config(text=text)
            elif throw >= 100:
                player.count_100 -= 1
                text = str(player.count_100)
                self.labels[throw100]['label'].config(text=text)
            elif throw >= 60:
                player.count_60 -= 1
                text = str(player.count_60)
                self.labels[throw60]['label'].config(text=text)
            elif throw == 26:
                self.data[b'matches'][self.match_id].twentysix -= 1
                text = str(self.data[b'matches'][self.match_id].twentysix)
                self.labels['count_26']['label'].config(text=text)

        else:
            if throw == 180:
                player.count_180 += 1
                text = str(player.count_180)
                self.labels[throw180]['label'].config(text=text)
            elif throw >= 140:
                player.count_140 += 1
                text = str(player.count_140)
                self.labels[throw140]['label'].config(text=text)
            elif throw >= 100:
                player.count_100 += 1
                text = str(player.count_100)
                self.labels[throw100]['label'].config(text=text)
            elif throw >= 60:
                player.count_60 += 1
                text = str(player.count_60)
                self.labels[throw60]['label'].config(text=text)
            elif throw == 26:
                self.data[b'matches'][self.match_id].twentysix += 1
                text = str(self.data[b'matches'][self.match_id].twentysix)
                self.labels['count_26']['label'].config(text=text)

    def check_finish_stats(self, throw, player):
        finish130up = 'finish130up_count_{:s}'.format(player.number)
        finish130 = 'finish130_count_{:s}'.format(player.number)
        finish80 = 'finish80_count_{:s}'.format(player.number)
        if throw >= 130:
            player.finish_130up += 1
            text = str(player.finish_130up)
            self.labels[finish130up]['label'].config(text=text)
        elif throw >= 80:
            player.finish_130 += 1
            text = str(player.finish_130)
            self.labels[finish130]['label'].config(text=text)
        else:
            player.finish_80 += 1
            text = str(player.finish_80)
            self.labels[finish80]['label'].config(text=text)

    def update_averages(self, data, Leg, Set, Match, player, BelowNine):
        first9_average = 'first9_average_%s' % player.number
        match_average = 'match_average_%s' % player.number
#        Leg_average = np.mean(Leg.leg_throws[player.name])
#        Set_average = np.mean(Set.set_throws[player.name])
        match_av = np.mean(Match.match_throws[player.name])
        Match_average = '{:.2f}'.format(match_av)

        if player.no_throws == 3 or BelowNine == 'Y':
            First_9 = []
            for key in data[b'legs'].keys():
                match_counter = data[b'match_counter']
                len_match_count = len(str(match_counter))
                if key[:len_match_count] == str(match_counter):
                    First_9 += data[b'legs'][key].leg_throws[player.name][:3]

            First_9_mean = '{:.2f}'.format(np.mean(First_9))
            self.labels[first9_average]['label'].config(text=First_9_mean)

        self.labels[match_average]['label'].config(text=Match_average)

    def cycle_label_text(self):
        self.LABEL_TEXT = ["Throw!", "Wait for it!"]
        self.label_index -= 1
        if self.label_index < -1:
            self.label_index = 0
        text1 = self.LABEL_TEXT[self.label_index]
        text2 = self.LABEL_TEXT[self.label_index+1]
        self.labels['turn_msg_p1']['textvar'].set(text1)
        self.labels['turn_msg_p2']['textvar'].set(text2)

    def CallBack1(self, event):
        caller = event.widget
        ind = list(self.entries.values()).index(caller)
        widget_name = list(self.entries.keys())[ind]

        player_number = widget_name.split('_')[-1]
        player_name = self.entries[widget_name].get()
        player = Darters(player_name, player_number)

        top_name = 'top_name_{:s}'.format(player.number)
        label_name = 'label_name_{:s}'.format(player.number)

        l_average = 'l_average_{:s}'.format(player.number)
        l_high = 'l_high_{:s}'.format(player.number)
        l_finish = 'l_finish_{:s}'.format(player.number)

        self.labels[top_name]['label'].config(text=player.name)
        self.labels[label_name]['label'].config(text=player.name)

        self.labels[l_average]['label'].config(text=player.name)
        self.labels[l_high]['label'].config(text=player.name)
        self.labels[l_finish]['label'].config(text=player.name)

        if len(self.players) < self.no_players:
            self.players.append(player)

        if len(self.players) == self.no_players:
            self.buttons['start_new_match'].focus_set()
        else:
            next_entry_box = 'name_input_p{:d}'.format(len(self.players)+1)
            self.entries[next_entry_box].focus_set()

    def CallBack2(self, event):
        self.labels['no_of_legs']['textvar'].set("Number of legs: %s" %
                                                 event.widget.get())
        self.bo_legs = int(event.widget.get())
        event.widget.delete(0, tkinter.END)
        self.entries['no_of_sets_input'].focus_set()

    def CallBack3(self, event):
        self.labels['no_of_sets']['textvar'].set("Number of sets: %s" %
                                                 event.widget.get())
        self.bo_sets = int(event.widget.get())
        event.widget.delete(0, tkinter.END)
        self.entries['name_input_p1'].focus_set()

    def CallBack4(self, event):
        caller = event.widget
        ind = list(self.entries.values()).index(caller)
        player_number = list(self.entries.keys())[ind].split('_')[-1]
        for player in self.players:
            if player.number == player_number:
                break

        opponent = [oppo for oppo in self.players if oppo != player][0]

        [score_keeper, score_input, leg_count,
         set_count, fin_msg] = self.get_correct_names_widgets(player.number)
        [score_keeper_oppo, score_input_oppo, leg_count_oppo, set_count_oppo,
         fin_msg_oppo] = self.get_correct_names_widgets(opponent.number)

        if not self.match_ongoing:
            logger.info("Start a new match")
            return

        if player.no_throws > opponent.no_throws:
            logger.info("It's not your turn!")
            return

        throw = int(event.widget.get())
        if throw < 0 or throw > 180 or throw in self.imp_throws:
            logger.info('No!')
            event.widget.delete(0, tkinter.END)
        else:
            self.cycle_label_text()
            player.score, throw = scoreKeeper(player.score, throw)
            self.labelText = str(player.score) + "    " + str(throw)
            self.listboxes[score_keeper].insert(tkinter.END, self.labelText)
            self.listboxes[score_keeper].yview(tkinter.END)
            event.widget.delete(0, 'end')

            self.data[b'legs'][self.leg_id_db].leg_throws[player.name].\
                append(throw)
            self.data[b'sets'][self.set_id_db].set_throws[player.name].\
                append(throw)
            self.data[b'matches'][self.match_id].match_throws[player.name].\
                append(throw)

            if player.score != 0:
                player.no_throws += 1
                self.entries[score_input_oppo].focus_set()
                self.check_throw_stats(throw, player)
                self.update_averages(self.data,
                                     self.data[b'legs'][self.leg_id_db],
                                     self.data[b'sets'][self.set_id_db],
                                     self.data[b'matches'][self.match_id],
                                     player, 'N')
                msg = find_finishes(player.score)
                self.labels[fin_msg]['textvar'].set(msg)

            else:
                player.no_throws += 1
                self.check_finish_stats(throw, player)
                self.check_throw_stats(throw, player)
                self.update_averages(self.data,
                                     self.data[b'legs'][self.leg_id_db],
                                     self.data[b'sets'][self.set_id_db],
                                     self.data[b'matches'][self.match_id],
                                     player, 'N')
                if opponent.no_throws < 9:
                    self.update_averages(self.data,
                                         self.data[b'legs'][self.leg_id_db],
                                         self.data[b'sets'][self.set_id_db],
                                         self.data[b'matches'][self.match_id],
                                         opponent, 'Y')

                self.data[b'legs'][self.leg_id_db].finish = throw
                self.data[b'legs'][self.leg_id_db].is_finished = True
                self.data[b'legs'][self.leg_id_db].won_by = player.name
                self.data[b'legs'][self.leg_id_db].lost_by = opponent.name

                save_data(self.data, fname)

                opponent.no_throws = 0
                player.no_throws = 0

                self.data[b'sets'][self.set_id_db].leg_counter += 1
                player.legs += 1

                if player.legs == self.bo_legs:

                    self.data[b'sets'][self.set_id_db].is_finished = True
                    self.data[b'sets'][self.set_id_db].won_by = player.name
                    self.data[b'sets'][self.set_id_db].lost_by = opponent.name

                    save_data(self.data, fname)

                    self.data[b'sets'][self.set_id_db].leg_counter = 0
                    self.leg_id = 1
                    self.data[b'matches'][self.match_id].set_counter += 1
                    player.sets += 1

                    self.change_number_label(player.sets,
                                             self.labels[set_count]['label'])

                    if player.sets == self.bo_sets:

                        legs_reset(self.players)

                        self.change_number_label(player.legs,
                                                 self.labels[leg_count]
                                                 ['label'])
                        self.change_number_label(opponent.legs,
                                                 self.labels[leg_count_oppo]
                                                 ['label'])

                        self.data[b'matches'][self.match_id].is_finished = True
                        self.data[b'matches'][self.match_id].won_by = \
                            player.name
                        self.data[b'matches'][self.match_id].lost_by = \
                            opponent.name

                        save_data(self.data, fname)

                        self.match_ongoing = False
                        logger.info('%s has won the game!', player.name)

                        self.buttons['start_new_match'].focus_set()
                        # TODO: Hier moet misschien nog iets van een break!
                    else:
                        score_reset(self.players)
                        self.listboxes[score_keeper].delete(0, tkinter.END)
                        self.listboxes[score_keeper_oppo].delete(0,
                                                                 tkinter.END)
                        self.listboxes[score_keeper].insert(tkinter.END, "501")
                        self.listboxes[score_keeper_oppo].insert(tkinter.END,
                                                                 "501")

                        self.labels[fin_msg]['textvar'].set("Not yet")
                        self.labels[fin_msg_oppo]['textvar'].set("Not yet")

                        self.set_id += 1
                        self.set_id_db = '.'.join([str(self.match_id),
                                                   str(self.set_id)])

                        self.data[b'sets'][self.set_id_db] = \
                            Set(self.set_id_db, self.bo_legs)
                        self.data[b'sets'][self.set_id_db].\
                            save_set_throws(self.players)

                        self.leg_id_db = '.'.join([str(self.match_id),
                                                   str(self.set_id),
                                                   str(self.leg_id)])
                        self.data[b'legs'][self.leg_id_db] = \
                            Leg(self.leg_id_db)
                        self.data[b'legs'][self.leg_id_db].\
                            save_leg_throws(self.players)

                        legs_reset(self.players)

                        self.entries[score_input_oppo].focus_set()

                        self.change_number_label(player.legs,
                                                 self.labels[leg_count]
                                                 ['label'])
                        self.change_number_label(opponent.legs,
                                                 self.labels[leg_count_oppo]
                                                 ['label'])

                        logger.info('%s has won the set %s!', player.name,
                                    self.data[b'matches']
                                    [self.match_id].set_counter)
                else:

                    self.leg_id += 1
                    self.leg_id_db = '.'.join([str(self.match_id),
                                               str(self.set_id),
                                               str(self.leg_id)])

                    self.data[b'legs'][self.leg_id_db] = Leg(self.leg_id_db)
                    self.data[b'legs'][self.leg_id_db].\
                        save_leg_throws(self.players)

                    score_reset(self.players)
                    self.change_number_label(player.legs,
                                             self.labels[leg_count]['label'])
                    self.labels[fin_msg]['textvar'].set("Not yet")
                    self.labels[fin_msg_oppo]['textvar'].set("Not yet")

                    self.entries[score_input_oppo].focus_set()

                    self.listboxes[score_keeper].delete(0, tkinter.END)
                    self.listboxes[score_keeper_oppo].delete(0, tkinter.END)
                    self.listboxes[score_keeper].insert(tkinter.END, "501")
                    self.listboxes[score_keeper_oppo].insert(tkinter.END,
                                                             "501")
                    logger.info('%s has won the leg %s!', player.name,
                                self.data[b'sets'][self.set_id_db].leg_counter)

    def start_dart_match(self, event):
        for attr in ['bo_legs', 'bo_sets']:
            if not hasattr(self, attr):
                msg = """%s is not defined yet!, make sure to press enter after
                      filling in an entrybox"""
                logger.info(msg, (attr))
                return

        if len(self.players) != self.no_players:
            range_players = range(1, self.no_players+1)
            for player in self.players:
                del range_players[range_players.index(int(player.number[1:]))]
            if not range_players:
                pass
            elif len(range_players) > 1:
                miss = ['player{:d}'.format(item) for item in range_players]
                missing_players = ', '.join(miss)
                msg = """%s are not defined yet! Make sure to press enter after
                          filling in an entrybox"""
                logger.info(msg, missing_players)
                return
            elif len(range_players) == 1:
                missing_player = 'player{:d}'.format(range_players[0])
                msg = """%s is not defined yet! Make sure to press enter after
                          filling in an entrybox"""
                logger.info(msg, missing_player)
                return

        self.listboxes['score_keeper_p1'].delete(0, tkinter.END)
        self.listboxes['score_keeper_p2'].delete(0, tkinter.END)
        self.listboxes['score_keeper_p1'].insert(tkinter.END, '501')
        self.listboxes['score_keeper_p2'].insert(tkinter.END, '501')

        self.entries['score_input_p1'].delete(0, tkinter.END)
        self.entries['score_input_p2'].delete(0, tkinter.END)
        self.entries['score_input_p1'].focus_set()

        self.label_index = 0
        self.labels['turn_msg_p1']['textvar'].set('Throw!')
        self.labels['turn_msg_p2']['textvar'].set('Wait for it!')
        self.labels['fin_msg_p1']['textvar'].set('Not yet')
        self.labels['fin_msg_p2']['textvar'].set('Not yet')

        [self.match_id, self.data, self.set_id, self.set_id_db, self.leg_id,
         self.leg_id_db, self.match_ongoing, self.imp_throws] = \
            dart_match(self.players, self.bo_legs, self.bo_sets, data_load)
        for player in self.players:
            #    player.__init__(name=player.name, number=player.number,
            #    matches=player.matches)
            if player.name not in self.data[b'player_list']:
                self.data[b'player_list'].append(player.name)

            self.labels_changing = [
                ['leg_count_{:s}', player.legs],
                ['set_count_{:s}', player.sets],
                ['l_average_{:s}', player.name],
                ['l_high_{:s}', player.name],
                ['l_finish_{:s}', player.name],
                ['throw60_count_{:s}', player.count_60],
                ['throw100_count_{:s}', player.count_100],
                ['throw140_count_{:s}', player.count_140],
                ['throw180_count_{:s}', player.count_180],
                ['finish80_count_{:s}', player.finish_80],
                ['finish130_count_{:s}', player.finish_130],
                ['finish130up_count_{:s}', player.finish_130up],
                ['first9_average_{:s}', '0'],
                ['match_average_{:s}', '0'],
                ['count_26', '0']
            ]
            for item in self.labels_changing:
                label_name = item[0].format(player.number)
                self.change_number_label(item[1],
                                         self.labels[label_name]['label'])

#        self.labels_changing = [
#            ['leg_count_p1', self.players[0].legs],
#            ['set_count_p1', self.players[0].sets],
#            ['leg_count_p2', self.players[1].legs],
#            ['set_count_p2', self.players[1].sets],
#            ['l_average_p1', self.players[0].name],
#            ['l_average_p2', self.players[1].name],
#            ['l_high_p1', self.players[0].name],
#            ['l_high_p2', self.players[1].name],
#            ['l_finish_p1', self.players[0].name],
#            ['l_finish_p2', self.players[1].name],
#            ['throw60_count_p1', self.players[0].count_60],
#            ['throw100_count_p1', self.players[0].count_100],
#            ['throw140_count_p1', self.players[0].count_140],
#            ['throw180_count_p1', self.players[0].count_180],
#            ['throw60_count_p2', self.players[1].count_60],
#            ['throw100_count_p2', self.players[1].count_100],
#            ['throw140_count_p2', self.players[1].count_140],
#            ['throw180_count_p2', self.players[1].count_180],
#            ['finish80_count_p1', self.players[0].finish_80],
#            ['finish130_count_p1', self.players[0].finish_130],
#            ['finish130up_count_p1', self.players[0].finish_130up],
#            ['finish80_count_p2', self.players[1].finish_80],
#            ['finish130_count_p2', self.players[1].finish_130],
#            ['finish130up_count_p2', self.players[1].finish_130up],
#            ['count_26', '0'],
#            ['first9_average_p1', '0'],
#            ['match_average_p1', '0'],
#            ['first9_average_p2', '0'],
#            ['match_average_p2', '0']
#        ]
#
#        for item in self.labels_changing:
#            self.change_number_label(item[1], self.labels[item[0]]['label'])

if __name__ == "__main__":
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    format_logger = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(format_logger)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fname = 'database.pkl'

    if os.path.isfile(fname):
        with open(fname, 'rb') as fp:
            if sys.version[0] == str(2):
                data_load = pickle.load(fp)
            else:
                data_load = pickle.load(fp, encoding='bytes')
    else:
        data_load = AutoVivification()
        data_load['match_counter'] = 0
        data_load['player_list'] = []

    myGUI = MyGUI()
