import cv2, numpy as np, json, sys
im = cv2.imread('capi-referencia.jpg')[:, :, ::-1].astype(np.float32)
H, W = im.shape[:2]
# 1) paleta por k-means
px = im.reshape(-1, 3)
crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, .5)
K = 22
_, lab, cen = cv2.kmeans(px, K, None, crit, 4, cv2.KMEANS_PP_CENTERS)
lab = lab.reshape(H, W)
cnt = np.bincount(lab.ravel(), minlength=K).astype(float)
remap = list(range(K))
for i in np.argsort(-cnt):
    for j in np.argsort(-cnt):
        if cnt[j] > cnt[i] and remap[j] == j and np.abs(cen[i] - cen[j]).max() < 14: remap[i] = j; break
keep = sorted(set(remap)); idx = {k: n for n, k in enumerate(keep)}
lab = np.array([idx[remap[i]] for i in range(K)])[lab]
cen = cen[keep]; K = len(keep)
# 2) filtro de moda (tira as franjas de antialias)
def mode(lab, k):
    best = None; bc = None
    for i in range(K):
        c = cv2.blur((lab == i).astype(np.float32), (k, k))
        if best is None: best = c; bc = np.zeros_like(lab)
        else: m = c > best; best[m] = c[m]; bc[m] = i
    return bc
lab = mode(lab, 7); lab = mode(lab, 5)
def clean(lab, min_px=500):
    bad = np.zeros(lab.shape, bool)
    for i in range(K):
        n, c, st, _ = cv2.connectedComponentsWithStats((lab == i).astype(np.uint8), connectivity=4)
        small = np.where(st[:, 4] < min_px)[0]; small = small[small > 0]
        if len(small): bad |= np.isin(c, small)
    lab2 = lab.copy(); lab2[bad] = -1
    for it in range(40):
        if not (lab2 == -1).any(): break
        best = None; bc = None
        for i in range(K):
            c = cv2.blur((lab2 == i).astype(np.float32), (5, 5))
            if best is None: best = c; bc = np.zeros_like(lab2)
            else: m = c > best; best[m] = c[m]; bc[m] = i
        fill = (lab2 == -1) & (best > 0); lab2[fill] = bc[fill]
    lab2[lab2 == -1] = lab[lab2 == -1]
    return lab2
lab = clean(lab)
hexs = ['#%02x%02x%02x' % tuple(int(round(v)) for v in c) for c in cen]
def nearest(rgb): return int(np.argmin(((cen - np.array(rgb, np.float32)) ** 2).sum(1)))
BG = nearest((246, 246, 243)); SH = nearest((217, 219, 217)); OUT = nearest((72, 25, 12)); SKIN = nearest((224, 166, 121))
EYE = nearest((34, 13, 7)); BROWN = nearest((165, 108, 86)); BLUSH = nearest((241, 139, 114)); YEL = nearest((252, 207, 42))
print('pal', hexs, 'BG', BG, 'SH', SH, 'OUT', OUT, 'SKIN', SKIN, 'EYE', EYE, file=sys.stderr)
# simetria: acha o eixo do corpo e espelha a metade esquerda na direita (a laranja/folha usam a imagem original)
labOrig = lab.copy()
fg0 = (lab != BG) & (lab != SH)
best = None
for a2 in range(1484, 1500):          # eixo = a2/2 (passos de meio pixel)
    xs_ = np.arange(W); mx = a2 - xs_
    ok = (mx >= 0) & (mx < W)
    m1 = fg0[600:1900][:, ok]; m2 = fg0[600:1900][:, mx[ok]]
    err = (m1 != m2).sum()
    if best is None or err < best[0]: best = (err, a2)
A2 = best[1]; print('eixo', A2 / 2, best[0], file=sys.stderr)
xs_ = np.arange(W); src_x = np.where(xs_ > A2 / 2, A2 - xs_, xs_)
src_x = np.clip(src_x, 0, W - 1)
lab = lab[:, src_x]
# orelha: a sombrinha escura dentro da orelha vira o marrom (forma mais limpa: só o miolo e o risco)
Yg, Xg = np.mgrid[0:H, 0:W]
for ex in (452, A2 - 452):
    z = np.hypot(Xg - ex, Yg - 616) < 150
    lab[z & (lab == nearest((142, 87, 67)))] = nearest((165, 108, 86))
    srcm = cv2.imread('capi-referencia.jpg')[:, :, ::-1].astype(int)[:, src_x]
    lab[z & (lab == nearest((72, 25, 12))) & (srcm[:, :, 0] > 112)] = nearest((165, 108, 86))   # sombrinha marrom que tinha virado contorno
