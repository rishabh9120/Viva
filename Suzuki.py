import time
from collections import deque
import random
import threading
from termcolor import colored

nodelist = []
threads = []


def sleep_(t, func):
    time.sleep(t)
    func()


class Token:
    def __init__(self, n) -> None:
        self.q = deque()
        self.LN = [0] * n


class Node:
    def __init__(self, id, n, color) -> None:
        self.n = n
        self.id = id
        self.rn = [0] * n
        self.color = color
        self.token = None
        self.insidecritial = False

    def send(self, receiver, msg):
        nodelist[receiver].receive(self.id, msg)

    def receive(self, sender, msg):
        print(colored(f"{self.id} : Received token request", self.color))
        self.rn[sender] = max(self.rn[sender], msg)
        if self.token is not None and not self.insidecritial:
            self.sendtoken(sender)

    def receivetoken(self, token):
        self.token = token
        print(colored(f"{self.id} : Received Token ", self.color))
        self.criticalsection()

    def removetoken(self):
        self.token = None

    def sendtoken(self, receiver):
        nodelist[receiver].receivetoken(self.token)
        self.removetoken()

    def broadcast(self, msg):
        for i in range(self.n):
            if i != self.id:
                self.send(i, msg)

    def acruiretoken(self):
        if self.token is not None:
            print(colored(f"Token Alredy with {self.id}", self.color))
            self.criticalsection()
        else:
            self.rn[self.id] += 1
            print(colored(f"{self.id} : Broadcasting", self.color))
            self.broadcast(self.rn[self.id])

    def enter(self):
        self.acruiretoken()

    def criticalsection(self):
        self.insidecritial = True
        print(colored(f"{self.id} : Entering Critical section", self.color))

        def func():
            print(colored(f"{self.id} : Exiting Critical section", self.color))
            self.token.LN[self.id] = self.rn[self.id]
            for i in range(self.n):
                if self.rn[i] == self.token.LN[i] + 1 and i not in self.token.q:
                    self.token.q.append(i)
            if len(self.token.q) != 0:
                self.sendtoken(self.token.q.popleft())
            self.insidecritial = False

        threads.append(
            threading.Thread(
                target=sleep_,
                args=(
                    random.randint(2, 7),
                    func,
                ),
            )
        )
        threads[-1].start()


def main():
    colours = ["red", "green", "yellow", "blue", "magenta", "cyan"]
    n = int(input("Enter Number of nodes :"))
    token = Token(n)
    for i in range(n):
        nodelist.append(Node(i, n, colours[i % 6]))

    # initilising token with node 0
    nodelist[0].token = token

    ch = "y"
    while ch == "y":
        pid = int(input("Enter the node id which want to execute critical section: "))
        nodelist[pid].enter()
        ch = input("some other process want to execute cs? (y/n)").lower()

    for i in threads:
        i.join()


if __name__ == "__main__":
    main()
