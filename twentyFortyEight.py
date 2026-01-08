import numpy as np
import random as rand
import os
class game:
  def __init__(self):
    self.grid = np.zeros((4,4), dtype=int)
    self.score = 0
    self.moves = 0
  def spawnRandom(self):
    posPositions = np.count_nonzero(self.grid == 0)
    if posPositions == 0:
      quit()
    choosePosition = rand.randint(0, posPositions - 1)
    options = np.where(self.grid == 0)
    arraylocation = (options[0][choosePosition],options[1][choosePosition])
    newPiece = 2
    if rand.randint(1,4) == 1:
      newPiece = 4
    self.grid[arraylocation] = newPiece
  def updateDisplay(self):
    os.system('clear')
    print(self.grid)
    print("Score: ", self.score)
  def shiftGrid(self, direction, grid):
    scoreChange = 0
    if direction == "up":
      rot = 0
    elif direction == "down":
      rot = 2
    elif direction == "left":
      rot = -1
    elif direction == "right":
      rot = 1
    else:
      print("Invalid direction")
      quit()
    editGrid = np.rot90(grid.copy(), k=rot, axes=(0,1))
    for y in range(3):
      for x in range(4):
        if editGrid[(y,x)] != 0:
          for i in range(1,4-y):
            if editGrid[(y+i,x)] != 0:
              if editGrid[(y,x)] == editGrid[(y+i,x)]:
                editGrid[(y,x)] = 2 * editGrid[(y,x)]
                editGrid[(y+i,x)] = 0 
                scoreChange += editGrid[(y,x)]
              break
    for y in range(1,4):
      for x in range(4):
        if editGrid[(y,x)] != 0:
          moveTo = (y,x)
          for i in range(1,y+1):
            if editGrid[(y-i,x)] == 0:
              moveTo = (y-i,x)
            else:
              break
          editGrid[moveTo] = editGrid[(y,x)]
          if moveTo != (y,x):
            editGrid[(y,x)] = 0
    editGrid = np.rot90(editGrid.copy(), k=rot, axes=(1,0))
    return editGrid.copy(), scoreChange
  def gameShift(self, direction):
    preMove = self.grid.copy()
    self.grid, scoreChange = self.shiftGrid(direction, self.grid)
    if (self.grid == preMove).all():
      return False
    self.score += scoreChange
    self.moves += 1
    return True
  def fullGameOverCheck(self):
    directions = ["up","down","left","right"]
    fails = 0
    for i in directions:
      if (self.grid == self.shiftGrid(i, self.grid)[0]).all():
        fails += 1
    return fails == 4
  def runGame(self, moveKeys = {'w':"up", 'a':"left", 's':"down", 'd':"right"}):
    gameOver = False
    self.spawnRandom()
    while not(gameOver):
      self.updateDisplay()
      moveInput = input('Move: ')
      if not(moveInput in moveKeys.keys()):
        continue
      didChange = self.gameShift(moveKeys[moveInput])
      if not(didChange):
        continue
      self.spawnRandom()
      if np.count_nonzero(self.grid == 0) == 0:
        gameOver = self.fullGameOverCheck()
    self.updateDisplay()
    print("Moves: ", self.moves)
    print("GAMEOVER")