# risquinho de pelo bem no meio (o espelho duplicava): some
TK = nearest((203, 142, 103))
n_, c_, st_, _ = cv2.connectedComponentsWithStats((lab == TK).astype(np.uint8))
for i in range(1, n_):
    x0_, w_ = st_[i, 0], st_[i, 2]
    if x0_ - 6 <= A2 / 2 <= x0_ + w_ + 6 and st_[i, 4] < 3000: lab[c_ == i] = nearest((224, 166, 121))
fg = (lab != BG) & (lab != SH)
# remove poeira fora do bicho
n, cc, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8))
big = np.argmax(st[1:, 4]) + 1
fg = cc == big
fg = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)) > 0
lab[~fg] = BG
# o que estiver dentro da silhueta e foi rotulado fundo/sombra (brilhos brancos) fica como está (branco)
Y, X = np.mgrid[0:H, 0:W]
# ---------- partes ----------
# laranja: disco + caixa da folha/cabinho; linha do topo da cabeça estimada pelas colunas vizinhas
ocx, ocy = 747, 420
d = np.hypot(X - ocx, Y - ocy)
def top_edge(x):
    col = fg[300:700, x]; return 300 + int(np.argmax(col))
xs = list(range(520, 604, 4)) + list(range(918, 990, 4))
ys = [top_edge(x) for x in xs]
pa = np.polyfit(xs, ys, 2)
topY = np.polyval(pa, X)
# espessura do contorno no topo da cabeça
thick = []
for x in xs:
    t = top_edge(x); c = lab[t:t + 80, x]; thick.append(int(np.argmax(c != OUT)))
TH = int(np.median(thick))
print('topo', pa, 'esp', TH, file=sys.stderr)
# raio do disco da laranja (contorno externo)
row = fg[ocy, :]; L = ocx - np.argmax(~row[ocx::-1]); R = ocx + np.argmax(~row[ocx:])
r_out = (R - L) / 2 + 1; ocx = (L + R) / 2
d = np.hypot(X - ocx, Y - ocy)
cl = lab[ocy, int(L):int(R)]; f0 = int(np.argmax(cl == OUT)); r_in = r_out - f0 - int(np.argmax(cl[f0:] != OUT))
print('laranja', ocx, r_out, r_in, file=sys.stderr)
fruitZone = ((d <= r_out + 2) | ((X > 660) & (X < 930) & (Y < 345))) & (Y < topY + TH + 40)
fruit = fg & fruitZone & ((Y < topY) | (d <= r_out + 2))
fruitLab = lab.copy()
# completa o contorno de baixo da laranja (escondido pela cabeça)
m = fruit & (Y >= topY - 2) & (d > r_in); fruitLab[m] = OUT
# corpo: tira a laranja e redesenha a faixa do contorno do topo da cabeça por baixo dela
bodyLab = lab.copy(); body = fg.copy()
body[fruit & (Y < topY)] = False
band = (d <= r_out + 2) & (Y >= topY) & (Y < topY + TH); bodyLab[band] = OUT; body[band] = True
bulge = (d <= r_out + 4) & (Y >= topY + TH) & (bodyLab == OUT); bodyLab[bulge] = SKIN
# olhos: componentes da cor do olho no rosto + brilhos dentro
eyes = np.zeros_like(fg)
for cx, cy in [(500, 680), (995, 680)]:
    m = ((lab == EYE) | (lab == OUT)) & (np.hypot(X - cx, Y - cy) < 85)
    nn, c2, s2, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8))
    k = c2[cy, cx] if c2[cy, cx] else np.argmax(s2[1:, 4]) + 1
    e = c2 == k
    e = cv2.morphologyEx(e.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8)) > 0
    from scipy import ndimage
    e = ndimage.binary_fill_holes(e)
    eyes |= e
# bochechas: cor de blush + risquinhos dentro da elipse
blush = np.zeros_like(fg)
for cx, cy in [(415, 832), (1075, 832)]:
    m = (np.hypot((X - cx) / 88, (Y - cy) / 66) < 1) & (lab != SKIN) & (lab != OUT)
    blush |= m
