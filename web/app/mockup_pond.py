#!/usr/bin/env python3
"""Still of the FM-1 pond screen, Rain, playing. Drawn with the shapes the device has:
filled ellipses, rings, and text. 240x240, saved at 3x."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from math import cos, sin, pi, sqrt

ROOT = Path(__file__).resolve().parents[2]

S = 3
W = 240
BG = (14, 42, 34)
LINE = (46, 96, 72)
DIM = (126, 164, 132)
TEXT = (232, 240, 214)
ACC = (176, 214, 112)
PAD = (186, 214, 96)
PAD_T = (62, 118, 70)
BELL = (150, 214, 168)
PULSE = (214, 228, 164)
BANK = (36, 90, 84)
WATER = (12, 44, 48)
DEEP = (8, 28, 34)
SHORE = (22, 64, 58)

# pitch class -> (x, y) in the 144px play area, then a notch angle
PADS = [
    (62, 100, 0.4), (128, 116, 1.2), (94, 108, -0.6), (48, 72, 0.9),
    (34, 96, 2.2), (168, 104, -0.3), (196, 96, 1.6), (154, 56, 0.2),
    (104, 44, -1.1), (72, 52, 0.7), (184, 74, -0.8), (172, 40, 1.9),
]
# C Dorian: C D Eb F G A Bb
SCALE = {0, 2, 3, 5, 7, 9, 10}
CHORD = {0, 3, 7, 10}  # Cm7
ROOT = 0
# ripples and a drip splash, in play-area coordinates
RIPPLES = [(86, 86, 13), (148, 66, 10)]
SPLASH = (132, 98)

FONT_B = str(ROOT / "base/assets/fonts/BarlowSemiCondensed-Bold.ttf")
FONT_S = str(ROOT / "base/assets/fonts/BarlowSemiCondensed-SemiBold.ttf")
FONT_M = str(ROOT / "base/assets/fonts/BarlowSemiCondensed-Medium.ttf")


def sc(x):
    return int(round(x * S))


def ell(d, box, fill, outline=None, width=1):
    d.ellipse([sc(v) for v in box], fill=fill, outline=outline, width=max(1, sc(width)) if outline else 1)


def ring(d, cx, cy, r, col, width=1.4):
    ell(d, (cx - r, cy - r, cx + r, cy + r), None, col, width)


def pad(d, x, y, rx, ry, rot, fill):
    # raster a rotated ellipse into a small overlay
    m = int(max(rx, ry) + 3)
    img = Image.new("RGBA", ((2 * m + 1) * S, (2 * m + 1) * S), (0, 0, 0, 0))
    px = img.load()
    c, s = cos(rot), sin(rot)
    for iy in range(img.size[1]):
        for ix in range(img.size[0]):
            dx = (ix + 0.5) / S - m
            dy = (iy + 0.5) / S - m
            lx, ly = dx * c + dy * s, -dx * s + dy * c
            if (lx / rx) ** 2 + (ly / ry) ** 2 <= 1:
                px[ix, iy] = (*fill, 255)
    # the slit
    sd = ImageDraw.Draw(img)
    ang = -0.5
    x2 = m + cos(ang) * rx * 0.95
    y2 = m + sin(ang) * ry * 0.95
    sd.line([(sc(m), sc(m)), (sc(x2), sc(y2))], fill=(*WATER, 255), width=max(1, sc(1.3)))
    im.paste(img, (sc(x - m), sc(y - m)), img)


im = Image.new("RGB", (W * S, W * S), BG)
dr = ImageDraw.Draw(im)
fb = ImageFont.truetype(FONT_B, sc(15))
fs = ImageFont.truetype(FONT_S, sc(13))
fxs = ImageFont.truetype(FONT_M, sc(11))
fb_sm = ImageFont.truetype(FONT_B, sc(13))

# header
dr.rounded_rectangle([sc(4), sc(4), sc(4 + 52), sc(24)], radius=sc(6), fill=TEXT)
dr.text((sc(10), sc(4)), "Rain", font=fb, fill=BG)
dr.text((sc(66), sc(7)), "C", font=fxs, fill=TEXT)
dr.text((sc(78), sc(7)), "Dorian", font=fxs, fill=DIM)
dr.ellipse([sc(168), sc(9), sc(178), sc(19)], fill=PAD)
dr.text((sc(184), sc(5)), "76", font=fs, fill=TEXT)
# battery
dr.rounded_rectangle([sc(208), sc(9), sc(226), sc(19)], radius=sc(2), outline=DIM, width=max(1, S))
dr.rectangle([sc(210), sc(11), sc(224), sc(17)], fill=BG)
dr.rectangle([sc(226), sc(12), sc(228), sc(16)], fill=DIM)
for i in range(3):
    dr.rectangle([sc(211 + i * 5), sc(12), sc(214 + i * 5), sc(16)], fill=PAD)

# play area origin
OY = 28
cx, cy = 120, OY + 78
# far bank, then the water, then a deeper middle
ell(dr, (cx - 110, cy - 68, cx + 110, cy + 56), BANK)
ell(dr, (cx - 104, cy - 58, cx + 104, cy + 50), SHORE)
ell(dr, (cx - 98, cy - 50, cx + 98, cy + 46), WATER)
ell(dr, (cx - 46, cy - 8, cx + 46, cy + 28), DEEP)

# a soft light moving across the surface (the chord on its way)
ell(dr, (55, OY + 46, 91, OY + 54), (150, 196, 176))

for i, (x, y, rot) in enumerate(PADS):
    X, Y = x, OY + y
    if i not in SCALE:
        dr.ellipse([sc(X - 2), sc(Y - 2), sc(X + 2), sc(Y + 2)], fill=LINE)
        continue
    chord = i in CHORD
    rx, ry = (15, 10) if i == ROOT else ((13, 9) if chord else (11, 8))
    pad(dr, X, Y, rx, ry, rot, PAD if chord else PAD_T)
    if i == ROOT:
        ring(dr, X, Y, 16, TEXT, 1.2)

for x, y, r in RIPPLES:
    ring(dr, x, OY + y, r, BELL, 1.3)
    ring(dr, x, OY + y, r * 0.62, BELL, 1.0)

sx, sy = SPLASH[0], OY + SPLASH[1]
ring(dr, sx, sy, 7, PULSE, 1.2)
dr.ellipse([sc(sx - 2.5), sc(sy - 2.5), sc(sx + 2.5), sc(sy + 2.5)], fill=PULSE)

# chord name
tw = dr.textlength("Cm7", font=fb)
dr.text((sc(120) - tw / 2, sc(OY + 68)), "Cm7", font=fb, fill=TEXT)

# knob strip
KY = 172
dr.line([(sc(4), sc(KY + 5)), (sc(150), sc(KY + 5))], fill=LINE, width=max(1, S))
dr.text((sc(156), sc(KY - 1)), "POND", font=fxs, fill=ACC)
for k in range(7):
    col = ACC if k == 0 else LINE
    dr.ellipse([sc(198 + k * 6), sc(KY + 3), sc(202 + k * 6), sc(KY + 7)], fill=col)

knobs = [("TEMPO", "76", 0.46), ("EVOLVE", "48", 0.48), ("MOTION", "58", 0.58), ("DRIFT", "18", 0.18)]
for i, (name, val, amt) in enumerate(knobs):
    x = i * 60
    if i:
        dr.line([(sc(x), sc(KY + 16)), (sc(x), sc(KY + 62))], fill=LINE, width=max(1, S))
    tw = dr.textlength(name, font=fxs)
    dr.text((sc(x + 30) - tw / 2, sc(KY + 12)), name, font=fxs, fill=DIM)
    # arc
    box = [sc(x + 18), sc(KY + 25), sc(x + 42), sc(KY + 49)]
    dr.arc(box, start=135, end=405, fill=LINE, width=max(2, S + 1))
    dr.arc(box, start=135, end=135 + 270 * amt, fill=PAD, width=max(2, S + 1))
    tw = dr.textlength(val, font=fb_sm)
    dr.text((sc(x + 30) - tw / 2, sc(KY + 48)), val, font=fb_sm, fill=TEXT)

out = ROOT / "web/app/pond-screen.png"
im.save(out)
print(out)
