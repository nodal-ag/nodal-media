from kit import *

TW = None
def setup(c):
    global TW
    TW = tower()
    st = K()
    st.WS = [(150, 700), (930, 700), (150, 1250), (930, 1250)]
    st.lap = spr_laptop(); st.mail = spr_tag('ATTACHMENT'); st.lock = spr_lock(s=0.55, c=VIO)
    st.FILES = [spr_doc('FILE', w=60, h=76, lines=4)]
    st.BK = [(215, 1435), (540, 1440), (865, 1440)]
    st.bk = spr_server(w=110, h=70)
    st.CARDS = [(1060, 'Three copies', 'TWO DIFFERENT MEDIA', c.CH[3] + 0.4, True),
                (1175, 'One of them offline', 'THE RANSOMWARE CAN\'T REACH IT', c.sub_t('one of them') + 0.1, True),
                (1290, 'Test your restore', 'REGULARLY', c.sub_t('And test') + 0.1, True)]
    return st

def scene(f):
    c, t, st, s = f.c, f.t, f.st, f.s
    dim = 1 - 0.6 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5)
    enc = seg(t, c.sub_t('then encrypts') - 0.1, c.sub_t('then encrypts') + 0.5) * (1 - seg(t, c.CH[3], c.CH[3] + 0.6))
    hook = fade(t, 0.3, c.CH[1], 0.5, 0.4)
    enc = max(enc, hook)
    ha = f.scene * dim
    floor(f, 560, 1402, 270, 44, ha)
    TW.draw(f.lay, f.cam, ha * (1 - 0.3 * enc)); TW.sheen(f.lay, f.cam, t, ha)
    engine_path(f, ha * (1 - 0.7 * enc))
    for n_, q in enumerate(st.WS):
        p = f.T(q); paste(f.lay, st.lap, p, s, ha)
        faded_line(f, (p[0] + (60 if q[0] < 540 else -60) * s, p[1]), f.T((390 if q[0] < 540 else 690, q[1])), ha * 0.6, 1.2)
        for j in range(3):
            fp = f.T((q[0] - 50 + j * 50, q[1] + 90)); paste(f.lay, st.FILES[0], fp, s * 0.8, ha * seg(t, 0.4, 1.0))
            if enc > 0: paste(f.lay, st.lock, fp, s, ha * enc)
    # entry (chapter 1)
    a1 = fade(t, c.CH[1], c.CH[2] + 0.6, 0.4, 0.5) * f.scene
    if a1 > 0:
        u = seg(t, c.CH[1] + 0.2, c.CH[1] + 1.4)
        p = (lerp(-40, st.WS[0][0], u), lerp(560, st.WS[0][1] - 60, u)); paste(f.lay, st.mail, f.T(p), s, a1 * (1 - seg(u, 0.9, 1)))
        if u >= 1: dark_node(f, f.T((st.WS[0][0], st.WS[0][1] - 60)), a1, 14)
    # spread (chapter 2)
    a2 = fade(t, c.CH[2], c.CH[3] + 0.3, 0.4, 0.6) * f.scene
    if a2 > 0:
        cv = Curve([(st.WS[0][0], st.WS[0][1] - 60), (300, 700), (392, 748)])
        for n_, q in enumerate(st.WS[1:]):
            g = seg(t, c.CH[2] + 0.5 + n_ * 0.6, c.CH[2] + 1.2 + n_ * 0.6)
            if g > 0:
                cvn = Curve([(540, 1030), ((540 + q[0]) / 2, (1030 + q[1]) / 2 - 40), (q[0], q[1] - 60)])
                packets(f, cvn, a2 * g, 2, 1.6, 'dark')
        packets(f, cv, a2, 3, 1.4, 'dark')
        if enc > 0:
            dark_node(f, f.T((540, 640)), a2 * enc, 34)
        # connected backup gets encrypted too
        bp = f.T((540, 1440)); paste(f.lay, st.bk, bp, s, a2); faded_line(f, f.T((540, 1372)), (bp[0], bp[1] - 40 * s), a2, 1.2)
        if enc > 0: paste(f.lay, st.lock, bp, s * 1.4, a2 * enc)
    # 3-2-1 (chapter 3)
    a3 = fade(t, c.CH[3] + 0.1, c.VEND, 0.4, 0.5) * f.scene
    if a3 > 0:
        for n_, q in enumerate(st.BK):
            u = seg(t, c.CH[3] + 0.2 + n_ * 0.4, c.CH[3] + 0.6 + n_ * 0.4)
            p = f.T(q); paste(f.lay, st.bk, p, s, a3 * u)
            if n_ < 2: faded_line(f, f.T((540, 1372)), (p[0], p[1] - 40 * s), a3 * u * 0.8, 1.2)
            else:
                dashed(f, [f.T((690, 1372)), (p[0], p[1] - 40 * s)], a3 * u * 0.6, 1.2, MUT)
                node(f, (p[0], p[1] - 56 * s), a3 * u, 1.0)

def text(f):
    c, t, st = f.c, f.t, f.st
    a1 = fade(t, c.CH[1] + 1.2, c.CH[2] + 0.4, 0.4, 0.5)
    p = f.T(st.WS[0]); label(f, (44, p[1] - 140), 'ONE ATTACHMENT', '', a1)
    enc = fade(t, c.sub_t('then encrypts') + 0.2, c.CH[3], 0.3, 0.5)
    p = f.T((540, 640)); label(f, (p[0], p[1] - 110), 'RANSOM', 'EVERYTHING ENCRYPTED', enc, 'm')
    a2 = fade(t, c.sub_t('connected backups'), c.CH[3], 0.3, 0.5)
    label(f, (630, 1405), 'CONNECTED BACKUP', 'ENCRYPTED TOO', a2)
    a3 = fade(t, c.sub_t('one of them') + 0.2, c.VEND, 0.4, 0.5) * 0
    cards(f, st.CARDS, c.VEND - 0.05)
