from termcolor import cprint

class Question:
    questionsQuantity = 0
    def __init__(self, description, answerList, rand):
        #provided description without question number, answerList must on the other hand be with a)b)c)d) etc.
        #correct answer must be marked with thriple '>', such as '>>>'
        Question.questionsQuantity += 1
        self.questionNo = Question.questionsQuantity
        self.desc = description.strip()
        self.ansDict = {}
        self.getAnswers(answerList)
        self.correctBool = False
        self.rand = rand

    def getAnswers(self, answerList):
        self.answerSet = set()
        for row in answerList:
            self.ansDict[row.lower().replace(">>>", "").strip()[0]] = row.replace(">>>", "").strip()[2:].strip()
            if ">>>" in row:
                self.answerSet.add(row.lower().replace(">>>", "").strip()[0])

    def printCorrectAnswers(self, command=None):
        if command == None:
            cprint("\nCorrect answers: {}".format(", ".join(sorted(self.answerSet))), 'green')
        elif command == "extended":
            cprint("\nCorrect answers: {}".format(", ".join(sorted(self.answerSet))), 'green')
            if self.answerSet:
                for key in sorted(self.answerSet):
                    cprint(str(key) + ") " + self.ansDict[key].replace(">>>", ""), 'green')
        elif command == "full":
            for key in sorted(self.ansDict.keys()):
                if key in self.answerSet:
                    cprint("\t" + str(key) + ") " + self.ansDict[key].replace(">>>", ""), 'green')
                else:
                    cprint("\t" + str(key) + ") " + self.ansDict[key].replace(">>>", ""), 'red')


    def parse(self):
        print(str(self.questionNo) + ". " + self.desc.strip())
        self.printCorrectAnswers("full")

        return False

    def ask(self):
        print(str(self.questionNo) + ". " + self.desc.strip(), "\n")
        iterDict = self.ansDict.keys() if self.rand else sorted(self.ansDict.keys())
        for key in iterDict:
            print(str(key) + ") " + self.ansDict[key].replace(">>>", ""))
        print("\nAnswer: ", end="")
        while True:
            answer = input().lower().replace(" ", "")
            diff = set(list(answer)).difference(set(self.ansDict.keys()))
            if diff:
                print("You entered unavailable answer {}! Try again: ".format(", ".join(diff)), end="")
                continue
            break

        if self.answerSet == (set(list(answer))):
            cprint("CORRECT!", 'green')
            self.correctBool = True
            return True
        else:
            wrongAnsSet = sorted(set(list(answer)).difference(self.answerSet))
            if wrongAnsSet:
                cprint("Wrong answers: {}!".format(", ".join(wrongAnsSet)), 'red')
            else:
                cprint("Wrong! Not enough correct answers!", 'red')
            self.printCorrectAnswers("extended")
            self.correctBool = False
            return False


