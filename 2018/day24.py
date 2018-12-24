import re
import copy
import fileinput

from utils import parse_line, parse_nums


class Group:
    def __init__(self, is_infection, num, _count, hp, weaknesses, immunities, dmg, type, initiative):
        self.alliance = 'Infection' if is_infection else 'Immune System'
        self.is_infection = is_infection
        self.num = num
        self.count = _count
        self.hp = hp
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.dmg = dmg + (0 if self.is_infection else BOOST)
        self.type = type
        self.initiative = initiative

    @property
    def power(self):
        return self.count * self.dmg

    def calc_dmg(self, other):
        if self.type in other.immunities:
            return 0
        elif self.type in other.weaknesses:
            return 2 * self.power
        else:
            return self.power

    def deal_dmg(self, other):
        dmg = self.calc_dmg(other)
        units_lost = min(dmg // other.hp, other.count)
        other.count -= units_lost
        return units_lost


def setup_simulation():
    immune = {}
    infect = {}
    groups = []

    for i, line in enumerate(IMMUNE):
        g = Group(False, i, *line)
        immune[i] = g
        groups.append(g)

    for i, line in enumerate(INFECT):
        g = Group(True, i, *line)
        infect[i] = g
        groups.append(g)

    return immune, infect, groups


# Read problem input
IMMUNE = []
INFECT = []
BOOST = 0
DEBUG = False

on_infection = False

for i, line in enumerate(fileinput.input()):
    line = line.strip()

    if line == 'Infection:':
        on_infection = True
        continue

    try:
        _count, hp, dmg, initiative = parse_nums(line, negatives=False)
    except Exception:
        continue
    clauses = next(iter(re.findall(r'(\(.+\))', line)), None)
    type = re.findall(r'(\S+) damage', line)
    type = next(iter(type), None)

    parts = (clauses or '').replace(',', '').replace('(', '').replace(')', '').split(';')
    weaknesses = []
    immunities = []

    if parts[0] != '':
        for part in parts:
            things = part.split()
            if things[0] == 'weak':
                weaknesses = things[2:]
            else:
                immunities = things[2:]

    group = (_count, hp, weaknesses, immunities, dmg, type, initiative)

    if on_infection:
        INFECT.append(group)
    else:
        IMMUNE.append(group)


def simulate(boost=0):
    global BOOST
    BOOST = boost
    immune, infection, groups = setup_simulation()

    last_infcount = None
    last_imscount = None

    while True:
        # Target selection
        targets = {}

        if DEBUG:
            for alliance, group in [("Immune System", immune), ("Infection", infection)]:
                print "{}:".format(alliance)
                for n, g in group.items():
                    if g.count > 0:
                        print "Group {} contains {} units".format(n, g.count)

            print

        for g in sorted(groups, key=lambda g: (g.power, g.initiative), reverse=True):
            if g.count == 0:
                continue

            other = immune if g.is_infection else infection

            target_num = None

            for h in (z for z in groups if z.alliance != g.alliance):
                if h.count == 0:
                    continue

                leave = False
                for a, b in targets.items():
                    if a[0] == g.alliance and h.num == b:
                        leave = True
                        break

                if leave:
                    continue

                if DEBUG:
                    print "{} group {} would deal defending group {} {} damage".format(g.alliance, g.num, h.num, g.calc_dmg(h))

                if g.calc_dmg(h) > 0:
                    if target_num is None:
                        target_num = h.num
                    else:
                        poss = other[target_num]
                        if g.calc_dmg(h) > g.calc_dmg(poss):
                            target_num = h.num
                        elif g.calc_dmg(h) == g.calc_dmg(poss):
                            if h.power > poss.power:
                                target_num = h.num
                            elif h.power == poss.power:
                                if h.initiative > poss.initiative:
                                    target_num = h.num

            targets[g.alliance, g.num] = target_num

        if DEBUG:
            print

        # Attack
        for g in sorted(groups, key=lambda g: g.initiative, reverse=True):
            other = immune if g.is_infection else infection
            h = other.get(targets.get((g.alliance, g.num), None), None)
            if h is None:
                continue
            killed = g.deal_dmg(h)

            if DEBUG:
                print "{} group {} attacks defending group {}, killing {} units".format(g.alliance, g.num, h.num, killed)

        if DEBUG:
            print
            print

        infcount = 0
        imscount = 0
        for g in groups:
            if g.is_infection:
                infcount += g.count
            else:
                imscount += g.count

        if infcount == 0:
            return True, imscount
        elif imscount == 0:
            return False, infcount
        elif infcount == last_infcount and imscount == last_imscount:
            return False, None

        last_infcount = infcount
        last_imscount = imscount

print "Units in the winning army:", simulate()[1]

lo = 0
hi = 1000

while lo < hi:
    mid = (lo + hi) // 2
    res, count = simulate(mid)
    if not res:
        lo = mid + 1
    else:
        hi = mid

print "Immune system units after smallest boost ({}): {}".format(mid + 1, simulate(mid + 1)[1])
