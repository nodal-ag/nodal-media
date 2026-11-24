from kit import *

LAP = None
INS = (14, 14, 14, 14)
def setup(c):
    global LAP
    LAP = Hero(290, 800, 790, 1130, 34, -16, radius=14, k=2.4, base='laptop')
    st = K()
    st.BR1 = (790, 900); st.BR2 = (290, 1050)
    st.ATT = [(960, 700), (990, 960), (940, 1250)]
    st.ZD = (120, 1260)
    st.ph = spr_phone(w=90, h=160)
    st.CARDS = [(1240, 'Update fast, everywhere', 'PHONES INCLUDED', c.sub_t('update fast') + 0.1, True),
                (1355, 'Automatic updates', 'TURN THEM ON TONIGHT', c.sub_t('Turn on') + 0.1, True)]
    return st

def screen_img(f):
    c, t = f.c, f.t; w, h = LAP.screen_size(INS); k = SS
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    done = seg(t, c.CH[4] + 0.2, c.CH[4] + 0.8)
    a = 1 - done
    bx0, by0, bx1, by1 = 70 * k, 50 * k, w - 70 * k, h - 50 * k
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=14 * k, fill=rgba(mixc(INK, LIN, 0.4), 1), outline=rgba(LIN, 1), width=int(2 * k))
    if a > 0:
        d.text((bx0 + 24 * k, by0 + 20 * k), 'Update available', font=UIB(24 * k), fill=rgba(OFF, a))
        d.text((bx0 + 24 * k, by0 + 58 * k), 'Security fix · restart required', font=UI(15 * k), fill=rgba(MUT, a))
        later = fade(t, 0.6, c.CH[1] + 0.2, 0.3, 0.4)
        d.rounded_rectangle([bx0 + 24 * k, by1 - 64 * k, bx0 + 150 * k, by1 - 24 * k], radius=20 * k, outline=rgba(mixc(MUT, VIO, later), a), width=int(2 * k), fill=rgba(mixc(INK, VIO, 0.35 * later), a))
        d.text((bx0 + 62 * k, by1 - 54 * k), 'Later', font=UIB(16 * k), fill=rgba(OFF, a))
        d.rounded_rectangle([bx1 - 170 * k, by1 - 64 * k, bx1 - 24 * k, by1 - 24 * k], radius=20 * k, fill=rgba(VIO, a))
        d.text((bx1 - 138 * k, by1 - 54 * k), 'Install now', font=UIB(16 * k), fill=rgba(OFF, a))
        u = seg(t, 0.3, 1.4); cx, cy = lerp(bx1, bx0 + 90 * k, u), lerp(by1 + 40 * k, by1 - 40 * k, u)
        d.polygon([(cx, cy), (cx, cy + 24 * k), (cx + 7 * k, cy + 18 * k), (cx + 17 * k, cy + 18 * k)], fill=rgba(OFF, a), outline=rgba(INK, a))
    if done > 0:
        tx = 'Up to date'; fB = UIB(28 * k)
        d.text(((w - d.textlength(tx, font=fB)) / 2, h / 2 - 20 * k), tx, font=fB, fill=rgba(OFF, done))
        cx, cy = w / 2, h / 2 - 70 * k
        d.ellipse([cx - 22 * k, cy - 22 * k, cx + 22 * k, cy + 22 * k], outline=rgba(VIO, done), width=int(3 * k))
        d.line([cx - 9 * k, cy, cx - 2 * k, cy + 8 * k, cx + 11 * k, cy - 9 * k], fill=rgba(VIO, done), width=int(3 * k))
    return im

def breach(f, p, a, closed):
    if a <= 0: return
    s = f.s; r_ = 18 * s * (1 - closed) + 4 * s
    f.dr.ellipse([(p[0] - r_) * SS, (p[1] - r_ * 1.6) * SS, (p[0] + r_) * SS, (p[1] + r_ * 1.6) * SS], fill=rgba(shade(INK, 0.3), a), outline=rgba(DEEP if closed < 1 else VIO, a), width=2 * SS)
    f.wd.ellipse([p[0] - 40, p[1] - 50, p[0] + 40, p[1] + 50], fill=rgba(DEEP, 0.5 * a * (1 - closed)))

def scene(f):
    c, t, st, s = f.c, f.t, f.st, f.s
    dim = 1 - 0.55 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5)
    ha = f.scene * dim
    floor(f, 556, 1190, 330, 40, ha)
    LAP.draw(f.lay, f.cam, ha); LAP.screen(f.lay, f.cam, screen_img(f), INS, ha); LAP.sheen(f.lay, f.cam, t, ha)
    closed = seg(t, c.CH[4] + 0.2, c.CH[4] + 1.0)
    b1 = fade(t, c.CH[2] + 0.2, 1e9, 0.4, 0.1) * f.scene
    breach(f, f.T(st.BR1), b1, closed)
    if b1 > 0 and closed < 1:
        for n_, q in enumerate(st.ATT):
            g = seg(t, c.sub_t('and hackers') + n_ * 0.3, c.sub_t('and hackers') + 0.8 + n_ * 0.3) * (1 - closed)
            if g <= 0: continue
            cv = Curve([q, ((q[0] + st.BR1[0]) / 2 + 30, (q[1] + st.BR1[1]) / 2), st.BR1])
            dark_node(f, f.T(q), g * b1, 18); path_line(f, [f.T(p) for p in cv.part(0, g)], g * b1 * 0.7, col=DEEP)
    b2 = fade(t, c.CH[3] + 0.3, 1e9, 0.4, 0.1) * f.scene
    breach(f, f.T(st.BR2), b2, closed)
    if b2 > 0 and closed < 1:
        cv = Curve([st.ZD, (170, 1180), (240, 1100), st.BR2])
        g = seg(t, c.CH[3] + 0.6, c.CH[3] + 1.4) * (1 - closed)
        dark_node(f, f.T(st.ZD), g, 20); path_line(f, [f.T(p) for p in cv.part(0, g)], g * 0.7, col=DEEP)
    pa = fade(t, c.sub_t('update fast') + 0.9, 1e9, 0.4, 0.1) * f.scene * dim
    if pa > 0:
        p = f.T((900, 1060)); paste(f.lay, st.ph, p, s, pa)
        cv_ = seg(t, c.sub_t('update fast') + 1.2, c.sub_t('update fast') + 1.8)
        ring(f.dr, (p[0], p[1] - 10 * s), 22 * s, VIO, pa * cv_, 2)

def text(f):
    c, t, st = f.c, f.t, f.st
    a = fade(t, c.CH[1] + 0.3, c.CH[2] + 0.2, 0.4, 0.5)
    label(f, (540, 1260), 'AN UPDATE FIXES A FLAW', '', a, 'm')
    a = fade(t, c.CH[2] + 0.6, c.CH[3] + 0.2, 0.4, 0.5)
    p = f.T(st.BR1); label(f, (1036, p[1] - 150), 'FLAW NOW PUBLIC', 'NOT UPDATED = TARGET', a, 'r')
    a = fade(t, c.CH[3] + 0.8, c.CH[4] + 0.2, 0.4, 0.5)
    p = f.T(st.ZD); label(f, (44, p[1] + 50), 'ZERO-DAY', 'KNOWN ONLY TO THE ATTACKER', a)
    cards(f, st.CARDS, c.VEND - 0.05)
