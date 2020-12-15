import numpy as np
import random
from enum import Enum 

#groups of deck in cards:
groups = np.array(["_Clubs", "_Diamonds", "_Hearts", "_Spade"], dtype=str)
value = np.array(["2","3","4","5","6","7","8","9","10","J","Q","K","ace"],dtype=str).reshape(13,1)
deck_lookup = np.char.add(value,groups)

class Player():
    def __init__(self):
        self.cards = []
        self.hand = 0
        self.cardsSign = [+1,+1]
    
    def __str__(self):
        string = ""
        for i,j in zip(self.cards, self.cardsSign):
            string += str(j)+" " + i + " | "
        return "\n__PLAYER__\n"+string+"\nHand Value: " + str(self.hand)

class Dealer():
    def __init__(self):
        self.cards = []
        self.hand = 0
        self.cardsSign = [+1,+1]
    
    def __str__(self):
        string = ""
        for i,j in zip(self.cards, self.cardsSign):
            string += str(j)+" " + i + " | "
        return "\n__DEALER__\n"+string+"\nHand Value: "+str(self.hand)

class GameStatus(Enum):
    # 1 <= Stat <= 3 Player Wins
    # 4 <= stat <= 6 Dealer Wins
    # else: Game Drawn
    Player_Won = 1
    Dealer_Busted_Player_Won = 2
    Dealer_Won = 3
    Player_Busted_Dealer_Won = 4
    GAME_DRAWN = 5
    NONE = 6

class log(Enum):
    Unfinished_Game = 2
    Player_Won = -1 
    Dealer_Won = 1
    Drawn = 0

