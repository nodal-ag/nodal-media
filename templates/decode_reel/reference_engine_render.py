"""Nodal Reel 3: 'the engine'. 24 s, 1080x1920, loopable. Spec: luxury, slow, easing only."""
import sys, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, DUR, SS = 1080, 1920, 30, 24.0, 2
OUT = sys.argv[1]
INK = (13, 11, 31); VIO = (139, 124, 255); OFF = (245, 246, 248); MUT = (169, 166, 191); LIN = (66, 61, 99)
TAU = 2 * math.pi
CAR = '/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf'
CP = '/home/claude/reel/fonts/CourierPrime-Regular.ttf'
HEAD = ImageFont.truetype(CAR, 70)
LAB = ImageFont.truetype(CP, 26)
CAP = ImageFont.truetype(CP, 29)
CAPS = ImageFont.truetype(CP, 23)

def ease(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def seg(t, a, b): return ease((t - a) / (b - a))
def fade(t, a, b, fi=0.6, fo=0.6):
    if t < a or t > b: return 0.0
    return min(ease((t - a) / fi), ease((b - t) / fo))
def lerp(a, b, u): return a + (b - a) * u
def rgba(c, a): return (int(c[0]), int(c[1]), int(c[2]), int(255 * max(0.0, min(1.0, a))))
def mixc(c1, c2, u): return tuple(lerp(a, b, u) for a, b in zip(c1, c2))
def shade(c, k): return tuple(v * k for v in c)

# ---------------- camera ----------------
C0 = (540.0, 1030.0)
def camera(t):
    s = 1.0 + 0.012 * math.sin(TAU * t / 24)
    s *= 1 + 0.30 * seg(t, 10.0, 11.6) - 0.30 * seg(t, 15.8, 17.0)
    ox = 7 * math.sin(TAU * t / 24); oy = 5 * math.sin(2 * TAU * t / 24)
    return s, ox, oy
def T(p, cam):
    s, ox, oy = cam
    return (C0[0] + (p[0] - C0[0]) * s + ox, C0[1] + (p[1] - C0[1]) * s + oy)

# ---------------- background (static) ----------------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.sqrt(((xx - 540) / 700) ** 2 + ((yy - 1000) / 1050) ** 2)
VIGN = np.clip(1.08 - 0.55 * r ** 1.6, 0.35, 1.0)[..., None]
BG = np.zeros((H, W, 3), np.float32) + np.array(INK, np.float32)
BG = BG * VIGN
rng = np.random.default_rng(3)
DUST = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.6, 1.6), rng.uniform(0.08, 0.32), rng.uniform(0, TAU), rng.integers(1, 3)) for _ in range(140)]

# ---------------- the engine (sprite, world units) ----------------
FX0, FX1, FY0, FY1 = 390.0, 690.0, 690.0, 1370.0     # front face
DX, DY = 42.0, -20.0                                  # depth offset (side + top faces)
SPR_K = 2.8                                           # sprite resolution (px per world unit)
SPR_OX, SPR_OY = FX0 - 10, FY0 + DY - 10              # sprite origin in world
SPR_W, SPR_H = (FX1 + DX + 10) - SPR_OX, (FY1 + 10) - SPR_OY

