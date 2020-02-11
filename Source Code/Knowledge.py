from collections import namedtuple


Knowledge = namedtuple("Knowledge", ['predicate', 'subject', 'object'])


def readKnowledge(line):
    tempPredicate = ""
    tempSubject = ""
    tempObject = ""

    for i in range(0, len(line)):
        if (line[i] != "("):
            tempPredicate += line[i]
        else:
            break

    isValidObject = 0
    for j in range(i + 1, len(line)):
        if (line[j] != "," and line[j] != ")"):
            tempSubject += line[j]
        else:
            if (line[j] == ","):
                isValidObject = 1
            break

    if (isValidObject):
        for k in range(j + 1, len(line)):
            if (line[k] != ")"):
                tempObject += line[k]
            else:
                break

    tempPredicate = tempPredicate.strip()
    tempSubject = tempSubject.strip()
    tempObject = tempObject.strip()
    knowledge = Knowledge(tempPredicate, tempSubject, tempObject)
    return knowledge