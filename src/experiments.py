"""
Experiments for Geometric Numerical Integration
================================================

This module contains experiments demonstrating:
1. Kepler orbit simulation and integrator comparison
2. Long-term energy behaviour
3. Time-reversibility test
4. Symplectic area preservation
5. Local error estimation
"""

import numpy as np
from typing import Tuple, Dict, List, Callable
from .integrators import integrate, verlet_step, euler_step, rk2_step, rk4_step, symplectic_euler_step


def run_kepler_comparison(kepler_system, q0: np.ndarray, p0: np.ndarray,
                          h: float, n_orbits: float = 10) -> Dict:
    """
    Run Kepler problem with multiple integrators for comparison.

    Parameters
    ----------
    kepler_system : KeplerSystem
        The Kepler system instance
    q0 : np.ndarray
        Initial position
    p0 : np.ndarray
        Initial momentum
    h : float
        Time step
    n_orbits : float
        Number of orbital periods to simulate

    Returns
    -------
    dict
        Results for each integrator with keys:
        't', 'q', 'p', 'energy', 'angular_momentum'
    """
    # Estimate orbital period (for ellipse: T = 2*pi*a^(3/2))
    E = kepler_system.hamiltonian(q0, p0)
    a = -kepler_system.mu / (2 * E)  # Semi-major axis
    T = 2 * np.pi * a ** 1.5  # Orbital period

    n_steps = int(n_orbits * T / h)

    results = {}

    for integrator in ['verlet', 'rk2', 'euler', 'rk4']:
        t, q_hist, p_hist = integrate(q0, p0, h, n_steps, kepler_system.gradV, integrator)

        # Compute conserved quantities
        energy = np.array([kepler_system.hamiltonian(q_hist[i], p_hist[i])
                          for i in range(len(t))])
        L = np.array([kepler_system.angular_momentum(q_hist[i], p_hist[i])
                     for i in range(len(t))])

        results[integrator] = {
            't': t,
            'q': q_hist,
            'p': p_hist,
            'energy': energy,
            'angular_momentum': L,
            'energy_error': energy - energy[0],
            'L_error': L - L[0]
        }

    return results


def long_term_energy_analysis(kepler_system, q0: np.ndarray, p0: np.ndarray,
                               h: float, T_final: float) -> Dict:
    """
    Analyze long-term energy behaviour for different integrators.

    This demonstrates the key property of symplectic integrators:
    they have bounded energy error, while non-symplectic methods
    (like RK4) show secular drift.

    Parameters
    ----------
    kepler_system : KeplerSystem
        The system to integrate
    q0, p0 : np.ndarray
        Initial conditions
    h : float
        Time step
    T_final : float
        Final integration time

    Returns
    -------
    dict
        Energy error histories for each integrator
    """
    n_steps = int(T_final / h)

    results = {}
    E0 = kepler_system.hamiltonian(q0, p0)

    for integrator in ['verlet', 'rk2', 'euler', 'rk4', 'symplectic_euler']:
        t, q_hist, p_hist = integrate(q0, p0, h, n_steps,
                                      kepler_system.gradV, integrator)

        energy = np.array([kepler_system.hamiltonian(q_hist[i], p_hist[i])
                          for i in range(len(t))])

        results[integrator] = {
            't': t,
            'energy': energy,
            'energy_error': (energy - E0) / np.abs(E0),  # Relative error
            'max_error': np.max(np.abs(energy - E0)) / np.abs(E0)
        }

    return results


def time_reversibility_test(gradV: Callable, q0: np.ndarray, p0: np.ndarray,
                            step_sizes: np.ndarray, n_steps: int = 100) -> Dict:
    """
    Test time-reversibility of the Verlet integrator.

    Procedure:
    1. Integrate forward N steps
    2. Reverse momenta
    3. Integrate forward N steps (effectively backward in time)
    4. Measure position error from initial condition

    For a time-reversible integrator, this error should be at machine precision.
    For non-reversible integrators, error grows with step size.

    Parameters
    ----------
    gradV : callable
        Gradient of potential
    q0 : np.ndarray
        Initial position
    p0 : np.ndarray
        Initial momentum
    step_sizes : np.ndarray
        Array of step sizes to test
    n_steps : int
        Number of forward (and backward) steps

    Returns
    -------
    dict
        Position errors for each integrator and step size
    """
    results = {'step_sizes': step_sizes}

    # Include all integrators: symplectic (verlet, symplectic_euler) and non-symplectic (euler, rk2, rk4)
    for integrator_name, step_func in [('verlet', verlet_step),
                                        ('symplectic_euler', symplectic_euler_step),
                                        ('euler', euler_step),
                                        ('rk2', rk2_step),
                                        ('rk4', rk4_step)]:
        errors = []

        for h in step_sizes:
            q, p = q0.copy(), p0.copy()

            # Forward integration
            for _ in range(n_steps):
                q, p = step_func(q, p, h, gradV)

            # Reverse momenta
            p = -p

            # Backward integration (forward with reversed momenta)
            for _ in range(n_steps):
                q, p = step_func(q, p, h, gradV)

            # Reverse momenta again to compare with initial
            p = -p

            # Position error
            error = np.linalg.norm(q - q0)
            errors.append(error)

        results[integrator_name] = np.array(errors)

    return results


