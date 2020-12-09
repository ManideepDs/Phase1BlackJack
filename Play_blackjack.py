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
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class log(Enum):
    Unfinished_Game = 2
    Player_Won = -1 
    Dealer_Won = 1
    Drawn = 0

class BlackJack():
    def __init__(self,numDecks=1):
        self.deck = deck_lookup.flatten()
        self.dealer = Dealer()
        self.player = Player()
        self.numDecks = numDecks
        self.log = log.Unfinished_Game
        #self.__threshold = threshold
        #1.deck , 2.dealer, 3.player, 4.sign
        self.gameStatus = np.full((4,13,4),0)

    def __str__(self):
        return Colors.GREEN+str(self.player)+Colors.ENDC+Colors.CYAN+str(self.dealer)+Colors.ENDC

    
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
            self.log = log.Player_Won
            #print("Dealer busted -- Player Wins")
        elif(self.player.hand == 21) and (self.dealer.hand == 21):
            if(len(self.dealer.cards) == len(self.player.cards)):
                self.log = log.Drawn
                #print("Player hand and Dealer hand are equal. GAME DRAWN")
            elif(len(self.dealer.cards) > len(self.player.cards)):
                self.log = log.Player_Won
                #print("Player hand and Dealer hand are equal. PLAYER won by the count of cards.")
            else:
                self.log = log.Dealer_Won
                #print("Player hand and Dealer hand sare equal. Dealer won by the count of cards.")
        elif(self.player.hand == self.dealer.hand):
            if(len(self.dealer.cards) == len(self.player.cards)):
                self.log = log.Drawn
                #print("Player hand and Dealer hand are equal. GAME DRAWN")
            elif(len(self.dealer.cards) > len(self.player.cards)):
                self.log = log.Player_Won
                #print("Player hand and Dealer hand are equal. PLAYER won by the count of cards.")
            else:
                self.log = log.Dealer_Won
                #print("Player hand and Dealer hand are equal. Dealer won by the count of cards.") 
        elif self.dealer.hand < self.player.hand:
            self.log = log.Player_Won
            #print("Player wins")
        elif self.dealer.hand > self.player.hand:
            self.log = log.Dealer_Won
            #print("Dealer wins")
        else:
            self.log = log.Drawn
            #print("Draw")
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

    def playerTurn(self):
        """
        Player Controls Implementation
        """
        while True:
            choice=input("\nDo you want to Hit [Press H] or Stand [Press S]")
            if (choice == 'H' or choice ==  'h'):
                choice2 = input("Press + to add next card to total!! or Press - to subtract next card to total")
                self.player = self.hit(self.player, choice2)
                if(self.player == None):
                    print("\n**** Invalid Choice - GAME INTERRUPTED ****")
                    print("\n")
                    break
                if(self.player.hand > 21 or self.player.hand <= 1):
                    print(self)
                    self.log = log.Dealer_Won
                    #print("\nBusted the threshold - You Lost")
                    break
                elif(self.player.hand == 21):
                    print(self)
                    if(self.dealer.hand == 21):
                        if(len(self.dealer.cards) == len(self.player.cards)):
                            self.log = log.Drawn
                            #print("Player hand and Dealer hand are equal.GAME DRAWN")
                        elif(len(self.dealer.cards) > len(self.player.cards)):
                            self.log = log.Player_Won
                            #print("Player hand and Dealer hand are equal. PLAYER WON by the count of cards.")
                        else:
                            self.log = log.Dealer_Won
                            #print("Player hand and Dealer hand are equal. DEALER WON by the count of cards.")
                        break
                    else:
                        self.log = log.Player_Won
                        #print("\nPlayer wins")
                        break
                else:
                    print(Colors.BOLD+Colors.GREEN+str(self.player)+Colors.ENDC)
            elif (choice == 'S' or choice =='s'):
                print("\nRevealing Dealer's cards")
                print(self)
                break
            else:
                print("\n**** Invalid Choice - Please select a valid option ****")
                print("\n")
                break
    
    def dealerTurn(self):
        while(self.dealer.hand<=17 and (self.player.hand > self.dealer.hand)):
            self.dealer.cards=np.append(self.dealer.cards,self.deck[0])
            self.dealer.cardsSign = np.append(self.dealer.cardsSign, +1)
            self.deck = self.deck[1:]
            self.dealer.hand = self.handValue(self.dealer)
        print(self)
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
        a = input("\nEnter an action: P: PLAY, Q:QUIT - ")
        if(a == "p" or a == "P"):
            carddeck = BlackJack()
            carddeck.beginGame() # Begin game
            carddeck.playerTurn() #Players Turns
            if(carddeck.log == log.Unfinished_Game):
                print("\n** DEALERS TURN _ Naive AI **")
                carddeck.dealerTurn()
            carddeck.compare() # Results
        elif(a == 'q' or a=="Q"):
            break
        else:
            print("Invalid Choice. Please try again")
    
