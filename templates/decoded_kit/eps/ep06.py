from kit import *

WIN = None
INS = (14, 14, 14, 14)
def setup(c):
    global WIN
    WIN = Hero(290, 760, 790, 1180, 36, -18, radius=16, k=2.4)
    st = K()
    st.META = (880, 600); st.ACC = (880, 600)
    st.PHONE = spr_phone(w=110, h=200)
    st.PH = (200, 1290)
    st.PIX = (750, 1145)
    st.C1 = Curve([st.PIX, (820, 1000), (900, 820), st.META])
    st.PEOPLE = [(390, 1370), (520, 1420), (650, 1380)]
    st.CARDS = [(1080, 'Ads for your business', 'TARGET PEOPLE LIKE YOUR CLIENTS', c.S(5) + 0.4, True)]
    return st

def screen_img(f):
    c, t = f.c, f.t; w, h = WIN.screen_size(INS); k = SS
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, 36 * k], radius=10 * k, fill=rgba(mixc(INK, LIN, 0.35), 1))
    for i in range(3): d.ellipse([(14 + i * 16) * k, 13 * k, (24 + i * 16) * k, 23 * k], fill=rgba(MUT, 0.7))
    d.rounded_rectangle([70 * k, 8 * k, w - 20 * k, 28 * k], radius=8 * k, fill=rgba(shade(INK, 0.7), 1))
    d.text((84 * k, 10 * k), 'shop.example/sofa-ocean', font=UI(13 * k), fill=rgba(MUT, 1))
    # product image: a sofa silhouette
    x0, y0, x1, y1 = 24 * k, 56 * k, 250 * k, 300 * k
    d.rounded_rectangle([x0, y0, x1, y1], radius=10 * k, fill=rgba(mixc(INK, LIN, 0.3), 1))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 20 * k
    d.rounded_rectangle([cx - 90 * k, cy - 50 * k, cx + 90 * k, cy + 10 * k], radius=16 * k, fill=rgba(mixc(LIN, VIO, 0.35), 1))
    d.rounded_rectangle([cx - 104 * k, cy - 10 * k, cx + 104 * k, cy + 40 * k], radius=14 * k, fill=rgba(mixc(LIN, VIO, 0.5), 1))
    for sx in (-80, 80): d.rectangle([cx + (sx - 4) * k, cy + 40 * k, cx + (sx + 4) * k, cy + 58 * k], fill=rgba(MUT, 1))
    d.text((272 * k, 60 * k), 'Sofa Ocean', font=UIB(26 * k), fill=rgba(OFF, 1))
    d.text((272 * k, 96 * k), '3 seats · grey', font=UI(16 * k), fill=rgba(MUT, 1))
    d.text((272 * k, 130 * k), '7 900 MAD', font=UIB(22 * k), fill=rgba(OFF, 1))
    d.rounded_rectangle([272 * k, 250 * k, 450 * k, 292 * k], radius=21 * k, fill=rgba(VIO, 1))
    d.text((300 * k, 260 * k), 'Add to cart', font=UIB(16 * k), fill=rgba(OFF, 1))
    for i, ww in enumerate([0.8, 0.6, 0.7]): d.line([272 * k, (176 + i * 20) * k, (272 + ww * 180) * k, (176 + i * 20) * k], fill=rgba(LIN, 1), width=int(2.4 * k))
    # cursor
    u = seg(t, 0.6, 2.2); cxp, cyp = lerp(w * 0.9, 150 * k, u), lerp(h * 0.95, 190 * k, u)
    d.polygon([(cxp, cyp), (cxp, cyp + 26 * k), (cxp + 7 * k, cyp + 20 * k), (cxp + 18 * k, cyp + 20 * k)], fill=rgba(OFF, 1), outline=rgba(INK, 1))
    return im

