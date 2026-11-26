#!/usr/bin/env python3
"""Build the news-image-20261125 v4: one 1024x1024 page.

V4 (26 Nov 07:02 WIB, on Mana's order "buat 1 gambar lagi, layout
harus sama 100%"): Mana's NEW 35 stories of Wednesday 25 November
2026 (7 regions x 5, stories-mana-25nov-v4.md — facts and figures
from that file ONLY, no figures from v1/v3), laid out EXACTLY like
the v1-ref template (build_v1ref.py) and the rank-1 reference
(reference-rank1-clear.jpg): scenes WIDE, full card width, with the
stat banner OVERLAID on the bottom of the scene — heroes 2 stacked
banners (stat1 colour, stat2 navy), cards 1 banner (region colour).
NO side stat panel, NO text beside any scene, NO red stat banner
(SE ASIA uses ORANGE). 13 featured (3 heroes + 10 cards) + 22
briefs = 35 stories. PREVIEW ONLY: no repo, no push, no bundle,
no kit check, no submit. Deterministic: no time, no randomness,
no network. PIL only.
"""
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024
CREAM = (247, 242, 234)
NAVY = (16, 28, 58)
RED = (207, 31, 38)
ORANGE = (222, 110, 24)
INK = (25, 25, 25)
GREY = (96, 96, 96)
GREEN = (46, 139, 87)
GOLD = (176, 132, 24)
OLIVE = (148, 138, 88)

FDIR = "/usr/share/fonts/truetype/liberation/"
SERIF_B = FDIR + "LiberationSerif-Bold.ttf"
SERIF_R = FDIR + "LiberationSerif-Regular.ttf"
SERIF_I = FDIR + "LiberationSerif-Italic.ttf"
SANS_B = FDIR + "LiberationSans-Bold.ttf"
SANS_R = FDIR + "LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, int(size))


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, path, size, max_w, max_lines, min_size=8):
    """Shrink font until text wraps to at most max_lines; return (font, lines)."""
    s = size
    while s > min_size:
        fnt = font(path, s)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        s -= 0.5
    fnt = font(path, min_size)
    return fnt, wrap(draw, text, fnt, max_w)[:max_lines]


def fit_single(draw, text, path, size, max_w, min_size=7):
    """Shrink font until text fits on one line; return font."""
    s = size
    while s > min_size:
        fnt = font(path, s)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        s -= 0.5
    return font(path, min_size)


def fit_head(draw, text, path, size, max_w, min_size=9):
    """Headline: prefer 2 lines (shrinking down to min_size); else 3 lines."""
    fnt, lines = fit_lines(draw, text, path, size, max_w, 2, min_size)
    if len(lines) <= 2:
        return fnt, lines
    return fit_lines(draw, text, path, size, max_w, 3, min_size)


def thumb_cover(fn, w, h):
    """Resize a v1 thumb to cover a (w, h) box, center-cropped."""
    im = fn()
    scale = max(w / im.width, h / im.height)
    nw, nh = round(im.width * scale), round(im.height * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - w) // 2
    y0 = (nh - h) // 2
    return im.crop((x0, y0, x0 + w, y0 + h))


# Region colours v4: 0 SE ASIA orange, 1 E & S ASIA blue,
# 2 OCEANIA navy, 3 MID EAST gold, 4 EUROPE green, 5 AMERICAS teal,
# 6 AFRICA purple. SE ASIA uses ORANGE, never red.
TAB_COLORS = [ORANGE, (36, 84, 160), NAVY, GOLD, (34, 120, 74),
              (20, 130, 138), (110, 62, 150)]
REGION_COLORS = [ORANGE, (36, 84, 160), NAVY, GOLD, (34, 120, 74),
                 (20, 130, 138), (110, 62, 150)]


# ---------------------------------------------------------------- thumbnails
# v4 scenes, drawn with PIL, flat 2D in the v1-ref style.
# Hero thumbs are drawn 648x260 and cover-cropped to 324x100, so
# keep the key drawing in the vertical middle band (y ~30..190);
# the bottom ~40 px of the drawing is covered by the 2 banners.
def thumb_hero_hormuz():
    im = Image.new("RGB", (648, 260), (198, 222, 236))
    d = ImageDraw.Draw(im)
    # sea (top edge at y100 so the hulls stay visible above the banners)
    d.rectangle([0, 100, 648, 260], fill=(18, 64, 112))
    d.rectangle([0, 100, 648, 106], fill=(120, 180, 220))
    for wx in (60, 240, 420, 560):
        d.arc([wx, 112, wx + 90, 136], 180, 360, fill=(220, 235, 245),
              width=4)
    # tanker 1 (left)
    d.polygon([(70, 100), (300, 100), (278, 146), (92, 146)],
              fill=(28, 28, 28))
    d.polygon([(84, 118), (288, 118), (278, 146), (92, 146)],
              fill=(150, 30, 30))
    d.rectangle([240, 62, 292, 100], fill=(235, 235, 235))
    d.rectangle([252, 48, 280, 62], fill=(235, 235, 235))
    # tanker 2 (right)
    d.polygon([(350, 100), (580, 100), (558, 146), (372, 146)],
              fill=(28, 28, 28))
    d.polygon([(364, 118), (568, 118), (558, 146), (372, 146)],
              fill=(150, 30, 30))
    d.rectangle([520, 62, 572, 100], fill=(235, 235, 235))
    d.rectangle([532, 48, 560, 62], fill=(235, 235, 235))
    # flames above both tankers
    for cx in (150, 210, 430, 500):
        d.polygon([(cx - 26, 100), (cx - 8, 52), (cx, 28), (cx + 10, 54),
                   (cx + 26, 100)], fill=(255, 140, 0))
        d.polygon([(cx - 14, 100), (cx - 4, 66), (cx, 52), (cx + 6, 68),
                   (cx + 14, 100)], fill=(255, 210, 0))
    # smoke
    for cx, cy, r in ((150, 22, 20), (180, 12, 24), (430, 22, 20),
                      (470, 10, 24), (500, 26, 16)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 90, 90))
    # sea mine (spiked ball) floating between the tankers
    import math
    cx, cy = 324, 128
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(20, 20, 20))
    for ang in range(0, 360, 45):
        x1 = cx + int(11 * math.cos(math.radians(ang)))
        y1 = cy + int(11 * math.sin(math.radians(ang)))
        x2 = cx + int(19 * math.cos(math.radians(ang)))
        y2 = cy + int(19 * math.sin(math.radians(ang)))
        d.line([(x1, y1), (x2, y2)], fill=(20, 20, 20), width=3)
    return im


