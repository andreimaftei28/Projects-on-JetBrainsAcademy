import random


def operations(*args):
    if len(args) > 1:
        var1, oper, var2 = args
        if oper == "+":
            return var1 + var2
        elif oper == "-":
            return var1 - var2
        elif oper == "*":
            return var1 * var2
    else:
        return args[0] ** 2


def int_or_float(var):
    if var == "":
        return "Incorrect format."
    try:
        if "." in var:
            return float(var)
        else:
            return int(var)
    except:
        return "Incorrect format."


def choose_level(var):
    if var not in ["1", "2"]:
        return "Incorrect format."
    return int(var)


level1 = "simple operations with numbers 2-9"
level2 = "integral squares of 11-29"
message = f"Which level do you want? Enter a number:\n1 - {level1}\n2 - {level2}\n "
user_choice = choose_level(input(message))
while user_choice == "Incorrect format.":
    print(user_choice)
    user_choice = choose_level(input(message))


def check_result(choice):
    a = 0
    for _ in range(5):
        if choice == 1:
            *args, = random.randrange(2, 10), random.choice("+-*"), random.randrange(2, 10)
        else:
            *args, = random.randrange(11, 30),
        print(*args)
        result = operations(*args)
        users_result = int_or_float(input())
        while users_result == "Incorrect format.":
            print(users_result)
            users_result = int_or_float(input())
        if users_result == result:
            a += 1
            print("Right!")
        else:
            print("Wrong!")
    return a


n = check_result(user_choice)
save_res = input(f"Your mark is {n}/5. Would you like to save the result? Enter yes or no.\n")
if save_res.lower() == "yes" or save_res.lower() == "y":
    name = input("What is your name?\n")
    with open("results.txt", "a") as file:
        file.write(f"{name}: {n}/5 in level {user_choice} ({level1 if user_choice == 1 else level2})")
        print(f'The results are saved in "{file.name}"')