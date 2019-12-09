import fileinput
from collections import Counter

WIDTH = 25
HEIGHT = 6
IMAGE = fileinput.input()[0].strip()

layers = []
layer_size = WIDTH * HEIGHT
num_layers = len(IMAGE) / layer_size

final_image = [[None for _ in range(WIDTH)] for _ in range(HEIGHT)]


for i in range(num_layers):
    layer = Counter()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            idx = (i * layer_size) + (y * WIDTH + x)
            c = IMAGE[idx]
            layer[c] += 1

            if final_image[y][x] is None:
                if c != '2':
                    final_image[y][x] = '#' if c == '1' else ' '

    layers.append(layer)

fewest_zeros = min(layers, key=lambda l: l['0'])
print "Image checksum:", fewest_zeros['1'] * fewest_zeros['2']
print

for row in final_image:
    print ''.join(row)
