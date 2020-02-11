from Rules import *
from Queries import *


newFacts = []
notNewFacts = []


def processQueryHasDash(facts, rules, query, listValue):
    if (not query.object):
        for i in range(0, len(listValue)):
            newQuery = Knowledge(query.predicate, listValue[i], query.object)
            result = processQuery(facts, rules, newQuery, listValue)
            if (result == [1]):
                return [1]
        return [0]
    else:
        if (query.subject == "_" and query.object == "_"):
            for i in range(0, len(listValue)):
                for j in range(0, len(listValue)):
                    newQuery = Knowledge(query.predicate, listValue[i], listValue[j])
                    result = processQuery(facts, rules, newQuery, listValue)
                    if (result == [1]):
                        return [1]
            return [0]
        else:
            result = []
            if (query.subject == "_"):
                if (query.object[0] >= "A" and query.object[0] <= "Z"):
                    variable = query.object
                    for i in range(0, len(listValue)):
                        for j in range(0, len(listValue)):
                            newQuery = Knowledge(query.predicate, listValue[j], listValue[i])
                            temp = processQuery(facts, rules, newQuery, listValue)
                            if (temp == [1]):
                                result.append(variable + "=" + listValue[i])
                                break
                    return result
                else:
                    for i in range(0, len(listValue)):
                        newQuery = Knowledge(query.predicate, listValue[i], query.object)
                        result = processQuery(facts, rules, newQuery, listValue)
                        if (result == [1]):
                            return [1]
                    return[0]
            else:
                if (query.subject[0] >= "A" and query.subject[0] <= "Z"):
                    variable = query.subject
                    for i in range(0, len(listValue)):
                        for j in range(0, len(listValue)):
                            newQuery = Knowledge(query.predicate, listValue[i], listValue[j])
                            temp = processQuery(facts, rules, newQuery, listValue)
                            if (temp == [1]):
                                result.append(variable + "=" + listValue[i])
                                break
                    return result
                else:
                    for i in range(0, len(listValue)):
                        newQuery = Knowledge(query.predicate, query.subject, listValue[i])
                        result = processQuery(facts, rules, newQuery, listValue)
                        if (result == [1]):
                            return [1]
                    return[0]


def processQueryInFact(facts, query):
    result = []

    if (not query.object):
        isHaveObject = 0
    else:
        isHaveObject = 1

    if (isHaveObject):
        if (query.subject[0] >= "A" and query.subject[0] <= "Z"):
            if (query.object[0] >= "A" and query.object[0] <= "Z"):
                for i in range(0, len(facts)):
                    if (query.predicate == facts[i].predicate):
                        temp = query.subject + "=" + facts[i].subject + ", " + query.object + "=" + facts[i].object
                        result.append(temp)
                return result
            else:
                for i in range(0, len(facts)):
                    if (query.predicate == facts[i].predicate and query.object == facts[i].object):
                        result.append(query.subject + "=" + facts[i].subject)
                        return result
                return [0]
        else:
            if (query.object[0] >= "A" and query.object[0] <= "Z"):
                for i in range(0, len(facts)):
                    if (query.predicate == facts[i].predicate and query.subject == facts[i].subject):
                        result.append(query.object + "=" + facts[i].object)
                        return result
                return [0]
            else:
                for i in range(0, len(facts)):
                    if (query == facts[i]):
                        return [1]
                return [0]
    else:
        if (query.subject[0] >= "A" and query.subject[0] <= "Z"):
            for i in range(0, len(facts)):
                if (query.predicate == facts[i].predicate):
                    result.append(query.subject + "=" + facts[i].subject)
            return result
        else:
            for i in range(0, len(facts)):
                if (query == facts[i]):
                    return [1]
            return [0]


def operatorEqual(a, b):
    if (a == b):
        return [1]
    return [0]


def operatorIsBigger(a, b):
    if (a.isnumeric() == 0 or b.isnumeric() == 0):
        return [0]
    if (int(a) > int(b)):
        return [1]
    return [0]


