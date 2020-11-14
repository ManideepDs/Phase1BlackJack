from blackjack import BlackJack 
import numpy as np
import random
import copy
import timeit

class State():
    def __init__(self,BlackJack):
        self.game = BlackJack
        #self.gameStatus = (self.game.player.hand < self.game.dealer.hand)
    
    def __str__(self):
        return str(self.game.player) +str(self.game.dealer)+"\nGame Status:"+ ("Dealer Leads" if(self.game.player.hand < self.game.dealer.hand) else "Player Leads")+"\n"
    
    def gameStatus(self):
        if(self.game.dealer.hand >21 or self.game.dealer.hand <=1 or (self.game.player.hand > self.game.dealer.hand)):
            return 0
        elif(self.game.dealer.hand == 21 or (self.game.player.hand < self.game.dealer.hand)):
            return 1
        return 0

    def positiveHit(self):
        """
        Generate child nodes for dealer's + hit
        """
        updated_game = copy.deepcopy(self.game)
        # introduce randomness in the selection of next card
        random.shuffle(updated_game.deck) 
        updated_game.hit(updated_game.dealer,"+")
        new_state = State(updated_game)
        return new_state

    def negativeHit(self):
        """
        Generate child nodes for dealer's - hit
        """
        updated_game = copy.deepcopy(self.game)
        # introduce randomness in the selection of next card
        random.shuffle(updated_game.deck)
        updated_game.hit(updated_game.dealer,"-")
        new_state = State(updated_game)
        return new_state
    
    def random_child(self, num_hits):
        sign = random.choice(["+","-"])
        for i in range(num_hits):
            if(sign == "+"):
                new_state =  self.positiveHit()
            else:
                new_state = self.negativeHit()
        return new_state
            
 
    def recurse_nodes(self):
        """
        Assuming the game ends when one-fourth of the deck is distributed to players and dealers
        num_hits in a best case scenario is 0.25 * num_decks - 4
        Randomly choosing num_hits(0,24):
        """
        num_walks = 1000
        # Game is over in node.state
        if((self.game.log.value != 1) and not (self.game.player.hand >= self.game.dealer.hand)):
            print("Game is finished/Interupted in the Current Stage")
            return
        else:
            for num_hits in range(1,10): # hard-coding num_hits for a single deck
                win_pct = 0
                expected_score = 0
                for i in range(num_walks):
                    new_state = self.random_child(num_hits)
                    win_pct += new_state.gameStatus()
                    expected_score += new_state.game.dealer.hand
                win_pct = float(win_pct)/num_walks
                expected_score = float(expected_score)/num_walks
                print("Number of hits: ", num_hits,"Expected score:",expected_score," Win pct: ",win_pct)


def intialState(self):
    game = BlackJack()
    game.beginGame()
    game.playerTurn()
    return State(game) 
    
    
if __name__ == "__main__":
    game = BlackJack()
    game.beginGame()
    game.playerTurn()
    initialState = State(game)
    print(initialState)
    start = timeit.default_timer()
    initialState.recurse_nodes()
    stop = timeit.default_timer()
    print('Time: ', stop - start)  
    

