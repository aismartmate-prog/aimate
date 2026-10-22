"""'Claude killed video editors' (Amir, organic): the edited 16:9 panel, frame by frame.

usage: python3 compose.py <v15 dir> [--start s --end s] [--out edited.mp4] [--stills t1,t2,...]
Inputs in <v15>: out/rough.mp4 (cut, 1920x1080@30), matte.mkv (person alpha, frame-aligned), plate.png (empty room),
hand.json (palm track), sp/*.png (sprites), coin/c00..59.png (3D coin turn), reels/r{k}_{i}.png (mini reels).
All times are on the rough-cut timeline (see the word list in rwords.json). The rough comes from smooth_cut.py
(cut.json), so every join is already smooth; the effects here ease across the joins instead of popping. Every effect sits on the word that
asks for it; the person is kept in front of 'behind' graphics with the matte.
"""
import argparse, json, math, subprocess, pathlib, numpy as np, cv2

W, H, FPS = 1920, 1080, 30
INK = np.array([15, 15, 17], np.float32) / 255
ORANGE = np.array([232, 105, 60], np.float32) / 255
CREAM = np.array([244, 239, 230], np.float32) / 255

# ---------------------------------------------------------------- timing (rough-cut seconds, on the spoken words)
T = dict(
    hook1=1.12, hook2=1.44, strike=1.95, realtime=3.82, snap1=4.28, hook_out=4.567, cut1=4.867, hook_end=5.09,
    zoom_in=6.77, coin=8.66, zoom_out=12.78, release=15.737, impact=15.967, crack_end=16.97,
    split=18.55, panel=19.11, hide=25.517, back=29.067, fold=29.517, fold_d=1.2, layers_end=30.75,
    tag1=33.24, tag2=34.34, stamp=35.54, tear=37.06, everyone=37.56, chip1=38.74, chip2=39.06, everyone_out=42.55,
    tagsmall=43.21, tiny=44.477, game=45.7, game_out=46.897,
    frame_r=48.423, frame_l=50.803, flip=51.5, head=52.003, s1=55.563, s2=60.363, s3=62.2, done=66.49, full=68.7,
    reels=70.547, reels_out=79.34, doc=82.4, st1=82.7, st2=83.1, st3=83.5, cut14=84.1, doc_end=84.35,
    cta=86.983, cta2=87.963, dm=88.623, end=91.5)
# cuts in the rough (smooth_cut.py, cut.json): morphs at 4.867 24.567 30.3 42.933 47.033 68.3 70.2 79.833 84.1,
# speed ramps at 12.267 66.267 75.533 84.9, a hard cut under the impact flash at 15.967 and under the card flip at 51.5

# ---------------------------------------------------------------- helpers
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def spring(t, w=14.0):
    """critically damped step response 0->1 (no bounce)."""
    if t <= 0: return 0.0
    return 1 - (1 + w * t) * math.exp(-w * t)
def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def win(t, a, b, fi=0.25, fo=0.25):
    if t < a or t > b + fo: return 0.0
    return min(eio((t - a) / fi) if fi > 0 else 1.0, 1 - eio((t - b) / fo) if fo > 0 else 1.0)

def load_rgba(p):
    im = cv2.imread(str(p), cv2.IMREAD_UNCHANGED)
    if im.shape[2] == 3: im = np.dstack([im, np.full(im.shape[:2], 255, np.uint8)])
    im = cv2.cvtColor(im, cv2.COLOR_BGRA2RGBA).astype(np.float32) / 255
    im[..., :3] *= im[..., 3:4]                      # premultiplied
    return im

def place(dst, spr, cx, cy, s=1.0, rot=0.0, alpha=1.0, blur=0.0):
    """composite a premultiplied RGBA sprite centred at (cx,cy), scaled and rotated (degrees)."""
    if alpha <= 0.002 or s <= 0.002: return
    if blur > 0.4:
        k = int(blur * 2) * 2 + 1; spr = cv2.GaussianBlur(spr, (k, k), blur)
    h, w = spr.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), -rot, s); M[0, 2] += cx - w / 2; M[1, 2] += cy - h / 2
    # only warp the bounding box region
    corners = np.array([[0, 0, 1], [w, 0, 1], [0, h, 1], [w, h, 1]], np.float32) @ M.T
    x0, y0 = np.floor(corners.min(0)).astype(int) - 2; x1, y1 = np.ceil(corners.max(0)).astype(int) + 2
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    if x1 <= x0 or y1 <= y0: return
    M2 = M.copy(); M2[0, 2] -= x0; M2[1, 2] -= y0
    p = cv2.warpAffine(spr, M2, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT) * alpha
    r = dst[y0:y1, x0:x1]; r *= (1 - p[..., 3:4]); r += p if dst.shape[2] == 4 else p[..., :3]

