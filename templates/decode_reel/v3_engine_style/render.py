"""Decoded #03 — VPN. Background, server, path, glow and wordmark exactly as 'the engine';
text style exactly as 'Des fichiers à la décision' (Inter Display headline with violet accent, mono caps labels, corner marks)."""
import sys, json, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, SS = 1080, 1920, 30, 2
TIM = json.load(open('/home/claude/decode03/timing.json'))
SUBS, SENTS, VEND = TIM['subs'], TIM['sents'], TIM['voice_end']
DUR = round(VEND + 3.2, 2)
INK = (13, 11, 31); VIO = (139, 124, 255); DEEP = (91, 72, 224); OFF = (245, 246, 248); MUT = (169, 166, 191); LIN = (66, 61, 99)
TXT = (245, 243, 251); SURF = (26, 22, 54)
TAU = 2 * math.pi
FD = '/usr/share/fonts/opentype/inter/'
def F(p, s): return ImageFont.truetype(p, s)
HEAD = F(FD + 'InterDisplay-Medium.otf', 66)
SUB = F(FD + 'InterDisplay-Regular.otf', 40)
SUBT = F(FD + 'InterDisplay-Medium.otf', 40)
CARDF = F(FD + 'InterDisplay-Medium.otf', 34)
MONO = F('/home/claude/reel/fonts/JBMono-500.ttf', 24)
MONOS = F('/home/claude/reel/fonts/JBMono-400.ttf', 20)
MONOT = F('/home/claude/reel/fonts/JBMono-400.ttf', 22)

def ease(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def seg(t, a, b): return ease((t - a) / (b - a))
def fade(t, a, b, fi=0.6, fo=0.6):
    if t < a or t > b: return 0.0
    return min(ease((t - a) / fi), ease((b - t) / fo))
def lerp(a, b, u): return a + (b - a) * u
def rgba(c, a): return (int(c[0]), int(c[1]), int(c[2]), int(255 * max(0.0, min(1.0, a))))
def mixc(c1, c2, u): return tuple(lerp(a, b, u) for a, b in zip(c1, c2))
def shade(c, k): return tuple(v * k for v in c)
def S_(i): return SENTS[i]['start']
def SE(i): return SENTS[i]['end']
CH = [0.0, S_(1) - 0.2, S_(2) - 0.2, S_(4) - 0.2, S_(5) - 0.2, S_(6) - 0.2, VEND]   # chapter starts

# ---------------- camera ----------------
C0 = (540.0, 1030.0)
def camera(t):
    s = 1.0 + 0.012 * math.sin(TAU * t / 24)
    s *= 1 + 0.10 * seg(t, CH[2], CH[2] + 1.4) - 0.10 * seg(t, CH[3] - 0.2, CH[3] + 1.0)
    ox = 7 * math.sin(TAU * t / 24); oy = 5 * math.sin(2 * TAU * t / 24)
    return s, ox, oy
def T(p, cam):
    s, ox, oy = cam
    return (C0[0] + (p[0] - C0[0]) * s + ox, C0[1] + (p[1] - C0[1]) * s + oy)

# ---------------- background: identical to 'the engine' + invisible dither against banding ----------------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.sqrt(((xx - 540) / 700) ** 2 + ((yy - 1000) / 1050) ** 2)
VIGN = np.clip(1.08 - 0.55 * r ** 1.6, 0.35, 1.0)[..., None]
BG = (np.zeros((H, W, 3), np.float32) + np.array(INK, np.float32)) * VIGN
DITHER = np.random.default_rng(11).uniform(-0.5, 0.5, (H, W, 1)).astype(np.float32)
rng = np.random.default_rng(3)
DUST = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.6, 1.6), rng.uniform(0.08, 0.32), rng.uniform(0, TAU), rng.integers(1, 3)) for _ in range(140)]

