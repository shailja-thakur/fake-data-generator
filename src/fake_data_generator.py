'''
Created on Mar 7, 2012

@author: anorberg
'''
from __future__ import division

from fakeDataGenerator import model
from fakeDataGenerator import config
import csv
import random


def shuffle(thisList):
    for x in range(len(thisList)-1):
        dex = random.randint(x, len(thisList) - 1)
        thisList[x], thisList[dex] = thisList[dex], thisList[x]
    return thisList #yes, it's a mutator, but let's also return it
        
def weldGraphViz(gvStrList):
    joinme = [gvStrList[0][:-1]] #strip trailing }
    for x in range(1, len(gvStrList) - 1):
        joinme.append(gvStrList[x][8:-1]) #strip leading digraph{ and trailing }
    joinme.append(gvStrList[-1][8:]) #strip leading digraph{
    return "".join(joinme) #weld

if __name__ == '__main__':
    settings = config.Config() #uses sys.argv
    
    model.graphviz_recursion_depth = settings.gvRecursion
    
    graphvizModels = []
    nodeBucket = []
    
    for prefixChar in range(ord('a'), ord('a') + settings.nGraphs):
        nodes, head = model.buildRandomModel(settings.graphSize,
                                             settings.nSeeds,
                                             1,
                                             0.5,
                                             1.25/settings.nSeeds,
                                             2,
                                             settings.behaviorPaths,
                                             settings.pruner,
                                             None,
                                             chr(prefixChar),
                                             3)
        graphvizModels.append(model.graphvizEntireThing(head))
        nodeBucket.extend(nodes)
    
    with open(settings.outputRoot + ".gv", "w") as gvfile:
        gvfile.write(weldGraphViz(graphvizModels))
        gvfile.flush()
    
    pickedColumns = [foo for foo in nodeBucket if random.random() <= settings.tsvColRate]
    shuffle(pickedColumns)
    
    with open(settings.outputRoot + ".txt", "w") as datafile:
        writer = csv.writer(datafile, dialect='excel-tab')
        writer.writerow(["{0}:{1}".format(node.name, node.genName(settings.tsvRecursion)) for node in pickedColumns])
        for x in range(settings.samples):
            writer.writerow([str(node.calculate(x)) for node in pickedColumns])
            if not x % 100:
                print x, "rows written"
        datafile.flush()