def thumb_hero_huawei():
    im = Image.new("RGB", (648, 260), (196, 216, 236))
    d = ImageDraw.Draw(im)
    # courthouse: stone base, columns, pediment
    d.rectangle([0, 220, 648, 260], fill=(210, 205, 195))
    d.rectangle([90, 110, 558, 220], fill=(232, 226, 214))
    d.polygon([(70, 110), (324, 30), (578, 110)], fill=(214, 206, 190))
    d.ellipse([296, 58, 352, 96], fill=(176, 132, 24))
    for cx in (140, 224, 308, 392, 476):
        d.rectangle([cx - 14, 112, cx + 14, 220], fill=(248, 246, 238))
        d.rectangle([cx - 20, 106, cx + 20, 114], fill=(200, 192, 176))
        d.rectangle([cx - 20, 218, cx + 20, 226], fill=(200, 192, 176))
    d.rectangle([292, 160, 356, 220], fill=(90, 70, 50))
    d.rectangle([304, 172, 344, 220], fill=(40, 40, 40))
    # flag pole + US flag
    d.rectangle([596, 40, 600, 220], fill=(120, 120, 120))
    d.rectangle([600, 40, 640, 66], fill=(178, 34, 52))
    for i in range(3):
        d.rectangle([600, 40 + i * 9, 640, 43 + i * 9], fill=(255, 255, 255))
    d.rectangle([600, 40, 618, 54], fill=(36, 54, 120))
    # scales of justice emblem on the pediment wall
    d.line([(324, 118), (324, 140)], fill=(176, 132, 24), width=3)
    d.line([(300, 122), (348, 122)], fill=(176, 132, 24), width=3)
    d.polygon([(292, 140), (308, 140), (300, 126)], fill=(176, 132, 24))
    d.polygon([(340, 140), (356, 140), (348, 126)], fill=(176, 132, 24))
    return im


def thumb_hero_cartagena():
    im = Image.new("RGB", (648, 260), (190, 214, 232))
    d = ImageDraw.Draw(im)
    # supermarket building, shifted up so doors + figures stay
    # visible above the two banners (visible band is thumb y30..150)
    d.rectangle([0, 150, 648, 260], fill=(200, 196, 188))
    d.rectangle([60, 28, 588, 150], fill=(240, 240, 235))
    d.rectangle([60, 28, 588, 62], fill=(20, 130, 138))
    d.text((324, 45), "EXITO", font=font(SANS_B, 22), fill="white",
           anchor="mm")
    # awning stripes
    for i in range(8):
        col = (255, 255, 255) if i % 2 == 0 else (20, 130, 138)
        d.polygon([(80 + i * 62, 62), (80 + (i + 1) * 62, 62),
                   (80 + (i + 1) * 62, 82), (80 + i * 62, 82)],
                  fill=col)
    # glass doors + windows
    d.rectangle([120, 96, 260, 150], fill=(140, 190, 210))
    d.rectangle([388, 96, 528, 150], fill=(140, 190, 210))
    d.rectangle([268, 96, 380, 150], fill=(60, 60, 60))
    d.line([(324, 96), (324, 150)], fill=(200, 200, 200), width=4)
    # soldiers / police in front (simple uniformed figures)
    for cx, col in ((150, (30, 90, 40)), (500, (30, 60, 120))):
        d.ellipse([cx - 14, 104, cx + 14, 128], fill=col)
        d.rectangle([cx - 12, 128, cx + 12, 150], fill=col)
    return im


# Card thumbs are drawn 576x168 and cover-cropped to 192x45, so
# keep the key drawing in the vertical middle band (y ~15..105);
# the bottom ~60 px is covered by the banner + crop.
def thumb_card_solomon():
    im = Image.new("RGB", (576, 168), (170, 210, 232))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 100, 576, 168], fill=(30, 110, 170))
    # island
    d.ellipse([150, 84, 426, 150], fill=(232, 205, 160))
    # palm tree
    d.rectangle([280, 40, 292, 100], fill=(120, 82, 40))
    for dx, dy in ((-46, -16), (-30, -28), (0, -32), (30, -26), (46, -12)):
        d.line([(286, 44), (286 + dx, 44 + dy)], fill=(46, 139, 87),
               width=7)
    # two flag poles + flags (Australia blue, Solomon green/blue)
    d.line([(180, 60), (180, 100)], fill=(120, 120, 120), width=3)
    d.polygon([(180, 60), (232, 68), (180, 78)], fill=(36, 54, 120))
    d.line([(396, 60), (396, 100)], fill=(120, 120, 120), width=3)
    d.polygon([(396, 60), (448, 68), (396, 78)], fill=(46, 139, 87))
    d.polygon([(396, 68), (448, 68), (396, 78)], fill=(36, 84, 160))
    # handshake: two clasped hands over the island
    d.ellipse([252, 84, 324, 116], fill=(232, 180, 140))
    d.rectangle([252, 92, 288, 108], fill=(232, 180, 140))
    d.rectangle([288, 92, 324, 108], fill=(210, 160, 120))
    return im


def thumb_card_kospi():
    im = Image.new("RGB", (576, 168), (13, 22, 46))
    d = ImageDraw.Draw(im)
    for gy in (30, 60, 90):
        d.line([(20, gy), (360, gy)], fill=(255, 255, 255), width=1)
    bars = [(40, 34, 96), (110, 52, 96), (180, 66, 96), (250, 80, 96)]
    for x0, y0, y1 in bars:
        d.rectangle([x0, y0, x0 + 52, y1], fill=(207, 31, 38))
    pts = [(30, 30), (120, 48), (200, 64), (290, 82), (350, 96)]
    d.line(pts, fill=(255, 80, 80), width=5, joint="curve")
    # chip factory block on the right
    d.rectangle([400, 30, 540, 96], fill=(60, 60, 70))
    d.rectangle([420, 46, 520, 80], fill=(36, 84, 160))
    d.rectangle([448, 52, 492, 74], fill=(120, 200, 240))
    for i in range(4):
        d.rectangle([420 + i * 26, 30, 428 + i * 26, 46],
                    fill=(120, 120, 130))
    return im


def thumb_card_canary():
    im = Image.new("RGB", (576, 168), (150, 195, 228))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 96, 576, 168], fill=(30, 100, 160))
    for wx in (40, 200, 360, 500):
        d.arc([wx, 104, wx + 80, 128], 180, 360, fill=(220, 235, 245),
              width=4)
    # island silhouette
    d.polygon([(430, 96), (480, 52), (540, 96)], fill=(120, 140, 120))
    # migrant boat
    d.polygon([(90, 88), (300, 88), (272, 122), (118, 122)],
              fill=(120, 70, 30))
    d.rectangle([150, 60, 162, 88], fill=(90, 60, 20))
    d.polygon([(162, 60), (210, 70), (162, 82)], fill=(240, 240, 240))
    for cx in (130, 160, 190, 220, 250):
        d.ellipse([cx - 8, 66, cx + 8, 82], fill=(232, 180, 140))
        d.rectangle([cx - 9, 80, cx + 9, 90], fill=(36, 84, 160))
    return im


