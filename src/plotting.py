"""
Plotting Utilities for Geometric Integration
=============================================

This module provides visualization functions for:
- Orbit plots
- Energy error plots
- Time-reversibility tests
- Symplectic area preservation
- Splitting structure diagrams
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch, Rectangle
from matplotlib.collections import LineCollection
from typing import Dict, List, Optional
import matplotlib.animation as animation


# Color scheme
COLORS = {
    'verlet': '#2ecc71',      # Green
    'euler': '#e74c3c',       # Red
    'rk2': '#e67e22',         # Orange (for RK2 - same order as Verlet)
    'rk4': '#3498db',         # Blue
    'symplectic_euler': '#9b59b6',  # Purple
    'exact': '#34495e'        # Dark gray
}

LABELS = {
    'verlet': 'Verlet (Symplectic)',
    'euler': 'Explicit Euler',
    'rk2': 'RK2 (Non-Symplectic)',
    'rk4': 'RK4',
    'symplectic_euler': 'Symplectic Euler'
}


def plot_kepler_orbits(results: Dict, title: str = "Kepler Orbit Comparison",
                       figsize: tuple = (16, 5)) -> plt.Figure:
    """
    Plot Kepler orbits for different integrators.
    """
    # Check which integrators are available
    available = [i for i in ['verlet', 'rk2', 'euler', 'rk4'] if i in results]
    n_plots = len(available)
    fig, axes = plt.subplots(1, n_plots, figsize=(4*n_plots, 5))
    if n_plots == 1:
        axes = [axes]

    for ax, integrator in zip(axes, available):
        data = results[integrator]
        q = data['q']

        ax.plot(q[:, 0], q[:, 1], color=COLORS[integrator], alpha=0.7, linewidth=0.5)
        ax.plot(0, 0, 'ko', markersize=10, label='Central body')
        ax.plot(q[0, 0], q[0, 1], 'go', markersize=5, label='Start')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(LABELS[integrator])
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    return fig


def plot_orbit_comparison(results: Dict, figsize: tuple = (8, 8)) -> plt.Figure:
    """
    Plot all orbits on a single figure for comparison.
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Include all available integrators
    for integrator in ['verlet', 'rk2', 'euler', 'rk4']:
        if integrator in results:
            data = results[integrator]
            q = data['q']
            ax.plot(q[:, 0], q[:, 1], color=COLORS[integrator],
                    alpha=0.7, linewidth=0.8, label=LABELS[integrator])

    ax.plot(0, 0, 'ko', markersize=12, label='Central body', zorder=5)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_title('Orbit Comparison', fontsize=14)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    plt.tight_layout()
    return fig


def plot_rk4_verlet_contrast(results: Dict, figsize: tuple = (14, 6)) -> plt.Figure:
    """
    Create a detailed contrast plot between RK4 and Verlet methods.
    Shows orbit overlay and energy error side by side.
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)

    # Left: Orbit comparison (zoomed on differences)
    ax = axes[0]
    q_verlet = results['verlet']['q']
    q_rk4 = results['rk4']['q']

    ax.plot(q_verlet[:, 0], q_verlet[:, 1], color=COLORS['verlet'],
            linewidth=1.5, label=LABELS['verlet'], alpha=0.8)
    ax.plot(q_rk4[:, 0], q_rk4[:, 1], color=COLORS['rk4'],
            linewidth=1.5, label=LABELS['rk4'], alpha=0.8, linestyle='--')
    ax.plot(0, 0, 'ko', markersize=12, zorder=5)

    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_title('Orbit Comparison: Verlet vs RK4', fontsize=13)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    # Right: Energy error comparison
    ax = axes[1]
    t_verlet = results['verlet']['t']
    t_rk4 = results['rk4']['t']
    E_err_verlet = np.abs(results['verlet']['energy_error'])
    E_err_rk4 = np.abs(results['rk4']['energy_error'])

    ax.semilogy(t_verlet, E_err_verlet, color=COLORS['verlet'],
                linewidth=1.5, label=LABELS['verlet'])
    ax.semilogy(t_rk4, E_err_rk4, color=COLORS['rk4'],
                linewidth=1.5, label=LABELS['rk4'])

    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('|Energy Error|', fontsize=12)
    ax.set_title('Energy Error: Verlet (bounded) vs RK4 (drift)', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    # Add annotation explaining the difference
    ax.text(0.02, 0.98, 'Verlet: oscillates (bounded)\nRK4: secular drift',
            transform=ax.transAxes, fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    return fig


def plot_energy_error(results: Dict, title: str = "Energy Error Over Time",
                      figsize: tuple = (10, 6), log_scale: bool = True) -> plt.Figure:
    """
    Plot energy error over time for different integrators.
    """
    fig, ax = plt.subplots(figsize=figsize)

    for integrator in results:
        if integrator == 'step_sizes':
            continue
        data = results[integrator]
        t = data['t']
        error = np.abs(data['energy_error'])

        ax.plot(t, error, color=COLORS.get(integrator, 'gray'),
                label=LABELS.get(integrator, integrator), linewidth=1)

    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('|Energy Error| / |E₀|', fontsize=12)
    ax.set_title(title, fontsize=14)
    if log_scale:
        ax.set_yscale('log')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    plt.tight_layout()
    return fig


def plot_long_term_energy(results: Dict, figsize: tuple = (12, 5)) -> plt.Figure:
    """
    Plot long-term energy behaviour with comparison.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Linear scale
    for integrator in results:
        if integrator == 'step_sizes':
            continue
        data = results[integrator]
        ax1.plot(data['t'], data['energy_error'],
                 color=COLORS.get(integrator, 'gray'),
                 label=LABELS.get(integrator, integrator), linewidth=0.8)

    ax1.set_xlabel('Time', fontsize=11)
    ax1.set_ylabel('Relative Energy Error', fontsize=11)
    ax1.set_title('Energy Error (Linear Scale)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=9)

    # Log scale of absolute error
    for integrator in results:
        if integrator == 'step_sizes':
            continue
        data = results[integrator]
        ax2.plot(data['t'], np.abs(data['energy_error']),
                 color=COLORS.get(integrator, 'gray'),
                 label=LABELS.get(integrator, integrator), linewidth=0.8)

    ax2.set_xlabel('Time', fontsize=11)
    ax2.set_ylabel('|Relative Energy Error|', fontsize=11)
    ax2.set_title('Energy Error (Log Scale)', fontsize=12)
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=9)

    plt.tight_layout()
    return fig


