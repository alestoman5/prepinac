# 02-freq

Analytic frequencies on the `01-opt` geometries, ωB97X-D3/def2-TZVP, `DefGrid3 VeryTightSCF Freq`.
Thermochemistry at 298.15 K, 1 atm (ORCA defaults).

## Procedure

```
nohup /usr/local/bin/orca_6_1_1/orca trans.inp > trans.out &
grep "imaginary mode" trans.out
grep -A12 "VIBRATIONAL FREQUENCIES" trans.out
grep -E "FINAL SINGLE POINT ENERGY|Zero point energy|Total enthalpy  |Final Gibbs free energy" trans.out
```

## Results

| Isomer | Imaginary modes | Lowest frequency / cm⁻¹ | E / Eh | ZPE / Eh | H / Eh | G / Eh |
|---|---|---|---|---|---|---|
| trans | 0 | 11.96 | −572.789576823 | 0.19263612 | −572.58515177 | −572.63330568 |
| cis | 0 | 40.59 | −572.770182344 | 0.19245172 | −572.56611586 | −572.61333818 |

cis − trans (1 Eh = 2625.4996 kJ/mol):

| ΔE | ΔE + ZPE | ΔH | ΔG |
|---|---|---|---|
| 50.92 kJ/mol | 50.44 kJ/mol | 49.98 kJ/mol | 52.42 kJ/mol |

Single-point energies agree with the end of the optimization within 2·10⁻⁶ Eh.
