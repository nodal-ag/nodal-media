from kit import *

PH = None
INS = (16, 30, 16, 30)
def setup(c):
    global PH
    PH = Hero(400, 700, 680, 1290, 34, -18, radius=34, k=2.6)
    st = K()
    st.SRC = [((170, 610), spr_tag('VIDEO')), ((165, 760), spr_tag('VOICE NOTE')), ((175, 910), spr_tag('INTERVIEW'))]
    st.AI = (900, 720)
    st.CV = [Curve([(240, 610), (380, 540), (600, 520), (800, 590), (875, 700)]), Curve([(255, 760), (330, 620), (560, 560), (790, 620), (872, 710)]),
             Curve([(255, 910), (320, 720), (500, 610), (780, 650), (870, 722)])]
    st.OUT = Curve([(900, 760), (880, 860), (760, 880), (684, 900)])
    st.BANK = (905, 1180)
    st.TOB = Curve([(684, 1100), (780, 1100), (840, 1160), (870, 1180)])
    st.TAGS = [(spr_tag('URGENT'), (215, 1070)), (spr_tag('CONFIDENTIAL'), (190, 1160)), (spr_tag('FRIDAY · 6 PM'), (200, 1250))]
    st.CARDS = [(1060, 'Call back on a known number', 'BEFORE ANY TRANSFER', c.sub_t('no transfer') + 0.2, True),
                (1175, 'A code word', 'MANAGEMENT · FINANCE', c.sub_t('and a code') + 0.2, True),
                (1290, 'A transfer on one phone call', 'NEVER', c.sub_t('Send this') + 0.0, False)]
    return st

def wave(f, center, a, w=150, h=34, ph=0.0):
    pts = [(center[0] - w / 2 + i * w / 60, center[1] + h / 2 * math.sin(i * 0.5 + f.t * 8 + ph) * math.sin(math.pi * i / 60) * (0.5 + 0.5 * math.sin(i * 0.23 + f.t * 3))) for i in range(61)]
    f.dr.line([(x * SS, y * SS) for x, y in pts], fill=rgba(VIO, a), width=int(2 * SS)); f.gd.line(pts, fill=rgba(VIO, 0.6 * a), width=4)

def screen_img(f):
    c, t = f.c, f.t; w, h = PH.screen_size(INS); k = SS
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    call = seg(t, c.CH[2] - 0.2, c.CH[2] + 0.3) + seg(t, 0.3, 0.9) * (1 - seg(t, c.CH[1] - 0.2, c.CH[1] + 0.3))
    call = min(call, 1)
    d.text((16 * k, 14 * k), '18:02', font=UI(13 * k), fill=rgba(MUT, 0.9))
    if call > 0:
        d.text((w / 2 - d.textlength('Incoming call', font=UI(15 * k)) / 2, 60 * k), 'Incoming call', font=UI(15 * k), fill=rgba(MUT, call))
        nm = 'The Director'; d.text((w / 2 - d.textlength(nm, font=UIB(26 * k)) / 2, 86 * k), nm, font=UIB(26 * k), fill=rgba(OFF, call))
        r_ = 46 * k; cx, cy = w / 2, 230 * k
        d.ellipse([cx - r_, cy - r_, cx + r_, cy + r_], outline=rgba(VIO, call), width=int(2 * k))
        for q in range(3):
            pr = ((t * 0.8) + q / 3) % 1; rr = r_ + pr * 40 * k
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=rgba(VIO, call * (1 - pr) * 0.6), width=int(1.4 * k))
        d.text((cx - d.textlength('D', font=UIB(36 * k)) / 2, cy - 24 * k), 'D', font=UIB(36 * k), fill=rgba(OFF, call))
        for i, (x, col) in enumerate([(w * 0.27, DEEP), (w * 0.73, VIO)]):
            d.ellipse([x - 26 * k, h - 110 * k, x + 26 * k, h - 58 * k], fill=rgba(col, call))
    return im

