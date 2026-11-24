from kit import *

TW = None
def setup(c):
    global TW
    TW = tower()
    st = K()
    st.A, st.B = (165, 760), (915, 1280)
    st.ph = spr_phone(w=100, h=186)
    st.key = spr_lock(s=0.6, c=VIO)
    st.C1 = Curve([(st.A[0] + 60, st.A[1]), (300, 740), (392, 748)])
    st.C2 = Curve([(688, 1322), (780, 1330), (860, 1300), (st.B[0] - 60, st.B[1])])
    st.bub = spr_tag('See you at 10?', dotc=VIO); st.scr = spr_tag('x9#Lq!7@pZ', dotc=MUT)
    st.CARDS = [(1180, 'Visible to the servers', 'WHO TALKS TO WHOM · WHEN', c.sub_t('What stays') + 0.2, False)]
    return st

def scene(f):
    c, t, st, s = f.c, f.t, f.st, f.s
    dim = 1 - 0.55 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5)
    ha = f.scene * dim
    floor(f, 560, 1402, 270, 44, ha)
    TW.draw(f.lay, f.cam, ha); TW.sheen(f.lay, f.cam, t, ha); engine_path(f, ha)
    pa, pb = f.T(st.A), f.T(st.B)
    paste(f.lay, st.ph, pa, s, ha); paste(f.lay, st.ph, pb, s, ha)
    ka = fade(t, c.CH[1], 1e9, 0.4, 0.1) * ha
    paste(f.lay, st.key, (pa[0], pa[1] - 130 * s), s, ka); paste(f.lay, st.key, (pb[0], pb[1] - 130 * s), s, ka)
    if ka > 0:
        f.gd.ellipse([pa[0] - 22, pa[1] - 152 * s, pa[0] + 22, pa[1] - 108 * s], fill=rgba(VIO, ka)); f.gd.ellipse([pb[0] - 22, pb[1] - 152 * s, pb[0] + 22, pb[1] - 108 * s], fill=rgba(VIO, ka))
    path_line(f, [f.T(q) for q in st.C1.pts], ha * 0.8); path_line(f, [f.T(q) for q in st.C2.pts], ha * 0.8)
    # message trip, repeats from chapter 2
    if t > c.CH[2]:
        cyc = 5.0; u = ((t - c.CH[2]) % cyc) / cyc
        if u < 0.25:
            q = st.C1.at(u / 0.25); spr = st.bub if u < 0.05 else st.scr
            paste(f.lay, spr, f.T(q), s * 1.2, ha)
        elif u < 0.65:
            q = ENGINE_PATH.at((u - 0.25) / 0.4); paste(f.lay, st.scr, f.T(q), s * 1.1, ha)
        else:
            v = (u - 0.65) / 0.35; q = st.C2.at(min(1, v / 0.8)); spr = st.scr if v < 0.85 else st.bub
            paste(f.lay, spr, f.T(q), s * 1.2, ha * (1 - seg(v, 0.95, 1)))
    else:
        paste(f.lay, st.bub, (pa[0] + 10, pa[1] - 20 * s), s * 0.8, ha * seg(t, 0.6, 1.2))

def text(f):
    c, t, st = f.c, f.t, f.st
    ka = fade(t, c.CH[1] + 0.3, c.CH[2] + 0.4, 0.4, 0.5)
    p = f.T(st.A); label(f, (44, p[1] + 110), 'YOUR KEYS', '', ka)
    p = f.T(st.B); label(f, (1036, p[1] + 110), 'THEIR KEYS', '', ka, 'r')
    sa = fade(t, c.CH[2] + 0.5, c.VEND, 0.4, 0.5) * (1 - 0.7 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5))
    p = f.T((732, 900)); label(f, (p[0], p[1]), 'SERVERS', "CAN'T READ IT", sa)
    oa = fade(t, c.CH[3] + 0.2, c.VEND, 0.4, 0.5) * (1 - 0.7 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5))
    p = f.T(st.B); label(f, (1036, p[1] + 110), 'ONLY THIS PHONE', 'CAN DECRYPT IT', oa * (t > c.CH[2] + 0.5), 'r')
    cards(f, st.CARDS, c.VEND - 0.05)
