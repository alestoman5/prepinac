import sys
import numpy as np

hess, xyz, mode, amp, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]

blk = open(hess).read().split('$normal_modes')[1].split('$')[0].split('\n')
n = int(blk[1].split()[0])
modes = np.zeros((n, n))
i = 2
while blk[i].strip():
    cols = [int(c) for c in blk[i].split()]
    for r in range(n):
        modes[r, cols] = [float(v) for v in blk[i + 1 + r].split()[1:]]
    i += n + 1

lines = open(xyz).read().split('\n')
atoms = [l.split() for l in lines[2:] if l.strip()]
x = np.array([[float(v) for v in a[1:4]] for a in atoms])
d = modes[:, mode].reshape(-1, 3)
x += amp * d / np.abs(d).max()
with open(out, 'w') as f:
    f.write(f'{len(atoms)}\ndisplaced along mode {mode} by {amp} A\n')
    for a, r in zip(atoms, x):
        f.write(f'{a[0]:2s} {r[0]:14.8f} {r[1]:14.8f} {r[2]:14.8f}\n')
