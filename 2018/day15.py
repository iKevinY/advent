import copy
import fileinput
from itertools import count

from utils import Point


class Entity:
    def __init__(self, x, y, type):
        self.pos = Point(x, y)
        self.hp = 200
        self.type = type

    def __str__(self):
        return "{}({} @ {},{})".format(self.type, self.hp, self.pos.x, self.pos.y)


GRID = {}
ENTITIES = []

for y, line in enumerate(fileinput.input()):
    for x, t in enumerate(line.strip()):
        if t == 'G' or t == 'E':
            ENTITIES.append(Entity(x, y, t))
            GRID[Point(x, y)] = '.'
        else:
            GRID[Point(x, y)] = t


def simulate(elf_dmg=3):
    grid = copy.deepcopy(GRID)
    entities = copy.deepcopy(ENTITIES)
    elves = set(e.pos for e in entities if e.type == 'E')
    goblins = set(e.pos for e in entities if e.type == 'G')

    def dmg(u):
        if u == 'E':
            return elf_dmg
        else:
            return 3

    def dist(p, q):
        horizon = [p]
        seen = set()

        depth = 0
        while horizon:
            next_horizon = []
            for h in horizon:
                if h == q:
                    return depth

                for n in h.neighbours_4():
                    if n in seen:
                        continue

                    if free(n):
                        next_horizon.append(n)
                        seen.add(n)

            horizon = next_horizon
            depth += 1

        return 1e8

    def free(p):
        return grid.get(p) == '.' and p not in goblins and p not in elves

    for curr_round in count():
        entities.sort(key=lambda u: (u.pos.y, u.pos.x))
        dead = set()

        for i, unit in enumerate(entities):
            if i in dead:
                continue

            enemies = goblins if unit.type == 'E' else elves
            selves = goblins if unit.type == 'G' else elves

            # First, attempt to attack if there are nearby enemies
            attack_can = [n for n in unit.pos.neighbours_4() if n in enemies]
            if attack_can:
                okays = []
                for j, qnit in enumerate(entities):
                    if qnit.pos in attack_can and unit.type != qnit.type:
                        okays.append((qnit, j))
                qnit, j = sorted(okays, key=lambda (qnit, j): (qnit.hp, qnit.pos.y, qnit.pos.x))[0]

                qnit.hp -= dmg(unit.type)
                if qnit.hp <= 0:
                    enemies.remove(qnit.pos)
                    dead.add(j)

                    if not enemies:
                        import sys
                        rr = curr_round
                        if i == len(entities) - len(dead):
                            rr += 1
                        score = sum(u.hp for u in entities if u.type == unit.type)
                        return rr * score, unit.type

                # Process next entity, since we can't attack and then move
                continue

            # Otherwise, move according to pathfinding algorithm
            in_range = set()
            for e in enemies:
                for n in e.neighbours_4():
                    if free(n):
                        in_range.add(n)

            horizon = [unit.pos]
            seen = set()

            next_spot = None

            while horizon:
                found = set()
                next_horizon = []
                for h in horizon:
                    for n in h.neighbours_4():
                        if n in seen:
                            continue

                        if free(n):
                            next_horizon.append(n)
                            seen.add(n)
                            if n in in_range:
                                found.add(n)

                if found:
                    next_spot = sorted(found, key=lambda zz: (zz.y, zz.x))[0]

                    poss = []
                    for n in unit.pos.neighbours_4():
                        if free(n):
                            poss.append((dist(n, next_spot), n))

                    poss.sort(key=lambda z: (z[0], z[1].y, z[1].x))

                    next_spot = poss[0][1]

                    selves.remove(unit.pos)
                    selves.add(next_spot)

                    unit.pos = next_spot if next_spot is not None else unit.pos
                    break

                horizon = next_horizon

            # Now try attacking again
            attack_can = [n for n in unit.pos.neighbours_4() if n in enemies]
            if attack_can:
                # Attack
                okays = []
                for j, qnit in enumerate(entities):
                    if qnit.pos in attack_can and unit.type != qnit.type:
                        okays.append((qnit, j))
                qnit, j = sorted(okays, key=lambda (qnit, j): (qnit.hp, qnit.pos.y, qnit.pos.x))[0]

                qnit.hp -= dmg(unit.type)
                if qnit.hp <= 0:
                    enemies.remove(qnit.pos)
                    dead.add(j)

                    if not enemies:
                        import sys
                        rr = curr_round
                        if i == len(entities) - len(dead):
                            rr += 1
                        score = sum(u.hp for u in entities if u.type == unit.type)
                        return rr * score, unit.type

        # Clean up any entities who have died
        for j in reversed(sorted(dead)):
            del entities[j]


print "Outcome of initial simulation:", simulate()[0]
print "Outcome of elf victory:", simulate(elf_dmg=23)[0]
