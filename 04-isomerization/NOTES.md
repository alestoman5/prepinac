# 04-isomerization

Trans → cis isomerization energies with different methods, compared with experiment.

## B3LYP/6-31G* (`b3lyp/`)

`! B3LYP 6-31G* DefGrid3 TightOpt Freq`, 8 cores, start from the ωB97X-D3/def2-TZVP minima (`01-opt`).
`Freq` in the same job keeps the optimization SCF thresholds (TolE 1e-9).

```
cp trans_start.xyz trans.xyz
nohup /usr/local/bin/orca_6_1_1/orca trans.inp > trans.out &
grep -A6 "Geometry convergence" trans.out | tail -4
grep "imaginary mode" trans.out
grep -E "FINAL SINGLE POINT ENERGY|Zero point energy|Total enthalpy  |Final Gibbs free energy" trans.out
```

| Isomer | Imaginary modes | Lowest frequency / cm⁻¹ | E / Eh | E + ZPE / Eh | H / Eh | G / Eh | Wall time |
|---|---|---|---|---|---|---|---|
| trans | 0 | 26.37 | −572.395665696 | −572.204443256 | −572.19267056 | −572.2404526 | 6.1 min |
| cis | 0 | 44.90 | −572.371481458 | −572.180852258 | −572.16910897 | −572.21655021 | 8.7 min |

trans: optimization stopped on "step convergence overachieved" with MAX gradient 2.9·10⁻⁴ Eh/bohr
(TightOpt limit 1·10⁻⁴); last energy change −6·10⁻⁶ Eh.

## PM6 (`pm6/`)

MOPAC 23.2.5 (conda env `mopac`). Final settings, identical for both isomers:

- optimization: `PM6 PRECISE BFGS GNORM=0.001 LET SCFCRT=1.D-9`
- frequencies: `PM6 PRECISE FORCE THERMO(298) SCFCRT=1.D-9`

```
/disk2/tomanl/miniforge3/envs/mopac/bin/mopac trans_rot0.03_opt.mop    # -> .out, .arc
grep "FINAL HEAT OF FORMATION" trans_rot0.03_opt.out
grep -E "^\s+FREQUENCY" trans_rot0.03_freq.out | head -3
```

The result is the heat of formation at 298 K (ΔH_f); ZPE and thermal terms are part of the PM6
parametrization, so ΔH(cis − trans) = ΔH_f(cis) − ΔH_f(trans).

| Isomer | Files | ΔH_f / kcal·mol⁻¹ | ΔH_f / kJ·mol⁻¹ | Gradient norm | Lowest frequency / cm⁻¹ | CNNC / ° | C–C–N=N / ° |
|---|---|---|---|---|---|---|---|
| trans | `trans_rot0.03_*` | 95.88429 | 401.17987 | 0.00096 | 10.41 | 179.2 | 163.4, −18.7 |
| cis | `cis_bfgs_*` | 91.94097 | 384.68102 | 0.00063 | 16.52 | 1.6 | 51.0, −134.3 |

ΔH(cis − trans) = −16.50 kJ/mol.

History (all runs kept in `pm6/`):

- Default EF optimizer (`*_opt`, `*_scf_*`, `*_tight_*`, `*_ddmin_*`) stopped on "heat of formation is
  essentially stationary" above `GNORM`; the lowest frequency of one isomer was always −8 to −12 cm⁻¹.
- `BFGS` reached `GNORM=0.001` for both. trans stayed planar (C2h start) with −7.75 cm⁻¹.
- MOPAC reorients the molecule for `FORCE`; `scripts/displace_mopac.py` now rotates the normal mode
  back into the input frame. Runs `cis_displaced_*`, `cis_disp04_*` and `trans_bfgs_disp_*` used the
  unrotated mode (wrong direction).
- Energy profile along the lowest trans mode of the planar structure (`mode_profile/trans_rot_*`) is
  almost purely quartic. Displacing by ±0.03 and ±0.10 Å and reoptimizing gave the same non-planar
  minimum (ΔH_f 95.88429 kcal/mol, 0.0245 kcal/mol below planar) with all frequencies positive.

## Comparison (cis − trans, kJ/mol, gas phase, 298.15 K)

| Method | ΔE | ΔE + ZPE | ΔH | ΔG |
|---|---|---|---|---|
| ωB97X-D3/def2-TZVP (`02-freq`) | 50.92 | 50.44 | 49.98 | 52.42 |
| B3LYP/6-31G* | 63.50 | 61.94 | 61.86 | 62.76 |
| PM6 (ΔH_f, see below) | – | – | −16.50 | – |

Experiment: 47.0 ± 1.3 kJ/mol, heat of isomerization measured by calorimetry in the liquid state
(o-terphenyl matrix); M. Zhu, L. Yu, https://par.nsf.gov/servlets/purl/10133412 (full text not checked).
