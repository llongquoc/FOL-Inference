from ReadFile import *
from Knowledge import *

Rule = namedtuple("Rule", ['newKnowledge', 'operator', 'sign'])
def readRules(fileName, rules):
    lines = readFile(fileName)

    for i in range(0, len(lines)):
        tick = -1
        check = 0
        for j in range(0, len(lines[i])):
            if (lines[i][j] == "-"):
                tick = j
                break
        for j in range(0, tick):
            if (lines[i][j] == "("):
                check = 1
                break
        if (check):
            temp = ""
            for j in range(0, tick - 1):
                temp += lines[i][j]
            newKnowledge = readKnowledge(temp)
            sign = []
            pos = []
            line = ""
            for j in range(tick + 1, len(lines[i])):
                line += lines[i][j]
            line.strip()
            for j in range(0, len(line)):
                if (line[j] == ","):
                    isSign = 1
                    for k in range(j - 1, -1, -1):
                        if (line[k] == " "):
                            continue
                        if (line[k] != ")"):
                            if (k >= 2):
                                if (line[k - 1] == "("):
                                    if ((line[k - 2] >= "A" and line[k - 2] <= "Z") or (line[k - 2] >= "a" and line[k - 2] <= "z")):
                                        isSign = 0
                            break
                        else:
                            break
                    if (isSign):
                        sign.append(line[j])
                        pos.append(j)
                else:
                    if (line[j] == ";" or line[j] == "\\" or line[j] == "=" or line[j] == ">" or line[j] == "<"):
                        sign.append(line[j])
                        pos.append(j)
                    else:
                        if (line[j] == "("):
                            if (j == 0):
                                sign.append(line[j])
                                pos.append(j)
                            else:
                                if (not (line[j - 1] >= "A" and line[j - 1] <= "Z") and not (line[j - 1] >= "a" and line[j - 1] <= "z")):
                                    sign.append(line[j])
                                    pos.append(j)
                        else:
                            if (line[j] == ")"):
                                countBracket = 0
                                for k in range(0, j):
                                    if (line[k] == "("):
                                        isNotBracket = 1
                                        for l in range(0, len(pos)):
                                            if (k == pos[l]):
                                                isNotBracket = 0
                                                break
                                        if (isNotBracket):
                                            countBracket += 1
                                    if (line[k] == ")"):
                                        isNotBracket = 1
                                        for l in range(0, len(pos)):
                                            if (k == pos[l]):
                                                isNotBracket = 0
                                                break
                                        if (isNotBracket):
                                            countBracket -= 1
                                if (countBracket == 0):
                                    sign.append(line[j])
                                    pos.append(j)
            operator = []
            if (line[pos[0]] != "("):
                isKnowledge = 0
                temp = ""
                for j in range(0, pos[0]):
                    temp += line[j]
                temp = temp.strip()
                for j in range(0, len(temp)):
                    if (temp[j] == "("):
                        newOperator = readKnowledge(temp)
                        isKnowledge = 1
                        operator.append(newOperator)
                        break
                if (isKnowledge == 0 and temp):
                    operator.append(temp)
            for j in range(0, len(pos) - 1):
                if (pos[j] + 1 == pos[j + 1]):
                    continue
                isKnowledge = 0
                temp = ""
                for l in range(pos[j] + 1, pos[j + 1]):
                    temp += line[l]
                temp = temp.strip()
                for l in range(0, len(temp)):
                    if (temp[l] == "("):
                        newOperator = readKnowledge(temp)
                        isKnowledge = 1
                        operator.append(newOperator)
                        break
                if (isKnowledge == 0 and temp):
                    operator.append(temp)
            if (line[pos[len(pos) - 1]] != ")"):
                isKnowledge = 0
                temp = ""
                for j in range(pos[len(pos) - 1] + 1, len(line) - 1):
                    temp += line[j]
                temp = temp.strip()
                for j in range(0, len(temp)):
                    if (temp[j] == "("):
                        newOperator = readKnowledge(temp)
                        isKnowledge = 1
                        operator.append(newOperator)
                        break
                if (isKnowledge == 0 and temp):
                    operator.append(temp)
            rule = Rule(newKnowledge, operator, sign)
            rules.append(rule)

    changeVariableInRules(rules)


def changeVariableInRules(rules):
    for i in range(0, len(rules)):
        changeVariableInRule(rules[i], 0)


def changeVariableInRule(rule, pos):
    variableSubject = rule.newKnowledge.subject
    variableObject = rule.newKnowledge.object

    i = pos
    while (i < len(rule.sign)):
        if (rule.sign[i] == ";"):
            count = 0
            for j in range(0, i + 1):
                if (rule.sign[j] == "," or rule.sign[j] == ";" or rule.sign[j] == "=" or rule.sign[j] == ">" or rule.sign[j] == "<"):
                    count += 1
                if (rule.sign[j] == ")"):
                    if (j == len(rule.sign) - 1):
                        count += 1
                    else:
                        if (rule.sign[j + 1] != "," and rule.sign[j + 1] != ";" and rule.sign[j + 1] != "=" and rule.sign[j + 1] != ">" and rule.sign[j + 1] != "<"):
                            count += 1
            variable = 1
            for j in range(0, count):
                if (type(rule.operator[j]) == Knowledge):
                    if (rule.operator[j].subject >= "A" and rule.operator[j].subject <= "Z"):
                        if (rule.operator[j].subject != variableSubject and rule.operator[j].subject != variableObject):
                            variable = rule.operator[j].subject
                            break
                    if (rule.operator[j].object):
                        if (rule.operator[j].object >= "A" and rule.operator[j].object <= "Z"):
                            if (rule.operator[j].object != variableSubject and rule.operator[j].object != variableObject):
                                variable = rule.operator[j].object
                                break
            if (variable != 1):
                variableNeedChange = 1
                for j in range(count, len(rule.operator)):
                    if (type(rule.operator[j]) == Knowledge):
                        if (rule.operator[j].subject >= "A" and rule.operator[j].subject <= "Z"):
                            if (rule.operator[j].subject != variableSubject and rule.operator[j].subject != variableObject):
                                variableNeedChange = rule.operator[j].subject
                                break
                        if (rule.operator[j].object):
                            if (rule.operator[j].object >= "A" and rule.operator[j].object <= "Z"):
                                if (rule.operator[j].object != variableSubject and rule.operator[j].object != variableObject):
                                    variableNeedChange = rule.operator[j].object
                                    break
                if (variableNeedChange != 1):
                    for j in range(count, len(rule.operator)):
                        if (type(rule.operator[j]) == Knowledge):
                            if (rule.operator[j].subject == variableNeedChange):
                                newOperator = Knowledge(rule.operator[j].predicate, variable, rule.operator[j].object)
                                rule.operator[j] = newOperator
                            if (rule.operator[j].object == variableNeedChange):
                                newOperator = Knowledge(rule.operator[j].predicate, rule.operator[j].subject, variable)
                                rule.operator[j] = newOperator
            changeVariableInRule(rule, i + 1)
            break
        else:
            i += 1