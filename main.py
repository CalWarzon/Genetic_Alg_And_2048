import numpy as np
import twentyFortyEight as TFE
import networkBase as NB
import importExport as IE
import naturalEvolutionNetwork as NEN
import time as t
import matplotlib.pyplot as plt
import copy
from pathlib import Path
#aNet = NB.neuralNetwork((NB.denseLayer(16, 8), NB.tanh(8), NB.denseLayer(8, 4), NB.softmax(4)))
#bNet = NB.neuralNetwork((NB.denseLayer(16, 32), NB.tanh(32), NB.denseLayer(32, 16), NB.tanh(16), NB.denseLayer(16,4), NB.softmax(4)))
#cNet = NB.neuralNetwork((NB.denseLayer(240, 32), NB.tanh(32), NB.denseLayer(32, 16), NB.tanh(16), NB.denseLayer(16,4), NB.softmax(4)))
#dNet = NB.neuralNetwork((NB.denseLayer(240, 128), NB.tanh(128), NB.denseLayer(128, 64), NB.tanh(64), NB.denseLayer(64,32), NB.tanh(32), NB.denseLayer(32,16), NB.tanh(16), NB.denseLayer(16,4), NB.softmax(4)))
#environmentLog = NEN.twentyFortyEightEnvironment(False, "logOutput")
#environmentDiscrete = NEN.twentyFortyEightEnvironment(False, "discrete")
#a = NEN.naturalEvolutionNetwork(aNet, environmentLog, 64, 0.1, 0.2, 0.8, 0.05, 1)
#b = NEN.naturalEvolutionNetwork(bNet, environmentLog, 64, 0.1, 0.2, 0.8, 0.05, 1)
#c = NEN.naturalEvolutionNetwork(cNet, environmentDiscrete, 64, 0.1, 0.2, 0.8, 0.05, 1)
#d = NEN.naturalEvolutionNetwork(dNet, environmentDiscrete, 64, 0.1, 0.2, 0.8, 0.05, 1)

nets = [None, None, None, None]
name = ['logSmall', 'logBig', 'DiscreteSmall', 'DiscreteBig']
for i in range(4):
  nets[i] = IE.importObject(name[i])
#size = [1, 5, 10, 20, 30, 50]
colors = ['red', 'blue', 'green', 'orange']
#for i in zip(nets, name):
  #print(i[1])
  #print('1 round')
  #i[0].runEvolution(50, 5, 1)
  #print('5 rounds')
  #i[0].runEvolution(5, 1, 15)
  #print('10 rounds')
  #i[0].runEvolution(10, 2, 10)
  #i[0].runEvolution(5, 1, 20)
for i in zip(nets, name, colors):
  plt.plot(range(len(i[0].meanScores)), i[0].meanScores, color = i[2], label = i[1])
plt.legend()
plt.show()
#for i in  zip(nets, name):
  #IE.exportObject(i[0], i[1])
