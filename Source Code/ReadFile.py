def readFile(fileName):
    with open(fileName, "r") as f:
        lines = f.readlines()

    for i in range(0, len(lines)):
        lines[i] = lines[i].strip()

    for i in range(len(lines) - 1, -1, -1):
        isNote = 0
        for j in range(0, len(lines[i])):
            if (lines[i][j] == "/"):
                isNote = 1
                break
        if (not lines[i] or isNote == 1):
            lines.pop(i)

    for i in range(len(lines) - 1, -1, -1):
        if (lines[i][len(lines[i]) - 1] != "."):
            lines[i] += lines[i + 1]
            lines.pop(i + 1)

    return lines