import os
import sys
import time
import fileinput
import threading
from collections import deque

from intcode import emulate


TAPE = [int(x) for x in fileinput.input()[0].split(',')]
TAPE += [0] * 1000

VMS = 50
PACKET_QUEUES = [deque([i]) for i in range(VMS)]
NAT = [None, None]


def start_nic(pid):
    vm = emulate(TAPE, PACKET_QUEUES[pid], consume_input=True)

    while True:
        addr = next(vm)
        x = next(vm)
        y = next(vm)

        if addr == 255:
            NAT[0] = x
            NAT[1] = y
        else:
            PACKET_QUEUES[addr].extend([x, y])


def start_nat():
    first_nat = False
    seen = set()

    while True:
        if NAT[1] is not None:
            if not first_nat:
                print "First Y value sent to NAT:", NAT[1]
                first_nat = True

            if not any(PACKET_QUEUES):
                x, y = NAT
                if y in seen:
                    print "Value delivered by NAT twice in a row:", y
                    os._exit(1)
                seen.add(y)

                PACKET_QUEUES[0].extend(NAT)
                NAT[0] = None
                NAT[1] = None

        time.sleep(1)


threads = []

sys.stdout.write("Starting NICs and NAT")
for pid in range(VMS):
    t = threading.Thread(target=start_nic, args=(pid,))
    threads.append(t)
    t.start()
    sys.stdout.write(".")
    sys.stdout.flush()

t = threading.Thread(target=start_nat)
threads.append(t)
t.start()
sys.stdout.write("!\n")

for t in threads:
    t.join()
