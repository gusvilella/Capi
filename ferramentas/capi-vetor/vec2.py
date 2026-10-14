import cv2, numpy as np, json, sys, time, potrace
P = np.load('parts.npy', allow_pickle=True).item(); pal = json.load(open('pal.json'))
hexs = pal['hex']; OUT = pal['OUT']; BG = pal['BG']
DS = 1
SC = 10.0 / DS
def f(v): s = ('%.1f' % (v / SC)).rstrip('0').rstrip('.'); return '0' if s in ('-0', '') else s
def pt(p): return f(p.x) + ' ' + f(p.y)
def region_path(mask):
    m = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 3.0)
    m = cv2.resize(m, (m.shape[1] // DS, m.shape[0] // DS), interpolation=cv2.INTER_AREA) > .5
    if m.sum() < 20: return ''
    bm = potrace.Bitmap(~m)   # potracer: False = tinta
    pl = bm.trace(turdsize=6, alphamax=1.15, opticurve=True, opttolerance=0.4)
    d = []
    for c in pl:
        s = 'M' + pt(c.start_point)
        for seg in c.segments:
            if seg.is_corner: s += 'L' + pt(seg.c) + 'L' + pt(seg.end_point)
            else: s += 'C' + pt(seg.c1) + ' ' + pt(seg.c2) + ' ' + pt(seg.end_point)
        d.append(s + 'Z')
    return ''.join(d)
k3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
def layer(name, base=True):
    m, lab = P[name]; m = m.astype(bool)
    svg = '<path d="%s" fill="%s" fill-rule="evenodd"/>' % (region_path(m), hexs[OUT]) if base else ''
    cols = [c for c in range(len(hexs)) if c not in (OUT, BG) and ((lab == c) & m).sum() > 300]
    cols.sort(key=lambda c: -((lab == c) & m).sum())
    for c in cols:
        cm = (cv2.dilate(((lab == c) & m).astype(np.uint8), k3) > 0) & m
        p = region_path(cm)
        if p: svg += '<path d="%s" fill="%s" fill-rule="evenodd"/>' % (p, hexs[c])
    # traços escuros por cima (garrinhas, boca, narinas, risco da orelha não somem embaixo das cores)
    if not base: return svg
    om = (cv2.dilate(((lab == OUT) & m).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))) > 0) & m
    p = region_path(om)
    if p: svg += '<path d="%s" fill="%s" fill-rule="evenodd"/>' % (p, hexs[OUT])
    wh = (lab == BG) & m
    if wh.sum() > 300:
        p = region_path(cv2.dilate(wh.astype(np.uint8), k3) > 0)
        if p: svg += '<path d="%s" fill="#fff" fill-rule="evenodd"/>' % p
    return svg
def single(mask, color):
    return '<path d="%s" fill="%s" fill-rule="evenodd"/>' % (region_path(mask), color)
from scipy import ndimage
import re
AX = json.load(open('pal.json'))['axis'] / 10 * 2      # 2 * eixo, em unidades do desenho
def mirror(svg):
    def fix_d(m):
        nums = re.findall(r'-?\d*\.?\d+', m.group(1)); cmds = re.findall(r'[MLCZ]|-?\d*\.?\d+', m.group(1))
        out = []; i = 0
        for t in cmds:
            if t in 'MLCZ': out.append(t); continue
            v = float(t)
            if i % 2 == 0: v = AX - v
            out.append(f(v * SC)); i += 1
        d = ''
        for t in out:
            d += t if t in 'MLCZ' or not d or d[-1] in 'MLCZ' else ' ' + t
        return 'd="' + d + '"'
    return re.sub(r'd="([^"]*)"', fix_d, svg)
Xs = np.arange(P['body'][0].shape[1])[None, :]
LEFT = Xs < 746
out = {}
out['body'] = layer('body')
em = ndimage.binary_fill_holes(P['eyes'][0]) & LEFT
le = single(em, '#220e08')
out['eyes'] = le + mirror(le) + '<circle cx="48.4" cy="64.8" r="1.42" fill="#fff"/><circle cx="%s" cy="64.8" r="1.42" fill="#fff"/>' % f((AX - 50 - 1.6) * SC)
m_, l_ = P['blush']; P['blushL'] = (m_ & LEFT, l_)
lb = layer('blushL', False)
def shift(svg, dx):
    def fix_d(m):
        toks = re.findall(r'[MLCZ]|-?\d*\.?\d+', m.group(1)); out = []; i = 0
        for t in toks:
            if t in 'MLCZ': out.append(t); continue
            v = float(t) + (dx if i % 2 == 0 else 0); out.append(f(v * SC)); i += 1
        d = ''
        for t in out: d += t if t in 'MLCZ' or not d or d[-1] in 'MLCZ' else ' ' + t
        return 'd="' + d + '"'
    return re.sub(r'd="([^"]*)"', fix_d, svg)
out['blush'] = lb + shift(lb, AX - 2 * 41.7)   # bochecha direita = cópia deslocada (risquinhos na mesma direção, como no desenho)
m, lab = P['pawsEmpty']
P['pl'] = (m & LEFT, lab)
rl = single(P['rays'][0] & LEFT, '#a56c56')   # risquinhos de pelo das patas, traçados à parte (não grudam na pata)
out['pl'] = rl + layer('pl'); out['pr'] = mirror(out['pl'])
out['leaf'] = layer('leaf')
out['stem'] = single(P['stem'][0], '#6e4021')
json.dump(out, open('layers.json', 'w'))
print({k: len(v) for k, v in out.items()}, sum(len(v) for v in out.values()))