def build_engine():
    k = SPR_K; w, h = int(SPR_W * k), int(SPR_H * k)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda x, y: ((x - SPR_OX) * k, (y - SPR_OY) * k)
    # side face
    d.polygon([P(FX1, FY0), P(FX1 + DX, FY0 + DY), P(FX1 + DX, FY1 + DY), P(FX1, FY1)], fill=rgba(shade(INK, 0.45), 1))
    # front face: vertical obsidian gradient
    fw, fh = int((FX1 - FX0) * k), int((FY1 - FY0) * k)
    gy = np.linspace(0, 1, fh)[:, None]; gx = np.linspace(0, 1, fw)[None, :]
    base = 0.62 - 0.22 * gy + 0.10 * np.exp(-((gx - 0.18) / 0.10) ** 2) * (1 - gy * 0.7)
    face = np.zeros((fh, fw, 4), np.float32)
    face[..., :3] = np.array(INK, np.float32) * base[..., None]
    face[..., 3] = 255
    im.alpha_composite(Image.fromarray(face.astype(np.uint8)), (int((FX0 - SPR_OX) * k), int((FY0 - SPR_OY) * k)))
    # top face (brushed metal)
    d.polygon([P(FX0, FY0), P(FX0 + DX, FY0 + DY), P(FX1 + DX, FY0 + DY), P(FX1, FY0)], fill=rgba(mixc(LIN, MUT, 0.35), 1))
    # caps: brushed metal bands
    for (y0, y1) in [(FY0, FY0 + 16), (FY1 - 16, FY1)]:
        for i in range(int((y1 - y0) * k)):
            u = i / ((y1 - y0) * k)
            c = mixc(LIN, MUT, 0.25 + 0.5 * math.sin(math.pi * u) + 0.08 * math.sin(i * 1.7))
            d.line([P(FX0, y0 + i / k), P(FX1, y0 + i / k)], fill=rgba(c, 1))
        d.line([P(FX1, y0), P(FX1 + DX, y0 + DY)], fill=rgba(LIN, 1), width=2)
    # glass front panel (faint)
    gx0, gx1, gy0, gy1 = FX0 + 18, FX1 - 18, FY0 + 34, FY1 - 34
    d.rectangle([P(gx0, gy0), P(gx1, gy1)], fill=rgba(OFF, 0.025), outline=rgba(LIN, 0.55), width=2)
    # rim light on the left edge, fading at its ends
    n = 80
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n; a = math.sin(math.pi * (u0 + u1) / 2) ** 1.5
        d.line([P(FX0, lerp(FY0, FY1, u0)), P(FX0, lerp(FY0, FY1, u1))], fill=rgba(MUT, 0.55 * a), width=3)
        d.line([P(FX1, lerp(FY0, FY1, u0)), P(FX1, lerp(FY0, FY1, u1))], fill=rgba(LIN, 0.9 * a), width=2)
    return im
ENGINE = build_engine()

# S-curve on the front face (Catmull-Rom through control points)
CTRL = [(FX0 + 2, 748), (470, 752), (628, 790), (640, 862), (470, 930), (446, 1000), (520, 1060), (628, 1100),
        (640, 1175), (470, 1240), (455, 1300), (560, 1318), (FX1 - 2, 1322)]
def catmull(pts, n=24):
    out = []; P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(n):
            u = j / n; u2, u3 = u * u, u * u * u
            out.append(tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * u + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * u2 +
                                  (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * u3) for k in (0, 1)))
    out.append(pts[-1]); return out
CURVE = catmull(CTRL)
CL = np.concatenate([[0], np.cumsum([math.dist(a, b) for a, b in zip(CURVE, CURVE[1:])])]); CL /= CL[-1]
def on_curve(s):
    i = int(np.searchsorted(CL, s)); i = min(max(i, 1), len(CURVE) - 1)
    u = (s - CL[i - 1]) / max(CL[i] - CL[i - 1], 1e-9)
    return (lerp(CURVE[i - 1][0], CURVE[i][0], u), lerp(CURVE[i - 1][1], CURVE[i][1], u))
NODES_S = [0.2, 0.4, 0.6, 0.8]
NODES = [on_curve(s) for s in NODES_S]
PORT_IN, PORT_OUT = CURVE[0], CURVE[-1]
STEP_T = [11.2, 12.4, 13.6, 14.8]
STEPS = [('01 · READ', 'field extraction from invoices, delivery notes, certificates'),
         ('02 · CHECK', 'consistency against the ERP and customs rules'),
         ('03 · ROUTE', 'each document sent to the right person or system'),
         ('04 · APPROVE', 'human sign-off only where it matters')]