def place_quad(dst, img_rgba, quad, alpha=1.0):
    """warp a premultiplied RGBA image onto a 4-point quad (tl,tr,br,bl) and composite."""
    h, w = img_rgba.shape[:2]
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]]); q = np.float32(quad)
    x0, y0 = np.floor(q.min(0)).astype(int) - 2; x1, y1 = np.ceil(q.max(0)).astype(int) + 2
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    if x1 <= x0 or y1 <= y0: return
    P = cv2.getPerspectiveTransform(src, q - np.float32([x0, y0]))
    p = cv2.warpPerspective(img_rgba, P, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR) * alpha
    r = dst[y0:y1, x0:x1]; r *= (1 - p[..., 3:4]); r += p if dst.shape[2] == 4 else p[..., :3]

def view(img, s, cx, cy, interp=cv2.INTER_LINEAR):
    """zoom: scale s about source point (cx,cy), which lands at the frame centre."""
    if abs(s - 1) < 1e-3 and abs(cx - W / 2) < 0.5 and abs(cy - H / 2) < 0.5: return img
    M = np.float32([[s, 0, W / 2 - s * cx], [0, s, H / 2 - s * cy]])
    return cv2.warpAffine(img, M, (W, H), flags=interp, borderMode=cv2.BORDER_REFLECT)

def bg_dark(t):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * 0.45) / H) ** 2)
    g = np.clip(1 - d * 1.3, 0, 1)[..., None]
    return (INK + (np.array([34, 33, 40], np.float32) / 255 - INK) * g).astype(np.float32)

def rounded_mask(w, h, r):
    m = np.zeros((h, w), np.uint8)
    cv2.rectangle(m, (r, 0), (w - r, h), 255, -1); cv2.rectangle(m, (0, r), (w, h - r), 255, -1)
    for c in [(r, r), (w - r, r), (r, h - r), (w - r, h - r)]: cv2.circle(m, c, r, 255, -1, cv2.LINE_AA)
    return m.astype(np.float32) / 255

def make_crack(cx, cy, seed=3):
    """glass crack (premultiplied RGBA), drawn at 2x and downsampled for clean anti-aliasing."""
    rng = np.random.default_rng(seed); S = 2
    img = np.zeros((H * S, W * S, 4), np.float32)
    def line(p, q, wpx, col):
        cv2.line(img, (int(p[0] * S), int(p[1] * S)), (int(q[0] * S), int(q[1] * S)), col, max(1, int(wpx * S)), cv2.LINE_AA)
    rays = []
    for i in range(16):
        a = i / 16 * 2 * math.pi + rng.uniform(-0.15, 0.15); L = rng.uniform(500, 1400)
        pts = [(cx, cy)]; ang = a
        for k in range(9):
            ang += rng.uniform(-0.22, 0.22); seg = L / 9
            pts.append((pts[-1][0] + seg * math.cos(ang), pts[-1][1] + seg * math.sin(ang)))
        rays.append(pts)
        for k in range(len(pts) - 1):
            wpx = 3.2 * (1 - k / 9) + 0.8
            line(pts[k], pts[k + 1], wpx + 2, (0, 0, 0, 0.35)); line(pts[k], pts[k + 1], wpx, (1, 1, 1, 0.95))
    # rings connecting neighbouring rays
    for ring in (2, 4, 6):
        for i in range(16):
            if rng.random() < 0.75:
                p, q = rays[i][ring], rays[(i + 1) % 16][ring + rng.integers(-1, 2)]
                line(p, q, 1.6, (1, 1, 1, 0.85))
    # light shards near the centre
    for i in range(10):
        a = rng.uniform(0, 2 * math.pi); r0 = rng.uniform(20, 160)
        poly = np.array([[cx + r0 * math.cos(a + d) * S / S, cy + r0 * math.sin(a + d)] for d in (0, 0.25, 0.12)]) * S
        cv2.fillConvexPoly(img, poly.astype(np.int32), (1, 1, 1, 0.18), cv2.LINE_AA)
    cv2.circle(img, (int(cx * S), int(cy * S)), int(26 * S), (1, 1, 1, 0.9), -1, cv2.LINE_AA)
    img = cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA)
    img[..., :3] *= 1  # colours above are already premultiplied-ish (white*alpha below)
    img[..., :3] = img[..., :3] * img[..., 3:4]
    return img

# ---------------------------------------------------------------- 3D planes
def project(corners3, ry, rx, f=2200.0, cx=W / 2, cy=H / 2):
    cyr, syr, cxr, sxr = math.cos(ry), math.sin(ry), math.cos(rx), math.sin(rx)
    out = []
    for X, Y, Z in corners3:
        X1, Z1 = X * cyr + Z * syr, -X * syr + Z * cyr
        Y2, Z2 = Y * cxr - Z1 * sxr, Y * sxr + Z1 * cxr
        k = f / (f + Z2); out.append((cx + X1 * k, cy + Y2 * k))
    return out

