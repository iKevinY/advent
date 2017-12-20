import math
import fileinput
from copy import deepcopy
from collections import Counter


def dist(particle):
    x, y, z = particle[0]
    return math.sqrt(x**2 + y**2 + z**2)


def simulate(particles, iterations, collisions=False):
    particles = deepcopy(particles)
    closest_particle = Counter()
    destroyed = set()

    for _ in range(iterations):
        # Update particle velocities and positions
        for i, (p, v, a) in enumerate(particles):
            # Don't update destroyed particles
            if i in destroyed:
                continue

            v[0] += a[0]
            v[1] += a[1]
            v[2] += a[2]

            p[0] += v[0]
            p[1] += v[1]
            p[2] += v[2]

        if collisions:
            for i in range(len(particles)):
                if i in destroyed:
                    continue

                for j in range(i + 1, len(particles)):
                    if j in destroyed:
                        continue

                    if particles[i][0] == particles[j][0]:
                        destroyed.add(i)
                        destroyed.add(j)

        candidates = [(i, p) for i, p in enumerate(particles) if i not in destroyed]
        idx, _ = min(candidates, key=lambda x: dist(x[1]))
        closest_particle[idx] += 1

    closest, _ = closest_particle.most_common()[0]
    remaining = len(particles) - len(destroyed)

    return closest, remaining


# Read puzzle input
PARTICLES = []

for line in fileinput.input():
    parts = (x[3:-1] for x in line.strip().split(', '))
    p, v, a = ([int(n) for n in part.split(',')] for part in parts)
    PARTICLES.append([p, v, a])

# Naively guess stopping criteria (TODO: solve analytically)
print "Long-term closest particle to origin:", simulate(PARTICLES, 500)[0]
print "Number of particles after collision resolution:", simulate(PARTICLES, 50, collisions=True)[1]
