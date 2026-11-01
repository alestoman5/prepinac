import re
import sys
import numpy as np

out, xyzfile = sys.argv[1], sys.argv[2]
mos = range(29, 39)

x = np.array([[float(v) for v in l.split()[1:4]] for l in open(xyzfile).read().split('\n')[2:] if l.strip()])
normal = np.cross(x[2] - x[0], x[13] - x[1])  # normal of the C2-N0-N1-C13 plane
normal /= np.linalg.norm(normal)

lines = open(out).read().split('MOLECULAR ORBITALS')[1].split('\n')[2:]
coef, energy, labels, idx = {}, {}, [], []
for k, l in enumerate(lines):
    p = l.split()
    if p and all(t.isdigit() for t in p):
        idx = [int(t) for t in p]
        for i, e in zip(idx, lines[k + 1].split()):
            energy[i] = float(e) * 27.211386
            coef[i] = []
    elif p and re.fullmatch(r'\d+[A-Z][a-z]?', p[0]):
        if idx[0] == 0:
            labels.append((int(re.match(r'\d+', p[0]).group()), p[1]))
        for j, i in enumerate(idx):
            coef[i].append(float(p[2 + j]))
    elif p and not p[0].startswith('-') and not re.fullmatch(r'-?\d+\.\d+', p[0]):
        break
coef = {i: np.array(c) for i, c in coef.items()}

el = [l.split()[0] for l in open(xyzfile).read().split('\n')[2:] if l.strip()]
nidx = [k for k, (a, f) in enumerate(labels) if el[a] == 'N']
print(f'{"MO":>3} {"E/eV":>7} {"N":>5} {"pi":>5}   (fractions of c^2; pi = p along the CNNC-plane normal)')
for i in mos:
    c2 = coef[i] ** 2 / (coef[i] ** 2).sum()
    pi = 0.0
    for a in range(len(el)):
        p = {f[-1]: coef[i][k] for k, (b, f) in enumerate(labels) if b == a and f.endswith(('px', 'py', 'pz'))}
        if p:
            pi += (np.array([p['x'], p['y'], p['z']]) @ normal) ** 2
    pi /= (coef[i] ** 2).sum()
    occ = 'occ' if i <= 33 else 'virt'
    print(f'{i:3d} {energy[i]:7.2f} {c2[nidx].sum():5.2f} {pi:5.2f}  {occ}')
