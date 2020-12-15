import numpy as np
from enum import Enum
import copy
from Play_blackjack import log, BlackJack, deck_lookup


class decision(Enum):
    PositiveHit = 1
    NegativeHit = 2
    Stand = 3
    PerformAction = 4
    NONE = 5

class State():
    def __init__(self, game, turn = 1):
        self.state = game
        self.turn = turn # 1- Dealer Decision(hit+ / hit- / stand). 2- Perform decision
        #self.ValidActionsList = []
        self.childAction = decision.NONE
        self.isLeaf = False
        if((game.dealer.hand > game.player.hand) or game.dealer.hand >= 21 or game.dealer.hand <=1):
            game.compare()
            self.isLeaf = True
    
    def __str__(self):
        return str(self.state)+"\nTurn:"+str(self.turn)+"\nChild Action:"+str(self.childAction)+"\nLeaf:"+str(self.isLeaf)
    
    def validAction(self):
        if(self.turn == 1):
            return [decision.PositiveHit, decision.NegativeHit,decision.Stand]
        else:
            #deck = deck_lookup - newState.state.player.cards - newState.state.player.cards
            return [decision.PerformAction]

    def PerformAction(self, action, card = None):
        newState = copy.deepcopy(self)
        if(newState.turn == 1):
            newState.childAction = action
            newState.turn = 2
        else:
            if(newState.childAction == decision.PositiveHit):
                newState.state.hit(newState.state.dealer,"+", card = card, custom=True)
            elif(newState.childAction == decision.NegativeHit):
                newState.state.hit(newState.state.dealer,"-", card = card, custom=True)
            else:
                #newState.state.stand()
                newState.isLeaf = True
            newState.childAction = decision.PerformAction
            newState.turn = 1
            newState.state.compare()
            if(newState.state.log == log.Dealer_Won or newState.state.dealer.hand >= 21 or newState.state.dealer.hand <= 1):
                newState.isLeaf = True
        return newState

if __name__ == "__main__":
    bj = BlackJack()
    bj.beginGame()
    bj.playerTurn()
    if(bj.log == log.Unfinished_Game):
        state1 = State(bj)
        print("Intial State")
        print(state1)
        valid_action = state1.validAction()
        state2 = state1.PerformAction(valid_action[0])
        print("_____________________")
        print("Left most child at Step 1")
        print(state2)
        print("_____________________")
        valid_action2 = state2.validAction()
        state3 = state2.PerformAction(valid_action2[0],card="5_Clubs")
        print("_____________________")
        print("Left most child at Step 2")
        print(state3)
        print("_____________________")