def plot_reversibility_test(results: Dict, figsize: tuple = (10, 7)) -> plt.Figure:
    """
    Plot time-reversibility test results including symplectic Euler.
    """
    fig, ax = plt.subplots(figsize=figsize)

    h = results['step_sizes']

    # Plot all integrators including symplectic_euler and rk2
    for integrator in ['verlet', 'symplectic_euler', 'euler', 'rk2', 'rk4']:
        if integrator in results:
            errors = results[integrator]
            ax.loglog(h, errors, 'o-', color=COLORS[integrator],
                      label=LABELS[integrator], linewidth=2, markersize=8)

    # Reference lines
    ref_error = results['euler'][0] if 'euler' in results else results['rk4'][0]
    ax.loglog(h, h**2 * ref_error/h[0]**2, 'k--', alpha=0.5, linewidth=1.5, label='O(h²)')
    ax.loglog(h, h * ref_error/h[0], 'k:', alpha=0.5, linewidth=1.5, label='O(h)')

    ax.set_xlabel('Step Size h', fontsize=12)
    ax.set_ylabel('Position Error After Reversal', fontsize=12)
    ax.set_title('Time-Reversibility Test\n(Forward N steps → Reverse momenta → Backward N steps)',
                 fontsize=13)
    ax.grid(True, alpha=0.3, which='both')
    ax.legend(fontsize=10, loc='upper left')

    # Add explanation text
    ax.text(0.98, 0.02, 'Time-reversible methods return to\ninitial state (error ~ machine precision)',
            transform=ax.transAxes, fontsize=9, verticalalignment='bottom',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

    plt.tight_layout()
    return fig


def plot_symplectic_area(results: Dict, figsize: tuple = (20, 8)) -> plt.Figure:
    """
    Plot symplectic area preservation test including symplectic Euler and RK2.
    Shows all integrators with clear visual differences.
    """
    # Determine which integrators we have
    integrators = ['verlet', 'symplectic_euler', 'euler', 'rk2', 'rk4']
    available = [i for i in integrators if i in results]

    n_plots = len(available) + 1  # +1 for initial circle
    fig, axes = plt.subplots(1, n_plots, figsize=(4*n_plots, 6))

    # Initial circle
    ax = axes[0]
    theta = np.linspace(0, 2*np.pi, len(results['initial_q']) + 1)
    q_closed = np.append(results['initial_q'], results['initial_q'][0])
    p_closed = np.append(results['initial_p'], results['initial_p'][0])

    ax.fill(q_closed, p_closed, alpha=0.4, color='gray', edgecolor='black', linewidth=2)
    ax.set_title(f"Initial Circle\nArea = {results['initial_area']:.4f}", fontsize=12)
    ax.set_xlabel('Position q', fontsize=11)
    ax.set_ylabel('Momentum p', fontsize=11)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    # Get axis limits from initial circle
    q_range = np.max(results['initial_q']) - np.min(results['initial_q'])
    p_range = np.max(results['initial_p']) - np.min(results['initial_p'])
    q_center = (np.max(results['initial_q']) + np.min(results['initial_q'])) / 2
    p_center = (np.max(results['initial_p']) + np.min(results['initial_p'])) / 2
    margin = max(q_range, p_range) * 1.5

    ax.set_xlim(q_center - margin, q_center + margin)
    ax.set_ylim(p_center - margin, p_center + margin)

    # Final shapes for each integrator
    for ax, integrator in zip(axes[1:], available):
        data = results[integrator]

        # Close the polygon
        q_closed = np.append(data['final_q'], data['final_q'][0])
        p_closed = np.append(data['final_p'], data['final_p'][0])

        ax.fill(q_closed, p_closed,
                alpha=0.4, color=COLORS[integrator], edgecolor=COLORS[integrator],
                linewidth=2)

        # Add initial circle for reference
        init_q_closed = np.append(results['initial_q'], results['initial_q'][0])
        init_p_closed = np.append(results['initial_p'], results['initial_p'][0])
        ax.plot(init_q_closed, init_p_closed, 'k--', alpha=0.5, linewidth=1.5,
                label='Initial')

        # Calculate area ratio and determine if preserved
        ratio = data['area_ratio']
        status = "PRESERVED" if abs(ratio - 1.0) < 0.01 else "DISTORTED"
        status_color = 'green' if status == "PRESERVED" else 'red'

        ax.set_title(f"{LABELS[integrator]}\nArea Ratio = {ratio:.4f} ({status})",
                     fontsize=11, color=status_color if status == "DISTORTED" else 'black')
        ax.set_xlabel('Position q', fontsize=11)
        ax.set_ylabel('Momentum p', fontsize=11)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)

        # Use same axis limits for fair comparison
        ax.set_xlim(q_center - margin, q_center + margin)
        ax.set_ylim(p_center - margin, p_center + margin)

    plt.suptitle('Symplectic Area Preservation Test\n(Symplectic methods preserve phase space volume)',
                 fontsize=14, y=1.02)
    plt.tight_layout()
    return fig