# ---------------- the server (same sprite as 'the engine') ----------------
FX0, FX1, FY0, FY1 = 390.0, 690.0, 690.0, 1370.0
DX, DY = 42.0, -20.0
SPR_K = 2.8
SPR_OX, SPR_OY = FX0 - 10, FY0 + DY - 10
SPR_W, SPR_H = (FX1 + DX + 10) - SPR_OX, (FY1 + 10) - SPR_OY
def build_engine():
    k = SPR_K; w, h = int(SPR_W * k), int(SPR_H * k)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda x, y: ((x - SPR_OX) * k, (y - SPR_OY) * k)
    d.polygon([P(FX1, FY0), P(FX1 + DX, FY0 + DY), P(FX1 + DX, FY1 + DY), P(FX1, FY1)], fill=rgba(shade(INK, 0.45), 1))
    fw, fh = int((FX1 - FX0) * k), int((FY1 - FY0) * k)
    gy = np.linspace(0, 1, fh)[:, None]; gx = np.linspace(0, 1, fw)[None, :]
    base = 0.62 - 0.22 * gy + 0.10 * np.exp(-((gx - 0.18) / 0.10) ** 2) * (1 - gy * 0.7)
    face = np.zeros((fh, fw, 4), np.float32); face[..., :3] = np.array(INK, np.float32) * base[..., None]; face[..., 3] = 255
    im.alpha_composite(Image.fromarray(face.astype(np.uint8)), (int((FX0 - SPR_OX) * k), int((FY0 - SPR_OY) * k)))
    d.polygon([P(FX0, FY0), P(FX0 + DX, FY0 + DY), P(FX1 + DX, FY0 + DY), P(FX1, FY0)], fill=rgba(mixc(LIN, MUT, 0.35), 1))
    for (y0, y1) in [(FY0, FY0 + 16), (FY1 - 16, FY1)]:
        for i in range(int((y1 - y0) * k)):
            u = i / ((y1 - y0) * k)
            c = mixc(LIN, MUT, 0.25 + 0.5 * math.sin(math.pi * u) + 0.08 * math.sin(i * 1.7))
            d.line([P(FX0, y0 + i / k), P(FX1, y0 + i / k)], fill=rgba(c, 1))
        d.line([P(FX1, y0), P(FX1 + DX, y0 + DY)], fill=rgba(LIN, 1), width=2)
    gx0, gx1, gy0, gy1 = FX0 + 18, FX1 - 18, FY0 + 34, FY1 - 34
    d.rectangle([P(gx0, gy0), P(gx1, gy1)], fill=rgba(OFF, 0.025), outline=rgba(LIN, 0.55), width=2)
    n = 80
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n; a = math.sin(math.pi * (u0 + u1) / 2) ** 1.5
        d.line([P(FX0, lerp(FY0, FY1, u0)), P(FX0, lerp(FY0, FY1, u1))], fill=rgba(MUT, 0.55 * a), width=3)
        d.line([P(FX1, lerp(FY0, FY1, u0)), P(FX1, lerp(FY0, FY1, u1))], fill=rgba(LIN, 0.9 * a), width=2)
    return im
ENGINE = build_engine()

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
    def __init__(self, ctrl, n=24):
        self.pts = catmull(ctrl, n)
        L = np.concatenate([[0], np.cumsum([math.dist(a, b) for a, b in zip(self.pts, self.pts[1:])])]); self.len = L[-1]; self.L = L / L[-1]
    def at(self, s):
        s = min(max(s, 0), 1); i = int(np.searchsorted(self.L, s)); i = min(max(i, 1), len(self.pts) - 1)
        u = (s - self.L[i - 1]) / max(self.L[i] - self.L[i - 1], 1e-9)
        return (lerp(self.pts[i - 1][0], self.pts[i][0], u), lerp(self.pts[i - 1][1], self.pts[i][1], u))
    def part(self, a, b, n=70): return [self.at(a + (b - a) * j / n) for j in range(n + 1)]
ENG = Curve([(FX0 + 2, 748), (470, 752), (628, 790), (640, 862), (470, 930), (446, 1000), (520, 1060), (628, 1100),
             (640, 1175), (470, 1240), (455, 1300), (560, 1318), (FX1 - 2, 1322)])
NODES = [ENG.at(s) for s in (0.2, 0.4, 0.6, 0.8)]
PORT_IN, PORT_OUT = ENG.pts[0], ENG.pts[-1]

# ---------------- scene geometry ----------------
LAPTOP = (165, 610)
WEB = (920, 1200)
ISP = (150, 960)
PROXY = (230, 1150)
TUNNEL = Curve([(LAPTOP[0] + 62, LAPTOP[1] + 10), (290, 660), (330, 730), (PORT_IN[0] - 2, PORT_IN[1])])
EXIT = Curve([PORT_OUT, (760, 1330), (850, 1290), (WEB[0] - 86, WEB[1] + 20)])
PX1 = Curve([(LAPTOP[0] - 70, LAPTOP[1] + 20), (70, 790), (95, 1010), (PROXY[0] - 40, PROXY[1] - 50)])
PX2 = Curve([(PROXY[0] + 45, PROXY[1] + 20), (380, 1330), (620, 1455), (780, 1420), (WEB[0] - 86, WEB[1] + 40)])

