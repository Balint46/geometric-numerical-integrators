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
    lennard_jones_simulation
)

from .plotting import (
    plot_long_term_energy,
    plot_reversibility_test,
    plot_splitting_diagram,
    plot_splitting_flow,
    plot_lennard_jones,
    plot_sv_vs_rk4_long_term,
    plot_sv_vs_euler,
    plot_sv_vs_rk2,
    plot_energy_crossover,
    plot_area_symplectic_methods,
    plot_area_nonsymplectic_methods,
    create_exact_vs_sv_animation,
    create_sv_vs_rk2_animation,
    create_molecular_animation
)

__version__ = '1.2.0'
__all__ = [
    # Integrators
    'verlet_step', 'euler_step', 'symplectic_euler_step', 'rk4_step',
    'integrate', 'integrate_with_splitting_detail',
    # Systems
    'KeplerSystem', 'LennardJonesSystem', 'HarmonicOscillator',
    # Experiments
    'run_kepler_comparison', 'long_term_energy_analysis',
    'time_reversibility_test', 'symplectic_area_test',
    'compute_local_error', 'lennard_jones_simulation',
    # Plotting
    'plot_long_term_energy', 'plot_reversibility_test',
    'plot_splitting_diagram', 'plot_splitting_flow',
    'plot_lennard_jones', 'plot_sv_vs_rk4_long_term',
    'plot_sv_vs_euler', 'plot_sv_vs_rk2',
    'plot_energy_crossover', 'plot_area_symplectic_methods',
    'plot_area_nonsymplectic_methods',
    'create_exact_vs_sv_animation', 'create_sv_vs_rk2_animation',
    'create_molecular_animation'
]