def thumb_card_nato():
    im = Image.new("RGB", (576, 168), (24, 34, 64))
    d = ImageDraw.Draw(im)
    for sx, sy in ((60, 24), (150, 14), (500, 20), (90, 44), (420, 36)):
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    # satellite
    d.rectangle([240, 40, 330, 72], fill=(200, 200, 210))
    d.rectangle([180, 48, 240, 64], fill=(36, 84, 160))
    d.rectangle([330, 48, 390, 64], fill=(36, 84, 160))
    d.ellipse([296, 28, 312, 44], fill=(255, 210, 0))
    d.line([(330, 56), (360, 76)], fill=(200, 200, 210), width=3)
    d.ellipse([356, 72, 372, 88], fill=(220, 220, 230))
    # HQ building below
    d.rectangle([120, 100, 456, 168], fill=(90, 100, 120))
    for i in range(6):
        d.rectangle([140 + i * 54, 112, 176 + i * 54, 140],
                    fill=(255, 214, 120))
    d.rectangle([262, 132, 314, 168], fill=(40, 40, 50))
    return im


def thumb_card_gaza():
    im = Image.new("RGB", (576, 168), (228, 196, 160))
    d = ImageDraw.Draw(im)
    d.ellipse([480, 18, 540, 78], fill=(255, 200, 90))
    # city skyline
    for x0, w, h in ((20, 70, 70), (100, 50, 96), (160, 80, 60),
                     (250, 56, 100), (316, 70, 66), (396, 60, 92),
                     (466, 70, 58)):
        d.rectangle([x0, 110 - h, x0 + w, 168], fill=(90, 80, 70))
        for wy in range(110 - h + 12, 100, 22):
            d.rectangle([x0 + 10, wy, x0 + 22, wy + 10],
                        fill=(255, 214, 120))
    # smoke plume
    for cx, cy, r in ((280, 40, 18), (300, 28, 24), (322, 44, 16)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 120))
    return im


def thumb_card_tariff():
    im = Image.new("RGB", (576, 168), (220, 228, 235))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 110, 576, 168], fill=(180, 185, 190))
    # stacked shipping containers
    cols = [(207, 31, 38), (36, 84, 160), (176, 132, 24), (34, 120, 74),
            (20, 130, 138)]
    for row, y0 in enumerate((76, 42)):
        for i in range(4):
            x0 = 60 + i * 118 + (row * 30)
            d.rectangle([x0, y0, x0 + 108, y0 + 32],
                        fill=cols[(i + row) % len(cols)])
            for k in range(1, 7):
                d.line([(x0 + k * 15, y0), (x0 + k * 15, y0 + 32)],
                       fill=(0, 0, 0), width=1)
    # crane hook above
    d.line([(480, 0), (480, 42)], fill=(60, 60, 60), width=4)
    d.polygon([(468, 42), (492, 42), (480, 60)], fill=(60, 60, 60))
    return im


def thumb_card_lukoil():
    im = Image.new("RGB", (576, 168), (240, 200, 140))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 110, 576, 168], fill=(120, 100, 80))
    # refinery towers
    for x0, w, h in ((60, 60, 80), (150, 44, 100), (230, 70, 66),
                     (330, 50, 92), (410, 66, 74)):
        d.rectangle([x0, 110 - h, x0 + w, 110], fill=(70, 70, 78))
        d.rectangle([x0 + 8, 110 - h - 12, x0 + w - 8, 110 - h],
                    fill=(100, 100, 110))
    # pipes
    d.line([(60, 96), (480, 96)], fill=(50, 50, 56), width=6)
    # flame on the tallest stack
    d.polygon([(160, 0), (150, 22), (172, 22)], fill=(255, 140, 0))
    d.polygon([(164, 10), (158, 24), (172, 24)], fill=(255, 210, 0))
    # oil barrel
    d.rectangle([500, 70, 548, 110], fill=(36, 84, 160))
    d.line([(500, 82), (548, 82)], fill=(20, 50, 100), width=3)
    d.line([(500, 98), (548, 98)], fill=(20, 50, 100), width=3)
    return im


def thumb_card_blackout():
    im = Image.new("RGB", (576, 168), (24, 28, 48))
    d = ImageDraw.Draw(im)
    for sx, sy in ((50, 20), (140, 12), (520, 24), (460, 14)):
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(200, 200, 220))
    # power pylons, one line broken
    for cx in (90, 250, 410):
        d.line([(cx, 110), (cx - 26, 40)], fill=(120, 125, 140), width=5)
        d.line([(cx, 110), (cx + 26, 40)], fill=(120, 125, 140), width=5)
        d.line([(cx - 34, 52), (cx + 34, 52)], fill=(120, 125, 140),
               width=4)
        d.line([(cx, 110), (cx, 44)], fill=(120, 125, 140), width=5)
    d.line([(64, 48), (216, 48)], fill=(180, 180, 190), width=2)
    d.line([(284, 48), (376, 48)], fill=(180, 180, 190), width=2)
    # lightning bolt in the gap
    d.polygon([(300, 20), (280, 62), (296, 62), (282, 104), (318, 52),
               (300, 52)], fill=(255, 210, 0))
    # dark houses below
    for x0 in (30, 150, 330, 460):
        d.rectangle([x0, 110, x0 + 70, 150], fill=(10, 12, 22))
        d.polygon([(x0 - 6, 110), (x0 + 35, 88), (x0 + 76, 110)],
                  fill=(16, 18, 32))
    return im


def thumb_card_inflation():
    im = Image.new("RGB", (576, 168), (247, 242, 234))
    d = ImageDraw.Draw(im)
    # rising bars
    for i, h in enumerate((30, 44, 58, 74)):
        x0 = 60 + i * 62
        d.rectangle([x0, 104 - h, x0 + 44, 104], fill=(36, 84, 160))
    # rising arrow
    pts = [(60, 92), (130, 72), (190, 54), (260, 30)]
    d.line(pts, fill=(207, 31, 38), width=6, joint="curve")
    d.polygon([(260, 30), (232, 30), (260, 58)], fill=(207, 31, 38))
    # coins stack
    for i in range(4):
        d.ellipse([400, 88 - i * 14, 480, 104 - i * 14],
                  fill=(212, 175, 55), outline=(150, 110, 20), width=2)
    d.ellipse([500, 74, 552, 104], fill=(212, 175, 55),
              outline=(150, 110, 20), width=2)
    d.text((526, 89), "$", font=font(SANS_B, 18), fill=(120, 85, 10),
           anchor="mm")
    return im


