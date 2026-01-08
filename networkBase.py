import numpy as np
class neuralNetwork:
  def __init__(self, layers):
    self.layers = layers
  def forward(self, input):
    self.input = input
    self.output = input
    for i in self.layers:
      self.output = i.forward(self.output)
    return self.output
  def randomize(self):
    for i in self.layers:
      i.randomize()
  def extractGenome(self):
    genes = []
    for i in self.layers:
      genes.append(i.extractGenome())
    return genes
  def updateGenome(self, genes):
    for i in range(len(genes)):
      self.layers[i].updateGenome(genes[i])
class denseLayer:
  def __init__(self, inputsize, outputsize):
    self.outputsize = outputsize
    self.inputsize = inputsize
    self.randomize()
  def forward(self, input):
    self.input = input
    self.output = np.dot(self.weights, input) + self.biases
    return self.output
  def randomize(self):
    self.weights = np.random.randn(self.outputsize, self.inputsize)
    self.biases = np.random.randn(self.outputsize, 1)
  def extractGenome(self):
    return np.concatenate((np.reshape(self.weights,(self.weights.size)), np.reshape(self.biases, (self.biases.size))))
  def updateGenome(self, genes):
    self.weights = genes[:self.weights.size].reshape(self.outputsize, self.inputsize)
    self.biases = genes[self.weights.size:].reshape(self.outputsize, 1)
class activationLayer:
  def __init__(self, inputsize, calculation):
    self.inputsize = inputsize
    self.calculation = calculation
  def forward(self, input):
    self.input = input
    self.output = self.calculation(input)
    return self.output
  def randomize(self):
    pass
  def extractGenome(self):
    return np.array([])
  def updateGenome(self, genes):
    pass
class sigmoid(activationLayer): 
  def __init__(self, inputsize):
    calculation = lambda x: 1 / (1 + np.exp(-x))
    super().__init__(inputsize, calculation)
class ReLU(activationLayer):
  def __init__(self, inputsize):
    calculation = lambda x: np.maximum(0, x)
    super().__init__(inputsize, calculation)
class tanh(activationLayer):
  def __init__(self, inputsize):
    calculation = np.tanh
    super().__init__(inputsize, calculation)
class softmax(activationLayer):
  def __init__(self, inputsize):
    calculation = lambda x: np.exp(x) / np.sum(np.exp(x))
    super().__init__(inputsize, calculation)
class leakyReLU(activationLayer):
  def __init__(self, inputsize):
    calculation = lambda x: np.maximum(0.1*x, x)
    super().__init__(inputsize, calculation)
class swish(activationLayer):
  def __init__(self, inputsize):
    calculation = lambda x: x / (1 + np.exp(-x))
    super().__init__(inputsize, calculation)