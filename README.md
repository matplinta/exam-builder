# exam-builder
Terminal script for learning test answeres and carrying out single & multiple choice tests.

Run it with `./exam.py <file>`

# Usage
Program parses provided test file and defaultly starts asking questions in the order corresponding to that in the file. If test is interrupted by pressing ^C or the number of questions runs out, user is taken into summary display, which enumerates number of questions answered correctly and not. Summary is also displayed after pressing ^C to exit the program. After pressing `Enter`, user is reminded of all the questions answered incorrectly.

There is also a possibility to run program in debug mode, which is essentially a learning tool, showing correct answeres to every question. 

## Additional options
`-r`, `--random` Questions will be asked in random order.

`-R`, `--rand_questions` Random order of possible answeres.

`-d`, `--debug` Enters debug mode.

`-h` Prints additional options and usage.


# Test files format requirements
Provided file containing test questions with answeres should meet the requirements. Any file format is ok, as long as it can be read as text file. 

Questions should start with a number followed by a `.` or a `)`. Following on the next separete lines should be answeres starting with a letter followed also by a `.` or a `)`. Technically the numbers and letters in questions and answeres does not reflect the numbers and letters parsed by program, as exam-builder has its own system of enumerating them. As long as questions are preceded by a number and answeres by a letter, parser should work as expected.

Correct answeres should be preceded by a triple greater by symbol, i.e. `>>>`. Program allowes multiple correct answeres.

An example test file can be found in this repository, by the name of `tisb.txt`

# Dependencies
Package `termicolor` should be installed in order to properly run exam-builder. You can install it with `pip install termicolor` or `pip3 install termicolor`