def thumb_card_afcon():
    im = Image.new("RGB", (576, 168), (34, 120, 74))
    d = ImageDraw.Draw(im)
    d.ellipse([180, 100, 396, 168], fill=(46, 139, 87))
    d.line([(0, 110), (576, 110)], fill=(255, 255, 255), width=3)
    # gold trophy
    d.polygon([(248, 30), (328, 30), (318, 78), (258, 78)],
              fill=(212, 175, 55))
    d.arc([222, 30, 262, 66], 90, 270, fill=(212, 175, 55), width=8)
    d.arc([314, 30, 354, 66], 270, 90, fill=(212, 175, 55), width=8)
    d.rectangle([280, 78, 296, 92], fill=(176, 132, 24))
    d.rectangle([262, 92, 314, 102], fill=(176, 132, 24))
    d.ellipse([284, 18, 292, 26], fill=(255, 220, 100))
    # football
    d.ellipse([420, 60, 470, 110], fill=(255, 255, 255),
              outline=(40, 40, 40), width=2)
    d.polygon([(445, 72), (455, 72), (458, 82), (450, 88), (440, 82)],
              fill=(40, 40, 40))
    d.polygon([(128, 70), (148, 70), (152, 84), (138, 92), (126, 82)],
              fill=(255, 255, 255))
    return im


AFRICA_POLY = [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
               (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20),
               (32, -28), (25, -34), (18, -35), (15, -27), (12, -18),
               (9, -1), (9, 4), (-8, 4), (-13, 8)]


# ---------------------------------------------------------------- map
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80), (-85, 70),
     (-75, 62), (-65, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 25),
     (-85, 20), (-90, 15), (-95, 18), (-105, 20), (-110, 23), (-120, 32),
     (-125, 40), (-130, 55), (-150, 60)],
    [(-80, 10), (-75, 5), (-60, 0), (-50, 0), (-40, -5), (-35, -10),
     (-40, -20), (-48, -28), (-55, -35), (-65, -40), (-70, -50),
     (-73, -40), (-72, -20), (-78, -5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 70), (40, 68),
     (45, 60), (40, 50), (35, 45), (30, 42), (28, 40), (23, 36),
     (19, 40), (15, 38), (12, 44), (8, 44), (3, 43), (-2, 37)],
    AFRICA_POLY,
    [(30, 70), (40, 68), (55, 70), (70, 72), (90, 75), (110, 74),
     (130, 72), (150, 70), (170, 66), (178, 65), (162, 60), (158, 52),
     (142, 50), (140, 40), (135, 35), (127, 33), (122, 38), (120, 30),
     (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20),
     (80, 8), (77, 8), (72, 20), (66, 25), (60, 25), (55, 28),
     (50, 30), (48, 30), (43, 35), (36, 36), (30, 42)],
    [(95, 5), (105, 0), (110, -5), (115, -8), (120, -10), (130, -5),
     (135, 0), (140, -5), (140, 2), (130, 5), (120, 8), (105, 10)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32),
     (137, -35), (140, -38), (145, -38), (150, -37), (153, -27),
     (150, -22), (146, -19), (142, -11), (136, -12), (132, -11),
     (126, -14), (122, -17), (118, -20)],
    [(167, -45), (170, -42), (174, -39), (178, -38), (175, -41),
     (172, -43), (168, -47)],
]

# ---------------------------------------------------------------- content
# v4 content — facts and figures ONLY from stories-mana-25nov-v4.md.
# Region index: 0 SE ASIA, 1 E & S ASIA, 2 OCEANIA, 3 MID EAST,
# 4 EUROPE, 5 AMERICAS, 6 AFRICA.
TICKER = ("HORMUZ: 2 tankers hit mines and burn \u00b7 BROOKLYN: "
          "Huawei guilty of fraud \u00b7 CARTAGENA: ~30\u201350 hostages freed")

TIMELINE_ITEMS = ["-6.16% KOSPI plunge", "4.9% Australia inflation",
                  "~2,000 Canary migrants", "30\u201350 hostages freed",
                  "5 tons lead azide", "5 provinces blacked out",
                  "14 tariff partners"]

TABS = ["SE ASIA 5", "E & S ASIA 5", "OCEANIA 5", "MID EAST 5",
        "EUROPE 5", "AMERICAS 5", "AFRICA 5"]

HEROES = [
    dict(num=1, bar="STRAIT OF HORMUZ \u00b7 WAR", region=3, pill="REPORTED",
         stat1="2 TANKERS \u00b7 HIT MINES", stat2="STRAIT OF HORMUZ",
         source="Reuters \u00b7 AP \u00b7 AFP",
         head="Two tankers burn in Strait of Hormuz after mine strikes",
         deck=("Iran reports two oil tankers hit sea mines and are burning "
               "in the strategic strait; a Saudi-led coalition intercepts "
               "four drones in Eastern Province."),
         thumb=thumb_hero_hormuz),
    dict(num=2, bar="BROOKLYN, NEW YORK \u00b7 TECH", region=1,
         pill="OFFICIAL", stat1="FRAUD: GUILTY",
         stat2="RACKETEERING: ACQUITTED", stat1_color=(110, 62, 150),
         source="Reuters \u00b7 AP \u00b7 AFP",
         head="Huawei found guilty of fraud in Brooklyn court",
         deck=("A federal court convicts Chinese tech giant Huawei of "
               "criminal fraud but acquits it of racketeering conspiracy."),
         thumb=thumb_hero_huawei),
    dict(num=3, bar="CARTAGENA \u00b7 SECURITY", region=5, pill="OFFICIAL",
         stat1="~30 FREED", stat2="CARTAGENA",
         source="Reuters \u00b7 AP \u00b7 AFP",
         head="Colombia forces free ~30\u201350 hostages in Cartagena",
         deck=("Police and troops storm an \u00c9xito supermarket in "
               "Cartagena and rescue all the hostages held almost a full "
               "day after a failed robbery."),
         thumb=thumb_hero_cartagena),
]

