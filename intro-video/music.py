"""Synthesizes a 30s, 120 BPM house track that lines up with the video's cuts (drop at 2.0s, end card at 21.0s; 26s long)."""
import math, random, wave, array, sys
SR = 44100; DUR = 26.0; N = int(SR * DUR); BEAT = 0.5; DROP = 2.0
L = [0.0] * N; R = [0.0] * N
random.seed(4)
def add(start, samples, gain=1.0, pan=0.0):
    i0 = int(start * SR); gl = gain * (1 - max(pan, 0)); gr = gain * (1 + min(pan, 0))
    for j, s in enumerate(samples):
        i = i0 + j
        if i >= N: break
        if i >= 0: L[i] += s * gl; R[i] += s * gr
def note(n): return 440.0 * 2 ** ((n - 69) / 12)

def kick(dur=0.45):
    out = []; ph = 0
    for j in range(int(dur * SR)):
        t = j / SR; f = 48 + 110 * math.exp(-t * 28); ph += 2 * math.pi * f / SR
        out.append(math.sin(ph) * math.exp(-t * 7) * (1 + 0.3 * math.exp(-t * 200)))
    return out
def noise(dur, decay, hp=0.0):
    out = []; prev = 0.0; prevo = 0.0
    for j in range(int(dur * SR)):
        x = random.uniform(-1, 1); y = x - prev if hp else x; prev = x
        out.append(y * math.exp(-j / SR * decay))
    return out
def clap():
    o = noise(0.25, 18, 1)
    for burst in (0.0, 0.011, 0.022):
        b = int(burst * SR)
        for j in range(int(0.008 * SR)): o[b + j] *= 1.6
    return [s * 0.8 for s in o]
def synth(freqs, dur, attack=0.01, decay=3.0, bright=6, detune=0.004):
    out = []; phs = [[random.random() * 6.28 for _ in range(3)] for _ in freqs]
    for j in range(int(dur * SR)):
        t = j / SR; env = min(1, t / attack) * math.exp(-t * decay); s = 0
        for fi, f in enumerate(freqs):
            for d in range(3):
                ff = f * (1 + (d - 1) * detune); p = phs[fi][d] + 2 * math.pi * ff * t
                for h in range(1, bright + 1): s += math.sin(p * h) / h * 0.12
        out.append(s * env / len(freqs))
    return out
def bass(f, dur):
    out = []
    for j in range(int(dur * SR)):
        t = j / SR; env = min(1, t / 0.005) * math.exp(-t * 6)
        p = 2 * math.pi * f * t; out.append((math.sin(p) + 0.35 * math.sin(2 * p) + 0.15 * math.sin(3 * p)) * env)
    return out

K = kick(); C = clap(); HC = noise(0.05, 90, 1); HO = noise(0.22, 16, 1)
PROG = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]   # Am F C G
ROOT = [45, 41, 36, 43]

# intro (0-2): filtered pad, hats from 1s, riser + snare roll into the drop
add(0, synth([note(n) for n in PROG[0]], 2.2, attack=0.6, decay=0.3, bright=3), 0.55)
for i in range(8):
    add(1.0 + i * 0.125, HC, 0.12 + 0.1 * (i % 2), pan=0.3)
t = 1.5
while t < DROP - 0.02:
    add(t, C, 0.2 + 0.6 * (t - 1.5)); t += 0.0625
rs = []
for j in range(int(1.4 * SR)):
    tt = j / SR; rs.append(random.uniform(-1, 1) * (tt / 1.4) ** 2 * 0.35 + math.sin(2 * math.pi * (200 + 1400 * tt ** 2) * tt) * 0.08 * tt / 1.4)
add(0.6, rs)

def whoosh(dur=0.45):
    out = []; lp = 0.0
    for j in range(int(dur * SR)):
        u = j / (dur * SR); a = 0.02 + 0.5 * math.sin(math.pi * u) ** 2
        lp += a * (random.uniform(-1, 1) - lp); out.append(lp * math.sin(math.pi * u) ** 1.5 * 1.6)
    return out
for tw in (2.6, 6.5, 10.95, 14.9, 19.0, 20.45):
    add(tw, whoosh(), 0.5, pan=0.0)

# groove (2-30)
crash = noise(2.5, 1.6, 1)
add(DROP, crash, 0.35); add(21.0, crash, 0.35)
t = DROP; b = 0
while t < 25.5:
    bar = int((t - DROP) // 2) % 4
    add(t, K, 0.95)
    if b % 2 == 1: add(t, C, 0.5)
    add(t + 0.25, HO, 0.16, pan=-0.2)
    add(t + 0.125, HC, 0.07, pan=0.4); add(t + 0.375, HC, 0.07, pan=0.4)
    add(t + 0.25, bass(note(ROOT[bar]), 0.22), 0.45)
    if b % 4 in (0, 2) or b % 4 == 3: pass
    if b % 2 == 0: add(t + 0.25 + (0.25 if b % 4 == 2 else 0), synth([note(n + 12) for n in PROG[bar]], 0.3, decay=9, bright=5), 0.42, pan=0.15 if b % 4 else -0.15)
    if b % 8 == 0: add(t, synth([note(n) for n in PROG[bar]], 2.0, attack=0.3, decay=0.6, bright=2), 0.25)
    t += BEAT; b += 1
# little "pop" sounds on the in-app taps
for tw in (8.42, 9.87, 15.65):           # card swipes
    add(tw, whoosh(0.3), 0.22, pan=-0.3)
for tt in (6.76, 11.08, 11.95, 14.1, 14.65, 15.5):
    add(tt, [math.sin(2 * math.pi * 1400 * j / SR * (1 - j / 4000)) * math.exp(-j / SR * 60) for j in range(3000)], 0.18)

# master: fade out tail, soft clip, sidechain-ish ducking is baked into kick level
pk = max(max(abs(x) for x in L), max(abs(x) for x in R))
out = array.array('h')
for i in range(N):
    t = i / SR; f = 1 - max(0, (t - 24.9) / 1.1)
    for ch in (L, R):
        x = ch[i] / pk * 1.4 * f; x = math.tanh(x) * 0.9; out.append(int(x * 32767))
w = wave.open(sys.argv[1], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes()); w.close()
print('ok')
