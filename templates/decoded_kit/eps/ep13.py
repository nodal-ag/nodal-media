from kit import *

TW = None
def inv(k=SS):
    w, h = 230, 300
    im = Image.new('RGBA', (w * k, h * k), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w * k - 1, h * k - 1], fill=rgba(OFF, 0.96))
    d.text((14 * k, 12 * k), 'INVOICE', font=MON(16 * k), fill=rgba(INK, 0.9))
    d.text((14 * k, 40 * k), 'Atlas Supply SARL', font=UIB(13 * k), fill=rgba(INK, 0.9))
    d.text((14 * k, 60 * k), '12/11/2026  · N° 0412', font=UI(11 * k), fill=rgba(INK, 0.7))
    for i in range(6):
        y = (96 + i * 20) * k; d.line([14 * k, y, 150 * k, y], fill=rgba(MUT, 0.8), width=int(2 * k)); d.line([170 * k, y, 214 * k, y], fill=rgba(MUT, 0.8), width=int(2 * k))
    d.text((14 * k, 232 * k), 'VAT 20 %', font=UI(11 * k), fill=rgba(INK, 0.7)); d.text((150 * k, 232 * k), '800,00', font=UI(11 * k), fill=rgba(INK, 0.7))
    d.text((14 * k, 256 * k), 'TOTAL', font=UIB(13 * k), fill=rgba(INK, 0.9)); d.text((136 * k, 256 * k), '4 800,00', font=UIB(13 * k), fill=rgba(INK, 0.9))
    return im
def rec(k=SS):
    im, d = spr_box(330, 210, fill=rgba(SURF, 0.96), outline=rgba(LIN, 1), r=12)
    d.text((22 * k, 16 * k), 'SUPPLIER RECORD', font=MON(15 * k), fill=rgba(MUT, 1))
    for i, (a, b) in enumerate([('Supplier', 'Atlas Supply'), ('Date', '12/11/2026'), ('Total', '4 800 MAD')]):
        y = (52 + i * 40) * k
        d.text((22 * k, y), a, font=UI(18 * k), fill=rgba(MUT, 1)); d.text((140 * k, y), b, font=UIB(18 * k), fill=rgba(OFF, 1))
    return im
INV, REC = None, None
ZONES = [((14, 34, 200, 76), 'SUPPLIER'), ((14, 56, 160, 74), 'DATE'), ((8, 250, 222, 276), 'TOTAL')]

def setup(c):
    global TW, INV, REC
    TW = tower(); INV = inv(); REC = rec()
    st = K()
    st.IP = (180, 1000)
    st.IN = Curve([(300, 900), (340, 820), (370, 760), (392, 748)])
    st.OUT = Curve([(688, 1322), (760, 1330), (850, 1260), (880, 1190)])
    return st

def scene(f):
    c, t, st, s = f.c, f.t, f.st, f.s
    ha = f.scene
    floor(f, 560, 1402, 270, 44, ha)
    TW.draw(f.lay, f.cam, ha); TW.sheen(f.lay, f.cam, t, ha)
    lit = [c.CH[2] + 0.6, c.CH[2] + 1.6, c.CH[3] + 0.2, c.CH[4]]
    engine_path(f, ha, nodes_t=lit)
    ia = seg(t, 0.4, 1.0) * f.scene * (1 - 0.4 * seg(t, c.CH[4], c.CH[4] + 0.6))
    p = f.T(st.IP); paste(f.lay, INV, p, s * 0.9, ia, -4)
    # pixels (chapter 1)
    pa = fade(t, c.CH[1], c.CH[2] + 0.2, 0.3, 0.5) * f.scene
    if pa > 0:
        w_, h_ = 230 * 0.9 * s, 300 * 0.9 * s; x0, y0 = p[0] - w_ / 2, p[1] - h_ / 2; n = 14
        for i in range(n + 1):
            f.dr.line([((x0 + i * w_ / n) * SS, y0 * SS), ((x0 + i * w_ / n) * SS, (y0 + h_) * SS)], fill=rgba(VIO, 0.35 * pa), width=SS)
            f.dr.line([(x0 * SS, (y0 + i * h_ / n) * SS), ((x0 + w_) * SS, (y0 + i * h_ / n) * SS)], fill=rgba(VIO, 0.35 * pa), width=SS)
    # zones (chapter 1 end + chapter 2)
    za = fade(t, c.sub_t('It finds'), c.CH[4] + 0.2, 0.3, 0.5) * f.scene
    if za > 0:
        w_, h_ = 230 * 0.9 * s, 300 * 0.9 * s; x0, y0 = p[0] - w_ / 2, p[1] - h_ / 2; k_ = 0.9 * s
        for n_, (b, lab) in enumerate(ZONES):
            u = seg(t, c.sub_t('It finds') + n_ * 0.3, c.sub_t('It finds') + 0.3 + n_ * 0.3)
            f.dr.rectangle([(x0 + b[0] * k_) * SS, (y0 + b[1] * k_) * SS, (x0 + b[2] * k_) * SS, (y0 + b[3] * k_) * SS], outline=rgba(VIO, za * u), width=2 * SS)
    # fields flow into the engine (chapter 2)
    fa = fade(t, c.CH[2], c.CH[4] + 0.4, 0.4, 0.5) * f.scene
    if fa > 0:
        path_line(f, [f.T(q) for q in st.IN.pts], fa); particles(f, st.IN, fa, 6, 1.2)
    # record out (chapter 4)
    ra = fade(t, c.CH[4], c.VEND, 0.4, 0.5) * f.scene
    if ra > 0:
        g = seg(t, c.CH[4], c.CH[4] + 0.8); path_line(f, [f.T(q) for q in st.OUT.part(0, g)], ra)
        u = seg(t, c.CH[4] + 0.6, c.CH[4] + 1.4); paste(f.lay, REC, f.T((lerp(700, 875, u), lerp(1320, 1090, u))), s * lerp(0.2, 0.95, u), ra * u)

def text(f):
    c, t, st = f.c, f.t, f.st
    pa = fade(t, c.CH[1] + 0.2, c.CH[2] + 0.2, 0.3, 0.5)
    p = f.T(st.IP); label(f, (44, p[1] - 260), 'PIXELS', 'FIRST, AN IMAGE', pa)
    for n_, (lab, sub) in enumerate([('SUPPLIER', ''), ('DATE', ''), ('TOTAL', '')]):
        tt = [c.sub_t('this is a supplier'), c.sub_t('this is a supplier') + 1.0, c.sub_t('this is a total')][n_]
        al = fade(t, tt, c.CH[3] + 0.2, 0.3, 0.5)
        p = f.T(ENGINE_PATH.at([0.2, 0.4, 0.6][n_])); right = p[0] > 520
        label(f, ((p[0] + 40) if right else (p[0] - 40), p[1] - 14), f'0{n_ + 1} · {lab}', '', al, 'l' if right else 'r')
    va = fade(t, c.CH[3] + 0.3, c.CH[4] + 0.2, 0.3, 0.5)
    p = f.T(ENGINE_PATH.at(0.8)); label(f, (p[0] + 40, p[1] - 14), '04 · VAT = TOTAL ✓', '', va)
    ra = fade(t, c.CH[4] + 1.4, c.VEND, 0.4, 0.5)
    label(f, (1036, 1225), 'COMPLETE', 'FILED IN THE RIGHT PLACE', ra, 'r')
