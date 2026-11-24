from kit import *

TILL = STOCK = API = None
def setup(c):
    global TILL, STOCK, API
    TILL = Hero(90, 980, 300, 1200, 30, -15, 0, 2.4, caps=False, glass=True)
    STOCK = Hero(760, 980, 970, 1200, 30, -15, 0, 2.4, caps=False, glass=True)
    API = Hero(470, 860, 610, 1260, 30, -15, 0, 2.4, caps=True, glass=False)
    st = K()
    st.REQ = Curve([(302, 1040), (380, 1000), (430, 990), (468, 1000)])
    st.REQ2 = Curve([(612, 1000), (660, 990), (720, 1000), (758, 1040)])
    st.RES = Curve([(758, 1140), (700, 1160), (650, 1160), (612, 1150)])
    st.RES2 = Curve([(468, 1150), (420, 1160), (360, 1160), (302, 1140)])
    st.ask, st.ans = spr_tag('STOCK?'), spr_tag('12 IN STOCK')
    st.CARDS = [(1330, 'Nodal', 'THE WAITER BETWEEN YOUR TOOLS', c.S(5) + 0.2, True)]
    return st

def scene(f):
    c, t, st, s = f.c, f.t, f.st, f.s
    ha = f.scene
    floor(f, 530, 1290, 470, 40, ha)
    TILL.draw(f.lay, f.cam, ha); STOCK.draw(f.lay, f.cam, ha)
    aa = seg(t, c.CH[2] - 0.2, c.CH[2] + 0.6) * ha
    API.draw(f.lay, f.cam, aa); API.sheen(f.lay, f.cam, t, aa)
    for (x0, x1, lab) in [(90, 300, 'TILL'), (760, 970, 'STOCK')]:
        for i in range(4):
            y = 1030 + i * 34; w_ = (x1 - x0 - 60) * [0.8, 0.6, 0.7, 0.5][i]
            line(f, f.T((x0 + 30, y)), f.T((x0 + 30 + w_, y)), ha * 0.6, 2.0, MUT, False)
    # the human copying (chapters 0-1)
    ma = fade(t, 0.3, c.CH[2] + 0.2, 0.4, 0.5) * f.scene
    if ma > 0:
        hp = f.T((530, 760)); dot(f.dr, (hp[0], hp[1] - 34 * s), 18 * s, MUT, ma)
        f.dr.rounded_rectangle([(hp[0] - 30 * s) * SS, (hp[1] - 10 * s) * SS, (hp[0] + 30 * s) * SS, (hp[1] + 50 * s) * SS], radius=int(20 * SS), fill=rgba(MUT, ma))
        cv = Curve([(200, 960), (300, 780), (480, 740), (580, 740), (760, 780), (860, 960)])
        dashed(f, [f.T(q) for q in cv.pts], ma * 0.7, 1.4, MUT)
        u = (t * 0.35) % 1; paste(f.lay, spr_tag('COPY'), f.T(cv.at(u)), s * 0.8, ma * math.sin(math.pi * u))
    # request / answer (chapter 2)
    ra = fade(t, c.CH[2] + 0.3, c.VEND, 0.4, 0.5) * f.scene
    if ra > 0:
        for cv in (st.REQ, st.REQ2, st.RES, st.RES2): path_line(f, [f.T(q) for q in cv.pts], ra * 0.8)
        cyc = 3.2; u = ((t - c.CH[2]) % cyc) / cyc
        if u < 0.25: paste(f.lay, st.ask, f.T(st.REQ.at(u / 0.25)), s, ra)
        elif u < 0.5: paste(f.lay, st.ask, f.T(st.REQ2.at((u - 0.25) / 0.25)), s, ra)
        elif u < 0.75: paste(f.lay, st.ans, f.T(st.RES.at((u - 0.5) / 0.25)), s, ra)
        else: paste(f.lay, st.ans, f.T(st.RES2.at((u - 0.75) / 0.25)), s, ra)
        if t > c.CH[3]:
            for cv in (st.REQ, st.REQ2, st.RES, st.RES2): particles(f, cv, ra, 5, 1.0)

def text(f):
    c, t, st = f.c, f.t, f.st
    la = seg(t, 0.6, 1.2) * f.scene
    p = f.T((195, 1200)); label(f, (p[0], p[1] + 30), 'YOUR TILL', '', la, 'm')
    p = f.T((865, 1200)); label(f, (p[0], p[1] + 30), 'YOUR STOCK', '', la, 'm')
    aa = fade(t, c.CH[2] + 0.2, c.VEND, 0.4, 0.5)
    p = f.T((540, 860)); label(f, (p[0], p[1] - 90), 'API', 'THE WAITER', aa, 'm')
    ma = fade(t, 0.6, c.CH[2] + 0.2, 0.4, 0.5)
    p = f.T((530, 760)); label(f, (p[0], p[1] - 120), 'YOU · BY HAND', '', ma, 'm')
    cards(f, st.CARDS, c.VEND - 0.05)
