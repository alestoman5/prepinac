# 01-opt

Geometry optimization of trans- and cis-azobenzene, ωB97X-D3/def2-TZVP, `DefGrid3 TightOpt`, ORCA 6.1.1.
`TightOpt` sets the SCF thresholds to the `VeryTightSCF` level (TolE 1e-9, Thresh 1e-12); all later
stages use `DefGrid3 VeryTightSCF` to stay consistent.

## Procedure

1. Starting geometries: `trans_start.xyz` (slightly non-planar, displaced along the out-of-plane mode of an
   earlier run), `cis_start.xyz`. ORCA overwrites `<name>.xyz` with the optimized geometry.
2. Run (8 cores):
   ```
   cp trans_start.xyz trans.xyz
   nohup /usr/local/bin/orca_6_1_1/orca trans.inp > trans.out &
   ```
3. Check:
   ```
   grep "OPTIMIZATION RUN DONE" trans.out
   grep -A6 "Geometry convergence" trans.out | tail -4
   grep "FINAL SINGLE POINT ENERGY" trans.out | tail -1
   ```

## Results

| Isomer | E / Eh | CNNC / ° | CNN / ° | N=N / Å | Wall time (8 cores) |
|---|---|---|---|---|---|
| trans | −572.789576490 | 180.0 | 115.1 | 1.235 | 15.4 min |
| cis | −572.770184076 | 5.8 | 122.6 | 1.231 | 13.3 min |

Atom indices (0-based, as ORCA uses them): C2–N0=N1–C13.

## History

- First runs with the default grid (`DefGrid2`): trans had one imaginary frequency (−16 cm⁻¹, out-of-plane
  phenyl torsion), −9 cm⁻¹ after two displace-and-reoptimize cycles (`scripts/displace.py`).
- `DefGrid3` with a `NormalSCF` frequency run still gave −5 cm⁻¹; the frequency job then used looser SCF
  thresholds than the optimization. With `VeryTightSCF` in the frequency run no imaginary mode remains
  (see `02-freq/`). Old runs are kept locally in `archive_defgrid2/` (not tracked).