CARDS = [
    dict(num=4, bar="SOLOMON IS. \u00b7 SECURITY PACT", region=2,
         pill="OFFICIAL", stat="SECURITY PACT",
         source="Reuters \u00b7 AP \u00b7 AFP",
         head="Solomon Islands sign security pact with Australia",
         deck=("Albanese and Wale sign a pact making Australia the main "
               "security partner and barring foreign military bases."),
         thumb=thumb_card_solomon),
    dict(num=5, bar="SEOUL \u00b7 KOSPI -6.16%", region=1, pill="OFFICIAL",
         stat="-6.16%", source="Reuters \u00b7 AP \u00b7 AFP",
         head="Taiwan output +29.8% as KOSPI plunges 6.16%",
         deck=("Taiwan industrial output surges 29.8% while South Korea's "
               "KOSPI index falls sharply by 6.16%."),
         thumb=thumb_card_kospi),
    dict(num=6, bar="CANARY IS. \u00b7 MIGRANTS", region=4, pill="REPORTED",
         stat="~2,000", source="Reuters \u00b7 AP \u00b7 AFP",
         head="Nearly 2,000 migrants reach Canary Islands in a day",
         deck=("Spain records almost 2,000 arrivals in one day \u2014 a "
               "daily record \u2014 ahead of national elections."),
         thumb=thumb_card_canary),
    dict(num=7, bar="BRUSSELS \u00b7 NATO WARNS", region=4, pill="REPORTED",
         stat="RUTTE WARNS", source="Reuters \u00b7 AP \u00b7 AFP",
         head="NATO chief Rutte warns over Russian nuclear satellite",
         deck=("Mark Rutte discusses reports of Russia planning a "
               "nuclear-armed satellite ahead of meeting President Trump."),
         thumb=thumb_card_nato),
    dict(num=8, bar="GAZA \u00b7 HAMAS OFFICIAL KILLED", region=3,
         pill="REPORTED", stat="HAMAS OFFICIAL",
         source="Reuters \u00b7 AP \u00b7 AFP",
         head="Israeli strike kills Hamas security chief in Gaza",
         deck=("An Israeli airstrike in western Gaza City kills Hamas "
               "internal security director Naeem Abu Nahel."),
         thumb=thumb_card_gaza),
    dict(num=9, bar="JAKARTA \u00b7 US TARIFFS", region=0, pill="OFFICIAL",
         stat="14 PARTNERS", source="Reuters \u00b7 AP \u00b7 AFP",
         head="US tariffs target ASEAN and 14 partners",
         deck=("New US tariffs target 14 major partners over excess "
               "capacity, including Indonesia and five ASEAN neighbours."),
         thumb=thumb_card_tariff),
    dict(num=10, bar="SOFIA \u00b7 LUKOIL DEAL", region=4, pill="OFFICIAL",
         stat="LUKOIL ASSETS", source="Reuters \u00b7 AP \u00b7 AFP",
         head="US-led consortium to buy Lukoil's non-Russian assets",
         deck=("A US-led consortium agrees to take over Lukoil's "
               "non-Russian oil and gas assets in Bulgaria, Romania and "
               "Europe."),
         thumb=thumb_card_lukoil),
    dict(num=11, bar="BOGOTA \u00b7 BLACKOUT", region=5, pill="REPORTED",
         stat="5 PROVINCES", source="Reuters \u00b7 AP \u00b7 AFP",
         head="Sabotage blacks out five provinces in Colombia",
         deck=("President Abelardo de la Espriella blames armed groups "
               "for energy sabotage causing blackouts in five provinces."),
         thumb=thumb_card_blackout),
    dict(num=12, bar="CANBERRA \u00b7 INFLATION", region=2, pill="OFFICIAL",
         stat="4.9%", source="Reuters \u00b7 AP \u00b7 AFP",
         head="Australia inflation hits 4.9%",
         deck=("Australia's inflation rate rises to 4.9% amid uncertainty "
               "in global supply chains."),
         thumb=thumb_card_inflation),
    dict(num=13, bar="DAKAR \u00b7 AFCON 2025", region=6, pill="OFFICIAL",
         stat="SENEGAL WINS", stat_color=NAVY,
         source="Reuters \u00b7 AP \u00b7 AFP",
         head="CAS hands AFCON 2025 title back to Senegal",
         deck=("CAS overturns CAF's appeal ruling giving AFCON 2025 to "
               "Morocco and restores Senegal as champions."),
         thumb=thumb_card_afcon),
]

# (card num, lon, lat, dx, dy, region index) — v4 pins, numbered
# 1-13 like the featured cards. dx/dy separate near neighbours:
# Cartagena/Bogota (~5 px apart) and Canary/Dakar (~12 px apart).
# Pin fill = the card's region colour, white number.
PINS = [(1, 56.5, 26.5, 0, 0, 3), (2, -74.0, 40.7, 0, -10, 1),
        (3, -75.5, 10.4, -12, -8, 5), (4, 159.9, -9.6, 0, 0, 2),
        (5, 127.0, 37.5, 0, -10, 1), (6, -15.6, 28.3, 0, -10, 4),
        (7, 4.35, 50.85, 0, -10, 4), (8, 34.45, 31.5, 0, 10, 3),
        (9, 106.8, -6.2, 0, 0, 0), (10, 23.3, 42.7, 0, -10, 4),
        (11, -74.1, 4.7, 12, 8, 5), (12, 149.1, -35.3, 0, 0, 2),
        (13, -17.4, 14.7, 0, 10, 6)]

# (story num, "Lead: rest", region index, wire source, claim?).
# 22 briefs = stories 2,3,4,5,6,8,10,12,14,15,17,18,20,21,24,26,
# 27,28,31,32,33,34 — facts/figures from the NEW summary only.
# CLAIM tag ONLY on story 18 (one side's accusation).
BRIEFS = [
    (14, "Indonesia: Teachers' Day marked; disaster summit IDMS 2026 opens", 0, "Reuters", False),
    (15, "Indonesia: BMKG and Finland launch PACIDFIN weather project", 0, "AP", False),
    (16, "Singapore: expands supply pact and carbon deal with Australia", 0, "AFP", False),
    (17, "Indonesia: police allege senior officer role in surveillance case", 0, "Reuters", False),
    (18, "US: proposes new tariffs on China, Japan and India", 1, "AP", False),
    (19, "Japan: support for Takaichi's China policy falls to 44%; Nikkei -2.78%", 1, "AFP", False),
    (20, "India: concern grows over Indians recruited to fight for Russia", 1, "Reuters", False),
    (21, "Australia: bushfire emergency warning \u2014 \u2018too late to leave\u2019", 2, "AP", False),
    (22, "Pacific: island states join Indonesia\u2013Finland early-warning scheme", 2, "AFP", False),
    (23, "New Zealand: shallow M3.9 quake 228 km north of Hicks Bay", 2, "Reuters", False),
    (24, "Israel: Eisenkot's Yashar signs coalition pact to oust Netanyahu", 3, "AP", False),
    (25, "Israel: Katz accuses Iran of chemical weapons programme", 3, "AFP", True),
    (26, "Yemen: Saudi-led coalition orders Hodeidah port evacuation", 3, "Reuters", False),
    (27, "Brussels: EU\u2013Western Balkans summit on membership and security", 4, "AP", False),
    (28, "Poland: signs defence research deal with the Pentagon", 4, "AFP", False),
    (29, "Iowa: US Army detonates nearly 5 tons of degraded lead azide", 5, "Reuters", False),
    (30, "Chicago: FAA imposes ground stop at O'Hare over navigation fault", 5, "AP", False),
    (31, "New York: mayor delays Macy's Thanksgiving Day Parade", 5, "AFP", False),
    (32, "Libya: condemns Ukraine drone strike that killed 2 naval officers", 6, "Reuters", False),
    (33, "DRC: Ebola staff evacuated after 3 days trapped; at least 10 killed", 6, "AP", False),
    (34, "West Africa: armed groups widen use of cheap explosive drones", 6, "AFP", False),
    (35, "Nigeria: AI disinformation rises ahead of elections", 6, "Reuters", False),
]

