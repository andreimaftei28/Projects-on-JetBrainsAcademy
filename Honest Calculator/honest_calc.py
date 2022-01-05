# write your code here

messages = {
    0: "Enter an equation",
    1: "Do you even know what numbers are? Stay focused!",
    2: "Yes ... an interesting math operation. You've slept through all classes, haven't you?",
    3: "Yeah... division by zero. Smart move...",
    4: "Do you want to store the result? (y / n):",
    5: "Do you want to continue calculations? (y / n):",
    6: " ... lazy",
    7: " ... very lazy",
    8: " ... very, very lazy",
    9: "You are",
    10: "Are you sure? It is only one digit! (y / n)",
    11: "Don't be silly! It's just one number! Add to the memory? (y / n)",
    12: "Last chance! Do you really want to embarrass yourself? (y / n)"
}
operators = "+ - * /"
def operations(x, y, oper):
    if oper == "+":
        return x + y
    elif oper == "-":
        return x - y
    elif oper == "*":
        return x * y
    else:
        return x / y

def is_one_digit(variable):
    return variable in range(-9, 10) and int(variable) == variable

def check(x, y, z):
    msg = ""
    if is_one_digit(x) and is_one_digit(y):
        msg += messages[6]
    if (x == 1 or y == 1) and z == "*":
        msg += messages[7]
    if (x == 0 or y == 0) and z in "*+-":
        msg += messages[8]
    if msg != "":
        return messages[9] + msg
    return None

def int_or_float(variable):
    return int(variable) if isinstance(variable, int) else float(variable)

def save_memory(index, limit, result, answer):
    if is_one_digit(result):
        while index <= limit:
            if answer == "y":
                print(messages[index])
                answer = input()
                index += 1
            else:
                return memory
        else:
            return result
    return result

memory = 0
while True:
    print(messages[0])
    x, oper, y = input().split()
    if x == "M":
        x = memory
    if y == "M":
        y = memory
    try:
        x, y = (float(x) if "." in str(x) else int(x)), (float(y) if "." in str(y) else int(y))
        if oper not in operators:
            print(messages[2])
        else:
            message = check(x, y, oper)
            if message is not None:
                print(message)
            try:
                result = operations(x, y, oper)
                print(float(result))
                answer = input(messages[4] + "\n")
                while answer not in "yn":
                    answer = input(messages[4] + "\n")
                else:
                    memory = save_memory(10, 12, result, answer)
                answer = input(messages[5] + "\n")
                if answer == "n":
                    exit()
                else:
                    continue
            except ZeroDivisionError:
                print(messages[3])
    except Exception:
        print(messages[1])