def symplectic_area_test(gradV: Callable, center_q: np.ndarray, center_p: np.ndarray,
                         radius: float, n_points: int = 50, h: float = 0.1,
                         n_steps: int = 10) -> Dict:
    """
    Test symplectic area preservation.

    Take a circle of initial conditions in phase space, integrate forward,
    and measure the area of the resulting region.

    Symplectic integrators preserve this area (Liouville's theorem).
    Non-symplectic integrators distort the area.

    Parameters
    ----------
    gradV : callable
        Gradient of potential
    center_q, center_p : np.ndarray
        Center of the circle in phase space (must be 1D)
    radius : float
        Radius of the initial circle
    n_points : int
        Number of points on the circle
    h : float
        Time step
    n_steps : int
        Number of integration steps

    Returns
    -------
    dict
        Initial and final point clouds, and area ratios
    """
    # Generate circle of initial conditions
    # For 1D system, phase space is (q, p)
    theta = np.linspace(0, 2*np.pi, n_points, endpoint=False)
    q_circle = center_q[0] + radius * np.cos(theta)
    p_circle = center_p[0] + radius * np.sin(theta)

    results = {
        'initial_q': q_circle.copy(),
        'initial_p': p_circle.copy(),
        'initial_area': np.pi * radius**2
    }

    # Include all integrators: symplectic (verlet, symplectic_euler) and non-symplectic (euler, rk2, rk4)
    for integrator_name, step_func in [('verlet', verlet_step),
                                        ('symplectic_euler', symplectic_euler_step),
                                        ('euler', euler_step),
                                        ('rk2', rk2_step),
                                        ('rk4', rk4_step)]:
        final_q = np.zeros(n_points)
        final_p = np.zeros(n_points)

        for i in range(n_points):
            q = np.array([q_circle[i]])
            p = np.array([p_circle[i]])

            for _ in range(n_steps):
                q, p = step_func(q, p, h, gradV)

            final_q[i] = q[0]
            final_p[i] = p[0]

        # Compute area using shoelace formula
        area = 0.5 * np.abs(np.sum(final_q * np.roll(final_p, -1) -
                                    np.roll(final_q, -1) * final_p))

        results[integrator_name] = {
            'final_q': final_q,
            'final_p': final_p,
            'area': area,
            'area_ratio': area / results['initial_area']
        }

    return results


def compute_local_error(gradV: Callable, q0: np.ndarray, p0: np.ndarray,
                        h: float, exact_solution: Callable = None) -> Dict:
    """
    Estimate local truncation error for a single step.

    For systems with exact solution, compare directly.
    Otherwise, use Richardson extrapolation.

    Parameters
    ----------
    gradV : callable
        Gradient of potential
    q0, p0 : np.ndarray
        Initial conditions
    h : float
        Step size
    exact_solution : callable, optional
        Function (q0, p0, t) -> (q, p) giving exact solution

    Returns
    -------
    dict
        Local errors for each integrator
    """
    results = {}

    if exact_solution is not None:
        # Compare with exact solution
        q_exact, p_exact = exact_solution(q0, p0, np.array([h]))
        q_exact, p_exact = q_exact[0], p_exact[0]

        for name, step_func in [('verlet', verlet_step),
                                ('euler', euler_step),
                                ('rk4', rk4_step)]:
            q_num, p_num = step_func(q0, p0, h, gradV)
            results[name] = {
                'q_error': np.linalg.norm(q_num - q_exact),
                'p_error': np.linalg.norm(p_num - p_exact),
                'total_error': np.linalg.norm(np.concatenate([q_num - q_exact,
                                                               p_num - p_exact]))
            }
    else:
        # Richardson extrapolation: compare with half-step result
        for name, step_func in [('verlet', verlet_step),
                                ('euler', euler_step),
                                ('rk4', rk4_step)]:
            # One step with h
            q1, p1 = step_func(q0, p0, h, gradV)

            # Two steps with h/2
            q_half, p_half = step_func(q0, p0, h/2, gradV)
            q2, p2 = step_func(q_half, p_half, h/2, gradV)

            # Error estimate (leading term)
            results[name] = {
                'q_error': np.linalg.norm(q1 - q2),
                'p_error': np.linalg.norm(p1 - p2),
                'total_error': np.linalg.norm(np.concatenate([q1 - q2, p1 - p2]))
            }

    return results


def lennard_jones_simulation(lj_system, q0: np.ndarray, p0: np.ndarray,
                              h: float, n_steps: int) -> Dict:
    """
    Run Lennard-Jones molecular dynamics simulation.

    Parameters
    ----------
    lj_system : LennardJonesSystem
        The LJ system instance
    q0, p0 : np.ndarray
        Initial conditions (flattened arrays)
    h : float
        Time step
    n_steps : int
        Number of steps

    Returns
    -------
    dict
        Simulation results for Verlet integrator
    """
    t, q_hist, p_hist = integrate(q0, p0, h, n_steps, lj_system.gradV, 'verlet')

    energy = np.array([lj_system.hamiltonian(q_hist[i], p_hist[i])
                      for i in range(len(t))])

    return {
        't': t,
        'q': q_hist,
        'p': p_hist,
        'energy': energy,
        'energy_error': energy - energy[0]
    }