LEGEND = [("SE ASIA", 0, 5), ("E & S ASIA", 1, 5), ("OCEANIA", 2, 5),
          ("MID EAST", 3, 5), ("EUROPE", 4, 5), ("AMERICAS", 5, 5),
          ("AFRICA", 6, 5)]

MAP_CAPTION = ("Pins locate the 13 illustrated lead & feature stories; "
               "all 35 items color-coded across 7 regions below.")

HOW_SURE = ("HOW SURE: CONFIRMED = 2+ outlets \u00b7 OFFICIAL = on record "
            "\u00b7 REPORTED = single wire/local \u00b7 CLAIM = one side's "
            "account \u00b7 Drawn scenes")

DATE_CHECK = ("Every main story on this page happened, or was first "
              "reported, on Wednesday 25 November 2026 (UTC).")


# ---------------------------------------------------------------- layout helpers
def _pill_colors(status):
    """(fill, text, outline) for a status pill, hero and card alike."""
    if status == "OFFICIAL":
        return ((144, 238, 144), NAVY, NAVY)
    if status == "REPORTED":
        return (RED, "white", None)
    return (NAVY, "white", None)


def _draw_pill(d, x, y, status, height=11, font_size=8):
    """Draw a status pill at (x, y); returns its width."""
    pf = font(SANS_B, font_size)
    pw = d.textlength(status, font=pf) + 12
    fill, tfill, outline = _pill_colors(status)
    d.rounded_rectangle([x, y, x + pw, y + height], radius=height // 2,
                        fill=fill, outline=outline, width=1)
    d.text((x + 6, y + 1), status, font=pf, fill=tfill)
    return pw


def _top_bar(d, x, y, w, h, color, num, text, pill, text_size=11,
             light=False):
    """Top bar: circle + number, bar text, status pill at the right.

    light=True (heroes): white bar with a thin light-grey outline, navy
    text, navy circle with a white number. Otherwise the bar keeps its
    region colour, white text and a white circle with a navy number.
    pill=None draws no pill and lets the text use the full bar width.
    """
    if light:
        d.rectangle([x, y, x + w, y + h], fill="white",
                    outline=(205, 205, 205), width=1)
    else:
        d.rectangle([x, y, x + w, y + h], fill=color)
    r = (h - 4) // 2
    d.ellipse([x + 4, y + 2, x + 4 + 2 * r, y + 2 + 2 * r],
              fill=NAVY if light else "white")
    nf = font(SANS_B, 8 if h >= 16 else 7)
    ns = str(num)
    d.text((x + 4 + r - d.textlength(ns, font=nf) / 2,
            y + 2 + r - 5), ns, font=nf,
           fill="white" if light else NAVY)
    text_right = x + w - 4
    if pill is not None:
        pf = font(SANS_B, 8)
        pw = d.textlength(pill, font=pf) + 12
        px = x + w - pw - 4
        _draw_pill(d, px, y + 2, pill, height=h - 4, font_size=8)
        text_right = px - 6
    tf = fit_single(d, text, SANS_B, text_size,
                    text_right - (x + 4 + 2 * r + 4), min_size=6.5)
    d.text((x + 4 + 2 * r + 4, y + 2), text, font=tf,
           fill=NAVY if light else "white")


