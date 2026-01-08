import numpy as np
import random as rand
import math as m
import time as t
from numpy._core.fromnumeric import argmax
import networkBase as NB
import twentyFortyEight as TFE
import copy
class twentyFortyEightEnvironment:
  def __init__(self, killOnWalls = False, outputType = 'direct'):
    self.killOnWalls = killOnWalls
    self.outputType = outputType
    self.numberToMove = {0: "up", 1: "down", 2: "left", 3: "right"}
  def start(self, show = False):
    self.game = TFE.game()
    self.game.spawnRandom()
    if show:
      self.game.updateDisplay()
    return self.formatOutput(self.game.grid)
  def input(self, input, show = False):
    didChange = False
    end = False
    inputUp = input
    while not(didChange):
      definiteInput = np.random.multinomial(1, inputUp.flatten())
      inputNumber = np.argmax(definiteInput)
      move = self.numberToMove[inputNumber]
      didChange = self.game.gameShift(move)
      if not(didChange):
        if self.killOnWalls:
          end = True
          return self.formatOutput(self.game.grid), self.game.score, end
        inputUp[inputNumber] = 0
        if (inputUp == 0).all():
          end = True
          return self.formatOutput(self.game.grid), self.game.score, end
        inputUp = inputUp/sum(inputUp)
    self.game.spawnRandom()
    if np.count_nonzero(self.game.grid == 0) == 0:
      end = self.game.fullGameOverCheck()
    if show:
      self.game.updateDisplay()
    return self.formatOutput(self.game.grid), self.game.score, end
  def formatOutput(self, output):
    formOutput = np.zeros((16,1))
    output = np.reshape(output, (16,1))
    if self.outputType == 'direct':
      formOutput = output
    elif self.outputType == 'discrete':
      formOutput = np.zeros((16,15))
      for i in range(16):
        if output[i] == 0:
          formOutput[i,0] = 1
        else:
          formOutput[(i,int(m.log(output[i],2)))] = 1
      formOutput = np.reshape(formOutput, (240, 1))
    elif self.outputType == 'logOutput':
      
      for i in range(16):
        if output[i] == 0:
          formOutput[i] = 0 
        else:
          formOutput[i] = m.log(output[i],2)
    return formOutput
class naturalEvolutionNetwork:
  def __init__(self, 
               decisionNetwork, 
               environment, 
               populationSize, 
               survivorPercentile, 
               parentPrecentile, 
               crossoverPercent, 
               mutationRate, 
               mutationRange):
    self.decisionNetwork = decisionNetwork
    self.environment = environment
    self.populationSize = populationSize
    self.survivorCount = round(survivorPercentile * populationSize)
    self.parentCount = round(parentPrecentile * populationSize)
    self.crossoverCount = round((self.populationSize -self.survivorCount) * crossoverPercent)
    self.mutationCount = self.populationSize - (self.crossoverCount + self.survivorCount)
    self.mutationRate = mutationRate
    self.mutationRange = mutationRange
    self.mutationStDev = mutationRange/6
    self.meanScores = []
    self.maxScores = []
    self.population = []
    for i in range(self.populationSize):
      self.decisionNetwork.randomize()
      agent = copy.deepcopy(self.decisionNetwork)
      self.population.append(agent)
    self.population = np.array(self.population)
  def createAgentFromGenome(self, genome):
    agent = copy.deepcopy(self.decisionNetwork)
    agent.updateGenome(genome)
    return agent
  def crossoverGenome(self, parent1genome, parent2genome):
    childGenome = []
    for chromosomePair in zip(parent1genome, parent2genome):
      conectedChromosomePair = zip(chromosomePair[0], chromosomePair[1])
      childChromosome = []
      for genePair in conectedChromosomePair:
        childChromosome.append(rand.choice(genePair))
      childGenome.append(np.array(childChromosome))
    return childGenome
  def createCrossOverChildren(self, parents):
    children = []
    parentGenomes = [None, None]
    parentindex =[0,0]
    for i in range(self.crossoverCount):
      parentpool = parents.copy()
      for j in range(2):
        parentindex[j] = np.random.randint(0, parentpool.size)
        parentGenomes[j] = parentpool[parentindex[j]].extractGenome()
        parentpool = np.delete(parentpool, parentindex[j])
      childGenome = self.crossoverGenome(parentGenomes[0], parentGenomes[1])
      child = self.createAgentFromGenome(childGenome)
      children.append(child)
    return np.array(children)
  def createMutantChildren(self, parents):
    children = []
    for i in range(self.mutationCount):
      parent = parents[np.random.randint(0, parents.size)]
      childGenome = parent.extractGenome()
      for chromosomeNumber in range(len(childGenome)):
        for geneNumber in range(len(childGenome[chromosomeNumber])):
          mutateGene = bool(argmax(1 - np.random.multinomial(1,[self.mutationRate, self.mutationRate])))
          if mutateGene:
            mutation = np.random.normal(0, self.mutationStDev)
            childGenome[chromosomeNumber][geneNumber] += mutation
      child = self.createAgentFromGenome(childGenome)
      children.append(child)
    return np.array(children)
  def runGeneration(self):
    self.scores = []
    for agent in self.population:
      agentScores = []
      for i in range(self.attemptsPerAgent):
        agentScore = self.runAgent(agent)
        agentScores.append(agentScore)
      score = np.mean(agentScores)
      self.scores.append(score)
    self.scores = np.array(self.scores)
    self.maxScores.append(np.max(self.scores))
    self.meanScores.append(np.mean(self.scores))
  def runAgent(self, agent, show = False):
    output = self.environment.start(show = show)
    done = False
    agentScore = 0
    while not(done):
      action = agent.forward(output)
      output, agentScore, done = self.environment.input(action, show = show)
      if show:
        t.sleep(0.1)
    return agentScore
  def createNewGeneration(self):
    self.population = self.population[np.argsort(self.scores)]
    survivors = self.population[-self.survivorCount:]
    parents = self.population[-self.parentCount:]
    crossovers = self.createCrossOverChildren(parents)
    mutants = self.createMutantChildren(parents)
    newGeneration = np.concatenate((survivors, crossovers, mutants))
    return newGeneration
  def runEvolution(self, generations, generationsPerUpdate, attemptsPerAgent = 1):
    self.attemptsPerAgent = attemptsPerAgent
    generation = 0
    for i in range(generations):
      generation += 1
      self.runGeneration()
      self.population = self.createNewGeneration()
      if generation % generationsPerUpdate == 0:
        print("Generation: " + str(generation) + " Mean Score: " + str(self.meanScores[-1]), " Max Score: ", str(self.maxScores[-1]))