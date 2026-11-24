#!/bin/bash
# usage: make.sh EP   -> renders out/Nodal_Decoded_EP_EN.mp4
set -e
cd /home/claude/decoded
EP=$1; P=$(printf "%02d" $EP)
read DUR N VEND < <(python3 kit.py $EP --info)
H=$((N/2))
python3 kit.py $EP tmp_${P}_a.mp4 0 $H > log_${P}_a.txt 2>&1 &
python3 kit.py $EP tmp_${P}_b.mp4 $H $N > log_${P}_b.txt 2>&1 &
PRESET=$(python3 -c "import sys;sys.path.insert(0,'.');from scripts import EP;print(EP[$EP]['music'])")
python3 music.py $DUR tmp_${P}_music.wav $VEND $PRESET
ffmpeg -v error -y -i ep${P}_voice.wav -i tmp_${P}_music.wav -filter_complex "[0:a]aresample=44100,aformat=channel_layouts=stereo,apad=whole_dur=$DUR,asplit=2[v][sc];[1:a]volume=-15dB[m];[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[md];[v][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5[a]" -map "[a]" -ar 48000 -c:a aac -b:a 192k tmp_${P}_mix.m4a
wait
printf "file tmp_${P}_a.mp4\nfile tmp_${P}_b.mp4\n" > tmp_${P}_list.txt
ffmpeg -v error -y -f concat -i tmp_${P}_list.txt -i tmp_${P}_mix.m4a -map 0:v -map 1:a -c copy -shortest -movflags +faststart out/Nodal_Decoded_${P}_EN.mp4
rm -f tmp_${P}_a.mp4 tmp_${P}_b.mp4
echo "OK $P $DUR"
