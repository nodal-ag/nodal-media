"""Decoded kit — validated v3 look: background/server/glow/wordmark of 'the engine',
text of 'Des fichiers à la décision'. Episodes only describe their scene."""
import sys, json, math, subprocess, importlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, SS = 1080, 1920, 30, 2
INK = (13, 11, 31); VIO = (139, 124, 255); DEEP = (91, 72, 224); OFF = (245, 246, 248); MUT = (169, 166, 191); LIN = (66, 61, 99)
TXT = (245, 243, 251); SURF = (26, 22, 54); PART = (225, 220, 255)
TAU = 2 * math.pi
FD = '/usr/share/fonts/opentype/inter/'
JB5 = '/home/claude/reel/fonts/JBMono-500.ttf'; JB4 = '/home/claude/reel/fonts/JBMono-400.ttf'
def F(p, s): return ImageFont.truetype(p, s)
HEAD = F(FD + 'InterDisplay-Medium.otf', 66)
SUBF = F(FD + 'InterDisplay-Regular.otf', 40)
SUBT = F(FD + 'InterDisplay-Medium.otf', 40)
CARDF = F(FD + 'InterDisplay-Medium.otf', 34)
UI = lambda s: F(FD + 'Inter-Medium.otf', s)
UIB = lambda s: F(FD + 'Inter-SemiBold.otf', s)
UIR = lambda s: F(FD + 'Inter-Regular.otf', s)
MONO = F(JB5, 24); MONOS = F(JB4, 20); MONOT = F(JB4, 22)
MON = lambda s: F(JB5, s)

def ease(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def seg(t, a, b): return ease((t - a) / (b - a)) if b != a else float(t >= a)
def fade(t, a, b, fi=0.6, fo=0.6):
    if t < a or t > b: return 0.0
    return min(ease((t - a) / fi), ease((b - t) / fo))
def lerp(a, b, u): return a + (b - a) * u
def rgba(c, a): return (int(c[0]), int(c[1]), int(c[2]), int(255 * max(0.0, min(1.0, a))))
def mixc(c1, c2, u): return tuple(lerp(a, b, u) for a, b in zip(c1, c2))
def shade(c, k): return tuple(v * k for v in c)
def setalpha(im, a):
    if a >= 0.999: return im
    x = np.asarray(im, np.float32).copy(); x[..., 3] *= max(a, 0); return Image.fromarray(x.astype(np.uint8))

# ---------------- background (identical to 'the engine') ----------------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
_r = np.sqrt(((xx - 540) / 700) ** 2 + ((yy - 1000) / 1050) ** 2)
BG = (np.zeros((H, W, 3), np.float32) + np.array(INK, np.float32)) * np.clip(1.08 - 0.55 * _r ** 1.6, 0.35, 1.0)[..., None]
DITHER = np.random.default_rng(11).uniform(-0.5, 0.5, (H, W, 1)).astype(np.float32)
_rng = np.random.default_rng(3)
DUST = [(_rng.uniform(0, W), _rng.uniform(0, H), _rng.uniform(0.6, 1.6), _rng.uniform(0.08, 0.32), _rng.uniform(0, TAU), _rng.integers(1, 3)) for _ in range(140)]

# ---------------- curves ----------------
def catmull(pts, n=24):
    out = []; P = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(n):
            u = j / n; u2, u3 = u * u, u * u * u
            out.append(tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * u + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * u2 +
                                  (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * u3) for k in (0, 1)))
    out.append(tuple(pts[-1])); return out
class Curve:
    def __init__(self, ctrl, n=24):
        self.pts = catmull(ctrl, n)
        L = np.concatenate([[0], np.cumsum([math.dist(a, b) for a, b in zip(self.pts, self.pts[1:])])]); self.L = L / max(L[-1], 1e-9)
    def at(self, s):
        s = min(max(s, 0), 1); i = int(np.searchsorted(self.L, s)); i = min(max(i, 1), len(self.pts) - 1)
        u = (s - self.L[i - 1]) / max(self.L[i] - self.L[i - 1], 1e-9)
        return (lerp(self.pts[i - 1][0], self.pts[i][0], u), lerp(self.pts[i - 1][1], self.pts[i][1], u))
    def part(self, a, b, n=70): return [self.at(a + (b - a) * j / n) for j in range(n + 1)]

# ---------------- sprites ----------------
def _face(w, h, k, top=0.62, bot=0.22):
    gy = np.linspace(0, 1, int(h * k))[:, None]; gx = np.linspace(0, 1, int(w * k))[None, :]
    base = top - bot * gy + 0.10 * np.exp(-((gx - 0.18) / 0.10) ** 2) * (1 - gy * 0.7)
    f = np.zeros((int(h * k), int(w * k), 4), np.float32); f[..., :3] = np.array(INK, np.float32) * base[..., None] + 3; f[..., 3] = 255
    return Image.fromarray(np.clip(f, 0, 255).astype(np.uint8))