def scene(f):
    c, t, st, s = f.c, f.t, f.st, f.s
    dim = 1 - 0.6 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5)
    ha = f.scene * dim
    floor(f, 556, 1215, 300, 40, ha)
    WIN.draw(f.lay, f.cam, ha); WIN.screen(f.lay, f.cam, screen_img(f), INS, ha); WIN.sheen(f.lay, f.cam, t, ha)
    # pixel
    pa = fade(t, c.CH[1] - 0.1, 1e9, 0.4, 0.1) * ha
    if pa > 0:
        p = f.T(st.PIX); r_ = 6 * s
        f.dr.rectangle([(p[0] - r_) * SS, (p[1] - r_) * SS, (p[0] + r_) * SS, (p[1] + r_) * SS], fill=rgba(OFF, pa))
        f.gd.rectangle([p[0] - 12, p[1] - 12, p[0] + 12, p[1] + 12], fill=rgba(VIO, pa))
        pr = ((t - c.CH[1]) % 1.4) / 1.4
        ring(f.dr, p, (12 + 40 * pr) * s, VIO, 0.6 * (1 - pr) * pa, 1.4)
    # signal -> meta -> account
    sa = fade(t, c.CH[2], c.VEND, 0.4, 0.5) * f.scene * dim
    if sa > 0:
        g = seg(t, c.CH[2] + 0.4, c.CH[2] + 1.3); path_line(f, [f.T(q) for q in st.C1.part(0, g)], sa)
        if g >= 1: particles(f, st.C1, sa, 8, 1.2)
        lit = fade(t, c.sub_t('Meta links'), 1e9, 0.3, 0.1)
        node(f, f.T(st.META), sa * g, lit, c.sub_t('Meta links'))
    # ad back to the phone + people like you
    aa = fade(t, c.CH[3], c.VEND, 0.4, 0.5) * f.scene * dim
    if aa > 0:
        cv = Curve([st.META, (700, 520), (300, 640), (150, 900), (st.PH[0], st.PH[1] - 110)])
        g = seg(t, c.CH[3] + 0.2, c.CH[3] + 1.2); path_line(f, [f.T(q) for q in cv.part(0, g)], aa)
        paste(f.lay, st.PHONE, f.T(st.PH), s, aa)
        ad = seg(t, c.CH[3] + 1.0, c.CH[3] + 1.4) * aa
        if ad > 0:
            p = f.T((st.PH[0], st.PH[1] - 20)); w_, h_ = 80 * s, 56 * s
            f.dr.rounded_rectangle([(p[0] - w_ / 2) * SS, (p[1] - h_ / 2) * SS, (p[0] + w_ / 2) * SS, (p[1] + h_ / 2) * SS], radius=int(6 * SS), fill=rgba(mixc(LIN, VIO, 0.5), ad))
            f.dr.text(((p[0] - w_ / 2 + 6) * SS, (p[1] + h_ / 2 + 6) * SS), 'Sponsored', font=UI(int(11 * SS)), fill=rgba(MUT, ad))
        for n_, q in enumerate(st.PEOPLE):
            g2 = seg(t, c.sub_t('and show it') + n_ * 0.2, c.sub_t('and show it') + 0.6 + n_ * 0.2)
            if g2 <= 0: continue
            faded_line(f, f.T((st.PH[0] + 60, st.PH[1])), f.T(q), aa * g2, 1.2); node(f, f.T(q), aa * g2)

def text(f):
    c, t, st = f.c, f.t, f.st
    pa = fade(t, c.CH[1] + 0.2, c.CH[2] + 0.6, 0.4, 0.5)
    p = f.T(st.PIX); label(f, (1036, p[1] + 60), 'PIXEL', 'INVISIBLE · 1 × 1', pa, 'r')
    sa = fade(t, c.CH[2] + 1.0, c.VEND, 0.4, 0.5) * (1 - 0.7 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5))
    p = f.T(st.META); label(f, (1036, p[1] - 100), 'META', 'LINKED TO YOUR ACCOUNT' if t > c.sub_t('Meta links') else '', sa, 'r')
    aa = fade(t, c.sub_t('and show it') + 0.4, c.VEND, 0.4, 0.5) * (1 - 0.7 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5))
    p = f.T(st.PEOPLE[2]); label(f, (p[0] + 40, p[1] + 20), 'PEOPLE', 'LIKE YOU', aa)
    cards(f, st.CARDS, c.VEND - 0.05)
