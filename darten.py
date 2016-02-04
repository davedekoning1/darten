# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 22:39:23 2016

@author: konin_de
"""

""" darten """

score = 0

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
    
    def __init__(self, id, bo_legs, bo_sets):
        self.id = id
        self.bo_legs = bo_legs
        self.bo_sets = bo_sets

class Set():
    is_finished = False
    won_by = None
    lost_by = None
    
    def __init__(self, id, bo_legs):
        self.id = id
        self.bo_legs = bo_legs
    
class Leg():
    is_finished = False
    won_by = None
    lost_by = None
    throws = {}
    finish = 0
    twentysix = []
    
    def __init__(self, id, players):
        self.id = id
    
    def save_throws(players):
        for player in players:
            throws[player.name] = []

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
        
def dart_match(players, bo_legs, bo_sets):
    match_id = 1
    
    Current_match = Match(match_id, bo_legs, bo_sets)
    
    set_id = 1

    Current_set = Set(str(match_id) + '.' + str(set_id), bo_legs)
    
    leg_id = 1

    Current_leg = Leg(str(match_id) + '.' + str(set_id) + '.' + str(leg_id))
    
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
                
                data[legs][leg_id].append(Current_leg)
                
                leg_counter += 1
                player.legs += 1
                
                if player.legs == bo_legs:
                    
                    Current_set.is_finished = True
                    Current.set.won_by = player.name
                    Current_set.lost_by = [loser.name for loser in players if loser != player]
                    
                    data[sets][set_id].append(Current_set)
                    
                    leg_counter = 0
                    set_counter += 1
                    player.sets += 1
                    
                    if player.sets == bo_sets:
                        
                        Current_match.is_finished = True
                        Current_match.won_by = player.name
                        Current_match.lost_by = [loser.name for loser in players if loser != player]
                        
                        data[matches][match_id].append(Current_match)
                        
                        match_ongoing = False
                        print '%s has won the game!' % player.name
                        break
                    else:
                        set_id += 1

                        Current_set = Set(str(match_id) + '.' + str(set_id), bo_legs)
                        
                        legs_reset(players)
                        print '%s has won the set %s!' % (player.name, set_counter)
                else:
                    
                    leg_id += 1
                
                    Current_leg = Leg(str(match_id) + '.' + str(set_id) + '.' + str(leg_id))
                    
                    score_reset(players)
                    print '%s has won the leg %s!' % (player.name, leg_counter)

player1 = Darters(raw_input("Player1: "))
player2 = Darters(raw_input("Player2: "))

dart_match([player1,player2], 3,3)
