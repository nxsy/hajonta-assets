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
mtls = {}
num_colors = 0
for color in colors:
    lastmtl, color = color
    color = color.split()
    color = "".join("{0:02x}".format(int(float(c) * 255)) for c in color)
    #print color,
    print lastmtl, color
    mtls[lastmtl] = num_colors
    num_colors += 1

squares_per_line = 1
while squares_per_line * squares_per_line < num_colors:
    squares_per_line += 1

offsets_by_mtl = {}
offset_per_x = 1.0 / squares_per_line
offset_per_y = 1.0 / squares_per_line
for k, v in mtls.items():
    x = v % squares_per_line
    y = v / squares_per_line
    y = squares_per_line - y - 1
    offsets_by_mtl[k] = (
        float(x) / squares_per_line,
        float(y) / squares_per_line,
    )

for k, v in offsets_by_mtl.items():
    print k, v

for filename in os.listdir('.'):
    if not filename.endswith('.obj'):
        continue

    if "Brown_Cliff_Top_01_2.obj" not in filename:
        continue

    with open(filename) as f:
        with open("palettised/" + filename, "w") as fw:
            last_mtl = None
            for line in f:
                line = line.strip()
                if line.startswith("usemtl "):
                    last_mtl = line.split(" ", 1)[1]
                    line = "usemtl merged"
                if line.startswith("mtllib "):
                    line = "mtllib merged.mtl"
                if line.startswith("vt "):
                    vt = line.split(" ", 1)[1]
                    offsets = offsets_by_mtl[last_mtl]
                    vt = [float(v) for v in vt.split()]
                    vt[0] = max(0.05, vt[0])
                    vt[1] = max(0.05, vt[1])
                    vt[0] = min(0.95, vt[0])
                    vt[1] = min(0.95, vt[1])

                    vt[0] = vt[0] / squares_per_line + offsets[0]
                    vt[1] = vt[1] / squares_per_line + offsets[1]
                    line = "vt {} {}".format(vt[0], vt[1])
                print >>fw, line
