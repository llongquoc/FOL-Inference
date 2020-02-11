from ReadFile import *
from Knowledge import *


def readFacts(fileName, facts):
    lines = readFile(fileName)

    for i in range(0, len(lines)):
        check = 1
        for j in range(0, len(lines[i])):
            if (lines[i][j] == "-"):
                check = 0
                break
        if (check):
            facts.append(readKnowledge(lines[i]))