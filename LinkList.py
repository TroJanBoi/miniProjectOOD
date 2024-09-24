from rich import print

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkList:
    def __init__(self):
        self.head = None

    def append(self, data):
        newNode = Node(data)
        if self.head == None:
            self.head = newNode
        else:
            currentNode = self.head
            while currentNode.next:
                currentNode = currentNode.next
            currentNode.next = newNode

    def display(self):
        currentNode = self.head
        while currentNode:
            print(currentNode.data)
            currentNode = currentNode.next
    
    def search_card(self, atm_card):
        currentNode = self.head
        while currentNode:
            if currentNode.data.atm_card == atm_card:
                return (True)
            currentNode = currentNode.next
        return (False)
    
    def check_password(self, atm_card, password):
        currentNode = self.head
        while currentNode:
            if currentNode.data.atm_card == atm_card:
                if currentNode.data.password == password:
                    return (True)
                else:
                    return (False)
            currentNode = currentNode.next
        return (False)