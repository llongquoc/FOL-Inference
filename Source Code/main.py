from Facts import *
from Process import *


def main():
    facts = []
    readFacts("input.txt", facts)

    rules = []
    readRules("input.txt", rules)

    queries = []
    readQueries("input.txt", queries)

    processQueries("output.txt", facts, rules, queries)


if __name__ == '__main__':
    main()