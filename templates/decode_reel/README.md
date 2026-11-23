# Décodé Reel template

Reference episode: Décodé #01 (faux SMS « colis en attente »).

1. `voice.py` – Kokoro TTS (voice ff_siwis, fr-fr, speed 0.9), one clip per subtitle chunk, writes voice.wav + timing.json (chapter, text, start, end).
2. `render.py` – renders the video from timing.json: dark #0D0B1F background, one central isometric object, violet node path, `// 0N — LABEL` chapter titles, burned-in subtitles, Nodal wordmark end card. Typography: Quicksand (fonts/, OFL) everywhere – no "//" or monospace labels; chapter labels = small ring + stem (like the N of the logo), number in violet, word in sentence case. Copy fonts/ to /home/claude/fonts/ or edit the font paths.
3. Ambient pad + mix: see the ffmpeg commands in the creation task; loudnorm I=-14.

For a new episode: keep the helpers, camera, background, subtitles, end card; replace the central object and the chapter scenes following the "Prompt visuel" column of the Décodé tab.
