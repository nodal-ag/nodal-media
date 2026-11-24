from kit import *

SAFE = None
INS = (0, 0, 0, 0)
def setup(c):
    global SAFE
    SAFE = Hero(380, 780, 700, 1150, 40, -20, 0, 2.6, caps=True, glass=False)
    st = K()
    st.DOCS = [spr_doc('LEAKED PASSWORDS', w=120, h=150), spr_doc('LEAKED PASSWORDS', w=120, h=150), spr_doc('COMBO LIST', w=120, h=150)]
    st.DPOS = [(160, 640), (150, 900), (170, 1160)]
    st.IN = Curve([(240, 900), (300, 930), (340, 960), (378, 965)])
    st.BLOCKS = [spr_tag('MOROCCO'), spr_tag('2026'), spr_tag('!')]
    st.PHRASE = [spr_tag(w_) for w_ in ('blue', 'tajine', 'sings', 'at', 'noon', 'in', 'fez')]
    st.CARDS = [(1060, 'A long phrase', 'DIFFERENT FOR EVERY SITE', c.CH[3] + 0.3, True),
                (1175, 'A password manager', 'KEEPS THEM ALL', c.sub_t('kept in') + 0.1, True),
                (1290, 'Two-factor authentication', 'EVERYWHERE', c.sub_t('And two-factor') + 0.1, True)]
    return st

def safe_img(f):
    c, t = f.c, f.t; w, h = SAFE.screen_size(INS); k = SS
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, cy, r_ = w / 2, h / 2 - 10 * k, 90 * k
    opened = seg(t, c.sub_t('and it') - 0.2, c.sub_t('and it') + 0.4) * (1 - seg(t, c.CH[3] - 0.2, c.CH[3] + 0.3))
    ang = t * 40 + 200 * seg(t, c.CH[2], c.sub_t('and it'))
    d.ellipse([cx - r_, cy - r_, cx + r_, cy + r_], outline=rgba(mixc(LIN, MUT, 0.5), 1), width=int(4 * k), fill=rgba(shade(INK, 0.7), 1))
    for i in range(24):
        a = math.radians(ang + i * 15); r1, r2 = r_ - 14 * k, r_ - (4 if i % 2 else 0) * k - 4 * k
        d.line([cx + r1 * math.cos(a), cy + r1 * math.sin(a), cx + r2 * math.cos(a), cy + r2 * math.sin(a)], fill=rgba(MUT, 0.8), width=int(2 * k))
    a = math.radians(ang); d.line([cx, cy, cx + (r_ - 30 * k) * math.cos(a), cy + (r_ - 30 * k) * math.sin(a)], fill=rgba(OFF, 1), width=int(4 * k))
    d.ellipse([cx - 10 * k, cy - 10 * k, cx + 10 * k, cy + 10 * k], fill=rgba(OFF, 1))
    lc = mixc(LIN, VIO, opened)
    d.rounded_rectangle([cx - 60 * k, h - 60 * k, cx + 60 * k, h - 34 * k], radius=13 * k, fill=rgba(lc, 1))
    tx = 'OPEN' if opened > 0.5 else 'LOCKED'; f2 = MON(15 * k)
    d.text((cx - d.textlength(tx, font=f2) / 2, h - 57 * k), tx, font=f2, fill=rgba(OFF, 1))
    return im

def scene(f):
    c, t, st, s = f.c, f.t, f.st, f.s
    dim = 1 - 0.6 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5)
    ha = f.scene * dim
    floor(f, 560, 1180, 260, 38, ha)
    SAFE.draw(f.lay, f.cam, ha); SAFE.screen(f.lay, f.cam, safe_img(f), INS, ha); SAFE.sheen(f.lay, f.cam, t, ha)
    a1 = fade(t, c.CH[1], c.CH[2] + 0.4, 0.5, 0.6) * f.scene
    if a1 > 0:
        for n_, (spr, q) in enumerate(zip(st.DOCS, st.DPOS)):
            paste(f.lay, spr, f.T((q[0], q[1] + 6 * math.sin(t * 1.3 + n_))), s * 0.9, a1 * seg(t, c.CH[1] + n_ * 0.3, c.CH[1] + 0.5 + n_ * 0.3), [-8, 6, -4][n_])
        g = seg(t, c.sub_t('They try'), c.sub_t('They try') + 0.8)
        path_line(f, [f.T(q) for q in st.IN.part(0, g)], a1)
        if g >= 1: packets(f, st.IN, a1, 6, 0.9, 'open')
    if True:
        for n_, spr in enumerate(st.BLOCKS):
            tb = c.sub_t('a word') + n_ * 0.55
            u = seg(t, tb, tb + 0.4)
            x = [400, 560, 680][n_]
            paste(f.lay, spr, f.T((x, 690 - 20 * (1 - u))), s * 1.3, u * fade(t, tb, c.CH[3] + 0.2, 0.3, 0.5))
    # long phrase (chapter 3)
    a3 = fade(t, c.CH[3], c.VEND, 0.4, 0.5) * f.scene
    if a3 > 0:
        x = 130
        for n_, spr in enumerate(st.PHRASE):
            u = seg(t, c.CH[3] + n_ * 0.18, c.CH[3] + 0.4 + n_ * 0.18)
            w_ = spr.width / SS * 1.25
            paste(f.lay, spr, f.T((x + w_ / 2, 680)), s * 1.25, a3 * u); x += w_ + 10
        p = f.T((540, 760)); g = 0.5 + 0.5 * math.sin(t * 2)
        dashed(f, [f.T((150, 980)), f.T((300, 900)), f.T((370, 860))], a3 * 0.5, 1.4, MUT)

def text(f):
    c, t, st = f.c, f.t, f.st
    a1 = fade(t, c.CH[1] + 0.6, c.CH[2] + 0.2, 0.4, 0.5)
    label(f, (44, 470), 'LEAKED LISTS', 'TRIED FIRST', a1)
    a2 = fade(t, c.sub_t('and it') + 0.2, c.CH[3] + 0.2, 0.3, 0.5)
    p = f.T((540, 1150)); label(f, (p[0], p[1] + 58), 'GUESSED EARLY', 'FOLLOWS EVERY RULE', a2, 'm')
    a3 = fade(t, c.CH[3] + 0.8, c.CH[3] + 3.0, 0.4, 0.5)
    label(f, (44, 590), 'A LONG PHRASE', 'TOO LONG TO GUESS', a3)
    cards(f, st.CARDS, c.VEND - 0.05)
