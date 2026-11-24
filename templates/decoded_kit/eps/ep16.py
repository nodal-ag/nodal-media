from kit import *

TW = None
def setup(c):
    global TW
    TW = tower()
    st = K()
    st.DC = [((170, 760), 'EUROPE'), ((910, 760), 'UNITED STATES')]
    st.srv = spr_server(w=120, h=200)
    st.LAP = (170, 1300); st.lap = spr_laptop(); st.doc = spr_doc('FILE', w=60, h=76, lines=4)
    st.UP = Curve([(240, 1270), (300, 1150), (340, 900), (392, 748)])
    st.CP = [Curve([(392, 760), (300, 700), (230, 720)]), Curve([(690, 760), (800, 700), (850, 720)])]
    st.CARDS = [(1180, 'Ask your providers', 'WHERE IS OUR DATA HOSTED?', c.sub_t('Ask your') + 0.1, True)]
    return st

def cloud(f, p, a, r_=1.0):
    E = [(-60, 10, 50), (0, -20, 70), (70, 5, 55), (-10, 30, 60), (40, 30, 50)]
    for pas, (col, grow) in enumerate([(VIO, 3), (mixc(INK, LIN, 0.55), 0)]):
        for (dx, dy, rr) in E:
            q = (p[0] + dx * r_, p[1] + dy * r_); R = rr * r_ + grow
            f.dr.ellipse([(q[0] - R) * SS, (q[1] - R * 0.8) * SS, (q[0] + R) * SS, (q[1] + R * 0.8) * SS], fill=rgba(col, a))
    f.wd.ellipse([p[0] - 150 * r_, p[1] - 70 * r_, p[0] + 150 * r_, p[1] + 70 * r_], fill=rgba(VIO, 0.35 * a))

def scene(f):
    c, t, st, s = f.c, f.t, f.st, f.s
    dim = 1 - 0.55 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5)
    ha = f.scene * dim
    floor(f, 560, 1402, 270, 44, ha)
    reveal = seg(t, c.sub_t('Which one') if True else 0, c.sub_t('Which one') + 0.8)
    TW.draw(f.lay, f.cam, ha * (0.2 + 0.8 * reveal)); TW.sheen(f.lay, f.cam, t, ha * reveal)
    engine_path(f, ha * reveal)
    ca = (1 - reveal) * f.scene
    if ca > 0: cloud(f, f.T((540, 1000)), ca, 2.6 * f.s)
    # other data centres (chapter 1)
    a1 = fade(t, c.CH[1] + 0.2, c.VEND, 0.4, 0.5) * f.scene * dim
    for n_, (q, lab) in enumerate(st.DC):
        u = seg(t, c.sub_t('in Europe') + n_ * 0.7, c.sub_t('in Europe') + 0.5 + n_ * 0.7)
        paste(f.lay, st.srv, f.T(q), s, a1 * u)
    # upload + copies (chapter 2)
    a2 = fade(t, c.CH[2], c.VEND, 0.4, 0.5) * f.scene * dim
    if a2 > 0:
        paste(f.lay, st.lap, f.T(st.LAP), s, a2)
        g = seg(t, c.CH[2] + 0.2, c.CH[2] + 1.0); path_line(f, [f.T(q) for q in st.UP.part(0, g)], a2)
        u = seg(t, c.CH[2] + 0.3, c.CH[2] + 1.6); paste(f.lay, st.doc, f.T(st.UP.at(u)), s, a2 * (1 - seg(u, 0.9, 1)))
        for n_, cv in enumerate(st.CP):
            g2 = seg(t, c.sub_t('and it') + n_ * 0.3, c.sub_t('and it') + 0.8 + n_ * 0.3)
            path_line(f, [f.T(q) for q in cv.part(0, g2)], a2 * 0.8)
            if g2 >= 1:
                q = f.T(cv.at(1)); paste(f.lay, st.doc, (q[0] + (-50 if n_ == 0 else 50), q[1] + 80), s * 0.7, a2)
    # law ring (chapter 3)
    a3 = fade(t, c.CH[3] + 0.2, c.VEND, 0.4, 0.5) * f.scene
    if a3 > 0:
        p = f.T((540, 1030)); R = 330 * s
        f.dr.ellipse([(p[0] - R) * SS, (p[1] - R * 1.12) * SS, (p[0] + R) * SS, (p[1] + R * 1.12) * SS], outline=rgba(VIO, a3 * 0.8), width=int(2.4 * SS))

def text(f):
    c, t, st = f.c, f.t, f.st
    a1 = fade(t, c.CH[1] + 0.4, c.VEND, 0.4, 0.5) * (1 - 0.7 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5))
    for n_, (q, lab) in enumerate(st.DC):
        u = seg(t, c.sub_t('in Europe') + n_ * 0.7, c.sub_t('in Europe') + 0.5 + n_ * 0.7)
        p = f.T(q); label(f, (p[0], p[1] - 150), lab, '', a1 * u, 'm')
    u = seg(t, c.sub_t('or in Morocco'), c.sub_t('or in Morocco') + 0.5)
    p = f.T((540, 1370)); label(f, (p[0], p[1] + 56), 'MOROCCO', '', a1 * u, 'm')
    a2 = fade(t, c.sub_t('and it'), c.CH[3] + 0.2, 0.4, 0.5)
    label(f, (540, 560), 'COPIED SEVERAL TIMES', '', a2, 'm')
    a3 = fade(t, c.sub_t('Law 09-08'), c.VEND, 0.4, 0.5)
    label(f, (540, 560), 'LAW 09-08', 'TRANSFER ABROAD IS REGULATED', a3, 'm')
    cards(f, st.CARDS, c.VEND - 0.05)
