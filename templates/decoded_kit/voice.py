import json, sys, numpy as np, soundfile as sf
sys.path.insert(0, '/home/claude/decoded')
from scripts import EP
from kokoro_onnx import Kokoro
k = Kokoro('/home/claude/tts/kokoro-v1.0.onnx', '/home/claude/tts/voices-v1.0.bin')
SPOKEN = [("Law 09-08", "Law zero nine, zero eight"), ("CNSS", "C.N.S.S."), ("CNDP", "C.N.D.P."), ("VAT", "V.A.T."),
          ("\"Morocco2026!\"", "\"Morocco twenty twenty-six, exclamation mark\""), ("lmaw3id", "lmaw-aid"), ("nbdl", "nbeddel"),
          ("8 a.m.", "eight a.m."), ("IDs", "I.D.s"), ("API", "A.P.I.")]
GAP = {'.': 0.42, '?': 0.5, '!': 0.45, '…': 0.45, '"': 0.42}
def weight(c):
    w = len(c)
    if c.endswith(','): w += 6
    if c.endswith((':', ';')): w += 9
    if c.endswith(('.', '?', '!', '…', '"')): w += 8
    return w
for n in [int(a) for a in sys.argv[1:]] or sorted(EP):
    E = EP[n]; sr = 24000; out = [np.zeros(int(0.35 * sr), np.float32)]; t = 0.35; subs = []; sents = []
    for ch, s, chunks in E['SENT']:
        say = s
        for a, b in SPOKEN: say = say.replace(a, b)
        a_, sr = k.create(say, voice='af_heart', speed=0.97, lang='en-us'); a_ = a_.astype(np.float32)
        nz = np.where(np.abs(a_) > 0.008)[0]; a_ = a_[max(0, nz[0] - 500): nz[-1] + 1500]
        dur = len(a_) / sr; W = [weight(c) for c in chunks]; acc = 0
        for c, w in zip(chunks, W):
            st = t + dur * acc / sum(W); acc += w
            subs.append(dict(ch=ch, text=c, start=round(st, 3), end=round(t + dur * acc / sum(W), 3)))
        sents.append(dict(ch=ch, text=s, start=round(t, 3), end=round(t + dur, 3)))
        gap = GAP.get(s.strip()[-1], 0.4); out += [a_, np.zeros(int(gap * sr), np.float32)]; t += dur + gap
    sf.write(f'ep{n:02d}_voice.wav', np.concatenate(out), sr)
    json.dump(dict(subs=subs, sents=sents, voice_end=round(t, 3)), open(f'ep{n:02d}_timing.json', 'w'), ensure_ascii=False, indent=1)
    print(n, round(t, 1), flush=True)
