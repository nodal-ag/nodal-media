from kit import *

PH = None
INS = (16, 30, 16, 30)
def setup(c):
    global PH
    PH = Hero(400, 700, 680, 1290, 34, -18, radius=34, k=2.6)
    st = K()
    st.SRC = [((175, 640), 'HACKED WEBSITES', 'db', c.sub_t('hacked')),
              ((905, 700), 'ONLINE FORMS', 'doc', c.sub_t('hacked') + 0.85),
              ((900, 1180), 'RESOLD LISTS', 'list', c.sub_t('resold'))]
    st.SPR = [spr_db(), spr_doc('FORM', w=96, h=124), spr_doc('LIST', w=96, h=124)]
    st.CUR = [Curve([(200, 700), (240, 790), (330, 760), (398, 800)]),
              Curve([(860, 740), (800, 800), (740, 790), (682, 860)]),
              Curve([(900, 1120), (850, 1030), (760, 1060), (682, 1020)])]
    st.TAGS = [spr_tag(x) for x in ('NAME', 'NUMBER', 'EMAIL')]
    st.ROBOT = (540, 560)
    crowd = []
    for (y, n, x0, x1) in [(700, 4, 120, 960), (900, 4, 110, 970), (1110, 4, 110, 970), (1320, 5, 130, 950)]:
        for j in range(n):
            x = lerp(x0, x1, j / (n - 1))
            if 330 < x < 750 and y < 1300: x = 150 + (j % 2) * 30 if x < 540 else 930 - (j % 2) * 30
            crowd.append((round(x), y))
    st.CROWD = sorted(set(crowd), key=lambda p: math.dist(p, st.ROBOT))
    st.MINI = spr_phone(bubble=True)
    st.PIR = (905, 1150)
    st.PIRC = Curve([(682, 1080), (780, 1080), (830, 1160), (879, 1150)])
    st.CARDS = [(1060, 'Paying through a text link', 'NEVER · FAKE PAGES', c.sub_t('The rule') + 0.3, False),
                (1175, "The courier's official app", 'OPENED BY YOU', c.sub_t('Open') + 0.2, True),
                (1290, 'Someone waiting for a parcel', 'SHARE THIS WITH THEM', c.sub_t('Share') + 0.2, True)]
    return st

