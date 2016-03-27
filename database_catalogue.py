import pickle
import os
import numpy as np
from datetime import datetime
from Tkinter import *
import ttk
from darten_gui import Darters, Leg, Set, Match
import matplotlib.pyplot as plt

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
            
class overview:
    
    frame_defaults = {'rowspan': 1,
                    'columnspan': 1}
                            
    listbox_defaults = {'rowspan': 1,
                        'columnspan': 1,
                        'width': 10}
                        
    labels_defaults = {'rowspan': 1,
                        'columnspan': 1,
                        'width': 10,
                        'var': False,
                        'textvariable': None,
                        'text': None}
    
    button_defaults = {'rowspan': 1,
                        'columnspan': 1,
                        'width': 10}
                        
    optionmenu_defaults = {'rowspan': 1,
                        'columnspan': 1,
                        'width': 10}
    
    def check_defaults(self, defaults, objects):
        for frame in objects.values():
            for default in defaults.keys():
                try:
                    frame[default]
                except:
                    frame[default] = defaults[default]
    
    def __init__(self):   
        
        self.__mainWindow = Tk()
        
        self.frames = dict()
        self.listboxes = dict()
        self.labels = dict()
        self.player_labels = dict()
        self.buttons = dict()
        self.optionmenus = AutoVivification()
        
        self.players = data_load['player_list']
        self.selected_player = self.players[0]
        self.getting_playerstats(self.selected_player, data_load)
        
        ### Frames ###
        self.define_frames_dict()
        self.check_defaults(self.frame_defaults, self.Frames)
        for frame in self.Frames.values():
            self.frames[frame['name']] = self.create_frame(frame['parent'], frame['row'], frame['column'], frame['rowspan'], frame['columnspan'])
        
        ### Listboxes ###        
        self.define_listboxes_dict()
        self.check_defaults(self.listbox_defaults, self.Listboxes)
        for listbox in self.Listboxes.values():
            self.listboxes[listbox['name']] = self.create_listbox(listbox['parent'], listbox['row'], listbox['column'], listbox['rowspan'], listbox['columnspan'], listbox['width'])
        
        ### Menus ###
        self.define_optionmenus_dict()
        self.check_defaults(self.optionmenu_defaults, self.Optionmenus)
        for optionmenu in self.Optionmenus.values():
            self.optionmenus[optionmenu['name']]['menu'], self.optionmenus[optionmenu['name']]['variable'] = self.create_optionmenu(optionmenu['parent'], optionmenu['row'], optionmenu['column'], optionmenu['rowspan'], optionmenu['columnspan'], optionmenu['width'], optionmenu['option_list'])
        
        ### Buttons ###
        self.define_buttons_dict()
        self.check_defaults(self.button_defaults, self.Buttons)
        for button in self.Buttons.values():
            self.buttons[button['name']] = self.create_button(button['parent'], button['row'], button['column'], button['rowspan'], button['columnspan'], button['width'], button['text'], button['command'])
        
        ### Labels ###
        self.define_labels_dict()                        
        self.check_defaults(self.labels_defaults, self.Labels)
        for label in self.Labels.values():
            self.labels[label['name']] = self.create_labels(label['parent'], label['row'], label['column'], label['rowspan'], label['columnspan'], label['width'], label['var'], label['textvariable'], label['text'])
        
        ### Initialize stats in listboxes ###
        self.filling_listbox(self.listboxes['match_box'])
        
        mainloop()
        
    def option_changed(self, varia):
        self.selected_player = varia.get()
        self.getting_playerstats(varia.get(), data_load) 
        self.filling_listbox(self.listboxes['match_box'])
        
        self.define_labels_dict()
        
        self.check_defaults(self.labels_defaults, self.Labels)
        for label in self.Labels.values():
            self.labels[label['name']] = self.create_labels(label['parent'], label['row'], label['column'], label['rowspan'], label['columnspan'], label['width'], label['var'], label['textvariable'], label['text'])
    
    def define_frames_dict(self):
        self.Frames = {'top_frame': {'name': 'top_frame',
                                'parent': self.__mainWindow,
                                'row': 1,
                                'column': 1},
                  'match_overview': {'name': 'match_overview',
                                'parent': self.__mainWindow,
                                'row': 2,
                                'column': 1},
                  'player_overview': {'name': 'player_overview',
                                'parent': self.__mainWindow,
                                'row': 1,
                                'column': 2},
                  'graph_frame': {'name': 'graph_frame',
                                'parent': self.__mainWindow,
                                'row': 2,
                                'column': 2,
                                'rowspan': 1}}
    
    def define_buttons_dict(self):
        self.Buttons = {'savehistogram': {'name': 'savehistogram',
                                    'parent': self.frames['top_frame'],
                                    'row': 1,
                                    'column': 2,
                                    'width': 10,
                                    'text': "Save histogram",
                                    'command': self.savefigure}}
                                    
    def define_listboxes_dict(self):
        self.Listboxes = {'match_box': {'name': 'match_box',
                                    'parent': self.frames['match_overview'],
                                    'row': 1,
                                    'column': 1,
                                    'width': 50}}
    
    def define_labels_dict(self):
        self.Labels = {'av_last_match': {'name': 'av_last_match',
                                        'parent': self.frames['player_overview'],
                                        'row': 1,
                                        'column': 1,
                                        'text': 'Last match average'},
                        'av_last_match_val': {'name': 'av_last_match_val',
                                        'parent': self.frames['player_overview'],
                                        'row': 1,
                                        'column': 2,
                                        'var': True,
                                        'textvariable': self.av_last_match},
                        'result_last_match': {'name': 'result_last_match',
                                        'parent': self.frames['player_overview'],
                                        'row': 1,
                                        'column': 3,
                                        'var': True,
                                        'textvariable': self.result_last_match},
                        'highest_fin': {'name': 'highest_fin',
                                        'parent': self.frames['player_overview'],
                                        'row': 2,
                                        'column': 1,
                                        'text': 'Highest finish'},
                        'highest_fin_val': {'name': 'highest_fin_val',
                                        'parent': self.frames['player_overview'],
                                        'row': 2,
                                        'column': 2,
                                        'var': True,
                                        'textvariable': self.highest_fin},
                        'highest_av': {'name': 'highest_av',
                                        'parent': self.frames['player_overview'],
                                        'row': 2,
                                        'column': 3,
                                        'text': 'Highest average'},
                        'highest_av_val': {'name': 'highest_av_val',
                                        'parent': self.frames['player_overview'],
                                        'row': 2,
                                        'column': 4,
                                        'var': True,
                                        'textvariable': self.highest_av},
                        'highest_throw': {'name': 'highest_throw',
                                        'parent': self.frames['player_overview'],
                                        'row': 2,
                                        'column': 5,
                                        'text': 'Highest throw'},
                        'highest_throw_val': {'name': 'highest_throw_val',
                                        'parent': self.frames['player_overview'],
                                        'row': 2,
                                        'column': 6,
                                        'var': True,
                                        'textvariable': self.highest_throw},
                        'wins': {'name': 'wins',
                                        'parent': self.frames['player_overview'],
                                        'row': 3,
                                        'column': 1,
                                        'text': 'wins'},
                        'wins_val': {'name': 'wins_val',
                                        'parent': self.frames['player_overview'],
                                        'row': 4,
                                        'column': 1,
                                        'var': True,
                                        'textvariable': self.win_count},
                        'losses': {'name': 'losses',
                                        'parent': self.frames['player_overview'],
                                        'row': 3,
                                        'column': 2,
                                        'text': 'losses'},
                        'losses_val': {'name': 'losses_val',
                                        'parent': self.frames['player_overview'],
                                        'row': 4,
                                        'column': 2,
                                        'var': True,
                                        'textvariable': self.loss_count},
                        'win_loss_ratio': {'name': 'win_loss_ratio',
                                        'parent': self.frames['player_overview'],
                                        'row': 3,
                                        'column': 3,
                                        'text': 'win/loss ratio'},
                        'win_loss_ratio_val': {'name': 'win_loss_ratio_val',
                                        'parent': self.frames['player_overview'],
                                        'row': 4,
                                        'column': 3,
                                        'var': True,
                                        'textvariable': self.win_loss_ratio},
                                    }
    
    def define_labels_match_overview_dict(self):
        match_id = int(self.selected_match_id)
        
        all_sets = list()
        all_legs = list()
        row = 1
    
        self.label_dict = {'top1': {'name': 'top1',
                                        'parent': self.frames['graph_frame'],
                                        'row': row,
                                        'column': 1,
                                        'text': ''},
                        'top2': {'name': 'top2',
                                        'parent': self.frames['graph_frame'],
                                        'row': row,
                                        'column': 2,
                                        'var': True,
                                        'textvariable': self.selected_player},
                        'top3': {'name': 'top3',
                                        'parent': self.frames['graph_frame'],
                                        'row': row,
                                        'column': 3,
                                        'var': True,
                                        'textvariable': self.opponent}}
    
        all_set_ids = list()
    
        f_set_id = 1
        for sets in data_load['sets'].values():
            set_id = [int(s_id) for s_id in sets.set_id.split('.')]
            if match_id == set_id[0]:
                all_sets.append(sets)
                all_set_ids.append(set_id[-1])
    
        all_set_ids_sorted = sorted(all_set_ids)
    
        for c_set_id in all_set_ids_sorted:
            set_id = '.'.join([str(match_id),str(c_set_id)])
            sets = data_load['sets'][set_id]
            row += 1
            all_leg_ids = list()
        
            for legs in data_load['legs'].values():
                leg_id = [int(l_id) for l_id in legs.leg_id.split('.')]
                if match_id == leg_id[0] and c_set_id == leg_id[1]:
                    all_legs.append(legs)
                    all_leg_ids.append(leg_id[-1])
        
            all_leg_ids_sorted = sorted(all_leg_ids)
        
            for c_leg_id in all_leg_ids_sorted:
                leg_id = '.'.join([str(match_id),str(c_set_id),str(c_leg_id)])
                legs = data_load['legs'][leg_id]
                if legs.leg_throws[self.selected_player]:
                    leg_average_player = '{:.2f}'.format(np.mean(legs.leg_throws[self.selected_player]))
                else:
                    leg_average_player = 'No throws'
                if legs.leg_throws[self.opponent]:
                    leg_average_oppo = '{:.2f}'.format(np.mean(legs.leg_throws[self.opponent]))
                else:
                    leg_average_oppo = 'No throws'
                
                col = 1
                input_string = 'Set %s - Leg %s' % (c_set_id, c_leg_id)
            
                for text in [input_string, leg_average_player, leg_average_oppo]:
                    self.add_to_label_dict(col, row, text)
                    col += 1
                row += 1

            f_set_id += 1
            col = 1
            for text in ['', '', '']:
                self.add_to_label_dict(col, row, text)
                col += 1
    
    def define_optionmenus_dict(self):
        self.Optionmenus = {'playermenu': {'name': 'playermenu',
                                    'parent': self.frames['top_frame'],
                                    'row': 1,
                                    'column': 1,
                                    'option_list': self.players},}
    
    def create_frame(self, parent, row, column, rowspan, columnspan):
        new_frame = Frame(parent)
        new_frame.grid(row = row, column = column, rowspan = rowspan, columnspan = columnspan)
        return new_frame
    
    def create_button(self, parent, row, column, rowspan, columnspan, width, text, command):
        new_button = Button(parent, width = width, text = text, command = command)
        new_button.grid(row = row, column = column, rowspan = rowspan, columnspan = columnspan)
        return new_button
    
    def create_listbox(self, parent, row, column, rowspan, columnspan, width):
        new_listbox = Listbox(parent, width = width)
        new_listbox.grid(row = row, column = column, rowspan = rowspan, columnspan = columnspan)
        new_listbox.bind('<<ListboxSelect>>', self.onselect)
        return new_listbox
        
    def create_labels(self, parent, row, column, rowspan, columnspan, width, var, textvariable, text):
        
        if var == True:
            textvar = StringVar()
            textvar.set(textvariable)
            new_label = Label(parent, textvariable = textvar)
        else:
            new_label = Label(parent, text = text)
        
        new_label.grid(row = row, column = column, rowspan = rowspan, columnspan = columnspan, sticky = EW)
        
        return new_label
        
    def create_optionmenu(self, parent, row, column, rowspan, columnspan, width, option_list):
        variable = StringVar()
        new_optionmenu = OptionMenu(parent, variable, *option_list)

        new_optionmenu.grid(row = row, column = column, rowspan = rowspan, columnspan = columnspan)
        new_optionmenu.config(width = width)
        
        variable.set(option_list[0])
        variable.trace("w", lambda *args: self.option_changed(variable))
        return new_optionmenu, variable

    def filling_listbox(self, listbox):
        listbox.delete(0,END)
        for item in self.list_of_strings:
            listbox.insert(END, item)
            
    def onselect(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        
        for label in self.player_labels.values():
            label.grid_forget()
        
        self.selected_match_id = value.split()[0]
        
        self.selected_match = data_load['matches'][int(self.selected_match_id)]
        self.opponent = [player for player in self.selected_match.players if player != self.selected_player][0]
        
        self.define_labels_match_overview_dict()
        
        self.check_defaults(self.labels_defaults, self.label_dict)
        for label in self.label_dict.values():
            self.player_labels[label['name']] = self.create_labels(label['parent'], label['row'], label['column'], label['rowspan'], label['columnspan'], label['width'], label['var'],label['textvariable'], label['text'])
    
    def add_to_label_dict(self, col, row, text):
        c_frame = self.frames['graph_frame']
        name = col + (row - 1) * 3
        self.label_dict[name] = dict(name=name, parent=c_frame, row=row, column=col, text=text)
        
    def savefigure(self):
        fig, ax = plt.subplots(1,1)
        plt.hist(self.all_throws, bins=range(np.min(self.all_throws), np.max(self.all_throws) + 1, 1), color = "#87CEFA", edgecolor='none')
        pl_mean = np.mean(self.all_throws)
        all_throws_no_zeros = [val for val in self.all_throws if val != 0]
        pl_mode = np.argmax(np.bincount(all_throws_no_zeros))
        pl_highest = np.max(self.all_throws)
        pl_lowest = np.min(all_throws_no_zeros)
        plt.axvline(pl_mean, color='r')
        
        text = "Average:\nMost frequent throw:\nHighest throw:\nLowest throw:"
        values = "{:>.2f}\n{:>d}\n{:>d}\n{:>d}".format(pl_mean, pl_mode, pl_highest, pl_lowest)
        ax.text(0.5,0.8, text, transform=ax.transAxes, ha='left', fontsize=14)
        ax.text(0.9,0.8, values, transform=ax.transAxes, ha='right', fontsize=14)
        
        fig.savefig("../../histogram_%s.png" % self.selected_player)
    
    ## filling player overview
    def getting_playerstats(self, name, data):
        all_matches = []
        all_match_ids = []
        self.all_throws = []
        all_averages = []
        all_dates = []
        all_finishes = []

        all_sets = []
        all_legs = []
        
        self.win_count = 0
        self.loss_count = 0
        
        self.list_of_strings = []
    
        for match in data['matches'].values():
            if name in match.players:
                name_opp = [item for item in match.players if item != name][0]
                all_matches.append(match)
                all_match_ids.append(match.match_id)
                self.all_throws += match.match_throws[name]
                if match.match_throws[name]:
                    all_averages.append(np.mean(match.match_throws[name]))
                all_dates.append(match.date_tag)
                if match.won_by is not None and match.lost_by is not None:
                    if match.won_by == name:
                        self.win_count += 1
                    elif match.lost_by[0] == name:
                        self.loss_count += 1
            
                string = '{:<4d}{:<20s}{:<10s}{:<10s}{:>3d}{:>3d}'.format(match.match_id, datetime.strftime(match.date_tag,"%Y-%m-%d %H:%M"), name, name_opp, match.bo_sets, match.bo_legs)
                self.list_of_strings.append(string)
        
        for match in all_matches:
            for sets in data['sets'].values():
                if sets.set_id.split('.')[0] == str(match.match_id):
                    all_sets.append(sets)
            for leg in data['legs'].values():
                if leg.leg_id.split('.')[0] == str(match.match_id):
                    all_legs.append(leg)
                    if leg.won_by == self.selected_player:
                        all_finishes.append(leg.finish)
        
        if all_finishes:
            self.highest_fin = np.max(all_finishes)
        else:
            self.highest_fin = 'Never finished'
        
        self.highest_av = '{:.2f}'.format(np.max(all_averages))
        self.highest_throw = np.max(self.all_throws)
        self.av_last_match = '{:.2f}'.format(all_averages[-1])
        last_match_id = all_match_ids.index(np.max(all_match_ids))
        if name == all_matches[last_match_id].won_by:
            self.result_last_match = 'win'
        elif name == all_matches[last_match_id].lost_by:
            self.result_last_match = 'lose'
        else:
            self.result_last_match = 'Did not finish last match'
        
        if self.loss_count == 0 and self.win_count != 0:
            self.win_loss_ratio = 'Only wins bitch!'
        elif self.loss_count == 0 and self.win_count == 0:
            self.win_loss_ratio = 'No games finished yet'
        else:
            self.win_loss_ratio = '{:.2f}'.format(float(self.win_count)/float(self.loss_count))

if __name__ == "__main__":
    fname = 'database.pkl'

    if os.path.isfile(fname):
        with open(fname, 'rb') as fp:
            data_load = pickle.load(fp)
    else:
        print "file not available"
        
    overview = overview()