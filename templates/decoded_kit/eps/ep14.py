from kit import *

CUBE = None
def setup(c):
    global CUBE
    CUBE = Hero(380, 860, 700, 1180, 44, -22, 0, 2.6, caps=False, glass=True)
    st = K()
    st.DOCS = [spr_doc(x, w=90, h=116) for x in ('ARTICLE', 'BOOK', 'EMAIL', 'FORUM', 'MANUAL', 'REPORT')]
    st.DP = [(130, 640), (250, 560), (130, 860), (950, 640), (830, 560), (950, 860)]
    st.WORDS = ['The', 'customer', 'wants', 'to', 'change', 'the', 'delivery', 'date.']
    st.CAND = [('change', 0.62), ('cancel', 0.21), ('book', 0.09)]
    st.CARDS = [(1060, "Your company's context", 'GIVE IT TO THE AI', c.sub_t('give it') + 0.1, True),
                (1175, 'What matters', 'ALWAYS CHECK IT', c.sub_t('and always') + 0.1, True)]
    return st

def scene(f):
    c, t, st, s = f.c, f.t, f.st, f.s
    dim = 1 - 0.6 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5)
    ha = f.scene * dim
    floor(f, 560, 1210, 270, 40, ha)
    CUBE.draw(f.lay, f.cam, ha); CUBE.sheen(f.lay, f.cam, t, ha)
    # inner network of nodes
    pts = [(430 + (i % 4) * 75, 920 + (i // 4) * 75) for i in range(16)]
    for i, p in enumerate(pts):
        for j in (i + 1, i + 4, i + 5):
            if j < 16 and (j != i + 1 or (i % 4) != 3) and (j != i + 5 or (i % 4) != 3):
                q = pts[j]; on = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * 3 + i * 0.7 + j))
                line(f, f.T(p), f.T(q), ha * 0.5 * on, 1.0, VIO, False)
        node(f, f.T(p), ha * 0.8, 0.5 + 0.5 * math.sin(t * 2 + i))
    # pages flowing in (chapter 1)
    a1 = fade(t, c.CH[1] - 0.1, c.CH[2] + 0.3, 0.4, 0.5) * f.scene
    for n_, (spr, q) in enumerate(zip(st.DOCS, st.DP)):
        if a1 <= 0: break
        u = ((t - c.CH[1] - n_ * 0.25) % 2.2) / 2.2 if t > c.CH[1] + n_ * 0.25 else 0
        p = (lerp(q[0], 540, ease(u)), lerp(q[1], 980, ease(u)))
        paste(f.lay, spr, f.T(p), s * lerp(0.9, 0.2, u), a1 * (1 - seg(u, 0.8, 1)))

def text(f):
    c, t, st = f.c, f.t, f.st
    td = f.td
    # sentence being written (chapters 2-3)
    a = fade(t, c.CH[2], c.CH[4] + 0.3, 0.4, 0.5)
    if a > 0:
        nshow = 4 + int(seg(t, c.sub_t('this is') if False else c.CH[2] + 2.5, c.CH[2] + 3.0)) + int(max(0, (t - c.CH[3]) / 0.45))
        nshow = min(nshow, len(st.WORDS))
        x = 80; y = 560; fnt = F(FD + 'InterDisplay-Medium.otf', 44)
        for i, w_ in enumerate(st.WORDS[:nshow]):
            col = VIO if i == nshow - 1 and t > c.CH[2] + 2.5 else TXT
            td.text((x, y), w_, font=fnt, fill=rgba(col, a)); x += td.textlength(w_ + ' ', font=fnt)
            if x > 960: x = 80; y += 56
        if nshow == 4:
            td.rounded_rectangle([x, y + 4, x + 120, y + 52], radius=8, outline=rgba(VIO, a), width=2)
        ca = fade(t, c.CH[2] + 0.4, c.CH[3] + 0.1, 0.3, 0.4)
        if ca > 0:
            for i, (w_, pr) in enumerate(st.CAND):
                yy_ = 660 + i * 52
                td.text((120, yy_), w_, font=UI(30), fill=rgba(TXT if i == 0 else MUT, ca))
                bw = 360 * pr * seg(t, c.CH[2] + 0.6 + i * 0.2, c.CH[2] + 1.2 + i * 0.2)
                td.rounded_rectangle([300, yy_ + 10, 300 + 360, yy_ + 26], radius=8, fill=rgba(LIN, ca * 0.6))
                td.rounded_rectangle([300, yy_ + 10, 300 + max(bw, 8), yy_ + 26], radius=8, fill=rgba(VIO if i == 0 else MUT, ca))
                spaced(td, (680, yy_ + 4), f'{int(pr * 100)} %', MONOS, rgba(VIO if i == 0 else MUT, ca), 0.1)
    a1 = fade(t, c.CH[1] + 0.3, c.CH[2] + 0.3, 0.4, 0.5)
    label(f, (540, 1240), 'BILLIONS OF SENTENCES', '', a1, 'm')
    a3 = fade(t, c.sub_t('and why it can') , c.CH[4] + 0.3, 0.3, 0.5)
    label(f, (540, 1240), 'FAST · CONFIDENT · SOMETIMES WRONG', '', a3, 'm')
    cards(f, st.CARDS, c.VEND - 0.05)
