"""One Kokoro call per full sentence (punctuation kept, so intonation follows it).
Subtitle chunks are timed inside each sentence by character weight, punctuation adds weight for its pause."""
import json, re, sys, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro('/home/claude/tts/kokoro-v1.0.onnx', '/home/claude/tts/voices-v1.0.bin')
VOICE, LANG, SPEED = 'af_heart', 'en-us', 0.97
SENT = [  # (chapter, sentence, subtitle chunks)
 (0, "A VPN doesn't make you invisible.", ["A VPN doesn't make you invisible."]),
 (1, "It creates an encrypted tunnel between your device and a server.", ["It creates an encrypted tunnel", "between your device and a server."]),
 (2, "Your internet provider can no longer see where you go: it only sees the tunnel.", ["Your internet provider can no longer", "see where you go:", "it only sees the tunnel."]),
 (2, "But the VPN server? It sees everything.", ["But the VPN server?", "It sees everything."]),
 (3, "And websites still recognise you: your accounts, your cookies, your browser's fingerprint.", ["And websites still recognise you:", "your accounts, your cookies,", "your browser's fingerprint."]),
 (4, "A proxy is just a middleman, often with no encryption at all.", ["A proxy is just a middleman,", "often with no encryption at all."]),
 (5, "A VPN protects you on an unsafe network, or connects you to your company's network.", ["A VPN protects you on an unsafe network,", "or connects you to your company's network."]),
 (5, "It won't make you disappear.", ["It won't make you disappear."]),
 (5, "Did you think it would? Tell us in the comments.", ["Did you think it would?", "Tell us in the comments."]),
]
GAP = {'.': 0.42, '?': 0.5, '!': 0.45}
def weight(c):
    w = len(c)
    if c.endswith((',',)): w += 6
    if c.endswith((':', ';')): w += 9
    if c.endswith(('.', '?', '!')): w += 8
    return w
sr = 24000; out = [np.zeros(int(0.35 * sr), np.float32)]; t = 0.35; subs = []; sents = []
for ch, s, chunks in SENT:
    a, sr = k.create(s, voice=VOICE, speed=SPEED, lang=LANG); a = a.astype(np.float32)
    nz = np.where(np.abs(a) > 0.008)[0]; a = a[max(0, nz[0] - 500): nz[-1] + 1500]
    dur = len(a) / sr; W = [weight(c) for c in chunks]; acc = 0
    for c, w in zip(chunks, W):
        st = t + dur * acc / sum(W); acc += w; en = t + dur * acc / sum(W)
        subs.append(dict(ch=ch, text=c, start=round(st, 3), end=round(en, 3)))
    sents.append(dict(ch=ch, text=s, start=round(t, 3), end=round(t + dur, 3)))
    gap = GAP.get(s.strip()[-1], 0.4)
    out += [a, np.zeros(int(gap * sr), np.float32)]; t += dur + gap
sf.write('voice.wav', np.concatenate(out), sr)
json.dump(dict(subs=subs, sents=sents, voice_end=round(t, 3)), open('timing.json', 'w'), ensure_ascii=False, indent=1)
print(round(t, 2)); [print(x['ch'], x['start'], x['end'], x['text']) for x in sents]
