from ReadFile import *
from Knowledge import *


def readQueries(fileName, queries):
    lines = readFile(fileName)

    for i in range(0, len(lines)):
        tick = -1
        check = 0
        for j in range(0, len(lines[i])):
            if (lines[i][j] == "-"):
                tick = j
                break
        for j in range(0, tick):
            if (lines[i][j] == "?"):
                check = 1
                break
        if (check):
            query = ""
            for j in range(tick + 1, len(lines[i])):
                query += lines[i][j]
            query = query.strip()
            queries.append(readKnowledge(query))