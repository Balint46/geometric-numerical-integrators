"""
Numerical Integrators for Hamiltonian Systems
==============================================

This module implements various numerical integration methods:
- Störmer-Verlet (Velocity Verlet) - symplectic, time-reversible
- Explicit Euler - non-symplectic, for comparison
- RK2 (Runge-Kutta 2nd order / Midpoint) - non-symplectic, 2nd order accuracy
- RK4 (Runge-Kutta 4th order) - high accuracy but non-symplectic

The Verlet method is implemented in kick-drift-kick splitting form.
"""

import numpy as np
from typing import Callable, Tuple


def verlet_step(q: np.ndarray, p: np.ndarray, h: float,
                gradV: Callable[[np.ndarray], np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Single step of velocity Verlet (Störmer-Verlet) integrator.

    Splitting structure (Kick-Drift-Kick):
        1. Kick: p_half = p - 0.5*h*gradV(q)
        2. Drift: q_new = q + h*p_half
        3. Kick: p_new = p_half - 0.5*h*gradV(q_new)

    Parameters
    ----------
    q : np.ndarray
        Position vector
    p : np.ndarray
        Momentum vector
    h : float
        Time step
    gradV : callable
        Gradient of potential energy V(q)

    Returns
    -------
    q_new, p_new : tuple of np.ndarray
        Updated position and momentum
    """
    # Kick (half step in momentum)
    p_half = p - 0.5 * h * gradV(q)
    # Drift (full step in position)
    q_new = q + h * p_half
    # Kick (half step in momentum)
    p_new = p_half - 0.5 * h * gradV(q_new)

    return q_new, p_new


def euler_step(q: np.ndarray, p: np.ndarray, h: float,
               gradV: Callable[[np.ndarray], np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Single step of explicit Euler integrator.

    q_new = q + h*p
    p_new = p - h*gradV(q)

    This is NOT symplectic and will show energy drift and area distortion.

    Parameters
    ----------
    q : np.ndarray
        Position vector
    p : np.ndarray
        Momentum vector
    h : float
        Time step
    gradV : callable
        Gradient of potential energy V(q)

    Returns
    -------
    q_new, p_new : tuple of np.ndarray
        Updated position and momentum
    """
    q_new = q + h * p
    p_new = p - h * gradV(q)

    return q_new, p_new


def symplectic_euler_step(q: np.ndarray, p: np.ndarray, h: float,
                          gradV: Callable[[np.ndarray], np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Single step of symplectic Euler integrator.

    p_new = p - h*gradV(q)
    q_new = q + h*p_new

    This IS symplectic but only first-order accurate.

    Parameters
    ----------
    q : np.ndarray
        Position vector
    p : np.ndarray
        Momentum vector
    h : float
        Time step
    gradV : callable
        Gradient of potential energy V(q)

    Returns
    -------
    q_new, p_new : tuple of np.ndarray
        Updated position and momentum
    """
    p_new = p - h * gradV(q)
    q_new = q + h * p_new

    return q_new, p_new


def rk2_step(q: np.ndarray, p: np.ndarray, h: float,
             gradV: Callable[[np.ndarray], np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Single step of 2nd-order Runge-Kutta (Midpoint) integrator.

    For Hamiltonian systems: dq/dt = p, dp/dt = -gradV(q)

    This is NOT symplectic and will show energy drift.
    Same order as Störmer-Verlet (2nd order) but non-symplectic,
    making it ideal for comparing energy conservation properties.

    Parameters
    ----------
    q : np.ndarray
        Position vector
    p : np.ndarray
        Momentum vector
    h : float
        Time step
    gradV : callable
        Gradient of potential energy V(q)

    Returns
    -------
    q_new, p_new : tuple of np.ndarray
        Updated position and momentum
    """
    # k1 (slope at current point)
    k1_q = p
    k1_p = -gradV(q)

    # k2 (slope at midpoint)
    k2_q = p + 0.5 * h * k1_p
    k2_p = -gradV(q + 0.5 * h * k1_q)

    # Update using midpoint slope
    q_new = q + h * k2_q
    p_new = p + h * k2_p

    return q_new, p_new


def rk4_step(q: np.ndarray, p: np.ndarray, h: float,
             gradV: Callable[[np.ndarray], np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Single step of classical 4th-order Runge-Kutta integrator.

    For Hamiltonian systems: dq/dt = p, dp/dt = -gradV(q)

    This is NOT symplectic but has high accuracy per step.
    Over long times, it will show secular energy drift.

    Parameters
    ----------
    q : np.ndarray
        Position vector
    p : np.ndarray
        Momentum vector
    h : float
        Time step
    gradV : callable
        Gradient of potential energy V(q)

    Returns
    -------
    q_new, p_new : tuple of np.ndarray
        Updated position and momentum
    """
    # k1
    k1_q = p
    k1_p = -gradV(q)

    # k2
    k2_q = p + 0.5 * h * k1_p
    k2_p = -gradV(q + 0.5 * h * k1_q)

    # k3
    k3_q = p + 0.5 * h * k2_p
    k3_p = -gradV(q + 0.5 * h * k2_q)

    # k4
    k4_q = p + h * k3_p
    k4_p = -gradV(q + h * k3_q)

    # Update
    q_new = q + (h / 6.0) * (k1_q + 2*k2_q + 2*k3_q + k4_q)
    p_new = p + (h / 6.0) * (k1_p + 2*k2_p + 2*k3_p + k4_p)

    return q_new, p_new


def integrate(q0: np.ndarray, p0: np.ndarray, h: float, n_steps: int,
              gradV: Callable[[np.ndarray], np.ndarray],
              integrator: str = 'verlet') -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Integrate a Hamiltonian system for n_steps.

    Parameters
    ----------
    q0 : np.ndarray
        Initial position
    p0 : np.ndarray
        Initial momentum
    h : float
        Time step
    n_steps : int
        Number of integration steps
    gradV : callable
        Gradient of potential energy
    integrator : str
        One of 'verlet', 'euler', 'symplectic_euler', 'rk4'

    Returns
    -------
    t : np.ndarray
        Time array
    q_hist : np.ndarray
        Position history (n_steps+1, dim)
    p_hist : np.ndarray
        Momentum history (n_steps+1, dim)
    """
    integrators = {
        'verlet': verlet_step,
        'euler': euler_step,
        'symplectic_euler': symplectic_euler_step,
        'rk2': rk2_step,
        'rk4': rk4_step
    }

    if integrator not in integrators:
        raise ValueError(f"Unknown integrator: {integrator}. Choose from {list(integrators.keys())}")

    step_func = integrators[integrator]

    dim = len(q0)
    q_hist = np.zeros((n_steps + 1, dim))
    p_hist = np.zeros((n_steps + 1, dim))
    t = np.zeros(n_steps + 1)

    q_hist[0] = q0.copy()
    p_hist[0] = p0.copy()

    q, p = q0.copy(), p0.copy()

    for i in range(n_steps):
        q, p = step_func(q, p, h, gradV)
        q_hist[i+1] = q
        p_hist[i+1] = p
        t[i+1] = (i+1) * h

    return t, q_hist, p_hist


def integrate_with_splitting_detail(q0: np.ndarray, p0: np.ndarray, h: float, n_steps: int,
                                    gradV: Callable[[np.ndarray], np.ndarray]) -> dict:
    """
    Integrate using Verlet with detailed splitting information.

    Returns intermediate states after each kick/drift operation
    for visualization of the splitting structure.

    Parameters
    ----------
    q0 : np.ndarray
        Initial position
    p0 : np.ndarray
        Initial momentum
    h : float
        Time step
    n_steps : int
        Number of steps
    gradV : callable
        Gradient of potential energy

    Returns
    -------
    dict with keys:
        'q': position history
        'p': momentum history
        'q_after_kick1': position after first kick (unchanged)
        'p_after_kick1': momentum after first kick
        'q_after_drift': position after drift
        'p_after_drift': momentum after drift (unchanged from kick1)
        'q_after_kick2': position after second kick (unchanged from drift)
        'p_after_kick2': momentum after second kick
    """
    dim = len(q0)

    result = {
        'q': [q0.copy()],
        'p': [p0.copy()],
        'q_after_kick1': [],
        'p_after_kick1': [],
        'q_after_drift': [],
        'p_after_drift': [],
        'q_after_kick2': [],
        'p_after_kick2': []
    }

    q, p = q0.copy(), p0.copy()

    for i in range(n_steps):
        # Kick 1
        p_half = p - 0.5 * h * gradV(q)
        result['q_after_kick1'].append(q.copy())
        result['p_after_kick1'].append(p_half.copy())

        # Drift
        q_new = q + h * p_half
        result['q_after_drift'].append(q_new.copy())
        result['p_after_drift'].append(p_half.copy())

        # Kick 2
        p_new = p_half - 0.5 * h * gradV(q_new)
        result['q_after_kick2'].append(q_new.copy())
        result['p_after_kick2'].append(p_new.copy())

        q, p = q_new, p_new
        result['q'].append(q.copy())
        result['p'].append(p.copy())

    # Convert to arrays
    for key in result:
        result[key] = np.array(result[key])

    return result
