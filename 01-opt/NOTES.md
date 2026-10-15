# 01-opt

Geometry optimization of trans- and cis-azobenzene, ωB97X-D3/def2-TZVP, `TightOpt`, ORCA 6.1.1.

## Procedure

1. Starting geometries `trans.xyz`, `cis.xyz` (CNNC ≈ 180° and ≈ 10°).
   ORCA overwrites `<name>.xyz` with the optimized geometry, so the tracked `*.xyz` are the optimized ones.
2. Run (8 cores):
   ```
   nohup /usr/local/bin/orca_6_1_1/orca trans.inp > trans.inp.out &
   nohup /usr/local/bin/orca_6_1_1/orca cis.inp > cis.inp.out &
   ```
3. Check:
   ```
   grep "OPTIMIZATION RUN DONE" trans.inp.out
   grep "FINAL SINGLE POINT ENERGY" trans.inp.out | tail -1
   ```

## Results

| Isomer | E / Eh | CNNC / ° | CNN / ° | N=N / Å | Wall time (8 cores) |
|---|---|---|---|---|---|
| trans | −572.789639015 | 180.0 | 115.1 | 1.235 | 8.5 min |
| cis | −572.770408446 | 5.4 | 122.7 | 1.231 | 13.4 min |

Atom indices (0-based, as ORCA uses them): C2–N0=N1–C13.