def laptop_sprite(k=SS):
    w, h = 150, 110; im = Image.new('RGBA', (w * k, h * k), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([14 * k, 0, (w - 14) * k, 78 * k], radius=6 * k, fill=rgba(shade(INK, 0.6), 1), outline=rgba(mixc(LIN, MUT, 0.4), 1), width=2 * k)
    d.rectangle([22 * k, 8 * k, (w - 22) * k, 70 * k], fill=rgba(mixc(INK, LIN, 0.25), 1))
    for i, ww in enumerate([0.7, 0.5, 0.62]):
        d.line([30 * k, (20 + i * 14) * k, (30 + ww * 86) * k, (20 + i * 14) * k], fill=rgba(MUT, 0.6), width=int(2.4 * k))
    d.polygon([(0, 84 * k), (w * k, 84 * k), ((w - 10) * k, 96 * k), (10 * k, 96 * k)], fill=rgba(mixc(LIN, MUT, 0.35), 1))
    d.line([(14 * k, 80 * k), ((w - 14) * k, 80 * k)], fill=rgba(LIN, 1), width=2 * k)
    return im
def web_sprite(k=SS):
    w, h = 172, 128; im = Image.new('RGBA', (w * k, h * k), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w * k - 1, h * k - 1], radius=10 * k, fill=rgba(mixc(INK, LIN, 0.22), 1), outline=rgba(mixc(LIN, MUT, 0.4), 1), width=2 * k)
    d.line([(0, 26 * k), (w * k, 26 * k)], fill=rgba(LIN, 1), width=2 * k)
    for i in range(3): d.ellipse([(12 + i * 14) * k, 9 * k, (20 + i * 14) * k, 17 * k], fill=rgba(MUT, 0.7))
    d.rounded_rectangle([14 * k, 40 * k, 74 * k, 100 * k], radius=6 * k, fill=rgba(LIN, 0.9))
    for i, ww in enumerate([0.9, 0.7, 0.8, 0.5]):
        d.line([86 * k, (46 + i * 15) * k, (86 + ww * 70) * k, (46 + i * 15) * k], fill=rgba(MUT, 0.6), width=int(2.4 * k))
    return im
