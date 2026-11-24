from kit import *

PH = None
INS = (16, 30, 16, 30)
def setup(c):
    global PH
    PH = Hero(400, 700, 680, 1290, 34, -18, radius=34, k=2.6)
    st = K()
    rr = np.random.default_rng(4)
    st.RAIN = [(rr.uniform(90, 990), rr.uniform(480, 1380), rr.uniform(0, 1)) for _ in range(34)]
    st.RAIN = [p for p in st.RAIN if not (360 < p[0] < 720 and 640 < p[1] < 1330)]
    st.post = spr_box(70, 86, r=8)[0]
    st.HIST = [(spr_tag('ACCOUNTS YOU FOLLOW'), (230, 560)), (spr_tag('TIME SPENT'), (180, 690)), (spr_tag('MESSAGES'), (190, 820))]
    st.RANK = [(870, 620 + i * 110) for i in range(6)]
    st.CARDS = [(1180, 'Shares and saves', 'WEIGH A LOT', c.sub_t('shares and saves') + 0.1, True)]
    return st

def feed_img(f):
    c, t = f.c, f.t; w, h = PH.screen_size(INS); k = SS
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((16 * k, 14 * k), '09:41', font=UI(13 * k), fill=rgba(MUT, 0.9))
    off = 0 if t < c.CH[4] else -260 * k * seg(t, c.CH[4] + 0.6, c.CH[4] + 1.4)
    for i in range(3):
        y0 = 50 * k + i * 260 * k + off + 260 * k * (t >= c.CH[4])
        d.ellipse([16 * k, y0, 40 * k, y0 + 24 * k], fill=rgba(LIN, 1)); d.line([48 * k, y0 + 12 * k, 140 * k, y0 + 12 * k], fill=rgba(MUT, 0.8), width=int(3 * k))
        d.rounded_rectangle([12 * k, y0 + 34 * k, w - 12 * k, y0 + 210 * k], radius=10 * k, fill=rgba(mixc(LIN, VIO, 0.2 + 0.25 * (i == 0)), 1))
        for j in range(4): d.ellipse([(16 + j * 34) * k, y0 + 220 * k, (34 + j * 34) * k, y0 + 238 * k], outline=rgba(MUT, 0.8), width=int(2 * k))
    if t >= c.CH[4]:
        y0 = 50 * k + off
        a = seg(t, c.CH[4] + 0.6, c.CH[4] + 1.4)
        d.rounded_rectangle([12 * k, y0 + 34 * k, w - 12 * k, y0 + 210 * k], radius=10 * k, outline=rgba(VIO, a), width=int(3 * k), fill=rgba(mixc(LIN, VIO, 0.5), 1))
        d.ellipse([16 * k, y0, 40 * k, y0 + 24 * k], fill=rgba(VIO, 1))
    return im

def scene(f):
    c, t, st, s = f.c, f.t, f.st, f.s
    dim = 1 - 0.6 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5)
    ha = f.scene * dim
    floor(f, 556, 1318, 250, 40, ha)
    PH.draw(f.lay, f.cam, ha); PH.screen(f.lay, f.cam, feed_img(f), INS, ha); PH.sheen(f.lay, f.cam, t, ha)
    ra = fade(t, c.CH[1], c.CH[4] + 0.6, 0.4, 0.5) * f.scene
    if ra > 0:
        for n_, (x, y, ph) in enumerate(st.RAIN):
            a = ra * seg(t, c.CH[1] + ph * 1.2, c.CH[1] + ph * 1.2 + 0.4)
            if t > c.sub_t('Then it ranks') - 0.3: a *= 1 - seg(t, c.sub_t('Then it ranks') - 0.3, c.sub_t('Then it ranks') + 0.3)
            p = f.T((x, y + 8 * math.sin(t + n_))); paste(f.lay, st.post, p, s * 0.8, a)
            ba = seg(t, c.CH[2] + 0.2 + ph * 1.5, c.CH[2] + 0.6 + ph * 1.5) * a
            if ba > 0:
                for j in range(4):
                    hgt = (8 + 26 * abs(math.sin(n_ * 3.1 + j * 1.7))) * s
                    q = (p[0] - 21 * s + j * 14 * s, p[1] + 52 * s)
                    f.dr.rectangle([(q[0] - 4 * s) * SS, (q[1] - hgt) * SS, (q[0] + 4 * s) * SS, q[1] * SS], fill=rgba(VIO if j == 3 else MUT, ba))
    ha3 = fade(t, c.CH[3], c.CH[4] + 0.4, 0.4, 0.5) * f.scene
    if ha3 > 0:
        for n_, (spr, q) in enumerate(st.HIST):
            u = seg(t, c.CH[3] + 0.3 + n_ * 0.6, c.CH[3] + 1.3 + n_ * 0.6)
            p = (lerp(q[0], 400, u), lerp(q[1], 900, u))
            paste(f.lay, spr, f.T(p), s * lerp(1.0, 0.4, u), ha3 * (1 - seg(u, 0.85, 1)) * seg(t, c.CH[3] + n_ * 0.6, c.CH[3] + n_ * 0.6 + 0.3))
    rk = fade(t, c.sub_t('Then it ranks'), c.CH[4] + 1.2, 0.3, 0.5) * f.scene
    if rk > 0:
        for i, q in enumerate(st.RANK):
            u = seg(t, c.sub_t('Then it ranks') + i * 0.12, c.sub_t('Then it ranks') + 0.4 + i * 0.12)
            p = f.T(q); paste(f.lay, st.post, p, s * 0.8, rk * u)
            if i == 0: ring(f.dr, p, 52 * s, VIO, rk * u, 2)

def text(f):
    c, t, st = f.c, f.t, f.st
    a = fade(t, c.CH[1] + 0.6, c.CH[2] + 0.2, 0.4, 0.5)
    label(f, (540, 1440), 'THOUSANDS OF CANDIDATES', '', a, 'm')
    a = fade(t, c.CH[2] + 0.6, c.CH[3] + 0.2, 0.4, 0.5)
    label(f, (540, 1440), 'WATCH · LIKE · SHARE · SAVE', '', a, 'm')
    rk = fade(t, c.sub_t('Then it ranks') + 0.4, c.CH[4] + 1.2, 0.3, 0.5)
    p = f.T(st.RANK[0]); label(f, (1036, p[1] - 140), 'RANKED', '#1 GOES FIRST', rk, 'r')
    cards(f, st.CARDS, c.VEND - 0.05)
