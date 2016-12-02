import fileinput
import re

TICKER = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}

sues = [{k: int(v) for k, v in re.findall(r'(\w+): (\d+)', line)} for line in fileinput.input()]

def which_sue(sues, outdated=False):
    for i, sue in enumerate(sues, start=1):
        for key in sue:
            if outdated and (key in ('cats', 'trees')):
                if not (sue[key] > TICKER[key]):
                    break
            elif outdated and (key in ('pomeranians', 'goldfish')):
                if not (sue[key] < TICKER[key]):
                    break

            elif TICKER[key] != sue[key]:
                break
        else:
            return i
    else:
        return -1

print "The gift was from Sue #%d." % which_sue(sues)
print "With ranges gives Sue #%d." % which_sue(sues, outdated=True)
