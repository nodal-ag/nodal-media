"""Décodé #01 — Le faux SMS « colis en attente ». Style of 'the engine' reel. Voice-timed."""
import sys, json, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, SS = 1080, 1920, 30, 2
TIM = json.load(open('/home/claude/decode01/timing.json'))
SUBS = TIM['subs']; VEND = TIM['voice_end']
DUR = round(VEND + 2.9, 2)
INK = (13, 11, 31); VIO = (139, 124, 255); DEEP = (91, 72, 224); OFF = (245, 246, 248); MUT = (169, 166, 191); LIN = (66, 61, 99)
SURF = (26, 22, 54)
TAU = 2 * math.pi
CAR = '/home/claude/fonts/Quicksand-500.ttf'
CARB = '/home/claude/fonts/Quicksand-700.ttf'
CP = '/home/claude/fonts/Quicksand-600.ttf'
QL = '/home/claude/fonts/Quicksand-400.ttf'
HEAD = ImageFont.truetype(CAR, 66)
LAB = ImageFont.truetype(CP, 30)
CAP = ImageFont.truetype(CP, 28)
CAPS = ImageFont.truetype(QL, 24)
CAPS2 = ImageFont.truetype(CP, 28)
SUBF = ImageFont.truetype(CARB, 44)

def ease(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def seg(t, a, b): return ease((t - a) / (b - a))
def fade(t, a, b, fi=0.6, fo=0.6):
    if t < a or t > b: return 0.0
    return min(ease((t - a) / fi), ease((b - t) / fo))
def lerp(a, b, u): return a + (b - a) * u
def rgba(c, a): return (int(c[0]), int(c[1]), int(c[2]), int(255 * max(0.0, min(1.0, a))))
def mixc(c1, c2, u): return tuple(lerp(a, b, u) for a, b in zip(c1, c2))
def shade(c, k): return tuple(v * k for v in c)

# chapter boundaries from the voice
def ch_start(c): return min(s['start'] for s in SUBS if s['ch'] == c)
CS = [0.0] + [ch_start(c) - 0.25 for c in range(1, 5)] + [VEND]
ACTS = [(CS[0], CS[1], ('', 'Décodé #01'), 'Ce SMS connaît votre nom.'),
        (CS[1], CS[2], ('01', 'Fuite'), 'Vos données circulent déjà.'),
        (CS[2], CS[3], ('02', 'Envoi'), 'Un message, des milliers de téléphones.'),
        (CS[3], CS[4], ('03', 'Piège'), 'Une fausse page de suivi.'),
        (CS[4], CS[5], ('04', 'Réflexe'), 'Jamais de paiement par lien.')]
def sub_t(txt_start):
    for s in SUBS:
        if s['text'].startswith(txt_start): return s['start']
    raise KeyError(txt_start)

# ---------------- camera ----------------
C0 = (540.0, 1000.0)
def camera(t):
    s = 1.0 + 0.012 * math.sin(TAU * t / 30)
    s *= 1 - 0.16 * seg(t, CS[2] + 0.2, CS[2] + 1.6) + 0.16 * seg(t, CS[3] - 0.4, CS[3] + 0.8)
    s *= 1 - 0.12 * seg(t, VEND - 0.2, VEND + 0.6)
    ox = 7 * math.sin(TAU * t / 30); oy = 5 * math.sin(2 * TAU * t / 30)
    return s, ox, oy
def T(p, cam):
    s, ox, oy = cam
    return (C0[0] + (p[0] - C0[0]) * s + ox, C0[1] + (p[1] - C0[1]) * s + oy)

# ---------------- background ----------------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.sqrt(((xx - 540) / 700) ** 2 + ((yy - 980) / 1050) ** 2)
VIGN = np.clip(1.08 - 0.55 * r ** 1.6, 0.35, 1.0)[..., None]
BG = (np.zeros((H, W, 3), np.float32) + np.array(INK, np.float32)) * VIGN
halo = np.exp(-(((xx - 540) / 420) ** 2 + ((yy - 1000) / 560) ** 2))[..., None]
BG = BG + halo * (np.array(SURF, np.float32) - np.array(INK, np.float32)) * 0.9
rng = np.random.default_rng(5)
DUST = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.6, 1.6), rng.uniform(0.08, 0.3), rng.uniform(0, TAU), rng.integers(1, 3)) for _ in range(140)]

