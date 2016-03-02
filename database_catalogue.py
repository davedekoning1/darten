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
    
    def __init__(self):
        self.__mainWindow = Tk()
        
        ## 
    
    ## filling player overview
    def Filling_Overview(player, data):
        name = player.name
        
        all_throws = []
        all_averages = []
        all_dates = []
        list_of_strings = []
        
        for match in data['matches'].values():
            if name in match.players:
                name_opp = [item for item in match.players if item != name][0]
                all_matches.append(match)
                all_throws += match.throws[name]
                all_averages.append(np.mean(match.throws[name]))
                all_dates.append(match.date_tag) ## stull need s to be added to the darten_gui
                
                string = "{:8s}{:15s}{:15s}{:15s}{:4i}{:4i}".format((match.match_id, datetime.strftime(match.date_tag,"%Y-%m-%d %H:%M"), name, name_opp, match.bo_sets, match.bo_legs))
                list_of_strings.append()
                
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
            
            string = "{:8s}{:15s}{:15s}{:15s}{:4i}{:4i}".format((match.match_id, datetime.strftime(match.date_tag,"%Y-%m-%d %H:%M"), name, name_opp, match.bo_sets, match.bo_legs))
            list_of_strings.append(string)
            
    return list_of_strings

if __name__ == "__main__":
    fname = 'database.pkl'

    if os.path.isfile(fname):
        with open(fname, 'rb') as fp:
            data_load = pickle.load(fp)
    else:
        print "file not available"
        
    players = data_load['player_list']
    
    print players
    
    for player in players:
        print Filling_Overview(player, data_load)