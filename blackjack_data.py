"""
This file is individualized for NetID mkannaia.
"""
import torch as tr
import numpy as np
import pickle as pk
from Play_blackjack import BlackJack, GameStatus, log, deck_lookup
from BlackJackState import decision, State
from TreeSearch import Node, puct, decide_action


def generate(num_games=2, gamesize = 1, num_rollouts=10, max_depth=4, choose_method=None):
    if choose_method is None: choose_method = puct
    data = []
    for i in range(num_games):
        print("\n\n Game"+str(i+1))
        game = BlackJack(gamesize)
        game.beginGame()
        game.playerTurn()
        state = State(game = game)
        node = Node(state = state)
        while game.log == log.Unfinished_Game:
            if node.state.isLeaf: break
            a, n, nump = decide_action(node.state,choose_method=puct, num_rollouts=100, max_depth = 10, verbose=True)
            state = n.children()[a].state
            Q = n.get_score_estimates()
            for c,child in enumerate(n.children()):
                    data.append((child, Q[c]))
            if(state.childAction == decision.PositiveHit):
                game.hit(member = game.dealer,sign="+")
            elif(state.childAction == decision.NegativeHit):
                game.hit(member = game.dealer,sign="-")
            else:
                game.stand()
                print(game)
                break
            state = State(game = game)
            node = Node(state = state)
            print(game)
    return data

def encode(node):
    gameEncode = np.zeros((4,13,4), dtype = 'float32')
    p = (np.array(node.state.state.player.cards).reshape(len(node.state.state.player.cards),1,1) == deck_lookup) #Encode player cards
    ps = np.sum(p * np.array(node.state.state.player.cardsSign).reshape(len(node.state.state.player.cards),1,1), axis=0) #Encode player cards Sign
    gameEncode[2,:,:] = np.sum(p, axis =0) # Add to encoding state
    d = (np.array(node.state.state.dealer.cards).reshape(len(node.state.state.dealer.cards),1,1) == deck_lookup) #Encode delaer cards
    ds = np.sum(d * np.array(node.state.state.dealer.cardsSign).reshape(len(node.state.state.dealer.cards),1,1), axis=0) #Encode dealer cards sign
    gameEncode[1,:,:] = np.sum(d, axis =0) # Add to encoding state
    deck =np.abs(node.state.state.numDecks - gameEncode[1,:,:] - gameEncode[2,:,:]) #Deck cards encoding
    gameEncode[0,:,:] = deck
    a = ps+ds
    if(node.state.childAction == decision.PositiveHit):
        gameEncode[3,:,:] = np.where(a == 0,node.state.state.numDecks, a)
        #gameEncode[3,:,:] = ps+ds
    elif(node.state.childAction == decision.NegativeHit):
        gameEncode[3,:,:] = np.where(a == 0,node.state.state.numDecks*(-1), a)
    else:
        gameEncode[3,:,:] = ps+ds
    return tr.tensor(gameEncode)

def get_batch(num_games=50, gamesize=1, num_rollouts=100, max_depth=10, choose_method=None):
    data = generate(num_games, gamesize, num_rollouts, max_depth, choose_method)
    inputs = tr.zeros(len(data))
    inputs_tr = []
    outputs = tr.zeros(len(data),1)
    for i,d in enumerate(data):
        inputs_tr.append(encode(d[0]))
        outputs[i] = d[1]
    inputs = tr.stack(inputs_tr)
    return inputs,outputs


if __name__ == "__main__":
    
    num_games = 50
    # Genearting Data
    #1
    inputs, outputs = get_batch(num_games= num_games, gamesize=1)
    with open("data1.pkl", "wb") as f: pk.dump((inputs, outputs), f)

    #2
    inputs, outputs = get_batch(num_games= num_games, gamesize=2)
    with open("data2.pkl", "wb") as f: pk.dump((inputs, outputs), f)

    #3
    inputs, outputs = get_batch(num_games= num_games, gamesize=3)
    with open("data3.pkl", "wb") as f: pk.dump((inputs, outputs), f)

    #4
    inputs, outputs = get_batch(num_games= num_games, gamesize=4)
    with open("data4.pkl", "wb") as f: pk.dump((inputs, outputs), f)

    #5
    inputs, outputs = get_batch(num_games= num_games, gamesize=5)
    with open("data5.pkl", "wb") as f: pk.dump((inputs, outputs), f)