def scene(f):
    c, t, st, s = f.c, f.t, f.st, f.s
    dim = 1 - 0.65 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5)
    ha = f.scene * dim
    floor(f, 556, 1318, 250, 40, ha)
    a1 = fade(t, c.CH[1] - 0.1, c.CH[2] + 0.2, 0.5, 0.6) * f.scene
    if a1 > 0:
        for n_, ((pos, spr), cv) in enumerate(zip(st.SRC, st.CV)):
            ts = c.sub_t('a video') + n_ * 0.6
            ap = seg(t, ts - 0.2, ts + 0.3) * a1
            paste(f.lay, spr, f.T(pos), s, ap)
            g = seg(t, ts, ts + 0.8); path_line(f, [f.T(q) for q in cv.part(0, g)], ap * 0.8)
            if g >= 1: particles(f, cv, ap, 8, 1.3)
        aa = seg(t, c.sub_t('a video') + 1.4, c.sub_t('a video') + 1.9) * a1
        node(f, f.T(st.AI), aa, fade(t, c.sub_t('An AI'), 1e9, 0.3, 0.1), c.sub_t('An AI'))
        cp = seg(t, c.sub_t('An AI'), c.sub_t('An AI') + 0.8) * a1
        path_line(f, [f.T(q) for q in st.OUT.part(0, cp)], cp, col=DEEP)
        wave(f, f.T((900, 820)), cp * 0.9, 120, 26)
    PH.draw(f.lay, f.cam, ha); PH.screen(f.lay, f.cam, screen_img(f), INS, ha); PH.sheen(f.lay, f.cam, t, ha)
    a2 = fade(t, c.CH[2], c.CH[3] + 0.6, 0.5, 0.6) * f.scene
    if a2 > 0:
        wave(f, f.T((540, 640)), a2 * 0.9, 200, 40, 1.0)
        for n_, (spr, pos) in enumerate(st.TAGS):
            tt = [c.sub_t('The tone'), c.sub_t('and he insists'), c.S(3)][n_] if n_ < 2 else c.S(3) + 0.3
            paste(f.lay, spr, f.T(pos), s, seg(t, tt, tt + 0.4) * a2)
        g = seg(t, c.sub_t('The tone') + 0.6, c.sub_t('The tone') + 1.4)
        cut = seg(t, c.sub_t('no transfer'), c.sub_t('no transfer') + 0.6)
        path_line(f, [f.T(q) for q in st.TOB.part(0, g * (1 - 0.45 * cut))], a2 * (1 - 0.5 * cut))
        if g >= 1 and cut < 1: particles(f, st.TOB, a2 * (1 - cut), 6, 1.0)
        bp = f.T(st.BANK); ring(f.dr, bp, 34 * s, VIO, a2 * g, 2); dot(f.dr, bp, 8 * s, OFF, a2 * g)
        if cut > 0:
            m = f.T(st.TOB.at(0.6))
            for dx_ in (-8, 8):
                f.dr.line([((m[0] + dx_ - 7) * SS, (m[1] + 14) * SS), ((m[0] + dx_ + 7) * SS, (m[1] - 14) * SS)], fill=rgba(OFF, cut * a2), width=3 * SS)

def text(f):
    c, t, st = f.c, f.t, f.st
    a1 = fade(t, c.sub_t('An AI'), c.CH[2] + 0.2, 0.4, 0.6)
    p = f.T(st.AI); label(f, (1036, p[1] + 150), 'AI', 'COPIES THE VOICE', a1, 'r')
    a2 = fade(t, c.sub_t('The tone') + 1.2, c.CH[3] + 0.6, 0.4, 0.6)
    p = f.T(st.BANK); label(f, (1036, p[1] + 50), 'TRANSFER', 'LARGE AMOUNT', a2, 'r')
    cards(f, st.CARDS, c.VEND - 0.05)
