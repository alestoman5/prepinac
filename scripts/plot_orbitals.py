import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage.measure import marching_cubes

D = '/disk2/tomanl/prepinac/06-orbitals/'
BOHR = 0.529177
ISO = 0.03


def read_cube(path):
    lines = open(path).read().split('\n')
    p = lines[2].split()
    nat, origin = int(p[0]), np.array([float(v) for v in p[1:4]])
    axes = [lines[3 + i].split() for i in range(3)]
    n = [int(a[0]) for a in axes]
    step = np.array([[float(v) for v in a[1:4]] for a in axes])
    atoms = [lines[6 + i].split() for i in range(abs(nat))]
    z = [int(a[0]) for a in atoms]
    xyz = np.array([[float(v) for v in a[2:5]] for a in atoms]) * BOHR
    start = 6 + abs(nat) + (1 if nat < 0 else 0)
    vals = np.array(' '.join(lines[start:]).split(), float).reshape(n)
    return z, xyz, vals, origin * BOHR, step * BOHR


def frame(xyz):
    # x along N=N, z along the normal of the C2-N0-N1-C13 plane
    ex = xyz[1] - xyz[0]
    ex /= np.linalg.norm(ex)
    ez = np.cross(xyz[2] - xyz[0], xyz[13] - xyz[1])
    ez -= (ez @ ex) * ex
    ez /= np.linalg.norm(ez)
    return np.array([ex, np.cross(ez, ex), ez]), (xyz[0] + xyz[1]) / 2


def draw(ax, iso, mo):
    z, xyz, vals, origin, step = read_cube(f'{D}{iso}_mo{mo}.cube')
    rot, center = frame(xyz)
    tr = lambda p: (p - center) @ rot.T
    for level, color in [(ISO, '#2a78d6'), (-ISO, '#eb6834')]:
        verts, faces, _, _ = marching_cubes(vals, level)
        verts = tr(origin + verts @ step)
        ax.add_collection3d(Poly3DCollection(verts[faces], color=color, alpha=0.55, linewidth=0))
    pos = tr(xyz)
    for i in range(len(z)):
        for j in range(i):
            if np.linalg.norm(pos[i] - pos[j]) < (1.2 if 1 in (z[i], z[j]) else 1.6):
                ax.plot(*pos[[i, j]].T, color='0.3', lw=1.2)
    colors = {1: '0.85', 6: '0.35', 7: '#1f3fbf'}
    ax.scatter(*pos.T, c=[colors[k] for k in z], s=[8 if k == 1 else 18 for k in z], depthshade=False)
    r = np.abs(pos).max() + 0.5
    ax.set(xlim=(-r, r), ylim=(-r, r), zlim=(-r, r))
    ax.set_box_aspect((1, 1, 1), zoom=1.6)
    ax.set_proj_type('ortho')
    ax.view_init(elev=25, azim=-15)
    ax.set_axis_off()
    ax.text2D(0.02, 0.92, f'{iso}, MO {mo}', transform=ax.transAxes, fontsize=10)


fig = plt.figure(figsize=(9, 10))
for row, mo in enumerate([29, 33, 34]):
    for col, iso in enumerate(['trans', 'cis']):
        draw(fig.add_subplot(3, 2, 2 * row + col + 1, projection='3d'), iso, mo)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
fig.savefig(f'{D}orbitals.png', dpi=150)
