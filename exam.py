from question import Question
from termcolor import cprint
import re
import sys
import os
import argparse


class Exam:
    def __init__(self, file, debug):
        self.filePath = file
        self.questions = list()
        self.loadQuestions()
        self.questionsDict = {}
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
                        self.questions.append(Question(currentDesc, currentAnsList))
                    currentAnsList = list()
                    currentDesc = line[0:4].replace(newQuestionSearch.group(), "").lstrip() + line[4:].rstrip()
                    continue
                elif answerRegex.search(line.replace(">>>", "").strip().lower()[0:2]):
                    currentAnsList.append(line)
                    continue
                currentDesc += " " + line
            self.questions.append(Question(currentDesc, currentAnsList))
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
args = parser.parse_args()
instance = Exam(args.file, args.debug)