class Hero:
    """A 3D block in the engine style. kind: tower | slab (phone, window, laptop screen...) ; screen callback paints the front."""
    def __init__(self, x0, y0, x1, y1, dx=42, dy=-20, radius=0, k=2.6, caps=False, glass=True, base=None):
        self.x0, self.y0, self.x1, self.y1, self.dx, self.dy, self.R, self.k = x0, y0, x1, y1, dx, dy, radius, k
        self.ox, self.oy = x0 - 12, y0 + dy - 12
        self.w, self.h = (x1 + dx + 12) - self.ox, (y1 + 12) - self.oy
        k_ = k; w, h = int(self.w * k_), int(self.h * k_)
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        P = lambda x, y: ((x - self.ox) * k_, (y - self.oy) * k_)
        R = radius
        if R == 0:
            d.polygon([P(x1, y0), P(x1 + dx, y0 + dy), P(x1 + dx, y1 + dy), P(x1, y1)], fill=rgba(shade(INK, 0.45), 1))
            im.alpha_composite(_face(x1 - x0, y1 - y0, k_), (int((x0 - self.ox) * k_), int((y0 - self.oy) * k_)))
            d = ImageDraw.Draw(im)
            d.polygon([P(x0, y0), P(x0 + dx, y0 + dy), P(x1 + dx, y0 + dy), P(x1, y0)], fill=rgba(mixc(LIN, MUT, 0.35), 1))
        else:
            for i in range(16, -1, -1):
                u = i / 16
                d.rounded_rectangle([P(x0 + dx * u, y0 + dy * u), P(x1 + dx * u, y1 + dy * u)], radius=R * k_, fill=rgba(mixc(shade(INK, 0.5), LIN, 0.35 * (1 - u) + 0.08), 1))
            fc = _face(x1 - x0, y1 - y0, k_, 0.95, 0.30)
            m = Image.new('L', fc.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, fc.width - 1, fc.height - 1], radius=R * k_, fill=255)
            fc.putalpha(m); im.alpha_composite(fc, (int((x0 - self.ox) * k_), int((y0 - self.oy) * k_)))
            d = ImageDraw.Draw(im)
            d.rounded_rectangle([P(x0, y0), P(x1, y1)], radius=R * k_, outline=rgba(mixc(LIN, MUT, 0.4), 0.9), width=int(2 * k_))
        if caps:
            for (a, b) in [(y0, y0 + 16), (y1 - 16, y1)]:
                for i in range(int((b - a) * k_)):
                    u = i / ((b - a) * k_)
                    c = mixc(LIN, MUT, 0.25 + 0.5 * math.sin(math.pi * u) + 0.08 * math.sin(i * 1.7))
                    d.line([P(x0, a + i / k_), P(x1, a + i / k_)], fill=rgba(c, 1))
                d.line([P(x1, a), P(x1 + dx, a + dy)], fill=rgba(LIN, 1), width=2)
        if glass and R == 0:
            d.rectangle([P(x0 + 18, y0 + 34), P(x1 - 18, y1 - 34)], fill=rgba(OFF, 0.025), outline=rgba(LIN, 0.55), width=2)
        if R == 0:
            n = 80
            for i in range(n):
                u0, u1 = i / n, (i + 1) / n; a = math.sin(math.pi * (u0 + u1) / 2) ** 1.5
                d.line([P(x0, lerp(y0, y1, u0)), P(x0, lerp(y0, y1, u1))], fill=rgba(MUT, 0.55 * a), width=3)
                d.line([P(x1, lerp(y0, y1, u0)), P(x1, lerp(y0, y1, u1))], fill=rgba(LIN, 0.9 * a), width=2)
        if base == 'laptop':
            d.polygon([P(x0 - 70, y1 + 6), P(x1 + 70, y1 + 6), P(x1 + 70 + dx * 0.4, y1 + 26), P(x0 - 70 + dx * 0.4, y1 + 26)], fill=rgba(mixc(LIN, MUT, 0.35), 1))
        self.im = im
    def draw(self, lay, cam, alpha):
        s = cam[0]; tl = T((self.ox, self.oy), cam)
        im = self.im.resize((max(2, int(self.w * s * SS)), max(2, int(self.h * s * SS))), Image.BILINEAR)
        lay.alpha_composite(setalpha(im, alpha), (int(tl[0] * SS), int(tl[1] * SS)))
    def sheen(self, lay, cam, t, alpha):
        s = cam[0]; u = 0.5 + 0.5 * math.sin(TAU * t / 24 - 1.2); sx = lerp(self.x0 - 80, self.x1 + 40, u)
        sh = Image.new('RGBA', lay.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
        poly = [T((sx, self.y0), cam), T((sx + 70, self.y0), cam), T((sx + 10, self.y1), cam), T((sx - 60, self.y1), cam)]
        sd.polygon([(x * SS, y * SS) for x, y in poly], fill=rgba(OFF, 0.06 * alpha))
        m = Image.new('L', lay.size, 0); a, b = T((self.x0, self.y0), cam), T((self.x1, self.y1), cam)
        ImageDraw.Draw(m).rounded_rectangle([a[0] * SS, a[1] * SS, b[0] * SS, b[1] * SS], radius=int(self.R * s * SS), fill=255)
        lay.paste(sh, (0, 0), Image.fromarray(np.minimum(np.asarray(m), np.asarray(sh.split()[-1])).astype(np.uint8)))
    def screen(self, lay, cam, img, inset, alpha):
        """img: RGBA painted at SS scale for the rect (x0+inset[0], y0+inset[1], x1-inset[2], y1-inset[3])."""
        s = cam[0]; tl = T((self.x0 + inset[0], self.y0 + inset[1]), cam)
        im = img.resize((max(2, int(img.width * s)), max(2, int(img.height * s))), Image.BILINEAR)
        lay.alpha_composite(setalpha(im, alpha), (int(tl[0] * SS), int(tl[1] * SS)))
    def screen_size(self, inset): return (int((self.x1 - self.x0 - inset[0] - inset[2]) * SS), int((self.y1 - self.y0 - inset[1] - inset[3]) * SS))

ENGINE_PATH = Curve([(392, 748), (470, 752), (628, 790), (640, 862), (470, 930), (446, 1000), (520, 1060), (628, 1100),
                     (640, 1175), (470, 1240), (455, 1300), (560, 1318), (688, 1322)])

def spr_box(w, h, fill=None, outline=None, r=8, k=SS):
    im = Image.new('RGBA', (int(w * k), int(h * k)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, int(w * k) - 1, int(h * k) - 1], radius=int(r * k), fill=fill or rgba(mixc(INK, LIN, 0.22), 1), outline=outline or rgba(mixc(LIN, MUT, 0.4), 1), width=int(2 * k))
    return im, d
def spr_laptop(k=SS):
    w, h = 150, 100; im = Image.new('RGBA', (w * k, h * k), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([14 * k, 0, (w - 14) * k, 78 * k], radius=6 * k, fill=rgba(shade(INK, 0.6), 1), outline=rgba(mixc(LIN, MUT, 0.4), 1), width=2 * k)
    d.rectangle([22 * k, 8 * k, (w - 22) * k, 70 * k], fill=rgba(mixc(INK, LIN, 0.25), 1))
    for i, ww in enumerate([0.7, 0.5, 0.62]): d.line([30 * k, (20 + i * 14) * k, (30 + ww * 86) * k, (20 + i * 14) * k], fill=rgba(MUT, 0.6), width=int(2.4 * k))
    d.polygon([(0, 84 * k), (w * k, 84 * k), ((w - 10) * k, 96 * k), (10 * k, 96 * k)], fill=rgba(mixc(LIN, MUT, 0.35), 1))
    return im
def spr_web(k=SS, w=172, h=128):
    im, d = spr_box(w, h, r=10)
    d.line([(0, 26 * k), (w * k, 26 * k)], fill=rgba(LIN, 1), width=2 * k)
    for i in range(3): d.ellipse([(12 + i * 14) * k, 9 * k, (20 + i * 14) * k, 17 * k], fill=rgba(MUT, 0.7))
    d.rounded_rectangle([14 * k, 40 * k, (14 + w * 0.35) * k, (h - 28) * k], radius=6 * k, fill=rgba(LIN, 0.9))
    for i, ww in enumerate([0.9, 0.7, 0.8, 0.5]): d.line([(w * 0.45 + 14) * k, (46 + i * 15) * k, (w * 0.45 + 14 + ww * w * 0.4) * k, (46 + i * 15) * k], fill=rgba(MUT, 0.6), width=int(2.4 * k))
    return im
def spr_server(k=SS, w=92, h=150):
    im = Image.new('RGBA', (w * k + 4, h * k + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([2, 2, 2 + w * k, 2 + h * k], fill=rgba(shade(INK, 0.55), 1), outline=rgba(LIN, 1), width=k)
    for i in range(int((h - 20) / 22)):
        y = 2 + (14 + i * 22) * k; d.rectangle([2 + 8 * k, y, 2 + w * k - 8 * k, y + 14 * k], outline=rgba(LIN, 0.9), width=k)
    return im
def spr_phone(k=SS, w=54, h=100, bubble=False):
    im = Image.new('RGBA', (w * k, h * k), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w * k - 1, h * k - 1], radius=9 * k, fill=rgba(mixc(INK, LIN, 0.25), 1), outline=rgba(mixc(LIN, MUT, 0.3), 1), width=k)
    d.rounded_rectangle([5 * k, 8 * k, (w - 5) * k, (h - 8) * k], radius=5 * k, fill=rgba(shade(INK, 0.6), 1))
    if bubble: d.rounded_rectangle([10 * k, 20 * k, (w - 12) * k, 40 * k], radius=5 * k, fill=rgba(LIN, 1))
    return im
def spr_doc(title, k=SS, w=110, h=140, lines=7):
    im = Image.new('RGBA', (w * k + 30, h * k + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([20, 22, 20 + w * k, 22 + h * k], fill=(0, 0, 0, 80)); im = im.filter(ImageFilter.GaussianBlur(6)); d = ImageDraw.Draw(im)
    d.rectangle([15, 15, 15 + w * k, 15 + h * k], fill=rgba(OFF, 0.94))
    d.text((15 + 10 * k, 15 + 9 * k), title, font=MON(int(8.5 * k)), fill=rgba(INK, 0.85))
    d.line([15 + 10 * k, 15 + 24 * k, 15 + (w - 10) * k, 15 + 24 * k], fill=rgba(MUT, 0.9), width=k)
    rr = np.random.default_rng(len(title))
    for i in range(lines):
        y = 15 + (36 + i * 13) * k; d.line([15 + 10 * k, y, 15 + 10 * k + rr.uniform(0.4, 0.92) * (w - 20) * k, y], fill=rgba(MUT, 0.75), width=int(2.2 * k))
    return im
def spr_tag(label, k=SS, dotc=DEEP):
    f = MON(15 * k); tw = ImageDraw.Draw(Image.new('RGBA', (1, 1))).textlength(label, font=f)
    w, h = int(tw + 34 * k), 40 * k
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=8 * k, fill=rgba(OFF, 0.95))
    d.ellipse([10 * k, 16 * k, 18 * k, 24 * k], fill=rgba(dotc, 1)); d.text((24 * k, 10 * k), label, font=f, fill=rgba(INK, 0.9))
    return im
def spr_db(k=SS, w=110, h=120):
    im = Image.new('RGBA', (w * k, h * k), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i in range(3):
        y = (16 + i * 34) * k
        d.rectangle([4 * k, y, (w - 4) * k, y + 34 * k], fill=rgba(mixc(INK, LIN, 0.35), 1))
        d.ellipse([4 * k, y + 22 * k, (w - 4) * k, y + 46 * k], fill=rgba(mixc(INK, LIN, 0.35), 1), outline=rgba(MUT, 0.7), width=k)
        d.ellipse([4 * k, y - 12 * k, (w - 4) * k, y + 12 * k], fill=rgba(mixc(INK, LIN, 0.55), 1), outline=rgba(MUT, 0.8), width=k)
    return im
def spr_lock(k=SS, s=1.0, c=OFF):
    w, h = int(40 * s), int(48 * s); im = Image.new('RGBA', (w * k, h * k), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.arc([8 * s * k, 0, 32 * s * k, 30 * s * k], 180, 360, fill=rgba(c, 1), width=int(4 * s * k))
    d.line([8 * s * k, 15 * s * k, 8 * s * k, 22 * s * k], fill=rgba(c, 1), width=int(4 * s * k)); d.line([32 * s * k - 1, 15 * s * k, 32 * s * k - 1, 22 * s * k], fill=rgba(c, 1), width=int(4 * s * k))
    d.rounded_rectangle([2 * s * k, 20 * s * k, 38 * s * k, 46 * s * k], radius=int(5 * s * k), fill=rgba(c, 1))
    d.ellipse([17 * s * k, 28 * s * k, 23 * s * k, 34 * s * k], fill=rgba(INK, 1))
    return im
def spr_card(title, sub, w=420, k=SS, ok=True):
    im, d = spr_box(w, 92, fill=rgba(SURF, 0.95), outline=rgba(LIN, 1), r=10)
    cx, cy = 36 * k, 46 * k
    if ok: d.ellipse([cx - 9 * k, cy - 9 * k, cx + 9 * k, cy + 9 * k], fill=rgba(VIO, 1))
    else: d.ellipse([cx - 9 * k, cy - 9 * k, cx + 9 * k, cy + 9 * k], outline=rgba(MUT, 1), width=2 * k)
    d.text((70 * k, 14 * k), title, font=F(FD + 'InterDisplay-Medium.otf', 32 * k), fill=rgba(TXT if ok else MUT, 1))
    x = 70 * k
    for ch in sub: d.text((x, 58 * k), ch, font=MON(18 * k), fill=rgba(VIO if ok else MUT, 1)); x += d.textlength(ch, font=MON(18 * k)) + 18 * k * 0.12
    return im

# ---------------- camera ----------------
C0 = (540.0, 1030.0)
def T(p, cam):
    s, ox, oy = cam
    return (C0[0] + (p[0] - C0[0]) * s + ox, C0[1] + (p[1] - C0[1]) * s + oy)

# ---------------- wordmark ----------------
def _quad(p0, c, p1, n=14): return [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * c[0] + u * u * p1[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * c[1] + u * u * p1[1]) for u in np.linspace(0, 1, n)]
def _circ(cx, cy, r_, n=64): return [(cx + r_ * math.cos(-math.pi / 2 - a), cy + r_ * math.sin(-math.pi / 2 - a)) for a in np.linspace(0, TAU, n)]
_N = [(24, 78), (24, 31)] + _quad((24, 31), (24, 20), (32, 28))[1:] + [(68, 72)] + _quad((68, 72), (76, 80), (76, 69))[1:] + [(76, 22)]
STROKES = [[(x + 2, y) for x, y in s] for s in [_N, _circ(108, 58, 20), _circ(158, 58, 20), [(178, 22), (178, 78)], _circ(210, 58, 20),
           [(230, 40), (230, 70)] + _quad((230, 70), (230, 78), (238, 78))[1:], [(250, 22), (250, 70)] + _quad((250, 70), (250, 78), (258, 78))[1:]]]
WK = 3.25
def wm(p): return (540 + (p[0] - 139.5) * WK, 900 + (p[1] - 50) * WK)
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

# ---------------- text helpers ----------------
def spaced(dr, xy, s, font, fill, sp=0.12, anchor='l'):
    x, y = xy; ws = [dr.textlength(c, font=font) + font.size * sp for c in s]; tot = sum(ws) - font.size * sp
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

# ---------------- context passed to episodes ----------------
class K:
    pass

def make_ctx(ep_num):
    tim = json.load(open(f'/home/claude/decoded/ep{ep_num:02d}_timing.json'))
    c = K(); c.SUBS, c.SENTS, c.VEND = tim['subs'], tim['sents'], tim['voice_end']
    c.DUR = round(c.VEND + 3.2, 2)
    chs = sorted(set(s['ch'] for s in c.SENTS))
    c.CH = [0.0] + [min(s['start'] for s in c.SENTS if s['ch'] == ch) - 0.2 for ch in chs[1:]] + [c.VEND]
    c.S = lambda i: c.SENTS[i]['start']; c.E = lambda i: c.SENTS[i]['end']
    def sub_t(prefix):
        for s in c.SUBS:
            if s['text'].startswith(prefix): return s['start']
        raise KeyError(prefix)
    c.sub_t = sub_t
    return c

# drawing helpers bound per frame
def dot(dr, p, r_, col, a, k=SS): dr.ellipse([(p[0] - r_) * k, (p[1] - r_) * k, (p[0] + r_) * k, (p[1] + r_) * k], fill=rgba(col, a))
def ring(dr, p, r_, col, a, w, k=SS): dr.ellipse([(p[0] - r_) * k, (p[1] - r_) * k, (p[0] + r_) * k, (p[1] + r_) * k], outline=rgba(col, a), width=max(1, int(w * k)))
def paste(lay, spr, center, scale, alpha, ang=0):
    if alpha <= 0.005 or scale <= 0.01: return
    im = spr.resize((max(2, int(spr.width * scale)), max(2, int(spr.height * scale))), Image.BILINEAR)
    if ang: im = im.rotate(ang, resample=Image.BICUBIC, expand=True)
    lay.alpha_composite(setalpha(im, alpha), (int(center[0] * SS - im.width / 2), int(center[1] * SS - im.height / 2)))
def path_line(f, pts, a, width=2.2, col=VIO):
    if a <= 0 or len(pts) < 2: return
    s = f.s
    f.dr.line([(x * SS, y * SS) for x, y in pts], fill=rgba(col, 0.85 * a), width=max(1, int(width * s * SS)), joint='curve')
    f.gd.line(pts, fill=rgba(VIO, 0.7 * a), width=max(1, int(6 * s))); f.wd.line(pts, fill=rgba(VIO, 0.3 * a), width=max(1, int(14 * s)))
def line(f, p, q, a, width=1.6, col=VIO, glow=True):
    if a <= 0: return
    f.dr.line([(p[0] * SS, p[1] * SS), (q[0] * SS, q[1] * SS)], fill=rgba(col, a), width=max(1, int(width * SS)))
    if glow: f.gd.line([p, q], fill=rgba(VIO, 0.45 * a), width=4)
def faded_line(f, p0, p1, a, w=1.4, n=24, col=VIO):
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n; al = a * math.sin(math.pi * (u0 + u1) / 2) ** 0.8
        f.dr.line([(lerp(p0[0], p1[0], u0) * SS, lerp(p0[1], p1[1], u0) * SS), (lerp(p0[0], p1[0], u1) * SS, lerp(p0[1], p1[1], u1) * SS)], fill=rgba(col, al), width=max(1, int(w * SS)))
def dashed(f, pts, a, w=1.6, col=OFF, on=10, off=9):
    if a <= 0 or len(pts) < 2: return
    acc, draw_on, sp = 0.0, True, [pts[0]]
    for p, q in zip(pts, pts[1:]):
        acc += math.dist(p, q); sp.append(q)
        if acc >= (on if draw_on else off):
            if draw_on: f.dr.line([(x * SS, y * SS) for x, y in sp], fill=rgba(col, a), width=max(1, int(w * SS)))
            draw_on = not draw_on; acc = 0; sp = [q]
    if draw_on and len(sp) > 1: f.dr.line([(x * SS, y * SS) for x, y in sp], fill=rgba(col, a), width=max(1, int(w * SS)))
def particles(f, curve, a, n=14, speed=1.6, size=2.4):
    for k_ in range(n):
        sp = ((k_ / n) + f.t / speed) % 1.0
        p = f.T(curve.at(sp)); aa = math.sin(math.pi * sp) ** 0.5 * a
        dot(f.dr, p, size * f.s, PART, aa); f.gd.ellipse([p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7], fill=rgba(VIO, 0.55 * aa))
def packets(f, curve, a, n=6, speed=2.2, kind='open', grow=1.0):
    s = f.s
    for k_ in range(n):
        sp = ((k_ / n) + f.t / speed) % 1.0
        if sp > grow: continue
        p = f.T(curve.at(sp)); aa = math.sin(math.pi * sp) ** 0.5 * a; dr = f.dr
        if kind == 'lock':
            r_ = 5.5 * s
            dr.rounded_rectangle([(p[0] - r_) * SS, (p[1] - r_ * 0.6) * SS, (p[0] + r_) * SS, (p[1] + r_) * SS], radius=int(2 * SS), fill=rgba(OFF, aa))
            dr.arc([(p[0] - r_ * 0.6) * SS, (p[1] - r_ * 1.5) * SS, (p[0] + r_ * 0.6) * SS, (p[1] - r_ * 0.1) * SS], 180, 360, fill=rgba(OFF, aa), width=int(1.6 * SS))
        elif kind == 'dark':
            dot(dr, p, 7 * s, shade(INK, 0.4), aa); ring(dr, p, 7 * s, DEEP, aa, 1.6)
        else:
            dr.rectangle([(p[0] - 9 * s) * SS, (p[1] - 6 * s) * SS, (p[0] + 9 * s) * SS, (p[1] + 6 * s) * SS], fill=rgba(OFF, aa))
        f.gd.ellipse([p[0] - 9, p[1] - 9, p[0] + 9, p[1] + 9], fill=rgba(VIO if kind != 'dark' else DEEP, 0.5 * aa))
def tube(f, curve, a, grow=1.0):
    if a <= 0 or grow <= 0: return
    pts = [f.T(p) for p in curve.part(0, grow)]; s = f.s
    f.wd.line(pts, fill=rgba(VIO, 0.22 * a), width=int(40 * s)); f.gd.line(pts, fill=rgba(VIO, 0.16 * a), width=int(22 * s))
    for side in (-1, 1):
        edge = []
        for p, q in zip(pts, pts[1:] + [pts[-1]]):
            dx, dy = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dy) or 1
            edge.append((p[0] - side * dy / L * 11 * s, p[1] + side * dx / L * 11 * s))
        edge[-1] = (pts[-1][0] + (edge[-2][0] - pts[-2][0]), pts[-1][1] + (edge[-2][1] - pts[-2][1]))
        f.dr.line([(x * SS, y * SS) for x, y in edge], fill=rgba(VIO, 0.8 * a), width=int(1.6 * s * SS), joint='curve')
def node(f, p, a, lit=0.0, ts=None):
    """engine-style node: dot + ring + glow, ripple when ts given"""
    if a <= 0: return
    s = f.s
    dot(f.dr, p, (4.5 + 2.5 * lit) * s, mixc((200, 192, 255), OFF, lit), a)
    ring(f.dr, p, (11 + 5 * lit) * s, VIO, (0.55 + 0.45 * lit) * a, 1.6)
    f.gd.ellipse([p[0] - 18 * s, p[1] - 18 * s, p[0] + 18 * s, p[1] + 18 * s], fill=rgba(VIO, (0.5 + 0.5 * lit) * a))
    if ts is not None:
        pr = (f.t - ts) / 0.9
        if 0 < pr < 1: ring(f.dr, p, (16 + 40 * pr) * s, VIO, 0.6 * (1 - pr) * a, 1.4)
def dark_node(f, p, a, r_=28):
    if a <= 0: return
    s = f.s
    f.dr.ellipse([(p[0] - r_ * s) * SS, (p[1] - r_ * s) * SS, (p[0] + r_ * s) * SS, (p[1] + r_ * s) * SS], fill=rgba(shade(INK, 0.4), a), outline=rgba(DEEP, a), width=3 * SS)
    ring(f.dr, p, (r_ + 14) * s + 3 * math.sin(f.t * 5), DEEP, 0.5 * a, 1.4)
    f.wd.ellipse([p[0] - 60, p[1] - 60, p[0] + 60, p[1] + 60], fill=rgba(DEEP, 0.55 * a))
def burst(f, p, t0, a=1.0, n=10, rad=46):
    bt = f.t - t0
    if 0 < bt < 0.7:
        for q in range(n):
            ang = q / n * TAU; r_ = 6 + rad * ease(bt / 0.7)
            dot(f.dr, (p[0] + r_ * math.cos(ang), p[1] + r_ * math.sin(ang) * 0.8), 2.0, PART, (1 - bt / 0.7) * a)
def label(f, p, title, sub, al, anchor='l'):
    if al <= 0: return
    if title: spaced(f.td, (p[0], p[1]), title, MONO, rgba(TXT, al), 0.12, anchor)
    if sub: spaced(f.td, (p[0], p[1] + (34 if title else 0)), sub, MONOS, rgba(VIO, al), 0.12, anchor)
def mlabel(f, p, s_, al, col=TXT, font=None, anchor='m'):
    if al > 0: spaced(f.td, p, s_, font or MONO, rgba(col, al), 0.12, anchor)
def cards(f, items, until, x0=210, x1=870):
    """decision cards (style 'Des fichiers à la décision'): items = (y, title, sub, t_on, ok)"""
    for (cy, title, sub, ts, ok) in items:
        ca = seg(f.t, ts, ts + 0.45) * fade(f.t, ts, until, 0.01, 0.5)
        if ca <= 0: continue
        off = (1 - seg(f.t, ts, ts + 0.45)) * 16; td = f.td
        td.rounded_rectangle([x0, cy + off, x1, cy + 92 + off], radius=10, fill=rgba(SURF, 0.94 * ca), outline=rgba(LIN, ca), width=2)
        cx, cyy = x0 + 36, cy + 46 + off
        if ok: td.ellipse([cx - 9, cyy - 9, cx + 9, cyy + 9], fill=rgba(VIO, ca))
        else:
            td.ellipse([cx - 9, cyy - 9, cx + 9, cyy + 9], outline=rgba(MUT, ca), width=2)
            td.line([cx - 5, cyy - 5, cx + 5, cyy + 5], fill=rgba(MUT, ca), width=2); td.line([cx - 5, cyy + 5, cx + 5, cyy - 5], fill=rgba(MUT, ca), width=2)
        td.text((x0 + 70, cy + 14 + off), title, font=CARDF, fill=rgba(TXT if ok else MUT, ca))
        spaced(td, (x0 + 70, cy + 58 + off), sub, MONOS, rgba(VIO if ok else MUT, ca), 0.12)

# ---------------- frame ----------------
def build(ep_num):
    sys.path.insert(0, '/home/claude/decoded')
    from scripts import EP
    E = EP[ep_num]; c = make_ctx(ep_num)
    mod = importlib.import_module(f'eps.ep{ep_num:02d}')
    st = mod.setup(c)          # episode builds sprites/geometry once
    WM0, WM1 = c.VEND + 0.35, c.VEND + 1.55
    def frame(i):
        t = i / FPS
        cam = mod.camera(c, t) if hasattr(mod, 'camera') else (1.0 + 0.012 * math.sin(TAU * t / 24), 7 * math.sin(TAU * t / 24), 5 * math.sin(2 * TAU * t / 24))
        f = K(); f.t = t; f.cam = cam; f.s = cam[0]; f.T = lambda p: T(p, cam); f.c = c; f.st = st
        f.lay = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0)); f.dr = ImageDraw.Draw(f.lay)
        f.glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); f.gd = ImageDraw.Draw(f.glow)
        f.wide = Image.new('RGBA', (W, H), (0, 0, 0, 0)); f.wd = ImageDraw.Draw(f.wide)
        f.scene = seg(t, 0.0, 0.8) * (1 - seg(t, c.VEND - 0.15, c.VEND + 0.45))
        for (x, y, rr_, a, ph, m) in DUST:
            dot(f.dr, (x + 18 * math.sin(TAU * t / 24 * m + ph), y + 26 * math.sin(TAU * t / 24 + ph * 1.3)), rr_, MUT, a)
        mod.scene(f)
        # wordmark close
        if t > WM0 - 0.05:
            drawn = (t - WM0) / (WM1 - WM0) * TOT; acc = 0
            na = seg(t, WM0, WM0 + 0.25); nc = wm((26, 78))
            for st_, L in zip(STROKES, SLEN):
                frac = min(max((drawn - acc) / L, 0), 1); acc += L
                pp = [wm(p) for p in partial(st_, frac)]
                if len(pp) > 1:
                    f.dr.line([(x * SS, y * SS) for x, y in pp], fill=rgba(OFF, 1), width=int(3.2 * WK * SS), joint='curve')
                    for e in (pp[0], pp[-1]): dot(f.dr, e, 1.6 * WK, OFF, 1)
            if na > 0: dot(f.dr, nc, 7.86 * WK, OFF, na); dot(f.dr, nc, 5.14 * WK, INK, na)
            da = seg(t, WM1 + 0.05, WM1 + 0.4)
            if da > 0:
                dc = wm((78, 22 - 10 * (1 - da))); dot(f.dr, dc, 8 * WK * (0.6 + 0.4 * da), VIO, da)
                f.wd.ellipse([dc[0] - 70, dc[1] - 70, dc[0] + 70, dc[1] + 70], fill=rgba(VIO, 0.8 * da)); f.gd.ellipse([dc[0] - 34, dc[1] - 34, dc[0] + 34, dc[1] + 34], fill=rgba(VIO, 0.7 * da))
        lay = f.lay.resize((W, H), Image.LANCZOS)
        out = BG.copy()
        for g_, rad, k_, dn in [(f.wide, 38, 0.9, 4), (f.glow, 10, 1.0, 2)]:
            ga = np.asarray(g_.resize((W // dn, H // dn), Image.BILINEAR).filter(ImageFilter.GaussianBlur(rad / dn)).resize((W, H), Image.BILINEAR), np.float32)
            out = out + ga[..., :3] * (ga[..., 3:] / 255) * k_
        l = np.asarray(lay, np.float32); la = l[..., 3:] / 255
        out = out * (1 - la) + l[..., :3] * la
        im = Image.fromarray(np.clip(out + DITHER, 0, 255).astype(np.uint8)).convert('RGBA')
        f.tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); f.td = ImageDraw.Draw(f.tx)
        if hasattr(mod, 'text'): mod.text(f)
        td = f.td
        ga_ = seg(t, 0.2, 0.8) * (1 - seg(t, c.VEND - 0.2, c.VEND + 0.3))
        col = (245, 243, 251, int(64 * ga_)); Ln, mm = 26, 40
        for (x, y, sx_, sy_) in [(mm, mm, 1, 1), (W - mm, mm, -1, 1), (mm, H - mm, 1, -1), (W - mm, H - mm, -1, -1)]:
            td.line((x, y, x + sx_ * Ln, y), fill=col, width=2); td.line((x, y, x, y + sy_ * Ln), fill=col, width=2)
        spaced(td, (72, 150), 'NODAL — DECODED · ' + E['topic'], MONOT, (245, 243, 251, int(150 * ga_)))
        for n_, parts in enumerate(E['HEADS']):
            a0 = c.CH[n_] + (0.3 if n_ == 0 else 0.1); a1 = c.CH[n_ + 1] - (0.1 if n_ + 1 < len(c.CH) - 1 else 0.1)
            al = fade(t, a0, a1, 0.45, 0.4)
            if al > 0: rich(td, 80, 300 + (1 - ease((t - a0) / 0.5)) * 18, parts, HEAD, al)
        for si, sb in enumerate(c.SUBS):
            nxt = c.SUBS[si + 1]['start'] if si + 1 < len(c.SUBS) else 1e9
            al = fade(t, sb['start'] - 0.04, min(sb['end'] + 0.12, nxt - 0.04), 0.08, 0.06)
            if al <= 0: continue
            lines, cur = [], ''
            for w_ in sb['text'].split(' '):
                nx = (cur + ' ' + w_).strip()
                if td.textlength(nx, font=SUBT) > 880 and cur: lines.append(cur); cur = w_
                else: cur = nx
            lines.append(cur)
            lh = 54; bh = len(lines) * lh + 26; y0 = getattr(mod, 'SUB_Y', 1505)
            mw = max(td.textlength(ln, font=SUBT) for ln in lines)
            td.rounded_rectangle([540 - mw / 2 - 24, y0, 540 + mw / 2 + 24, y0 + bh], radius=12, fill=rgba(SURF, 0.82 * al))
            for j, ln in enumerate(lines):
                lw_ = td.textlength(ln, font=SUBT); td.text((540 - lw_ / 2, y0 + 10 + j * lh), ln, font=SUBT, fill=rgba(TXT, al))
        e = seg(t, WM1 + 0.2, WM1 + 0.8)
        if e > 0:
            ty = wm((0, 86))[1] + 80
            rich(td, 0, ty, [('Where everything', 0), ('connects.', 1)], SUBF, e * 0.9, center=True)
            spaced(td, (W / 2, ty + 80), f'NODAL — DECODED #{ep_num:02d}', MONO, VIO + (int(255 * e),), anchor='m')
        im.alpha_composite(f.tx)
        return im.convert('RGB')
    return c, frame

if __name__ == '__main__':
    ep = int(sys.argv[1]); c, frame = build(ep)
    if '--still' in sys.argv:
        for ts in sys.argv[sys.argv.index('--still') + 1:]:
            frame(int(round(float(ts) * FPS))).save(f'/home/claude/decoded/st/ep{ep:02d}_{ts}.png')
        sys.exit()
    if '--info' in sys.argv: print(c.DUR, int(c.DUR * FPS), c.VEND); sys.exit()
    OUT = sys.argv[2]; a, b = int(sys.argv[3]), int(sys.argv[4])
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
    for i in range(a, b):
        p.stdin.write(frame(i).tobytes())
    p.stdin.close(); p.wait(); print('done', OUT, flush=True)

def floor(f, cx, cy, rx, ry, a):
    if a <= 0: return
    fc = f.T((cx, cy)); s = f.s
    f.wd.ellipse([fc[0] - rx * s, fc[1] - ry * s, fc[0] + rx * s, fc[1] + ry * s], outline=rgba(VIO, 0.55 * a), width=6)
    f.dr.ellipse([(fc[0] - rx * s) * SS, (fc[1] - ry * s) * SS, (fc[0] + rx * s) * SS, (fc[1] + ry * s) * SS], outline=rgba(VIO, 0.45 * a), width=2 * SS)
def engine_path(f, a, lit_from=None, nodes_t=None):
    """S-curve + particles + 4 nodes + ports inside the tower (same as 'the engine')."""
    s = f.s; pts = [f.T(p) for p in ENGINE_PATH.pts]
    path_line(f, pts, a)
    for k_ in range(42):
        sp = ((k_ / 42) + f.t / 3.0) % 1.0
        p = f.T(ENGINE_PATH.at(sp)); aa = math.sin(math.pi * sp) ** 0.5 * a
        dot(f.dr, p, 2.4 * s, PART, aa); f.gd.ellipse([p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7], fill=rgba(VIO, 0.6 * aa))
    for n_, sv in enumerate((0.2, 0.4, 0.6, 0.8)):
        ts = nodes_t[n_] if nodes_t else None
        lit = fade(f.t, ts, 1e9, 0.35, 0.6) if ts is not None else 0.0
        node(f, f.T(ENGINE_PATH.at(sv)), a, lit, ts)
    for port in (ENGINE_PATH.pts[0], ENGINE_PATH.pts[-1]):
        p = f.T(port); b = 0.6 * a
        ring(f.dr, p, 8 * s, OFF, 0.8 * b, 1.6); dot(f.dr, p, 3.5 * s, OFF, b)
        f.wd.ellipse([p[0] - 34 * s, p[1] - 34 * s, p[0] + 34 * s, p[1] + 34 * s], fill=rgba(VIO, 0.6 * b))
def tower():
    return Hero(390, 690, 690, 1370, 42, -20, 0, 2.8, caps=True)
