"""
Geometric Numerical Integrators
===============================

A package for demonstrating geometric numerical integration methods,
particularly the Störmer-Verlet (velocity Verlet) method.

Modules:
    - integrators: Core integration methods (Verlet, Euler, RK4)
    - systems: Physical systems (Kepler, Lennard-Jones)
    - experiments: Test functions for demonstrating properties
    - plotting: Visualization utilities
"""

from .integrators import (
    verlet_step,
    euler_step,
    symplectic_euler_step,
    rk4_step,
    integrate,
    integrate_with_splitting_detail
)

from .systems import (
    KeplerSystem,
    LennardJonesSystem,
    HarmonicOscillator
)

from .experiments import (
    run_kepler_comparison,
    long_term_energy_analysis,
    time_reversibility_test,
    symplectic_area_test,
    compute_local_error,
    convergence_study,
    lennard_jones_simulation
)

from .plotting import (
    plot_kepler_orbits,
    plot_orbit_comparison,
    plot_rk4_verlet_contrast,
    plot_energy_error,
    plot_long_term_energy,
    plot_reversibility_test,
    plot_symplectic_area,
    plot_splitting_diagram,
    plot_splitting_flow,
    plot_lennard_jones,
    plot_convergence,
    create_orbit_animation,
    plot_sv_vs_rk4_long_term,
    plot_sv_vs_rk2_euler_short_term,
    plot_energy_crossover,
    plot_symplectic_area_enhanced,
    create_exact_vs_sv_animation,
    create_sv_vs_rk2_animation,
    create_molecular_animation
)

__version__ = '1.0.0'
__all__ = [
    # Integrators
    'verlet_step', 'euler_step', 'symplectic_euler_step', 'rk4_step',
    'integrate', 'integrate_with_splitting_detail',
    # Systems
    'KeplerSystem', 'LennardJonesSystem', 'HarmonicOscillator',
    # Experiments
    'run_kepler_comparison', 'long_term_energy_analysis',
    'time_reversibility_test', 'symplectic_area_test',
    'compute_local_error', 'convergence_study', 'lennard_jones_simulation',
    # Plotting
    'plot_kepler_orbits', 'plot_orbit_comparison', 'plot_rk4_verlet_contrast',
    'plot_energy_error', 'plot_long_term_energy', 'plot_reversibility_test',
    'plot_symplectic_area', 'plot_splitting_diagram', 'plot_splitting_flow',
    'plot_lennard_jones', 'plot_convergence', 'create_orbit_animation',
    'plot_sv_vs_rk4_long_term', 'plot_sv_vs_rk2_euler_short_term',
    'plot_energy_crossover', 'plot_symplectic_area_enhanced',
    'create_exact_vs_sv_animation', 'create_sv_vs_rk2_animation',
    'create_molecular_animation'
]
