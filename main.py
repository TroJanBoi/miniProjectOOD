# ธนาคาร ที่มีการเก็บข้อมูลของผู้ใช้งานเป็นแบบ linklist
# ฝากเงิน ใช้
# id_card

import json
from rich import print
from LinkList import LinkList, Node
from datetime import date

class Slips:
    def __init__(self, date, amount, transaction):
        self.date = date
        self.amount = amount
        self.transaction = transaction

    def __repr__(self):
        return f"Slips(date='{self.date}', amount={self.amount}, transaction={self.transaction}"

class Transaction:
    def __init__(self, linklist):
        self.linklist = linklist
    
    def check_info(self, atm_card):
        currentNode = self.linklist.head
        while currentNode:
            if currentNode.data.atm_card == atm_card:
                print(currentNode.data)
                return
            currentNode = currentNode.next
        print("[red]ATM card not found![/red]")

    def deposit(self, atm_card, amount):
        currentNode = self.linklist.head
        while currentNode:
            if currentNode.data.atm_card == atm_card:
                currentNode.data.total += amount
                currentNode.data.slips.append(Slips(date=date.today(), amount=amount, transaction="deposit"))
                print(f"[green]Deposit successfull! New Balance: {currentNode.data.total}[/green]")
                return
            currentNode = currentNode.next
        print("[red]ATM card not found![/red]")

    def withdraw(self, atm_card, amount):
        currentNode = self.linklist.head
        while currentNode:
            if currentNode.data.atm_card == atm_card:
                if currentNode.data.total > 100:
                    if currentNode.data.total > amount:
                        currentNode.data.total -= amount
                        currentNode.data.slips.append(Slips(date=date.today(), amount=amount, transaction="withdraw"))
                        print(f"[green]Withdraw successfull! New Balance: {currentNode.data.total}[/green]")
                        return
                    else:
                        print(f"[red]Your account has insufficient money.[/red]")
                        return
                else:
                    print(f"[red]Your account has insufficient money.[/red]")
                    return
            else:
                print("[red]ATM card not found![/red]")


class ATMCard:
    def __init__(self, atm_card, password, name, age, total, slips):
        self.atm_card = atm_card
        self.password = password
        self.name = name
        self.age = age
        self.total = total
        self.slips = [Slips(**trans) for trans in slips]

    def __repr__(self):
        return (
            f"atm_card='{self.atm_card}'\n"
            f"password='{self.password}'\n"
            f"name='{self.name}'\n"
            f"age={self.age}\n"
            f"total={self.total}\n"
            f"Slips={self.slips}"
        )

class Menu:  
    def __init__(self):
        print("-----MENU-----")
        print("[1] [green]check info[/green]")
        print("[2] deposit")
        print("[3] [red]withdraw[/red]")
        print("---------------")


def check_type_amount(content):
    while True:
        try:
            amount = int(input(f"Enter amount to {content}: "))
            if amount <= 0:
                print("Amount must be greater than zero. Please try again.")
            else:
                return amount
        except ValueError:
            print("Invalid input. Please enter a valid number.")

with open('account.json', 'r') as file:
    data = json.load(file)

llst = LinkList()
for i in data:
    first_atm_card = i
    atm_card = ATMCard(
        atm_card=first_atm_card["atm_card"],
        password=first_atm_card["password"],
        name=first_atm_card["name"],
        age=first_atm_card["age"],
        total=first_atm_card["total"],
        slips=first_atm_card["slips"]
    )
    llst.append(atm_card)

# print(__name__)
if __name__ == "__main__":
    trans = Transaction(llst)
    while True:
        data = input("ATM Card : ")
        if llst.search_card(data):
            # print("[green]success atm card[/green]")
            quickTime = 0
            while quickTime < 3:
                password = input("Password : ")
                if llst.check_password(data, password):
                    # print("[green]success password[/green]")
                    state = True
                    while state:
                        Menu()
                        choice = input("Choose: ")
                        match choice:
                            case "1":
                                trans.check_info(data)
                            case "2":
                                amount = check_type_amount("deposit")
                                trans.deposit(data, amount)
                            case "3":
                                amount = check_type_amount("withdraw")
                                trans.withdraw(data, amount)
                            case "0":
                                exit()
                            case _:
                                print("[yellow]Please select [1 -3][/yellow]")
                else:
                    quickTime += 1
                    if quickTime < 3:
                        print("[yellow]Please Try Again![/yellow]")
                    else:
                        print("[red]You have entered the wrong input 3 times. Access denied.[/red]")
                        break
        else:
            print("[red]Failed[/red]")
# กรณี เช็คว่า ATM card นี้มีอยู่ใน ระบบไหม
# data = input()
# if llst.search_card(data):
#     print("success")
# else:
#     print("failed")