import fileinput
from collections import deque

from utils import mul, parse_nums


# Parse input.
BLUEPRINTS = []

for line in fileinput.input():
    BLUEPRINTS.append(parse_nums(line))


def simulate(bp, max_time=24):
    id_num, ore_cost, clay_cost, ob_ore, ob_clay, geo_ore, geo_ob = bp

    # Pruning Heuristic #1: Cap Resources
    #
    # Since we can only build one robot per minute, at a certain point,
    # we will have so much of a resource that collecting any more will
    # make no effective difference to the end goal of mining geodes.
    #
    # In order to keep the search space smaller, cap the number of the
    # lower-level resources based on trial-and-error multipliers on the
    # resource costs of the various robots.
    MAX_ORE_MULTIPLIER = 1.5
    MAX_CLAY_MULTIPLER = 1.5
    MAX_OB_MULTIPLIER = 1

    max_ore = (ore_cost + clay_cost + ob_ore + geo_ore) * MAX_ORE_MULTIPLIER
    max_clay = ob_clay * MAX_CLAY_MULTIPLER
    max_ob = geo_ob * MAX_CLAY_MULTIPLER

    # minutes, ore_bots, clay_bots, ob_bots, geo_bots, ore, clay, ob, geo
    state = (1, 1, 0, 0, 0, 0, 0, 0, 0)
    horizon = deque([state])
    seen = {}

    best = 0

    while horizon:
        state = horizon.popleft()
        minutes, ore_bots, clay_bots, ob_bots, geo_bots, ore, clay, ob, geo = state

        # Cap resources before checking/saving state.
        ore = min(ore, max_ore)
        clay = min(clay, max_clay)
        max_ob = min(ob, max_ob)

        key = (minutes, ore_bots, clay_bots, ob_bots, geo_bots)
        val = (ore, clay, ob, geo)
        if key in seen:
            if all(a <= b for a, b in zip(val, seen[key])):
                continue

        if minutes >= max_time + 1:
            if geo > best:
                best = geo
            continue

        seen[key] = val

        next_poss = []

        # Pruning Heuristic #2: Limit Lower Bots
        #
        # Once we get to the "late-game" and are building geode robots,
        # building additional ore or clay (and even obsidian) bots becomes
        # a waste, as it doesn't help improve the ability to build geode
        # robots as quickly as possible.
        #
        # We define some heuristics based on when to stop building the
        # lower-level bots, based on how many geode robots we have.
        GEO_ORE_STOPPAGE = 1
        GEO_CLAY_STOPPAGE = 1
        GEO_OB_STOPPAGE = 7

        # Build a geode bot.
        if ore >= geo_ore and ob >= geo_ob:
            ns = minutes + 1, ore_bots, clay_bots, ob_bots, geo_bots + 1, ore - geo_ore, clay, ob - geo_ob, geo
            next_poss.append(ns)

        # Build an obsidian bot.
        if ore >= ob_ore and clay >= ob_clay and geo_bots < GEO_OB_STOPPAGE:
            ns = minutes + 1, ore_bots, clay_bots, ob_bots + 1, geo_bots, ore - ob_ore, clay - ob_clay, ob, geo
            next_poss.append(ns)

        # Build a clay bot.
        if ore >= clay_cost and geo_bots < GEO_CLAY_STOPPAGE:
            ns = minutes + 1, ore_bots, clay_bots + 1, ob_bots, geo_bots, ore - clay_cost, clay, ob, geo
            next_poss.append(ns)

        # Build an ore bot.
        if ore >= ore_cost and geo_bots < GEO_ORE_STOPPAGE:
            ns = minutes + 1, ore_bots + 1, clay_bots, ob_bots, geo_bots, ore - ore_cost, clay, ob, geo
            next_poss.append(ns)

        # Don't build anything; just accrue resources.
        if ore < max_ore:
            ns = minutes + 1, ore_bots, clay_bots, ob_bots, geo_bots, ore, clay, ob, geo
            next_poss.append(ns)

        # Actually acquire resources.
        for ns in next_poss:
            m, oreb, clayb, obb, geob, ore, clay, ob, geo = ns
            horizon.append((m, oreb, clayb, obb, geob, ore + ore_bots, clay + clay_bots, ob + ob_bots, geo + geo_bots))

    return best


quality_levels = [simulate(bp, max_time=24) * bp[0] for bp in BLUEPRINTS]
print("Part 1:", (sum(quality_levels)))

part_2 = [simulate(bp, max_time=32) for bp in BLUEPRINTS[:3]]
part_2.sort(reverse=True)
print("Part 2:", mul(part_2))
