"""Mix music + sound effects under a rendered ad and normalise to -14 LUFS.
usage: python3 mix.py video_silent.mp4 music.wav sfx_dir events.json out.mp4 [voice.wav]
events.json: {"T": seconds, "events": [[sfx_name, time, volume], ...]}"""
import json, subprocess, sys
video, music, sfx, events, out = sys.argv[1:6]; voice = sys.argv[6] if len(sys.argv) > 6 else None
cfg = json.load(open(events)); T = cfg['T']; ev = cfg['events']
inp = ['-i', video, '-i', music]
f = [f'[1:a]volume={0.33 if voice else 0.5}[mus]']
for i, (n, t, v) in enumerate(ev):
    inp += ['-i', f'{sfx}/{n}.wav']; d = int(t * 1000)
    f.append(f'[{i+2}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={d}|{d},volume={v}[s{i}]')
mixin = '[mus]' + ''.join(f'[s{i}]' for i in range(len(ev)))
n = len(ev) + 1
if voice:
    inp += ['-i', voice]; f.append(f'[{len(ev)+2}:a]aformat=sample_rates=48000:channel_layouts=stereo[vo]'); mixin += '[vo]'; n += 1
f.append(f'{mixin}amix=inputs={n}:normalize=0:duration=longest,loudnorm=I=-14:TP=-1.5:LRA=11[a]')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(f), '-map', '0:v', '-map', '[a]', '-c:v', 'copy',
                '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-t', str(T), '-movflags', '+faststart', out], check=True)
print('wrote', out)
