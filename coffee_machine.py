"""this script is simulating a real world coffee machine program."""

class CoffeeMachine:
    
    def  __init__ (self, water, milk, coffee_b, cups, money):
        self.water = water
        self.milk = milk
        self.coffee_b = coffee_b
        self.cups = cups
        self.money = money

    def __str__(self):
        status = f"The coffee machine has:\n{self.water} of water\n\
{self.milk} of milk\n{self.coffee_b} of coffee beans\n\
{self.cups} of disposable cups\n${self.money} of money"

        return status

    def espresso(self):
        self.water -= 250
        self.coffee_b -= 16
        self.cups -= 1
        self.money += 4
        return self.water, self.coffee_b, self.cups, self.money


    def latte(self):
        self.water -= 350
        self.milk -= 75
        self.coffee_b -= 20
        self.cups -= 1
        self.money += 7

        return self.water, self.milk, self.coffee_b, self.cups, self.money

    def cappucinno(self):
        self.water -= 200
        self.milk -= 100
        self.coffee_b -= 12
        self.cups -= 1
        self.money += 6
        return self.water, self.milk, self.coffee_b, self.cups, self.money

    def fill(self):
        water = int(input("Write how many ml of watre do you want to add: "))
        milk = int(input("Write how many ml of milk do you want to add: "))
        coffee_b = int(input("Write how many grams of coffee beans do you want to add: "))
        cups = int(input("Write how many disposable cups of coffee do you want to add: "))
        self.water += water
        self.milk += milk
        self.coffee_b += coffee_b
        self.cups += cups
        return self.water, self.milk, self.coffee_b, self.cups

    def take(self):
        print(f"I gave you ${self.money} of money")
        self.money = 0
        return self.money



    def action(self):

        action = " "
        while action != "exit":
            CoffeeMachine.__str__(self)
            action = input("\nWrite action (buy, fill, take, remaining, exit): ")
            if action == "buy":
                message = input("\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappucinno, back - to main menu: ")
                if message  == "1":

                    if self.water < 200:
                        print("Sorry, not enough water!")
                    elif self.coffee_b < 16:
                        print("Sorry, not enough coffee beans!")
                    elif self.cups < 1:
                        print("Sorry, not enough disposable cups!")
                    else:
                        self.espresso()
                        print("I have enough resources, making a coffee!")

                elif message == "2":

                    if self.water < 350:
                        print("Sorry, not enough water!")
                    elif self.milk < 75:
                        print("Sorry, not enough milk!")
                    elif self.coffee_b < 20:
                        print("Sorry, not enough coffee beans!")
                    elif self.cups < 1:
                        print("Sorry, not enough disposable cups!")
                    else:
                        self.latte()
                        print("I have enough resources, making a coffee!")
                elif message == "3":

                    if self.water < 200:
                        print("Sorry, not enough water!")
                    elif self.milk < 100:
                        print("Sorry, not enough milk!")
                    elif self.coffee_b < 12:
                        print("Sorry, not enough coffee beans!")
                    elif self.cups < 1:
                        print("Sorry, not enough disposable cups!")
                    else:
                        self.cappucinno()
                        print("I have enough resources, making a coffee!")

                elif message == "back":
                    continue

                else:
                    print("No such option")

            elif action == "fill":
                self.fill()

            elif action == "take":
                self.take()

            elif action == "remaining":
                print(CoffeeMachine.__str__(self))







my_coffee_machine = CoffeeMachine(400, 540, 120, 9, 550)
my_coffee_machine.action()
