"""The program performs simple mathematic operations based on user input"""

from collections import deque

class Calculator:

    precedence = {"^":3, "*": 2, "/": 2, "+": 1, "-": 1}

    def __init__(self):
        self.variables = {}

    def addition(self, nums):
        """method used for adding numbers"""
        total = 0
        for i, num in enumerate(nums):
            value = 0
            if "-" in num or "+" in num:
                pass
            elif num in self.variables:
                value = int(self.variables[num])
            else:
                value = int(num)
            if i == 0:
                total += value
            elif "-" in num or "+" in num:
                continue
            else:
                if self.negative_num(nums[i-1]):
                    total += (value * -1)
                else:
                    total += value
        return total

    def negative_num(self, operators):
        """method used to check if a number is negative"""
        if operators.count("-") % 2 == 0:
            return False
        return True


    def variable(self, inp):
        """method used to store variables from user input into a dictionary"""
        var = inp.split("=")[0].strip()
        value = inp.split("=")[1].strip()
        if value in self.variables:
            value = self.variables[value]
        if self.ok_var(var) and self.ok_value(value):
            self.variables[var] = value
        else:
            print("Invalid identifier")

    def ok_var(self, var):
        """method user to check if a variable name is correct"""
        if not var.isalpha():
            return False
        return True

    def ok_value(self, value):
        """method used to check the value introduced is numeric"""
        if not value.replace("-", "").isdigit():
            return False
        return True

    def reversedPolish(self, expression):
        """method used to transform users input from infix to postfix notation"""
        output_exp = []
        operators = deque()
        temp = None
        for _, item in enumerate(expression):
            if item.isnumeric():
                output_exp.append(item)
            elif item in self.variables:
                output_exp.append(self.variables[item])
            elif len(operators) == 0 or operators[-1] == "(":
                operators.append(item)
            elif item == "(":
                operators.append(item)
            elif item == ")":
                temp = operators.pop()
                while temp != "(":
                    output_exp.append(temp)
                    temp = operators.pop()
            elif self.precedence[item] > self.precedence[operators[-1]]:
                operators.append(item)
            elif self.precedence[item] <= self.precedence[operators[-1]]:
                temp = operators.pop()
                while self.precedence[temp] < self.precedence[item]:
                    output_exp.append(temp)
                    temp = operators.pop()
                operators.append(item)
                output_exp.append(temp)
        if len(operators) != 0:
            while len(operators) > 0:
                output_exp.append(operators.pop())

        return output_exp

    def evaluate(self, a, b, operator):
        """method used to evaluate operators in user input and perform calculation acordingly"""
        if operator == "^":
            return a ** b
        elif operator == '*':
            return a*b
        elif operator == '/':
            return a//b
        elif operator == '+':
            return a+b
        elif operator == '-':
            return a-b
        else:
            return None

    def calculate(self, exp):
        """method used to perform calculation using postfix notation"""
        postfix = self.reversedPolish(exp)
        result = deque()

        for i in postfix:
            if i.isnumeric():
                result.append(int(i))
            else:
                temp = result.pop()
                tmp = result.pop()
                result.append(self.evaluate(int(tmp), int(temp), i))

        return result[0]



def commands(user_input):
    """funtion used to evaluate user's commands"""
    if user_input == "/help":
        print("The program performs simple mathematic operations based on user input")
        return False
    elif user_input == "/exit":
        print("Bye!")
        return True
    else:
        print("Unknown command")
        return False

def errors(usr_input):
    """functions check's user input for errors such as double operators(excluding + and -)"""
    for i, ch in enumerate(usr_input):
        if ch == "*" and usr_input[i + 1] == "*":
            return True
        elif ch == "/" and usr_input[i + 1] == "/":
            return True

    if "(" in usr_input and ")" in usr_input:
        if usr_input.index(")") < usr_input.index("("):
            return True

    if usr_input.count("(") != usr_input.count(")"):
        return True
    return False


def parse_input(inp_string):
    """function parses user input and change multiple + and - operators to single operator"""
    neg_start = False
    temp = []
    parsed_string = inp_string.replace(' ', '')
    parse_list = []
    for i, c in enumerate(parsed_string):
        # group all common characters
        if i == 0 and c == '-':
            neg_start = True
        elif i+1 == len(parsed_string):
            if temp != [] and c.isnumeric():
                temp.append(c)
                parse_list.append(''.join(temp))
                temp.clear()
            else:
                if temp != []:
                    parse_list.append(''.join(temp))
                temp.clear()
                parse_list.append(c)
        elif c == '*' or c == '/' or c == '(' or c == ')':
            parse_list.append(c)
        elif c.isnumeric() and (parsed_string[i+1].isnumeric()):
            temp.append(c)
        elif c.isnumeric() and not parsed_string[i+1].isnumeric():
            temp.append(c)
            parse_list.append(''.join(temp))
            temp.clear()
        elif c.isalpha() and parsed_string[i+1].isalpha():
            temp.append(c)
        elif c.isalpha() and not parsed_string[i+1].isalpha():
            temp.append(c)
            parse_list.append(''.join(temp))
            temp.clear()
        elif c == '-' and parsed_string[i + 1] == '-':
            temp.append(c)
        elif c == '-' and not parsed_string[i + 1] == '-':
            temp.append(c)
            parse_list.append(''.join(temp))
            temp.clear()
        elif c == '+' and parsed_string[i + 1] == '+':
            temp.append(c)
        elif c == '+' and not parsed_string[i + 1] == '+':
            temp.append(c)
            parse_list.append(''.join(temp))
            temp.clear()
        else:
            pass

    if neg_start:
        parse_list[0] *= -1
    # replace groups of - and + with single characters
    for i, c in enumerate(parse_list):
        if '+' in c:
            parse_list[i] = '+'
        elif '-' in c:
            if c.count('-') % 2 == 0:
                parse_list[i] = '+'
            else:
                parse_list[i] = '-'
    return parse_list


if __name__ == '__main__':
    EXT = False
    calculator = Calculator()
    while EXT is False:
        user_input = input().strip()
        if user_input.startswith('/'):
            EXT = commands(user_input)
        elif user_input == '':
            continue
        elif '=' in user_input:
            calculator.variable(user_input)
        elif user_input.isalpha():
            if user_input in calculator.variables:
                print(calculator.variables[user_input])
            else:
                print('Unknown variable')
        elif user_input.replace("-", "").isnumeric():
            print(user_input)
        elif errors(user_input):
            print('Invalid expression')
            continue
        else:
            calc = parse_input(user_input)
            print(calculator.calculate(calc))