def screen_img(f):
    c, t = f.c, f.t; w, h = PH.screen_size(INS); k = SS
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fS, fB, fBb, fT = UI(13 * k), UI(20 * k), UIB(20 * k), UIB(25 * k)
    page = seg(t, c.CH[3] - 0.1, c.CH[3] + 0.5) * (1 - seg(t, c.CH[4] + 0.2, c.CH[4] + 0.8)); sms = 1 - page
    d.text((16 * k, 14 * k), '09:41', font=fS, fill=rgba(MUT, 0.9))
    if sms > 0.01:
        ab = seg(t, 0.4, 1.0) * sms
        d.text((16 * k, 44 * k), 'Parcel-Post', font=fS, fill=rgba(MUT, ab))
        bx0, by0, bx1 = 12 * k, 70 * k, w - 14 * k
        lines = [('Hi ', 'Youssef', ','), ('your parcel is on', None, ''), ('hold. A delivery', None, ''), ('fee is due:', None, '')]
        by1 = by0 + (len(lines) * 28 + 56) * k
        d.rounded_rectangle([bx0, by0, bx1, by1], radius=14 * k, fill=rgba(mixc(INK, LIN, 0.55), ab))
        hl = min(1, fade(t, 0.5, c.CH[1] + 0.4, 0.4, 0.5) + 0.8 * sum(fade(t, s_[3] + 0.9, s_[3] + 1.9, 0.2, 0.4) for s_ in f.st.SRC))
        for i, (a_, nm, b_) in enumerate(lines):
            y = by0 + (14 + i * 28) * k; x = bx0 + 14 * k
            d.text((x, y), a_, font=fB, fill=rgba(OFF, ab)); x += d.textlength(a_, font=fB)
            if nm:
                nw = d.textlength(nm, font=fBb)
                if hl > 0: d.rounded_rectangle([x - 3 * k, y - 1 * k, x + nw + 3 * k, y + 25 * k], radius=5 * k, fill=rgba(VIO, 0.45 * hl * ab))
                d.text((x, y), nm, font=fBb, fill=rgba(OFF, ab)); x += nw; d.text((x, y), b_, font=fB, fill=rgba(OFF, ab))
        ly = by0 + (14 + len(lines) * 28) * k; lk = 'parcel-track.top/pay'
        gl = fade(t, c.sub_t('with a link'), c.CH[3] + 0.2, 0.3, 0.5); cut = seg(t, c.sub_t('The rule') + 0.4, c.sub_t('The rule') + 1.0)
        lc = mixc((170, 160, 255), (230, 226, 255), gl); lw_ = d.textlength(lk, font=fB)
        d.text((bx0 + 14 * k, ly), lk, font=fB, fill=rgba(lc, ab))
        d.line([bx0 + 14 * k, ly + 25 * k, bx0 + 14 * k + lw_, ly + 25 * k], fill=rgba(lc, ab * (0.6 + 0.4 * gl)), width=int(1.5 * k))
        if cut > 0: d.line([bx0 + 10 * k, ly + 13 * k, bx0 + 10 * k + (lw_ + 8 * k) * cut, ly + 13 * k], fill=rgba(OFF, ab), width=int(3 * k))
    if page > 0.01:
        a = page
        d.text((16 * k, 44 * k), 'Parcel tracking', font=fS, fill=rgba(MUT, a))
        d.text((16 * k, 66 * k), 'Awaiting', font=fT, fill=rgba(OFF, a)); d.text((16 * k, 96 * k), 'payment', font=fT, fill=rgba(OFF, a))
        d.rounded_rectangle([16 * k, 140 * k, w - 16 * k, 146 * k], radius=3 * k, fill=rgba(LIN, a))
        d.rounded_rectangle([16 * k, 140 * k, 16 * k + (w - 32 * k) * 0.72, 146 * k], radius=3 * k, fill=rgba(VIO, a))
        t0 = c.CH[3] + 0.7
        for i, (lab, val) in enumerate([('Card number', '•••• •••• •••• '), ('Expiry', '•• / ••'), ('CVV', '•••')]):
            y = (176 + i * 84) * k; lit = seg(t, t0 + i * 0.6, t0 + i * 0.6 + 0.3)
            d.text((16 * k, y), lab, font=fS, fill=rgba(MUT, a))
            d.rounded_rectangle([16 * k, y + 22 * k, w - 16 * k, y + 62 * k], radius=8 * k, fill=rgba(shade(INK, 0.8), a), outline=rgba(mixc(LIN, VIO, lit), a), width=int((1 + lit) * k))
            fu = seg(t, t0 + i * 0.6 + 0.1, t0 + i * 0.6 + 0.55); d.text((28 * k, y + 32 * k), val[:int(len(val) * fu)], font=fB, fill=rgba(OFF, a))
        by = (176 + 3 * 84 + 6) * k; press = fade(t, c.sub_t('and you hand'), c.CH[4], 0.2, 0.4)
        d.rounded_rectangle([16 * k, by, w - 16 * k, by + 50 * k], radius=25 * k, fill=rgba(mixc(DEEP, VIO, press), a))
        tw = d.textlength('PAY', font=fBb); d.text(((w - tw) / 2, by + 13 * k), 'PAY', font=fBb, fill=rgba(OFF, a))
    return im