blush = ndimage.binary_fill_holes(cv2.morphologyEx(blush.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8)) > 0) & fg
# patas e moeda
paw_area = (Y > 1080) & (Y < 1400) & (X > 430) & (X < 1060)
brownish = paw_area & np.isin(lab, [BROWN, nearest((138, 85, 65))])
nn, c2, s2, _ = cv2.connectedComponentsWithStats(brownish.astype(np.uint8))
pf = np.zeros_like(fg)
for i in range(1, nn):
    if s2[i, 4] > 8000: pf |= c2 == i
pf = ndimage.binary_fill_holes(pf)
ccx, ccy = 747, 1218
dc = np.hypot(X - ccx, Y - ccy)
near = cv2.dilate(pf.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (81, 81))) > 0
paws = (pf | (near & (lab == OUT) & ~((np.abs(X - 747) < 60) & (np.hypot(X - 747, Y - 1218) > 84) & (np.hypot(X - 747, Y - 1218) < 135)))) & paw_area
rays = paw_area & np.isin(lab, [BROWN, nearest((138, 85, 65)), nearest((181, 127, 103))]) & ~pf & (cv2.dilate(pf.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (121, 121))) > 0)
paws = ndimage.binary_fill_holes(paws) & ~((np.abs(X - 747) < 60) & (dc > 84) & (dc < 135)) & paw_area & ~np.isin(lab, [SKIN, nearest((203, 142, 103))])
paws |= rays
yel = paw_area & (dc < 130) & ~paws & ~np.isin(lab, [SKIN, nearest((203, 142, 103))])
coin = ndimage.binary_fill_holes(cv2.morphologyEx(yel.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)) > 0) & ~paws
# patinhas com moeda (traçado fiel) e sem moeda (moeda vira pele, contornos internos das patas ficam)
TICK = nearest((203, 142, 103))
coinZone = dc < 128
pawsAll = paw_area & ~np.isin(lab, [SKIN, TICK]) & (near | coinZone | rays)
pawsAll = ndimage.binary_fill_holes(pawsAll) & ~np.isin(lab, [SKIN, TICK]) | rays
distPf = cv2.distanceTransform((~pf).astype(np.uint8), cv2.DIST_L2, 5)
pawsEmpty = ndimage.binary_fill_holes(pf | ((lab == OUT) & (distPf <= 38) & paw_area)) & ~rays
# folha (com contorno) e cabinho, pra desenhar em volta da laranja feita à mão
GREEN = nearest((114, 167, 63))
green = (labOrig == GREEN) & (Y < 360)
leaf = (green | ((labOrig == OUT) & (cv2.dilate(green.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (45, 45))) > 0))) & (Y < 345) & (np.hypot(X - 746, Y - 413) > 112)
stem = np.isin(labOrig, [nearest((100, 55, 32)), nearest((120, 74, 54))]) & (Y < 320) & (X > 660) & (X < 790) & ~leaf
print('areas', fruit.sum(), eyes.sum(), blush.sum(), pawsAll.sum(), pawsEmpty.sum(), leaf.sum(), stem.sum(), file=sys.stderr)
src = cv2.imread('capi-referencia.jpg')[:, :, ::-1].astype(int)
dark = (src.max(2) < 95)[:, src_x]
eyesSrc = np.zeros_like(fg)
for cx, cy in [(500, 680), (995, 680)]:
    m = dark & (np.hypot(X - cx, Y - cy) < 80)
    nn, c2, s2, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8))
    eyesSrc |= c2 == (np.argmax(s2[1:, 4]) + 1)
eyesSrc = ndimage.binary_fill_holes(eyesSrc)
eyes = eyes | eyesSrc
hole = (eyes | blush | pawsAll)
bodyLab[(lab == BG) & body] = SKIN
bodyLab[hole] = SKIN
body &= ~(fruit & (Y < topY))
body = ndimage.binary_fill_holes(body | hole)   # sem buracos (o brilho do olho era 'fundo' e aparecia ao piscar)
bodyLab[body & (bodyLab == BG)] = SKIN
parts = {'body': (body, bodyLab), 'eyes': (eyesSrc, lab), 'blush': (blush, lab), 'pawsCoin': (pawsAll, lab), 'pawsEmpty': (pawsEmpty, lab), 'rays': (rays, lab), 'leaf': (leaf, labOrig), 'stem': (stem, labOrig)}
np.save('parts.npy', {k: (v[0], v[1]) for k, v in parts.items()}, allow_pickle=True)
json.dump({'hex': hexs, 'OUT': OUT, 'BG': BG, 'SKIN': SKIN, 'EYE': EYE, 'axis': A2 / 2}, open('pal.json', 'w'))
