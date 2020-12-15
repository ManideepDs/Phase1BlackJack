"""
This file and its tests are individualized for NetID mkannaia.
"""
import torch as tr
import numpy as np 
from Play_blackjack import deck_lookup, BlackJack, log
from BlackJackState import State, decision

"""
from blackjack_net import BlackjackNet1
from blackjack_data import encode
def nn_puct(node, net):
    with tr.no_grad():
        x = tr.stack(tuple(map(encode, [child for child in node.children()])))
        y = net(x)
        probs = tr.softmax(y.flatten(), dim=0)
        a = np.random.choice(len(probs), p=probs.detach().numpy())
    return node.children()[a]
"""

def uniform(node):
    c = np.random.choice(len(node.children()))
    return node.children()[c]

def puct(node):
    c = np.random.choice(len(node.children()), p=puct_probs(node))
    return node.children()[c]

def puct_probs(node):
    probs = []
    n = node.get_visit_counts()
    q = node.get_score_estimates()
    probs  = np.exp(q + np.power(np.divide(np.log(node.visit_count+1),n+1),0.5))
    return(np.divide(probs,sum(probs)))
    #raise(NotImplementedError)

class Node(object):
    def __init__(self, state, depth = 0, choose_method=uniform):
        self.state = state
        self.child_list = None
        self.visit_count = 0
        self.score_total = 0
        self.depth = depth
        self.visited = False
        self.choose_method = choose_method

    def make_child_list(self):
        self.child_list = []
        actions = self.state.validAction()
        #print(self.state)
        #print(actions)
        for i in actions:
            if(self.state.turn == 2):
                deck = deck_lookup.flatten().tolist()
                rmv_list = np.append(self.state.state.player.cards,self.state.state.dealer.cards).tolist()
                deck = [i for i in deck if i not in rmv_list]
                for j in deck:
                    child_state = self.state.PerformAction(action = i, card = j)
                    #print(child_state)
                    child_node = Node(state= child_state, depth=self.depth+1, choose_method= self.choose_method)
                    self.child_list.append(child_node)
            else:
                child_state = self.state.PerformAction(i)
                child_node = Node(state= child_state, depth=self.depth+1, choose_method= self.choose_method)
                self.child_list.append(child_node)

    def children(self):
        #print("Enters here")
        if self.child_list is None: self.make_child_list()
        return self.child_list

    def get_score_estimates(self):
        Q = []
        for i in self.child_list:
            if(i.visit_count == 0):
                Q.append(0)
            else:
                Q.append(i.score_total/i.visit_count)
        return np.array(Q)

    def get_visit_counts(self):
        N=[]
        for i in self.child_list:
            N.append(i.visit_count)
        return np.array(N)

    def choose_child(self):
        return self.choose_method(self)

def rollout(node, max_depth=None):
    if node.depth == max_depth or node.state.isLeaf:
        result = node.state.state.score
    else:
        result = rollout(node.choose_child(), max_depth)
    node.visit_count += 1
    node.score_total += result
    node.visited = True
    return result

def processedNodes(node, max_depth):
    result = 0
    if node.depth == max_depth or node.state.isLeaf:
        if node.visited: return 1
        else: return 0
    elif node.child_list is not None:
        for i in node.child_list:
            result += processedNodes(i, node.depth)
    else:
        return 0
    return result+1 # +1 for Root node 

def decide_action(state, num_rollouts, choose_method=puct, max_depth=None, verbose=False):
    node = Node(state, choose_method=choose_method)
    for n in range(num_rollouts):
        if verbose and n % 100 == 0: print("Rollout %d of %d..." % (n+1, num_rollouts))
        rollout(node, max_depth=max_depth)
    #print(node.get_score_estimates())
    return np.argmax(node.get_score_estimates()), node, processedNodes(node,max_depth)

if __name__ == "__main__":
    #Problem size
    while True:
        try:
            gameSize = int(input("Enter the number of decks:"))
            break
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
            #net = BlackjackNet1(gameSize)
            #net.load_state_dict(tr.load("model%d.pth" % gameSize))
            #Choice of AI
            while bj.log == log.Unfinished_Game:
                AI = input("Choose an AI: B: Baseline AI, T: Tree-based - ")
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
                    print("\nNumber of Processed nodes: ",nump)
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
                """
                else:
                    if node.state.isLeaf:
                        break
                    a, n, nump = decide_action(node.state,choose_method=nn_puct, num_rollouts=1000, max_depth = 10, verbose=True)
                    state = n.children()[a].state
                    print("\nNumber of Processed nodes: ",nump)
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
                """
            print(bj.gameStatus.name)
        elif(a == 'q' or a=="Q"):
            break
        else:
            print("Invalid Choice. Please try again")
    #print(bj.log.value)