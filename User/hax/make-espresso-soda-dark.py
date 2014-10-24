#!/usr/bin/python

import re
import colorsys
import sys

def hexToFloat(hex):
    if isinstance(hex, list):
        return [ hexToFloat(x) for x in hex ]

    return int(hex, 16) / 255.0

def floatToHex(float):
    if isinstance(float, list):
        return [ floatToHex(x) for x in float ]

    return ("%X" % (float * 255)).zfill(2)

def darkVersionOf(color):
    r, g, b = hexToFloat( [color[1:3], color[3:5], color[5:7]] )

    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    prevHue = h

    r = 1.0 - r
    g = 1.0 - g
    b = 1.0 - b

    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    r, g, b = colorsys.hsv_to_rgb(prevHue, s, v)

    darkColor = "#" + "".join(floatToHex( [r, g, b] )) + color[7:]
    return darkColor


out = open("../Espresso Soda Dark.tmTheme", "w")

for line in open("../Espresso Soda.tmTheme"):
    for color in re.findall("[#][0-9a-fA-F]{6,8}", line):
        darkColor = darkVersionOf(color)

        line = line.replace(color, darkColor)

    out.write(line)

out.flush()
out.close()