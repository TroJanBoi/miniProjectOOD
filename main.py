import json
from rich import print
from datetime import date

class BankSystem:
    def __init__(self, accounts, json_handle):
        self.accounts = accounts
        self.json_handle = json_handle
    
    def authenticate_atm_card(self, atm_card):
        for account in self.accounts:
            if account.atm_card == atm_card:
                return True
        return False
    
    def authenticate_password(self, atm_card, password):
        for account in self.accounts:
            if account.atm_card == atm_card and account.password == password:
               return True
        return False

    def check_info(self, atm_card):
        for account in self.accounts:
            if account.atm_card == atm_card:
                print(f"[#00ff04]ATM Card[/#00ff04]: [white]{account.atm_card}[/white]")
                print(f"[cyan]Age[/cyan]: [white]{account.age}[/white]")
                print(f"[#ffa500]Total[/#ffa500]: [white]{account.total}[/white]")
                Message().msg_slip(account.slips)
                return
        print("[red]ATM card not found![/red]")

    def check_type_amount(self, content):
        while True:
            try:
                amount = int(input(f"Enter amount to {content}: "))
                if amount <= 0:
                    print("Amount must be greater than zero. Please try again.")
                else:
                    return amount
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def deposit(self, atm_card, amount):
        for account in self.accounts:
            if account.atm_card == atm_card:
                account.total += amount
                account.slips.append(Slips(date=date.today(), amount=amount, transaction="deposit"))
                print(f"[green]Deposit successful! New Balance: {account.total}[/green]")

                self.json_handle.update_json_file(self.accounts)
                return
        print("[red]ATM card not found![/red]")

    def withdraw(self, atm_card, amount):
        for account in self.accounts:
            if account.atm_card == atm_card:
                if account.total >= 100 and amount >= 100:
                    if account.total >= amount:
                        account.total -= amount
                        account.slips.append(Slips(date=date.today(), amount=amount, transaction="withdraw"))
                        print(f"[green]Withdraw successful! New Balance: {account.total}[/green]")

                        self.json_handle.update_json_file(self.accounts)
                        return
                    else:
                        print(f"[red]Your account has insufficient money.[/red]")
                        return
                else:
                    print(f"[red]Your account has insufficient money.[/red]")
                    return
        print("[red]ATM card not found![/red]")

    def transfer(self, atm_card):
        i = 0
        while i < 3:
            recipient_card = input("Recipient ATM card: ")
            recipient_account = None
            sender_account = None

            for account in self.accounts:
                if account.atm_card == recipient_card:
                    recipient_account = account
                    break

            if recipient_account and atm_card != recipient_card:
                for account in self.accounts:
                    if account.atm_card == atm_card:
                        sender_account = account
                        break

                if sender_account:
                    amount = self.check_type_amount("transfer")
                    
                    if sender_account.total >= amount and amount >= 100:
                        sender_account.total -= amount
                        sender_account.slips.append(Slips(date=date.today(), amount=amount, transaction="transfer"))
                        recipient_account.total += amount
                        self.json_handle.update_json_file(self.accounts)
                        print("[green]Transfer successful![/green]")
                        return
                    else:
                        print(f"[red]Insufficient funds or amount is less than 100.[/red]")
                        return
            elif atm_card == recipient_card:
                print("[yellow]Cannot transfer to the same account! Please try again.[/yellow]")
            else:
                i += 1
                if i < 3:
                    print("[yellow]Recipient ATM card not found! Please try again.[/yellow]")

        if i == 3:
            print("[red]Recipient ATM card not found after 3 attempts! Transfer failed.[/red]")
            return

class Message:  
    def menu(self):
        print("-----MENU-----")
        print("[1] [green]check info[/green]")
        print("[2] [yellow]deposit[/yellow]")
        print("[3] [red]withdraw[/red]")
        print("[4] [blue]Transfer[/blue]")
        print("[0] Exit")
        print("---------------")

    def msg_slip(self, slips):
        if slips:
            print("[#00ff04]Transaction History[/#00ff04]")
            for slip in slips:
                print(f"[#ff00dd]Date[/#ff00dd]: [white]{slip.date}[/white], [#ff9900]Amount[/#ff9900]: [white]{slip.amount}[/white], [#0015ff]Transaction[/#0015ff]: [white]{slip.transaction}[/white]")
        else:
            print("[#00ff04]No transaction history available.[/#00ff04]")

class Slips:
    def __init__(self, date, amount, transaction):
        self.date = date
        self.amount = amount
        self.transaction = transaction

    def __repr__(self):
        return f"Slips(date='{self.date}', amount={self.amount}, transaction={self.transaction}"

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

class JSON:
    def __init__(self, filename='account.json'):
        self.filename = filename

    def update_json_file(self, account_list):
            data = []
            for account in account_list:
                account_dict = {
                    "atm_card": account.atm_card,
                    "password": account.password,
                    "name": account.name,
                    "age": account.age,
                    "total": account.total,
                    "slips": [{"date": str(slip.date), "amount": slip.amount, "transaction": slip.transaction} for slip in account.slips]
                }
                data.append(account_dict)
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=4)

    def load_file(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)

        account_list = []
        for account_dict in data:
            account = ATMCard(
                atm_card=account_dict["atm_card"],
                password=account_dict["password"],
                name=account_dict["name"],
                age=account_dict["age"],
                total=account_dict["total"],
                slips=account_dict["slips"]
            )
            account_list.append(account)

        return account_list
    
if __name__ == "__main__":
    json_handle = JSON()
    account = json_handle.load_file()
    system = BankSystem(account, json_handle)
    msg = Message()
    while True:
        atm_card = input("ATM Card: ")
        if system.authenticate_atm_card(atm_card):
            quick_time = 0
            stat = True
            while quick_time < 3:
                if stat == True:
                    password = input("Password: ")
                else:
                    break
                if system.authenticate_password(atm_card, password):
                    while True:
                        msg.menu()
                        choice = input("choose: ")
                        
                        match choice:
                            case '1':
                                system.check_info(atm_card)
                            case '2':
                                amount = system.check_type_amount("deposit")
                                system.deposit(atm_card, amount)
                            case '3':
                                amount = system.check_type_amount("withdraw")
                                system.withdraw(atm_card, amount)
                            case '4':
                                system.transfer(atm_card)
                            case '0':
                                stat = False
                                break
                            case _:
                                print("[yellow]Please select [1 -3][/yellow]")
                else:
                    quick_time += 1
                    if quick_time < 3:
                        print("[yellow]Please Try Again![/yellow]")
                    else:
                        print("[red]You have entered the wrong input 3 times. Access denied.[/red]")
                        break
        else:
            print("[red]Failed[/red]")