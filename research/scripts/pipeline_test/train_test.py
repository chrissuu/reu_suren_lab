import torch
import torch.nn as nn
import torch.optim as optim
from torcheval.metrics.functional import binary_auprc
from utils import *

def train(criterion1, criterion2, optimizer, net, num_epochs, dldr_trn):
    for epoch in range(num_epochs):  # loop over the dataset multiple times
        print("epoch {epoch}".format(epoch=epoch))
        running_loss = 0.0
        for i, data in enumerate(dldr_trn, 0):
            # get the inputs; data is a list of [inputs, labels]
        
            inputs, labels = data
            print(f"inputs shape: {inputs.shape}")
            inputs = torch.log10(torch.tensor(inputs).transpose(1,3) + 1)
            # print(inputs.shape)
            labels = torch.tensor(labels)
            # zero the parameter gradients
            optimizer.zero_grad()

            # print(inputs)
            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion1(outputs, labels.reshape(20,1).type(torch.float32))
            if criterion2: 
                loss += criterion2(curly_Nprime(net.vhn.weights), \
                                curly_N(torch.sum(inputs, dim = 0) \
                                        / dldr_trn.batch_size))
            # print("netvhn", net.vhn.weights.shape)
            # print(curly_N(torch.sum(inputs, dim = 0) / dldr.batch_size).shape)
       
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            
            # if i % 5 == 4:    # print every 2000 mini-batches
            #     print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 5:.3f}')
              
            #     running_loss = 0.0

    return

def test(net, dldr_tst):
    preds = []
    labels = []
    # imax = []


    with torch.no_grad():
        for i, data in enumerate(dldr_tst,0):
            inputs, label = data
            
            inputs = torch.log10(torch.tensor(inputs).transpose(1,3) + 1)
            # print(inputs.shape)
            label = torch.tensor(label)
            # calculate outputs by running images through the 
            output = net(inputs)

            preds.append(output.tolist())
            labels.append(label.tolist())
            # imax.append(i)
            # print(inputs.shape)

    # print(f"num_test {i}".format(i = max(imax)))

    return "PRAUC" + str(binary_auprc(torch.tensor(preds).squeeze(0).squeeze(2), \
           torch.tensor(labels), num_tasks=len(preds)).mean())