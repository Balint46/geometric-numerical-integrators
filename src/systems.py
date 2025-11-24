"""
Physical Systems for Geometric Integration
===========================================

This module implements Hamiltonian systems:
- Kepler problem (planetary motion)
- Lennard-Jones molecular dynamics (2-3 particle system)
"""

import numpy as np
from typing import Callable, Tuple


# ============================================================================
# KEPLER PROBLEM
# ============================================================================

class KeplerSystem:
    """
    The Kepler problem: motion of a planet around a fixed star.

    Potential: V(q) = -1/||q||
    Gradient: gradV(q) = q / ||q||^3

    In 2D: q = (x, y), p = (px, py)
    Hamiltonian: H = 0.5*||p||^2 - 1/||q||
    """

    def __init__(self, mu: float = 1.0):
        """
        Parameters
        ----------
        mu : float
            Gravitational parameter (G*M). Default is 1 for normalized units.
        """
        self.mu = mu

    def potential(self, q: np.ndarray) -> float:
        """Potential energy V(q) = -mu/||q||"""
        r = np.linalg.norm(q)
        return -self.mu / r

    def gradV(self, q: np.ndarray) -> np.ndarray:
        """Gradient of potential: gradV(q) = mu * q / ||q||^3"""
        r = np.linalg.norm(q)
        return self.mu * q / (r ** 3)

    def kinetic(self, p: np.ndarray) -> float:
        """Kinetic energy T(p) = 0.5*||p||^2"""
        return 0.5 * np.dot(p, p)

    def hamiltonian(self, q: np.ndarray, p: np.ndarray) -> float:
        """Total energy H(q,p) = T(p) + V(q)"""
        return self.kinetic(p) + self.potential(q)

    def angular_momentum(self, q: np.ndarray, p: np.ndarray) -> float:
        """Angular momentum L = q x p (scalar in 2D)"""
        if len(q) == 2:
            return q[0] * p[1] - q[1] * p[0]
        else:
            return np.linalg.norm(np.cross(q, p))

    def eccentricity(self, q: np.ndarray, p: np.ndarray) -> float:
        """Compute orbital eccentricity from initial conditions"""
        E = self.hamiltonian(q, p)
        L = self.angular_momentum(q, p)
        # e = sqrt(1 + 2*E*L^2/mu^2)
        return np.sqrt(1 + 2 * E * L**2 / self.mu**2)

    def get_elliptical_orbit_ic(self, e: float = 0.6, a: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get initial conditions for an elliptical orbit.

        Parameters
        ----------
        e : float
            Eccentricity (0 < e < 1 for ellipse)
        a : float
            Semi-major axis

        Returns
        -------
        q0, p0 : tuple of np.ndarray
            Initial position (at perihelion) and momentum
        """
        # Start at perihelion (closest approach)
        r_peri = a * (1 - e)
        q0 = np.array([r_peri, 0.0])

        # Velocity at perihelion (vis-viva equation)
        v_peri = np.sqrt(self.mu * (2/r_peri - 1/a))
        p0 = np.array([0.0, v_peri])

        return q0, p0

    def get_circular_orbit_ic(self, r: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """Get initial conditions for a circular orbit of radius r."""
        q0 = np.array([r, 0.0])
        v = np.sqrt(self.mu / r)
        p0 = np.array([0.0, v])
        return q0, p0


# ============================================================================
# LENNARD-JONES SYSTEM
# ============================================================================

class LennardJonesSystem:
    """
    Lennard-Jones molecular dynamics for 2-3 particles.

    Pairwise potential: V_LJ(r) = 4*epsilon * [(sigma/r)^12 - (sigma/r)^6]

    The system uses reduced units where epsilon = sigma = mass = 1.
    """

    def __init__(self, n_particles: int = 2, epsilon: float = 1.0,
                 sigma: float = 1.0, dim: int = 2):
        """
        Parameters
        ----------
        n_particles : int
            Number of particles (2 or 3)
        epsilon : float
            Depth of potential well
        sigma : float
            Distance at which potential is zero
        dim : int
            Spatial dimension (2 or 3)
        """
        self.n_particles = n_particles
        self.epsilon = epsilon
        self.sigma = sigma
        self.dim = dim

    def pairwise_potential(self, r: float) -> float:
        """Lennard-Jones potential for distance r"""
        sr6 = (self.sigma / r) ** 6
        sr12 = sr6 ** 2
        return 4 * self.epsilon * (sr12 - sr6)

    def pairwise_force_magnitude(self, r: float) -> float:
        """
        Magnitude of LJ force (positive = repulsive, negative = attractive)
        F = -dV/dr = 24*epsilon/r * [2*(sigma/r)^12 - (sigma/r)^6]
        """
        sr6 = (self.sigma / r) ** 6
        sr12 = sr6 ** 2
        return 24 * self.epsilon / r * (2 * sr12 - sr6)

    def _reshape_q(self, q: np.ndarray) -> np.ndarray:
        """Reshape flat q array to (n_particles, dim)"""
        return q.reshape(self.n_particles, self.dim)

    def potential(self, q: np.ndarray) -> float:
        """Total potential energy (sum of pairwise interactions)"""
        positions = self._reshape_q(q)
        V = 0.0

        for i in range(self.n_particles):
            for j in range(i + 1, self.n_particles):
                r_ij = np.linalg.norm(positions[i] - positions[j])
                V += self.pairwise_potential(r_ij)

        return V

    def gradV(self, q: np.ndarray) -> np.ndarray:
        """
        Gradient of potential energy.

        Returns flat array matching input shape.
        """
        positions = self._reshape_q(q)
        grad = np.zeros_like(positions)

        for i in range(self.n_particles):
            for j in range(i + 1, self.n_particles):
                r_vec = positions[i] - positions[j]
                r = np.linalg.norm(r_vec)
                r_hat = r_vec / r

                # Force magnitude (positive = repulsive)
                f_mag = self.pairwise_force_magnitude(r)

                # Force on particle i from j (and vice versa by Newton 3)
                # F = -gradV, so gradV = -F
                grad[i] -= f_mag * r_hat
                grad[j] += f_mag * r_hat

        return grad.flatten()

    def kinetic(self, p: np.ndarray) -> float:
        """Kinetic energy T(p) = 0.5*||p||^2 (unit masses)"""
        return 0.5 * np.dot(p, p)

    def hamiltonian(self, q: np.ndarray, p: np.ndarray) -> float:
        """Total energy H(q,p) = T(p) + V(q)"""
        return self.kinetic(p) + self.potential(q)

    def get_two_particle_ic(self, separation: float = 1.5,
                            velocity: float = 0.1) -> Tuple[np.ndarray, np.ndarray]:
        """
        Initial conditions for two particles.

        Parameters
        ----------
        separation : float
            Initial distance between particles
        velocity : float
            Initial velocity magnitude (perpendicular to separation)

        Returns
        -------
        q0, p0 : tuple of np.ndarray
            Flattened initial positions and momenta
        """
        # Place particles symmetrically
        q0 = np.array([
            [-separation/2, 0.0],
            [separation/2, 0.0]
        ]).flatten()

        # Give perpendicular velocities
        p0 = np.array([
            [0.0, velocity],
            [0.0, -velocity]
        ]).flatten()

        return q0, p0

    def get_three_particle_ic(self, separation: float = 1.5,
                              velocity: float = 0.1) -> Tuple[np.ndarray, np.ndarray]:
        """
        Initial conditions for three particles in equilateral triangle.

        Parameters
        ----------
        separation : float
            Side length of triangle
        velocity : float
            Initial velocity magnitude

        Returns
        -------
        q0, p0 : tuple of np.ndarray
            Flattened initial positions and momenta
        """
        # Equilateral triangle centered at origin
        r = separation / np.sqrt(3)
        angles = np.array([0, 2*np.pi/3, 4*np.pi/3])

        positions = np.array([
            [r * np.cos(a), r * np.sin(a)] for a in angles
        ])

        # Perpendicular velocities (tangent to circumscribed circle)
        momenta = np.array([
            [-velocity * np.sin(a), velocity * np.cos(a)] for a in angles
        ])

        return positions.flatten(), momenta.flatten()


# ============================================================================
# HARMONIC OSCILLATOR (for testing)
# ============================================================================

class HarmonicOscillator:
    """
    Simple harmonic oscillator for testing.

    V(q) = 0.5*omega^2*q^2
    Exact solution is known.
    """

    def __init__(self, omega: float = 1.0):
        self.omega = omega

    def potential(self, q: np.ndarray) -> float:
        return 0.5 * self.omega**2 * np.dot(q, q)

    def gradV(self, q: np.ndarray) -> np.ndarray:
        return self.omega**2 * q

    def kinetic(self, p: np.ndarray) -> float:
        return 0.5 * np.dot(p, p)

    def hamiltonian(self, q: np.ndarray, p: np.ndarray) -> float:
        return self.kinetic(p) + self.potential(q)

    def exact_solution(self, q0: np.ndarray, p0: np.ndarray, t: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Exact analytical solution"""
        A = q0
        B = p0 / self.omega

        q_exact = np.outer(np.cos(self.omega * t), A) + np.outer(np.sin(self.omega * t), B)
        p_exact = -self.omega * np.outer(np.sin(self.omega * t), A) + self.omega * np.outer(np.cos(self.omega * t), B)

        return q_exact, p_exact