def operatorIsSmaller(a, b):
    if (a.isnumeric() == 0 or b.isnumeric() == 0):
        return [0]
    if (int(a) < int(b)):
        return [1]
    return [0]


def operatorAnd(a, b):
    if (a == [1] and b == [1]):
        return [1]
    return [0]


def operatorOr(a, b):
    if (a == [1] or b == [1]):
        return [1]
    return [0]


def processClause(operator, sign):
    i = 0
    while (i < len(sign)):
        if (sign[i] == "("):
            count = 0
            for j in range(0, i + 1):
                if (sign[j] == "," or sign[j] == ";" or sign[j] == "=" or sign[j] == ">" or sign[j] == "<"):
                    count += 1
                if (sign[j] == ")"):
                    if (j == len(sign) - 1):
                        count += 1
                    else:
                        if (sign[j + 1] != "," and sign[j + 1] != ";" and sign[j + 1] != "=" and sign[j + 1] != ">" and sign[j + 1] != "<"):
                            count += 1
            newOperator = []
            newSign = []
            countBracket = 1
            for j in range(i + 1, len(sign)):
                if (sign[j] == "," or sign[j] == ";" or sign[j] == "=" or sign[j] == ">" or sign[j] == "<"):
                    newSign.append(sign[j])
                    newOperator.append(operator[count])
                    operator.pop(count)
                if (sign[j] == "\\"):
                    newSign.append(sign[j])
                if (sign[j] == "("):
                    newSign.append(sign[j])
                    countBracket += 1
                if (sign[j] == ")"):
                    countBracket -= 1
                    if (countBracket == 0):
                        newOperator.append(operator[count])
                        operator.pop(count)
                        temp = j
                        break
                    else:
                        newSign.append(sign[j])
            resClause = processClause(newOperator, newSign)
            operator.insert(count, resClause)
            for j in range(i, temp + 1):
                sign.pop(i)
        else:
            i += 1

    while (len(sign)):
        isHaveCompare = 0
        isHaveAnd = 0
        for i in range(0, len(sign)):
            if (sign[i] == "=" or sign[i] == ">" or sign[i] == "<"):
                isHaveCompare = 1
            if (sign[i] == ","):
                isHaveAnd = 1
        i = 0
        while(i < len(sign)):
            checkUse = 0
            isOperatorNotEqual = 0
            if (sign[i] == "\\"):
                checkUse = 1
                isOperatorNotEqual = 1
                result = operatorEqual(operator[i], operator[i + 1])
                if (result == [1]):
                    result = [0]
                else:
                    result = [1]
            if (sign[i] == "="):
                checkUse = 1
                result = operatorEqual(operator[i], operator[i + 1])
            if (sign[i] == ">"):
                checkUse = 1
                result = operatorIsBigger(operator[i], operator[i + 1])
            if (sign[i] == "<"):
                checkUse = 1
                result = operatorIsSmaller(operator[i], operator[i + 1])
            if (isHaveCompare == 0 and sign[i] == ","):
                checkUse = 1
                result = operatorAnd(operator[i], operator[i + 1])
            if (isHaveCompare == 0 and isHaveAnd == 0 and sign[i] == ";"):
                checkUse = 1
                result = operatorOr(operator[i], operator[i + 1])
            if (checkUse):
                operator.pop(i)
                operator.pop(i)
                operator.insert(i, result)
                sign.pop(i)
                if (isOperatorNotEqual == 1):
                    sign.pop(i)
            else:
                i += 1

    return operator[0]


def isInFacts(rule, facts):
    for i in range(0, len(facts)):
        if (rule.predicate == facts[i].predicate):
            return 1
    return 0


