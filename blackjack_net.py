"""
This file and its tests are individualized for NetID sakaur.
"""
import numpy as np
import torch as tr
import matplotlib.pyplot as pt
import pickle as pk
from blackjack_data import encode
from torch.nn import Sequential, Conv2d, Linear, Flatten, LeakyReLU, Tanh

def BlackjackNet1():
    model = Sequential(
            Flatten(),
            Linear(4*13*4,1)
        )
    return model

def calculate_loss(net, x, y_targ):
    y = net(x)
    return y,tr.sum(tr.square(tr.sub(y,y_targ)))

def optimization_step(optimizer, net, x, y_targ):
    optimizer.zero_grad()
    y,e = calculate_loss(net, x, y_targ)
    e.backward()
    optimizer.step()
    return (y,e)

def neuralnet(num_decks):

    net = BlackjackNet1()
    print(net)
    
    with open("data%d.pkl" % num_decks,"rb") as f: (x, y_targ) = pk.load(f)

    # Optimization loop
    optimizer = tr.optim.Adam(net.parameters())
    train_loss, test_loss = [], []
    shuffle = np.random.permutation(range(len(x)))
    split = 10
    train, test = shuffle[:-split], shuffle[-split:]
    for epoch in range(100):
        y_train, e_train = optimization_step(optimizer, net, x[train], y_targ[train])
        y_test, e_test = calculate_loss(net, x[test], y_targ[test])
        #if epoch % 10 == 0: print("%d: %f (%f)" % (epoch, e_train.item(), e_test.item()))
        train_loss.append(e_train.item() / (len(shuffle)-split))
        test_loss.append(e_test.item() / split)
    
    tr.save(net.state_dict(), "model%d.pth" % num_decks)
    
    pt.plot(train_loss,'b-')
    pt.plot(test_loss,'r-')
    pt.legend(["Train","Test"])
    pt.xlabel("Iteration")
    pt.ylabel("Average Loss")
    pt.title("Game Size "+str(num_decks)+" Average Loss over the iteration")
    pt.show()
    
    pt.plot(y_train.detach().numpy(), y_targ[train].detach().numpy(),'bo')
    pt.plot(y_test.detach().numpy(), y_targ[test].detach().numpy(),'ro')
    pt.legend(["Train","Test"])
    pt.xlabel("Actual output")
    pt.ylabel("Target output")
    pt.title("Game Size "+str(num_decks)+" Actual vs Target")
    pt.show()

if __name__ == "__main__":
    neuralnet(1)
    neuralnet(2)
    neuralnet(3)
    neuralnet(4)
    neuralnet(5)

    

