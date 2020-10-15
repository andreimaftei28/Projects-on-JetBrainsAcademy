"""Simple banking system script generates card numbers, check's them with
Luhn algoritm add's created accounts into a database and makes simple bank operations"""
import random
import sqlite3
import sys
class BankSystem:

    def __init__(self):


        self.iin = "400000"
        self.balance = 0
        self.card_number = ""
        self.card_pin = ""


    def generate_account(self):
        """method for creating bank account and checking it with luhn algoritm"""
        card_number = []
        card_pin = []
        check_sum = "0"
        for _ in range(9):
            card_number.append(str(random.randint(0, 9)))

        #check with Luhn algoritm
        #find number to check
        iin = [int(x) for x in self.iin]
        number_to_check = iin + [int(x) for x in card_number]
        #multiply odds positions by 2
        for i in range(0, len(number_to_check), 2):
            number_to_check[i] *= 2
        #substract 9 tu numbers over 9
        for i in range(len(number_to_check)):
            if number_to_check[i] > 9:
                number_to_check[i] -= 9
        sum_number = sum(number_to_check)
        #find check_sum
        if sum_number % 10 == 0:
            check_sum = "0"
        else:
            check_sum = str(10 - (sum_number % 10))
        self.card_number = self.iin + "".join(card_number) + check_sum
        for _ in range(4):
            card_pin.append(str(random.randint(0, 9)))
        self.card_pin = "".join(card_pin)

        self.check_database()


    def create_database(self):
        """method used to create database if not exists"""
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS card (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    number TEXT,
                    pin TEXT,
                    balance INT DEFAULT 0 );""")
        conn.commit()


    def add_to_database(self):
        """method ads data when database is empty"""
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("INSERT INTO card VALUES (1, ?, ? ,?)",(self.card_number, self.card_pin, self.balance))
        conn.commit()

    def update_database(self):
        """method adds data when databes is not empty"""
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("""INSERT INTO card (number, pin, balance)
                    VALUES (?, ?, ?)""",(self.card_number, self.card_pin, self.balance))
        conn.commit()

    def check_database(self):
        """method is checking if database is empty and adds data into it"""
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM card")
        rows = cur.fetchall()
        if len(rows) == 0:
            self.add_to_database()
        else:
            self.update_database()
            conn.commit()

    def retrieve_balance(self):
        """method is used to optain balance for current account"""
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("SELECT balance FROM card WHERE (number = ?)",(self.card_number,))
        balance = cur.fetchone()
        self.balance = balance[0]
        return(self.balance)
        conn.commit()

    def retrieve_from_database(self):
        """method is used to optain all data from database"""
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM card")
        data = cur.fetchall()
        return data
        conn.commit()

    def add_income(self):
        """method for updating account's balance by the amount inputed by user"""
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("SELECT balance FROM card WHERE (number = ?)", (self.card_number,))
        balance = cur.fetchone()[0]
        message = input("Enter income:\n")
        balance += int(message)
        cur.execute("""UPDATE card
                    SET balance = ?
                    WHERE number = ? """, (balance, self.card_number,))
        print("Income was added!\n")
        conn.commit()

    def transfer_income(self):
        """method for performing a money transfer current account into another account in database"""
        data = self.retrieve_from_database()
        card_numbers = [line[1] for line in data]
        print("Transfer")
        transfer_card = input("Enter card number:\n")
        #check with Luhn algoritm
        #find number to check
        check_number = [int(x) for x in transfer_card]
        check_sum = check_number[-1]
        luhn_check = check_number[:-1]
        #multiply odds positions by 2
        for i in range(0, len(luhn_check), 2):
            luhn_check[i] *= 2
        #substract 9 tu numbers over 9
        for i in range(len(luhn_check)):
            if luhn_check[i] > 9:
                luhn_check[i] -= 9
        sum_number = sum(luhn_check) + check_sum
        if sum_number % 10 != 0:
            print("Probably you made a mistake in the card number. Please try again!\n")
        elif transfer_card == self.card_number:
            print("You can't transfer money to the same account!\n")
        elif transfer_card not in card_numbers:
            print("Such a card does not exist.\n")
        else:
            transfer_money = input("Enter how much money you want to transfer:\n")
            self.balance = self.retrieve_balance()
            if int(transfer_money) > int(self.balance):
                print("Not enough money!\n")
            else:
                conn = sqlite3.connect("card.s3db")
                cur = conn.cursor()
                cur.execute("SELECT balance FROM card WHERE (number = ?)", (transfer_card,))
                balance = cur.fetchone()[0]
                balance += int(transfer_money)
                cur.execute("""UPDATE card
                            SET balance = ?
                            WHERE number = ? """, (balance, transfer_card,))
                print("Success!\n")
                cur.execute("SELECT balance FROM card WHERE (number = ?)", (self.card_number,))
                new_balance = int(cur.fetchone()[0]) - int(transfer_money)
                cur.execute("""UPDATE card
                            SET balance = ?
                            WHERE number = ? """, (new_balance, self.card_number,))

                conn.commit()

    def close_account(self):
        """method for deleting column from database"""

        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("DELETE FROM card WHERE (number = ?)", (self.card_number,))
        print("The account has been closed!\n")
        conn.commit()

    def generate_menu(self):
        """main method of this script.Takes user input and perform tasks acordingly"""
        self.create_database()
        while True:
            home_menu = input("1. Create an account\n2. Log into account\n0. Exit\n")
            if home_menu == "1":
                self.generate_account()

                print(f"\nYour card has been created\n\
Your card number:\n{self.card_number}\nYour card PIN:\n{self.card_pin}\n")
            elif home_menu == "2":
                card_number = input("\nEnter your card number:\n")
                card_pin = input("Enter your PIN:\n")
                self.card_number = card_number
                self.card_pin = card_pin
                data = self.retrieve_from_database()
                message = ""
                card_numbers = []
                for line in data:
                    card_numbers.append(line[1])
                    if card_number in line and card_pin in line:
                        message = "\nYou have successfully logged in!\n"
                        print(message)
                        break
                else:
                    print("\nWrong card number or PIN!\n")
                if len(message) > 1:
                    submenu = ""
                    while submenu != 0:
                        submenu = input("1. Balance\n2. Add income\n3. Do transfer\n\
4. Close account\n5. Log out\n0. Exit\n")
                        if submenu == "1":
                            print(f"\nBalance: {self.retrieve_balance()}\n")
                            self.balance = self.retrieve_balance()
                            continue
                        elif submenu == "2":
                            self.add_income()
                            continue
                        elif submenu == "3":
                            self.transfer_income()
                            continue
                        elif submenu == "4":
                            self.close_account()
                            break
                        elif submenu == "5":
                            print("\nYou have successfully logged out!\n")
                            break
                        else:
                            if submenu == "0":
                                print("\nBye!\n")
                                sys.exit()
                        break

            else:
                if home_menu == "0":
                    print("\nBye!")
                    break

if __name__ == "__main__":
    card = BankSystem()

    card.generate_menu()