def processRule(facts, rule, rules, value, listValue):
    for i in range(0, len(value)):
        if (value[i] == [1]):
            return

    variable = 1
    for i in range(0, len(rule.operator)):
        if (type(rule.operator[i]) == Knowledge):
            if (rule.operator[i].subject[0] >= "A" and rule.operator[i].subject[0] <= "Z"):
                variable = rule.operator[i].subject
                break
            else:
                if (rule.operator[i].object):
                    if (rule.operator[i].object[0] >= "A" and rule.operator[i].object[0] <= "Z"):
                        variable = rule.operator[i].object
                        break

    if (variable == 1):
        newOperator = []
        newSign = []
        for j in range(0, len(rule.sign)):
            newSign.append(rule.sign[j])
        for i in range(0, len(rule.operator)):
            tempOperator = rule.operator[i]
            if (type(tempOperator) == Knowledge):
                newOperator.append(processQuery(facts, rules, tempOperator, listValue))
            else:
                newOperator.append(tempOperator)
        value.append(processClause(newOperator, newSign))
    else:
        inFacts = 1
        for i in range(0, len(rule.operator)):
            tempOperator = rule.operator[i]
            if (type(tempOperator) == Knowledge):
                if (tempOperator.subject == variable):
                    temp = isInFacts(tempOperator, facts)
                    if (temp == 0):
                        inFacts = 0
                        break
                else:
                    if (tempOperator.object):
                        if (tempOperator.object == variable):
                            temp = isInFacts(tempOperator, facts)
                            if (temp == 0):
                                inFacts = 0
                                break
        if (inFacts == 1):
            predicate = []
            for i in range(0, len(rule.operator)):
                tempOperator = rule.operator[i]
                if (type(tempOperator) == Knowledge):
                    if (tempOperator.subject == variable):
                        predicate.append(tempOperator.predicate)
                    else:
                        if (tempOperator.object):
                            if (tempOperator.object == variable):
                                predicate.append(tempOperator.predicate)
            list = []
            for i in range(0, len(facts)):
                trueFact = 0
                for j in range(0, len(predicate)):
                    if (facts[i].predicate == predicate[j]):
                        trueFact = 1
                        break
                if (trueFact == 0):
                    continue
                isInList = 0
                for j in range(0, len(list)):
                    if (facts[i].subject == list[j]):
                        isInList = 1
                        break
                if (isInList == 0):
                    list.append(facts[i].subject)
                isInList = 0
                for j in range(0, len(list)):
                    if (facts[i].object == list[j]):
                        isInList = 1
                        break
                if (isInList == 0 and facts[i].object):
                    list.append(facts[i].object)
            for i in range(0, len(list)):
                newKnowledge = rule.newKnowledge
                newOperator = []
                newSign = []
                for j in range(0, len(rule.sign)):
                    newSign.append(rule.sign[j])
                for j in range(0, len(rule.operator)):
                    tempOperator = rule.operator[j]
                    if (type(tempOperator) == Knowledge):
                        if (tempOperator.subject == variable):
                            tempOperator = Knowledge(tempOperator.predicate, list[i], tempOperator.object)
                        if (tempOperator.object):
                            if (tempOperator.object == variable):
                                tempOperator = Knowledge(tempOperator.predicate, tempOperator.subject, list[i])
                    else:
                        if (tempOperator == variable):
                            tempOperator = list[i]
                    newOperator.append(tempOperator)
                newRule = Rule(newKnowledge, newOperator, newSign)
                processRule(facts, newRule, rules, value, listValue)
                for j in range(0, len(value)):
                    if (value[j] == [1]):
                        return
        else:
            for i in range(0, len(listValue)):
                newKnowledge = rule.newKnowledge
                newOperator = []
                newSign = []
                for j in range(0, len(rule.sign)):
                    newSign.append(rule.sign[j])
                for j in range(0, len(rule.operator)):
                    tempOperator = rule.operator[j]
                    if (type(tempOperator) == Knowledge):
                        if (tempOperator.subject == variable):
                            tempOperator = Knowledge(tempOperator.predicate, listValue[i], tempOperator.object)
                        if (tempOperator.object):
                            if (tempOperator.object == variable):
                                tempOperator = Knowledge(tempOperator.predicate, tempOperator.subject, listValue[i])
                    else:
                        if (tempOperator == variable):
                            tempOperator = listValue[i]
                    newOperator.append(tempOperator)
                newRule = Rule(newKnowledge, newOperator, newSign)
                processRule(facts, newRule, rules, value, listValue)
                for j in range(0, len(value)):
                    if (value[j] == [1]):
                        return


