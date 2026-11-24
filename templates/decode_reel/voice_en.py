import json, sys, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro('/home/claude/tts/kokoro-v1.0.onnx', '/home/claude/tts/voices-v1.0.bin')
VOICE = sys.argv[1] if len(sys.argv) > 1 else 'af_heart'
CH = [
 (0, "This text knows your name.", 0.25), (0, "Here's how.", 0.6),
 (1, "Your name and number are already out there:", 0.2), (1, "hacked websites, online forms, resold lists.", 0.55),
 (2, "A bot sends the same message", 0.1), (2, "to thousands of people,", 0.2), (2, "with a link to a fake tracking page.", 0.55),
 (3, "You pay a small “delivery fee”…", 0.3), (3, "and hand over your card.", 0.6),
 (4, "The rule: never pay through a link", 0.1), (4, "you got by text message.", 0.3), (4, "Open the courier's app yourself.", 0.45),
 (4, "Share this with someone waiting for a parcel.", 0.4),
]
sr = 24000; out = [np.zeros(int(0.35 * sr), np.float32)]; t = 0.35; subs = []
for ch, txt, pause in CH:
    s, sr = k.create(txt, voice=VOICE, speed=1.0, lang='en-us'); s = s.astype(np.float32)
    nz = np.where(np.abs(s) > 0.01)[0]; s = s[max(0, nz[0] - 600): nz[-1] + 1200]
    subs.append(dict(ch=ch, text=txt, start=round(t, 3), end=round(t + len(s) / sr, 3)))
    out += [s, np.zeros(int(pause * sr), np.float32)]; t += len(s) / sr + pause
sf.write(f'voice_en_{VOICE}.wav', np.concatenate(out), sr)
json.dump(dict(subs=subs, voice_end=round(t, 3)), open(f'timing_en_{VOICE}.json', 'w'), ensure_ascii=False, indent=1)
print(VOICE, round(t, 2))
