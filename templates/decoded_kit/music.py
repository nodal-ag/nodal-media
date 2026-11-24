"""Original ambient-tech music, one preset per episode. usage: music.py DUR OUT HIT PRESET"""
import sys, numpy as np, soundfile as sf
from scipy.signal import fftconvolve, butter, lfilter
DUR, OUT, HIT, PR = float(sys.argv[1]), sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
PRESETS = {
 1: dict(bpm=92, ch=[[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]], arp=[0, 1, 2, 4, 2, 1, 3, 2], cut=1800, hat=True, tone=0.25),
 2: dict(bpm=86, ch=[[50, 53, 57], [46, 50, 53], [53, 57, 60], [48, 52, 55]], arp=[0, 2, 1, 2, 3, 2, 1, 2], cut=1400, hat=False, tone=0.35),
 3: dict(bpm=98, ch=[[52, 55, 59], [48, 52, 55], [55, 59, 62], [50, 54, 57]], arp=[0, 1, 2, 3, 4, 3, 2, 1], cut=2200, hat=True, tone=0.2),
 4: dict(bpm=88, ch=[[54, 57, 61], [50, 54, 57], [57, 61, 64], [52, 56, 59]], arp=[2, 1, 0, 1, 2, 3, 4, 3], cut=1600, hat=True, tone=0.3),
 5: dict(bpm=82, ch=[[48, 51, 55], [44, 48, 51], [51, 55, 58], [46, 50, 53]], arp=[0, 2, 4, 2, 1, 3, 2, 1], cut=1200, hat=False, tone=0.4),
 6: dict(bpm=94, ch=[[55, 58, 62], [51, 55, 58], [58, 62, 65], [53, 57, 60]], arp=[0, 1, 2, 1, 3, 2, 4, 2], cut=2000, hat=True, tone=0.22),
}
P = PRESETS[PR]; sr = 44100; n = int(DUR * sr); t = np.arange(n) / sr
beat = 60 / P['bpm']; bar = 4 * beat
def hz(m): return 440 * 2 ** ((m - 69) / 12)
pad = np.zeros(n); arp = np.zeros(n); bass = np.zeros(n); kick = np.zeros(n); hat = np.zeros(n)
rng = np.random.default_rng(PR)
nb = int(DUR / bar) + 1
for b in range(nb):
    t0 = b * bar; ch = P['ch'][b % 4]; i0 = int(t0 * sr); i1 = min(n, int((t0 + bar + 0.6) * sr))
    if i0 >= n: break
    tt = np.arange(i1 - i0) / sr; env = np.minimum(1, tt / 0.5) * np.exp(-np.maximum(0, tt - bar) / 0.25)
    for m in ch:
        for det in (-0.06, 0.06):
            f = hz(m) * 2 ** (det / 12)
            pad[i0:i1] += env * sum(np.sin(2 * np.pi * f * h * tt + h) / h ** 1.6 for h in range(1, 7)) * 0.05
    for q in range(4):
        j0 = int((t0 + q * beat) * sr); j1 = min(n, j0 + int(beat * sr))
        if j0 >= n: break
        tq = np.arange(j1 - j0) / sr
        bass[j0:j1] += np.sin(2 * np.pi * hz(ch[0] - 24) * tq) * np.exp(-tq / 0.35) * 0.35
        if b >= 1 and q in (0, 2):
            f = 45 + 80 * np.exp(-tq / 0.04); kick[j0:j1] += np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-tq / 0.18) * 0.7
    tones = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 24, ch[0] + 24]
    for q, idx in enumerate(P['arp']):
        j0 = int((t0 + q * beat / 2) * sr); j1 = min(n, j0 + int(0.6 * sr))
        if j0 >= n: break
        tq = np.arange(j1 - j0) / sr; f = hz(tones[idx])
        arp[j0:j1] += (np.sin(2 * np.pi * f * tq) + P['tone'] * np.sin(4 * np.pi * f * tq)) * np.exp(-tq / 0.22) * 0.12
        if P['hat'] and b >= 2 and q % 2 == 1:
            hl = min(n, j0 + int(0.06 * sr)); hat[j0:hl] += rng.normal(0, 1, hl - j0) * np.exp(-np.arange(hl - j0) / sr / 0.015) * 0.05
bb, ab = butter(2, P['cut'] / (sr / 2)); pad = lfilter(bb, ab, pad)
bh, ah = butter(2, 7000 / (sr / 2), 'high'); hat = lfilter(bh, ah, hat)
duck = np.ones(n)
for b in range(1, nb):
    for q in (0, 2):
        j0 = int((b * bar + q * beat) * sr)
        if j0 >= n: continue
        j1 = min(n, j0 + int(0.4 * sr)); tq = np.arange(j1 - j0) / sr
        duck[j0:j1] = np.minimum(duck[j0:j1], 1 - 0.55 * np.exp(-tq / 0.12))
mix = pad * duck + arp * (0.7 + 0.3 * duck) + bass * duck + kick + hat
ir = rng.normal(0, 1, int(1.6 * sr)) * np.exp(-np.arange(int(1.6 * sr)) / sr / 0.45)
wet = fftconvolve(mix, ir)[:n]; wet /= np.max(np.abs(wet)) + 1e-9; mix = mix / (np.max(np.abs(mix)) + 1e-9)
mix = 0.78 * mix + 0.22 * wet
g = np.minimum(1, t / 1.5) * np.clip((DUR - t) / 2.2, 0, 1) * (1 + 0.35 * np.clip((t - HIT) / 0.6, 0, 1))
mix *= g; mix /= np.max(np.abs(mix)) + 1e-9
sf.write(OUT, (np.stack([mix, np.roll(mix, int(0.012 * sr)) * 0.96], 1) * 0.8).astype(np.float32), sr)
