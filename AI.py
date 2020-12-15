import torch as tr
import numpy as np 
from Play_blackjack import deck_lookup, BlackJack, log
from BlackJackState import State, decision
from TreeSearch import Node, puct, decide_action
from blackjack_net import BlackjackNet1
from blackjack_data import encode

net = BlackjackNet1()

def nn_puct(node):
    with tr.no_grad():
        x = tr.stack(tuple(map(encode, [child for child in node.children()])))
        y = net(x)
        probs = tr.softmax(y.flatten(), dim=0)
        a = np.random.choice(len(probs), p=probs.detach().numpy())
    return node.children()[a]



if __name__ == "__main__":
    #Problem size
    while True:
        try:
            gameSize = int(input("Enter the number of decks(1-5):"))
            if(gameSize >=1 and gameSize<=5): break
            else:print("Invalid input. Please try again")
        except ValueError:
            print("Invalid input. Please enter an integer")
    while True:
        a = input("\nEnter an action: P: PLAY, Q:QUIT - ")
        if(a == "p" or a == "P"):
            bj = BlackJack(gameSize)
            bj.beginGame()
            bj.playerTurn()
            state = State(game = bj)
            node = Node(state = state)
            AI = ""
            nodesPros = 0
            net.load_state_dict(tr.load("model%d.pth" % gameSize))
            #Choice of AI
            while bj.log == log.Unfinished_Game:
                AI = input("Choose an AI: B: Baseline AI, T: Tree-based, N: Tree+NN - ")
                if(AI == "T" or AI == "t" or AI == "B" or AI == "b"or AI == "N"or AI == "n"): break
                print("Please enter a valid input")

            while(bj.log == log.Unfinished_Game):
                #Baseline AI
                if(AI == "B" or AI == "b"):
                    bj.dealerTurn()
                    bj.compare()
                    #print(bj.gameStatus.name)
                    break
                #Tree-Based
                elif(AI == "T" or AI == "t"):
                    # Stop when game is over
                    if node.state.isLeaf:
                        break
                    a, n, nump = decide_action(node.state,choose_method=puct, num_rollouts=1000, max_depth = 10, verbose=True)
                    state = n.children()[a].state
                    nodesPros += nump
                    print("\nNumber of nodes processed for this turn: ",nump)
                    if(state.childAction == decision.PositiveHit):
                        bj.hit(member = bj.dealer,sign="+")
                    elif(state.childAction == decision.NegativeHit):
                        bj.hit(member = bj.dealer,sign="-")
                    else:
                        bj.stand()
                        print(bj)
                        break
                    state = State(game = bj)
                    node = Node(state = state)
                    print(bj)
                    continue
                #Tree + NN
                else:
                    if node.state.isLeaf:
                        break
                    a, n, nump = decide_action(node.state,choose_method=nn_puct, num_rollouts=1000, max_depth = 10, verbose=True)
                    state = n.children()[a].state
                    #print("\nNumber of Processed nodes: ",nump)
                    if(state.childAction == decision.PositiveHit):
                        bj.hit(member = bj.dealer,sign="+")
                    elif(state.childAction == decision.NegativeHit):
                        bj.hit(member = bj.dealer,sign="-")
                    else:
                        bj.stand()
                        print(bj)
                        break
                    state = State(game = bj)
                    node = Node(state = state)
                    print(bj)
                    continue
            if(AI == "T" or AI == "t"): print("Number of nodes processed over the course of game: ", nodesPros)
            print(bj.gameStatus.name)
        elif(a == 'q' or a=="Q"):
            break
        else:
            print("Invalid Choice. Please try again")
    #print(bj.log.value)
