# photoswitch

Quantum-chemical study of the **azobenzene photoswitch**: trans/cis structures, isomerization
pathways and excited states. Student project, UCT Prague (VŠCHT).

## Tasks

- Choose the quantum-chemical method for the calculations
- Optimize trans- and cis-azobenzene
- Verify that both structures are minima on the potential energy surface
- Compare the relative stability of the isomers
- Relaxed scan between the two forms
- Isomerization energies with PM6 and B3LYP/6-31G*, comparison with experiment
- Ground and two excited states along the reaction coordinate with ZINDO
- Molecular orbitals and the character of the electronic transitions
- Applications of photoswitches in current technologies

## Stages

| Stage | Status | Contents |
|---|---|---|
| [`01-opt/`](01-opt/) | done | trans/cis geometry optimization, ωB97X-D3/def2-TZVP, DefGrid3 |
| [`02-freq/`](02-freq/) | done | frequencies (no imaginary modes), relative stability |
| [`03-scan/`](03-scan/) | done | relaxed scans: CNNC torsion and CNN inversion, lower envelope |
| [`04-isomerization/`](04-isomerization/) | done | isomerization energies: B3LYP/6-31G*, PM6 (MOPAC) |
| [`05-zindo/`](05-zindo/) | done | ZINDO/S + CIS excitation energies along the scan envelopes |
| [`06-orbitals/`](06-orbitals/) | done | ZINDO/S orbitals and character of S1, S2 at trans and cis |

The procedure for each stage (commands in order) is in its `NOTES.md`.

## Requirements

- [ORCA 6.1.1](https://orcaforum.kofo.mpg.de/) (academic license, not redistributable)
- [MOPAC 23.2.5](https://github.com/openmopac/mopac) (conda-forge, `mopac` environment)
- Python with numpy, matplotlib and scikit-image (`scripts/`)
