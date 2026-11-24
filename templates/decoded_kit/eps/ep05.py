from kit import *

def setup(c):
    st = K()
    st.DB = spr_db(w=110, h=120)
    st.DBC = (540, 980)
    st.TAGS = [spr_tag(x) for x in ('NAME', 'NUMBER', 'EMAIL', 'EMPLOYER')]
    st.ESC = [(230, 700), (850, 690), (215, 1240), (865, 1250)]
    st.FOLD = [(170, 900), (910, 900), (540, 640)]
    st.PROF = (850, 1180)
    st.PHONE = spr_phone(w=90, h=168, bubble=True)
    st.PH = (215, 1160)
    st.CARDS = [(1270, 'A message that knows too much', 'BE WARY', c.sub_t('Be wary') + 0.1, True)]
    return st

def prof_card(k=SS):
    im, d = spr_box(250, 150, fill=rgba(OFF, 0.95), outline=rgba(OFF, 1), r=10)
    d.text((16 * k, 12 * k), 'PROFILE', font=MON(14 * k), fill=rgba(INK, 0.8))
    for i, (a, b) in enumerate([('Name', 'Y. Alami'), ('Phone', '06 •• •• 47'), ('Email', 'y.alami@…'), ('Employer', 'SARL ••••')]):
        d.text((16 * k, (38 + i * 26) * k), a, font=UI(15 * k), fill=rgba(MUT, 1)); d.text((110 * k, (38 + i * 26) * k), b, font=UIB(15 * k), fill=rgba(INK, 1))
    return im
PROF = prof_card()

def scene(f):
    c, t, st, s = f.c, f.t, f.st, f.s
    db_a = f.scene * (1 - 0.55 * seg(t, c.CH[3], c.CH[3] + 0.6) + 0.55 * seg(t, c.CH[4], c.CH[4] + 0.6))
    floor(f, 540, 1150, 220, 36, db_a)
    paste(f.lay, st.DB, f.T(st.DBC), s * 2.6, db_a)
    # crack
    ca = seg(t, c.sub_t('a stolen') - 0.2, c.sub_t('a stolen') + 0.4) * db_a
    if ca > 0:
        pts = [f.T(p) for p in [(520, 860), (548, 930), (530, 990), (556, 1060), (538, 1110)]]
        f.dr.line([(x * SS, y * SS) for x, y in pts], fill=rgba(VIO, ca), width=int(3 * SS)); f.gd.line(pts, fill=rgba(VIO, ca), width=6)
    # escaping tags
    ea = fade(t, c.sub_t('a stolen') + 0.2, c.CH[3] + 0.3, 0.4, 0.6) * f.scene
    for n_, (spr, dest) in enumerate(zip(st.TAGS, st.ESC)):
        u = seg(t, c.sub_t('a stolen') + 0.3 + n_ * 0.25, c.sub_t('a stolen') + 1.3 + n_ * 0.25)
        if u <= 0 or ea <= 0: continue
        # chapter 2: they get matched into the profile
        m = seg(t, c.sub_t('Names') + n_ * 0.3, c.sub_t('Names') + 0.9 + n_ * 0.3)
        p0 = (lerp(540, dest[0], u), lerp(980, dest[1], u)); p = (lerp(p0[0], st.PROF[0], m), lerp(p0[1], st.PROF[1], m))
        paste(f.lay, spr, f.T(p), s * lerp(1.0, 0.4, m), ea * (1 - seg(m, 0.8, 1)))
    # copies (chapter 2)
    ka = fade(t, c.CH[2], c.CH[3] + 0.2, 0.4, 0.6) * f.scene
    for n_, q in enumerate(st.FOLD):
        g = seg(t, c.CH[2] + n_ * 0.35, c.CH[2] + 0.6 + n_ * 0.35)
        if g <= 0: continue
        faded_line(f, f.T((540, 980)), f.T(q), ka * g, 1.2); dark_node(f, f.T(q), ka * g, 24)
    pa = fade(t, c.sub_t('Names') + 0.6, c.CH[4] + 0.2, 0.4, 0.6) * f.scene
    paste(f.lay, PROF, f.T(st.PROF), s, pa)
    # target (chapter 3)
    ta = fade(t, c.CH[3], c.CH[4] + 0.2, 0.4, 0.6) * f.scene
    if ta > 0:
        cv = Curve([(st.PROF[0] - 125, st.PROF[1] + 10), (600, 1260), (380, 1230), (st.PH[0] + 50, st.PH[1])])
        g = seg(t, c.CH[3] + 0.3, c.CH[3] + 1.2); path_line(f, [f.T(q) for q in cv.part(0, g)], ta, col=DEEP)
        paste(f.lay, st.PHONE, f.T(st.PH), s, ta)
        if g >= 1: packets(f, cv, ta, 3, 1.4, 'dark')
    # law shield (chapter 4)
    la = fade(t, c.CH[4] + 0.1, c.VEND, 0.5, 0.5) * f.scene
    if la > 0:
        p = f.T((540, 980)); r_ = 230 * s
        f.dr.ellipse([(p[0] - r_) * SS, (p[1] - r_ * 1.05) * SS, (p[0] + r_) * SS, (p[1] + r_ * 1.05) * SS], outline=rgba(VIO, la), width=int(3 * SS))
        f.wd.ellipse([p[0] - r_, p[1] - r_ * 1.05, p[0] + r_, p[1] + r_ * 1.05], outline=rgba(VIO, 0.6 * la), width=10)

def text(f):
    c, t, st = f.c, f.t, f.st
    al = fade(t, c.sub_t('In April') + 0.3, c.CH[2] + 0.2, 0.4, 0.5)
    p = f.T((540, 1150)); label(f, (p[0], p[1] + 34), 'CNSS · APRIL 2025', '', al, 'm')
    ka = fade(t, c.CH[2] + 0.4, c.CH[3] + 0.2, 0.4, 0.6)
    p = f.T(st.FOLD[2]); label(f, (p[0], p[1] - 80), 'COPIED · SOLD ON', '', ka, 'm')
    pa = fade(t, c.sub_t('Names') + 0.9, c.CH[4] + 0.2, 0.4, 0.6)
    p = f.T(st.PROF); label(f, (1036, p[1] + 96), 'MATCHED', '', pa, 'r')
    ta = fade(t, c.CH[3] + 0.6, c.CH[4] + 0.2, 0.4, 0.6)
    p = f.T(st.PH); label(f, (44, p[1] + 110), 'TARGETED MESSAGE', 'YOUR BANK · YOUR COMPANY', ta)
    la = fade(t, c.CH[4] + 0.4, c.VEND, 0.5, 0.5)
    p = f.T((540, 980)); label(f, (p[0], p[1] - 335), 'LAW 09-08 · CNDP', 'PROTECT · DECLARE', la, 'm')
    cards(f, st.CARDS, c.VEND - 0.05)
