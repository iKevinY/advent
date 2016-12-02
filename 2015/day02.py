import fileinput

paper = 0
ribbon = 0

for line in fileinput.input():
    l, w, h = [int(n) for n in line.strip().split('x')]
    a, b, c = l*w, w*h, h*l

    paper += 2*(a+b+c) + min(a, b, c)
    ribbon += (l*w*h) + 2*(l+w+h - max(l, w, h))

print "ft^2 of paper: %d" % paper
print "Feet of ribbon: %d" % ribbon
