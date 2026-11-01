import glob
import re
import matplotlib.pyplot as plt

R = '/disk2/tomanl/prepinac/'
EV = 27.211386


def parse(out):
    txt = open(out).read()
    assert 'ORCA TERMINATED NORMALLY' in txt
    states = []
    for block in re.split(r'\nSTATE\s+\d+:', txt.split('CIS-EXCITED STATES (SINGLETS)')[1])[1:3]:
        de = float(re.search(r'E=\s+([\d.]+) au', block).group(1)) * EV
        exc = re.findall(r'(\d+)a ->\s+(\d+)a\s+:\s+([\d.]+)', block.split('\n\n')[0])
        i, a, w = max(exc, key=lambda t: float(t[2]))
        states.append((de, f'{i}->{a}', float(w)))
    spec = txt.split('ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS')[1]
    f = [float(m) for m in re.findall(r'0-1A\s+->\s+\d-1A\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+([\d.]+)', spec)[:2]]
    return states, f


def dft_s0(scan):
    rows = [l.split() for l in open(f'{R}03-scan/{scan}_envelope.dat') if not l.startswith('#')]
    return {float(r[0]): float(r[1]) / 96.485332 for r in rows}  # kJ/mol -> eV, relative to trans


data = {}
for scan in ['torsion', 'inversion']:
    s0 = dft_s0(scan)
    rows = []
    for out in sorted(glob.glob(f'{R}05-zindo/{scan}/p*.out')):
        q = float(open(out.replace('.out', '.xyz')).read().split('\n')[1].split()[1])
        st, f = parse(out)
        rows.append((q, s0[q], st, f))
    data[scan] = rows
    with open(f'{R}05-zindo/{scan}_zindo.dat', 'w') as fh:
        fh.write('# coord/deg  S0(DFT)  S1  S2 (eV, rel. to trans; S_n = S0(DFT) + dE_n(ZINDO/S))  '
                 'dE1  dE2 (eV)  f1  f2  main excitation S1, S2 (weight)\n')
        for q, e0, st, (f1, f2) in rows:
            fh.write(f'{q:7.1f} {e0:8.3f} {e0 + st[0][0]:8.3f} {e0 + st[1][0]:8.3f} {st[0][0]:7.3f} {st[1][0]:7.3f} '
                     f'{f1:7.4f} {f2:7.4f}  {st[0][1]} ({st[0][2]:.2f})  {st[1][1]} ({st[1][2]:.2f})\n')

colors = ['#2a78d6', '#eb6834', '#1baf7a']
fig, axes = plt.subplots(2, 2, figsize=(10, 7), sharex='col', sharey='row')
for col, scan in enumerate(['torsion', 'inversion']):
    rows = data[scan]
    q = [r[0] for r in rows]
    top, bottom = axes[0, col], axes[1, col]
    top.plot(q, [r[1] for r in rows], 'o-', color=colors[0], ms=3, lw=1.5, label='S$_0$ (ωB97X-D3)')
    for k in range(2):
        top.plot(q, [r[1] + r[2][k][0] for r in rows], 'o-', color=colors[k + 1], ms=3, lw=1.5,
                 label=f'S$_{k + 1}$ = S$_0$ + ΔE$_{k + 1}$(ZINDO/S)')
        bottom.plot(q, [r[2][k][0] for r in rows], 'o-', color=colors[k + 1], ms=3, lw=1.5,
                    label=f'ΔE$_{k + 1}$ (ZINDO/S)')
    top.legend(frameon=False, fontsize=8)
    bottom.legend(frameon=False, fontsize=8)
axes[0, 0].set_ylabel('E − E$_{S_0}$(trans) / eV')
axes[1, 0].set_ylabel('vertical excitation energy / eV')
axes[1, 0].set_xlim(180, 0)
axes[1, 0].set_xlabel('CNNC dihedral / °')
axes[1, 1].set_xticks([120, 140, 160, 180, 200, 220], ['120', '140', '160', '180', '160', '140'])
axes[1, 1].set_xlabel('CNN angle / °  (trans side → linear → cis side)')
fig.tight_layout()
fig.savefig(f'{R}05-zindo/zindo_states.png', dpi=200)
