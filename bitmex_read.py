# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 20:12:29 2019

@author: EJ
"""

import csv
from datetime import date
import numpy as np   # python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
# from io import StringIO
import matplotlib.pyplot as plt



today = str(date.today().isoformat())
#today = "2019-06-11"
print(today)

###### read csv file and conversion to string/float data type
table = []
with open("test_{}.csv".format(today), newline='') as raw_table:
    raw = csv.reader(raw_table, delimiter = ',')
    headers = next(raw)
    table.append(headers)
    for line in raw:
        # print(line)
        # print(type(line))
        for i in range(2,len(line),1):
            if line[i] == "":
                line[i] = 0.
            else:
                 line[i] = float(line[i])   #read as float
        table.append(line)
            # print(line[i])
            # print(type(line[i]))
    raw_table.close()

for i in range(5):
    print(table[i])

def getTable(table, coin, column):
    new_table = []
    for i in range(len(table)):
        if table[i][1] == coin:
            new_table.append([table[i][0][0:19].replace('T',' ') , table[i][column]])
    return new_table

def getTableOHLCV(table, coin):
    new_table = []
    for i in range(len(table)):
        if table[i][1] == coin:
            new_table.append([table[i][0][0:19].replace('T',' ') , table[i][2], table[i][3], table[i][4], table[i][5], table[i][7] ])
    return new_table

def binaryTrans(table, columns):
    new_table = []
    for i in range(len(table)):
        temp = []
        temp.append( table[i][0] )
        for j in range(len(columns)) :
            if table[i][columns[j]] > 0 :
                temp.append(1)    # up = 1
            else :
                temp.append(0)    # down = 0
        new_table.append(temp)
    return new_table

def getTableRef(table):
    new_table = []
    for i in range(1,len(table)):
        new_table.append([ table[i][0] , 100 * (table[i][1]-table[i-1][1])/table[i-1][1] ])     # percentile move
    return new_table


def getColumnNum(table, name):
    for i in range(len(table[0])):
        if name == table[0][i]:
            return i
def tableMerge(table1, table2):
    length = min(len(table1),len(table2))
    table_new = []
    for i in range(length):
        if table1[i][0] == table2[i][0]:
            table_new.append([table1[i][0],table1[i][1],table2[i][1]])
    return table_new

def testValid(table):
    cut = round(0.7 * len(table))
    test = table[:cut]
    valid = table[-(len(table)-cut):]
    return [test,valid]

def writeCSV( filename , table ):
    with open("{}.csv".format(filename),'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(table)
    csvFile.close()
    # with open("C:/Users/EJ/tf/{}.csv".format(filename),'w', newline='') as csvFile:
    #     writer = csv.writer(csvFile)
    #     writer.writerows(table)
    # csvFile.close()


column = getColumnNum(table,'close')
coin_xbt = 'XBTUSD'
coin_eth = 'ETHUSD'

table_xbt = getTable(table, coin_xbt, column)
table_xbtOHLCV = getTableOHLCV(table, coin_xbt)
table_xbt_ref = getTableRef(table_xbt)
table_eth = getTable(table, coin_eth, column)
table_ethOHLCV = getTableOHLCV(table, coin_eth)
table_eth_ref = getTableRef(table_eth)
table_xbt_eth = tableMerge(table_xbt,table_eth)
table_xbt_eth_ref = tableMerge(table_xbt_ref,table_eth_ref)
table_xbt_eth_binary = binaryTrans(table_xbt_eth_ref,[1,2])

writeCSV(coin_xbt,table_xbt)
writeCSV('XBT_OHLCV',table_xbtOHLCV)
writeCSV(coin_eth,table_eth)
writeCSV('ETH_OHLCV',table_ethOHLCV)
writeCSV('XBTETH',table_xbt_eth)
writeCSV('XBTETH_return',table_xbt_eth_ref)
writeCSV('XBTETH_binary', table_xbt_eth_binary)


# data_xbt = table_xbt[1]
# data_xbt.plot(y='xbt')

# for i in range(5):
#     print(table_xbt[i])
for i in range(10):
    print(table_xbt_ref[i])
# for i in range(5):
    # print(table_eth[i])
for i in range(10):
    print(table_eth_ref[i])
# for i in range(5):
    # print(table_xbt_eth[i])
for i in range(10):
    print(table_xbt_eth_ref[i])

for i in range(10):
    print(table_xbt_eth_binary[i])

table_set = testValid(table_xbt_eth)
table_set_ref = testValid(table_xbt_eth_ref)

print(column, coin_xbt, len(table_xbt), len(table_eth), len(table),len(table_set[0]),len(table_set[1]))

print(table_xbtOHLCV[0:10])

###### calculation start

class NeuralNetwork:
    def __init__(self, x, y):
        self.input      = x
        self.weights1   = np.random.rand(self.input.shape[1],4)
        self.weights2   = np.random.rand(4,1)
        self.y          = y
        self.output     = np.zeros(y.shape)

    def feedforward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weights1))
        self.output = sigmoid(np.dot(self.layer1, self.weights2))

    def backprop(self):
        # application of the chain rule to find derivative of the loss function with respect to weights2 and weights1
        d_weights2 = np.dot(self.layer1.T, (2*(self.y - self.output) * sigmoid_derivative(self.output)))
        d_weights1 = np.dot(self.input.T,  (np.dot(2*(self.y - self.output) * sigmoid_derivative(self.output), self.weights2.T) * sigmoid_derivative(self.layer1)))

        # update the weights with the derivative (slope) of the loss function
        self.weights1 += d_weights1
        self.weights2 += d_weights2