# ---------------- floating documents and servers ----------------
TITLES = ['COMMERCIAL INVOICE', 'CERTIFICATE OF ORIGIN', 'DELIVERY NOTE', 'EXPORT DECLARATION', 'EUR.1', 'PACKING LIST', 'CUSTOMER STATEMENT']
def doc_sprite(title, seed):
    k = SS; w, h = int(150 * k), int(196 * k)
    im = Image.new('RGBA', (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([20 + 6, 20 + 8, 20 + w + 6, 20 + h + 8], fill=(0, 0, 0, 90))
    im = im.filter(ImageFilter.GaussianBlur(8)); d = ImageDraw.Draw(im)
    d.rectangle([20, 20, 20 + w, 20 + h], fill=rgba(OFF, 0.93))
    f = ImageFont.truetype(CP, int(9.5 * k)); tw = d.textlength(title, font=f)
    d.text((20 + 14 * k, 20 + 14 * k), title, font=f, fill=rgba(INK, 0.85))
    d.line([20 + 14 * k, 20 + 30 * k, 20 + w - 14 * k, 20 + 30 * k], fill=rgba(MUT, 0.9), width=k)
    rr = np.random.default_rng(seed)
    for i in range(9):
        y = 20 + (44 + i * 14) * k; ww = rr.uniform(0.45, 0.95) * (w - 28 * k)
        d.line([20 + 14 * k, y, 20 + 14 * k + ww, y], fill=rgba(MUT, 0.75), width=int(2.4 * k))
    return im
def server_sprite(seed):
    k = SS; w, h = int(92 * k), int(150 * k)
    im = Image.new('RGBA', (w + 4, h + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([2, 2, 2 + w, 2 + h], fill=rgba(shade(INK, 0.55), 1), outline=rgba(LIN, 1), width=k)
    for i in range(6):
        y = 2 + (14 + i * 22) * k
        d.rectangle([2 + 8 * k, y, 2 + w - 8 * k, y + 14 * k], outline=rgba(LIN, 0.9), width=k)
    return im
ITEMS = []   # (kind, sprite, world pos, base angle, scale)
DOCPOS = [(170, 650, -18), (895, 640, 14), (115, 905, 22), (975, 900, -12), (235, 1190, 9), (905, 1165, -25),
          (150, 1450, -8), (935, 1440, 17), (330, 610, 7), (770, 1545, -15)]
SRVPOS = [(290, 1015), (790, 560), (300, 1560), (800, 1270)]
for i, (x, y, a) in enumerate(DOCPOS): ITEMS.append(('doc', doc_sprite(TITLES[i % len(TITLES)], i), (x, y), a, 0.92 + 0.12 * (i % 3) / 2))
for i, (x, y) in enumerate(SRVPOS): ITEMS.append(('srv', server_sprite(i), (x, y), [4, -6, 3, -5][i], 0.8))
ORDER = [0, 10, 1, 2, 11, 3, 4, 12, 5, 6, 13, 7, 8, 9]   # capture order, servers interleaved
CAPT = {idx: 5.2 + n * 0.32 for n, idx in enumerate(ORDER)}

def item_state(i, t):
    kind, spr, (x, y), a0, sc = ITEMS[i]
    w1, w2 = TAU / 24 * 2, TAU / 24 * 3
    fx = x + 9 * math.sin(w1 * t + i * 1.3); fy = y + 11 * math.sin(w2 * t + i * 0.7)
    ang = a0 + 5 * math.sin(w1 * t + i)
    appear = seg(t, 0.15 + i * 0.03, 0.9 + i * 0.03)
    tc = CAPT[i]
    if kind == 'doc':
        straighten = seg(t, tc + 0.22, tc + 0.5); u = seg(t, tc + 0.4, tc + 1.05)
        px, py = lerp(fx, PORT_IN[0], u), lerp(fy, PORT_IN[1], u)
        return dict(pos=(px, py), ang=ang * (1 - straighten), scale=sc * lerp(1, 0.12, u), alpha=appear * (1 - seg(u, 0.85, 1.0)), u=u)
    fadeout = 1 - seg(t, 10.0, 11.0)
    return dict(pos=(fx, fy), ang=ang * (1 - seg(t, tc + 0.22, tc + 0.6)), scale=sc, alpha=appear * fadeout, u=0)

# ---------------- wordmark (from the SVG paths, translate(2,0)) ----------------
def quad(p0, c, p1, n=14): return [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * c[0] + u * u * p1[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * c[1] + u * u * p1[1]) for u in np.linspace(0, 1, n)]
def circ(cx, cy, r_, n=64): return [(cx + r_ * math.cos(-math.pi / 2 - a), cy + r_ * math.sin(-math.pi / 2 - a)) for a in np.linspace(0, TAU, n)]
N_PATH = [(24, 78), (24, 31)] + quad((24, 31), (24, 20), (32, 28))[1:] + [(68, 72)] + quad((68, 72), (76, 80), (76, 69))[1:] + [(76, 22)]
STROKES = [N_PATH, circ(108, 58, 20), circ(158, 58, 20), [(178, 22), (178, 78)], circ(210, 58, 20),
           [(230, 40), (230, 70)] + quad((230, 70), (230, 78), (238, 78))[1:], [(250, 22), (250, 70)] + quad((250, 70), (250, 78), (258, 78))[1:]]
STROKES = [[(x + 2, y) for x, y in s] for s in STROKES]
WK = 3.25; WCX, WCY = 540, 980
def wm(p): return (WCX + (p[0] - 139.5) * WK, WCY + (p[1] - 50) * WK)
SLEN = [sum(math.dist(a, b) for a, b in zip(s, s[1:])) for s in STROKES]; TOT = sum(SLEN)
def partial(pts, frac):
    if frac <= 0: return []
    L = sum(math.dist(a, b) for a, b in zip(pts, pts[1:])); goal = L * frac; out = [pts[0]]; acc = 0
    for a, b in zip(pts, pts[1:]):
        d = math.dist(a, b)
        if acc + d >= goal:
            u = (goal - acc) / d if d else 0; out.append((lerp(a[0], b[0], u), lerp(a[1], b[1], u))); return out
        out.append(b); acc += d
    return out
WM0, WM1 = 21.35, 22.55

# ---------------- drawing helpers ----------------
def faded_line(dr, p0, p1, c, a, w, n=24, k=SS):
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n; al = a * math.sin(math.pi * (u0 + u1) / 2) ** 0.8
        dr.line([(lerp(p0[0], p1[0], u0) * k, lerp(p0[1], p1[1], u0) * k), (lerp(p0[0], p1[0], u1) * k, lerp(p0[1], p1[1], u1) * k)], fill=rgba(c, al), width=max(1, int(w * k)))
def dot(dr, p, r_, c, a, k=SS): dr.ellipse([(p[0] - r_) * k, (p[1] - r_) * k, (p[0] + r_) * k, (p[1] + r_) * k], fill=rgba(c, a))
def ring(dr, p, r_, c, a, w, k=SS): dr.ellipse([(p[0] - r_) * k, (p[1] - r_) * k, (p[0] + r_) * k, (p[1] + r_) * k], outline=rgba(c, a), width=max(1, int(w * k)))
def tracked(dr, xy, s, font, fill, track=0.3, anchor='l', k=1):
    ws = [dr.textlength(ch, font=font) + font.size * track for ch in s]; tot = sum(ws) - font.size * track
    x, y = xy
    if anchor == 'm': x -= tot / 2
    if anchor == 'r': x -= tot
    for ch, w_ in zip(s, ws): dr.text((x, y), ch, font=font, fill=fill); x += w_
def wrap(dr, s, font, maxw):
    lines, cur = [], ''
    for w_ in s.split(' '):
        nx = (cur + ' ' + w_).strip()
        if dr.textlength(nx, font=font) > maxw and cur: lines.append(cur); cur = w_
        else: cur = nx
    return lines + [cur]

ACTS = [(0.0, 5.0, '// 01 — CHAOS', 'Files everywhere. Hours lost.'),
        (5.0, 10.0, '// 02 — CAPTURE', 'Every document captured the moment it arrives.'),
        (10.0, 15.8, '// 03 — PROCESS', 'Read, checked, routed, approved. Untouched.'),
        (15.8, 21.1, '// 04 — RESULT', 'Every shipment file, assembled automatically.')]

def card_sprite(kind):
    k = SS; w = 800 if kind == 'main' else 740; h = 500 if kind == 'main' else 150
    im = Image.new('RGBA', (w * k, h * k), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w * k - 1, h * k - 1], radius=14 * k, fill=rgba(mixc(INK, LIN, 0.18), 0.97), outline=rgba(LIN, 1), width=2 * k)
    fT = ImageFont.truetype(CAR, 40 * k); fL = ImageFont.truetype(CP, 19 * k); fR = ImageFont.truetype(CAR, 32 * k)
    if kind == 'main':
        tracked(d, (40 * k, 34 * k), 'EXPORT FILE', fL, rgba(MUT, 1), 0.3)
        d.text((40 * k, 66 * k), 'Shipment No. 2611-047', font=fT, fill=rgba(OFF, 1))
        for i in range(24):
            u0, u1 = i / 24, (i + 1) / 24; a = math.sin(math.pi * (u0 + u1) / 2)
            d.line([(40 + 720 * u0) * k, 132 * k, (40 + 720 * u1) * k, 132 * k], fill=rgba(LIN, a), width=k)
        for j, row in enumerate(['Commercial invoice', 'Packing list', 'Certificate of origin', 'Customs declaration']):
            y = (160 + j * 66) * k
            d.text((96 * k, y), row, font=fR, fill=rgba(OFF, 0.92))
            d.ellipse([40 * k, y + 4 * k, 72 * k, y + 36 * k], outline=rgba(LIN, 1), width=2 * k)
    else:
        tracked(d, (40 * k, 34 * k), 'DOCUMENT', fL, rgba(MUT, 1), 0.3)
        d.text((40 * k, 66 * k), 'CERTIFICATE OF CONFORMITY', font=ImageFont.truetype(CAR, 34 * k), fill=rgba(OFF, 0.95))
    return im
CARD_MAIN, CARD_2 = card_sprite('main'), card_sprite('second')
MAIN_C, SEC_C = (540, 1110), (540, 830)

# ---------------- frame ----------------
def frame(i):
    t = i / FPS; cam = camera(t); s = cam[0]
    base = BG.copy()
    lay = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0)); dr = ImageDraw.Draw(lay)
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    wide = Image.new('RGBA', (W, H), (0, 0, 0, 0)); wd = ImageDraw.Draw(wide)
    # dust
    for (x, y, rr_, a, ph, m) in DUST:
        px = x + 18 * math.sin(TAU * t / 24 * m + ph); py = y + 26 * math.sin(TAU * t / 24 + ph * 1.3)
        dot(dr, (px, py), rr_, MUT, a)
    # engine brightness
    dim = 1 - 0.62 * seg(t, 16.0, 17.0) - 0.25 * seg(t, 21.0, 21.6) + 0.87 * seg(t, 23.3, 24.0)
    dim = min(1.0, max(0.12, dim))
    # floor ring
    fc = T((560, 1402), cam); rx, ry = 270 * s, 44 * s
    wd.ellipse([fc[0] - rx, fc[1] - ry, fc[0] + rx, fc[1] + ry], outline=rgba(VIO, 0.55 * dim), width=6)
    dr.ellipse([(fc[0] - rx) * SS, (fc[1] - ry) * SS, (fc[0] + rx) * SS, (fc[1] + ry) * SS], outline=rgba(VIO, 0.45 * dim), width=2 * SS)
    # engine sprite
    tl = T((SPR_OX, SPR_OY), cam); sw, sh = int(SPR_W * s * SS), int(SPR_H * s * SS)
    eng = ENGINE.resize((sw, sh), Image.BILINEAR)
    if dim < 0.999:
        a_ = np.asarray(eng, np.float32); a_[..., 3] *= dim; eng = Image.fromarray(a_.astype(np.uint8))
    lay.alpha_composite(eng, (int(tl[0] * SS), int(tl[1] * SS)))
    # clearcoat sheen sweeping slowly across the front face
    u = 0.5 + 0.5 * math.sin(TAU * t / 24 - 1.2)
    sx = lerp(FX0 - 80, FX1 + 40, u)
    sheen = Image.new('RGBA', lay.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sheen)
    poly = [T((sx, FY0), cam), T((sx + 70, FY0), cam), T((sx + 10, FY1), cam), T((sx - 60, FY1), cam)]
    sd.polygon([(x * SS, y * SS) for x, y in poly], fill=rgba(OFF, 0.07 * dim))
    m = Image.new('L', lay.size, 0); ImageDraw.Draw(m).polygon([(x * SS, y * SS) for x, y in [T((FX0, FY0 + 16), cam), T((FX1, FY0 + 16), cam), T((FX1, FY1 - 16), cam), T((FX0, FY1 - 16), cam)]], fill=255)
    lay.paste(sheen, (0, 0), Image.fromarray(np.minimum(np.asarray(m), np.asarray(sheen.split()[-1])).astype(np.uint8)))
    # the S-curve line, nodes and particles
    lw = 0.85 * dim + 0.15
    pts = [T(p, cam) for p in CURVE]
    dr.line([(x * SS, y * SS) for x, y in pts], fill=rgba(VIO, 0.85 * lw), width=int(2.2 * s * SS), joint='curve')
    gd.line(pts, fill=rgba(VIO, 0.75 * lw), width=int(6 * s))
    wd.line(pts, fill=rgba(VIO, 0.35 * lw), width=int(14 * s))
    for k_ in range(42):
        sp = ((k_ / 42) + t / 3.0) % 1.0
        p = T(on_curve(sp), cam); a = math.sin(math.pi * sp) ** 0.5 * lw
        dot(dr, p, 2.4 * s, (225, 220, 255), a); gd.ellipse([p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7], fill=rgba(VIO, 0.6 * a))
    absorbed = sum(1 for idx in ORDER if ITEMS[idx][0] == 'doc' and t > CAPT[idx] + 1.05 and t < 23.9)
    for n_, (pn, ts) in enumerate(zip(NODES, STEP_T)):
        p = T(pn, cam); lit = fade(t, ts, 15.9, 0.35, 0.6)
        dot(dr, p, (4.5 + 2.5 * lit) * s, mixc((200, 192, 255), OFF, lit), lw)
        ring(dr, p, (11 + 5 * lit) * s, VIO, (0.55 + 0.45 * lit) * lw, 1.6)
        gd.ellipse([p[0] - 18 * s, p[1] - 18 * s, p[0] + 18 * s, p[1] + 18 * s], fill=rgba(VIO, (0.5 + 0.5 * lit) * lw))
        if lit > 0:
            pr = (t - ts) / 0.9
            if 0 < pr < 1: ring(dr, p, (16 + 40 * pr) * s, VIO, 0.6 * (1 - pr), 1.4)
    for port, boost in [(PORT_IN, min(1.0, 0.35 + 0.075 * absorbed + 0.5 * fade(t, 5.0, 10.4, 0.3, 0.6))), (PORT_OUT, 0.4 + 0.6 * fade(t, 16.2, 19.0, 0.3, 0.8))]:
        p = T(port, cam); b = boost * lw
        ring(dr, p, 8 * s, OFF, 0.8 * b, 1.6); dot(dr, p, 3.5 * s, OFF, b)
        wd.ellipse([p[0] - 34 * s, p[1] - 34 * s, p[0] + 34 * s, p[1] + 34 * s], fill=rgba(VIO, 0.6 * b))
    # documents and servers (acts 1-2)
    if t < 11.5:
        for idx in range(len(ITEMS)):
            st = item_state(idx, t)
            if st['alpha'] <= 0.01: continue
            kind, spr = ITEMS[idx][0], ITEMS[idx][1]
            p = T(st['pos'], cam); sc = st['scale'] * s
            im = spr.resize((max(2, int(spr.width * sc)), max(2, int(spr.height * sc))), Image.BILINEAR).rotate(st['ang'], resample=Image.BICUBIC, expand=True)
            if st['alpha'] < 1:
                a_ = np.asarray(im, np.float32); a_[..., 3] *= st['alpha']; im = Image.fromarray(a_.astype(np.uint8))
            lay.alpha_composite(im, (int(p[0] * SS - im.width / 2), int(p[1] * SS - im.height / 2)))
            if kind == 'srv':
                for j in range(6):
                    if (int(t * 2.2) + j + idx) % 3:
                        ly = st['pos'][1] - 75 * ITEMS[idx][4] + (21 + j * 22) * ITEMS[idx][4]
                        lp = T((st['pos'][0] + 30 * ITEMS[idx][4], ly), cam)
                        dot(dr, lp, 1.8 * s, (200, 192, 255), st['alpha'])
            # beam from the input port
            tc = CAPT[idx]; bu = seg(t, tc, tc + 0.28)
            if bu > 0:
                pin = T(PORT_IN, cam); tgt = p
                end = (lerp(pin[0], tgt[0], bu), lerp(pin[1], tgt[1], bu))
                if kind == 'doc':
                    ba = 1 - seg(t, tc + 0.9, tc + 1.2)
                else:
                    ba = 0.55 * (1 - seg(t, 9.8, 10.8)) + 0.45 * (1 - seg(t, tc + 0.3, tc + 0.8))
                if ba > 0:
                    faded_line(dr, pin, end, VIO, 0.9 * ba, 1.4)
                    gd.line([pin, end], fill=rgba(VIO, 0.45 * ba), width=4)
            # burst of particles when a document dissolves into the port
            if kind == 'doc':
                bt = t - (tc + 1.0)
                if 0 < bt < 0.7:
                    pin = T(PORT_IN, cam)
                    for q in range(12):
                        ang = q / 12 * TAU + idx; rr_ = 6 + 60 * ease(bt / 0.7)
                        pp = (pin[0] + rr_ * math.cos(ang), pin[1] + rr_ * math.sin(ang) * 0.8)
                        dot(dr, pp, 2.2, (220, 214, 255), 1 - bt / 0.7)
                        gd.ellipse([pp[0] - 6, pp[1] - 6, pp[0] + 6, pp[1] + 6], fill=rgba(VIO, 0.6 * (1 - bt / 0.7)))
    # output cards (act 4)
    cards_a = 1 - seg(t, 20.9, 21.5)
    for spr, c_end, t0 in [(CARD_2, SEC_C, 16.75), (CARD_MAIN, MAIN_C, 16.3)]:
        u = seg(t, t0, t0 + 1.1)
        if u <= 0 or cards_a <= 0: continue
        start = T(PORT_OUT, cam); pc = (lerp(start[0], c_end[0], u), lerp(start[1], c_end[1], u)); sc = lerp(0.08, 1.0, u)
        im = spr.resize((max(2, int(spr.width * sc)), max(2, int(spr.height * sc))), Image.BILINEAR)
        a_ = np.asarray(im, np.float32); a_[..., 3] *= min(1, u * 1.6) * cards_a; im = Image.fromarray(a_.astype(np.uint8))
        lay.alpha_composite(im, (int(pc[0] * SS - im.width / 2), int(pc[1] * SS - im.height / 2)))
    if t > 17.4 and cards_a > 0:
        x0, y0 = MAIN_C[0] - 400, MAIN_C[1] - 250
        for j in range(4):
            cu = seg(t, 17.6 + j * 0.45, 17.95 + j * 0.45)
            if cu > 0:
                cx_, cy_ = x0 + 56, y0 + 160 + j * 66 + 20
                pts_c = [(cx_ - 8, cy_), (cx_ - 2, cy_ + 7), (cx_ + 10, cy_ - 8)]
                L1 = math.dist(pts_c[0], pts_c[1]); L2 = math.dist(pts_c[1], pts_c[2]); g = cu * (L1 + L2)
                seg_pts = [pts_c[0]]
                if g <= L1: seg_pts.append((lerp(pts_c[0][0], pts_c[1][0], g / L1), lerp(pts_c[0][1], pts_c[1][1], g / L1)))
                else:
                    seg_pts.append(pts_c[1]); v = (g - L1) / L2; seg_pts.append((lerp(pts_c[1][0], pts_c[2][0], v), lerp(pts_c[1][1], pts_c[2][1], v)))
                dr.line([(x * SS, y * SS) for x, y in seg_pts], fill=rgba(VIO, cards_a), width=3 * SS, joint='curve')
                ring(dr, (cx_, cy_), 16, VIO, 0.9 * cards_a, 1.6)
                gd.ellipse([cx_ - 18, cy_ - 18, cx_ + 18, cy_ + 18], fill=rgba(VIO, 0.45 * cards_a))
        ba = seg(t, 19.6, 20.0) * cards_a
        if ba > 0:
            bx0, by0, bx1, by1 = MAIN_C[0] + 400 - 40 - 190, MAIN_C[1] + 250 - 40 - 50, MAIN_C[0] + 400 - 40, MAIN_C[1] + 250 - 40
            dr.rounded_rectangle([bx0 * SS, by0 * SS, bx1 * SS, by1 * SS], radius=25 * SS, outline=rgba(VIO, ba), width=2 * SS)
            gd.rounded_rectangle([bx0, by0, bx1, by1], radius=25, outline=rgba(VIO, 0.7 * ba), width=5)
            fB = ImageFont.truetype(CP, 22 * SS)
            tracked(dr, (((bx0 + bx1) / 2) * SS, (by0 + 13) * SS), 'COMPLETE', fB, rgba((205, 198, 255), ba), 0.3, 'm')
    # wordmark close
    if t > WM0 - 0.05:
        wa = 1 - seg(t, 23.35, 23.95)
        drawn = (t - WM0) / (WM1 - WM0) * TOT; acc = 0
        if wa > 0:
            # hollow node at the start of the N
            na = seg(t, WM0, WM0 + 0.25) * wa; nc = wm((26, 78))
            for si, (st_, L) in enumerate(zip(STROKES, SLEN)):
                frac = min(max((drawn - acc) / L, 0), 1); acc += L
                pp = [wm(p) for p in partial(st_, frac)]
                if len(pp) > 1:
                    dr.line([(x * SS, y * SS) for x, y in pp], fill=rgba(OFF, wa), width=int(3.2 * WK * SS), joint='curve')
                    for e in (pp[0], pp[-1]): dot(dr, e, 1.6 * WK, OFF, wa)
            if na > 0:
                dot(dr, nc, 6.5 * WK + 1.36 * WK, OFF, na); dot(dr, nc, 6.5 * WK - 1.36 * WK, INK, na)
            da = seg(t, WM1 + 0.05, WM1 + 0.4) * wa
            if da > 0:
                dc = wm((78, 22 - 10 * (1 - da)))
                dot(dr, dc, 8 * WK * (0.6 + 0.4 * da), VIO, da)
                wd.ellipse([dc[0] - 70, dc[1] - 70, dc[0] + 70, dc[1] + 70], fill=rgba(VIO, 0.8 * da))
                gd.ellipse([dc[0] - 34, dc[1] - 34, dc[0] + 34, dc[1] + 34], fill=rgba(VIO, 0.7 * da))
    # composite
    lay = lay.resize((W, H), Image.LANCZOS)
    out = base
    for g_, rad, k_ in [(wide, 38, 0.9), (glow, 10, 1.0)]:
        ga = np.asarray(g_.filter(ImageFilter.GaussianBlur(rad)), np.float32)
        out = out + ga[..., :3] * (ga[..., 3:] / 255) * k_
    l = np.asarray(lay, np.float32); la = l[..., 3:] / 255
    out = out * (1 - la) + l[..., :3] * la
    im = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert('RGBA')
    # text
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(tx)
    for (a0, a1, lab, head) in ACTS:
        al = fade(t, a0 + (0.5 if a0 == 0 else 0.15), a1, 0.6, 0.5)
        if al > 0:
            off = (1 - ease((t - a0 - 0.15) / 0.8)) * 14
            tracked(td, (80, 282 + off), lab, LAB, rgba(MUT, al), 0.32)
            for j, ln in enumerate(wrap(td, head, HEAD, 900)):
                tracked(td, (80, 330 + off + j * 76), ln, HEAD, rgba(OFF, al), -0.01)
    # step captions + progress line (act 3)
    for n_, ((ttl, desc), ts) in enumerate(zip(STEPS, STEP_T)):
        al = fade(t, ts + 0.1, 15.9, 0.5, 0.5)
        if al > 0:
            p = T(NODES[n_], cam); right = NODES[n_][0] > 540
            if right: x = p[0] + 46; anchor = 'l'
            else: x = p[0] - 46; anchor = 'r'
            tracked(td, (x, p[1] - 30), ttl, CAP, rgba(OFF, al), 0.18, anchor)
            for j, ln in enumerate(wrap(td, desc, CAPS, 300)):
                lw_ = td.textlength(ln, font=CAPS)
                td.text((x if right else x - lw_, p[1] + 8 + j * 29), ln, font=CAPS, fill=rgba(MUT, al))
    pa = fade(t, 10.6, 15.9, 0.6, 0.6)
    if pa > 0:
        y0, y1, xl = 640, 1470, 40
        prog = sum(seg(t, ts, ts + 0.8) for ts in STEP_T) / 4
        for q in range(40):
            u0, u1 = q / 40, (q + 1) / 40; a = math.sin(math.pi * (u0 + u1) / 2) ** 0.7
            on = (u0 + u1) / 2 <= prog
            td.line([(xl, lerp(y0, y1, u0)), (xl, lerp(y0, y1, u1))], fill=rgba(VIO if on else LIN, pa * a * (1 if on else 0.9)), width=3 if on else 2)
        for n_ in range(4):
            yy_ = lerp(y0, y1, (n_ + 1) / 4 - 0.125); done = seg(t, STEP_T[n_], STEP_T[n_] + 0.5)
            td.ellipse([xl - 6, yy_ - 6, xl + 6, yy_ + 6], outline=rgba(VIO if done > 0.5 else LIN, pa), width=2)
    ca = seg(t, WM1 + 0.3, WM1 + 0.8) * (1 - seg(t, 23.35, 23.95))
    if ca > 0:
        tracked(td, (540, wm((0, 86))[1] + 110), 'PROCESS AUTOMATION — MARRAKECH', LAB, rgba(MUT, ca), 0.32, 'm')
    im.alpha_composite(tx)
    return im.convert('RGB')

if __name__ == '__main__':
    if '--still' in sys.argv:
        for ts in sys.argv[sys.argv.index('--still') + 1:]:
            frame(int(round(float(ts) * FPS))).save(f'/home/claude/reel/s3_{ts}.png')
        sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        p.stdin.write(frame(i).tobytes())
        if i % 120 == 0: print(i, '/', n, flush=True)
    p.stdin.close(); p.wait(); print('done', OUT)