def scene(f):
    c, t, st = f.c, f.t, f.st
    dimc = 1 - 0.6 * seg(t, st.CARDS[0][3] - 0.3, st.CARDS[0][3] + 0.5)
    ha = f.scene * dimc
    floor(f, 556, 1318, 250, 40, ha)
    # chapter 1: leak sources
    a1 = fade(t, c.CH[1] - 0.1, c.CH[2] + 0.4, 0.6, 0.7) * f.scene
    if a1 > 0:
        for n_, ((pos, lab, kind, ts), cv) in enumerate(zip(st.SRC, st.CUR)):
            ap = seg(t, c.CH[1] + n_ * 0.25, c.CH[1] + 0.7 + n_ * 0.25) * a1
            paste(f.lay, st.SPR[n_], f.T((pos[0], pos[1] + 3 * math.sin(TAU * t / 6 + n_))), f.s * 0.95, ap, [0, 8, -6][n_])
            grow = seg(t, ts - 0.3, ts + 0.5)
            path_line(f, [f.T(q) for q in cv.part(0, grow)], ap)
            if grow >= 1: particles(f, cv, ap * 0.9, 8, 1.4)
            u = seg(t, ts + 0.2, ts + 1.1)
            if 0 < u < 1: paste(f.lay, st.TAGS[n_], f.T(cv.at(u)), f.s * lerp(0.9, 0.3, u), ap * (1 - seg(u, 0.85, 1)))
            burst(f, f.T(cv.at(1)), ts + 1.1, ap)
    # chapter 2: bot -> crowd
    a2 = fade(t, c.CH[2], c.CH[3] + 0.2, 0.6, 0.6) * f.scene
    if a2 > 0:
        rp = f.T(st.ROBOT); node(f, rp, a2, 1.0)
        t_send = c.sub_t('A bot') + 0.6
        for n_, q in enumerate(st.CROWD):
            tq = t_send + n_ * 0.12; u = seg(t, tq, tq + 0.45)
            if u <= 0: continue
            qp = f.T(q); end = (lerp(rp[0], qp[0], u), lerp(rp[1], qp[1], u))
            faded_line(f, rp, end, a2 * (0.75 - 0.4 * seg(t, tq + 0.6, tq + 1.4)), 1.1, 12)
            if u >= 1: paste(f.lay, st.MINI, qp, f.s * 0.95, a2 * seg(t, tq + 0.4, tq + 0.7))
        u = seg(t, t_send - 0.4, t_send + 0.1); top = f.T((540, 694))
        if u > 0: faded_line(f, rp, (lerp(rp[0], top[0], u), lerp(rp[1], top[1], u)), a2, 1.6, 12)
    # phone
    PH.draw(f.lay, f.cam, ha); PH.screen(f.lay, f.cam, screen_img(f), INS, ha); PH.sheen(f.lay, f.cam, t, ha)
    # chapter 3: phone -> scammer
    a3 = fade(t, c.CH[3], c.CH[4] + 1.4, 0.5, 0.6) * f.scene
    if a3 > 0:
        th = c.sub_t('and you hand'); pa = seg(t, th - 0.3, th + 0.3) * a3
        cut = seg(t, c.sub_t('The rule') + 0.2, c.sub_t('The rule') + 0.8); grow = seg(t, th - 0.1, th + 0.6)
        if cut <= 0:
            path_line(f, [f.T(q) for q in st.PIRC.part(0, grow)], pa)
            if grow >= 1: packets(f, st.PIRC, pa, 4, 1.0, 'open')
        else:
            gap = 0.08 * cut
            path_line(f, [f.T(q) for q in st.PIRC.part(0, 0.5 - gap)], pa * (1 - 0.6 * cut))
            path_line(f, [f.T(q) for q in st.PIRC.part(0.5 + gap, 1)], pa * (1 - cut))
        dark_node(f, f.T(st.PIR), pa * (1 - 0.8 * cut))

def text(f):
    c, t, st = f.c, f.t, f.st
    for n_, (pos, lab, kind, ts) in enumerate(st.SRC):
        al = fade(t, ts - 0.1, c.CH[2] + 0.3, 0.4, 0.6)
        p = f.T(pos)
        if n_ == 0: label(f, (44, p[1] - 150), lab, '', al)
        elif n_ == 1: label(f, (1036, p[1] - 150), lab, '', al, 'r')
        else: label(f, (1036, p[1] + 82), lab, '', al, 'r')
    al = fade(t, c.CH[2] + 0.4, c.CH[3], 0.4, 0.5)
    if al > 0:
        rp = f.T(st.ROBOT); mlabel(f, (rp[0], rp[1] - 66), 'BOT · 1 MESSAGE', al)
        mlabel(f, (rp[0], rp[1] + 30), '× THOUSANDS', fade(t, c.sub_t('to thousands'), c.CH[3], 0.3, 0.5), VIO, MONOS)
    al = fade(t, c.sub_t('and you hand') + 0.2, c.sub_t('The rule') + 0.8, 0.4, 0.5)
    if al > 0:
        pp = f.T(st.PIR); mlabel(f, (pp[0], pp[1] + 52), 'SCAMMER', al); mlabel(f, (pp[0], pp[1] + 86), 'YOUR CARD', al, VIO, MONOS)
    cards(f, st.CARDS, c.VEND - 0.05)
