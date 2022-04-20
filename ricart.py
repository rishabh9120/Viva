"""
Author: Rishabh Agrawal
Roll no.: BT18CSE054
"""
import time
from heapq import heapify, heappush, heappop
import threading
from regex import F
from requests import request
from termcolor import colored

nodelist = []
threads = []

# sleeps for t time and then executes func
def sleep_(t, func, *args):
    time.sleep(t)
    func(*args)


class node:
    def __init__(self, id, n, colour, time_) -> None:
        self.colour = colour  # colour of the printing representing this node
        self.id = id  # id of the node
        self.n = n  # total number of nodes in the system
        self.time = time_  # time of the node
        self.all = set()  # set of all nodes that have replied
        self.requests = []  # priority queue of requests
        self.toreply = []
        heapify(self.requests)

    # sends message to all nodes
    def broadcast(self, type):
        print(
            colored(
                f"{self.id} : Broadcasting {type}  at time : {self.time}", self.colour
            )
        )
        # call receive function for all nodes except self
        for i in range(self.n):
            if i != self.id:
                nodelist[self.id].send(i, type)

    # simulates the process of calling for entering critical section
    def enter(self):
        # increamenting the lamports clock and adding the request to the queue
        self.time += 1
        heappush(self.requests, (self.time, self.id))
        self.broadcast("request")

    # sending message to a node
    def send(self, ind, type):
        # types : "request" or "reply" or "confirmation"
        nodelist[ind].receive((self.time, self.id, type))

    # check if current node can enter critical section
    def check(self):
        # if all nodes have replied and the current node is the highest priority
        if len(self.all) == self.n - 1:
            print(
                colored(
                    f"{self.id} : Entering critical section ",
                    self.colour,
                )
            )
            print(colored(f"{self.id} : Exiting critical section", self.colour))
            for i in self.toreply:
                nodelist[self.id].send(i, "reply")

    # simulating receiving a msg
    def receive(self, data):
        print(
            colored(
                f"{self.id} : receives a msg of {data[2].upper()} from {data[1]} at time : {data[0]}",
                self.colour,
            )
        )
        # if the message is of type request push to heap of current node and send a reply
        if data[2] == "request":
            heappush(self.requests, (data[0], data[1]))
            requested = False
            for i in self.requests:
                if i[1] == self.id:
                    requested = True
                    break

            def func(tosend):
                nodelist[self.id].send(tosend, "reply")

            # # to simulate actual network delay we added a sleep in another thread so that program keeps running and current node is a sleep
            if not requested:
                threads.append(
                    threading.Thread(
                        target=sleep_,
                        args=(5, func, data[1]),
                    )
                )
                threads[-1].start()
            else:
                self.toreply.append(data[1])

        # if the message is of type reply add to set of all nodes that have replied
        elif data[2] == "reply":
            self.all.add(data[1])
            # print(self.all)
            self.check()


def main():
    n = int(input("Enter no of processes: "))
    colours = ["red", "green", "yellow", "blue", "magenta", "cyan"]
    for i in range(n):
        nodelist.append(node(i, n, colours[i % 6], 0))
    ch = "y"
    while ch == "y":
        pid = int(input("Enter the node id which want to execute critical section: "))
        nodelist[pid].enter()
        ch = input("some other process want to execute cs? (y/n)").lower()
    for i in threads:
        i.join()


if __name__ == "__main__":
    main()