class BlackJack():
    def __init__(self,numDecks=1):
        self.deck = list(deck_lookup.flatten()) * numDecks
        self.dealer = Dealer()
        self.player = Player()
        self.numDecks = numDecks
        self.log = log.Unfinished_Game
        self.score = 0
        #self.__threshold = threshold
        #1.deck , 2.dealer, 3.player, 4.sign
        self.gameStatus = GameStatus.NONE

    def __str__(self):
        return str(self.player)+str(self.dealer)

    
    def __shuffleDeck(self):
        random.shuffle(self.deck)
    
    def deal(self):
        self.__shuffleDeck()
        self.dealer.cards = self.deck[0:4:2]
        self.player.cards = self.deck[1:4:2]
        self.deck = self.deck[4:]
        self.player.hand = self.handValue(self.player)
        self.dealer.hand = self.handValue(self.dealer)
    
    def ace_val(self,current_sum,sign): 
        """
        Determining whether ace needs to be 1 or 11
        """
        if(sign == +1):
            if(current_sum+11 <= 21):
                return 11
            return 1
        elif(sign == -1):
            if(current_sum >= 12):
                return -11
            return -1
    
    def handValue(self,member):
        """
        Calculate hand value of player/dealer at any point in the game.
        """
        x = zip(np.sort(member.cards), np.argsort(member.cards))
        hand = 0
        for i,j in x:
            if i[0].isnumeric() & (i[0] != '1'):
                hand += int(i[0])*member.cardsSign[j]
            elif i[0] == 'a':
                hand += self.ace_val(hand,member.cardsSign[j])
            else:
                hand += 10*member.cardsSign[j]
        return hand
    
    def hit(self, member, sign, custom = False, card=None):
        """
        Each turn, player gets asked whether they want to add or subtract the next card value before the next card is dealt. 
        If its above 21, automatically busts, if not keep going until stand or bust
        """
        #choice2 = input("Press + to add next card to total!! or Press - to subtract next card to total")
        if custom:
            member.cards = np.append(member.cards, card)
            self.deck = np.delete(self.deck, np.where(self.deck == card))
        else:
            member.cards = np.append(member.cards, self.deck[0])
            self.deck = self.deck[1:]
        if sign == '+':
            member.cardsSign = np.append(member.cardsSign, +1)
        elif sign == '-':
            member.cardsSign = np.append(member.cardsSign, -1)
        else:
            return None
        member.hand = self.handValue(member)
        return member
    
    
    def stand(self): #no more hits on players card
        return self.compare() 

 
    def compare(self): #compare player and dealers card value to determine who wins
        if(self.dealer.hand>21):
            self.score = 21 - self.dealer.hand
            self.log = log.Player_Won
            self.gameStatus = GameStatus.Dealer_Busted_Player_Won
        elif(self.dealer.hand<=1):
            self.score = self.dealer.hand - 1
            self.log = log.Player_Won
            self.gameStatus = GameStatus.Dealer_Busted_Player_Won
        elif((self.player.hand == 21) and (self.dealer.hand == 21)):
            self.score = 0
            self.log = log.Drawn
            self.gameStatus = GameStatus.GAME_DRAWN
        elif(self.player.hand == self.dealer.hand):
            self.score = 0
            self.log = log.Drawn
            self.gameStatus = GameStatus.GAME_DRAWN
        elif self.dealer.hand < self.player.hand:
            self.score = self.dealer.hand - self.player.hand
            self.log = log.Player_Won
            self.gameStatus = GameStatus.Player_Won
        elif self.dealer.hand > self.player.hand:
            self.score = self.dealer.hand - self.player.hand
            self.log = log.Dealer_Won
            self.gameStatus = GameStatus.Dealer_Won
        else:
            self.score = 0
            self.log = log.Drawn
            self.gameStatus = GameStatus.GAME_DRAWN
        #self.restart()
        return 

    def beginGame(self):
        print("**** GAME BEGINS ****")
        print("\n......Dealing cards......")
        print("\n....Shuffing the deck....")
        self.deal()
        print(self.player)
        print("\n __Dealer__:")
        print(self.dealer.cards[0])
        print("\n** PLAYERS TURN  **")

    def playerTurn(self,verbose = True):
        """
        Player Controls Implementation
        """
        while True:
            choice=input("\nDo you want to Hit [Press H] or Stand [Press S]")
            if (choice == 'H' or choice ==  'h'):
                choice2 = input("Press + to add next card to total!! or Press - to subtract next card to total")
                if(choice2 == '+' or choice2 == '-'):
                    self.player = self.hit(self.player, choice2)
                    if(self.player == None):
                        print("\n**** Invalid Choice - GAME INTERRUPTED ****")
                        print("\n")
                        break
                    if(self.player.hand > 21 or self.player.hand <= 1):
                        if verbose: print(self)
                        self.log = log.Dealer_Won
                        self.score = 21-self.dealer.hand
                        self.gameStatus = GameStatus.Player_Busted_Dealer_Won
                        break
                    elif(self.player.hand == 21 and self.dealer.hand == 21):
                        if verbose: print(self)
                        self.score = 0
                        self.log = log.Drawn
                        self.gameStatus = GameStatus.GAME_DRAWN
                        break
                    else:
                        if verbose: print(str(self.player))
                else:
                    print("\n**** Invalid Choice - Please select a valid option ****")
            elif (choice == 'S' or choice =='s'):
                if verbose:
                    print("\nRevealing Dealer's cards")
                    print(self)
                break
            else:
                print("\n**** Invalid Choice - Please select a valid option ****")
    
    def dealerTurn(self, verbose = True):
        #BaseAI
        while(self.dealer.hand<=17 and (self.player.hand >= self.dealer.hand)):
            self.dealer.cards=np.append(self.dealer.cards,self.deck[0])
            self.dealer.cardsSign = np.append(self.dealer.cardsSign, +1)
            self.deck = self.deck[1:]
            self.dealer.hand = self.handValue(self.dealer)
        if verbose: print(self)
        return    
    
    def restart(self):
        self.deck = deck_lookup.flatten()
        self.dealerCards = []
        self.playerCards = []
        self.playerHand = 0
        self.dealerHand = 0
        #1.deck , 2.dealer, 3.player, 4.sign
        self.gameStatus = np.full((13,4,4),0)


if __name__ == "__main__":
    while True:
        try:
            gameSize = int(input("Enter the number of decks:"))
            break
        except ValueError:
            print("Invalid input. Please enter an integer")
    while True:
        a = input("\nEnter an action: P: PLAY, Q:QUIT - ")
        if(a == "p" or a == "P"):
            carddeck = BlackJack(1)
            carddeck.beginGame() # Begin game
            carddeck.playerTurn() #Players Turns
            if(carddeck.log == log.Unfinished_Game):
                print("\n** DEALERS TURN _ Naive AI **")
                carddeck.dealerTurn()
                carddeck.compare() # Results
            print("\nScore: ",carddeck.score)
            print(carddeck.gameStatus.name)
        elif(a == 'q' or a=="Q"):
            break
        else:
            print("Invalid Choice. Please try again")
    
