import pickle
import os
import numpy as np
from datetime import datetime
from Tkinter import *
import ttk
from darten_gui import Darters, Leg, Set, Match

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
    
    def check_defaults(self, defaults, objects):
        for frame in objects.values():
            for default in defaults.keys():
                try:
                    frame[default]
                except:
                    frame[default] = defaults[default]
    
    def __init__(self):   
        
        self.__mainWindow = Tk()
        
        ### Frames ###
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
        self.frames = dict()
        self.listboxes = dict()
        self.labels = dict()
        self.player_labels = dict()
        
        self.check_defaults(self.frame_defaults, self.Frames)
        
        for frame in self.Frames.values():
            self.frames[frame['name']] = self.create_frame(frame['parent'], frame['row'], frame['column'], frame['rowspan'], frame['columnspan'])
        
        ### Listboxes ###
        self.Listboxes = {'match_box': {'name': 'match_box',
                                    'parent': self.frames['match_overview'],
                                    'row': 1,
                                    'column': 1,
                                    'width': 50}}
        
        self.check_defaults(self.listbox_defaults, self.Listboxes)
        
        for listbox in self.Listboxes.values():
            self.listboxes[listbox['name']] = self.create_listbox(listbox['parent'], listbox['row'], listbox['column'], listbox['rowspan'], listbox['columnspan'], listbox['width'])
        
        ### Menu ###
        self.var = StringVar(self.frames['top_frame'])
        players = data_load['player_list']
        menu = OptionMenu(self.frames['top_frame'], self.var, *players)
        menu.grid(row = 1, column = 1)
        self.var.set(players[0])
        self.selected_player = players[0]
        self.var.trace("w", lambda *args: self.option_changed(self.var))
        
        self.getting_playerstats(players[0], data_load) ## Zorg ervoor dat hier de speler komt die geselecteerd is in het menu.
        self.filling_listbox(self.listboxes['match_box'])
        
        ### Labels ###
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
                                    }
                                    
        self.check_defaults(self.labels_defaults, self.Labels)
        for label in self.Labels.values():
            self.labels[label['name']] = self.create_labels(label['parent'], label['row'], label['column'], label['rowspan'], label['columnspan'], label['width'], label['var'], label['textvariable'], label['text'])
        
        mainloop()
        
    def option_changed(self, varia):
        self.selected_player = varia.get()
        self.getting_playerstats(varia.get(), data_load) 
        self.filling_listbox(self.listboxes['match_box'])
        
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
                                    }
        
        self.check_defaults(self.labels_defaults, self.Labels)
        for label in self.Labels.values():
            self.labels[label['name']] = self.create_labels(label['parent'], label['row'], label['column'], label['rowspan'], label['columnspan'], label['width'], label['var'], label['textvariable'], label['text'])
        
        
    def create_frame(self, parent, row, column, rowspan, columnspan):
        new_frame = Frame(parent)
        new_frame.grid(row = row, column = column, rowspan = rowspan, columnspan = columnspan)
        return new_frame
    
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
        
        match_id = int(self.selected_match_id)
        
        self.selected_match = data_load['matches'][match_id]
        self.opponent = [player for player in self.selected_match.players if player != self.selected_player][0]
        
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
            print set_id, match_id
            if match_id == set_id[0]:
                print f_set_id, match_id, set_id
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
                leg_average_player = '{:.2f}'.format(np.mean(legs.leg_throws[self.selected_player]))
                leg_average_oppo = '{:.2f}'.format(np.mean(legs.leg_throws[self.opponent]))
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
        
        self.check_defaults(self.labels_defaults, self.label_dict)
        for label in self.label_dict.values():
            self.player_labels[label['name']] = self.create_labels(label['parent'], label['row'], label['column'], label['rowspan'], label['columnspan'], label['width'], label['var'],label['textvariable'], label['text'])
    
    def add_to_label_dict(self, col, row, text):
        c_frame = self.frames['graph_frame']
        name = col + (row - 1) * 3
        self.label_dict[name] = dict(name=name, parent=c_frame, row=row, column=col, text=text)
    
    ## filling player overview
    def getting_playerstats(self, name, data):
        all_matches = []
        all_throws = []
        all_averages = []
        all_dates = []
        all_finishes = []

        all_sets = []
        all_legs = []
        
        self.list_of_strings = []
    
        for match in data['matches'].values():
            if name in match.players:
                name_opp = [item for item in match.players if item != name][0]
                all_matches.append(match)
                all_throws += match.match_throws[name]
                all_averages.append(np.mean(match.match_throws[name]))
                all_dates.append(match.date_tag)
            
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
                    
        self.highest_fin = np.max(all_finishes)
        self.highest_av = '{:.2f}'.format(np.max(all_averages))
        self.highest_throw = np.max(all_throws)
        self.av_last_match = '{:.2f}'.format(all_averages[-1])
        if name == match.won_by:
            self.result_last_match = 'win'
        else:
            self.result_last_match = 'lose'

                
def Filling_Overview(name, data):
    
    all_matches = []
    all_throws = []
    all_averages = []
    all_dates = []
    list_of_strings = []
    
    for match in data['matches'].values():
        if name in match.players:
            name_opp = [item for item in match.players if item != name][0]
            all_matches.append(match)
            all_throws += match.match_throws[name]
            all_averages.append(np.mean(match.match_throws[name]))
            all_dates.append(match.date_tag) ## stull need s to be added to the darten_gui
            #print (match.match_id, datetime.strftime(match.date_tag,"%Y-%m-%d %H:%M"), name, name_opp, match.bo_sets, match.bo_legs)
            string = '{:<4d}{:<20s}{:<10s}{:<10s}{:>3d}{:>3d}'.format(match.match_id, datetime.strftime(match.date_tag,"%Y-%m-%d %H:%M"), name, name_opp, match.bo_sets, match.bo_legs)
            list_of_strings.append(string)
            
    return [list_of_strings, all_averages]

if __name__ == "__main__":
    fname = 'database.pkl'

    if os.path.isfile(fname):
        with open(fname, 'rb') as fp:
            data_load = pickle.load(fp)
    else:
        print "file not available"
        
    players = data_load['player_list']
    
    # print players
#
#     for player in players:
#         print Filling_Overview(player, data_load)
        
    overview = overview()