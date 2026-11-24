from kit import *

TW = None
def setup(c):
    global TW
    TW = tower()
    st = K()
    st.CO, st.CU = (160, 620), (920, 1300)
    st.lap = spr_laptop(); st.cus = spr_web()
    st.inv = spr_doc('INVOICE.PDF', w=70, h=90, lines=5); st.xml = spr_tag('STRUCTURED')
    st.DIRECT = Curve([(220, 640), (600, 560), (900, 800), (930, 1220)])
    st.IN = Curve([(240, 640), (320, 680), (360, 740), (392, 748)])
    st.OUT = Curve([(688, 1322), (780, 1340), (850, 1320), (st.CU[0] - 86, st.CU[1])])
    st.CARDS = [(1080, 'Clean data in your software', 'IDS · VAT · INVOICE NUMBERS', c.S(4) + 0.2, True),
                (1195, 'Get ready now', 'NOT THE DAY BEFORE', c.sub_t('Get ready') + 0.1, True)]
    return st

def scene(f):
    c, t, st, s = f.c, f.t, f.st, f.s
    dim = 1 - 0.6 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5)
    ha = f.scene * dim
    floor(f, 560, 1402, 270, 44, ha)
    pa = seg(t, c.CH[2] - 0.2, c.CH[2] + 0.6) * ha + 0.25 * ha
    TW.draw(f.lay, f.cam, min(1, pa)); TW.sheen(f.lay, f.cam, t, ha)
    engine_path(f, min(1, pa) * (0.3 + 0.7 * seg(t, c.CH[2], c.CH[2] + 0.6)), nodes_t=[c.CH[3] + 0.3 + i * 0.5 for i in range(3)] + [None])
    paste(f.lay, st.lap, f.T(st.CO), s, ha * seg(t, 0.3, 0.9)); paste(f.lay, st.cus, f.T(st.CU), s, ha * seg(t, 0.5, 1.1))
    # old way: PDF by email (hook + chapter 1)
    oa = fade(t, 0.6, c.CH[2] + 0.3, 0.4, 0.5) * f.scene
    if oa > 0:
        cut = seg(t, c.sub_t('no longer'), c.sub_t('no longer') + 0.6)
        dashed(f, [f.T(q) for q in st.DIRECT.pts], oa * (1 - 0.6 * cut), 1.6, MUT)
        u = ((t - 0.6) % 2.4) / 2.4
        if cut < 1: paste(f.lay, st.inv, f.T(st.DIRECT.at(u)), s, oa * (1 - cut) * math.sin(math.pi * u))
        if cut > 0:
            m = f.T(st.DIRECT.at(0.5))
            for dx_ in (-9, 9):
                f.dr.line([((m[0] + dx_ - 8) * SS, (m[1] + 16) * SS), ((m[0] + dx_ + 8) * SS, (m[1] - 16) * SS)], fill=rgba(OFF, cut * oa), width=3 * SS)
    # new way through the platform (chapter 2+)
    na = fade(t, c.CH[2], c.VEND, 0.4, 0.5) * f.scene * dim
    if na > 0:
        g1 = seg(t, c.CH[2] + 0.2, c.CH[2] + 0.8); path_line(f, [f.T(q) for q in st.IN.part(0, g1)], na)
        g2 = seg(t, c.sub_t('then passed'), c.sub_t('then passed') + 0.8); path_line(f, [f.T(q) for q in st.OUT.part(0, g2)], na)
        cyc = 4.0; u = ((t - c.CH[2]) % cyc) / cyc
        if u < 0.2: paste(f.lay, st.xml, f.T(st.IN.at(u / 0.2)), s * 0.9, na)
        elif u < 0.75: paste(f.lay, st.xml, f.T(ENGINE_PATH.at((u - 0.2) / 0.55)), s * 0.8, na)
        elif g2 >= 1: paste(f.lay, st.xml, f.T(st.OUT.at((u - 0.75) / 0.25)), s * 0.9, na)

def text(f):
    c, t, st = f.c, f.t, f.st
    la = seg(t, 0.8, 1.4) * f.scene * (1 - 0.7 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5))
    p = f.T(st.CO); label(f, (p[0], p[1] - 100), 'YOUR COMPANY', '', la, 'm')
    p = f.T(st.CU); label(f, (p[0], p[1] + 78), 'YOUR CUSTOMER', '', la, 'm')
    oa = fade(t, 1.0, c.CH[2] + 0.3, 0.4, 0.5)
    label(f, (1036, 560), 'PDF · EMAIL', '', oa, 'r')
    na = fade(t, c.CH[2] + 0.6, c.VEND, 0.4, 0.5) * (1 - 0.7 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5))
    p = f.T((740, 590)); label(f, (p[0], p[1]), 'PLATFORM', 'CHECKED · PASSED ON', na)
    for n_, lab in enumerate(['01 · IDS', '02 · VAT', '03 · INVOICE NO.']):
        al = fade(t, c.CH[3] + 0.3 + n_ * 0.5, c.VEND, 0.3, 0.5) * (1 - 0.8 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5))
        p = f.T(ENGINE_PATH.at([0.2, 0.4, 0.6][n_])); right = p[0] > 520
        label(f, ((p[0] + 40) if right else (p[0] - 40), p[1] - 14), lab, '', al, 'l' if right else 'r')
    cards(f, st.CARDS, c.VEND - 0.05)