# ---------------- the phone (sprite) ----------------
FX0, FX1, FY0, FY1 = 398.0, 682.0, 712.0, 1290.0
DX, DY = 34.0, -18.0
SX0, SX1, SY0, SY1 = FX0 + 16, FX1 - 16, FY0 + 30, FY1 - 30   # screen
SPR_K = 2.6
SPR_OX, SPR_OY = FX0 - 10, FY0 + DY - 10
SPR_W, SPR_H = (FX1 + DX + 10) - SPR_OX, (FY1 + 10) - SPR_OY
def build_phone():
    k = SPR_K; w, h = int(SPR_W * k), int(SPR_H * k)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda x, y: ((x - SPR_OX) * k, (y - SPR_OY) * k)
    R = 34
    # depth (side + top) as an offset rounded slab
    for i in range(14, -1, -1):
        u = i / 14; ox, oy = DX * u, DY * u
        d.rounded_rectangle([P(FX0 + ox, FY0 + oy), P(FX1 + ox, FY1 + oy)], radius=R * k, fill=rgba(mixc(shade(INK, 0.5), LIN, 0.35 * (1 - u) + 0.1), 1))
    # front face gradient
    fw, fh = int((FX1 - FX0) * k), int((FY1 - FY0) * k)
    gy = np.linspace(0, 1, fh)[:, None]; gx = np.linspace(0, 1, fw)[None, :]
    base = 0.95 - 0.30 * gy + 0.12 * np.exp(-((gx - 0.15) / 0.10) ** 2) * (1 - gy * 0.7)
    face = np.zeros((fh, fw, 4), np.float32); face[..., :3] = np.array(INK, np.float32) * base[..., None] + 6
    mask = Image.new('L', (fw, fh), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, fw - 1, fh - 1], radius=R * k, fill=255)
    face[..., 3] = np.asarray(mask, np.float32)
    im.alpha_composite(Image.fromarray(np.clip(face, 0, 255).astype(np.uint8)), (int((FX0 - SPR_OX) * k), int((FY0 - SPR_OY) * k)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([P(FX0, FY0), P(FX1, FY1)], radius=R * k, outline=rgba(mixc(LIN, MUT, 0.4), 0.9), width=int(2 * k))
    # screen glass
    d.rounded_rectangle([P(SX0, SY0), P(SX1, SY1)], radius=18 * k, fill=rgba(shade(INK, 0.55), 1), outline=rgba(LIN, 0.8), width=int(1.4 * k))
    # notch pill
    d.rounded_rectangle([P(540 - 36, FY0 + 12), P(540 + 36, FY0 + 22)], radius=5 * k, fill=rgba(shade(INK, 0.4), 1))
    return im
PHONE = build_phone()

def mini_phone(k=SS):
    w, h = 54, 100
    im = Image.new('RGBA', (w * k, h * k), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w * k - 1, h * k - 1], radius=9 * k, fill=rgba(mixc(INK, LIN, 0.25), 1), outline=rgba(LIN, 1), width=k)
    d.rounded_rectangle([5 * k, 8 * k, (w - 5) * k, (h - 8) * k], radius=5 * k, fill=rgba(shade(INK, 0.6), 1))
    return im
MINI = mini_phone()

# ---------------- curves ----------------
def catmull(pts, n=24):
    out = []; P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(n):
            u = j / n; u2, u3 = u * u, u * u * u
            out.append(tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * u + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * u2 +
                                  (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * u3) for k in (0, 1)))
    out.append(pts[-1]); return out
class Curve:
    def __init__(self, ctrl):
        self.pts = catmull(ctrl)
        L = np.concatenate([[0], np.cumsum([math.dist(a, b) for a, b in zip(self.pts, self.pts[1:])])]); self.L = L / L[-1]
    def at(self, s):
        s = min(max(s, 0), 1); i = int(np.searchsorted(self.L, s)); i = min(max(i, 1), len(self.pts) - 1)
        u = (s - self.L[i - 1]) / max(self.L[i] - self.L[i - 1], 1e-9)
        return (lerp(self.pts[i - 1][0], self.pts[i][0], u), lerp(self.pts[i - 1][1], self.pts[i][1], u))
    def part(self, a, b):
        return [self.at(a + (b - a) * j / 60) for j in range(61)]

# sources of leaked data (chapter 1)
SRC = [((175, 640), '01|Sites piratés', 'base de données volée', 'db', sub_t('sites')),
       ((905, 700), '02|Formulaires', 'jeux, livraisons, inscriptions', 'doc', sub_t('sites') + 0.85),
       ((900, 1180), '03|Listes revendues', 'copiées et revendues', 'list', sub_t('sites') + 1.7)]
SRC_CURVES = [Curve([(200, 700), (240, 790), (330, 760), (FX0 - 4, 800)]),
              Curve([(860, 740), (800, 800), (740, 790), (FX1 + 4, 860)]),
              Curve([(900, 1120), (850, 1030), (760, 1060), (FX1 + 4, 1020)])]
CARDS = ['NOM', 'NUMÉRO', 'E-MAIL']
# robot + crowd (chapter 2)
ROBOT = (540, 560)
CROWD = []
for row, (y, n, x0, x1) in enumerate([(700, 4, 120, 960), (900, 4, 110, 970), (1110, 4, 110, 970), (1320, 5, 130, 950)]):
    for j in range(n):
        x = lerp(x0, x1, j / (n - 1))
        if 330 < x < 750 and y < 1300: x = 150 + (j % 2) * 30 if x < 540 else 930 - (j % 2) * 30
        CROWD.append((x, y))
CROWD = sorted(set((round(a), round(b)) for a, b in CROWD), key=lambda p: (math.dist(p, ROBOT)))
# pirate (chapter 3)
PIR = (905, 1150)
PIR_CURVE = Curve([(FX1 + 4, 1080), (780, 1080), (830, 1160), (PIR[0] - 26, PIR[1])])
# reflex nodes (chapter 4)
RFX = [((FX0, 860), '01|Aucun lien', 'jamais de paiement depuis un SMS', sub_t('Le réflexe')),
       ((FX1, 1010), '02|L\'appli', 'officielle, ouverte par vous', sub_t('Ouvrez')),
       ((FX0, 1160), '03|Partagez', 'à quelqu\'un qui attend un colis', sub_t('Partagez'))]

