# 03-scan

Relaxed scans trans → cis, ωB97X-D3/def2-TZVP, `DefGrid3 VeryTightSCF Opt`, 6–8 cores per job.
Atom indices (0-based): C2–N0=N1–C13.

## Runs

| Directory | Start | Scan | Points | Wall time |
|---|---|---|---|---|
| `torsion/` | `01-opt/trans.xyz` | `D 2 0 1 13 = 180, 0, 37` | 37 | 9 h 50 min |
| `inversion_trans/` | `01-opt/trans.xyz` | `A 2 0 1 = 115, 180, 14` | 14 | 3 h 01 min |
| `inversion_cis/` | `01-opt/cis.xyz` | `A 2 0 1 = 125, 180, 12` | 12 | 3 h 57 min |
| `torsion_from75/` | point 75° of `torsion` | `D 2 0 1 13 = 80, 120, 9` | 4 (stopped at 100°) | – |
| `inversion_trans_from160/` | point 160° of `inversion_trans` | `A 2 0 1 = 155, 130, 6` | 6 | 1 h 42 min |

```
nohup /usr/local/bin/orca_6_1_1/orca torsion.inp > torsion.out &
cat torsion.relaxscanact.dat          # coordinate, energy / Eh
```

`torsion_from75` stopped with "angle approaching 180 or 0 degrees" (second CNN angle → 178°) at 100°;
the four finished points are in `torsion_from75.allxyz`.

## Two branches

- `torsion`: between 80° and 75° the energy drops by 96 kJ/mol and both phenyl rings flip
  (C–C–N=N 178.9° → −174.0°, −9.2° → 12.7°) while the N=N geometry stays continuous.
- `inversion_trans`: between 155° and 160° the inverting phenyl turns from planar to ~92°
  (N=N 1.225 → 1.211 Å, energy drops by 2.5 kJ/mol).
- Recomputing from the other branch (`*_from75`, `*_from160`) gives lower energies for torsion
  80–90° and inversion 145–155°. The branches cross between 90° and 95° (torsion) and between
  140° and 145° (inversion).

## Lower envelope

```
python scripts/scan_envelope.py
```

Takes the lower energy at each coordinate value from all branches (coordinate measured from the
geometry, rounded to 0.1°) and writes:

- `torsion_envelope.dat`, `inversion_envelope.dat`: coordinate, E − E(trans) / kJ mol⁻¹, E / Eh, source run
- `torsion_envelope.xyz`, `inversion_envelope.xyz`: geometries of the envelope points
- `scan_envelope.png`

The inversion path is plotted as CNN on the trans side (115–180°) followed by 360° − CNN on the cis side.
At 180° the trans and cis branches differ by 0.04 kJ/mol.
