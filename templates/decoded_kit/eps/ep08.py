from kit import *

WIN = None
INS = (14, 14, 14, 14)
def setup(c):
    global WIN
    WIN = Hero(250, 800, 730, 1180, 36, -18, radius=16, k=2.4)
    st = K()
    st.SITE = (905, 700)
    st.TUN = Curve([(735, 900), (800, 860), (850, 780), (st.SITE[0] - 10, st.SITE[1] + 40)])
    st.srv = spr_server(w=96, h=130); st.web = spr_web(w=130, h=96); st.lock = spr_lock(s=0.9); st.lockv = spr_lock(s=0.7, c=VIO)
    st.GRID = [(150, 600), (330, 560), (520, 590), (170, 1330), (380, 1370), (590, 1340)]
    return st

def screen_img(f):
    c, t = f.c, f.t; w, h = WIN.screen_size(INS); k = SS
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fake = seg(t, c.CH[2] + 0.2, c.CH[2] + 0.8)
    d.rounded_rectangle([0, 0, w - 1, 40 * k], radius=10 * k, fill=rgba(mixc(INK, LIN, 0.35), 1))
    for i in range(3): d.ellipse([(14 + i * 16) * k, 15 * k, (24 + i * 16) * k, 25 * k], fill=rgba(MUT, 0.7))
    d.rounded_rectangle([70 * k, 8 * k, w - 20 * k, 32 * k], radius=10 * k, fill=rgba(shade(INK, 0.7), 1))
    lk = spr_lock(k=SS, s=0.34, c=VIO); im.alpha_composite(lk, (int(82 * k), int(11 * k)))
    url = 'https://rnybank.example/login' if fake > 0.5 else 'https://mybank.example/login'
    d.text((104 * k, 12 * k), url, font=UI(14 * k), fill=rgba(OFF, 1))
    big = seg(t, c.CH[4] + 0.1, c.CH[4] + 0.6)
    if big < 1:
        a = 1 - big
        d.text((40 * k, 80 * k), 'My Bank', font=UIB(30 * k), fill=rgba(OFF, a))
        d.text((40 * k, 122 * k), 'Sign in to your account', font=UI(16 * k), fill=rgba(MUT, a))
        for i, lab in enumerate(['Customer ID', 'Password']):
            y = (164 + i * 66) * k; d.text((40 * k, y), lab, font=UI(13 * k), fill=rgba(MUT, a))
            d.rounded_rectangle([40 * k, y + 20 * k, w - 40 * k, y + 54 * k], radius=8 * k, outline=rgba(LIN, a), width=int(1.6 * k), fill=rgba(shade(INK, 0.8), a))
        d.rounded_rectangle([40 * k, 306 * k, 220 * k, 342 * k], radius=18 * k, fill=rgba(VIO, a))
        d.text((92 * k, 314 * k), 'Sign in', font=UIB(15 * k), fill=rgba(OFF, a))
    if big > 0:
        f2 = UIB(44 * k); y = 140 * k; x = 30 * k
        wbad = d.textlength('rn', font=f2)
        if big > 0.5: d.rounded_rectangle([x - 5 * k, y - 2 * k, x + wbad + 5 * k, y + 56 * k], radius=8 * k, outline=rgba(VIO, big), width=int(2.6 * k))
        d.text((x, y), 'rn', font=f2, fill=rgba(VIO, big)); d.text((x + wbad, y), 'ybank.example', font=f2, fill=rgba(OFF, big))
        d.text((30 * k, 230 * k), '"rn" is not "m"', font=MON(18 * k), fill=rgba(VIO, seg(t, c.CH[4] + 0.8, c.CH[4] + 1.2)))
    return im

def scene(f):
    c, t, st, s = f.c, f.t, f.st, f.s
    ha = f.scene
    floor(f, 520, 1215, 290, 40, ha)
    WIN.draw(f.lay, f.cam, ha); WIN.screen(f.lay, f.cam, screen_img(f), INS, ha); WIN.sheen(f.lay, f.cam, t, ha)
    fake = seg(t, c.CH[2] + 0.2, c.CH[2] + 0.8)
    ta = fade(t, c.CH[1] - 0.1, c.CH[3] + 0.2, 0.5, 0.6) * f.scene
    g = seg(t, c.CH[1] + 0.2, c.CH[1] + 1.2)
    tube(f, st.TUN, ta, g)
    if g > 0: packets(f, st.TUN, ta, 5, 1.8, 'lock', g)
    sa = seg(t, 0.8, 1.4) * f.scene * (1 - seg(t, c.CH[3] + 0.2, c.CH[3] + 0.8))
    p = f.T(st.SITE)
    paste(f.lay, st.srv, p, s, sa * (1 - fake))
    if fake > 0: dark_node(f, p, sa * fake, 34)
    paste(f.lay, st.lock, (p[0], p[1] - 98 * s), s, sa)
    # padlocks for anyone (chapter 3)
    ga = fade(t, c.CH[3], c.CH[4] + 0.2, 0.4, 0.5) * f.scene
    for n_, q in enumerate(st.GRID):
        u = seg(t, c.CH[3] + 0.2 + n_ * 0.25, c.CH[3] + 0.6 + n_ * 0.25)
        if u <= 0: continue
        paste(f.lay, st.web, f.T(q), s * 0.9, ga * u); paste(f.lay, st.lockv, f.T((q[0] + 52, q[1] - 40)), s, ga * seg(t, c.CH[3] + 0.5 + n_ * 0.25, c.CH[3] + 0.8 + n_ * 0.25))

def text(f):
    c, t, st = f.c, f.t, f.st
    ta = fade(t, c.CH[1] + 0.8, c.CH[2] + 0.2, 0.4, 0.5)
    p = f.T(st.SITE); label(f, (44, 660), 'ENCRYPTED', 'NO ONE READS IT ON THE WAY', ta)
    fa = fade(t, c.CH[2] + 0.6, c.CH[3] + 0.2, 0.4, 0.5)
    label(f, (1036, p[1] + 60), 'FRAUDSTER', 'SAME PADLOCK', fa, 'r')
    ga = fade(t, c.CH[3] + 0.6, c.CH[4] + 0.2, 0.4, 0.5)
    p = f.T((540, 1460)); label(f, (1036, 1470), 'FREE · A FEW MINUTES', '', ga, 'r')
