#!/usr/bin/env python2

import os

colors = set()

for filename in os.listdir('.'):
    if not filename.endswith('.mtl'):
        continue
    with open(filename) as f:
        last_mtl = None
        for line in f:
            line = line.strip()
            if line.startswith("newmtl "):
                last_mtl = line.split(" ", 1)[1]
            if line.startswith("Kd "):
                color = line.split(" ", 1)[1]
                colors.add((last_mtl, color))

colors = list(colors)
colors.sort()
for color in colors:
    lastmtl, color = color
    color = color.split()
    color = "".join("{0:02x}".format(int(float(c) * 255)) for c in color)
    print color,
    #print lastmtl, color
