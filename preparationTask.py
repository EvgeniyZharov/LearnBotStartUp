def prepare(TaskName):
    file = open(TaskName, 'r', encoding="utf-8")
    data = file.read().split('\n')
    task = {}
    for line in data:
        if "--" in line:
            task[line.split('--')[0].lower().strip()] = line.split('--')[1].lower().strip()
    return task


def prepareText(TaskNameText):
    file = open(TaskNameText, 'r', encoding="utf-8")
    data = file.read().split('\n')
    taskText = dict()
    for line in data:
        if "---" in line:
            taskText[line.split('---')[0].lower().strip()] = line.split('---')[1].lower().strip()
    return taskText


def checkTexts(textOne, textTwo):
    textOne, textTwo = textOne.split(), textTwo.split()
    a = min([len(textOne), len(textTwo)])
    b = max([len(textOne), len(textTwo)])
    score = 0
    # errors = list()
    for ii in range(a):
        if textOne[ii] == textTwo[ii]:
            score += 1
    accuracy = int(score/b * 100)

    return score, accuracy



