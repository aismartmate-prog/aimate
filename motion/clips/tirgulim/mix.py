"""Mix music + sound effects under the rendered ad and normalise to -14 LUFS.
usage: python3 mix.py video_silent.mp4 music.wav sfx_dir out.mp4 [voice.wav]"""
import subprocess, sys
video, music, sfx, out = sys.argv[1:5]; voice = sys.argv[5] if len(sys.argv) > 5 else None
T = 27.8
L = [[0.3, 2.9, 5], [3.1, 6.4, 5], [6.6, 9.6, 7], [9.8, 13.2, 6], [13.4, 16.6, 6], [16.8, 20.4, 7], [20.6, 23.4, 5], [23.6, 27.8, 3]]
wt = lambda i, j: L[i][0] + min(2.6, (L[i][1] - L[i][0]) * 0.72) * j / L[i][2]
ev = [('hit', 1.45, 0.5)]
ev += [('whoosh', x, 0.45) for x in [3.0, 6.45, 16.7, 20.6, 23.6]]
ev += [('swoosh-short', x, 0.4) for x in [9.8, 11.05, 13.4]]
ev += [('pop', x, 0.3) for x in [wt(2, 0), wt(2, 1), wt(2, 2), 10.15, 12.25, 12.7, 22.7, 24.6, 25.1]]
ev += [('pop', wt(5, j), 0.3) for j in [0, 1, 2, 3, 4, 6]]
ev += [('click', 26.1, 0.7)]
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