def _deck(d, x, text, width, head_lines, y_top, y_bottom, size=11,
          lh=12):
    """Deck text between y_top and y_bottom; returns end y.

    3 lines when the headline took 2, else 2 — clipped by the space left
    before the source line.
    """
    max_dl = 3 if head_lines <= 2 else 2
    room = max(1, int((y_bottom - y_top) // lh))
    max_dl = min(max_dl, room)
    df, dlines = fit_lines(d, text, SANS_R, size, width, max_dl, min_size=8)
    y = y_top
    for ln in dlines:
        d.text((x, y), ln, font=df, fill=INK)
        y += lh
    return y, len(dlines), len(wrap(d, text, df, width))

# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    problems = []

    # ---- masthead on cream paper (v3 format, v1 counts)
    f = font(SERIF_B, 14)
    d.text((14, 6), "THE WORLD IN ONE DAY", font=f, fill=RED)
    f2 = font(SANS_B, 9)
    right = ("35 DATED STORIES \u00b7 7 REGIONS \u00b7 "
             "ALL FROM WED 25 NOV 2026")
    d.text((W - 14 - d.textlength(right, font=f2), 8), right, font=f2,
           fill=NAVY)

    # ---- date masthead, 58 pt
    t = "Wednesday 25 November 2026"
    f = fit_single(d, t, SERIF_B, 58, W - 28)
    d.text(((W - d.textlength(t, font=f)) / 2, 20), t, font=f, fill=NAVY)

    # ---- ticker: v1 text, red italic, one line
    tf = fit_single(d, TICKER, SERIF_I, 15, W - 28)
    d.text(((W - d.textlength(TICKER, font=tf)) / 2, 81), TICKER,
           font=tf, fill=RED)

    # ---- region tabs (v1 labels + colours)
    tw = 996 / 7
    for i, tab in enumerate(TABS):
        x0 = 14 + tw * i
        d.rectangle([x0, 98, x0 + tw - 2, 114], fill=TAB_COLORS[i])
        f = font(SANS_B, 10)
        d.text((x0 + (tw - 2) / 2 - d.textlength(tab, font=f) / 2, 101),
               tab, font=f, fill="white")

    # ---- thick navy line, 2 px, x14-1010
    d.rectangle([14, 116, 1010, 117], fill=(20, 26, 32))

    # ---- timeline: red WEDNESDAY box + 7 v1 key numbers, spread even
    d.rectangle([14, 120, 124, 136], fill=RED)
    wf = font(SANS_B, 10)
    wt = "WEDNESDAY"
    d.text((14 + (110 - d.textlength(wt, font=wf)) / 2, 122), wt,
           font=wf, fill="white")
    tx0, tx1 = 130, 1010
    ts = 11.5
    while ts >= 10.5:
        tf = font(SANS_B, ts)
        widths = [d.textlength(it, font=tf) for it in TIMELINE_ITEMS]
        gap = ((tx1 - 8) - (tx0 + 8) - sum(widths)) / (len(TIMELINE_ITEMS) - 1)
        if gap >= 20:
            break
        ts -= 0.5
    tf = font(SANS_B, ts)
    widths = [d.textlength(it, font=tf) for it in TIMELINE_ITEMS]
    gap = ((tx1 - 8) - (tx0 + 8) - sum(widths)) / (len(TIMELINE_ITEMS) - 1)
    if gap < 20:
        problems.append(f"timeline gap {gap:.1f}px at {ts}pt (items tight)")
    cx = tx0 + 8
    for i, it in enumerate(TIMELINE_ITEMS):
        d.text((cx, 122), it, font=tf, fill=INK)
        cx += widths[i]
        if i < len(TIMELINE_ITEMS) - 1:
            d.line([cx + gap / 2, 122, cx + gap / 2, 134],
                   fill=(150, 150, 150), width=1)
            cx += gap

    # ---- heroes: white bar + pill, 100 px visual slot (y156..256),
    # WIDE scene (324 px, full card width) with TWO stacked stat
    # banners OVERLAID on the bottom of the scene, as in the
    # reference: stat1 y216..236 in the hero's region colour, stat2
    # y236..256 navy, white bold text centred. NO side panel, NO text
    # beside the scene. Headline, deck, source below, unchanged.
    hx = [14, 350, 686]
    HW = 324
    for col, h in enumerate(HEROES):
        x = hx[col]
        _top_bar(d, x, 140, HW, 16, RED, h["num"], h["bar"], h["pill"],
                 text_size=11, light=True)
        img.paste(thumb_cover(h["thumb"], HW, 100), (x, 156))
        d.rectangle([x, 216, x + HW, 236],
                    fill=h.get("stat1_color", REGION_COLORS[h["region"]]))
        f1 = fit_single(d, h["stat1"], SANS_B, 12, HW - 12, min_size=8)
        d.text((x + HW / 2, 226), h["stat1"], font=f1,
               fill="white", anchor="mm")
        d.rectangle([x, 236, x + HW, 256], fill=NAVY)
        f2 = fit_single(d, h["stat2"], SANS_B, 10, HW - 12, min_size=8)
        d.text((x + HW / 2, 246), h["stat2"], font=f2,
               fill="white", anchor="mm")
        hf, lines = fit_head(d, h["head"], SERIF_B, 19, HW - 12)
        y = 260
        for ln in lines:
            d.text((x + 6, y), ln, font=hf, fill=INK)
            y += int(hf.size * 1.08)
        end, n_drawn, n_full = _deck(d, x + 6, h["deck"], HW - 12,
                                     len(lines), y + 2, 344)
        if n_drawn < n_full:
            problems.append(
                f"hero {h['num']} deck truncated: {n_drawn}/{n_full} lines")
        assert end <= 344, (h["bar"], end)
        sf = font(SANS_R, 9)
        d.text((x + 6, 346), h["source"], font=sf, fill=GREY)
        d.rectangle([x - 1, 139, x + HW + 1, 360],
                    outline=(130, 130, 130), width=1)

    # ---- small cards, two rows of five (145 px tall): region-coloured
    # bar, WIDE scene (192 px, full card width, 45 px tall) with ONE
    # region-coloured stat banner OVERLAID on the bottom of the scene
    # (y0+45..y0+60, ~15 px, white bold text centred), as in the
    # reference. Region 0 uses ORANGE, never red. NO side panel, NO
    # text beside the scene. Headline, deck, wire source at the bottom
    # right, status pill at the bottom left — unchanged.
    rows_y = [366, 516]
    CARD_H = 145
    CW2 = 192
    for ri, y0 in enumerate(rows_y):
        for ci in range(5):
            c = CARDS[ri * 5 + ci]
            x = 14 + ci * 201
            _top_bar(d, x, y0, CW2, 15, TAB_COLORS[c["region"]], c["num"],
                     c["bar"], None, text_size=8.5)
            img.paste(thumb_cover(c["thumb"], CW2, 45), (x, y0 + 15))
            pcol = c.get("stat_color", REGION_COLORS[c["region"]])
            d.rectangle([x, y0 + 45, x + CW2, y0 + 60], fill=pcol)
            f1 = fit_single(d, c["stat"], SANS_B, 11, CW2 - 12,
                            min_size=7)
            d.text((x + CW2 / 2, y0 + 15 + 37), c["stat"],
                   font=f1, fill="white", anchor="mm")
            hf, lines = fit_head(d, c["head"], SERIF_B, 13, CW2 - 12)
            y = y0 + 64
            for ln in lines:
                d.text((x + 6, y), ln, font=hf, fill=INK)
                y += 15
            src_y = y0 + CARD_H - 16
            end, n_drawn, n_full = _deck(d, x + 6, c["deck"], CW2 - 12,
                                         len(lines), y, src_y - 2,
                                         size=9.5, lh=11)
            if n_drawn < n_full:
                problems.append(
                    f"card {c['num']} deck truncated: "
                    f"{n_drawn}/{n_full} lines")
            assert end <= src_y, (c["bar"], end - y0)
            sf = font(SANS_R, 8.5)
            src = c["source"]
            d.text((x + CW2 - 6 - d.textlength(src, font=sf), src_y),
                   src, font=sf, fill=GREY)
            _draw_pill(d, x + 6, src_y, c["pill"], height=11,
                       font_size=8)
            d.rectangle([x - 1, y0 - 1, x + CW2 + 1, y0 + CARD_H],
                        outline=(130, 130, 130), width=1)

    # ---- bottom: solid-land map + briefs
    d.text((14, 671), "WHERE IT HAPPENED \u00b7 13 PINS",
           font=font(SANS_B, 11), fill=INK)
    bh = ("ALSO ON WEDNESDAY 25 NOVEMBER \u00b7 22 MORE DATED BRIEFS "
          "(7 REGIONS MATCHED BY COLOR)")
    bf = fit_single(d, bh, SANS_B, 11, 670)
    d.text((340, 671), bh, font=bf, fill=INK)
    d.line([14, 687, W - 14, 687], fill=INK, width=1)

    # solid-land map, x 14..330, y 691..821, on a pale blue-grey box
    mx0, my0, mx1, my1 = 14, 691, 330, 821
    mw, mh = mx1 - mx0, my1 - my0
    d.rectangle([mx0, my0, mx1, my1], fill=(208, 221, 232),
                outline=(120, 130, 140), width=1)
    for poly in CONTINENTS:
        pts = [(mx0 + (lon + 180) / 360 * mw,
                my0 + (84 - lat) / 142 * mh) for lon, lat in poly]
        d.polygon(pts, fill=(213, 197, 163))
    nf = font(SANS_B, 8)
    for num, lon, lat, dx, dy, reg in PINS:
        px = mx0 + (lon + 180) / 360 * mw + dx
        py = my0 + (84 - lat) / 142 * mh + dy
        print(f"PIN {num}: lon={lon} lat={lat} -> x={px:.1f} y={py:.1f} "
              f"region={reg}")
        px = min(max(px, mx0 + 9), mx1 - 9)
        py = min(max(py, my0 + 9), my1 - 9)
        d.ellipse([px - 8, py - 8, px + 8, py + 8],
                  fill=REGION_COLORS[reg], outline="white", width=1)
        s = str(num)
        d.text((px - d.textlength(s, font=nf) / 2, py - 6), s,
               font=nf, fill="white")

    # map caption + 7-region legend, flowed under the map
    cf, clines = fit_lines(d, MAP_CAPTION, SANS_R, 8.5, 316, 2, min_size=8)
    cy = 825
    for ln in clines:
        d.text((14, cy), ln, font=cf, fill=INK)
        cy += 11
    ly = cy + 4
    lx = 14
    lf = font(SANS_B, 8)
    for name, ci, cnt in LEGEND:
        label = f"{name} {cnt}"
        iw = 10 + d.textlength(label, font=lf) + 10
        if lx + iw > 330:
            lx = 14
            ly += 13
        d.ellipse([lx, ly + 2, lx + 7, ly + 9], fill=TAB_COLORS[ci])
        d.text((lx + 10, ly), label, font=lf, fill=INK)
        lx += iw
    if ly + 11 > 916:
        problems.append(f"legend overflows: ly={ly}")

    # briefs: two columns (11 + 11), one line each — coloured chip with
    # the display number, bold lead (place before the colon), regular
    # rest, wire source right-aligned; a red CLAIM tag only where the
    # brief is one side's account (story 18)
    for k, (num, txt, reg, src, claim) in enumerate(BRIEFS):
        col = k // 11
        row = k % 11
        x = 340 + col * 340
        y = 691 + row * 17
        col_right = x + 330
        bf = font(SANS_B, 9)
        ns = str(num)
        d.rectangle([x, y - 1, x + 17, y + 14], fill=TAB_COLORS[reg])
        d.text((x + (18 - d.textlength(ns, font=bf)) / 2, y), ns,
               font=bf, fill="white")
        tx = x + 22
        lead, rest = txt.split(": ", 1)
        lead_disp = lead + ":"
        sz = 9.0
        while sz > 7:
            blf = font(SANS_B, sz)
            rlf = font(SANS_R, sz)
            sf = font(SANS_R, 8)
            cf = font(SANS_B, 7)
            claim_w = d.textlength("CLAIM", font=cf) + 8 if claim else 0
            need = (d.textlength(lead_disp, font=blf) + 3
                    + d.textlength(rest, font=rlf) + 6 + claim_w
                    + d.textlength(src, font=sf))
            if tx + need <= col_right:
                break
            sz -= 0.5
        blf = font(SANS_B, sz)
        rlf = font(SANS_R, sz)
        sf = font(SANS_R, 8)
        cf = font(SANS_B, 7)
        d.text((tx, y), lead_disp, font=blf, fill=INK)
        rx = tx + d.textlength(lead_disp, font=blf) + 3
        d.text((rx, y), rest, font=rlf, fill=INK)
        ex = rx + d.textlength(rest, font=rlf)
        src_w = d.textlength(src, font=sf)
        if claim:
            cw = d.textlength("CLAIM", font=cf) + 8
            cx0 = col_right - src_w - 4 - cw
            d.rectangle([cx0, y, cx0 + cw, y + 11], fill=RED)
            d.text((cx0 + 4, y + 1), "CLAIM", font=cf, fill="white")
            ex = cx0
        if ex + 6 + src_w > col_right:
            problems.append(f"brief {num} text collides with source")
        d.text((col_right - src_w, y), src,
               font=sf, fill=GREY)

    # ---- date check box (v1 text, not v3 "EXCLUDED")
    d.rectangle([14, 892, W - 14, 930], outline=RED, width=2)
    lf = fit_single(d, "DATE CHECK", SANS_B, 11, 168, min_size=8)
    d.text((24, 905), "DATE CHECK", font=lf, fill=RED)
    tf = font(SANS_R, 10.5)
    lines = wrap(d, DATE_CHECK, tf, W - 14 - 214)
    # Center the sentence vertically on the box middle (y911, same as the
    # "DATE CHECK" label) and horizontally in the space right of the label.
    label_end = 24 + d.textlength("DATE CHECK", font=lf)
    sent_w = d.textlength(lines[0], font=tf)
    sent_x = (label_end + 8 + (W - 14) - sent_w) / 2
    tb = d.textbbox((0, 0), lines[0], font=tf)
    sent_y = 911 - (tb[1] + tb[3]) / 2
    d.text((sent_x, sent_y), lines[0], font=tf, fill=INK)
    if len(lines) != 1 or sent_y + tb[3] > 930:
        problems.append("date check text overflows box")

    # ---- how sure line + sources
    hs_b = font(SANS_B, 9)
    hs_r = font(SANS_R, 9)
    hs_head = "HOW SURE: "
    d.text((14, 936), hs_head, font=hs_b, fill=GREY)
    d.text((14 + d.textlength(hs_head, font=hs_b), 936), HOW_SURE[10:],
           font=hs_r, fill=GREY)
    rt = "Sources: Reuters, AP, AFP."
    f = font(SANS_R, 9)
    d.text((W - 14 - d.textlength(rt, font=f), 936), rt, font=f, fill=GREY)

    # ---- footer bar
    d.rectangle([0, 962, W, H], fill=NAVY)
    d.text((14, 987), "THE WORLD IN ONE DAY", font=font(SANS_B, 11),
           fill="white")
    rt = "WEDNESDAY 25 NOVEMBER 2026 \u00b7 ONE PAGE"
    f = font(SANS_B, 9)
    d.text((W - 14 - d.textlength(rt, font=f), 989), rt, font=f,
           fill="white")

    return img, problems


if __name__ == "__main__":
    img, problems = build()
    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True, compress_level=9)
    data = open(out, "rb").read()
    print(out, img.size, len(data), "bytes",
          hashlib.sha256(data).hexdigest())
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print(" -", p)
    else:
        print("no problems detected by build checks")
