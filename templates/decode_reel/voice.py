import json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro('/home/claude/tts/kokoro-v1.0.onnx', '/home/claude/tts/voices-v1.0.bin')
# (chapter, subtitle chunk, pause after in s)
CH = [
 (0, "Ce SMS connaît votre nom.", 0.25), (0, "Voici comment.", 0.6),
 (1, "Votre nom et votre numéro circulent déjà :", 0.2), (1, "sites piratés, formulaires, listes revendues.", 0.55),
 (2, "Un robot envoie le même message", 0.1), (2, "à des milliers de personnes,", 0.2), (2, "avec un lien vers une fausse page de suivi.", 0.55),
 (3, "Vous payez de petits « frais de livraison »…", 0.3), (3, "et vous donnez votre carte.", 0.6),
 (4, "Le réflexe : jamais de paiement", 0.1), (4, "depuis un lien reçu par SMS.", 0.3), (4, "Ouvrez vous-même l'application du transporteur.", 0.45),
 (4, "Partagez ça à quelqu'un qui attend un colis.", 0.4),
]
sr = 24000; out = [np.zeros(int(0.35 * sr), np.float32)]; t = 0.35; subs = []
for ch, txt, pause in CH:
    s, sr = k.create(txt, voice='ff_siwis', speed=0.9, lang='fr-fr')
    s = s.astype(np.float32)
    # trim leading/trailing silence
    nz = np.where(np.abs(s) > 0.01)[0]; s = s[max(0, nz[0] - 600): nz[-1] + 1200]
    subs.append(dict(ch=ch, text=txt, start=round(t, 3), end=round(t + len(s) / sr, 3)))
    out += [s, np.zeros(int(pause * sr), np.float32)]; t += len(s) / sr + pause
audio = np.concatenate(out); sf.write('voice.wav', audio, sr)
json.dump(dict(subs=subs, voice_end=round(t, 3)), open('timing.json', 'w'), ensure_ascii=False, indent=1)
print(round(t, 2)); [print(s['ch'], s['start'], s['end'], s['text']) for s in subs]