def processQueryInRulesWithNonVariable(facts, rule, rules, query, listValue):
    variableSubject = rule.newKnowledge.subject
    variableObject = rule.newKnowledge.object

    for i in range(0, len(rule.operator)):
        if (type(rule.operator[i]) == Knowledge):
            if (rule.operator[i].subject == variableSubject):
                newOperator = Knowledge(rule.operator[i].predicate, query.subject, rule.operator[i].object)
                rule.operator[i] = newOperator
            else:
                if (rule.operator[i].subject == variableObject):
                    newOperator = Knowledge(rule.operator[i].predicate, query.object, rule.operator[i].object)
                    rule.operator[i] = newOperator
            if (rule.operator[i].object == variableSubject):
                newOperator = Knowledge(rule.operator[i].predicate, rule.operator[i].subject, query.subject)
                rule.operator[i] = newOperator
            else:
                if (rule.operator[i].object == variableObject):
                    newOperator = Knowledge(rule.operator[i].predicate, rule.operator[i].subject, query.object)
                    rule.operator[i] = newOperator
        else:
            if (rule.operator[i] == variableSubject):
                rule.operator[i] = query.subject
            else:
                if (rule.operator[i] == variableObject):
                    rule.operator[i] = query.object

    value = []
    processRule(facts, rule, rules, value, listValue)

    tempResult = 0
    for i in range(0, len(value)):
        if (value[i] == [1]):
            tempResult = 1
            break

    if (tempResult):
        newFacts.append(query)
        return [1]
    else:
        notNewFacts.append(query)
        return [0]


def processQueryInRulesWithOneVariable(facts, rule, rules, query, listValue):
    result = []

    if (query.subject[0] >= "A" and query.subject[0] <= "Z"):
        variable = query.subject
        for i in range(0, len(listValue)):
            tempNewKnowledge = rule.newKnowledge
            tempOperator = []
            for j in range(0, len(rule.operator)):
                tempOperator.append(rule.operator[j])
            tempSign = []
            for j in range(0, len(rule.sign)):
                tempSign.append(rule.sign[j])
            newRule = Rule(tempNewKnowledge, tempOperator, tempSign)
            newQuery = Knowledge(query.predicate, listValue[i], query.object)
            temp = processQueryInRulesWithNonVariable(facts, newRule, rules, newQuery, listValue)
            if (temp == [1]):
                result.append(variable + "=" + listValue[i])
    else:
        variable = query.object
        for i in range(0, len(listValue)):
            tempNewKnowledge = rule.newKnowledge
            tempOperator = []
            for j in range(0, len(rule.operator)):
                tempOperator.append(rule.operator[j])
            tempSign = []
            for j in range(0, len(rule.sign)):
                tempSign.append(rule.sign[j])
            newRule = Rule(tempNewKnowledge, tempOperator, tempSign)
            newQuery = Knowledge(query.predicate, query.subject, listValue[i])
            temp = processQueryInRulesWithNonVariable(facts, newRule, rules, newQuery, listValue)
            if (temp == [1]):
                result.append(variable + "=" + listValue[i])

    return result


