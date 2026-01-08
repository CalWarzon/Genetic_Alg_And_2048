import dill
def importObject(filename):
  with open(filename, 'rb') as dillFile:
   object = dill.load(dillFile)
  return object
def exportObject(object, filename):
  with open(filename, 'wb') as dillFile:
    dill.dump(object, dillFile)