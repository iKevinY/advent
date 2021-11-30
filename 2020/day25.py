import sys
import fileinput


MOD = 20201227
KEYS = [int(n) for n in fileinput.input()]

card_pub = KEYS[0]
door_pub = KEYS[1]


for loop_size in range(1, MOD + 1):
    val = pow(7, loop_size, MOD)
    if val == card_pub:
        print pow(door_pub, loop_size, MOD)
        break
    elif val == door_pub:
        print pow(card_pub, loop_size, MOD)
        break