def processQueryInRulesWithTwoVariable(facts, rule, rules, query, listValue):
    variable = query.subject
    result = []

    for i in range(0, len(listValue)):
        tempNewKnowledge = rule.newKnowledge
        tempOperator = []
        for j in range(0, len(rule.operator)):
            tempOperator.append(rule.operator[j])
        tempSign = []
        for j in range(0, len(rule.sign)):
            tempSign.append(rule.sign[j])
        newRule = Rule(tempNewKnowledge, tempOperator, tempSign)
        newQuery = Knowledge(query.predicate, listValue[i], query.object)
        temp = processQueryInRulesWithOneVariable(facts, newRule, rules, newQuery, listValue)
        for j in range(0, len(temp)):
            tempResult = variable + "=" + listValue[i] + ", " + temp[j]
            result.append(tempResult)

    return result


def processQueryNotInFactsAndRules():
    return [0]


def processQuery(facts, rules, query, listValue):
    for i in range(0, len(newFacts)):
        if (query == newFacts[i]):
            return [1]
    for i in range(0, len(notNewFacts)):
        if (query == notNewFacts[i]):
            return [0]

    isInFacts = 0

    for i in range(0, len(facts)):
        if (query.predicate == facts[i].predicate):
            isInFacts = 1
            break
    if (isInFacts):
        temp = processQueryInFact(facts, query)
        if (temp == [0]):
            notNewFacts.append(query)
        return temp
    else:
        isInRules = 0
        for i in range(0, len(rules)):
            if (query.predicate == rules[i].newKnowledge.predicate):
                tempNewKnowledge = rules[i].newKnowledge
                tempOperator = []
                for j in range(0, len(rules[i].operator)):
                    tempOperator.append(rules[i].operator[j])
                tempSign = []
                for j in range(0, len(rules[i].sign)):
                    tempSign.append(rules[i].sign[j])
                rule = Rule(tempNewKnowledge, tempOperator, tempSign)
                isInRules = 1
                break
        if (isInRules):
            if (not query.object):
                isHaveObject = 0
            else:
                isHaveObject = 1
            if (query.subject[0] >= "A" and query.subject[0] <= "Z"):
                if (not isHaveObject):
                    countVariable = 1
                else:
                    if (query.object[0] >= "A" and query.object[0] <= "Z"):
                        countVariable = 2
                    else:
                        countVariable = 1
            else:
                if (not isHaveObject):
                    countVariable = 0
                else:
                    if (query.object[0] >= "A" and query.object[0] <= "Z"):
                        countVariable = 1
                    else:
                        countVariable = 0
            if (countVariable == 0):
                return processQueryInRulesWithNonVariable(facts, rule, rules, query, listValue)
            if (countVariable == 1):
                return processQueryInRulesWithOneVariable(facts, rule, rules, query, listValue)
            return processQueryInRulesWithTwoVariable(facts, rule, rules, query, listValue)
        else:
            return processQueryNotInFactsAndRules()


def processQueries(fileName, facts, rules, queries):
    listValue = []
    for i in range(0, len(facts)):
        isInList = 0
        for j in range(0, len(listValue)):
            if (facts[i].subject == listValue[j]):
                isInList = 1
                break
        if (isInList == 0):
            listValue.append(facts[i].subject)
        isInList = 0
        for j in range(0, len(listValue)):
            if (facts[i].object == listValue[j]):
                isInList = 1
                break
        if (isInList == 0 and facts[i].object):
            listValue.append(facts[i].object)

    f = open(fileName, "w")

    for i in range(0, len(queries)):
        print("Processing query", i + 1, end = "\n")
        f.write("/* Query " + str(i + 1) + " */\n")
        if (queries[i].subject == "_" or queries[i].object == "_"):
            result = processQueryHasDash(facts, rules, queries[i], listValue)
        else:
            result = processQuery(facts, rules, queries[i], listValue)
        if (not result):
            f.write("False" + "\n")
        else:
            for j in range(0, len(result)):
                if (result[j] == 1):
                    f.write("True" + "\n")
                    break
                if (result[j] == 0):
                    f.write("False" + "\n")
                    break
                f.write(result[j] + "\n")
        print("Success!", end = "\n")