def server_sprite(k=SS):
    w, h = 92, 150; im = Image.new('RGBA', (w * k + 4, h * k + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([2, 2, 2 + w * k, 2 + h * k], fill=rgba(shade(INK, 0.55), 1), outline=rgba(LIN, 1), width=k)
    for i in range(6):
        y = 2 + (14 + i * 22) * k
        d.rectangle([2 + 8 * k, y, 2 + w * k - 8 * k, y + 14 * k], outline=rgba(LIN, 0.9), width=k)
    return im
def tag_sprite(label, k=SS):
    f = ImageFont.truetype('/home/claude/reel/fonts/JBMono-500.ttf', 15 * k)
    tw = ImageDraw.Draw(Image.new('RGBA', (1, 1))).textlength(label, font=f)
    w, h = int(tw + 34 * k), 40 * k
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=8 * k, fill=rgba(OFF, 0.95))
    d.ellipse([10 * k, 16 * k, 18 * k, 24 * k], fill=rgba(DEEP, 1))
    d.text((24 * k, 10 * k), label, font=f, fill=rgba(INK, 0.9))
    return im
LAPTOP_SPR, WEB_SPR, PROXY_SPR = laptop_sprite(), web_sprite(), server_sprite()
TAGS = [tag_sprite(s) for s in ('ACCOUNT', 'COOKIES', 'FINGERPRINT')]
TAG_T = [S_(4) + 1.35, S_(4) + 2.35, S_(4) + 3.3]

# ---------------- wordmark (same as 'the engine') ----------------
def quad(p0, c, p1, n=14): return [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * c[0] + u * u * p1[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * c[1] + u * u * p1[1]) for u in np.linspace(0, 1, n)]
def circ(cx, cy, r_, n=64): return [(cx + r_ * math.cos(-math.pi / 2 - a), cy + r_ * math.sin(-math.pi / 2 - a)) for a in np.linspace(0, TAU, n)]
N_PATH = [(24, 78), (24, 31)] + quad((24, 31), (24, 20), (32, 28))[1:] + [(68, 72)] + quad((68, 72), (76, 80), (76, 69))[1:] + [(76, 22)]
STROKES = [N_PATH, circ(108, 58, 20), circ(158, 58, 20), [(178, 22), (178, 78)], circ(210, 58, 20),
           [(230, 40), (230, 70)] + quad((230, 70), (230, 78), (238, 78))[1:], [(250, 22), (250, 70)] + quad((250, 70), (250, 78), (258, 78))[1:]]
STROKES = [[(x + 2, y) for x, y in s] for s in STROKES]
WK = 3.25; WCX, WCY = 540, 900
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
WM0, WM1 = VEND + 0.35, VEND + 1.55

# ---------------- helpers ----------------
def dot(dr, p, r_, c, a, k=SS): dr.ellipse([(p[0] - r_) * k, (p[1] - r_) * k, (p[0] + r_) * k, (p[1] + r_) * k], fill=rgba(c, a))
def ring(dr, p, r_, c, a, w, k=SS): dr.ellipse([(p[0] - r_) * k, (p[1] - r_) * k, (p[0] + r_) * k, (p[1] + r_) * k], outline=rgba(c, a), width=max(1, int(w * k)))
def paste(lay, spr, center, scale, alpha, ang=0):
    if alpha <= 0.005: return
    im = spr.resize((max(2, int(spr.width * scale)), max(2, int(spr.height * scale))), Image.BILINEAR)
    if ang: im = im.rotate(ang, resample=Image.BICUBIC, expand=True)
    if alpha < 0.999:
        a_ = np.asarray(im, np.float32).copy(); a_[..., 3] *= alpha; im = Image.fromarray(a_.astype(np.uint8))
    lay.alpha_composite(im, (int(center[0] * SS - im.width / 2), int(center[1] * SS - im.height / 2)))
def path_line(dr, gd, wd, pts, a, s, width=2.2):
    if a <= 0 or len(pts) < 2: return
    dr.line([(x * SS, y * SS) for x, y in pts], fill=rgba(VIO, 0.85 * a), width=max(1, int(width * s * SS)), joint='curve')
    gd.line(pts, fill=rgba(VIO, 0.7 * a), width=max(1, int(6 * s))); wd.line(pts, fill=rgba(VIO, 0.3 * a), width=max(1, int(14 * s)))
def dashed(dr, pts, c, a, w, on=10, off=9):
    acc, draw_on, seg_pts = 0.0, True, [pts[0]]
    for p, q in zip(pts, pts[1:]):
        d = math.dist(p, q); acc += d; seg_pts.append(q)
        if acc >= (on if draw_on else off):
            if draw_on: dr.line([(x * SS, y * SS) for x, y in seg_pts], fill=rgba(c, a), width=max(1, int(w * SS)))
            draw_on = not draw_on; acc = 0; seg_pts = [q]
    if draw_on and len(seg_pts) > 1: dr.line([(x * SS, y * SS) for x, y in seg_pts], fill=rgba(c, a), width=max(1, int(w * SS)))
def tube(dr, gd, wd, curve, cam, a, grow=1.0):
    if a <= 0 or grow <= 0: return
    pts = [T(p, cam) for p in curve.part(0, grow)]
    s = cam[0]
    wd.line(pts, fill=rgba(VIO, 0.22 * a), width=int(40 * s))
    gd.line(pts, fill=rgba(VIO, 0.16 * a), width=int(22 * s))
    for side in (-1, 1):
        edge = []
        for p, q in zip(pts, pts[1:] + [pts[-1]]):
            dx, dy = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dy) or 1
            edge.append((p[0] - side * dy / L * 11 * s, p[1] + side * dx / L * 11 * s))
        edge[-1] = (pts[-1][0] + (edge[-2][0] - pts[-2][0]), pts[-1][1] + (edge[-2][1] - pts[-2][1]))
        dr.line([(x * SS, y * SS) for x, y in edge], fill=rgba(VIO, 0.8 * a), width=int(1.6 * s * SS), joint='curve')
def packets(dr, gd, curve, cam, t, a, n=7, speed=2.2, locked=True, grow=1.0):
    s = cam[0]
    for k_ in range(n):
        sp = ((k_ / n) + t / speed) % 1.0
        if sp > grow: continue
        p = T(curve.at(sp), cam); aa = math.sin(math.pi * sp) ** 0.5 * a
        if locked:
            r_ = 5.5 * s
            dr.rounded_rectangle([(p[0] - r_) * SS, (p[1] - r_ * 0.6) * SS, (p[0] + r_) * SS, (p[1] + r_) * SS], radius=int(2 * SS), fill=rgba(OFF, aa))
            dr.arc([(p[0] - r_ * 0.6) * SS, (p[1] - r_ * 1.5) * SS, (p[0] + r_ * 0.6) * SS, (p[1] - r_ * 0.1) * SS], 180, 360, fill=rgba(OFF, aa), width=int(1.6 * SS))
        else:
            dr.rectangle([(p[0] - 9 * s) * SS, (p[1] - 6 * s) * SS, (p[0] + 9 * s) * SS, (p[1] + 6 * s) * SS], fill=rgba(OFF, aa))
            dr.line([((p[0] - 6 * s) * SS, (p[1] - 1) * SS), ((p[0] + 5 * s) * SS, (p[1] - 1) * SS)], fill=rgba(MUT, aa), width=SS)
        gd.ellipse([p[0] - 9, p[1] - 9, p[0] + 9, p[1] + 9], fill=rgba(VIO, 0.5 * aa))

