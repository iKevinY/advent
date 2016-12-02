import fileinput
import re

VOWELS = {'a', 'e', 'i', 'o', 'u'}
NAUGHTY = {'ab', 'cd', 'pq', 'xy'}

nice_count_1 = 0
nice_count_2 = 0

for string in fileinput.input():
    # Ruleset 1
    num_letters = len(string)
    num_vowels = 0
    double_letter = False

    for i, char in enumerate(string):
        if char in VOWELS:
            num_vowels += 1

        if i < num_letters - 1:
            if char + string[i+1] in NAUGHTY:
                break

            if char == string[i+1]:
                double_letter = True

    else:
        if double_letter and (num_vowels >= 3):
            nice_count_1 += 1


    # Ruleset 2
    overlap = False
    is_pair = False

    for i, char in enumerate(string):
        if i < len(string) - 2:
            if char == string[i+2]:
                overlap = True
                break

    if re.search(r'(..).*\1', string):
        is_pair = True


    if overlap and is_pair:
        nice_count_2 += 1


print "Number of nice strings (first ruleset): %d" % nice_count_1
print "Number of nice strings (second ruleset): %d" % nice_count_2
