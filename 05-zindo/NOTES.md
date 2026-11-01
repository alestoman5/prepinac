# 05-zindo

ZINDO/S + CIS (2 singlet roots) single points on the lower-envelope geometries of `03-scan`
(37 torsion points, 25 inversion points), ORCA 6.1.1, 1 core, < 1 s per point.

## Procedure

```
# split the envelope into one xyz per point and run
awk -v d=torsion 'NR%26==1{n++; f=sprintf("%s/p%03d.xyz", d, n-1)} {print > f}' ../03-scan/torsion_envelope.xyz
cd torsion && /usr/local/bin/orca_6_1_1/orca p000.inp > p000.out
python scripts/zindo_plot.py        # -> torsion_zindo.dat, inversion_zindo.dat, zindo_states.png (S0 from 03-scan envelope)
```

Input (`p000.inp`):
```
! ZINDO/S
%cis nroots 2 end
* xyzfile 0 1 p000.xyz
```

In the output: `FINAL SINGLE POINT ENERGY` (S0), `CIS-EXCITED STATES (SINGLETS)` (excitation energies and
weights of i → a excitations), `ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS` (oscillator strengths).

## Notes

- Valence electrons only: 68 electrons, 66 basis functions; HOMO = 33, LUMO = 34 (0-based).
- The ZINDO/S ground-state energy changes by tens to hundreds of eV along the path (cis 157 eV above trans);
  the nuclear repulsion grows faster than the electronic energy compensates
  (`torsion/p000.out` vs `p036.out`: nuclear repulsion 375.5 vs 397.3 Eh).
- The energy does not depend on molecular orientation (four rotated copies of trans agree within 3·10⁻⁷ Eh).
- ZINDO/1 on the same geometries (test, not tracked): trans −105.616235, 90° −105.551483, cis −105.623746 Eh.
- Plotted states: S0 = ωB97X-D3/def2-TZVP energy of the envelope point (`03-scan/*_envelope.dat`),
  S1 = S0 + ΔE1(ZINDO/S), S2 = S0 + ΔE2(ZINDO/S). The bottom panels show the ZINDO/S excitation energies alone.
- Inversion: ΔE2 jumps from 3.81 to 4.33 eV between 140° and 145°, where the envelope switches from the
  planar branch to the branch with the inverting phenyl perpendicular (`03-scan/NOTES.md`).
