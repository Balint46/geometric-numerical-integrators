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
│   ├── __init__.py               # Package exports
│   ├── integrators.py            # Core integration methods
│   ├── systems.py                # Physical systems (Kepler, LJ)
│   ├── experiments.py            # Experiment functions
│   ├── plotting.py               # Visualization utilities
│   ├── generate_static_plots.py  # Generate all static plots
│   └── generate_animations.py    # Generate all animations
├── media/
│   ├── docs/                     # Theory and reference materials
│   ├── plots/                    # Generated static plots (PNG)
│   └── animations/               # Generated animations (GIF/MP4)
├── main_notebook.ipynb           # Complete demonstration notebook
├── requirements.txt              # Python dependencies
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

## Generating Plots and Animations

The project includes scripts to generate all plots and animations used in the documentation:

### Generate Static Plots

```bash
# Generate all 14 static plots (saves to media/plots/)
python src/generate_static_plots.py
```

This creates high-resolution PNG images including:
- Splitting diagrams and flow visualizations
- Method comparisons (Störmer-Verlet vs Euler, RK2, RK4)
- Energy behavior and convergence analysis
- Time-reversibility tests
- Symplectic area preservation
- Lennard-Jones simulations

### Generate Animations

```bash
# Generate all animations (saves to media/animations/)
python src/generate_animations.py
```

This creates animations in GIF format (and MP4 if ffmpeg is installed):
- Exact orbit vs Störmer-Verlet comparison
- Störmer-Verlet vs RK2 comparison
- Lennard-Jones 2-particle and 3-particle dynamics

**Note:** Animation generation may take several minutes. For MP4 support, install ffmpeg:
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
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
| RK2 (Midpoint) | 2 | No | No |
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
from src.integrators import integrate
from src.systems import KeplerSystem
from src.experiments import run_kepler_comparison
from src.plotting import plot_sv_vs_rk4_long_term

# Create Kepler system
kepler = KeplerSystem(mu=1.0)

# Initial conditions for elliptical orbit
q0, p0 = kepler.get_elliptical_orbit_ic(e=0.6, a=1.0)

# Compare integrators over 100 orbits
results = run_kepler_comparison(kepler, q0, p0, h=0.05, n_orbits=100)

# Visualize long-term behavior
fig = plot_sv_vs_rk4_long_term(results)
```

For a complete demonstration with all experiments, see `main_notebook.ipynb`.

## References

- Hairer, E., Lubich, C., & Wanner, G. (2006). *Geometric Numerical Integration*. Springer.
- Leimkuhler, B., & Reich, S. (2004). *Simulating Hamiltonian Dynamics*. Cambridge University Press.
- Verlet, L. (1967). Computer "Experiments" on Classical Fluids. *Physical Review*, 159(1), 98-103.

See the `media/docs/` folder for additional reference materials.