class Comp:
    def __init__(self, d):
        self.d = pathlib.Path(d)
        sp = lambda n: load_rgba(self.d / 'sp' / f'{n}.png')
        self.S = {p.stem: sp(p.stem) for p in (self.d / 'sp').glob('*.png')}
        self.coin = [load_rgba(self.d / 'coin' / f'c{i:02d}.png') for i in range(60)]
        self.reels = [[load_rgba(self.d / 'reels' / f'r{k}_{i:02d}.png') for i in range(60)] for k in range(5)]
        pl = cv2.cvtColor(cv2.imread(str(self.d / 'plate.png')), cv2.COLOR_BGR2RGB).astype(np.float32) / 255
        self.plate = pl
        hand = json.load(open(self.d / 'hand.json'))
        self.hand = self._smooth_hand(hand)
        self.crack = make_crack(960, 470)
        self.dark = bg_dark(0)
        yy, xx = np.mgrid[-200:200, -200:200].astype(np.float32); g = np.exp(-(xx ** 2 + yy ** 2) / (2 * 70 ** 2))
        self.glow = np.dstack([ORANGE * g[..., None], g]).astype(np.float32)
        self.grain = np.random.default_rng(1).normal(0, 1, (H // 2, W // 2)).astype(np.float32)
        # text plane for the 3D split: the hook sentence, centred high
        tp = np.zeros((H, W, 4), np.float32); place(tp, self.S['textplane'], W / 2, 330, 1.25)
        self.textplane = tp
        # card frame (rounded) used in the frame/steps section
        self.cardW, self.cardH = 640, 900
        self.cardmask = rounded_mask(self.cardW, self.cardH, 46)
        self.paper = (CREAM[None, None] * np.ones((H, W, 1), np.float32)).astype(np.float32)

    def _smooth_hand(self, hand):
        ts = np.array([h['t'] for h in hand]); xs = []; ys = []; ss = []
        lx, ly, ls = 350.0, 865.0, 117.0
        for h in hand:
            if 'x' in h: lx, ly, ls = h['x'], h['y'], h['size']
            xs.append(lx); ys.append(ly); ss.append(ls)
        k = np.ones(5) / 5
        sm = lambda a: np.convolve(np.pad(a, 2, mode='edge'), k, 'valid')
        return ts, sm(np.array(xs)), sm(np.array(ys)), sm(np.array(ss))
    def palm(self, t):
        ts, xs, ys, ss = self.hand
        return float(np.interp(t, ts, xs)), float(np.interp(t, ts, ys)), float(np.interp(t, ts, ss))

    # ------------------------------------------------------------ the frame
    def frame(self, t, F, A):
        S = self.S; out = F.copy(); A3 = A[..., None]
        sfront = []                                      # (fn) graphics drawn after the main image
        # ---------- 1. hook: words behind the head, strike, 'real time' + REC, snap zoom
        if t < T['hook_end']:
            k1 = spring(t - T['hook1'], 12); k2 = spring(t - T['hook2'], 12)
            out_k = 1 - eio((t - T['realtime'] + 0.05) / 0.25)
            hf = 1 - eio((t - T['hook_out']) / 0.35)          # everything eases out across the cut to the hand shot
            dim = 1 - 0.30 * max(k1 * out_k, spring(t - T['realtime'], 10)) * hf
            beh = F * (1 - A3) * dim                     # background only, dimmed for contrast
            if out_k > 0:
                place(beh, S['hook1'], 960, 285 - 30 * (1 - k1), 1.25 * (0.92 + 0.08 * k1), alpha=k1 * out_k, blur=6 * (1 - k1))
                place(beh, S['hook2'], 960, 575 - 30 * (1 - k2), 1.25 * (0.92 + 0.08 * k2), alpha=k2 * out_k, blur=6 * (1 - k2))
                ks = eio((t - T['strike']) / 0.22)
                if ks > 0:                                # strike-through across both lines
                    x0, x1 = 300, 300 + (1320) * ks
                    cv2.line(beh, (int(x0), 470), (int(x1), 380), tuple(float(c) * out_k for c in ORANGE), 26, cv2.LINE_AA)
            kr = spring(t - T['realtime'], 11) * hf
            if kr > 0.002:
                place(beh, S['realtime'], 960, 330 - 26 * (1 - kr), 1.3 * (0.9 + 0.1 * kr), alpha=kr, blur=6 * (1 - kr))
            out = beh + F * A3
            if t > T['realtime']:
                blink = 1.0 if int((t - T['realtime']) * 2.2) % 2 == 0 else 0.35
                sfront.append(lambda o: place(o, S['rec'], 1760, 72, 1.0, alpha=spring(t - T['realtime'], 12) * blink * hf))
            zs = 1 + 0.12 * eio((t - T['snap1']) / 0.18) * (1 - eio((t - T['cut1'] + 0.2) / 0.4))
            out = view(out, zs, 960, 470)
        # ---------- 2. hand: zoom to the palm, 3D coin, throw, crack
        elif t < T['split']:
            px, py, psz = self.palm(t)
            zin = eio((t - T['zoom_in']) / 0.75); zout = eio((t - T['zoom_out']) / 0.9)
            z = 1 + 0.55 * zin * (1 - zout) + 0.08 * zout * (1 - eio((t - T['crack_end']) / 0.6))
            fx = 960 + (px - 960 + 120) * zin * (1 - zout)   # keep the palm left of centre, room for the coin above
            fy = 540 + (py - 160 - 540) * zin * (1 - zout)
            fx = clamp(fx, W / (2 * z), W - W / (2 * z)); fy = clamp(fy, H / (2 * z), H - H / (2 * z))
            img = view(out, z, fx, fy)
            to_scr = lambda x, y: ((x - fx) * z + W / 2, (y - fy) * z + H / 2)
            kc = spring(t - T['coin'], 10)
            if kc > 0 and t < T['impact']:
                spin = int((t - T['coin']) * 45) % 60
                if t < T['release']:
                    cx, cy = to_scr(px, py - psz * 1.55); cs = psz * 2.6 * z / 400
                    bob = 6 * math.sin((t - T['coin']) * 3.2) * z
                    # warm glow on the palm
                    gx, gy = to_scr(px, py - psz * 0.2)
                    place(img, self.glow, gx, gy, psz * 2.4 * z / 400, alpha=0.55 * kc)
                    place(img, self.coin[spin], cx, cy + bob, cs * (0.4 + 0.6 * kc), alpha=min(1, kc * 1.3), blur=3 * (1 - kc))
                else:
                    # flies to the lens: accelerates, grows, motion trail
                    u = clamp((t - T['release']) / (T['impact'] - T['release']))
                    sx, sy = to_scr(*self.palm(T['release'])[:2]); sy -= psz * 1.2 * z
                    for j, a in enumerate((0.25, 0.45, 1.0)):
                        uu = clamp(u - (2 - j) * 0.06); e = uu ** 2.2
                        cx = sx + (960 - sx) * e; cy = sy + (470 - sy) * e
                        cs = (psz * 2.6 * z / 400) * (1 + 9 * e)
                        place(img, self.coin[(spin + j * 3) % 60], cx, cy, cs, alpha=a, blur=8 * e)
            out = img
            if t >= T['impact'] - 2.5 / FPS and t < T['impact']:
                out = out + clamp((t - T['impact'] + 2.5 / FPS) / (2.5 / FPS)) * 0.8 * (1 - out)   # white builds as the coin hits
            if t >= T['impact']:
                u = t - T['impact']
                flash = 1.0 if u < 1.5 / FPS else 1 - eio((u - 1.5 / FPS) / 0.28)
                shake = 14 * math.exp(-u * 9) * math.sin(u * 70)
                if abs(shake) > 0.5: out = view(out, 1.0, 960 - shake, 540 + shake * 0.6)
                ka = 1 - eio((t - T['crack_end']) / 0.45)
                cr = self.crack * ka
                out = out * (1 - cr[..., 3:4]) + cr[..., :3]
                out = out * (1 - 0.15 * ka) + 0.15 * ka * 0.0          # slight darkening behind the glass
                out = out + flash * (1 - out)
        # ---------- 3-4. 3D layers, hide, bring back, fold
        elif t < T['layers_end']:
            u = spring(t - T['split'], 4.2) * (1 - eio((t - T['fold']) / T['fold_d']))
            if u < 0.002:
                out = F
            else:
                hide = eio((t - T['hide']) / 0.4) * (1 - eio((t - T['back']) / 0.35))
                drift = math.sin((t - T['split']) * 0.8) * 0.07
                ry = (-0.72 + drift) * u; rx = 0.16 * u; sep = 560 * u; g = 1 - 0.5 * u; pcx = W / 2 - 150 * u
                canvas = self.dark * u + F * (1 - u) * 0          # dark stage behind the planes
                canvas = self.dark.copy()
                hw, hh = W / 2 * g, H / 2 * g
                planes = [('wall', sep), ('me', 0.0), ('text', -sep)]
                quads = {}
                for name, z in planes:
                    q = project([(-hw, -hh, z), (hw, -hh, z), (hw, hh, z), (-hw, hh, z)], ry, rx, cx=pcx, cy=H / 2 - 30 * u)
                    quads[name] = q
                # wall: the empty room
                wall = np.dstack([self.plate, np.ones((H, W), np.float32)])
                place_quad(canvas, wall, quads['wall'], alpha=1.0)
                glass = np.zeros((8, 8, 4), np.float32); glass[...] = (0.07, 0.07, 0.08, 0.07)
                fo = 1 - eio((t - T['fold']) / 0.55)            # text plane, glass and edges leave first when folding
                place_quad(canvas, glass, quads['me'], alpha=clamp(u * 1.6) * fo)
                me = np.dstack([F * A3, A]); place_quad(canvas, me, quads['me'], alpha=1 - hide)
                place_quad(canvas, glass, quads['text'], alpha=clamp(u * 1.6) * fo)
                place_quad(canvas, self.textplane, quads['text'], alpha=clamp(u * 1.6) * fo)
                for name in ('wall', 'me', 'text'):
                    q = np.int32(np.round(quads[name]))
                    ov = canvas.copy(); cv2.polylines(ov, [q], True, (1, 1, 1), 2, cv2.LINE_AA)
                    canvas = canvas * (1 - 0.45 * fo) + ov * 0.45 * fo
                # crossfade from the flat frame at the start / end of the effect
                mix = clamp(u * 25)                               # only once the planes have (almost) re-aligned: no double image
                out = F * (1 - mix) + canvas * mix
                lab = clamp((u - 0.6) / 0.3)
                if lab > 0:
                    for name, key in (('wall', 'lbl_wall'), ('me', 'lbl_me'), ('text', 'lbl_text')):
                        q = quads[name]; c = q[0] if name == 'text' else q[3]; dy = -40 if name == 'text' else 42
                        place(out, S[key], c[0] + 95, c[1] + dy, 0.85, alpha=lab * (1 - 0.7 * hide if name == 'me' else 1))
                    if hide > 0:
                        q = quads['me']; mx, my = (q[0][0] + q[2][0]) / 2, (q[0][1] + q[2][1]) / 2
                        place(out, S['hidden'], mx, my, 1.0, alpha=hide)
                kp = spring(t - T['panel'], 9) * (1 - eio((t - T['fold']) / 0.4))
                if kp > 0:
                    pan = S['layers_off'] if hide > 0.5 else S['layers_on']
                    place(out, pan, 1690 + 140 * (1 - kp), 600, 1.0, alpha=kp)
        # ---------- 5. price tags, tear, 'every person', chips, game changer
        elif t < T['frame_r'] - 0.0:
            out = F.copy()
            ev = spring(t - T['everyone'], 11) * (1 - eio((t - T['everyone_out']) / 0.3))
            gm = spring(t - T['game'], 12) * (1 - eio((t - T['game_out']) / 0.25))
            if ev > 0 or gm > 0:
                beh = F * (1 - A3) * (1 - 0.3 * max(ev, gm))
                if ev > 0: place(beh, S['everyone'], 960, 300 - 24 * (1 - ev), 1.3 * (0.9 + 0.1 * ev), alpha=ev, blur=5 * (1 - ev))
                if gm > 0: place(beh, S['gamechanger'], 960, 320 - 24 * (1 - gm), 0.95 * (0.9 + 0.1 * gm), alpha=gm, blur=5 * (1 - gm))
                out = beh + F * A3
            zg = 0.09 * eio((t - T['game']) / 0.2) * (1 - eio((t - T['game_out']) / 0.35))
            if zg > 1e-4: out = view(out, 1 + zg, 960, 470)
            def tags(o):
                if T['tag1'] - 0.1 < t < T['tear'] + 1.4:
                    k1 = spring(t - T['tag1'], 9); swing = 14 * math.exp(-(t - T['tag1']) * 3) * math.cos((t - T['tag1']) * 9)
                    k2 = eio((t - T['tag2']) / 0.18); bump = 1 + 0.12 * math.sin(math.pi * clamp((t - T['tag2']) / 0.3))
                    tx, ty = 1460, 420; rot = swing
                    if t < T['tear']:
                        place(o, S['tag1'], tx, ty, 0.95 * k1, rot, alpha=k1 * (1 - k2))
                        place(o, S['tag2'], tx, ty, 0.85 * bump, rot, alpha=k2)
                        ks = spring(t - T['stamp'], 16)
                        if ks > 0: place(o, S['stamp'], tx + 30, ty + 120, 0.9 * (1.6 - 0.6 * ks), alpha=min(1, ks * 1.4))
                    else:
                        # torn in two: halves fall and turn away
                        u = t - T['tear']; tg = S['tag2']; h_, w_ = tg.shape[:2]
                        L = tg.copy(); R = tg.copy()
                        xs = np.arange(h_); cut = (w_ // 2 + 18 * np.sin(xs / 9.0)).astype(int)
                        cols = np.arange(w_)[None, :]
                        L[cols >= cut[:, None]] = 0; R[cols < cut[:, None]] = 0
                        fall = 900 * u * u
                        place(o, L, tx - 40 * u * 3, ty + fall, 0.85, -25 * u * 3, alpha=1 - clamp(u / 1.2))
                        place(o, R, tx + 40 * u * 3, ty + fall * 1.1, 0.85, 30 * u * 3, alpha=1 - clamp(u / 1.2))
                        place(o, S['stamp'], tx + 30, ty + 120 + fall * 1.2, 0.9, -40 * u, alpha=1 - clamp(u / 1.0))
                kc1 = spring(t - T['chip1'], 12) * (1 - eio((t - T['everyone_out']) / 0.3))
                kc2 = spring(t - T['chip2'], 12) * (1 - eio((t - T['everyone_out']) / 0.3))
                if kc1 > 0: place(o, S['chip_claude'], 1450, 760 + 20 * (1 - kc1), 1.1 * (0.85 + 0.15 * kc1), alpha=kc1, blur=4 * (1 - kc1))
                if kc2 > 0: place(o, S['chip_ai'], 470, 760 + 20 * (1 - kc2), 1.1 * (0.85 + 0.15 * kc2), alpha=kc2, blur=4 * (1 - kc2))
                ksm = spring(t - T['tagsmall'], 10) * (1 - eio((t - T['game'] + 0.1) / 0.25))
                if ksm > 0:
                    tiny = 1 - 0.55 * eio((t - T['tiny']) / 0.35)
                    place(o, S['tag_small'], 1470, 470, 0.9 * ksm * tiny, 8 * math.sin((t - T['tagsmall']) * 4), alpha=ksm)
            sfront.append(tags)
        # ---------- 6-8. into a card frame, right then left, steps, back to full
        elif t < T['full'] + 0.62:
            kr = spring(t - T['frame_r'], 6.5); kl = spring(t - T['frame_l'], 6.5); kf = eio((t - T['full']) / 0.6)
            if kr < 0.002:
                out = F
            else:
                k = kr * (1 - kf)
                # card target: portrait crop around the person; x moves screen-left, then screen-right
                cx_t = 420 + (1500 - 420) * kl
                cw = W + (self.cardW - W) * k; ch = H + (self.cardH - H) * k
                ccx = W / 2 + (cx_t - W / 2) * k; ccy = H / 2 + (560 - H / 2) * k
                # source crop that fills the card (person centred)
                src_w = W + (self.cardW / self.cardH * H - W) * k; src_h = H
                sx0 = 960 - src_w / 2
                crop = F[:, int(max(0, sx0)):int(min(W, sx0 + src_w))]
                card = cv2.resize(crop, (max(2, int(cw)), max(2, int(ch))), interpolation=cv2.INTER_AREA)
                r = int(46 * k); m = rounded_mask(card.shape[1], card.shape[0], max(1, r))[..., None]
                out = self.dark.copy()
                # steps content on the left (behind the card position, right-aligned to x≈1150)
                def ui(o):
                    pass
                x0 = int(ccx - card.shape[1] / 2); y0 = int(ccy - card.shape[0] / 2)
                ys0, xs0 = max(0, y0), max(0, x0); ys1, xs1 = min(H, y0 + card.shape[0]), min(W, x0 + card.shape[1])
                cc = card[ys0 - y0:ys1 - y0, xs0 - x0:xs1 - x0]; mm = m[ys0 - y0:ys1 - y0, xs0 - x0:xs1 - x0]
                # card flip on the cut (frames take -> steps take): edge-on exactly on the cut frame
                fp = (t - T['flip'] + 0.225) / 0.45
                if 0 < fp < 1:
                    th = math.pi * eio(fp); th = th if th <= math.pi / 2 else th - math.pi
                    ct = abs(math.cos(th))
                    sh = np.zeros((H // 4, W // 4), np.float32); hw_ = card.shape[1] * ct / 2
                    cv2.rectangle(sh, (int(ccx - hw_ + 10) // 4, int(y0 + 30) // 4), (int(ccx + hw_ - 10) // 4, int(y0 + card.shape[0] + 10) // 4), 1.0, -1)
                    sh = cv2.resize(cv2.GaussianBlur(sh, (0, 0), 8), (W, H))[..., None] * 0.55 * k
                    out = out * (1 - sh)
                    if ct > 0.02:
                        rgba = np.dstack([card * m * (0.72 + 0.28 * ct), m[..., 0]]).astype(np.float32)
                        cw2, ch2 = card.shape[1] / 2, card.shape[0] / 2
                        q = project([(-cw2, -ch2, 0), (cw2, -ch2, 0), (cw2, ch2, 0), (-cw2, ch2, 0)], th, 0, f=2200, cx=ccx, cy=ccy)
                        place_quad(out, rgba, q)
                else:
                    # soft shadow + hairline that follows the rounded corners
                    sh = np.zeros((H // 4, W // 4), np.float32); cv2.rectangle(sh, ((xs0 + 10) // 4, (ys0 + 30) // 4), ((xs1 - 10) // 4, (ys1 + 10) // 4), 1.0, -1)
                    sh = cv2.resize(cv2.GaussianBlur(sh, (0, 0), 8), (W, H))[..., None] * 0.55 * k
                    out = out * (1 - sh)
                    reg = out[ys0:ys1, xs0:xs1]; out[ys0:ys1, xs0:xs1] = reg * (1 - mm) + cc * mm
                    if k > 0.05:
                        ring = (mm[..., 0] - cv2.erode(mm[..., 0], np.ones((3, 3), np.uint8)))[..., None] * 0.4 * clamp((k - 0.05) / 0.3)
                        reg = out[ys0:ys1, xs0:xs1]; out[ys0:ys1, xs0:xs1] = reg + ring * (1 - reg)
                # steps card (left area) once the frame is on the right
                if t > T['head'] - 0.3:
                    ex = 1 - eio((t - T['full']) / 0.3)
                    def steps(o):
                        right = 1060; sc = 1.15
                        for key, tt, y in (('steps_head', T['head'], 300), ('step1', T['s1'], 560), ('step2', T['s2'], 685), ('step3', T['s3'], 810), ('done', T['done'], 945)):
                            kk = spring(t - tt, 11) * ex
                            if kk > 0:
                                spr = S[key]; w_ = spr.shape[1] * sc
                                place(o, spr, right - w_ / 2 + 30 * (1 - kk), y, sc, alpha=kk, blur=5 * (1 - kk))
                    sfront.append(steps)
        # ---------- 9. floating reels behind him
        elif t < T['doc']:
            kin = spring(t - T['reels'], 5) * (1 - eio((t - T['reels_out']) / 0.4))
            if kin < 0.002:
                out = F
            else:
                beh = F * (1 - A3) * (1 - 0.35 * kin)
                cards = [(300, 480, -0.38, 0.98), (640, 300, -0.2, 0.74), (1280, 300, 0.2, 0.74), (1620, 480, 0.38, 0.98)]
                for i, (x, y, ry, s) in enumerate(cards):
                    kk = spring(t - T['reels'] - i * 0.12, 6) * (1 - eio((t - T['reels_out']) / 0.4))
                    if kk <= 0: continue
                    fr_ = self.reels[(0, 1, 2, 3)[i]][int((t * 30 + i * 13)) % 60]
                    rgba = np.dstack([fr_[..., :3], np.ones(fr_.shape[:2], np.float32)])
                    mk = rounded_mask(fr_.shape[1], fr_.shape[0], 30)[..., None]; rgba = rgba * mk
                    cv2.rectangle(rgba, (1, 1), (rgba.shape[1] - 2, rgba.shape[0] - 2), (0.9, 0.9, 0.9, 0.9), 2, cv2.LINE_AA)
                    rgba[..., :3] *= 1
                    ww, hh = 360 * s * 1.05, 640 * s * 1.05
                    yy = y + 14 * math.sin(t * 1.4 + i) + 220 * (1 - kk)
                    rr = ry + 0.12 * math.sin(t * 0.9 + i * 1.7)
                    q = project([(-ww / 2, -hh / 2, 0), (ww / 2, -hh / 2, 0), (ww / 2, hh / 2, 0), (-ww / 2, hh / 2, 0)], rr, 0.05, f=1400, cx=x, cy=yy)
                    place_quad(beh, rgba, q, alpha=kk)
                out = beh + F * A3
        # ---------- 10. documentary
        elif t < T['doc_end']:
            k = eio((t - T['doc']) / 0.2) * (1 - eio((t - T['cut14'] + 0.2) / 0.4))
            if k <= 0:
                out = F
            else:
                gray = (F @ np.float32([0.3, 0.59, 0.11]))[..., None]
                gray = np.clip((gray - 0.5) * 1.35 + 0.5, 0, 1)
                bw = np.repeat(gray, 3, 2)
                bg = self.paper.copy()
                # big orange circle behind the head
                circ = np.zeros((H, W), np.float32); cv2.circle(circ, (960, 420), 380, 1.0, -1, cv2.LINE_AA)
                bg = bg * (1 - circ[..., None]) + ORANGE * circ[..., None]
                g = cv2.resize(self.grain, (W, H))[..., None] * 0.035
                doc = np.clip(bg * (1 - A3) + bw * A3 + g, 0, 1)
                out = F * (1 - k) + doc * k
                def stamps(o):
                    for key, tt, x, y in (('st1', T['st1'], 1490, 300), ('st2', T['st2'], 1500, 440), ('st3', T['st3'], 1470, 580)):
                        kk = spring(t - tt, 18)
                        if kk > 0: place(o, S[key], x, y, 1.0 * (1.5 - 0.5 * kk), alpha=min(1, kk * 1.5) * k)
                    kn = spring(t - T['doc'] - 0.3, 10)
                    place(o, S['docname'], 300, 930, 1.0, alpha=kn * k)
                    # letterbox bars
                    bar = int(70 * k); o[:bar] *= 0; o[H - bar:] *= 0
                sfront.append(stamps)
        # ---------- 11. CTA
        else:
            k = eio((t - T['cta']) / 0.25)
            if k <= 0:
                out = F
            else:
                shift = -380 * spring(t - T['cta'], 7)
                M = np.float32([[1, 0, shift], [0, 1, 0]])
                Fs = cv2.warpAffine(F, M, (W, H)); As = cv2.warpAffine(A, M, (W, H))[..., None]
                bg = self.paper.copy()
                circ = np.zeros((H, W), np.float32); cv2.circle(circ, (int(960 + shift), 430), 360, 1.0, -1, cv2.LINE_AA)
                bg = bg * (1 - circ[..., None] * 0.9) + ORANGE * circ[..., None] * 0.9
                cta = bg * (1 - As) + Fs * As
                out = F * (1 - k) + cta * k
                def ctatext(o):
                    k1 = spring(t - T['cta'] - 0.1, 11); k2 = spring(t - T['cta2'], 11); k3 = spring(t - T['dm'], 11)
                    place(o, S['cta1'], 1440, 300, 1.0 * (0.9 + 0.1 * k1), alpha=k1, blur=5 * (1 - k1))
                    place(o, S['cta2'], 1400, 520, 1.0 * (0.9 + 0.1 * k2), alpha=k2, blur=5 * (1 - k2))
                    place(o, S['dm'], 1420, 760, 1.0, alpha=k3, blur=4 * (1 - k3))
                sfront.append(ctatext)
        out = np.clip(out, 0, 1).astype(np.float32)
        for fn in sfront: fn(out)
        # persistent label, top-left (like the reference)
        kcc = 0.95 * (1 - win(t, T['doc'], T['cut14'] - 0.2, 0.2, 0.4)) * (1 - eio((t - T['cta']) / 0.25))
        if kcc > 0.002:
            place(out, S['cc'], 230, 70, 0.9, alpha=kcc)
        return np.clip(out, 0, 1)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('d'); ap.add_argument('--start', type=float, default=0)
    ap.add_argument('--end', type=float); ap.add_argument('--out'); ap.add_argument('--stills')
    a = ap.parse_args(); d = pathlib.Path(a.d); C = Comp(d)
    capF = cv2.VideoCapture(str(d / 'out/rough.mp4')); capA = cv2.VideoCapture(str(d / 'matte.mkv'))
    n0 = int(round(a.start * FPS)); n1 = int(round((a.end or T['end']) * FPS))
    if a.stills:
        for ts in a.stills.split(','):
            n = int(round(float(ts) * FPS)); capF.set(cv2.CAP_PROP_POS_FRAMES, n); capA.set(cv2.CAP_PROP_POS_FRAMES, n)
            _, f = capF.read(); _, m = capA.read()
            F = cv2.cvtColor(f, cv2.COLOR_BGR2RGB).astype(np.float32) / 255; A = m[..., 0].astype(np.float32) / 255
            o = C.frame(n / FPS, F, A)
            cv2.imwrite(str(d / 'peek' / f'st_{float(ts):06.2f}.jpg'), cv2.cvtColor((o * 255).astype(np.uint8), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 88])
        return
    capF.set(cv2.CAP_PROP_POS_FRAMES, n0); capA.set(cv2.CAP_PROP_POS_FRAMES, n0)
    cv2.setNumThreads(1)
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '8', '-threads', '1', '-pix_fmt', 'yuv420p', a.out or str(d / 'edited.mp4')], stdin=subprocess.PIPE)
    for n in range(n0, n1):
        ok, f = capF.read(); ok2, m = capA.read()
        if not ok: break
        F = cv2.cvtColor(f, cv2.COLOR_BGR2RGB).astype(np.float32) / 255
        A = (m[..., 0].astype(np.float32) / 255) if ok2 else np.zeros((H, W), np.float32)
        o = C.frame(n / FPS, F, A)
        ff.stdin.write((o * 255 + 0.5).astype(np.uint8).tobytes())
        if n % 150 == 0: print('frame', n, flush=True)
    ff.stdin.close(); ff.wait()

if __name__ == '__main__':
    main()
