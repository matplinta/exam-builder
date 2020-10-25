#!/usr/bin/env python3
from termcolor import cprint
import re
import sys
import os
import argparse
from random import sample

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


class Exam:
    def __init__(self, file, debug, random, randomQuestions):
        self.filePath = file
        self.randomQuestions = randomQuestions
        self.questions = list()
        self.loadQuestions()
        self.questionsDict = {}
        if random:
            self.questions = sample(self.questions, len(self.questions))

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Questions: {}".format(Question.questionsQuantity))
        input("Press Enter to start")
        print("\033[A                                                     \033[A\n")
        if debug:
            try:
                for question in self.questions:
                    # os.system('cls' if os.name == 'nt' else 'clear')
                    self.questionsDict[question.questionNo] = question.parse()
                    input("Press Enter")
                    print("\033[A                                                     \033[A\n")
            except KeyboardInterrupt:
                print("Ctrl C, interrupted.")
        else:
            try:
                for question in self.questions:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.questionsDict[question.questionNo] = question.ask()
                    input("Press Enter")
            except KeyboardInterrupt:
                print("Ctrl C, test interrupted.")
            os.system('cls' if os.name == 'nt' else 'clear')
            try:
                self.summarise()
            except KeyboardInterrupt:
                print("Ctrl C, goodbye.")

    def loadQuestions(self):
        newQuestionRegex = re.compile(r'(\d){1,3}(\)|\.)')
        answerRegex = re.compile(r'[a-l](\)|\.)', re.IGNORECASE)
        with open(self.filePath, "r") as file:
            currentDesc = str()
            currentAnsList = list()
            for line in file:
                newQuestionSearch = newQuestionRegex.search(line.strip()[0:4])
                if newQuestionSearch:
                    if currentAnsList and currentDesc:
                        self.questions.append(Question(currentDesc, currentAnsList, self.randomQuestions))
                    currentAnsList = list()
                    currentDesc = line[0:4].replace(newQuestionSearch.group(), "").lstrip() + line[4:].rstrip()
                    continue
                elif answerRegex.search(line.replace(">>>", "").strip().lower()[0:2]):
                    currentAnsList.append(line)
                    continue
                currentDesc += " " + line
            self.questions.append(Question(currentDesc, currentAnsList, self.randomQuestions))
            file.close()

    def summarise(self):
        self.right = list()
        self.wrong = list()
        for i in self.questionsDict.keys():
            if self.questionsDict[i] == False:
                self.wrong.append(i)
            else:
                self.right.append(i)
        cprint("            RESULTS            RESULTS            RESULTS            ", on_color='on_blue')
        print("")
        cprint("Correct answers:\t{}".format(len(self.right)), on_color='on_green')
        cprint("Wrong answers:\t\t{}".format(len(self.wrong)), on_color='on_red')
        if self.wrong:
            input("Press enter to print incorrectly answered questions")
            print("Wrong answered questions: ")
            for number in self.wrong:
                for question in self.questions:
                    if question.questionNo == number:
                        question.parse()
                        input("Press Enter")
                        print("\033[A                                                     \033[A\n")
        cprint("Great work! See you on the exam :]", 'magenta')

parser = argparse.ArgumentParser()
parser.add_argument('file', help="File with exam questions and answers")
parser.add_argument('-d', '--debug', action="store_true", help="Enter debugging(learning) mode, with correct answers displayed")
parser.add_argument('-r', '--random', action="store_true", help="Questions in random sequence")
parser.add_argument('-R', '--rand_questions', action="store_true", help="Answers given in random sequence")
args = parser.parse_args()
instance = Exam(args.file, args.debug, args.random, args.rand_questions)
