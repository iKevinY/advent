import fileinput
import itertools
from collections import namedtuple

Item = namedtuple('Item', ['name', 'cost', 'dmg', 'arm'])
Char = namedtuple('Character', ['hp', 'dmg', 'arm'])

# Cost, Damage, Armour
WEAPONS = [
    Item("Dagger", 8, 4, 0),
    Item("Shortsword", 10, 5, 0),
    Item("Warhammer", 25, 6, 0),
    Item("Longsword", 40, 7, 0),
    Item("Greataxe", 74, 8, 0),
]

ARMOUR = [
    Item("Leather", 13, 0, 1),
    Item("Chainmail", 31, 0, 2),
    Item("Splintmail", 53, 0, 3),
    Item("Bandedmail", 75, 0, 4),
    Item("Platemail", 102, 0, 5),
]

RINGS = [
    Item("Damage +1", 25, 1, 0),
    Item("Damage +2", 50, 2, 0),
    Item("Damage +3", 100, 3, 0),
    Item("Defense +1", 20, 0, 1),
    Item("Defense +2", 40, 0, 2),
    Item("Defense +3", 80, 0, 3),
]

# HP, Damage, Armour
boss_data = []

for line in fileinput.input():
    boss_data.append(int(line.split(': ')[1]))

BOSS = Char(*boss_data)
HP = 100

def boss_fight(player_hp, boss, weapon, armour, rings):
    player_dmg = weapon.dmg + sum(r.dmg for r in rings)
    player_arm = sum(a.arm for a in armour) + sum(r.arm for r in rings)
    player = Char(player_hp, player_dmg, player_arm)

    loadout = ', '.join((x for x in (weapon.name, ', '.join(a.name for a in armour), ', '.join(r.name for r in rings)) if x))
    loadout_cost = weapon.cost + sum(a.cost for a in armour) + sum(r.cost for r in rings)

    player_hurt = boss_hurt = 0

    while player.hp - player_hurt > 0:
        boss_hurt += max(1, player.dmg - boss.arm)

        if boss.hp - boss_hurt <= 0:
            return True, loadout_cost, loadout

        player_hurt += max(1, boss.dmg - player.arm)

    return False, loadout_cost, loadout


loadouts = []

# 1 weapon, 0-1 armour, 0-2 rings
for weapon in WEAPONS:
    for num_a in range(2):
        for armour in itertools.combinations(ARMOUR, num_a):
            for num_r in range(3):
                for rings in itertools.combinations(RINGS, num_r):
                    loadouts.append((weapon, armour, rings))


print "Optimal spend to win: {}g <{}>".format(*min((c, l) for win, c, l in (boss_fight(HP, BOSS, *l) for l in loadouts) if win))
print "Worst spend and lose: {}g <{}>".format(*max((c, l) for win, c, l in (boss_fight(HP, BOSS, *l) for l in loadouts) if not win))
