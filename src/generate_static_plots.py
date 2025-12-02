"""
Generate all static plots for documentation

This script generates all the static plots from the notebook with proper saving
to the media/plots directory. Each plot is saved as a high-resolution PNG.

Usage:
    python src/generate_static_plots.py
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.insert(0, '.')

from src.integrators import integrate_with_splitting_detail
from src.systems import KeplerSystem, LennardJonesSystem, HarmonicOscillator
from src.experiments import (
    run_kepler_comparison, long_term_energy_analysis,
    time_reversibility_test, symplectic_area_test,
    compute_local_error, lennard_jones_simulation
)
from src.plotting import (
    plot_long_term_energy, plot_reversibility_test,
    plot_splitting_diagram, plot_splitting_flow,
    plot_lennard_jones,
    plot_sv_vs_rk4_long_term, plot_energy_crossover,
    plot_sv_vs_euler, plot_sv_vs_rk2,
    plot_area_symplectic_methods, plot_area_nonsymplectic_methods
)

# Set plot parameters for high-quality output
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 11
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

# Create output directory
OUTPUT_DIR = 'media/plots'
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("="*80)
print("GENERATING STATIC PLOTS FOR DOCUMENTATION")
print("="*80)

# ============================================================================
# 1. KICK-DRIFT-KICK SPLITTING DIAGRAM
# ============================================================================
print("\n[1/14] Generating kick-drift-kick splitting diagram...")
fig = plot_splitting_diagram()
plt.savefig(f'{OUTPUT_DIR}/01_splitting_diagram.png')
plt.close()
print(f"   Saved: {OUTPUT_DIR}/01_splitting_diagram.png")

# ============================================================================
# 2. STÖRMER-VERLET VS EXPLICIT EULER
# ============================================================================
print("\n[2/14] Generating Störmer-Verlet vs Explicit Euler comparison...")
kepler = KeplerSystem(mu=1.0)
q0, p0 = kepler.get_elliptical_orbit_ic(e=0.6, a=1.0)

h_sv_vs_euler = 0.01
n_orbits_sv_vs_euler = 10
kepler_results_sv_vs_euler = run_kepler_comparison(kepler, q0, p0, h_sv_vs_euler, n_orbits_sv_vs_euler)

fig = plot_sv_vs_euler(kepler_results_sv_vs_euler)
plt.savefig(f'{OUTPUT_DIR}/02_sv_vs_euler.png')
plt.close()
print(f"   Saved: {OUTPUT_DIR}/02_sv_vs_euler.png")

# ============================================================================
# 3. STÖRMER-VERLET VS RK2 (CRITICAL COMPARISON!)
# ============================================================================
print("\n[3/14] Generating Störmer-Verlet vs RK2 comparison (both 2nd order)...")
h_sv_vs_rk2 = 0.05
n_orbits_sv_vs_rk2 = 250
kepler_results_sv_vs_rk2 = run_kepler_comparison(kepler, q0, p0, h_sv_vs_rk2, n_orbits_sv_vs_rk2)

fig = plot_sv_vs_rk2(kepler_results_sv_vs_rk2)
plt.savefig(f'{OUTPUT_DIR}/03_sv_vs_rk2.png')
plt.close()
print(f"   Saved: {OUTPUT_DIR}/03_sv_vs_rk2.png")

# ============================================================================
# 4. STÖRMER-VERLET VS RK4 LONG-TERM
# ============================================================================
print("\n[4/14] Generating Störmer-Verlet vs RK4 long-term comparison...")
h_sv_vs_rk4 = 0.05
n_orbits_sv_vs_rk4 = 1000
kepler_results_sv_vs_rk4 = run_kepler_comparison(kepler, q0, p0, h_sv_vs_rk4, n_orbits_sv_vs_rk4)

fig = plot_sv_vs_rk4_long_term(kepler_results_sv_vs_rk4)
plt.savefig(f'{OUTPUT_DIR}/04_sv_vs_rk4_long_term.png')
plt.close()
print(f"   Saved: {OUTPUT_DIR}/04_sv_vs_rk4_long_term.png")

# ============================================================================
# 5. ENERGY CROSSOVER: WHEN RK4 BECOMES WORSE
# ============================================================================
print("\n[5/14] Generating energy crossover plot...")
h_crossover = 0.08
n_orbits_crossover = 300
kepler_results_crossover = run_kepler_comparison(kepler, q0, p0, h_crossover, n_orbits_crossover)

fig = plot_energy_crossover(kepler_results_crossover)
plt.savefig(f'{OUTPUT_DIR}/05_energy_crossover.png')
plt.close()
print(f"   Saved: {OUTPUT_DIR}/05_energy_crossover.png")

# ============================================================================
# 6. LONG-TERM ENERGY BEHAVIOR - ALL METHODS
# ============================================================================
print("\n[6/14] Generating long-term energy behavior (all methods)...")
T_final = 200
h_energy = 0.05
energy_results = long_term_energy_analysis(kepler, q0, p0, h_energy, T_final)

fig = plot_long_term_energy(energy_results)
plt.savefig(f'{OUTPUT_DIR}/06_long_term_energy_all_methods.png')
plt.close()
print(f"   Saved: {OUTPUT_DIR}/06_long_term_energy_all_methods.png")

# ============================================================================
# 7. TIME-REVERSIBILITY TEST
# ============================================================================
print("\n[7/14] Generating time-reversibility test...")
step_sizes = np.logspace(-3, -1, 10)
n_steps = 100
reversibility_results = time_reversibility_test(kepler.gradV, q0, p0, step_sizes, n_steps)

fig = plot_reversibility_test(reversibility_results)
plt.savefig(f'{OUTPUT_DIR}/07_time_reversibility.png')
plt.close()
print(f"   Saved: {OUTPUT_DIR}/07_time_reversibility.png")

# ============================================================================
# 8. SYMPLECTIC AREA PRESERVATION - SYMPLECTIC METHODS
# ============================================================================
print("\n[8/14] Generating symplectic area preservation (symplectic methods)...")
ho = HarmonicOscillator(omega=1.0)
center_q = np.array([1.0])
center_p = np.array([0.0])
radius = 0.3

area_results_symplectic = symplectic_area_test(
    ho.gradV, center_q, center_p,
    radius=radius, n_points=100, h=0.2, n_steps=100
)

fig = plot_area_symplectic_methods(area_results_symplectic)
plt.savefig(f'{OUTPUT_DIR}/08_area_preservation_symplectic.png')
plt.close()
print(f"   Saved: {OUTPUT_DIR}/08_area_preservation_symplectic.png")

# ============================================================================
# 9. SYMPLECTIC AREA PRESERVATION - NON-SYMPLECTIC METHODS
# ============================================================================
print("\n[9/14] Generating symplectic area preservation (non-symplectic methods)...")
area_results_nonsymplectic = symplectic_area_test(
    ho.gradV, center_q, center_p,
    radius=radius, n_points=100, h=0.5, n_steps=1000
)

fig = plot_area_nonsymplectic_methods(area_results_nonsymplectic)
plt.savefig(f'{OUTPUT_DIR}/09_area_preservation_nonsymplectic.png')
plt.close()
print(f"   Saved: {OUTPUT_DIR}/09_area_preservation_nonsymplectic.png")

# ============================================================================
# 10. SPLITTING FLOW - SINGLE STEP
# ============================================================================
print("\n[10/14] Generating splitting flow visualization (single step)...")
h_split = 0.3
n_steps_split = 5
splitting_data = integrate_with_splitting_detail(q0, p0, h_split, n_steps_split, kepler.gradV)

fig = plot_splitting_flow(splitting_data, step_idx=0)
plt.savefig(f'{OUTPUT_DIR}/10_splitting_flow_single_step.png')
plt.close()
print(f"   Saved: {OUTPUT_DIR}/10_splitting_flow_single_step.png")

# ============================================================================
# 11. SPLITTING FLOW - MULTIPLE STEPS TRAJECTORY
# ============================================================================
print("\n[11/14] Generating splitting flow visualization (multiple steps)...")
fig, ax = plt.subplots(figsize=(10, 10))

# Plot central body (Sun)
ax.scatter([0], [0], s=400, c='yellow', marker='*', edgecolors='orange',
           linewidth=2, zorder=10, label='Sun')

# Plot the position trajectory
q_traj = splitting_data['q']
ax.plot(q_traj[:, 0], q_traj[:, 1], 'b-', linewidth=2, alpha=0.6, label='Trajectory')

# Mark each complete step with different colors
colors = plt.cm.viridis(np.linspace(0, 1, n_steps_split + 1))
for i in range(n_steps_split + 1):
    ax.scatter(q_traj[i, 0], q_traj[i, 1], s=150, c=[colors[i]],
               edgecolors='black', linewidth=2, zorder=5)
    ax.annotate(f'Step {i}', (q_traj[i, 0], q_traj[i, 1]),
                xytext=(10, 10), textcoords='offset points', fontsize=9)

# Draw drift arrows for each step
for i in range(n_steps_split):
    q_start = splitting_data['q'][i]
    q_drift = splitting_data['q_after_drift'][i]

    ax.annotate('', xy=(q_drift[0], q_drift[1]), xytext=(q_start[0], q_start[1]),
               arrowprops=dict(arrowstyle='->', color='orange', lw=2, alpha=0.7))

ax.set_xlabel('x position', fontsize=12)
ax.set_ylabel('y position', fontsize=12)
ax.set_title(f'Verlet Integration: {n_steps_split} Steps on Kepler Orbit\n'
             f'(Step size h = {h_split}, Orange arrows show DRIFT phase)',
             fontsize=13)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.legend(loc='upper right', fontsize=10)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/11_splitting_flow_trajectory.png')
plt.close()
print(f"   Saved: {OUTPUT_DIR}/11_splitting_flow_trajectory.png")

# ============================================================================
# 12. LENNARD-JONES TWO-PARTICLE SIMULATION
# ============================================================================
print("\n[12/14] Generating Lennard-Jones two-particle simulation...")
lj = LennardJonesSystem(n_particles=2, epsilon=1.0, sigma=1.0, dim=2)
q0_lj, p0_lj = lj.get_two_particle_ic(separation=1.5, velocity=0.3)

h_lj = 0.005
n_steps_lj = 10000
lj_results = lennard_jones_simulation(lj, q0_lj, p0_lj, h_lj, n_steps_lj)

fig = plot_lennard_jones(lj_results, lj)
plt.savefig(f'{OUTPUT_DIR}/12_lennard_jones_2_particle.png')
plt.close()
print(f"   Saved: {OUTPUT_DIR}/12_lennard_jones_2_particle.png")

# ============================================================================
# 13. LENNARD-JONES THREE-PARTICLE SIMULATION
# ============================================================================
print("\n[13/14] Generating Lennard-Jones three-particle simulation...")
lj3 = LennardJonesSystem(n_particles=3, epsilon=1.0, sigma=1.0, dim=2)
q0_lj3, p0_lj3 = lj3.get_three_particle_ic(separation=1.5, velocity=0.2)

lj3_results = lennard_jones_simulation(lj3, q0_lj3, p0_lj3, h=0.002, n_steps=20000)

fig = plot_lennard_jones(lj3_results, lj3)
plt.savefig(f'{OUTPUT_DIR}/13_lennard_jones_3_particle.png')
plt.close()
print(f"   Saved: {OUTPUT_DIR}/13_lennard_jones_3_particle.png")

# ============================================================================
# 14. LOCAL ERROR CONVERGENCE
# ============================================================================
print("\n[14/14] Generating local error convergence plot...")
ho = HarmonicOscillator(omega=1.0)
q0_ho = np.array([1.0, 0.0])
p0_ho = np.array([0.0, 1.0])

h_values = [0.1, 0.05, 0.025, 0.0125]
h_array = np.array(h_values)

euler_errors = [compute_local_error(ho.gradV, q0_ho, p0_ho, h, ho.exact_solution)['euler']['total_error']
                for h in h_array]
verlet_errors = [compute_local_error(ho.gradV, q0_ho, p0_ho, h, ho.exact_solution)['verlet']['total_error']
                 for h in h_array]
rk4_errors = [compute_local_error(ho.gradV, q0_ho, p0_ho, h, ho.exact_solution)['rk4']['total_error']
              for h in h_array]

fig, ax = plt.subplots(figsize=(10, 7))

ax.loglog(h_array, euler_errors, 'ro-', label='Euler (measured)', linewidth=2, markersize=10)
ax.loglog(h_array, verlet_errors, 'go-', label='Verlet (measured)', linewidth=2, markersize=10)
ax.loglog(h_array, rk4_errors, 'bo-', label='RK4 (measured)', linewidth=2, markersize=10)

# Reference lines for expected orders
ax.loglog(h_array, h_array * euler_errors[0]/h_array[0], 'r--', alpha=0.5, linewidth=1.5, label='O(h) reference')
ax.loglog(h_array, h_array**2 * verlet_errors[0]/h_array[0]**2, 'g--', alpha=0.5, linewidth=1.5, label='O(h²) reference')
ax.loglog(h_array, h_array**4 * rk4_errors[0]/h_array[0]**4, 'b--', alpha=0.5, linewidth=1.5, label='O(h⁴) reference')

ax.set_xlabel('Step size h', fontsize=12)
ax.set_ylabel('Local Truncation Error', fontsize=12)
ax.set_title('Local Error vs Step Size\n(Slopes match expected convergence orders)', fontsize=14)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, which='both')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/14_local_error_convergence.png')
plt.close()
print(f"   Saved: {OUTPUT_DIR}/14_local_error_convergence.png")

print("\n" + "="*80)
print("ALL STATIC PLOTS GENERATED SUCCESSFULLY!")
print(f"Output directory: {OUTPUT_DIR}/")
print("="*80)
