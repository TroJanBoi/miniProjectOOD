# ธนาคาร ที่มีการเก็บข้อมูลของผู้ใช้งานเป็นแบบ linklist
# ฝากเงิน ใช้
# id_card

import json
from rich import print
from LinkList import LinkList, Node  # ตรวจสอบให้แน่ใจว่า LinkList และ Node ถูกต้อง

class Transaction:
    def __init__(self, date, amount):
        self.date = date
        self.amount = amount

    def __repr__(self):
        return f"Transaction(date='{self.date}', amount={self.amount})"

class ATMCard:
    def __init__(self, atm_card, name, age, total, transactions):
        self.atm_card = atm_card
        self.name = name
        self.age = age
        self.total = total
        self.transactions = [Transaction(**trans) for trans in transactions]

    def __repr__(self):
        return (f"ATMCard(atm_card='{self.atm_card}', name='{self.name}', "
                f"age={self.age}, total={self.total}, transactions={self.transactions})")

with open('account.json', 'r') as file:
    data = json.load(file)

llst = LinkList()
for i in data:
    first_atm_card = i
    atm_card = ATMCard(
        atm_card=first_atm_card["atm_card"],
        name=first_atm_card["name"],
        age=first_atm_card["age"],
        total=first_atm_card["total"],
        transactions=first_atm_card["transactions"]
    )
    llst.append(atm_card)
    
llst.display()
