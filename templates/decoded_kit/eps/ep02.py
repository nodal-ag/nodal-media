from kit import *

R = None
def setup(c):
    global R
    R = Hero(340, 960, 740, 1090, 40, -20, 0, 2.6, caps=False, glass=False)
    st = K()
    st.LAP, st.WEB, st.CLONE, st.ATT = (170, 1290), (915, 640), (880, 1230), (900, 960)
    st.lap, st.web, st.srv = spr_phone(w=62, h=112), spr_web(), spr_server(w=110, h=60)
    st.A = Curve([(240, 1260), (300, 1180), (330, 1100), (360, 1050)])
    st.B = Curve([(700, 950), (760, 830), (840, 760), (880, 705)])
    st.L2C = Curve([(240, 1300), (420, 1330), (650, 1320), (820, 1250)])
    st.C2W = Curve([(905, 1190), (960, 1000), (975, 820), (955, 705)])
    st.C2A = Curve([(880, 1195), (860, 1100), (880, 1020), (900, 990)])
    st.TAGS = [spr_tag('EMAIL'), spr_tag('PASSWORD'), spr_tag('MESSAGES')]
    st.CARDS = [(1060, 'The website padlock', 'HELPS · NOT EVERYTHING', c.S(5) + 0.3, True),
                (1175, "Your phone's hotspot", 'FOR ANYTHING SENSITIVE', c.sub_t('for anything') + 0.1, True),
                (1290, 'Unknown free networks', 'FORGET THEM', c.sub_t('and forget') + 0.1, False)]
    return st

def scene(f):
    c, t, st, s = f.c, f.t, f.st, f.s
    dim = 1 - 0.65 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5)
    ha = f.scene * dim
    floor(f, 560, 1125, 300, 40, ha)
    # antennas
    for ax in (420, 660):
        p0, p1 = f.T((ax, 960)), f.T((ax + 10, 830))
        f.dr.line([(p0[0] * SS, p0[1] * SS), (p1[0] * SS, p1[1] * SS)], fill=rgba(mixc(LIN, MUT, 0.5), ha), width=int(5 * s * SS))
        dot(f.dr, p1, 7 * s, MUT, ha)
    R.draw(f.lay, f.cam, ha); R.sheen(f.lay, f.cam, t, ha)
    for i in range(5):
        p = f.T((400 + i * 36, 1045)); on = (int(t * 3) + i) % 4 != 0
        dot(f.dr, p, 4 * s, VIO if on else LIN, ha); f.gd.ellipse([p[0] - 8, p[1] - 8, p[0] + 8, p[1] + 8], fill=rgba(VIO, 0.6 * ha * on))
    # waves
    for k_ in range(3):
        pr = ((t * 0.6) + k_ / 3) % 1
        p = f.T((540, 890)); r_ = (40 + 120 * pr) * s
        f.dr.arc([(p[0] - r_) * SS, (p[1] - r_) * SS, (p[0] + r_) * SS, (p[1] + r_) * SS], 220, 320, fill=rgba(VIO, 0.6 * (1 - pr) * ha), width=int(2 * SS))
    devs = seg(t, 0.4, 1.2) * f.scene * dim
    paste(f.lay, st.lap, f.T(st.LAP), s, devs); paste(f.lay, st.web, f.T(st.WEB), s, devs)
    normal = f.scene * (1 - seg(t, c.S(2) - 0.3, c.S(2) + 0.6)) * dim
    for cv in (st.A, st.B):
        path_line(f, [f.T(q) for q in cv.pts], normal); particles(f, cv, normal, 8, 1.4)
    # clone router
    ca = fade(t, c.CH[1] + 0.3, 1e9, 0.6, 0.1) * f.scene * dim
    if ca > 0:
        paste(f.lay, st.srv, f.T(st.CLONE), s, ca, 0)
        dark_node(f, f.T((st.CLONE[0], st.CLONE[1] - 2)), 0.0)
        g = seg(t, c.S(2), c.S(2) + 1.0)
        path_line(f, [f.T(q) for q in st.L2C.part(0, g)], ca)
        g2 = seg(t, c.S(2) + 0.8, c.S(2) + 1.6)
        path_line(f, [f.T(q) for q in st.C2W.part(0, g2)], ca)
        if g2 >= 1:
            particles(f, st.L2C, ca, 8, 1.6); particles(f, st.C2W, ca, 8, 1.6)
    # interception
    ia = fade(t, c.CH[2] + 0.2, c.CH[3] + 0.6, 0.5, 0.6) * f.scene
    if ia > 0:
        dark_node(f, f.T(st.ATT), ia, 26)
        path_line(f, [f.T(q) for q in st.C2A.pts], ia * 0.8, col=DEEP)
        for n_, spr in enumerate(st.TAGS):
            u = ((t - (c.CH[2] + 0.6) - n_ * 0.9) % 2.7) / 2.7
            if t < c.CH[2] + 0.6 + n_ * 0.9: continue
            paste(f.lay, spr, f.T(st.C2A.at(u)), s * 0.7, ia * math.sin(math.pi * u))

def text(f):
    c, t, st = f.c, f.t, f.st
    la = seg(t, 1.0, 1.6) * f.scene * (1 - 0.8 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5))
    p = f.T(st.LAP); label(f, (p[0], p[1] + 62), 'YOUR PHONE', '', la, 'm')
    p = f.T(st.WEB); label(f, (p[0], p[1] - 110), 'INTERNET', '', la, 'm')
    p = f.T((540, 1100)); label(f, (p[0], p[1] + 24), 'CAFE_WIFI', '', la * (1 - 0.6 * seg(t, c.CH[1], c.CH[1] + 0.6)), 'm')
    ca = fade(t, c.CH[1] + 0.5, 1e9, 0.5, 0.1) * la
    p = f.T(st.CLONE); label(f, (1036, p[1] + 50), 'CAFE_WIFI', 'SAME NAME · NOT THE CAFÉ', ca, 'r')
    ia = fade(t, c.CH[2] + 0.4, c.CH[3] + 0.6, 0.5, 0.6)
    p = f.T(st.ATT); label(f, (1036, p[1] - 110), 'MAN IN', 'THE MIDDLE', ia, 'r')
    cards(f, st.CARDS, c.VEND - 0.05)
