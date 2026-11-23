#!/usr/bin/env python3
"""Draw the news-image-20261123 entry: Monday 23 November 2026, 31 stories.
Numbers-led angle: giant number grid on top, 3 hero scenes, 10 small cards,
world map + pins, ALSO list, DATE CHECK box. Stdlib + PIL only.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FB if bold else FR, size)


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, f, fill, lh=None, max_lines=None):
    lh = lh or int(f.size * 1.25)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


# ---------------- palette ----------------
PAPER = (250, 247, 240)
INK = (18, 18, 18)
RED = (178, 24, 24)
DARKRED = (120, 12, 12)
NAVY = (16, 42, 90)
TEAL = (0, 110, 110)
GOLD = (176, 124, 0)
GREEN = (28, 110, 44)
PURPLE = (96, 48, 140)
GREY = (110, 110, 110)
LIGHT = (238, 234, 226)
CARD_BG = (255, 255, 255)
CHIP = {
    "REPORTED": (28, 110, 44),
    "CLAIM": (176, 124, 0),
    "ONGOING": (16, 90, 160),
    "OFFICIAL": (70, 70, 70),
}
REGIONS = [
    ("NORTH AMERICA", 8, (16, 90, 160)),
    ("EUROPE", 6, (16, 42, 90)),
    ("MIDDLE EAST", 6, (120, 60, 10)),
    ("ASIA-PACIFIC", 6, (0, 110, 110)),
    ("AFRICA", 3, (28, 110, 44)),
    ("WORLD", 2, (96, 48, 140)),
]

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ================= MASTHEAD =================
d.rectangle([0, 0, W, 64], fill=NAVY)
d.text((16, 8), "THE WORLD TODAY", font=font(34, True), fill=(255, 255, 255))
d.text((16, 44), "MONDAY 23 NOVEMBER 2026", font=font(13, True), fill=(255, 205, 60))
d.text((W - 16, 12), "31 STORIES", font=font(15, True), fill=(255, 255, 255), anchor="ra")
d.text((W - 16, 34), "6 REGIONS", font=font(13, True), fill=(200, 210, 235), anchor="ra")

# ================= KICKER =================
d.rectangle([0, 64, W, 88], fill=(255, 205, 60))
d.text((16, 70), "AI ROUT HITS ASIA  ·  GUTERRES: REGULATE AI  ·  US LEAD OVER CHINA AT RECORD LOW",
       font=font(13, True), fill=INK)

# ================= NUMBER GRID =================
NUMBERS = [
    ("-3.3%", "Kospi rout, Asia", RED),
    ("5.3", "US-China power gap", NAVY),
    ("11,762", "Ebola cases, DRC", GREEN),
    ("10T won", "Seoul rescue fund", TEAL),
    ("2%", "Billionaire tax plan", PURPLE),
    ("$450M", "Skubal Mets deal", (120, 60, 10)),
    ("165", "Missiles in a week", RED),
    ("12,000", "Cleared, Manchester", (16, 90, 160)),
    ("264 kg", "Explosives, Lebanon", (120, 60, 10)),
    ("$107.3B", "Anthropic IPO", NAVY),
]
gx, gy, cw, ch = 16, 96, 198, 58
for i, (num, lab, col) in enumerate(NUMBERS):
    x = gx + (i % 5) * cw
    y = gy + (i // 5) * ch
    d.rectangle([x, y, x + cw - 6, y + ch - 6], fill=CARD_BG, outline=(200, 196, 186))
    d.rectangle([x, y, x + 4, y + ch - 6], fill=col)
    d.text((x + 12, y + 4), num, font=font(21, True), fill=col)
    d.text((x + 12, y + 32), lab, font=font(10), fill=(60, 60, 60))

# ================= REGION BAR =================
ry = 218
bx = 16
total = 31
for name, n, col in REGIONS:
    wseg = int((W - 32) * n / total)
    d.rectangle([bx, ry, bx + wseg - 2, ry + 22], fill=col)
    d.text((bx + 6, ry + 4), f"{name} {n}", font=font(10, True), fill=(255, 255, 255))
    bx += wseg

# ================= UTC STRIP =================
uy = 244
d.rectangle([0, uy, W, uy + 26], fill=(30, 30, 30))
d.text((16, uy + 5), "THE DAY IN UTC", font=font(11, True), fill=(255, 205, 60))
utc = ("00:00 Asia opens lower  ·  06:30 Kospi closes -3.3%  ·  ~12:00 Guterres at Bridgetown  ·  "
       "14:30 US opens, futures +3%  ·  ~18:00 Poland: 3 missiles  ·  23:00 wires read")
d.text((150, uy + 5), utc, font=font(10), fill=(235, 235, 235))

# ================= HEROES =================
HEROES = [
    dict(n=1, kick="SEOUL · MARKETS", chip="REPORTED", title="AI ROUT HITS ASIA",
         body="Kospi -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
         src="Yonhap · Reuters", col=RED, scene="chart"),
    dict(n=2, kick="BRIDGETOWN · AI", chip="REPORTED", title="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         body="UN chief urges global AI rules; 150 back a risk framework.",
         src="UN News · AP", col=NAVY, scene="podium"),
    dict(n=3, kick="ASIA POWER INDEX 2026", chip="REPORTED", title="US LEAD OVER CHINA AT RECORD LOW",
         body="US 78.9, China 73.6 — gap 5.3, narrowest since 2018. US diplomatic influence -6 to 76.7. India 3rd at 40.5.",
         src="Lowy Institute", col=TEAL, scene="bars"),
]
hx, hy, hw, hh = 16, 278, 322, 172
for i, hro in enumerate(HEROES):
    x = hx + i * (hw + 8)
    d.rectangle([x, hy, x + hw, hy + hh], fill=CARD_BG, outline=(200, 196, 186))
    # scene
    sx, sy, sw, sh = x + 6, hy + 6, hw - 12, 84
    d.rectangle([sx, sy, sx + sw, sy + sh], fill=(24, 34, 56))
    if hro["scene"] == "chart":
        # plunging chart
        pts = [(sx + 8, sy + 20), (sx + 50, sy + 30), (sx + 95, sy + 26),
               (sx + 140, sy + 48), (sx + 185, sy + 44), (sx + 230, sy + 66),
               (sx + 280, sy + 72)]
        d.line(pts, fill=(255, 80, 80), width=4)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 205, 60))
        d.text((sx + 10, sy + 6), "KOSPI 4,708.54", font=font(10, True), fill=(255, 255, 255))
        d.text((sx + sw - 10, sy + sh - 18), "-3.3%", font=font(16, True), fill=(255, 80, 80), anchor="ra")
    elif hro["scene"] == "podium":
        # UN-style podium + flags
        for j in range(5):
            fx = sx + 30 + j * 56
            d.line([fx, sy + 14, fx, sy + 56], fill=(180, 180, 180), width=2)
            d.polygon([(fx, sy + 14), (fx + 22, sy + 20), (fx, sy + 26)],
                      fill=[(0, 120, 180), (255, 205, 60), (178, 24, 24), (28, 110, 44), (96, 48, 140)][j])
        d.rectangle([sx + 120, sy + 52, sx + 190, sy + 84], fill=(120, 90, 40))
        d.ellipse([sx + 140, sy + 34, sx + 170, sy + 58], fill=(230, 200, 150))
        d.text((sx + 10, sy + 6), "BRIDGETOWN SUMMIT", font=font(10, True), fill=(255, 255, 255))
    else:
        # bar chart US vs China
        d.text((sx + 10, sy + 6), "POWER INDEX 2026", font=font(10, True), fill=(255, 255, 255))
        d.rectangle([sx + 40, sy + 34, sx + 120, sy + 78], fill=(0, 120, 200))
        d.rectangle([sx + 150, sy + 38, sx + 230, sy + 78], fill=(220, 60, 60))
        d.text((sx + 80, sy + 18), "78.9", font=font(13, True), fill=(255, 255, 255), anchor="ma")
        d.text((sx + 190, sy + 22), "73.6", font=font(13, True), fill=(255, 255, 255), anchor="ma")
        d.text((sx + 80, sy + 56), "US", font=font(9, True), fill=(255, 255, 255), anchor="ma")
        d.text((sx + 190, sy + 56), "CHINA", font=font(9, True), fill=(255, 255, 255), anchor="ma")
        d.text((sx + 255, sy + 10), "GAP 5.3", font=font(11, True), fill=(255, 205, 60))
    # text
    ty = hy + 96
    d.text((x + 8, ty), f"#{hro['n']}  {hro['kick']}", font=font(9, True), fill=hro["col"])
    chipc = CHIP[hro["chip"]]
    cw_ = d.textlength(hro["chip"], font=font(8, True)) + 10
    d.rectangle([x + hw - cw_ - 8, ty - 1, x + hw - 8, ty + 13], fill=chipc)
    d.text((x + hw - cw_ - 3, ty + 1), hro["chip"], font=font(8, True), fill=(255, 255, 255))
    ty += 16
    ty = text_block(d, x + 8, ty, wrap(d, hro["title"], font(13, True), hw - 16),
                    font(13, True), INK, lh=16, max_lines=2)
    ty = text_block(d, x + 8, ty + 2, wrap(d, hro["body"], font(10), hw - 16),
                    font(10), (50, 50, 50), lh=12, max_lines=3)
    d.text((x + 8, hy + hh - 14), f"Source: {hro['src']}", font=font(8), fill=GREY)

# ================= 10 SMALL CARDS =================
CARDS = [
    (4, "WASHINGTON · TECH", "REPORTED", "Bessent demands Nvidia answers",
     "Treasury chief wants to know who approved China chip sales.", "Reuters", (16, 90, 160)),
    (5, "FBI · CYBER", "REPORTED", "FBI probes hack of police database",
     "Intruders hit NCIC, used by police nationwide.", "AP", (16, 42, 90)),
    (6, "WASHINGTON · IRAN", "ONGOING", "Trump: Iran strikes may resume in New Year",
     "\u201cAll they do is talk,\u201d he says of Tehran.", "NewsNation", (120, 60, 10)),
    (8, "NEW YORK · SPORT", "REPORTED", "Skubal signs $450M Mets deal",
     "Two-time Cy Young winner, nine years — largest ever for a pitcher.", "ESPN", (28, 110, 44)),
    (11, "SAN FRANCISCO · TECH", "REPORTED", "Anthropic IPO: $107.3B, largest ever",
     "Claude maker debuts at $97.17 after pricing at $88 a share.", "Bloomberg", (96, 48, 140)),
    (12, "WARSAW · WAR", "CLAIM", "Poland: 3 Russian missiles crossed airspace",
     "Kyiv says three Kh-101s entered Poland on Friday; Tusk: provocation.", "AP", RED),
    (13, "SPACE · SECURITY", "CLAIM", "Intel warns of Russian nuclear satellite",
     "Moscow built a satellite to carry a warhead; launch possible next month.", "Bloomberg", (16, 42, 90)),
    (14, "PARIS · TAX", "REPORTED", "100+ back 2% billionaire tax",
     "Economists, politicians and unions rally behind the wealth-tax plan.", "AFP", PURPLE),
    (15, "MANCHESTER · UK", "REPORTED", "12,000 cleared after substance scare",
     "City centre emptied; no casualties reported.", "AP", (16, 90, 160)),
    (16, "KYIV · WAR", "REPORTED", "Zelenskyy: 165 Russian missiles in a week",
     "Moscow fired 165 missiles in seven days as US delays Patriots.", "Kyiv", RED),
]
cx, cy, cw2, ch2 = 16, 458, 198, 100
for i, (n, kick, chip, title, body, src, col) in enumerate(CARDS):
    x = cx + (i % 5) * cw2
    y = cy + (i // 5) * ch2
    d.rectangle([x, y, x + cw2 - 6, y + ch2 - 6], fill=CARD_BG, outline=(200, 196, 186))
    d.rectangle([x, y, x + cw2 - 6, y + 5], fill=col)
    d.text((x + 6, y + 10), f"#{n} {kick}", font=font(8, True), fill=col)
    chipc = CHIP[chip]
    cwid = d.textlength(chip, font=font(7, True)) + 8
    d.rectangle([x + cw2 - cwid - 12, y + 9, x + cw2 - 12, y + 21], fill=chipc)
    d.text((x + cw2 - cwid - 8, y + 10), chip, font=font(7, True), fill=(255, 255, 255))
    ty = y + 24
    ty = text_block(d, x + 6, ty, wrap(d, title, font(10, True), cw2 - 18),
                    font(10, True), INK, lh=12, max_lines=2)
    ty = text_block(d, x + 6, ty + 1, wrap(d, body, font(9), cw2 - 18),
                    font(9), (50, 50, 50), lh=11, max_lines=2)
    d.text((x + 6, y + ch2 - 16), f"Source: {src}", font=font(8), fill=GREY)

# ================= MAP + ALSO =================
my = 664
d.text((16, my), "THE WORLD — WHERE IT HAPPENED", font=font(12, True), fill=RED)
d.text((16, my + 14), "PIN = STORY NUMBER", font=font(8), fill=GREY)
d.text((640, my), "ALSO ON MONDAY — 18 MORE STORIES", font=font(12, True), fill=RED)

# simplified world map (equirectangular, lon -180..180 -> 16..624, lat 75..-55 -> my+30..my+150)
MAP_X0, MAP_X1, MAP_Y0, MAP_Y1 = 16, 624, my + 30, my + 152
d.rectangle([MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], fill=(205, 225, 240), outline=(160, 180, 200))


def ll(lon, lat):
    return (MAP_X0 + (lon + 180) / 360 * (MAP_X1 - MAP_X0),
            MAP_Y0 + (75 - lat) / 130 * (MAP_Y1 - MAP_Y0))


CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66), (-80, 62),
     (-75, 58), (-65, 60), (-55, 47), (-60, 45), (-70, 42), (-75, 35), (-80, 32),
     (-81, 26), (-85, 20), (-90, 14), (-95, 16), (-105, 20), (-110, 24), (-120, 34),
     (-125, 40), (-125, 49), (-135, 58), (-155, 58), (-165, 60)],
    # South America
    [(-80, 9), (-75, 11), (-65, 10), (-55, 6), (-50, 0), (-45, -5), (-35, -8),
     (-40, -20), (-48, -28), (-55, -35), (-65, -45), (-70, -52), (-73, -40),
     (-72, -20), (-78, -5), (-81, 2)],
    # Africa
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 20), (43, 12), (48, 10), (42, 0), (40, -10), (35, -20), (32, -28),
     (25, -34), (18, -32), (12, -18), (10, -5), (8, 4), (-8, 4), (-15, 10)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (35, 66), (40, 68),
     (45, 68), (40, 60), (35, 55), (30, 50), (28, 45), (23, 40), (20, 40),
     (15, 38), (10, 38), (3, 38), (-2, 37)],
    # Asia
    [(40, 68), (50, 70), (60, 70), (70, 72), (80, 73), (100, 76), (120, 73),
     (140, 72), (160, 70), (178, 65), (170, 60), (158, 52), (142, 45), (135, 35),
     (127, 40), (122, 32), (120, 25), (110, 20), (105, 10), (100, 8), (95, 15),
     (90, 22), (85, 20), (80, 15), (75, 8), (70, 20), (65, 25), (58, 25),
     (52, 28), (48, 30), (44, 30), (40, 36), (36, 36), (30, 36), (28, 42),
     (32, 45), (38, 48), (42, 55), (40, 62)],
    # Australia
    [(114, -22), (122, -14), (132, -12), (142, -11), (146, -19), (150, -22),
     (153, -27), (150, -37), (140, -38), (130, -32), (120, -34), (114, -30)],
]
LAND = (232, 214, 170)
for poly in CONTINENTS:
    d.polygon([ll(lon, lat) for lon, lat in poly], fill=LAND, outline=(180, 165, 130))

PINS = [
    (1, 127, 37.5), (2, -59.6, 13.1), (3, -77, 39), (4, -77, 39), (5, -77, 38),
    (6, -77, 39), (7, -74, 40.7), (8, -74, 40.7), (9, -105, 39.7), (10, -78, 37.5),
    (11, -122.4, 37.8), (12, 21, 52.2), (13, 37.6, 55.75), (14, 2.35, 48.85),
    (15, -2.24, 53.48), (16, 30.5, 50.45), (17, 30.7, 36.9), (18, 20.1, 32.1),
    (19, 34.8, 32.1), (20, 34.45, 31.5), (21, 35.2, 31.9), (22, 51.4, 35.7),
    (23, 35.5, 33.9), (24, 50.6, 26.2), (25, 32.5, 15.6), (26, 29.5, 1.5),
    (27, 90.4, 23.8), (28, 127, 37.5), (29, 127, 37.5), (30, 116.4, 39.9),
    (31, 127, 37.5),
]
# nudge overlapping pins (Seoul cluster, Washington cluster, NYC, Levant, Moscow/Kyiv)
NUDGE = {1: (0, -11), 3: (0, -11), 4: (-12, 0), 5: (12, 0), 6: (0, 11),
         7: (-8, -8), 8: (8, 8), 13: (8, -8), 16: (-8, 8),
         19: (-11, -10), 20: (11, 9), 21: (11, -10), 22: (9, -8),
         23: (-11, 9), 24: (-9, 8), 28: (-11, 8), 29: (11, -8), 31: (0, 10)}
for n, lon, lat in PINS:
    x, y = ll(lon, lat)
    dx, dy = NUDGE.get(n, (0, 0))
    x, y = x + dx, y + dy
    r = 6
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=(255, 255, 255))
    d.text((x, y - 1), str(n), font=font(6, True), fill=(255, 255, 255), anchor="mm")

# ALSO list (right column, 2 sub-columns)
ALSO = [
    ("7", "Nasdaq futures jump 3%"),
    ("9", "Tom Jackson dies at 75"),
    ("10", "10 states sue SpaceX"),
    ("17", "COP31: the day after"),
    ("18", "Benghazi: UN wants port probe"),
    ("19", "Israel unity talks resume"),
    ("20", "Gaza: two killed in strike"),
    ("21", "West Bank settler attacks"),
    ("22", "Iran war: no deal in sight"),
    ("23", "Lebanon seizes 264 kg explosives"),
    ("24", "Bahrain: strike hits plant"),
    ("25", "Sudan downs drones over Khartoum"),
    ("26", "DRC: fighting traps Ebola teams"),
    ("27", "Bangladesh: Hasina jailed if back"),
    ("28", "Seoul minister quits in exam row"),
    ("29", "SK Telecom -7.3%"),
    ("30", "China eases margin rules"),
    ("31", "Seoul readies 10T-won fund"),
]
ay = my + 26
for i, (n, t) in enumerate(ALSO):
    col = 0 if i < 9 else 1
    row = i % 9
    x = 640 + col * 190
    y = ay + row * 17
    d.text((x, y), n, font=font(9, True), fill=RED)
    lines = wrap(d, t, font(9), 168)
    text_block(d, x + 18, y, lines, font(9), INK, lh=11, max_lines=1)

# ================= DATE CHECK =================
dy = 844
d.rectangle([16, dy, W - 16, dy + 104], fill=(255, 235, 235), outline=RED, width=2)
d.text((28, dy + 8), "DATE CHECK", font=font(13, True), fill=RED)
d.text((28, dy + 26),
       "Every story above happened or was first reported on Monday 23 November 2026.",
       font=font(11, True), fill=INK)
d.text((W - 28, dy + 8), "WIRES READ UP TO 23:00 UTC", font=font(10, True), fill=RED, anchor="ra")
left = ("LEFT OUT (not 23 Nov): Democrats reach 258 (22 Nov) · Sparta II fire (22 Nov) · "
        "El Chapo Isidro captured (22 Nov) · EU–Indonesia pact (21 Nov) · "
        "Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov).")
ny = ("NOT YET: Dymer search continues (14 missing) · 4 House races uncalled · "
      "COP32 venue not set · WHO evacuating trapped Ebola staff.")
text_block(d, 28, dy + 46, wrap(d, left, font(10), W - 56), font(10), INK, lh=13, max_lines=2)
text_block(d, 28, dy + 74, wrap(d, ny, font(10), W - 56), font(10), INK, lh=13, max_lines=2)

# ================= FOOTER =================
fy = 958
d.text((16, fy), "SOURCES: AP · Reuters · Bloomberg · Yonhap · AFP · ESPN · BBC · UN News · Lowy Institute · Kyiv · SCMP · NewsNation",
       font=font(9), fill=GREY)
d.text((16, fy + 14), "REPORTED = confirmed by its source  ·  CLAIM = one side alleges, unverified  ·  ONGOING = still developing  ·  OFFICIAL = recorded result",
       font=font(9), fill=GREY)
d.text((16, fy + 28), "Red pin = reported  ·  Amber pin = claim (unverified).  Times marked ~ are approximate, UTC.",
       font=font(9), fill=GREY)
d.text((W - 16, fy + 42), "Scenes are drawn illustrations, not photographs.",
       font=font(9), fill=GREY, anchor="ra")

img.save(OUT, optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
