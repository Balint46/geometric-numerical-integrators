# Geometric Numerical Integrators

A Python implementation demonstrating geometric numerical integration methods, with focus on the **Störmer-Verlet (velocity Verlet)** method for Hamiltonian systems.

## Overview

This project explores the fundamental properties of symplectic integrators through practical examples:

- **Kepler Problem** - Planetary motion simulation
- **Lennard-Jones Molecular Dynamics** - Multi-particle interactions

## Key Properties Demonstrated

| Property | Description |
|----------|-------------|
| **Symplecticity** | Preservation of phase space volume (area in 2D) |
| **Time-reversibility** | Integration can be reversed exactly |
| **Long-term energy behaviour** | Bounded energy error without secular drift |
| **Splitting structure** | Kick-Drift-Kick decomposition |

## Project Structure

```
geometric-numerical-integrators/
├── src/
│   ├── __init__.py          # Package exports
│   ├── integrators.py       # Core integration methods
│   ├── systems.py           # Physical systems (Kepler, LJ)
│   ├── experiments.py       # Experiment functions
│   └── plotting.py          # Visualization utilities
├── docs/                    # Theory and reference materials
├── main_notebook.ipynb      # Complete demonstration notebook
├── requirements.txt         # Python dependencies
└── README.md
```

## Installation

```bash
# Clone or download the repository
cd geometric-numerical-integrators

# Install dependencies
pip install -r requirements.txt

# Run the notebook
jupyter notebook main_notebook.ipynb
```

## The Störmer-Verlet Method

The velocity Verlet integrator uses a **Kick-Drift-Kick** splitting:

```
1. Kick:  p_{1/2} = p_n - (h/2) * gradV(q_n)
2. Drift: q_{n+1} = q_n + h * p_{1/2}
3. Kick:  p_{n+1} = p_{1/2} - (h/2) * gradV(q_{n+1})
```

This decomposition:
- Preserves the symplectic structure
- Is time-reversible
- Has second-order accuracy O(h²)
- Requires only one force evaluation per step

## Implemented Integrators

| Integrator | Order | Symplectic | Time-Reversible |
|------------|-------|------------|-----------------|
| Verlet | 2 | Yes | Yes |
| Symplectic Euler | 1 | Yes | No |
| Explicit Euler | 1 | No | No |
| RK4 | 4 | No | No |

## Physical Systems

### Kepler Problem
- Potential: V(q) = -1/||q||
- Conserves: Energy, Angular momentum
- Demonstrates: Orbit preservation, energy bounded errors

### Lennard-Jones
- Pairwise potential: V(r) = 4ε[(σ/r)¹² - (σ/r)⁶]
- 2-3 particle configurations
- Demonstrates: Molecular dynamics stability

## Usage Example

```python
from src.integrators import verlet_step, integrate
from src.systems import KeplerSystem

# Create Kepler system
kepler = KeplerSystem(mu=1.0)

# Initial conditions for elliptical orbit
q0, p0 = kepler.get_elliptical_orbit_ic(e=0.6, a=1.0)

# Integrate
t, q_hist, p_hist = integrate(q0, p0, h=0.01, n_steps=10000,
                               gradV=kepler.gradV, integrator='verlet')
```

## References

- Hairer, E., Lubich, C., & Wanner, G. (2006). *Geometric Numerical Integration*. Springer.
- Leimkuhler, B., & Reich, S. (2004). *Simulating Hamiltonian Dynamics*. Cambridge University Press.
- Verlet, L. (1967). Computer "Experiments" on Classical Fluids. *Physical Review*, 159(1), 98-103.

See the `docs/` folder for additional reference materials.