def plot_splitting_diagram(figsize: tuple = (14, 10)) -> plt.Figure:
    """
    Create an improved step-by-step diagram of the kick-drift-kick splitting.
    Shows the flow in phase space with clear annotations.
    """
    fig = plt.figure(figsize=figsize)

    # Create a single large plot showing the full trajectory
    ax_main = fig.add_subplot(111)

    # Define the trajectory points for visualization
    # Starting point
    q0, p0 = 1.0, 2.0

    # After Kick 1 (momentum decreases, position unchanged)
    q1, p1 = 1.0, 1.4

    # After Drift (position increases along momentum direction)
    q2, p2 = 1.7, 1.4

    # After Kick 2 (momentum decreases again)
    q3, p3 = 1.7, 0.9

    # Plot the three stages with distinct colors and styles
    stages = [
        ((q0, p0), (q1, p1), 'KICK 1', '#e74c3c', 'Momentum update:\np₁/₂ = p - ½h∇V(q)'),
        ((q1, p1), (q2, p2), 'DRIFT', '#f39c12', 'Position update:\nq_new = q + h·p₁/₂'),
        ((q2, p2), (q3, p3), 'KICK 2', '#9b59b6', 'Momentum update:\np_new = p₁/₂ - ½h∇V(q_new)')
    ]

    # Draw the stages
    for (start, end, label, color, formula) in stages:
        # Draw arrow
        ax_main.annotate('', xy=end, xytext=start,
                        arrowprops=dict(arrowstyle='->', color=color, lw=4,
                                       mutation_scale=25))

        # Label the arrow
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2

        # Offset for label placement
        if label == 'KICK 1':
            ax_main.text(mid_x - 0.3, mid_y, f'{label}\n{formula}',
                        fontsize=10, ha='right', va='center',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.3))
        elif label == 'DRIFT':
            ax_main.text(mid_x, mid_y + 0.3, f'{label}\n{formula}',
                        fontsize=10, ha='center', va='bottom',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.3))
        else:
            ax_main.text(mid_x + 0.3, mid_y, f'{label}\n{formula}',
                        fontsize=10, ha='left', va='center',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.3))

    # Draw points
    points = [
        (q0, p0, '(qₙ, pₙ)\nInitial', 'blue', 200),
        (q1, p1, '(qₙ, p₁/₂)\nAfter Kick 1', '#e74c3c', 150),
        (q2, p2, '(qₙ₊₁, p₁/₂)\nAfter Drift', '#f39c12', 150),
        (q3, p3, '(qₙ₊₁, pₙ₊₁)\nFinal', '#9b59b6', 200)
    ]

    for x, y, label, color, size in points:
        ax_main.scatter([x], [y], s=size, c=color, zorder=10, edgecolors='black', linewidth=2)
        if 'Initial' in label:
            ax_main.annotate(label, (x, y), xytext=(-50, 20), textcoords='offset points',
                           fontsize=10, fontweight='bold',
                           arrowprops=dict(arrowstyle='->', color='gray'))
        elif 'Final' in label:
            ax_main.annotate(label, (x, y), xytext=(20, -40), textcoords='offset points',
                           fontsize=10, fontweight='bold',
                           arrowprops=dict(arrowstyle='->', color='gray'))

    ax_main.set_xlim(0.3, 2.5)
    ax_main.set_ylim(0.3, 2.5)
    ax_main.set_xlabel('Position q', fontsize=14)
    ax_main.set_ylabel('Momentum p', fontsize=14)
    ax_main.set_title('Störmer-Verlet: Kick-Drift-Kick Splitting in Phase Space\n'
                      'One complete integration step from (qₙ, pₙ) to (qₙ₊₁, pₙ₊₁)',
                      fontsize=14, fontweight='bold')
    ax_main.grid(True, alpha=0.3)
    ax_main.set_aspect('equal')

    # Add legend box explaining the structure
    legend_text = ('Splitting Structure:\n'
                   '━━━━━━━━━━━━━━━━━━━━\n'
                   '1. KICK: Update p (force acts)\n'
                   '2. DRIFT: Update q (free motion)\n'
                   '3. KICK: Update p (force acts)\n'
                   '━━━━━━━━━━━━━━━━━━━━\n'
                   'This is symmetric & reversible!')

    ax_main.text(0.02, 0.98, legend_text, transform=ax_main.transAxes,
                fontsize=10, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

    plt.tight_layout()
    return fig


def plot_splitting_flow(splitting_data: Dict, step_idx: int = 0,
                        figsize: tuple = (10, 8)) -> plt.Figure:
    """
    Plot the flow of a single Verlet step showing kick-drift-kick
    with clear annotations explaining each phase.
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Extract data for the specified step
    q0, p0 = splitting_data['q'][step_idx], splitting_data['p'][step_idx]
    q_k1, p_k1 = splitting_data['q_after_kick1'][step_idx], splitting_data['p_after_kick1'][step_idx]
    q_d, p_d = splitting_data['q_after_drift'][step_idx], splitting_data['p_after_drift'][step_idx]
    q_k2, p_k2 = splitting_data['q_after_kick2'][step_idx], splitting_data['p_after_kick2'][step_idx]

    # For 2D systems, plot in position space
    if len(q0) >= 2:
        # Plot central body
        ax.scatter([0], [0], s=300, c='black', marker='*', zorder=10, label='Central body')

        # Draw trajectory with annotations
        points = [
            (q0[0], q0[1], 'Start\n(qₙ)', 'blue', 150),
            (q_d[0], q_d[1], 'After Drift\n(qₙ₊₁)', 'orange', 150),
        ]

        for x, y, label, color, size in points:
            ax.scatter([x], [y], s=size, c=color, zorder=5, edgecolors='black', linewidth=2)
            ax.annotate(label, (x, y), xytext=(10, 10), textcoords='offset points',
                       fontsize=10, fontweight='bold')

        # Draw the drift arrow
        ax.annotate('', xy=(q_d[0], q_d[1]), xytext=(q0[0], q0[1]),
                   arrowprops=dict(arrowstyle='->', color='orange', lw=3, mutation_scale=20))

        ax.set_xlabel('x position', fontsize=12)
        ax.set_ylabel('y position', fontsize=12)
        ax.set_title(f'Verlet Step {step_idx}: Position Update (Drift Phase)\n'
                     f'Kick operations only change momentum (not visible in position space)',
                     fontsize=12)

    else:
        # 1D case: plot in (q, p) phase space
        stages = [
            ((q0[0], p0[0]), (q_k1[0], p_k1[0]), 'Kick 1', '#e74c3c'),
            ((q_k1[0], p_k1[0]), (q_d[0], p_d[0]), 'Drift', '#f39c12'),
            ((q_d[0], p_d[0]), (q_k2[0], p_k2[0]), 'Kick 2', '#9b59b6'),
        ]

        for (start, end, label, color) in stages:
            ax.annotate('', xy=end, xytext=start,
                       arrowprops=dict(arrowstyle='->', color=color, lw=3, mutation_scale=20))
            mid = ((start[0]+end[0])/2, (start[1]+end[1])/2)
            ax.annotate(label, mid, fontsize=10, fontweight='bold', color=color)

        points = [
            (q0[0], p0[0], 'Initial', 'blue'),
            (q_k1[0], p_k1[0], 'After Kick 1', '#e74c3c'),
            (q_d[0], p_d[0], 'After Drift', '#f39c12'),
            (q_k2[0], p_k2[0], 'Final', '#9b59b6')
        ]

        for x, y, label, color in points:
            ax.scatter([x], [y], s=150, c=color, zorder=5, edgecolors='black', linewidth=2)
            ax.annotate(label, (x, y), xytext=(10, 10), textcoords='offset points', fontsize=10)

        ax.set_xlabel('Position q', fontsize=12)
        ax.set_ylabel('Momentum p', fontsize=12)
        ax.set_title(f'Kick-Drift-Kick in Phase Space (Step {step_idx})', fontsize=14)

    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    plt.tight_layout()
    return fig


def plot_lennard_jones(results: Dict, lj_system, figsize: tuple = (15, 10)) -> plt.Figure:
    """
    Plot Lennard-Jones simulation results with detailed descriptions.
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize)

    t = results['t']
    q = results['q']
    n_particles = lj_system.n_particles
    dim = lj_system.dim

    # Panel 1: Trajectory in space
    ax = axes[0, 0]
    positions = q.reshape(-1, n_particles, dim)

    colors = plt.cm.tab10(np.linspace(0, 1, n_particles))
    for i in range(n_particles):
        ax.plot(positions[:, i, 0], positions[:, i, 1],
                color=colors[i], alpha=0.7, linewidth=0.5)
        ax.scatter(positions[0, i, 0], positions[0, i, 1],
                  color=colors[i], s=150, marker='o', edgecolors='black',
                  label=f'Particle {i+1} (start)', zorder=5)
        ax.scatter(positions[-1, i, 0], positions[-1, i, 1],
                  color=colors[i], s=150, marker='s', edgecolors='black', zorder=5)

    ax.set_xlabel('x position')
    ax.set_ylabel('y position')
    ax.set_title('Particle Trajectories in Space\n'
                 '(Circle = start, Square = end)', fontsize=11)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, loc='upper right')

    # Panel 2: Pairwise distance over time with description
    ax = axes[0, 1]
    r_eq = lj_system.sigma * 2**(1/6)

    for i in range(n_particles):
        for j in range(i+1, n_particles):
            r_ij = np.linalg.norm(positions[:, i, :] - positions[:, j, :], axis=1)
            ax.plot(t, r_ij, label=f'r_{i+1}{j+1}', linewidth=1.5)

    ax.axhline(y=r_eq, color='red', linestyle='--', alpha=0.8, linewidth=2,
               label=f'Equilibrium r = {r_eq:.3f}')
    ax.axhline(y=lj_system.sigma, color='gray', linestyle=':', alpha=0.7,
               label=f'σ = {lj_system.sigma}')

    ax.set_xlabel('Time')
    ax.set_ylabel('Distance between particles')
    ax.set_title('Pairwise Distances Over Time\n'
                 '(Oscillations around equilibrium distance)', fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)

    # Add explanation
    ax.text(0.02, 0.98, f'r_eq = 2^(1/6)·σ ≈ {r_eq:.3f}\n'
            'Particles oscillate around\nequilibrium separation',
            transform=ax.transAxes, fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # Panel 3: Energy conservation
    ax = axes[1, 0]
    ax.plot(t, results['energy'], 'b-', linewidth=1, label='Total Energy')
    ax.axhline(y=results['energy'][0], color='red', linestyle='--',
               alpha=0.7, label='Initial Energy')

    ax.set_xlabel('Time')
    ax.set_ylabel('Total Energy')
    ax.set_title('Energy Conservation (Verlet Method)\n'
                 'Symplectic integrators preserve energy well', fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9)

    # Panel 4: Energy error
    ax = axes[1, 1]
    ax.plot(t, results['energy_error'], 'g-', linewidth=1)
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.5)

    max_err = np.max(np.abs(results['energy_error']))
    ax.set_xlabel('Time')
    ax.set_ylabel('Energy Error (E - E₀)')
    ax.set_title(f'Energy Error Over Time\n'
                 f'Maximum |ΔE| = {max_err:.2e} (bounded, no drift!)', fontsize=11)
    ax.grid(True, alpha=0.3)

    # Add annotation
    ax.text(0.98, 0.98, 'Symplectic integrator:\n• Error oscillates\n• No secular drift\n• Bounded for all time',
            transform=ax.transAxes, fontsize=9, verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    plt.suptitle(f'Lennard-Jones Molecular Dynamics ({n_particles} particles)',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    return fig


def plot_convergence(results: Dict, figsize: tuple = (8, 6)) -> plt.Figure:
    """
    Plot convergence study results.
    """
    fig, ax = plt.subplots(figsize=figsize)

    h = results['step_sizes']

    for integrator in ['verlet', 'rk2', 'euler', 'rk4']:
        if integrator in results:
            errors = results[integrator]
            ax.loglog(h, errors, 'o-', color=COLORS[integrator],
                      label=LABELS[integrator], linewidth=2, markersize=6)

    # Reference lines
    ax.loglog(h, h, 'k:', alpha=0.5, label='O(h)')
    ax.loglog(h, h**2, 'k--', alpha=0.5, label='O(h²)')
    ax.loglog(h, h**4, 'k-.', alpha=0.5, label='O(h⁴)')

    ax.set_xlabel('Step Size h', fontsize=12)
    ax.set_ylabel('Global Error', fontsize=12)
    ax.set_title('Convergence Study', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    plt.tight_layout()
    return fig


def plot_sv_vs_rk4_long_term(results: Dict, figsize: tuple = (14, 6)) -> plt.Figure:
    """
    Create a detailed comparison plot between Störmer-Verlet and RK4 over long time periods.
    Shows that RK4 eventually drifts significantly while SV remains bounded.
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)

    # Left: Orbit comparison
    ax = axes[0]
    q_verlet = results['verlet']['q']
    q_rk4 = results['rk4']['q']

    ax.plot(q_verlet[:, 0], q_verlet[:, 1], color=COLORS['verlet'],
            linewidth=1, label=LABELS['verlet'], alpha=0.8)
    ax.plot(q_rk4[:, 0], q_rk4[:, 1], color=COLORS['rk4'],
            linewidth=1, label=LABELS['rk4'], alpha=0.8)
    ax.plot(0, 0, 'ko', markersize=12, zorder=5)

    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_title('Long-term Orbit: Verlet vs RK4\n(RK4 drifts over time)', fontsize=13)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    # Right: Energy error comparison showing crossover
    ax = axes[1]
    t_verlet = results['verlet']['t']
    t_rk4 = results['rk4']['t']
    E_err_verlet = np.abs(results['verlet']['energy_error'])
    E_err_rk4 = np.abs(results['rk4']['energy_error'])

    ax.semilogy(t_verlet, E_err_verlet, color=COLORS['verlet'],
                linewidth=1, label=LABELS['verlet'], alpha=0.8)
    ax.semilogy(t_rk4, E_err_rk4, color=COLORS['rk4'],
                linewidth=1, label=LABELS['rk4'], alpha=0.8)

    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('|Energy Error|', fontsize=12)
    ax.set_title('Energy Error: Verlet (bounded) vs RK4 (unbounded drift)', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    # Add annotation
    ax.text(0.02, 0.98, 'RK4 error grows without bound\nVerlet error oscillates (bounded)',
            transform=ax.transAxes, fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    return fig


def plot_sv_vs_rk2_euler_short_term(results: Dict, figsize: tuple = (16, 6)) -> plt.Figure:
    """
    Create comparison plot between Störmer-Verlet, RK2, and Explicit Euler over short time.
    Shows the quick drift of RK2 and Euler compared to SV.
    """
    fig, axes = plt.subplots(1, 3, figsize=figsize)

    # Left: Orbit comparison
    ax = axes[0]
    q_verlet = results['verlet']['q']
    q_rk2 = results['rk2']['q']
    q_euler = results['euler']['q']

    ax.plot(q_verlet[:, 0], q_verlet[:, 1], color=COLORS['verlet'],
            linewidth=1.5, label=LABELS['verlet'], alpha=0.9)
    ax.plot(q_rk2[:, 0], q_rk2[:, 1], color=COLORS['rk2'],
            linewidth=1.5, label=LABELS['rk2'], alpha=0.9)
    ax.plot(q_euler[:, 0], q_euler[:, 1], color=COLORS['euler'],
            linewidth=1.5, label=LABELS['euler'], alpha=0.9)
    ax.plot(0, 0, 'ko', markersize=12, zorder=5)

    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_title('Orbit Comparison\n(Short-term)', fontsize=13)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    # Middle: Energy error on linear scale
    ax = axes[1]
    t_verlet = results['verlet']['t']
    t_rk2 = results['rk2']['t']
    t_euler = results['euler']['t']

    ax.plot(t_verlet, results['verlet']['energy_error'], color=COLORS['verlet'],
            linewidth=1.5, label=LABELS['verlet'])
    ax.plot(t_rk2, results['rk2']['energy_error'], color=COLORS['rk2'],
            linewidth=1.5, label=LABELS['rk2'])
    ax.plot(t_euler, results['euler']['energy_error'], color=COLORS['euler'],
            linewidth=1.5, label=LABELS['euler'])

    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Energy Error', fontsize=12)
    ax.set_title('Energy Error (Linear Scale)\nRK2/Euler drift quickly', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    # Right: Energy error on log scale
    ax = axes[2]
    E_err_verlet = np.abs(results['verlet']['energy_error'])
    E_err_rk2 = np.abs(results['rk2']['energy_error'])
    E_err_euler = np.abs(results['euler']['energy_error'])

    ax.semilogy(t_verlet, E_err_verlet + 1e-16, color=COLORS['verlet'],
                linewidth=1.5, label=LABELS['verlet'])
    ax.semilogy(t_rk2, E_err_rk2 + 1e-16, color=COLORS['rk2'],
                linewidth=1.5, label=LABELS['rk2'])
    ax.semilogy(t_euler, E_err_euler + 1e-16, color=COLORS['euler'],
                linewidth=1.5, label=LABELS['euler'])

    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('|Energy Error|', fontsize=12)
    ax.set_title('Energy Error (Log Scale)\nExponential growth visible', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    plt.suptitle('Short-term Comparison: Störmer-Verlet vs RK2 vs Explicit Euler\n'
                 '(Both RK2 and Euler drift; only Verlet preserves energy)',
                 fontsize=14, y=1.02)
    plt.tight_layout()
    return fig


def plot_energy_crossover(results: Dict, figsize: tuple = (12, 8)) -> plt.Figure:
    """
    Create a plot specifically showing the energy error crossover point
    where RK4 error exceeds SV error.
    """
    fig, axes = plt.subplots(2, 1, figsize=figsize)

    t_verlet = results['verlet']['t']
    t_rk4 = results['rk4']['t']
    E_err_verlet = np.abs(results['verlet']['energy_error'])
    E_err_rk4 = np.abs(results['rk4']['energy_error'])

    # Top: Full comparison on log scale
    ax = axes[0]
    ax.semilogy(t_verlet, E_err_verlet, color=COLORS['verlet'],
                linewidth=1.5, label=f'{LABELS["verlet"]} (bounded)', alpha=0.9)
    ax.semilogy(t_rk4, E_err_rk4, color=COLORS['rk4'],
                linewidth=1.5, label=f'{LABELS["rk4"]} (grows)', alpha=0.9)

    # Find crossover point (where RK4 error exceeds max Verlet error)
    max_verlet_error = np.max(E_err_verlet)
    crossover_indices = np.where(E_err_rk4 > max_verlet_error)[0]
    if len(crossover_indices) > 0:
        crossover_idx = crossover_indices[0]
        crossover_time = t_rk4[crossover_idx]
        ax.axvline(x=crossover_time, color='purple', linestyle='--', alpha=0.7,
                   label=f'Crossover at t ≈ {crossover_time:.1f}')
        ax.axhline(y=max_verlet_error, color='gray', linestyle=':', alpha=0.5)

    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('|Energy Error|', fontsize=12)
    ax.set_title('Energy Error: RK4 Eventually Exceeds Verlet\n'
                 '(RK4 has higher per-step accuracy but unbounded long-term error)', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    # Bottom: Ratio of errors
    ax = axes[1]
    min_len = min(len(E_err_verlet), len(E_err_rk4))
    ratio = E_err_rk4[:min_len] / (E_err_verlet[:min_len] + 1e-16)
    ax.semilogy(t_verlet[:min_len], ratio, color='purple', linewidth=1.5)
    ax.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Equal error (ratio = 1)')

    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('|E_RK4| / |E_Verlet|', fontsize=12)
    ax.set_title('Error Ratio: RK4 / Verlet\n(Ratio > 1 means RK4 is worse)', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    # Add annotation
    ax.text(0.98, 0.98, 'RK4: O(h⁴) per step\nbut grows linearly in time\n\n'
                         'Verlet: O(h²) per step\nbut bounded for all time',
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

    plt.tight_layout()
    return fig


def plot_symplectic_area_enhanced(results: Dict, figsize: tuple = (16, 8)) -> plt.Figure:
    """
    Enhanced symplectic area preservation plot showing clear visual distortion
    for RK2 and Explicit Euler compared to Symplectic Euler and Verlet.
    """
    fig, axes = plt.subplots(2, 3, figsize=figsize)
    axes = axes.flatten()

    # Initial circle
    ax = axes[0]
    q_closed = np.append(results['initial_q'], results['initial_q'][0])
    p_closed = np.append(results['initial_p'], results['initial_p'][0])

    ax.fill(q_closed, p_closed, alpha=0.4, color='gray', edgecolor='black', linewidth=2)
    ax.plot(q_closed, p_closed, 'k-', linewidth=2)
    ax.set_title(f"Initial Circle\nArea = {results['initial_area']:.4f}", fontsize=11)
    ax.set_xlabel('Position q', fontsize=10)
    ax.set_ylabel('Momentum p', fontsize=10)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    # Get axis limits
    margin = 2.0
    all_q = [results['initial_q']]
    all_p = [results['initial_p']]
    for integrator in ['verlet', 'symplectic_euler', 'euler', 'rk2', 'rk4']:
        if integrator in results:
            all_q.append(results[integrator]['final_q'])
            all_p.append(results[integrator]['final_p'])
    all_q = np.concatenate(all_q)
    all_p = np.concatenate(all_p)

    q_min, q_max = np.min(all_q) - 0.5, np.max(all_q) + 0.5
    p_min, p_max = np.min(all_p) - 0.5, np.max(all_p) + 0.5

    ax.set_xlim(q_min, q_max)
    ax.set_ylim(p_min, p_max)

    # Symplectic methods (preserved)
    symplectic_order = ['verlet', 'symplectic_euler']
    # Non-symplectic methods (distorted)
    non_symplectic_order = ['euler', 'rk2', 'rk4']

    plot_order = symplectic_order + non_symplectic_order
    plot_idx = 1

    for integrator in plot_order:
        if integrator not in results:
            continue

        ax = axes[plot_idx]
        data = results[integrator]

        # Close the polygon
        q_final = np.append(data['final_q'], data['final_q'][0])
        p_final = np.append(data['final_p'], data['final_p'][0])

        # Draw final shape
        ax.fill(q_final, p_final, alpha=0.4, color=COLORS[integrator],
                edgecolor=COLORS[integrator], linewidth=2)
        ax.plot(q_final, p_final, color=COLORS[integrator], linewidth=2)

        # Draw initial circle for reference
        ax.plot(q_closed, p_closed, 'k--', alpha=0.4, linewidth=1.5, label='Initial')

        # Calculate area ratio and determine status
        ratio = data['area_ratio']
        is_preserved = abs(ratio - 1.0) < 0.01
        status = "PRESERVED" if is_preserved else "DISTORTED"
        status_color = 'green' if is_preserved else 'red'

        ax.set_title(f"{LABELS[integrator]}\nArea Ratio = {ratio:.4f}\n({status})",
                     fontsize=10, color=status_color if not is_preserved else 'black',
                     fontweight='bold' if not is_preserved else 'normal')
        ax.set_xlabel('Position q', fontsize=10)
        ax.set_ylabel('Momentum p', fontsize=10)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(q_min, q_max)
        ax.set_ylim(p_min, p_max)

        plot_idx += 1

    plt.suptitle('Symplectic Area Preservation Test\n'
                 'Symplectic methods (Verlet, Symplectic Euler) preserve area; '
                 'Non-symplectic methods (Euler, RK2, RK4) distort it',
                 fontsize=13, y=1.02)
    plt.tight_layout()
    return fig


def create_exact_vs_sv_animation(results: Dict, kepler_system,
                                  interval: int = 40, skip: int = 10,
                                  max_frames: int = 300) -> animation.FuncAnimation:
    """
    Create a focused animation comparing the exact orbit with Störmer-Verlet.
    Shows how well SV tracks the true solution.
    """
    q_verlet = results['verlet']['q'][::skip]
    t_verlet = results['verlet']['t'][::skip]

    n_frames = min(len(q_verlet), max_frames)
    q_verlet = q_verlet[:n_frames]
    t_verlet = t_verlet[:n_frames]

    # Compute exact orbit
    E = results['verlet']['energy'][0]
    L = kepler_system.angular_momentum(results['verlet']['q'][0], results['verlet']['p'][0])
    a = -kepler_system.mu / (2 * E)
    e = kepler_system.eccentricity(results['verlet']['q'][0], results['verlet']['p'][0])

    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw exact orbit
    theta_exact = np.linspace(0, 2*np.pi, 500)
    r_exact = a * (1 - e**2) / (1 + e * np.cos(theta_exact))
    x_exact = r_exact * np.cos(theta_exact)
    y_exact = r_exact * np.sin(theta_exact)
    ax.plot(x_exact, y_exact, 'k-', linewidth=2, alpha=0.7, label='Exact orbit')

    # Set up axes
    margin = 0.5
    ax.set_xlim(np.min(x_exact) - margin, np.max(x_exact) + margin)
    ax.set_ylim(np.min(y_exact) - margin, np.max(y_exact) + margin)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    # Central body
    ax.plot(0, 0, 'yo', markersize=20, markeredgecolor='orange', markeredgewidth=2, zorder=10)

    # Initialize trail and point
    line_verlet, = ax.plot([], [], color=COLORS['verlet'], alpha=0.8, linewidth=2,
                           label='Störmer-Verlet')
    point_verlet, = ax.plot([], [], 'o', color=COLORS['verlet'], markersize=12,
                            markeredgecolor='black', markeredgewidth=2)

    ax.legend(loc='upper right', fontsize=11)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_title('Exact Orbit vs Störmer-Verlet\n(Verlet stays on the exact orbit)', fontsize=13)

    time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, fontsize=10,
                        verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    def init():
        line_verlet.set_data([], [])
        point_verlet.set_data([], [])
        time_text.set_text('')
        return line_verlet, point_verlet, time_text

    def animate(frame):
        line_verlet.set_data(q_verlet[:frame+1, 0], q_verlet[:frame+1, 1])
        point_verlet.set_data([q_verlet[frame, 0]], [q_verlet[frame, 1]])
        time_text.set_text(f'Time: {t_verlet[frame]:.1f}\nFrame: {frame+1}/{n_frames}')
        return line_verlet, point_verlet, time_text

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=n_frames, interval=interval, blit=True)
    plt.close(fig)
    return anim


def create_sv_vs_rk2_animation(results: Dict, kepler_system,
                                interval: int = 40, skip: int = 10,
                                max_frames: int = 300) -> animation.FuncAnimation:
    """
    Create a focused animation comparing Störmer-Verlet with RK2.
    Both are 2nd order methods, but only SV preserves the orbit.
    """
    q_verlet = results['verlet']['q'][::skip]
    q_rk2 = results['rk2']['q'][::skip]
    t_verlet = results['verlet']['t'][::skip]

    n_frames = min(len(q_verlet), len(q_rk2), max_frames)
    q_verlet = q_verlet[:n_frames]
    q_rk2 = q_rk2[:n_frames]
    t_verlet = t_verlet[:n_frames]

    # Compute exact orbit for reference
    E = results['verlet']['energy'][0]
    a = -kepler_system.mu / (2 * E)
    e = kepler_system.eccentricity(results['verlet']['q'][0], results['verlet']['p'][0])

    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw exact orbit
    theta_exact = np.linspace(0, 2*np.pi, 500)
    r_exact = a * (1 - e**2) / (1 + e * np.cos(theta_exact))
    x_exact = r_exact * np.cos(theta_exact)
    y_exact = r_exact * np.sin(theta_exact)
    ax.plot(x_exact, y_exact, 'k--', linewidth=1.5, alpha=0.5, label='Exact orbit')

    # Set up axes with buffer for RK2 drift
    all_q = np.vstack([q_verlet, q_rk2])
    margin = 0.5
    ax.set_xlim(np.min(all_q[:, 0]) - margin, np.max(all_q[:, 0]) + margin)
    ax.set_ylim(np.min(all_q[:, 1]) - margin, np.max(all_q[:, 1]) + margin)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    # Central body
    ax.plot(0, 0, 'yo', markersize=20, markeredgecolor='orange', markeredgewidth=2, zorder=10)

    # Initialize trails and points
    line_verlet, = ax.plot([], [], color=COLORS['verlet'], alpha=0.8, linewidth=2,
                           label='Verlet (symplectic)')
    line_rk2, = ax.plot([], [], color=COLORS['rk2'], alpha=0.8, linewidth=2,
                        label='RK2 (non-symplectic)')
    point_verlet, = ax.plot([], [], 'o', color=COLORS['verlet'], markersize=12,
                            markeredgecolor='black', markeredgewidth=2)
    point_rk2, = ax.plot([], [], 'o', color=COLORS['rk2'], markersize=12,
                         markeredgecolor='black', markeredgewidth=2)

    ax.legend(loc='upper right', fontsize=10)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_title('Verlet vs RK2 (Both 2nd Order!)\n'
                 'Verlet preserves orbit; RK2 drifts', fontsize=13)

    time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, fontsize=10,
                        verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    def init():
        line_verlet.set_data([], [])
        line_rk2.set_data([], [])
        point_verlet.set_data([], [])
        point_rk2.set_data([], [])
        time_text.set_text('')
        return line_verlet, line_rk2, point_verlet, point_rk2, time_text

    def animate(frame):
        line_verlet.set_data(q_verlet[:frame+1, 0], q_verlet[:frame+1, 1])
        line_rk2.set_data(q_rk2[:frame+1, 0], q_rk2[:frame+1, 1])
        point_verlet.set_data([q_verlet[frame, 0]], [q_verlet[frame, 1]])
        point_rk2.set_data([q_rk2[frame, 0]], [q_rk2[frame, 1]])
        time_text.set_text(f'Time: {t_verlet[frame]:.1f}\nFrame: {frame+1}/{n_frames}\n\n'
                          f'Both methods: O(h²)\n'
                          f'Only Verlet is symplectic!')
        return line_verlet, line_rk2, point_verlet, point_rk2, time_text

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=n_frames, interval=interval, blit=True)
    plt.close(fig)
    return anim


def create_molecular_animation(lj_results: Dict, lj_system, title: str = "Molecular Dynamics",
                                interval: int = 50, skip: int = 20,
                                max_frames: int = 200) -> animation.FuncAnimation:
    """
    Create an animation of Lennard-Jones molecular dynamics with dynamic energy plot.
    Shows particle motion and energy conservation simultaneously.
    """
    t = lj_results['t'][::skip]
    q = lj_results['q'][::skip]
    energy = lj_results['energy'][::skip]
    energy_error = lj_results['energy_error'][::skip]

    n_frames = min(len(t), max_frames)
    t = t[:n_frames]
    q = q[:n_frames]
    energy = energy[:n_frames]
    energy_error = energy_error[:n_frames]

    n_particles = lj_system.n_particles
    dim = lj_system.dim
    positions = q.reshape(-1, n_particles, dim)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: Particle positions
    ax_pos = axes[0]
    colors = plt.cm.tab10(np.linspace(0, 1, n_particles))

    # Set up axes for positions
    all_pos = positions.reshape(-1, dim)
    margin = 0.5
    x_min, x_max = np.min(all_pos[:, 0]) - margin, np.max(all_pos[:, 0]) + margin
    y_min, y_max = np.min(all_pos[:, 1]) - margin, np.max(all_pos[:, 1]) + margin
    ax_pos.set_xlim(x_min, x_max)
    ax_pos.set_ylim(y_min, y_max)
    ax_pos.set_aspect('equal')
    ax_pos.grid(True, alpha=0.3)
    ax_pos.set_xlabel('x position', fontsize=11)
    ax_pos.set_ylabel('y position', fontsize=11)
    ax_pos.set_title('Particle Positions', fontsize=12)

    # Initialize particle trails and points
    trails = []
    points = []
    for i in range(n_particles):
        trail, = ax_pos.plot([], [], color=colors[i], alpha=0.5, linewidth=1)
        point, = ax_pos.plot([], [], 'o', color=colors[i], markersize=15,
                             markeredgecolor='black', markeredgewidth=2,
                             label=f'Particle {i+1}')
        trails.append(trail)
        points.append(point)
    ax_pos.legend(loc='upper right', fontsize=9)

    # Right: Energy error over time
    ax_energy = axes[1]
    ax_energy.set_xlim(0, t[-1])
    max_err = np.max(np.abs(energy_error)) * 1.5
    ax_energy.set_ylim(-max_err, max_err)
    ax_energy.axhline(y=0, color='gray', linestyle='-', alpha=0.5)
    ax_energy.set_xlabel('Time', fontsize=11)
    ax_energy.set_ylabel('Energy Error (E - E₀)', fontsize=11)
    ax_energy.set_title('Energy Conservation (Verlet Method)', fontsize=12)
    ax_energy.grid(True, alpha=0.3)

    energy_line, = ax_energy.plot([], [], 'g-', linewidth=1.5, label='Energy error')
    ax_energy.legend(loc='upper right', fontsize=10)

    time_text = ax_energy.text(0.02, 0.98, '', transform=ax_energy.transAxes, fontsize=10,
                                verticalalignment='top',
                                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    fig.suptitle(f'{title} ({n_particles} particles)', fontsize=14, fontweight='bold')

    def init():
        for trail in trails:
            trail.set_data([], [])
        for point in points:
            point.set_data([], [])
        energy_line.set_data([], [])
        time_text.set_text('')
        return trails + points + [energy_line, time_text]

    def animate(frame):
        # Update particle trails and positions
        for i in range(n_particles):
            trails[i].set_data(positions[:frame+1, i, 0], positions[:frame+1, i, 1])
            points[i].set_data([positions[frame, i, 0]], [positions[frame, i, 1]])

        # Update energy plot
        energy_line.set_data(t[:frame+1], energy_error[:frame+1])

        current_err = energy_error[frame]
        time_text.set_text(f'Time: {t[frame]:.2f}\n'
                          f'Frame: {frame+1}/{n_frames}\n'
                          f'Energy error: {current_err:.2e}\n\n'
                          f'Symplectic integrator:\n'
                          f'Error bounded!')

        return trails + points + [energy_line, time_text]

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=n_frames, interval=interval, blit=True)
    plt.close(fig)
    return anim


def create_orbit_animation(results: Dict, kepler_system=None,
                           interval: int = 30, skip: int = 5,
                           embed_limit: int = 20000000) -> animation.FuncAnimation:
    """
    Create an animation comparing multiple integrators with the exact orbit.

    Shows Verlet, RK2, RK4, and Euler simultaneously, plus the exact elliptical orbit
    for reference. This clearly demonstrates which method tracks the true orbit.
    """
    # Get data for all methods
    q_verlet = results['verlet']['q'][::skip]
    q_rk2 = results['rk2']['q'][::skip] if 'rk2' in results else None
    q_rk4 = results['rk4']['q'][::skip]
    q_euler = results['euler']['q'][::skip]

    # Find global bounds
    all_q_list = [q_verlet, q_rk4, q_euler]
    if q_rk2 is not None:
        all_q_list.append(q_rk2)
    all_q = np.vstack(all_q_list)
    x_min, x_max = np.min(all_q[:, 0]) - 0.5, np.max(all_q[:, 0]) + 0.5
    y_min, y_max = np.min(all_q[:, 1]) - 0.5, np.max(all_q[:, 1]) + 0.5

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    # Central body
    ax.plot(0, 0, 'ko', markersize=20, zorder=10)

    # If we have the Kepler system, draw the exact orbit
    if kepler_system is not None:
        E = results['verlet']['energy'][0]
        L = kepler_system.angular_momentum(results['verlet']['q'][0], results['verlet']['p'][0])
        a = -kepler_system.mu / (2 * E)  # Semi-major axis
        e = kepler_system.eccentricity(results['verlet']['q'][0], results['verlet']['p'][0])

        if e < 1:  # Elliptical orbit
            theta_exact = np.linspace(0, 2*np.pi, 500)
            r_exact = a * (1 - e**2) / (1 + e * np.cos(theta_exact))
            x_exact = r_exact * np.cos(theta_exact)
            y_exact = r_exact * np.sin(theta_exact)
            ax.plot(x_exact, y_exact, 'k--', linewidth=2, alpha=0.5, label='Exact orbit')

    # Initialize trail lines and moving points
    line_verlet, = ax.plot([], [], color=COLORS['verlet'], alpha=0.6, linewidth=1,
                           label=LABELS['verlet'])
    line_rk2, = ax.plot([], [], color=COLORS['rk2'], alpha=0.6, linewidth=1,
                        label=LABELS['rk2']) if q_rk2 is not None else (None,)
    line_rk4, = ax.plot([], [], color=COLORS['rk4'], alpha=0.6, linewidth=1,
                        label=LABELS['rk4'])
    line_euler, = ax.plot([], [], color=COLORS['euler'], alpha=0.6, linewidth=1,
                          label=LABELS['euler'])

    point_verlet, = ax.plot([], [], 'o', color=COLORS['verlet'], markersize=12,
                            markeredgecolor='black')
    point_rk2, = ax.plot([], [], 'o', color=COLORS['rk2'], markersize=12,
                         markeredgecolor='black') if q_rk2 is not None else (None,)
    point_rk4, = ax.plot([], [], 'o', color=COLORS['rk4'], markersize=12,
                         markeredgecolor='black')
    point_euler, = ax.plot([], [], 'o', color=COLORS['euler'], markersize=12,
                           markeredgecolor='black')

    ax.legend(loc='upper right', fontsize=10)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    title_text = 'Kepler Orbit: Integrator Comparison\nVerlet (green) vs RK2 (orange) vs RK4 (blue) vs Euler (red)' if q_rk2 is not None else 'Kepler Orbit: Integrator Comparison\nVerlet (green) vs RK4 (blue) vs Euler (red)'
    ax.set_title(title_text, fontsize=13)

    # Frame counter text
    time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, fontsize=10,
                        verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    def init():
        line_verlet.set_data([], [])
        if line_rk2 is not None:
            line_rk2.set_data([], [])
        line_rk4.set_data([], [])
        line_euler.set_data([], [])
        point_verlet.set_data([], [])
        if point_rk2 is not None:
            point_rk2.set_data([], [])
        point_rk4.set_data([], [])
        point_euler.set_data([], [])
        time_text.set_text('')
        artists = [line_verlet, line_rk4, line_euler, point_verlet, point_rk4, point_euler, time_text]
        if line_rk2 is not None:
            artists.insert(1, line_rk2)
            artists.insert(5, point_rk2)
        return tuple(artists)

    n_frames_list = [len(q_verlet), len(q_rk4), len(q_euler)]
    if q_rk2 is not None:
        n_frames_list.append(len(q_rk2))
    n_frames = min(n_frames_list)

    def animate(frame):
        # Update trails
        line_verlet.set_data(q_verlet[:frame+1, 0], q_verlet[:frame+1, 1])
        if line_rk2 is not None and q_rk2 is not None:
            line_rk2.set_data(q_rk2[:frame+1, 0], q_rk2[:frame+1, 1])
        line_rk4.set_data(q_rk4[:frame+1, 0], q_rk4[:frame+1, 1])
        line_euler.set_data(q_euler[:frame+1, 0], q_euler[:frame+1, 1])

        # Update current positions
        point_verlet.set_data([q_verlet[frame, 0]], [q_verlet[frame, 1]])
        if point_rk2 is not None and q_rk2 is not None:
            point_rk2.set_data([q_rk2[frame, 0]], [q_rk2[frame, 1]])
        point_rk4.set_data([q_rk4[frame, 0]], [q_rk4[frame, 1]])
        point_euler.set_data([q_euler[frame, 0]], [q_euler[frame, 1]])

        # Update time text
        if q_rk2 is not None:
            time_text.set_text(f'Frame: {frame}/{n_frames}\n'
                               f'Verlet stays on orbit\n'
                               f'RK2 drifts (same order as Verlet!)\n'
                               f'Euler spirals outward\n'
                               f'RK4 drifts slowly')
        else:
            time_text.set_text(f'Frame: {frame}/{n_frames}\n'
                               f'Verlet stays on orbit\n'
                               f'Euler spirals outward\n'
                               f'RK4 drifts slowly')

        artists = [line_verlet, line_rk4, line_euler, point_verlet, point_rk4, point_euler, time_text]
        if line_rk2 is not None:
            artists.insert(1, line_rk2)
            artists.insert(5, point_rk2)
        return tuple(artists)

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=n_frames, interval=interval, blit=True)

    # Set embed limit for HTML export
    plt.rcParams['animation.embed_limit'] = embed_limit

    return anim
