import numpy as np
import random
#Initialize the required variables

#groups of deck in cards:
groups = np.array(["_Clubs", "_Diamonds", "_Hearts", "_Spade"], dtype=str)
value = np.array(["2","3","4","5","6","7","8","9","10","J","Q","K","A"],dtype=str).reshape(13,1)
deck_lookup = np.char.add(value,groups)
global player_sum, dealer_sum


class BlackJack():
    def __init__(self):
        self.deck = deck_lookup.flatten()
        self.dealerCards = []
        self.dealerCardsSign = [+1,+1]
        self.playerCards = []
        self.playerCardsSign = [+1,+1]
        self.playerHand = 0
        self.dealerHand = 0
        #self.__threshold = threshold
        #1.deck , 2.dealer, 3.player, 4.sign
        self.gameStatus = np.full((4,13,4),0)

    def __shuffleDeck(self):
        random.shuffle(self.deck)
    
    def deal(self):
        self.__shuffleDeck()
        #print("\nDeck after shuffing:")
        #print(self.deck)
        self.dealerCards = self.deck[0:4:2]
        self.playerCards = self.deck[1:4:2]
        self.deck = self.deck[4:]
        self.PlayerHand()
        self.DealerHand()

    
    def face_value(self): #adding values to face cards such as jack,queen,king are 10 and remaining cards obtain same value as written on card except ace
        value = {'2': 2,'3' : 3,'4' : 4,' 5' : 5,'6' : 6,'7' : 7,'8' : 8,'9' : 9,'10' : 10,'J' : 10,'Q' : 10,'K' : 10} #creating a dictionary
        return value
    
    def ace_val(self,current_sum, sign): #determining whether ace needs to be 1 or 11
        if(sign == +1):
            if(current_sum+11 <= 21):
                return 11
            return 1
        elif(sign == -1):
            if(current_sum >= 12):
                return -11
            return -1

    def restart(self):
        self.deck = deck_lookup.flatten()
        self.dealerCards = []
        self.playerCards = []
        self.playerHand = 0
        self.dealerHand = 0
        #1.deck , 2.dealer, 3.player, 4.sign
        self.gameStatus = np.full((13,4,4),0)
    
    def PlayerHand(self):
        x = zip(np.sort(self.playerCards), np.argsort(self.playerCards))
        self.playerHand = 0
        for i,j in x:
            if i[0].isnumeric() & (i[0] != '1'):
                self.playerHand += int(i[0])*self.playerCardsSign[j]
            elif i[0] == 'A':
                self.playerHand += self.ace_val(self.playerHand,self.playerCardsSign[j])
            else:
                self.playerHand += 10*self.playerCardsSign[j]

    def DealerHand(self):
        x = zip(np.sort(self.dealerCards), np.argsort(self.dealerCards))
        self.dealerHand = 0 
        for i,j in x:
            if i[0].isnumeric() & (i[0] != '1'):
                self.dealerHand += int(i[0])*self.dealerCardsSign[j]
            elif i[0] == 'A':
                self.dealerHand += self.ace_val(self.dealerHand,self.dealerCardsSign[j])
            else:
                self.dealerHand += 10*self.dealerCardsSign[j]
    
    #each turn, player gets asked whether they want to add or subtract the next card value before the next card is dealt. If its above 21, automatically busts, if not keep going until stand or bust
    def hit(self):
      choice2 = input("Press + to add next card to total!! or Press - to subtract next card to total")
      if choice2 == '+':
        self.playerCards=np.append(self.playerCards,self.deck[0])
        self.playerCardsSign = np.append(self.playerCardsSign, +1)
        self.deck = self.deck[1:]
        self.PlayerHand()
        return 1
      elif choice2 == '-':
        self.playerCards=np.append(self.playerCards,self.deck[0])
        self.playerCardsSign = np.append(self.playerCardsSign, -1)
        self.deck = self.deck[1:]
        self.PlayerHand()
        return 1
      return 0
  
    def stand(self): #no more hits on players card
        return self.compare() 
    
    def bust(self):
      if self.playerHand>21:
        return "player Busted"
      elif self.dealerHand>21:
        return "Dealer Busted"
      
    def compare(self): #compare player and dealers card value to determine who wins
        if self.dealerHand < self.playerHand:
        	print("Player wins")
        elif self.dealerHand > self.playerHand:
        	print("Dealer wins")
        else:
        	print("Draw")
        self.restart()
        return 
     

if __name__ == "__main__":
    print("**** GAME BEGINS ****")
    #threshold = input("Please select your threshold or Press any alphabet key for Default value of 21")
    #if(threshold.isnumeric() & )
    carddeck = BlackJack()
    print("\nDeck:")
    print(carddeck.deck)
    print("\n......Dealing cards......")
    print("\n....Shuffing the deck....")
    carddeck.deal()
    #print("\nDealer Cards:")
    #print(carddeck.dealerCards) #better if player doesn't know what cards the dealer has
    print("\nPlayer Cards:")
    print(carddeck.playerCards)
    #print(carddeck.face_value())
    print("\n Player Score :",carddeck.playerHand)
    print("\n Dealer Cards:")
    print(carddeck.dealerCards[0])
    print("____________________________________________________________")
    #print(carddeck.dealerCards)
    # print("\nDeck after Dealing: ")
    # print(carddeck.deck) #not necessary to show the deck after deck is dealt.

    #implementation of the hit function
    while True:
        choice=input("\nDo you want to Hit [Press H] or Stand [Press S]")
        if choice == ('H' or 'h'):
            hitVal = carddeck.hit()
            if(hitVal == 0):
                print("\n**** Invalid Choice - GAME INTERRUPTED ****")
                print("\n")
                break
            if(carddeck.playerHand > 21 or carddeck.playerHand <= 1):
                print("\nPlayer Cards:", carddeck.playerCards)
                print("\nPlayer score:", carddeck.playerHand)
                print("\nDealer Cards:", carddeck.dealerCards)
                print("\nDealer SCore:", carddeck.dealerHand)
                print("\nBusted the threshold - You Lost")
                break
            elif(carddeck.playerHand == 21):
                print("\nPlayer Cards:", carddeck.playerCards)
                print("\nPlayer score:", carddeck.playerHand)
                print("\nDealer Cards:", carddeck.dealerCards)
                print("\nDealer SCore:", carddeck.dealerHand)
                if(carddeck.dealerHand == 21):
                    if(len(carddeck.dealerCards) == len(carddeck.playerCards)):
                        print("Player hand and Dealer hand are equal.GAME DRAWN")
                    elif(len(carddeck.dealerCards) > len(carddeck.playerCards)):
                        print("Player hand and Dealer hand are equal. DEALER WON by the count of cards.")
                    else:
                        print("Player hand and Dealer hand are equal. PLAYER WON by the count of cards.")
                else:
                    print("\nPlayer wins")
                break
            else:
                print("\nPlayer Cards:", carddeck.playerCards)
                print("\nPlayer score:", carddeck.playerHand)
        elif choice == ('S' or 's'):
            print("\nPlayer Cards:", carddeck.playerCards)
            print("\nPlayer score:", carddeck.playerHand)
            print("\nDealer Cards:", carddeck.dealerCards)
            print("\nDealer SCore:", carddeck.dealerHand)
            carddeck.stand()
            break
        else:
            print("\n**** Invalid Choice - GAME INTERRUPTED ****")
            print("\n")
            break
        print("____________________________________________________________")
