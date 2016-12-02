import fileinput
import itertools
import sys
from collections import namedtuple

class Character:
    def __init__(self, name, hp, mp, dmg, armour):
        # Stats
        self.name = name
        self.hp = hp
        self.mp = mp
        self.dmg = dmg
        self.armour = armour

        # Status Effects
        self.shielded = 0
        self.poisoned = 0
        self.recharging = 0

    def print_player(self):
        print '{} has {} hit points, {} mana, {} armour'.format(self.name, self.hp, self.mp, self.armour)

    def print_boss(self):
        print '{} has {} hit points'.format(self.name, self.hp)

    def process_status(self):
        if self.shielded:
            self.shielded -= 1
            self.armour = 7
            # print "Shield's timer is now {}.".format(self.shielded)
            if self.shielded == 0:
                self.armour = 0
                # print 'Shield wears off.'

        if self.poisoned:
            self.poisoned -= 1
            self.hp -= 3
            # print 'Poison deals 3 damage; its timer is now {}.'.format(self.poisoned)
            if self.poisoned == 0:
                pass
                # print 'Poison effects expired.'

        if self.recharging:
            self.recharging -= 1
            self.mp += 101
            # print 'Recharge provides 101 mana; its timer is now {}.'.format(self.recharging)
            if self.recharging == 0:
                pass
                # print 'Recharge wears off.'


Spell = namedtuple('Spell', ['name', 'cost', 'dmg', 'heal', 'effect', 'duration'])

# Magic Missile costs 53 mana. It instantly does 4 damage.
# Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
# Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
# Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
# Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.
SPELLS = [
    Spell('Missl',  53, 4, 0,    None, None),
    Spell('Drain',  73, 2, 2,    None, None),
    Spell('Shild', 113, 0, 0, 'shielded', 6),
    Spell('Poisn', 173, 0, 0, 'poisoned', 6),
    Spell('Rchrg', 229, 0, 0, 'recharge', 5),
]


def boss_fight(player, boss, spell_order, hard_mode=False):
    spent_mana = 0
    effects = []
    # print ', '.join(s.name for s in spell_order)

    for spell in spell_order:
        if hard_mode:
            player.hp -= 1
            if player.hp <= 0:
                # print 'Player died. Game over. :('
                return sys.maxint

        # print '-- Player Turn --'
        # player.print_player()
        # boss.print_boss()

        player.process_status()
        boss.process_status()


        # Pick a spell to use
        if spell.cost > player.mp:
            # print 'Not enough mana to cast.'
            return sys.maxint

        # Disallow repeated effects
        if spell.effect == 'shielded' and player.shielded:
            return sys.maxint
        elif spell.effect == 'poisoned' and boss.poisoned:
            return sys.maxint
        elif spell.effect == 'recharge' and player.recharging:
            return sys.maxint

        # print '> iKevinY casted {}!'.format(spell.name)
        spent_mana += spell.cost
        player.mp -= spell.cost
        boss.hp -= spell.dmg


        if spell.heal:
            # print 'iKevinY healed for {} hit points.'.format(spell.heal)
            player.hp += spell.heal

        if spell.effect == 'shielded':
            player.shielded = spell.duration
        elif spell.effect == 'poisoned':
            boss.poisoned = spell.duration
        elif spell.effect == 'recharge':
            player.recharging = spell.duration

        if boss.hp <= 0:
            # print 'Boss died. You win! :)'
            print spent_mana, '@', ' '.join(s.name for s in spell_order)
            return spent_mana

        # print '-- Boss Turn --'
        # player.print_player()
        # boss.print_boss()
        player.process_status()
        boss.process_status()

        if boss.hp <= 0:
            # print 'Boss died. You win! :)'
            print spent_mana, '@', ' '.join(s.name for s in spell_order)
            return spent_mana

        # print '> Boss attacks for {} damage!'.format(max(1, boss.dmg - player.armour))
        player.hp -= max(1, boss.dmg - player.armour)
        if player.hp <= 0:
            # print 'Player died. Game over. :('
            return sys.maxint

        # print

    else:
        # Fight did not terminate
        return sys.maxint

    return spent_mana


# # HP, Damage
# boss_data = []

# for line in fileinput.input():
#     boss_data.append(int(line.split(': ')[1]))

MOST_EFFICIENT = sys.maxint

# boss = Character('BOSS', 13, 0, 8, 0)
# player = Character('iKevinY', 10, 250, 0, 0)  # 50HP, 500MP
# boss_fight(player, boss, [SPELLS[3], SPELLS[0]])

# sys.exit()

for n in range(9, 12):
    found = False
    for so in itertools.product(SPELLS, repeat=n):
        if sum(s.cost for s in so) > MOST_EFFICIENT:
            continue

        boss = Character('BOSS', 55, 0, 8, 0)  # 55hp, 8dmg INPUT
        player = Character('iKevinY', 50, 500, 0, 0)  # 50HP, 500MP

        # boss = Character('BOSS', 13, 0, 8, 0)
        # player = Character('iKevinY', 10, 250, 0, 0)  # 50HP, 500MP
        a = boss_fight(player, boss, so, hard_mode=True)

        if a < MOST_EFFICIENT:
            MOST_EFFICIENT = a
            found = True

    if found:
        break

print 'Most efficient MP: %i' % MOST_EFFICIENT
