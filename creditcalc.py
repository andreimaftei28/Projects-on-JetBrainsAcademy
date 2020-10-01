"""Script for a basic loan calculator.It can calculate both annuity and
differentiated interest.Based on info entered it can return: monthly payment, total loan, overpayment or period"""

import math
import sys



def n_months(loan_p, m_payment, interest):
    """Function calculates number of months in wich user will repay loan
    and prints result in years and months"""
    i = interest / 1200
    n = math.ceil(math.log((m_payment / (m_payment - i * loan_p)), 1 + i))
    overpayment = int(m_payment * n - loan_p)
    if n % 12 == 0 and n / 12 >= 2:
        print(f"It will take {n // 12} years to repay this loan!")
    elif n / 12 == 1:
        print(f"It will take {n // 12} year to repay this loan!")
    elif n / 12 < 1:
        if n % 12 == 1:
            print(f"It will take {n % 12} month to repay this loan!")
        else:
            print(f"It will take {n % 12} months to repay this loan!")
    else:
        if n / 12 > 2 and n % 12 > 1:
            print(f"It will take {n // 12} years and {n % 12} months to repay this loan!")
        else:
            print(f"It will take {n // 12} years and {n % 12} month to repay this loan!")

    print("Overpayment = ", overpayment)


def annuity_payment(loan_p, periods, interest):
    """Function calculates the amount that user has to pay monthly in order to repay his loan
    It also prints the overpay amount"""
    i = interest / 1200
    a = math.ceil(loan_p * (i * math.pow((1+i), periods) / (math.pow((1+i), periods) - 1)))
    overpayment = int((a * periods) - loan_p)
    print(f"Your annuity payment = {a}!\nOverpayment = {overpayment}")

def calculate_loan(annuity_p, periods, interest):
    """Function calculates the amount of users initialy loan and
    the overpay"""
    i = interest / 1200
    loan = math.floor(annuity_p / ((i * math.pow((1 + i), periods) / (math.pow((1 + i), periods) - 1))))
    overpayment = int(annuity_p * periods - loan)
    print(f"Your loan principal = {loan}!\nOverpayment = {overpayment}")

def diff_payment(loan_p, periods, interest):
    """Function calculates differentiated monthly payment"""

    i = interest / 1200
    overpayment = 0
    for m in range(1, periods + 1):
        d_m = math.ceil((loan_p / periods) + i * (loan_p - ((loan_p * (m - 1)) / periods)))
        overpayment += d_m
        print(f"Month {m}: payment is {(d_m)}")
    print(f"\nOverpayment = {int(overpayment - loan_p)}")

def main():
    """Main function calls the other functions based on info set by user"""
    args = sys.argv
    if len(args) != 5:
        print("Incorrect parameters")
    else:
        typo = args[1].split("=")[1]
        principal = float(args[2].split("=")[1])
        periods = int(args[3].split("=")[1])
        payment = int(args[3].split("=")[1])
        interest = float(args[4].split("=")[1])

        list_args = []
        for arg in args:
            list_args.append(arg.split("=")[0][2:])
        list_args.pop(0)

        if "interest" not in list_args:
            print("Incorrect parameters")
        elif periods <= 0 or interest <= 0:
            print("Incorrect parameters")
        else:

            if typo == "diff":
                if  "payment" in list_args:
                    print("Incorrect parameters")
                else:
                    diff_payment(principal, periods, interest)

            elif typo == "annuity":
                if "periods" not in list_args:
                    n_months(principal, payment, interest)
                elif "payment" not in list_args:
                    annuity_payment(principal, periods, interest)
                else :
                    payment_n = float(args[2].split("=")[1])
                    calculate_loan(payment_n, periods, interest)


main()