# ---------------- text (style of 'Des fichiers à la décision') ----------------
def spaced(dr, xy, s, font, fill, sp=0.12, anchor='l'):
    x, y = xy; ws = [dr.textlength(c, font=font) + font.size * sp for c in s]
    tot = sum(ws) - font.size * sp
    if anchor == 'm': x -= tot / 2
    if anchor == 'r': x -= tot
    for c, w in zip(s, ws): dr.text((x, y), c, font=font, fill=fill); x += w
def rich(dr, x, y, parts, font, alpha, maxw=920, center=False):
    words = [(w_, acc) for tx, acc in parts for w_ in tx.split(' ') if w_]
    lines, cur, cw = [], [], 0; sp = dr.textlength(' ', font=font)
    for w_, acc in words:
        ww = dr.textlength(w_, font=font)
        if cur and cw + sp + ww > maxw: lines.append((cur, cw)); cur, cw = [], 0
        cw += (sp if cur else 0) + ww; cur.append((w_, acc, ww))
    if cur: lines.append((cur, cw))
    for i, (ln, lw) in enumerate(lines):
        x_ = (W - lw) / 2 if center else x
        for w_, acc, ww in ln:
            dr.text((x_, y + i * font.size * 1.12), w_, font=font, fill=(VIO if acc else TXT) + (int(255 * alpha),)); x_ += ww + sp
def label(dr, p, title, sub, al, anchor='l'):
    spaced(dr, (p[0], p[1]), title, MONO, rgba(TXT, al), 0.12, anchor)
    if sub: spaced(dr, (p[0], p[1] + 34), sub, MONOS, rgba(VIO, al), 0.12, anchor)
HEADS = [(CH[0] + 0.4, CH[1], [("A VPN doesn't make you", 0), ('invisible.', 1)]),
         (CH[1], CH[2], [('An encrypted', 0), ('tunnel.', 1)]),
         (CH[2], CH[3], [('Your provider sees the tunnel.', 0), ('The VPN sees everything.', 1)]),
         (CH[3], CH[4], [('Websites still', 0), ('recognise you.', 1)]),
         (CH[4], CH[5], [('A proxy is just a', 0), ('middleman.', 1)]),
         (CH[5], VEND - 0.1, [('It protects. It doesn\'t', 0), ('hide you.', 1)])]
CARDS = [(1075, 'Unsafe public Wi-Fi', 'PROTECTED · ENCRYPTED TUNNEL', S_(6) + 0.9, True),
         (1190, 'Your company\'s network', 'REMOTE ACCESS · SECURE', S_(6) + 2.8, True),
         (1305, 'Disappearing online', 'NO · STILL RECOGNISED', S_(7) + 0.3, False)]