# ---------------- wordmark ----------------
def quad(p0, c, p1, n=14): return [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * c[0] + u * u * p1[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * c[1] + u * u * p1[1]) for u in np.linspace(0, 1, n)]
def circ(cx, cy, r_, n=64): return [(cx + r_ * math.cos(-math.pi / 2 - a), cy + r_ * math.sin(-math.pi / 2 - a)) for a in np.linspace(0, TAU, n)]
N_PATH = [(24, 78), (24, 31)] + quad((24, 31), (24, 20), (32, 28))[1:] + [(68, 72)] + quad((68, 72), (76, 80), (76, 69))[1:] + [(76, 22)]
STROKES = [N_PATH, circ(108, 58, 20), circ(158, 58, 20), [(178, 22), (178, 78)], circ(210, 58, 20),
           [(230, 40), (230, 70)] + quad((230, 70), (230, 78), (238, 78))[1:], [(250, 22), (250, 70)] + quad((250, 70), (250, 78), (258, 78))[1:]]
STROKES = [[(x + 2, y) for x, y in s] for s in STROKES]
WK = 3.0; WCX, WCY = 540, 900
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
WM0, WM1 = VEND + 0.35, VEND + 1.45

# ---------------- helpers ----------------
def faded_line(dr, p0, p1, c, a, w, n=24, k=SS):
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n; al = a * math.sin(math.pi * (u0 + u1) / 2) ** 0.8
        dr.line([(lerp(p0[0], p1[0], u0) * k, lerp(p0[1], p1[1], u0) * k), (lerp(p0[0], p1[0], u1) * k, lerp(p0[1], p1[1], u1) * k)], fill=rgba(c, al), width=max(1, int(w * k)))
def dot(dr, p, r_, c, a, k=SS): dr.ellipse([(p[0] - r_) * k, (p[1] - r_) * k, (p[0] + r_) * k, (p[1] + r_) * k], fill=rgba(c, a))
def ring(dr, p, r_, c, a, w, k=SS): dr.ellipse([(p[0] - r_) * k, (p[1] - r_) * k, (p[0] + r_) * k, (p[1] + r_) * k], outline=rgba(c, a), width=max(1, int(w * k)))
def tracked(dr, xy, s, font, fill, track=0.3, anchor='l'):
    ws = [dr.textlength(ch, font=font) + font.size * track for ch in s]; tot = sum(ws) - font.size * track
    x, y = xy
    if anchor == 'm': x -= tot / 2
    if anchor == 'r': x -= tot
    for ch, w_ in zip(s, ws): dr.text((x, y), ch, font=font, fill=fill); x += w_
def nlabel(dr, xy, num, word, font, al, anchor='l', node=False):
    """Nodal label: number in violet, word in clear; optional ring + stem like the logo's N terminal."""
    x, y = xy
    gap = font.size * 0.45
    wn = dr.textlength(num, font=font) if num else 0
    ww = dr.textlength(word, font=font)
    tot = wn + (gap if num else 0) + ww + (60 if node else 0)
    if anchor == 'r': x -= tot
    if anchor == 'm': x -= tot / 2
    if node:
        cy = y + font.size * 0.62; r_ = font.size * 0.32
        dr.ellipse([x, cy - r_, x + 2 * r_, cy + r_], outline=rgba(VIO, al), width=3)
        dr.line([x + 2 * r_, cy, x + 2 * r_ + 26, cy], fill=rgba(VIO, al), width=3)
        x += 60
    if num:
        dr.text((x, y), num, font=font, fill=rgba(VIO, al)); x += wn + gap
    dr.text((x, y), word, font=font, fill=rgba(OFF, al))
def wrap(dr, s, font, maxw):
    lines, cur = [], ''
    for w_ in s.split(' '):
        nx = (cur + ' ' + w_).strip()
        if dr.textlength(nx, font=font) > maxw and cur: lines.append(cur); cur = w_
        else: cur = nx
    return lines + [cur]
def path_line(dr, gd, wd, pts, a, s, width=2.2):
    if a <= 0 or len(pts) < 2: return
    dr.line([(x * SS, y * SS) for x, y in pts], fill=rgba(VIO, 0.85 * a), width=int(width * s * SS), joint='curve')
    gd.line(pts, fill=rgba(VIO, 0.7 * a), width=int(6 * s)); wd.line(pts, fill=rgba(VIO, 0.3 * a), width=int(14 * s))
def particles(dr, gd, curve, cam, t, a, n=14, speed=1.6, col=(225, 220, 255)):
    for k_ in range(n):
        sp = ((k_ / n) + t / speed) % 1.0
        p = T(curve.at(sp), cam); aa = math.sin(math.pi * sp) ** 0.5 * a
        dot(dr, p, 2.4 * cam[0], col, aa); gd.ellipse([p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7], fill=rgba(VIO, 0.55 * aa))
def paste(lay, spr, center, scale, alpha, ang=0):
    im = spr.resize((max(2, int(spr.width * scale)), max(2, int(spr.height * scale))), Image.BILINEAR)
    if ang: im = im.rotate(ang, resample=Image.BICUBIC, expand=True)
    if alpha < 0.999:
        a_ = np.asarray(im, np.float32).copy(); a_[..., 3] *= max(alpha, 0); im = Image.fromarray(a_.astype(np.uint8))
    lay.alpha_composite(im, (int(center[0] * SS - im.width / 2), int(center[1] * SS - im.height / 2)))

