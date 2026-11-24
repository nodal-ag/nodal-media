from kit import *

PH = None
INS = (16, 30, 16, 30)
def setup(c):
    global PH
    PH = Hero(400, 700, 680, 1290, 34, -18, radius=34, k=2.6)
    st = K()
    st.WORDS = [(spr_tag('NBDL'), (170, 640)), (spr_tag('BEDDEL'), (170, 820)), (spr_tag('CHANGE'), (910, 640)), (spr_tag('MOVE'), (910, 820))]
    st.MEAN = (540, 560)
    st.CARDS = [(1180, 'Connection n°1', 'COMING SOON', c.S(4) + 0.2, True)]
    return st

def chat_img(f):
    c, t = f.c, f.t; w, h = PH.screen_size(INS); k = SS
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, 50 * k], radius=12 * k, fill=rgba(mixc(INK, LIN, 0.35), 1))
    d.ellipse([12 * k, 12 * k, 38 * k, 38 * k], fill=rgba(VIO, 1)); d.text((48 * k, 16 * k), 'Cabinet Dr. Bennani', font=UIB(14 * k), fill=rgba(OFF, 1))
    a = seg(t, 0.3, 0.8)
    msg = 'Bghit nbdl lmaw3id'
    fB = UI(19 * k); mw = d.textlength(msg, font=fB)
    x1 = w - 12 * k; x0 = x1 - mw - 28 * k; y0 = 80 * k
    d.rounded_rectangle([x0, y0, x1, y0 + 46 * k], radius=14 * k, fill=rgba(DEEP, a))
    d.text((x0 + 14 * k, y0 + 11 * k), msg, font=fB, fill=rgba(OFF, a))
    hl = fade(t, c.CH[1] + 1.4, c.CH[2] + 0.2, 0.3, 0.4)
    if hl > 0:
        cx = x0 + 14 * k + d.textlength('Bghit nbdl lmaw', font=fB); cw = d.textlength('3', font=fB)
        d.rounded_rectangle([cx - 3 * k, y0 + 8 * k, cx + cw + 3 * k, y0 + 38 * k], radius=4 * k, outline=rgba(OFF, hl), width=int(2 * k))
    r = seg(t, c.CH[3] + 0.6, c.CH[3] + 1.2)
    if r > 0:
        y1 = 150 * k
        d.rounded_rectangle([12 * k, y1, w - 40 * k, y1 + 70 * k], radius=14 * k, fill=rgba(mixc(INK, LIN, 0.55), r))
        d.text((26 * k, y1 + 10 * k), 'Sure. Pick a new slot:', font=UI(16 * k), fill=rgba(OFF, r))
        for i, sl in enumerate(['Tue 10:00', 'Wed 15:30', 'Thu 09:00']):
            u = seg(t, c.sub_t('then it offers') + i * 0.25, c.sub_t('then it offers') + 0.3 + i * 0.25)
            yy_ = y1 + (86 + i * 50) * k
            d.rounded_rectangle([12 * k, yy_, w - 40 * k, yy_ + 40 * k], radius=12 * k, outline=rgba(VIO, u), width=int(2 * k))
            d.text((30 * k, yy_ + 10 * k), sl, font=UIB(16 * k), fill=rgba(VIO, u))
    return im

def scene(f):
    c, t, st, s = f.c, f.t, f.st, f.s
    dim = 1 - 0.6 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5)
    ha = f.scene * dim
    floor(f, 556, 1318, 250, 40, ha)
    PH.draw(f.lay, f.cam, ha); PH.screen(f.lay, f.cam, chat_img(f), INS, ha); PH.sheen(f.lay, f.cam, t, ha)
    wa = fade(t, c.CH[2], c.CH[3] + 0.8, 0.4, 0.5) * f.scene
    if wa > 0:
        mp = f.T(st.MEAN)
        for n_, (spr, q) in enumerate(st.WORDS):
            ta = c.CH[2] + 0.3 + n_ * 0.3
            u = seg(t, c.sub_t('nbdl, change') + n_ * 0.3, c.sub_t('all end up') + 0.2)
            p = (lerp(q[0], st.MEAN[0], u), lerp(q[1], st.MEAN[1], u))
            paste(f.lay, spr, f.T(p), s * lerp(1.2, 0.5, u), wa * seg(t, ta, ta + 0.4) * (1 - seg(u, 0.85, 1)))
            if 0 < u < 1: faded_line(f, f.T(p), mp, wa * 0.6, 1.0)
        node(f, mp, wa * seg(t, c.sub_t('all end up'), c.sub_t('all end up') + 0.4), fade(t, c.sub_t('all end up'), 1e9, 0.3, 0.1), c.sub_t('all end up'))

def text(f):
    c, t, st = f.c, f.t, f.st
    a = fade(t, c.CH[1] + 0.3, c.CH[2] + 0.2, 0.4, 0.5)
    label(f, (540, 1340), 'LATIN · ARABIC · DIGITS', '3 = AYN  ·  9 = QAF', a, 'm')
    wa = fade(t, c.sub_t('all end up'), c.CH[3] + 0.8, 0.3, 0.5)
    p = f.T(st.MEAN); label(f, (p[0], p[1] - 92), 'SAME MEANING', '', wa, 'm')
    ia = fade(t, c.CH[3], c.VEND, 0.4, 0.5) * (1 - 0.7 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5))
    label(f, (1036, 600), 'INTENT', 'CHANGE APPOINTMENT', ia, 'r')
    cards(f, st.CARDS, c.VEND - 0.05)
