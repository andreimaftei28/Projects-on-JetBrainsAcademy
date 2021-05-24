"""Bill splitter script. Takes number and name of guests as user input,
stores it in a dictionary and updates the values into dictionary with the amount
each guest need to pay."""


import random


# create dictionary
def bill_splitter():
    people = int(input("Enter the number of friends joining (including you):\n"))
    if people <= 0:
        return "\nNo one is joining for the party"
    splitter = {}
    print("Enter the name of every friend (including you), each on a new line:")
    for _ in range(people):
        name = input()
        splitter[name] = 0
    return splitter


# update values into guests dictionary
def update_splitter(splitter):
    if isinstance(splitter, str):
        return splitter
    bill = int(input("\nEnter the total bill value:\n"))
    lucky = input("\nDo you want to use the 'Who is lucky?' feature? Write Yes/No:\n")
    if lucky == "Yes":
        lucky = random.choice(list(splitter.keys()))
        amount = round(bill / (len(splitter) - 1), 2)
        for name in splitter:
            if name != lucky:
                splitter[name] = amount
        print(f"{lucky} is the lucky one!\n")
        return splitter
    else:
        amount = round(bill / len(splitter), 2)
        for name in splitter:
            splitter[name] = amount

        print("No one is going to be lucky")
    return splitter


print(update_splitter(bill_splitter()))
