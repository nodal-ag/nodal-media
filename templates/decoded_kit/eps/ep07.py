from kit import *

SIM = None
INS = (0, 0, 0, 0)
def setup(c):
    global SIM
    SIM = Hero(360, 820, 720, 1060, 30, -16, radius=22, k=2.4)
    st = K()
    st.INFO = [(spr_tag('NAME'), (190, 600)), (spr_tag('ID CARD'), (180, 690)), (spr_tag('NUMBER'), (195, 780))]
    st.FR = (240, 1250); st.OPS = (880, 640)
    st.YOU = (175, 1360); st.THEM = (905, 1300)
    st.PH = spr_phone(w=80, h=150); st.MSIM = None
    st.BANK = (905, 1010)
    st.CARDS = [(1080, 'Phone suddenly without signal?', 'CALL YOUR OPERATOR RIGHT AWAY', c.S(3) + 0.3, True),
                (1195, 'An authenticator app', 'INSTEAD OF TEXT CODES', c.sub_t('use an authenticator') + 0.1, True)]
    return st

def sim_img(f, a=1.0):
    w, h = SIM.screen_size(INS); k = SS
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx0, cy0 = 60 * k, 70 * k
    d.rounded_rectangle([cx0, cy0, cx0 + 120 * k, cy0 + 100 * k], radius=10 * k, fill=rgba(mixc(LIN, MUT, 0.45), 1), outline=rgba(MUT, 1), width=int(2 * k))
    for x in (cx0 + 40 * k, cx0 + 80 * k): d.line([x, cy0, x, cy0 + 100 * k], fill=rgba(shade(INK, 0.8), 1), width=int(2 * k))
    d.line([cx0, cy0 + 50 * k, cx0 + 120 * k, cy0 + 50 * k], fill=rgba(shade(INK, 0.8), 1), width=int(2 * k))
    d.text((205 * k, 82 * k), '06 •• •• 47', font=UIB(20 * k), fill=rgba(OFF, 1))
    d.text((205 * k, 114 * k), 'YOUR NUMBER', font=MON(14 * k), fill=rgba(VIO, 1))
    return im
def mini_sim(k=SS):
    im, d = spr_box(90, 60, r=8)
    d.rounded_rectangle([12 * k, 14 * k, 44 * k, 42 * k], radius=4 * k, fill=rgba(mixc(LIN, MUT, 0.45), 1))
    return im
MSIM = None

def scene(f):
    global MSIM
    if MSIM is None: MSIM = mini_sim()
    c, t, st, s = f.c, f.t, f.st, f.s
    dim = 1 - 0.6 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5)
    ha = f.scene * dim
    floor(f, 556, 1080, 260, 36, ha)
    SIM.draw(f.lay, f.cam, ha); SIM.screen(f.lay, f.cam, sim_img(f), INS, ha); SIM.sheen(f.lay, f.cam, t, ha)
    # chapter 1: info -> fraudster -> operator -> new SIM
    a1 = fade(t, c.CH[1] - 0.1, c.CH[3] + 0.3, 0.5, 0.6) * f.scene * dim
    if a1 > 0:
        frp = f.T(st.FR)
        for n_, (spr, pos) in enumerate(st.INFO):
            u = seg(t, c.CH[1] + 0.4 + n_ * 0.3, c.CH[1] + 1.4 + n_ * 0.3)
            p = (lerp(pos[0], st.FR[0], u), lerp(pos[1], st.FR[1], u))
            paste(f.lay, spr, f.T(p), s * lerp(1, 0.4, u), a1 * (1 - seg(u, 0.85, 1)) * seg(t, c.CH[1], c.CH[1] + 0.4))
        dark_node(f, frp, a1 * seg(t, c.CH[1] + 0.6, c.CH[1] + 1.2), 26)
        g = seg(t, c.sub_t('poses as'), c.sub_t('poses as') + 1.0)
        cv = Curve([(st.FR[0] - 10, st.FR[1] - 40), (150, 980), (230, 720), (560, 590), (st.OPS[0] - 40, st.OPS[1] + 10)])
        path_line(f, [f.T(q) for q in cv.part(0, g)], a1, col=DEEP)
        node(f, f.T(st.OPS), a1 * g, fade(t, c.sub_t('and gets'), 1e9, 0.3, 0.1))
        u = seg(t, c.sub_t('and gets') + 0.3, c.sub_t('and gets') + 1.5)
        if u > 0:
            cv2 = Curve([st.OPS, (980, 900), (960, 1150), (st.THEM[0], st.THEM[1] - 90)])
            paste(f.lay, MSIM, f.T(cv2.at(u)), s, a1 * (1 - seg(u, 0.9, 1)))
    # phones (chapter 2)
    a2 = fade(t, c.CH[2] - 0.2, c.VEND, 0.5, 0.5) * f.scene * dim
    if a2 > 0:
        paste(f.lay, st.PH, f.T(st.YOU), s, a2); paste(f.lay, st.PH, f.T(st.THEM), s, a2)
        lost = seg(t, c.CH[2] + 0.3, c.CH[2] + 0.8)
        for b in range(4):
            p = f.T((st.YOU[0] - 18 + b * 12, st.YOU[1] - 40 - b * 5)); hgt = (6 + b * 5) * s
            f.dr.rectangle([(p[0] - 3) * SS, (p[1] - hgt / 2) * SS, (p[0] + 3) * SS, (p[1] + 8) * SS], fill=rgba(MUT if lost < 0.5 else LIN, a2))
        for b in range(4):
            p = f.T((st.THEM[0] - 18 + b * 12, st.THEM[1] - 40 - b * 5)); hgt = (6 + b * 5) * s
            f.dr.rectangle([(p[0] - 3) * SS, (p[1] - hgt / 2) * SS, (p[0] + 3) * SS, (p[1] + 8) * SS], fill=rgba(VIO if lost > 0.5 else LIN, a2))
        ca = fade(t, c.sub_t('Theirs'), c.CH[3] + 0.4, 0.4, 0.6) * a2
        if ca > 0:
            cv3 = Curve([st.BANK, (1000, 1120), (990, 1200), (st.THEM[0] + 30, st.THEM[1] - 80)])
            node(f, f.T(st.BANK), ca, 1.0)
            path_line(f, [f.T(q) for q in cv3.pts], ca); packets(f, cv3, ca, 4, 1.2, 'open')

def text(f):
    c, t, st = f.c, f.t, f.st
    a1 = fade(t, c.CH[1] + 1.0, c.CH[2] + 0.4, 0.4, 0.6)
    p = f.T(st.FR); label(f, (44, p[1] + 50), 'FRAUDSTER', 'POSES AS YOU', a1)
    p = f.T(st.OPS); label(f, (1036, p[1] - 100), 'OPERATOR', 'NEW SIM · YOUR NUMBER', fade(t, c.sub_t('poses as') + 0.8, c.CH[2] + 0.4, 0.4, 0.6), 'r')
    a2 = fade(t, c.CH[2] + 0.2, c.CH[3] + 0.4, 0.4, 0.6)
    p = f.T(st.YOU); label(f, (44, p[1] + 96), 'YOUR PHONE', 'NO SIGNAL', a2)
    p = f.T(st.BANK); label(f, (1036, p[1] - 80), 'YOUR BANK', '', fade(t, c.sub_t('Theirs'), c.CH[3] + 0.4, 0.4, 0.6), 'r')
    p = f.T(st.THEM); label(f, (1036, p[1] + 96), 'THEIR PHONE', 'YOUR BANK CODES', a2, 'r')
    cards(f, st.CARDS, c.VEND - 0.05)