def card_sprite(label, k=SS):
    w, h = 128, 64
    im = Image.new('RGBA', (w * k + 30, h * k + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([15 + 5, 15 + 7, 15 + w * k + 5, 15 + h * k + 7], fill=(0, 0, 0, 80)); im = im.filter(ImageFilter.GaussianBlur(6)); d = ImageDraw.Draw(im)
    d.rectangle([15, 15, 15 + w * k, 15 + h * k], fill=rgba(OFF, 0.95))
    f = ImageFont.truetype(CP, 15 * k); d.text((15 + 12 * k, 15 + 10 * k), label, font=f, fill=rgba(INK, 0.9))
    d.line([15 + 12 * k, 15 + 36 * k, 15 + (w - 18) * k, 15 + 36 * k], fill=rgba(MUT, 0.9), width=int(2.4 * k))
    d.line([15 + 12 * k, 15 + 48 * k, 15 + (w - 50) * k, 15 + 48 * k], fill=rgba(MUT, 0.7), width=int(2.4 * k))
    return im
CARD_SPR = [card_sprite(c) for c in CARDS]
def db_sprite(k=SS):
    w, h = 110, 120; im = Image.new('RGBA', (w * k, h * k), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i in range(3):
        y = (16 + i * 34) * k
        d.rectangle([4 * k, y, (w - 4) * k, y + 34 * k], fill=rgba(mixc(INK, LIN, 0.35), 1))
        d.ellipse([4 * k, y + 22 * k, (w - 4) * k, y + 46 * k], fill=rgba(mixc(INK, LIN, 0.35), 1), outline=rgba(MUT, 0.7), width=k)
        d.ellipse([4 * k, y - 12 * k, (w - 4) * k, y + 12 * k], fill=rgba(mixc(INK, LIN, 0.55), 1), outline=rgba(MUT, 0.8), width=k)
    d.line([(46 * k, 20 * k), (58 * k, 50 * k), (50 * k, 72 * k), (64 * k, 104 * k)], fill=rgba(VIO, 1), width=int(2 * k))
    return im
def doc_sprite(k=SS, lines=7, title='FORMULAIRE'):
    w, h = 96, 124; im = Image.new('RGBA', (w * k, h * k), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w * k - 1, h * k - 1], fill=rgba(OFF, 0.93))
    d.text((10 * k, 9 * k), title, font=ImageFont.truetype(CP, 9 * k), fill=rgba(INK, 0.85))
    rr = np.random.default_rng(len(title))
    for i in range(lines):
        y = (30 + i * 13) * k; d.line([10 * k, y, 10 * k + rr.uniform(0.4, 0.9) * (w - 20) * k, y], fill=rgba(MUT, 0.8), width=int(2.2 * k))
    return im
SRC_SPR = [db_sprite(), doc_sprite(), doc_sprite(title='LISTE')]

# ---------------- phone screen content ----------------
def screen(t, s, cam):
    """returns RGBA image of the screen content at SS resolution in world units, and its top-left world point"""
    k = SS; w, h = int((SX1 - SX0) * k), int((SY1 - SY0) * k)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fS = ImageFont.truetype(CP, 14 * k); fB = ImageFont.truetype(CAR, 21 * k); fBb = ImageFont.truetype(CARB, 21 * k)
    fT = ImageFont.truetype(CARB, 26 * k)
    page = seg(t, CS[3] - 0.1, CS[3] + 0.5) * (1 - seg(t, CS[4] + 0.2, CS[4] + 0.8))
    sms = (1 - page)
    # status line
    d.text((16 * k, 14 * k), '09:41', font=fS, fill=rgba(MUT, 0.9))
    if sms > 0.01:
        ab = seg(t, 0.4, 1.0) * sms
        d.text((16 * k, 44 * k), 'Colis-Maroc', font=fS, fill=rgba(MUT, ab))
        bx0, by0, bx1 = 12 * k, 70 * k, w - 14 * k
        lines = [('Bonjour ', 'Youssef', ','), ('Votre colis est en', None, ''), ('attente. Frais de', None, ''), ('livraison à régler :', None, '')]
        by1 = by0 + (len(lines) * 28 + 56) * k
        d.rounded_rectangle([bx0, by0, bx1, by1], radius=14 * k, fill=rgba(mixc(INK, LIN, 0.55), ab))
        hl = fade(t, 0.5, CS[1] + 0.4, 0.4, 0.5) + 0.8 * sum(fade(t, src[4] + 0.9, src[4] + 1.9, 0.2, 0.4) for src in SRC)
        hl = min(hl, 1)
        for i, (a_, nm, b_) in enumerate(lines):
            y = by0 + (14 + i * 28) * k; x = bx0 + 14 * k
            d.text((x, y), a_, font=fB, fill=rgba(OFF, ab)); x += d.textlength(a_, font=fB)
            if nm:
                nw = d.textlength(nm, font=fBb)
                if hl > 0: d.rounded_rectangle([x - 3 * k, y - 1 * k, x + nw + 3 * k, y + 25 * k], radius=5 * k, fill=rgba(VIO, 0.45 * hl * ab))
                d.text((x, y), nm, font=fBb, fill=rgba(mixc(OFF, (220, 214, 255), hl), ab)); x += nw
                d.text((x, y), b_, font=fB, fill=rgba(OFF, ab))
        # link
        ly = by0 + (14 + len(lines) * 28) * k
        lk = 'suivi-colis.top/pay'
        glow_l = fade(t, sub_t('avec un lien'), CS[3] + 0.2, 0.3, 0.5)
        cut = seg(t, sub_t('Le réflexe') + 0.4, sub_t('Le réflexe') + 1.0)
        lc = mixc((170, 160, 255), (230, 226, 255), glow_l)
        d.text((bx0 + 14 * k, ly), lk, font=fB, fill=rgba(lc, ab))
        lw_ = d.textlength(lk, font=fB)
        d.line([bx0 + 14 * k, ly + 25 * k, bx0 + 14 * k + lw_, ly + 25 * k], fill=rgba(lc, ab * (0.6 + 0.4 * glow_l)), width=int(1.5 * k))
        if cut > 0:
            d.line([bx0 + 10 * k, ly + 13 * k, bx0 + 10 * k + (lw_ + 8 * k) * cut, ly + 13 * k], fill=rgba(OFF, ab), width=int(3 * k))
        # reflex check card
        rc = seg(t, sub_t('Ouvrez') + 0.2, sub_t('Ouvrez') + 0.8) * sms
        if rc > 0:
            cy0 = by1 + 40 * k
            d.rounded_rectangle([bx0, cy0, bx1, cy0 + 120 * k], radius=14 * k, outline=rgba(VIO, rc), width=int(2 * k), fill=rgba(shade(INK, 0.7), rc))
            d.text((bx0 + 16 * k, cy0 + 16 * k), 'Application officielle', font=fS, fill=rgba(MUT, rc))
            d.text((bx0 + 16 * k, cy0 + 42 * k), 'Suivi du colis', font=fBb, fill=rgba(OFF, rc))
            d.text((bx0 + 16 * k, cy0 + 72 * k), 'Rien à payer', font=fB, fill=rgba((205, 198, 255), rc))
    if page > 0.01:
        a = page
        d.text((16 * k, 44 * k), 'Suivi de colis', font=fS, fill=rgba(MUT, a))
        d.text((16 * k, 66 * k), 'En attente de', font=fT, fill=rgba(OFF, a))
        d.text((16 * k, 98 * k), 'paiement', font=fT, fill=rgba(OFF, a))
        # progress bar
        d.rounded_rectangle([16 * k, 144 * k, w - 16 * k, 150 * k], radius=3 * k, fill=rgba(LIN, a))
        d.rounded_rectangle([16 * k, 144 * k, 16 * k + (w - 32 * k) * 0.72, 150 * k], radius=3 * k, fill=rgba(VIO, a))
        fields = [('N° de carte', '•••• •••• •••• ', 16), ('Expiration', '•• / ••', 7), ('CVV', '•••', 3)]
        t0 = CS[3] + 0.7
        for i, (lab, val, n) in enumerate(fields):
            y = (180 + i * 86) * k
            d.text((16 * k, y), lab, font=fS, fill=rgba(MUT, a))
            lit = seg(t, t0 + i * 0.7, t0 + i * 0.7 + 0.3)
            d.rounded_rectangle([16 * k, y + 22 * k, w - 16 * k, y + 64 * k], radius=8 * k, fill=rgba(shade(INK, 0.8), a), outline=rgba(mixc(LIN, VIO, lit), a), width=int((1 + lit) * k))
            fill_u = seg(t, t0 + i * 0.7 + 0.1, t0 + i * 0.7 + 0.65)
            shown = val[:int(len(val) * fill_u)]
            d.text((28 * k, y + 32 * k), shown, font=fB, fill=rgba(OFF, a))
        by = (180 + 3 * 86 + 6) * k
        press = fade(t, sub_t('et vous donnez'), CS[4], 0.2, 0.4)
        d.rounded_rectangle([16 * k, by, w - 16 * k, by + 52 * k], radius=26 * k, fill=rgba(mixc(DEEP, VIO, press), a))
        tw = d.textlength('PAYER', font=fBb); d.text(((w - tw) / 2, by + 13 * k), 'PAYER', font=fBb, fill=rgba(OFF, a))
    return im

# ---------------- frame ----------------
def frame(i):
    t = i / FPS; cam = camera(t); s = cam[0]
    lay = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0)); dr = ImageDraw.Draw(lay)
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    wide = Image.new('RGBA', (W, H), (0, 0, 0, 0)); wd = ImageDraw.Draw(wide)
    for (x, y, rr_, a, ph, m) in DUST:
        px = x + 18 * math.sin(TAU * t / 30 * m + ph); py = y + 26 * math.sin(TAU * t / 30 + ph * 1.3)
        dot(dr, (px, py), rr_, MUT, a)
    ph_a = seg(t, 0.0, 0.6) * (1 - seg(t, VEND - 0.1, VEND + 0.5))
    # floor ring
    fc = T((556, 1318), cam); rx, ry = 250 * s, 40 * s
    wd.ellipse([fc[0] - rx, fc[1] - ry, fc[0] + rx, fc[1] + ry], outline=rgba(VIO, 0.5 * ph_a), width=6)
    dr.ellipse([(fc[0] - rx) * SS, (fc[1] - ry) * SS, (fc[0] + rx) * SS, (fc[1] + ry) * SS], outline=rgba(VIO, 0.42 * ph_a), width=2 * SS)

    # ---- chapter 1: sources -> phone
    a1 = fade(t, CS[1] - 0.1, CS[2] + 0.4, 0.6, 0.7)
    if a1 > 0:
        for n_, ((pos, lab, desc, kind, ts), cv) in enumerate(zip(SRC, SRC_CURVES)):
            ap = seg(t, CS[1] + n_ * 0.25, CS[1] + 0.7 + n_ * 0.25) * a1
            p = T(pos, cam)
            fl = 3 * math.sin(TAU * t / 6 + n_)
            paste(lay, SRC_SPR[n_], (p[0], p[1] + fl), s * 0.95, ap, [0, 8, -6][n_])
            grow = seg(t, ts - 0.3, ts + 0.5)
            pts = [T(q, cam) for q in cv.part(0, grow)]
            path_line(dr, gd, wd, pts, ap, s)
            if grow >= 1: particles(dr, gd, cv, cam, t, ap * 0.9, 8, 1.4)
            # card travelling
            u = seg(t, ts + 0.2, ts + 1.1)
            if 0 < u < 1:
                cp = T(cv.at(u), cam); paste(lay, CARD_SPR[n_], cp, s * lerp(0.8, 0.25, u), ap * (1 - seg(u, 0.85, 1)))
            # port flash on the phone edge
            bt = t - (ts + 1.1)
            if 0 < bt < 0.7:
                pin = T(cv.at(1), cam)
                for q in range(10):
                    ang = q / 10 * TAU; rr_ = 6 + 46 * ease(bt / 0.7)
                    pp = (pin[0] + rr_ * math.cos(ang), pin[1] + rr_ * math.sin(ang) * 0.8)
                    dot(dr, pp, 2.0, (220, 214, 255), (1 - bt / 0.7) * ap)
    # ---- chapter 2: robot -> crowd
    a2 = fade(t, CS[2], CS[3] + 0.2, 0.6, 0.6)
    if a2 > 0:
        rp = T(ROBOT, cam)
        ring(dr, rp, 22 * s, VIO, a2, 2); dot(dr, rp, 7 * s, OFF, a2)
        wd.ellipse([rp[0] - 40, rp[1] - 40, rp[0] + 40, rp[1] + 40], fill=rgba(VIO, 0.5 * a2))
        t_send = sub_t('Un robot') + 0.6
        for n_, q in enumerate(CROWD):
            tq = t_send + n_ * 0.12
            u = seg(t, tq, tq + 0.45)
            if u <= 0: continue
            qp = T(q, cam)
            end = (lerp(rp[0], qp[0], u), lerp(rp[1], qp[1], u))
            la = a2 * (0.75 - 0.4 * seg(t, tq + 0.6, tq + 1.4))
            faded_line(dr, rp, end, VIO, la, 1.1, 12)
            if u >= 1:
                paste(lay, MINI, qp, s * 0.95, a2 * seg(t, tq + 0.4, tq + 0.7))
                dot(dr, (qp[0], qp[1] - 14 * s), 5 * s, VIO, a2 * seg(t, tq + 0.5, tq + 0.8))
                gd.ellipse([qp[0] - 14, qp[1] - 28, qp[0] + 14, qp[1]], fill=rgba(VIO, 0.5 * a2 * seg(t, tq + 0.5, tq + 0.8)))
        # line to the central phone
        u = seg(t, t_send - 0.4, t_send + 0.1); top = T((540, FY0 - 6), cam)
        if u > 0: faded_line(dr, rp, (lerp(rp[0], top[0], u), lerp(rp[1], top[1], u)), VIO, a2, 1.6, 12)
    # ---- phone
    tl = T((SPR_OX, SPR_OY), cam)
    spr = PHONE.resize((int(SPR_W * s * SS), int(SPR_H * s * SS)), Image.BILINEAR)
    if ph_a < 0.999:
        a_ = np.asarray(spr, np.float32).copy(); a_[..., 3] *= ph_a; spr = Image.fromarray(a_.astype(np.uint8))
    lay.alpha_composite(spr, (int(tl[0] * SS), int(tl[1] * SS)))
    sc = screen(t, s, cam)
    sc = sc.resize((max(2, int(sc.width * s)), max(2, int(sc.height * s))), Image.BILINEAR)
    if ph_a < 0.999:
        a_ = np.asarray(sc, np.float32).copy(); a_[..., 3] *= ph_a; sc = Image.fromarray(a_.astype(np.uint8))
    stl = T((SX0, SY0), cam); lay.alpha_composite(sc, (int(stl[0] * SS), int(stl[1] * SS)))
    # sheen
    u = 0.5 + 0.5 * math.sin(TAU * t / 30 - 1.2); sx = lerp(FX0 - 80, FX1 + 40, u)
    sheen = Image.new('RGBA', lay.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sheen)
    poly = [T((sx, FY0), cam), T((sx + 70, FY0), cam), T((sx + 10, FY1), cam), T((sx - 60, FY1), cam)]
    sd.polygon([(x * SS, y * SS) for x, y in poly], fill=rgba(OFF, 0.05 * ph_a))
    m = Image.new('L', lay.size, 0); ImageDraw.Draw(m).rounded_rectangle([T((FX0, FY0), cam)[0] * SS, T((FX0, FY0), cam)[1] * SS, T((FX1, FY1), cam)[0] * SS, T((FX1, FY1), cam)[1] * SS], radius=int(34 * s * SS), fill=255)
    lay.paste(sheen, (0, 0), Image.fromarray(np.minimum(np.asarray(m), np.asarray(sheen.split()[-1])).astype(np.uint8)))
    # ---- chapter 3: phone -> pirate
    a3 = fade(t, CS[3], CS[4] + 1.4, 0.5, 0.6)
    if a3 > 0:
        pp = T(PIR, cam)
        pa = seg(t, sub_t('et vous donnez') - 0.3, sub_t('et vous donnez') + 0.3) * a3
        cut = seg(t, sub_t('Le réflexe') + 0.2, sub_t('Le réflexe') + 0.8)
        grow = seg(t, sub_t('et vous donnez') - 0.1, sub_t('et vous donnez') + 0.6)
        if cut <= 0:
            path_line(dr, gd, wd, [T(q, cam) for q in PIR_CURVE.part(0, grow)], pa, s)
            if grow >= 1: particles(dr, gd, PIR_CURVE, cam, t, pa, 12, 1.0)
        else:
            gap = 0.08 * cut
            path_line(dr, gd, wd, [T(q, cam) for q in PIR_CURVE.part(0, 0.5 - gap)], pa * (1 - 0.6 * cut), s)
            path_line(dr, gd, wd, [T(q, cam) for q in PIR_CURVE.part(0.5 + gap, 1)], pa * (1 - cut), s)
            mid = T(PIR_CURVE.at(0.5), cam)
            for dx_ in (-9, 9):
                dr.line([((mid[0] + dx_ - 7) * SS, (mid[1] + 14) * SS), ((mid[0] + dx_ + 7) * SS, (mid[1] - 14) * SS)], fill=rgba(OFF, cut * a3), width=3 * SS)
        # pirate node: dark core, deep violet ring
        pna = pa * (1 - 0.8 * cut)
        if pna > 0:
            dr.ellipse([(pp[0] - 30 * s) * SS, (pp[1] - 30 * s) * SS, (pp[0] + 30 * s) * SS, (pp[1] + 30 * s) * SS], fill=rgba(shade(INK, 0.4), pna), outline=rgba(DEEP, pna), width=3 * SS)
            ring(dr, pp, 44 * s + 3 * math.sin(t * 5), DEEP, 0.5 * pna, 1.4)
            wd.ellipse([pp[0] - 60, pp[1] - 60, pp[0] + 60, pp[1] + 60], fill=rgba(DEEP, 0.55 * pna))
    # ---- chapter 4: reflex nodes on the phone edges
    for n_, (pos, lab, desc, ts) in enumerate(RFX):
        al = fade(t, ts, VEND - 0.05, 0.4, 0.5) * ph_a
        if al <= 0: continue
        p = T(pos, cam)
        dot(dr, p, 7 * s, OFF, al); ring(dr, p, 15 * s, VIO, al, 1.8)
        gd.ellipse([p[0] - 20 * s, p[1] - 20 * s, p[0] + 20 * s, p[1] + 20 * s], fill=rgba(VIO, al))
        pr = (t - ts) / 0.9
        if 0 < pr < 1: ring(dr, p, (18 + 40 * pr) * s, VIO, 0.6 * (1 - pr), 1.4)
    # ---- wordmark close
    if t > WM0 - 0.05:
        drawn = (t - WM0) / (WM1 - WM0) * TOT; acc = 0
        na = seg(t, WM0, WM0 + 0.25); nc = wm((26, 78))
        for st_, L in zip(STROKES, SLEN):
            frac = min(max((drawn - acc) / L, 0), 1); acc += L
            pp = [wm(p) for p in partial(st_, frac)]
            if len(pp) > 1:
                dr.line([(x * SS, y * SS) for x, y in pp], fill=rgba(OFF, 1), width=int(3.2 * WK * SS), joint='curve')
                for e in (pp[0], pp[-1]): dot(dr, e, 1.6 * WK, OFF, 1)
        if na > 0:
            dot(dr, nc, 6.5 * WK + 1.36 * WK, OFF, na); dot(dr, nc, 6.5 * WK - 1.36 * WK, INK, na)
        da = seg(t, WM1 + 0.05, WM1 + 0.4)
        if da > 0:
            dc = wm((78, 22 - 10 * (1 - da)))
            dot(dr, dc, 8 * WK * (0.6 + 0.4 * da), VIO, da)
            wd.ellipse([dc[0] - 70, dc[1] - 70, dc[0] + 70, dc[1] + 70], fill=rgba(VIO, 0.8 * da))
            gd.ellipse([dc[0] - 34, dc[1] - 34, dc[0] + 34, dc[1] + 34], fill=rgba(VIO, 0.7 * da))
    # ---- composite
    lay = lay.resize((W, H), Image.LANCZOS)
    out = BG.copy()
    for g_, rad, k_ in [(wide, 38, 0.9), (glow, 10, 1.0)]:
        ga = np.asarray(g_.filter(ImageFilter.GaussianBlur(rad)), np.float32)
        out = out + ga[..., :3] * (ga[..., 3:] / 255) * k_
    l = np.asarray(lay, np.float32); la = l[..., 3:] / 255
    out = out * (1 - la) + l[..., :3] * la
    im = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert('RGBA')
    # ---- text
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(tx)
    for (a0, a1_, lab, head) in ACTS:
        al = fade(t, a0 + (0.3 if a0 == 0 else 0.1), a1_ + 0.1, 0.5, 0.45)
        if al > 0:
            off = (1 - ease((t - a0 - 0.1) / 0.8)) * 14
            nlabel(td, (80, 246 + off), lab[0], lab[1], LAB, al, node=True)
            for j, ln in enumerate(wrap(td, head, HEAD, 900)):
                td.text((80, 300 + off + j * 80), ln, font=HEAD, fill=rgba(OFF, al))
    # source captions (chapter 1)
    for n_, (pos, lab, desc, kind, ts) in enumerate(SRC):
        al = fade(t, ts - 0.1, CS[2] + 0.3, 0.4, 0.6)
        if al <= 0: continue
        p = T(pos, cam); left = pos[0] < 540
        y = p[1] + 78 if n_ == 2 else p[1] - 150
        if left:
            nlabel(td, (44, y), *lab.split('|'), CAPS2, al, 'l'); td.text((44, y + 34), desc, font=CAPS, fill=rgba(MUT, al))
        else:
            nlabel(td, (1036, y), *lab.split('|'), CAPS2, al, 'r'); dl = td.textlength(desc, font=CAPS); td.text((1036 - dl, y + 34), desc, font=CAPS, fill=rgba(MUT, al))
    # robot caption
    al = fade(t, CS[2] + 0.4, CS[3], 0.4, 0.5)
    if al > 0:
        rp = T(ROBOT, cam); tracked(td, (rp[0], rp[1] - 66), 'Robot · 1 message', CAPS2, rgba(OFF, al), 0.02, 'm')
    al = fade(t, sub_t('à des milliers') + 0.1, CS[3], 0.4, 0.5)
    if al > 0:
        rp = T(ROBOT, cam); tracked(td, (rp[0], rp[1] + 36), '× des milliers', CAPS, rgba(MUT, al), 0.02, 'm')
    # pirate caption
    al = fade(t, sub_t('et vous donnez') + 0.2, sub_t('Le réflexe') + 0.8, 0.4, 0.5)
    if al > 0:
        pp = T(PIR, cam); tracked(td, (pp[0], pp[1] + 56), 'Pirate', CAPS2, rgba(OFF, al), 0.02, 'm')
        tracked(td, (pp[0], pp[1] + 92), 'votre carte', CAPS, rgba(MUT, al), 0.02, 'm')
    # reflex captions
    for n_, (pos, lab, desc, ts) in enumerate(RFX):
        al = fade(t, ts + 0.1, VEND - 0.05, 0.5, 0.5)
        if al <= 0: continue
        p = T(pos, cam); right = pos[0] > 540
        x = p[0] + 40 if right else p[0] - 40; anchor = 'l' if right else 'r'
        nlabel(td, (x, p[1] - 36), *lab.split('|'), CAPS2, al, anchor)
        for j, ln in enumerate(wrap(td, desc, CAPS, 300)):
            lw_ = td.textlength(ln, font=CAPS)
            td.text((x if right else x - lw_, p[1] + 8 + j * 28), ln, font=CAPS, fill=rgba(MUT, al))
    # end card text
    ca = seg(t, WM1 + 0.2, WM1 + 0.7)
    if ca > 0:
        y0 = wm((0, 86))[1] + 70
        td.text((540 - td.textlength('Là où tout se connecte.', font=ImageFont.truetype(CAR, 48)) / 2, y0), 'Là où tout se connecte.', font=ImageFont.truetype(CAR, 48), fill=rgba(OFF, ca))
        nlabel(td, (540, y0 + 88), '', 'Décodé #01', ImageFont.truetype(CP, 30), ca, 'm', node=True)
    # subtitles
    for sb in SUBS:
        al = fade(t, sb['start'] - 0.05, sb['end'] + 0.15, 0.12, 0.12)
        if al <= 0: continue
        lines = wrap(td, sb['text'], SUBF, 860)
        lh = 58; bh = len(lines) * lh + 28; y0 = 1415
        maxw = max(td.textlength(ln, font=SUBF) for ln in lines)
        td.rounded_rectangle([540 - maxw / 2 - 26, y0, 540 + maxw / 2 + 26, y0 + bh], radius=16, fill=rgba(SURF, 0.8 * al))
        for j, ln in enumerate(lines):
            lw_ = td.textlength(ln, font=SUBF)
            td.text((540 - lw_ / 2, y0 + 12 + j * lh), ln, font=SUBF, fill=rgba(OFF, al))
    im.alpha_composite(tx)
    return im.convert('RGB')

if __name__ == '__main__':
    if '--still' in sys.argv:
        for ts in sys.argv[sys.argv.index('--still') + 1:]:
            frame(int(round(float(ts) * FPS))).save(f'/home/claude/decode01/still_{ts}.png')
        sys.exit()
    OUT = sys.argv[1]
    a, b = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, int(DUR * FPS))
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
    for i in range(a, b):
        p.stdin.write(frame(i).tobytes())
        if i % 150 == 0: print(i, '/', b, flush=True)
    p.stdin.close(); p.wait(); print('done', OUT)
