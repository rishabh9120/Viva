import random
from collections import defaultdict, Counter


def consistentvalue(n, tosend, faulty, printing=True):
    nodelist = defaultdict(lambda: [])
    received = defaultdict(lambda: tosend)
    commaderfaulty = False
    if 0 in faulty:
        commaderfaulty = True
    for i in range(1, n):
        if commaderfaulty:
            received[i] = random.randint(0, 1)
        else:
            received[i] = tosend

    for i in range(1, n):
        if i in faulty:
            for j in range(1, n):
                if i != j:
                    nodelist[j].append(random.randint(0, 1))
        else:
            for j in range(1, n):
                if i != j:
                    nodelist[j].append(received[i])

    ansset = set()
    for i in range(n):
        if i not in faulty:
            ansset.add(Counter(nodelist[i] + [received[i]]).most_common(1)[0][0])
            if printing:
                print(
                    f"Node {i} -> {Counter(nodelist[i]+[received[i]]).most_common(1)[0][0]}"
                )

    return len(ansset) == 1


def main():
    n = int(input("Number of nodes : "))
    print("Commander is 0")
    tosend = int(input("Value to send : "))
    faulty = set(map(int, input("Enter all the faulty nodes : ").split()))
    # n=7
    # tosend=1
    # faulty=set([1,2,3])

    print(consistentvalue(n, tosend, faulty, False))


if __name__ == "__main__":
    main()
