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
            
def find_finishes(score):
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
    singles = singles + [25,50]
    all_throws =  singles + doubles + triples
    # for score in range(2,180):
    if score in doubles:
        num = score/2
        key = 'D' + str(num)
        print key, score
        
    
    for value in all_throws:
        for num in doubles:
            if score == value + num:
                if value in singles:
                    key = str(value) + ', D' + str(num/2)
                elif value in doubles:
                    key = 'D' + str(value/2) + ', D' + str(num/2)
                elif value in triples:
                    key = 'T' + str(value/3) + ', D' + str(num/2)
                print key, score
    
    for value1 in all_throws:
        for value2 in all_throws:
            for num in doubles:
                if score == value1 + value2 + num:
                    if value1 in triples:
                        if value2 in singles:
                            key = 'T' + str(value1/3) + ', ' + str(value2) + ', D' + str(num/2)
                        elif value2 in doubles:
                            key = 'T' + str(value1/3) + ', D' + str(value2/2) + ', D' + str(num/2)
                        elif value2 in triples:
                            key = 'T' + str(value1/3) + ', T' + str(value2/3) + ', D' + str(num/2)
                    elif value1 in doubles:
                        if value2 in singles:
                            key = 'D' + str(value1/2) + ', ' + str(value2) + ', D' + str(num/2)
                        elif value2 in doubles:
                            key = 'D' + str(value1/2) + ', D' + str(value2/2) + ', D' + str(num/2)
                        elif value2 in triples:
                            key = 'D' + str(value1/2) + ', T' + str(value2/3) + ', D' + str(num/2)
                    print key, score

def score_keeper(score, throw):
    if score - throw < 2 and score - throw != 0:
        pass
    else:
        score -= throw
    print score
    return score
    
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
    
    while match_ongoing:
        for player in players:
            throw = int(raw_input("Throw %s: " % player.name)) ## Let op dat het fout gaat zodra er iets anders dan een integer wordt ingevuld
            while throw < 0 or throw > 180:
                print 'No!'
                throw = int(raw_input("Throw %s: " % player.name))
            
            Current_leg.throws[player.name].append(throw)
            
            player.score = score_keeper(player.score, throw)
            
            if player.score != 0:
                player.no_throws += 1
                
            else:
                player.no_throws += 1
                Current_leg.finish = throw
                Current_leg.is_finished = True
                Current_leg.won_by = player.name
                Current_leg.lost_by = [loser.name for loser in players if loser != player]
                
                data['legs'][leg_id_db] = Current_leg
                
                save_data(data,fname)
                
                leg_counter += 1
                player.legs += 1
                
                if player.legs == bo_legs:
                    
                    Current_set.is_finished = True
                    Current_set.won_by = player.name
                    Current_set.lost_by = [loser.name for loser in players if loser != player]
                    
                    data['sets'][set_id_db] = Current_set
                    
                    save_data(data,fname)
                    
                    leg_counter = 0
                    leg_id = 1
                    set_counter += 1
                    player.sets += 1
                    
                    if player.sets == bo_sets:
                        
                        Current_match.is_finished = True
                        Current_match.won_by = player.name
                        Current_match.lost_by = [loser.name for loser in players if loser != player]
                        
                        data['matches'][match_id] = Current_match
                        
                        save_data(data,fname)
                        
                        match_ongoing = False
                        print '%s has won the game!' % player.name
                        break
                    else:
                        score_reset(players)
                        
                        set_id += 1
                        set_id_db = str(match_id) + '.' + str(set_id)

                        Current_set = Set(set_id_db, bo_legs)
                        
                        leg_id_db = str(match_id) + '.' + str(set_id) + '.' + str(leg_id)
                
                        Current_leg = Leg(leg_id_db)
                        Current_leg.save_throws(players)
                        
                        legs_reset(players)
                        print '%s has won the set %s!' % (player.name, set_counter)
                else:
                    
                    leg_id_db = str(match_id) + '.' + str(set_id) + '.' + str(leg_id)
                
                    Current_leg = Leg(leg_id_db)
                    Current_leg.save_throws(players)
                    
                    score_reset(players)
                    print '%s has won the leg %s!' % (player.name, leg_counter)

import pickle
import os

if __name__ == "__main__":
    player1 = Darters(raw_input("Player1: "))
    player2 = Darters(raw_input("Player2: "))

    bo_legs = int(raw_input("Best of legs: "))
    bo_sets = int(raw_input("Best of sets: "))

    fname = 'database.pkl'

    if os.path.isfile(fname):
        with open(fname, 'rb') as fp:
            data = pickle.load(fp)
    else:
        data = AutoVivification()
        data['match_counter'] = 0

    dart_match([player1,player2], bo_legs, bo_sets)
