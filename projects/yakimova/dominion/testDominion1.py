# -*- coding: utf-8 -*-
"""
Created on Thurs Jan 16 11:08 2020 

@author: Artyom Yakimov
"""

import Dominion
import random
from collections import defaultdict
import testUtility

#Get player names
player_names = ["Annie","*Ben","*Carla"]

#number of curses and victory cards
nV = testUtility.GetNumVictory(player_names)
nC = testUtility.GetNumCurses(player_names)

#Define box
box = testUtility.GetBoxes(nV)

#Get Supply Order
supply_order = testUtility.GetSupplyOrder()

#Generate a random supply from the box
supply = testUtility.GetSupply(box, nV, nC, len(player_names))

#initialize the trash
trash = []

#Costruct the Player objects
players = testUtility.GetPlayers(player_names)

#Play the game
turn = 0
while not Dominion.gameover(supply):
    turn += 1    
    print("\r")    
    for value in supply_order:
        print (value)
        for stack in supply_order[value]:
            if stack in supply:
                print (stack, len(supply[stack]))
    print("\r")
    for player in players:
        print (player.name,player.calcpoints())
    print("\rStart of turn " + str(turn))
    for player in players:
        if not Dominion.gameover(supply):
            print("\r")
            player.turn(players,supply,trash)
            

#Final score
dcs=Dominion.cardsummaries(players)
vp=dcs.loc['VICTORY POINTS']
vpmax=vp.max()
winners=[]
for i in vp.index:
    if vp.loc[i]==vpmax:
        winners.append(i)
if len(winners)>1:
    winstring= ' and '.join(winners) + ' win!'
else:
    winstring = ' '.join([winners[0],'wins!'])

print("\nGAME OVER!!!\n"+winstring+"\n")
print(dcs)
