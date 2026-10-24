"""Cinematic score for the drama ad: tense minor act (piano, drone, heartbeat, clock),
an impact at the turn, then a warm, building major act. No samples.
usage: python3 music_drama.py out.wav [seconds] [turn_seconds]"""
import sys, wave, numpy as np
SR = 48000
T = float(sys.argv[2]) if len(sys.argv) > 2 else 47.0
TURN = float(sys.argv[3]) if len(sys.argv) > 3 else 14.0
N = int(SR * T); out = np.zeros((N, 2)); rng = np.random.default_rng(7)
nf = lambda m: 440 * 2 ** ((m - 69) / 12)

def add(sig, start, gain=1.0, pan=0.0):
    i = int(start * SR); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    out[i:i+n, 0] += sig[:n] * gain * (1 - pan); out[i:i+n, 1] += sig[:n] * gain * (1 + pan)

def piano(m, d=2.5, vel=1.0):
    t = np.arange(int(d * SR)) / SR; f = nf(m)
    s = sum(a * np.sin(2 * np.pi * f * k * (1 + 0.0004 * k * k) * t) * np.exp(-t * (1.2 + 0.9 * k)) for k, a in enumerate([1, .45, .25, .12, .06], 1))
    return s * np.minimum(1, t / 0.004) * vel

def pad(ms, d, att=1.2, bright=0.25):
    t = np.arange(int(d * SR)) / SR; s = np.zeros_like(t)
    for m in ms:
        for det in (-0.12, 0.0, 0.12):
            f = nf(m) * (1 + det / 100)
            s += sum((bright ** (k - 1)) / k * np.sin(2 * np.pi * f * k * t + k) for k in range(1, 6))
    env = np.minimum(1, t / att) * np.minimum(1, (d - t) / 0.8)
    return s * env / (len(ms) * 3)

def thump(d=0.35, f0=58):
    t = np.arange(int(d * SR)) / SR; f = f0 + 40 * np.exp(-t * 25)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11)

def tick():
    t = np.arange(int(0.03 * SR)) / SR
    return (np.sin(2 * np.pi * 3200 * t) + 0.5 * rng.standard_normal(len(t))) * np.exp(-t * 260)

# ---- act 1: A minor, tense
t = np.arange(int(TURN * SR)) / SR
drone = (np.sin(2 * np.pi * nf(33) * t) + 0.5 * np.sin(2 * np.pi * nf(40) * t)) * np.minimum(1, t / 3) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.15 * t))
add(drone, 0, 0.16)
mel = [(0.4, 57), (1.6, 60), (2.8, 64), (4.4, 62), (5.6, 60), (6.8, 59), (8.4, 57), (9.6, 60), (10.4, 64), (11.2, 65), (12.0, 64), (12.8, 63)]
for s0, m in mel:
    add(piano(m, 2.8, 0.9), s0, 0.22, 0.15); add(piano(m - 12, 2.8, 0.6), s0, 0.14, -0.15)
add(pad([45, 52, 57, 60], 6.0, 2.0, 0.2), 4.2, 0.16); add(pad([41, 48, 53, 57], 4.6, 1.5, 0.25), 9.6, 0.2)
for k in range(int(TURN)):  # clock
    add(tick(), 0.3 + k * 1.0, 0.07, 0.4)
hb = 0.86
x = 2.0
while x < TURN - 0.6:  # heartbeat, speeding up into the climax
    add(thump(), x, 0.35); add(thump(0.3, 52), x + 0.22, 0.22)
    x += hb; hb = max(0.5, hb * 0.965)
# riser into the turn
tr = np.arange(int(3.2 * SR)) / SR
riser = rng.standard_normal(len(tr)); riser = np.convolve(riser, np.ones(40) / 40, 'same') * (tr / 3.2) ** 2
add(riser, TURN - 3.4, 0.12)
# ---- impact + turn
ti = np.arange(int(2.5 * SR)) / SR
boom = np.sin(2 * np.pi * np.cumsum(70 * np.exp(-ti * 3) + 30) / SR) * np.exp(-ti * 2.2)
add(boom, TURN - 0.05, 0.6)
# ---- act 2: C major, warm and building (C - G - Am - F), 92 bpm
beat = 60 / 92; bar = 4 * beat
prog = [[48, 55, 60, 64], [43, 50, 55, 59], [45, 52, 57, 60], [41, 48, 53, 57]]
s0 = TURN + 0.4; k = 0
while s0 < T - 0.5:
    ch = prog[k % 4]; d = min(bar * 2, T - s0)
    lvl = min(1.0, 0.45 + 0.08 * k)
    add(pad(ch, d + 0.6, 0.7, 0.35), s0, 0.22 * lvl)
    for b in range(8):
        if s0 + b * beat < T - 1.0:
            add(piano(ch[(b % 3) + 1] + 12, 1.6, 0.7), s0 + b * beat, 0.11 * lvl, 0.2 * (-1) ** b)
    add(piano(ch[0] - 12, 3.0, 0.9), s0, 0.18 * lvl)
    if k >= 1:
        for b in range(8):
            if s0 + b * beat < T - 1.2:
                if b % 2 == 0: add(thump(0.3, 50), s0 + b * beat, 0.32 * lvl)
                hh = rng.standard_normal(int(0.05 * SR)) * np.exp(-np.arange(int(0.05 * SR)) / SR * 80)
                add(np.diff(hh, prepend=0), s0 + b * beat + beat / 2, 0.05 * lvl, 0.3)
    s0 += bar * 2; k += 1
add(pad([48, 55, 60, 64, 67], 4.5, 0.3, 0.3), T - 4.6, 0.22)
out *= np.minimum(1, np.arange(N) / SR / 0.3)[:, None] * np.minimum(1, (T - np.arange(N) / SR) / 2.0)[:, None]
out /= np.abs(out).max() / 0.85
w = wave.open(sys.argv[1], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype('<i2').tobytes()); w.close(); print('score', T, 's')