# ---------------- frame ----------------
def frame(i):
    t = i / FPS; cam = camera(t); s = cam[0]
    lay = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0)); dr = ImageDraw.Draw(lay)
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    wide = Image.new('RGBA', (W, H), (0, 0, 0, 0)); wd = ImageDraw.Draw(wide)
    for (x, y, rr_, a, ph, m) in DUST:
        px = x + 18 * math.sin(TAU * t / 24 * m + ph); py = y + 26 * math.sin(TAU * t / 24 + ph * 1.3)
        dot(dr, (px, py), rr_, MUT, a)
    scene = seg(t, 0.0, 0.8) * (1 - seg(t, VEND - 0.15, VEND + 0.45))
    # server brightness: dims during the proxy chapter and under the cards
    dim = 1 - 0.6 * fade(t, CH[4] - 0.1, CH[5] + 0.3, 0.6, 0.6) - 0.55 * seg(t, S_(6) + 0.6, S_(6) + 1.4)
    dim = max(0.15, dim) * scene
    # floor ring (as in 'the engine')
    fc = T((560, 1402), cam); rx, ry = 270 * s, 44 * s
    wd.ellipse([fc[0] - rx, fc[1] - ry, fc[0] + rx, fc[1] + ry], outline=rgba(VIO, 0.55 * dim), width=6)
    dr.ellipse([(fc[0] - rx) * SS, (fc[1] - ry) * SS, (fc[0] + rx) * SS, (fc[1] + ry) * SS], outline=rgba(VIO, 0.45 * dim), width=2 * SS)
    # server
    tl = T((SPR_OX, SPR_OY), cam)
    eng = ENGINE.resize((int(SPR_W * s * SS), int(SPR_H * s * SS)), Image.BILINEAR)
    if dim < 0.999:
        a_ = np.asarray(eng, np.float32).copy(); a_[..., 3] *= dim; eng = Image.fromarray(a_.astype(np.uint8))
    lay.alpha_composite(eng, (int(tl[0] * SS), int(tl[1] * SS)))
    u = 0.5 + 0.5 * math.sin(TAU * t / 24 - 1.2); sx = lerp(FX0 - 80, FX1 + 40, u)
    sheen = Image.new('RGBA', lay.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sheen)
    poly = [T((sx, FY0), cam), T((sx + 70, FY0), cam), T((sx + 10, FY1), cam), T((sx - 60, FY1), cam)]
    sd.polygon([(x * SS, y * SS) for x, y in poly], fill=rgba(OFF, 0.07 * dim))
    m = Image.new('L', lay.size, 0); ImageDraw.Draw(m).polygon([(x * SS, y * SS) for x, y in [T((FX0, FY0 + 16), cam), T((FX1, FY0 + 16), cam), T((FX1, FY1 - 16), cam), T((FX0, FY1 - 16), cam)]], fill=255)
    lay.paste(sheen, (0, 0), Image.fromarray(np.minimum(np.asarray(m), np.asarray(sheen.split()[-1])).astype(np.uint8)))
    # S-curve inside the server
    lw = 0.85 * dim + 0.15 * scene
    pts = [T(p, cam) for p in ENG.pts]
    path_line(dr, gd, wd, pts, lw, s)
    sees = fade(t, S_(3) + 0.9, CH[4], 0.4, 0.6)
    for k_ in range(42):
        sp = ((k_ / 42) + t / 3.0) % 1.0
        p = T(ENG.at(sp), cam); a = math.sin(math.pi * sp) ** 0.5 * lw
        dot(dr, p, 2.4 * s, (225, 220, 255), a); gd.ellipse([p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7], fill=rgba(VIO, 0.6 * a))
    for n_, pn in enumerate(NODES):
        p = T(pn, cam); lit = fade(t, S_(3) + 0.9 + n_ * 0.18, CH[4], 0.35, 0.6)
        dot(dr, p, (4.5 + 2.5 * lit) * s, mixc((200, 192, 255), OFF, lit), lw)
        ring(dr, p, (11 + 5 * lit) * s, VIO, (0.55 + 0.45 * lit) * lw, 1.6)
        gd.ellipse([p[0] - 18 * s, p[1] - 18 * s, p[0] + 18 * s, p[1] + 18 * s], fill=rgba(VIO, (0.5 + 0.5 * lit) * lw))
        pr = (t - (S_(3) + 0.9 + n_ * 0.18)) / 0.9
        if 0 < pr < 1: ring(dr, p, (16 + 40 * pr) * s, VIO, 0.6 * (1 - pr), 1.4)
    for port in (PORT_IN, PORT_OUT):
        p = T(port, cam); b = 0.6 * lw
        ring(dr, p, 8 * s, OFF, 0.8 * b, 1.6); dot(dr, p, 3.5 * s, OFF, b)
        wd.ellipse([p[0] - 34 * s, p[1] - 34 * s, p[0] + 34 * s, p[1] + 34 * s], fill=rgba(VIO, 0.6 * b))
    # laptop + website
    dev_a = seg(t, 0.4, 1.2) * scene * (1 - 0.85 * seg(t, S_(6) + 0.6, S_(6) + 1.4))
    paste(lay, LAPTOP_SPR, T(LAPTOP, cam), s, dev_a)
    web_a = seg(t, 0.8, 1.6) * scene * (1 - 0.85 * seg(t, S_(6) + 0.6, S_(6) + 1.4))
    paste(lay, WEB_SPR, T(WEB, cam), s, web_a)
    # tunnel laptop -> server
    tg = seg(t, S_(1) + 0.5, S_(1) + 2.0)
    tun_a = scene * (1 - 0.75 * fade(t, CH[4] - 0.1, CH[5] + 0.3, 0.6, 0.6)) * (1 - 0.6 * seg(t, S_(6) + 0.6, S_(6) + 1.4))
    tube(dr, gd, wd, TUNNEL, cam, tun_a, tg)
    if tg > 0: packets(dr, gd, TUNNEL, cam, t, tun_a, 6, 2.0, True, tg)
    # exit server -> website (plain line, unencrypted after the VPN)
    eg = seg(t, S_(1) + 1.6, S_(1) + 2.8)
    ex_a = tun_a
    path_line(dr, gd, wd, [T(q, cam) for q in EXIT.part(0, eg)], ex_a * 0.9, s, 1.8)
    if eg >= 1: packets(dr, gd, EXIT, cam, t, ex_a, 5, 2.4, False)
    # internet provider (sees the tunnel only)
    isp_a = fade(t, S_(2) + 0.2, CH[4] - 0.1, 0.5, 0.6) * scene
    if isp_a > 0:
        p = T(ISP, cam); q = T(TUNNEL.at(0.45), cam)
        dashed(dr, [p, (lerp(p[0], q[0], 0.5), lerp(p[1], q[1], 0.5)), q], MUT, 0.7 * isp_a, 1.4)
        dr.ellipse([(p[0] - 24 * s) * SS, (p[1] - 24 * s) * SS, (p[0] + 24 * s) * SS, (p[1] + 24 * s) * SS], fill=rgba(shade(INK, 0.6), isp_a), outline=rgba(MUT, 0.8 * isp_a), width=2 * SS)
        dot(dr, p, 6 * s, MUT, isp_a)
    # tags riding to the website (traces)
    tr_a = fade(t, S_(4) + 1.0, CH[4] + 0.4, 0.4, 0.6) * scene
    for n_, (spr, tt) in enumerate(zip(TAGS, TAG_T)):
        uu = seg(t, tt - 0.9, tt)
        if uu <= 0 or tr_a <= 0: continue
        start = T(PORT_OUT, cam); dest = T((WEB[0] - 20, WEB[1] + 98 + n_ * 46), cam)
        pos = T(EXIT.at(uu), cam) if uu < 1 else dest
        if uu >= 1: pos = dest
        else: pos = (lerp(T(EXIT.at(uu), cam)[0], dest[0], uu ** 3), lerp(T(EXIT.at(uu), cam)[1], dest[1], uu ** 3))
        paste(lay, spr, pos, s * lerp(0.6, 0.9, uu), tr_a)
    if tr_a > 0:
        p = T(WEB, cam); pulse = fade(t, TAG_T[-1] + 0.1, TAG_T[-1] + 1.3, 0.2, 0.8)
        ring(dr, p, (100 + 30 * pulse) * s, VIO, 0.5 * pulse * tr_a, 1.4)
    # proxy (chapter 4)
    px_a = fade(t, CH[4] + 0.1, CH[5] + 0.4, 0.5, 0.6) * scene
    if px_a > 0:
        g1 = seg(t, CH[4] + 0.4, CH[4] + 1.3); g2 = seg(t, CH[4] + 1.1, CH[4] + 2.2)
        dashed(dr, [T(q, cam) for q in PX1.part(0, g1)], OFF, 0.75 * px_a, 1.6)
        dashed(dr, [T(q, cam) for q in PX2.part(0, g2)], OFF, 0.75 * px_a, 1.6)
        paste(lay, PROXY_SPR, T(PROXY, cam), s * 0.8, px_a)
        if g2 >= 1:
            packets(dr, gd, PX1, cam, t, px_a, 3, 2.0, False); packets(dr, gd, PX2, cam, t, px_a, 4, 2.4, False)
    # wordmark close
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
    # composite (same as 'the engine')
    lay = lay.resize((W, H), Image.LANCZOS)
    out = BG.copy()
    for g_, rad, k_ in [(wide, 38, 0.9), (glow, 10, 1.0)]:
        ga = np.asarray(g_.filter(ImageFilter.GaussianBlur(rad)), np.float32)
        out = out + ga[..., :3] * (ga[..., 3:] / 255) * k_
    l = np.asarray(lay, np.float32); la = l[..., 3:] / 255
    out = out * (1 - la) + l[..., :3] * la
    # decision cards (style of 'Des fichiers à la décision')
    im = Image.fromarray(np.clip(out + DITHER, 0, 255).astype(np.uint8)).convert('RGBA')
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(tx)
    ca_all = fade(t, S_(6) + 0.6, VEND - 0.05, 0.4, 0.5)
    if ca_all > 0:
        x0, x1 = 210, 870
        for k_, (cy, title, sub, ts, ok) in enumerate(CARDS):
            ca = seg(t, ts, ts + 0.45) * ca_all
            if ca <= 0: continue
            off = (1 - seg(t, ts, ts + 0.45)) * 16
            td.rounded_rectangle([x0, cy + off, x1, cy + 92 + off], radius=10, fill=rgba(SURF, 0.94 * ca), outline=rgba(LIN, ca), width=2)
            cx, cyy = x0 + 36, cy + 46 + off
            if ok:
                td.ellipse([cx - 9, cyy - 9, cx + 9, cyy + 9], fill=rgba(VIO, ca))
            else:
                td.ellipse([cx - 9, cyy - 9, cx + 9, cyy + 9], outline=rgba(MUT, ca), width=2)
                td.line([cx - 5, cyy - 5, cx + 5, cyy + 5], fill=rgba(MUT, ca), width=2); td.line([cx - 5, cyy + 5, cx + 5, cyy - 5], fill=rgba(MUT, ca), width=2)
            td.text((x0 + 70, cy + 14 + off), title, font=CARDF, fill=rgba(TXT if ok else MUT, ca))
            spaced(td, (x0 + 70, cy + 58 + off), sub, MONOS, rgba(VIO if ok else MUT, ca), 0.12)
            if ok and title.startswith('Unsafe'):
                pass
    # corner marks + top label
    ga_ = seg(t, 0.2, 0.8) * (1 - seg(t, VEND - 0.2, VEND + 0.3))
    c = (245, 243, 251, int(64 * ga_)); Ln, mm = 26, 40
    for (x, y, sx_, sy_) in [(mm, mm, 1, 1), (W - mm, mm, -1, 1), (mm, H - mm, 1, -1), (W - mm, H - mm, -1, -1)]:
        td.line((x, y, x + sx_ * Ln, y), fill=c, width=2); td.line((x, y, x, y + sy_ * Ln), fill=c, width=2)
    spaced(td, (72, 150), 'NODAL — DECODED · VPN', MONOT, (245, 243, 251, int(150 * ga_)))
    for (a0, a1, parts) in HEADS:
        al = fade(t, a0 + 0.1, a1, 0.45, 0.4)
        if al > 0: rich(td, 80, 300 + (1 - ease((t - a0 - 0.1) / 0.5)) * 18, parts, HEAD, al)
    # scene labels
    lab = seg(t, 1.0, 1.6) * scene * (1 - 0.9 * seg(t, S_(6) + 0.6, S_(6) + 1.4))
    if lab > 0:
        p = T(LAPTOP, cam); label(td, (p[0], p[1] + 66), 'YOUR DEVICE', '', lab, 'm')
        p = T(WEB, cam); label(td, (p[0], p[1] - 112), 'WEBSITE', '', lab, 'm')
    a = fade(t, S_(1) + 1.6, CH[2] + 0.2, 0.4, 0.5)
    if a > 0:
        p = T(TUNNEL.at(0.5), cam); label(td, (p[0] + 30, p[1] - 92), 'ENCRYPTED', 'TUNNEL', a, 'l')
    if isp_a > 0:
        p = T(ISP, cam); label(td, (44, p[1] + 40), 'INTERNET PROVIDER', 'SEES THE TUNNEL ONLY', isp_a, 'l')
    if sees > 0:
        p = T((FX1 + DX + 18, 900), cam); label(td, (p[0], p[1]), 'VPN SERVER', 'SEES EVERYTHING', sees, 'l')
    if tr_a > 0:
        p = T(WEB, cam); label(td, (1036, p[1] + 228), 'RECOGNISES YOU', '', seg(t, TAG_T[-1], TAG_T[-1] + 0.5) * tr_a, 'r')
    if px_a > 0:
        p = T(PROXY, cam); label(td, (44, p[1] + 90), 'PROXY', 'NO ENCRYPTION', seg(t, CH[4] + 0.6, CH[4] + 1.1) * px_a, 'l')
    # subtitles
    for sb in SUBS:
        al = fade(t, sb['start'] - 0.05, sb['end'] + 0.12, 0.1, 0.1)
        if al <= 0: continue
        words = sb['text']; lines = []
        cur = ''
        for w_ in words.split(' '):
            nx = (cur + ' ' + w_).strip()
            if td.textlength(nx, font=SUBT) > 880 and cur: lines.append(cur); cur = w_
            else: cur = nx
        lines.append(cur)
        lh = 54; bh = len(lines) * lh + 26; y0 = 1505
        maxw = max(td.textlength(ln, font=SUBT) for ln in lines)
        td.rounded_rectangle([540 - maxw / 2 - 24, y0, 540 + maxw / 2 + 24, y0 + bh], radius=12, fill=rgba(SURF, 0.82 * al))
        for j, ln in enumerate(lines):
            lw_ = td.textlength(ln, font=SUBT); td.text((540 - lw_ / 2, y0 + 10 + j * lh), ln, font=SUBT, fill=rgba(TXT, al))
    # end card text
    e = seg(t, WM1 + 0.2, WM1 + 0.8)
    if e > 0:
        ty = wm((0, 86))[1] + 80
        rich(td, 0, ty, [('Where everything', 0), ('connects.', 1)], SUB, e * 0.9, center=True)
        spaced(td, (W / 2, ty + 80), 'NODAL — DECODED #03', MONO, VIO + (int(255 * e),), anchor='m')
    im.alpha_composite(tx)
    return im.convert('RGB')

if __name__ == '__main__':
    if '--still' in sys.argv:
        for ts in sys.argv[sys.argv.index('--still') + 1:]:
            frame(int(round(float(ts) * FPS))).save(f'/home/claude/decode03/still_{ts}.png')
        sys.exit()
    OUT = sys.argv[1]
    a, b = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, int(DUR * FPS))
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
    for i in range(a, b):
        p.stdin.write(frame(i).tobytes())
        if i % 150 == 0: print(i, '/', b, flush=True)
    p.stdin.close(); p.wait(); print('done', OUT)
