import numpy as np
import random
from enum import Enum 
import matplotlib.pyplot as plt
import State as lc
#Initialize the required variables

#groups of deck in cards:
groups = np.array(["_Clubs", "_Diamonds", "_Hearts", "_Spade"], dtype=str)
value = np.array(["2","3","4","5","6","7","8","9","10","J","Q","K","ace"],dtype=str).reshape(13,1)
deck_lookup = np.char.add(value,groups)
global player_sum, dealer_sum
playerlose = 0
playerwin = 0
dealerwin = 0
dealerlose = 0
draw = 0
totalgames = 0

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

class log(Enum):
    Continue_Game = 1
    Player_Busted = 2
    Dealer_Busted = 3
    PLayer_Won = 4 
    Dealer_Won = 5 
    Game_Drawn = 6
    Invalid_Choice_Interupption = 7 

class BlackJack():
    def __init__(self):
        self.deck = deck_lookup.flatten()
        self.dealer = Dealer()
        self.player = Player()
        self.numDeck = 1
        self.log = log.Continue_Game
        #self.__threshold = threshold
        #1.deck , 2.dealer, 3.player, 4.sign
        self.gameStatus = np.full((4,13,4),0)

    def __shuffleDeck(self):
        random.shuffle(self.deck)
   
    def AddDecks(self):
        y = int(input("How many decks do u want to add to current deck?")) 
        copy = print(','.join(list(self.deck)) * y) 
        x = np.sort(copy,axis =None)
        print(x)
    
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
    
    def hit(self, member, sign):
        """
        Each turn, player gets asked whether they want to add or subtract the next card value before the next card is dealt. 
        If its above 21, automatically busts, if not keep going until stand or bust
        """
        #choice2 = input("Press + to add next card to total!! or Press - to subtract next card to total")
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
    
    def bust(self):
        if self.player.hand>21:
            return "Player Busted"
        elif self.dealer.hand>21:
            return "Dealer Busted"
 
    def compare(self): #compare player and dealers card value to determine who wins
        global playerlose, playerwin, dealerwin, dealerlose, draw, totalgames
        if(carddeck.dealer.hand>21):
            print("Dealer busted -- Player Wins")
            playerwin += 1
            dealerlose += 1
        elif(carddeck.player.hand == 21) and (carddeck.dealer.hand == 21):
            if(len(carddeck.dealer.cards) == len(carddeck.player.cards)):
                print("Player hand and Dealer hand are equal. GAME DRAWN")
                draw += 1
            elif(len(carddeck.dealer.cards) > len(carddeck.player.cards)):
                print("Player hand and Dealer hand are equal. PLAYER won by the count of cards.")
                playerwin += 1
                dealerlose += 1
            else:
                print("Player hand and Dealer hand sare equal. Dealer won by the count of cards.") 
                dealerwin += 1
                playerlose += 1
        elif(carddeck.player.hand == carddeck.dealer.hand):
            if(len(carddeck.dealer.cards) == len(carddeck.player.cards)):
                print("Player hand and Dealer hand are equal. GAME DRAWN")
                draw += 1
            elif(len(carddeck.dealer.cards) > len(carddeck.player.cards)):
                print("Player hand and Dealer hand are equal. PLAYER won by the count of cards.")
                playerwin += 1
                dealerlose += 1
            else:
                print("Player hand and Dealer hand are equal. Dealer won by the count of cards.") 
                dealerwin += 1
                playerlose += 1
        elif self.dealer.hand < self.player.hand:
            print("Player wins")
            playerwin += 1
            dealerlose += 1
        elif self.dealer.hand > self.player.hand:
            dealerwin += 1
            playerlose += 1
            print("Dealer wins")
        else:
            draw +=1
            print("Draw")
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
        print("____________________________________________________________")
        print("\n** PLAYERS TURN  **")

    def playerTurn(self):
        global playerlose, playerwin, dealerwin, dealerlose, draw, totalgames
        gameStatus = False
        while True:
            choice=input("\nDo you want to Hit [Press H] or Stand [Press S]")
            if (choice == 'H' or choice ==  'h'):
                choice2 = input("Press + to add next card to total!! or Press - to subtract next card to total")
                self.player = self.hit(self.player, choice2)
                if(self.player == None):
                    self.log = log.Invalid_Choice_Interupption
                    gameStatus = True
                    print("\n**** Invalid Choice - GAME INTERRUPTED ****")
                    print("\n")
                    break
                if(self.player.hand > 21 or self.player.hand <= 1):
                    self.log = log.Player_Busted
                    gameStatus = True
                    print(self.player)
                    print(self.dealer)
                    dealerwin += 1
                    playerlose += 1
                    print("\nBusted the threshold - You Lost")
                    break
                elif(self.player.hand == 21):
                    gameStatus = True
                    print(self.player)
                    print(self.dealer)
                    if(self.dealer.hand == 21):
                        if(len(self.dealer.cards) == len(self.player.cards)):
                            self.log = log.Game_Drawn
                            draw += 1
                            print("Player hand and Dealer hand are equal.GAME DRAWN")
                        elif(len(self.dealer.cards) > len(self.player.cards)):
                            self.log = log.PLayer_Won
                            playerwin += 1
                            dealerlose += 1
                            break
                            print("Player hand and Dealer hand are equal. PLAYER WON by the count of cards.")
                        else:
                            self.log = log.Dealer_Won
                            dealerwin += 1
                            playerlose += 1
                            print("Player hand and Dealer hand are equal. DEALER WON by the count of cards.")
                        break
                    else:
                        self.log = log.PLayer_Won
                        playerwin += 1
                        dealerlose += 1
                        print("\nPlayer wins")
                        break
                else:
                    print(self.player)
                    print("____________________________________________________________")
            elif (choice == 'S' or choice =='s'):
                if(self.dealer.hand > self.player.hand):
                    print(self.player)
                    print(self.dealer)
                    gameStatus = True
                    self.log = log.Dealer_Won
                    dealerwin += 1
                    playerlose += 1
                break
            else:
                self.log = log.Invalid_Choice_Interupption
                gameStatus = True
                print("\n**** Invalid Choice - GAME INTERRUPTED ****")
                print("\n")
                break
        return gameStatus
    
    def dealerTurn(self):
        while(self.dealer.hand<=17):
            self.dealer.cards=np.append(self.dealer.cards,self.deck[0])
            self.dealer.cardsSign = np.append(self.dealer.cardsSign, +1)
            self.deck = self.deck[1:]
            self.dealer.hand = self.handValue(self.dealer)
        print(self.player)
        print(self.dealer)
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
    #choose num deck
    
    gamenum = 0
    while True:
        a = input("\nEnter an action: P: PLAY, Q:QUIT - ")
        if(a == "p" or a == "P"):
            print("**** GAME BEGINS ****")
            carddeck = BlackJack()
            gamenum += 1
            print("This is Game number", gamenum )
            b = input("Which AI do you want to play with? ")
            if(b == 'b'or b == "B"):
                #implementation of the hit function
                print("\n** PLAYERS TURN  **")
                totalgames += 1
                print("\nDeck:")
                print(carddeck.deck)

                print("\n......Dealing cards......")
                carddeck.AddDecks()
                print("\n....Shuffing the deck....")
                carddeck.deal()

                print(carddeck.player)
                print("\n __Dealer__:")
                print(carddeck.dealer.cards[0])
                print("____________________________________________________________")

                if not carddeck.playerTurn():
                    print("\n** DEALERS TURN **")
                    carddeck.dealerTurn()
                    if(carddeck.dealer.hand>21):
                        print("Dealer busted -- Player Wins")
                        playerwin += 1
                        dealerlose += 1
                    else:
                        carddeck.compare()
                
            elif(b == 't' or b =='T'):
                lc.treee()
            
        elif(a == 'q' or a=="Q"):
            break
        else:
            print("Invalid Choice. Please try again")
    print("Total Numbers of games played are ", totalgames)
    print("Total Numbers of player won are ", playerwin)
    print("Total Numbers of player lost are ", playerlose)
    print("Total Numbers of dealer won are ", dealerwin)
    print("Total Numbers of dealer lost are ", dealerlose)
    print("Total numbers of draw games are ", draw)
    print("Win percentage for player is ", ((playerwin/totalgames)*100))
    print("Lose percentage for player is ", ((playerlose/totalgames)*100))
    print("Win percentage for dealer is ", ((dealerwin/totalgames)*100))
    print("Lose percentage for dealer is ", ((dealerlose/totalgames)*100))
    plt.title("Blackjack basic AI graph")
    plt.ylabel("Total Games")
    plt.xlabel("Player win/Player lose/Dealer win/Dealer lose/ Draw")
    plt.ylim(None,totalgames)
    plt.hist(playerwin,color = 'red')
    plt.hist(playerlose,color = 'yellow')
    plt.hist(dealerwin,color = 'green')
    plt.hist(dealerlose,color = 'blue')
    plt.hist(draw,color = 'orange')
