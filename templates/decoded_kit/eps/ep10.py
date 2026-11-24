from kit import *

MET = None
INS = (24, 40, 24, 300)
def setup(c):
    global MET
    MET = Hero(410, 700, 670, 1320, 40, -20, 0, 2.6, caps=True, glass=False)
    st = K()
    st.PH = spr_phone(w=120, h=220)
    st.PHP = (905, 1140)
    st.TOP = Curve([(672, 880), (760, 860), (850, 940), (900, 1020)])
    st.SC = (905, 650)
    st.TOS = Curve([(905, 1028), (980, 900), (960, 760), (920, 690)])
    st.CARDS = [(1060, 'Read the address first', 'BEFORE OPENING IT', c.sub_t('The habit') + 0.2, True),
                (1175, 'Stickers on QR codes', 'BE WARY', c.sub_t('be wary') + 0.1, False),
                (1290, 'The official app', 'PAY THERE', c.sub_t('and pay') + 0.1, True)]
    return st

def qr(k, n=21, seed=1, size=180):
    rr = np.random.default_rng(seed); cell = size / n
    im = Image.new('RGBA', (int(size * k), int(size * k)), rgba(OFF, 1)); d = ImageDraw.Draw(im)
    for i in range(n):
        for j in range(n):
            finder = (i < 7 and j < 7) or (i < 7 and j >= n - 7) or (i >= n - 7 and j < 7)
            if finder:
                ii, jj = i % (n - 7) if i >= 7 else i, j % (n - 7) if j >= 7 else j
                on = ii in (0, 6) or jj in (0, 6) or (2 <= ii <= 4 and 2 <= jj <= 4)
            else: on = rr.random() < 0.48
            if on: d.rectangle([j * cell * k, i * cell * k, (j + 1) * cell * k - 1, (i + 1) * cell * k - 1], fill=rgba(INK, 1))
    return im
QR1, QR2 = None, None

def met_img(f):
    global QR1, QR2
    if QR1 is None: QR1, QR2 = qr(SS, seed=1), qr(SS, seed=7)
    c, t = f.c, f.t; w, h = MET.screen_size(INS); k = SS
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=8 * k, fill=rgba(mixc(INK, LIN, 0.25), 1))
    d.text((18 * k, 14 * k), 'CAR PARK · PAY HERE', font=MON(15 * k), fill=rgba(MUT, 1))
    im.alpha_composite(QR1, (int((w - QR1.width) / 2), int(50 * k)))
    u = seg(t, c.CH[1] + 0.2, c.CH[1] + 1.0)
    if u > 0:
        q2 = QR2.copy(); ImageDraw.Draw(q2).rectangle([0, 0, q2.width - 1, q2.height - 1], outline=rgba(VIO, 1), width=int(5 * k))
        st2 = q2.rotate(-4, expand=True, fillcolor=(0, 0, 0, 0))
        y = int(50 * k - (1 - u) * 260 * k) + int(6 * k)
        im.alpha_composite(setalpha(st2, u), (int((w - st2.width) / 2 + 8 * k), max(-st2.height + 1, y)))
    return im

def scene(f):
    c, t, st, s = f.c, f.t, f.st, f.s
    dim = 1 - 0.6 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5)
    ha = f.scene * dim
    floor(f, 560, 1350, 230, 36, ha)
    MET.draw(f.lay, f.cam, ha); MET.screen(f.lay, f.cam, met_img(f), INS, ha); MET.sheen(f.lay, f.cam, t, ha)
    a2 = fade(t, c.CH[2] - 0.1, c.VEND, 0.5, 0.5) * f.scene * dim
    if a2 > 0:
        g = seg(t, c.CH[2] + 0.1, c.CH[2] + 0.9); path_line(f, [f.T(q) for q in st.TOP.part(0, g)], a2)
        p = f.T(st.PHP); paste(f.lay, st.PH, p, s, a2)
        pg = seg(t, c.CH[2] + 0.8, c.CH[2] + 1.2) * a2
        if pg > 0:
            x0, y0 = p[0] - 46 * s, p[1] - 80 * s
            f.dr.text((x0 * SS, y0 * SS), 'Car park · Pay', font=UIB(int(12 * s * SS)), fill=rgba(OFF, pg))
            for i in range(3):
                yy_ = y0 + (30 + i * 34) * s
                lit = seg(t, c.sub_t('and you enter') + i * 0.3, c.sub_t('and you enter') + i * 0.3 + 0.3)
                f.dr.rounded_rectangle([x0 * SS, yy_ * SS, (x0 + 92 * s) * SS, (yy_ + 22 * s) * SS], radius=int(4 * SS), outline=rgba(mixc(LIN, VIO, lit), pg), width=SS)
        sa = seg(t, c.sub_t('and you enter') + 0.4, c.sub_t('and you enter') + 1.0) * a2
        path_line(f, [f.T(q) for q in st.TOS.part(0, sa)], sa, col=DEEP)
        dark_node(f, f.T(st.SC), sa, 26)

def text(f):
    c, t, st = f.c, f.t, f.st
    a1 = fade(t, c.CH[1] + 0.9, c.CH[2] + 0.4, 0.4, 0.5)
    label(f, (44, 760), 'STICKER', 'STUCK OVER THE REAL ONE', a1)
    a2 = fade(t, c.sub_t('A QR code hides'), c.CH[3] + 0.2, 0.4, 0.5)
    p = f.T(st.PHP); label(f, (1036, p[1] + 128), 'ADDRESS', 'HIDDEN UNTIL YOU SCAN', a2, 'r')
    a3 = fade(t, c.sub_t('and you enter') + 0.8, c.CH[3] + 0.4, 0.4, 0.5)
    p = f.T(st.SC); label(f, (1036, p[1] - 96), 'SCAMMER', 'YOUR CARD', a3, 'r')
    cards(f, st.CARDS, c.VEND - 0.05)
