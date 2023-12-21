import fileinput
from collections import defaultdict, Counter, deque
from itertools import count

from utils import mul


# Parse problem input.
broadcaster = []
flip_flops = defaultdict(list)
conjunctions = defaultdict(list)
graph = defaultdict(list)

for line in fileinput.input():
    line = line.strip()
    if line.startswith('broadcaster'):
        outputs = line.split(' -> ')[1]
        for out in outputs.split(', '):
            broadcaster.append(out)

    elif line.startswith('%'):
        mod, outputs = line.split(' -> ')
        mod = mod[1:]
        for out in outputs.split(', '):
            flip_flops[mod].append(out)
            graph[out].append(mod)

    elif line.startswith('&'):
        mod, outputs = line.split(' -> ')
        mod = mod[1:]
        for out in outputs.split(', '):
            conjunctions[mod].append(out)
            graph[out].append(mod)


def press_button(state):
    # Start the cycle with the broadcaster receiving a
    # low pulse from the button.
    horizon = deque([('broadcaster', False, 'button')])

    while horizon:
        dst, pulse, frm = horizon.popleft()

        # Output all pulses to be examined.
        yield dst, pulse

        if dst == 'broadcaster':
            for r in broadcaster:
                horizon.append((r, pulse, dst))

        elif dst in flip_flops:
            # If a flip-flop receives a high pulse, do nothing.
            if pulse is True:
                continue

            # Invert the state of the flip-flop.
            STATE[dst] = not STATE[dst]

            # Broadcast the new state to all output modules.
            for r in flip_flops[dst]:
                horizon.append((r, STATE[dst], dst))

        elif dst in conjunctions:
            # Set memory of this pulse.
            STATE[dst][frm] = pulse

            # If memory is all high pulses...
            for inp, mem in STATE[dst].items():
                if not mem:
                    break
            else:
                # ...send a low pulse to all output modules.
                for r in conjunctions[dst]:
                    horizon.append((r, False, dst))

                continue

            # Otherwise, send a high pulse to all output modules.
            for r in conjunctions[dst]:
                horizon.append((r, True, dst))


# Solve problem.
STATE = {k: False for k in flip_flops}

for mod in conjunctions:
    STATE[mod] = {inp: False for inp in graph[mod]}

# Need to find the aligned cycle of the four modules that
# feed into conjunction X, where X feeds into `rx`.
key_regs = graph[graph['rx'][0]]
cycle_lens = {mod: -1 for mod in key_regs}

pulse_counts = Counter()

for cycle in count(start=1):
    for module, pulse in press_button(STATE):
        if pulse is False and cycle_lens.get(module) == -1:
            cycle_lens[module] = cycle

        if cycle <= 1000:
            pulse_counts[pulse] += 1

    if all(v != -1 for v in cycle_lens.values()):
        break

print("Part 1:", mul(pulse_counts.values()))
print("Part 2:", mul(cycle_lens.values()))
