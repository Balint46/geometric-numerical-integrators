"""
Generate all animations for documentation

This script generates all the animations from the notebook and saves them
as GIF files (and MP4 if ffmpeg is available) to the media/animations directory.

Usage:
    python src/generate_animations.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import sys
import os
sys.path.insert(0, '.')

from src.systems import KeplerSystem, LennardJonesSystem
from src.experiments import run_kepler_comparison, lennard_jones_simulation
from src.plotting import (
    create_exact_vs_sv_animation,
    create_sv_vs_rk2_animation,
    create_molecular_animation
)

# Set plot parameters for high-quality output
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 11

# Check if ffmpeg is available
def is_ffmpeg_available():
    """Check if ffmpeg writer is available for MP4 export"""
    try:
        writer = animation.writers['ffmpeg']
        writer.isAvailable()
        return True
    except (KeyError, RuntimeError):
        return False

FFMPEG_AVAILABLE = is_ffmpeg_available()

# Create output directory
OUTPUT_DIR = 'media/animations'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_animation(anim, basename, fps=25, dpi_mp4=150, dpi_gif=100):
    """Save animation as GIF (and MP4 if ffmpeg is available)"""
    # Always save GIF (Pillow writer)
    gif_path = f'{OUTPUT_DIR}/{basename}.gif'
    print(f"   Saving as GIF...")
    anim.save(gif_path, writer='pillow', fps=fps, dpi=dpi_gif)
    print(f"   Saved: {gif_path}")

    # Save MP4 only if ffmpeg is available
    if FFMPEG_AVAILABLE:
        mp4_path = f'{OUTPUT_DIR}/{basename}.mp4'
        print(f"   Saving as MP4...")
        anim.save(mp4_path, writer='ffmpeg', fps=fps, dpi=dpi_mp4)
        print(f"   Saved: {mp4_path}")
    else:
        print(f"   Skipping MP4 (ffmpeg not available)")

print("="*80)
print("GENERATING ANIMATIONS FOR DOCUMENTATION")
print("="*80)
if FFMPEG_AVAILABLE:
    print("\nffmpeg detected: Will generate both MP4 and GIF files")
else:
    print("\nffmpeg not available: Will generate GIF files only")
    print("(Install ffmpeg to enable MP4 export)")
print("\nNote: Animation generation may take several minutes...")

# Setup Kepler system
kepler = KeplerSystem(mu=1.0)
q0, p0 = kepler.get_elliptical_orbit_ic(e=0.6, a=1.0)

# Run Kepler comparison for animations
print("\nRunning Kepler orbit simulations...")
h_sv_vs_rk2 = 0.05
n_orbits_sv_vs_rk2 = 250
kepler_results = run_kepler_comparison(kepler, q0, p0, h_sv_vs_rk2, n_orbits_sv_vs_rk2)

# ============================================================================
# 1. EXACT ORBIT VS STÖRMER-VERLET ANIMATION
# ============================================================================
print("\n[1/4] Generating Exact Orbit vs Störmer-Verlet animation...")
print("   Creating animation object...")
anim1 = create_exact_vs_sv_animation(kepler_results, kepler,
                                     interval=40, skip=5, max_frames=500)
save_animation(anim1, '01_exact_vs_sv', fps=25, dpi_mp4=150, dpi_gif=100)

# ============================================================================
# 2. STÖRMER-VERLET VS RK2 ANIMATION
# ============================================================================
print("\n[2/4] Generating Störmer-Verlet vs RK2 animation...")
print("   Creating animation object...")
anim2 = create_sv_vs_rk2_animation(kepler_results, kepler,
                                   interval=40, skip=5, max_frames=500)
save_animation(anim2, '02_sv_vs_rk2', fps=25, dpi_mp4=150, dpi_gif=100)

# ============================================================================
# 3. TWO-PARTICLE LENNARD-JONES ANIMATION
# ============================================================================
print("\n[3/4] Generating two-particle Lennard-Jones animation...")
lj = LennardJonesSystem(n_particles=2, epsilon=1.0, sigma=1.0, dim=2)
q0_lj, p0_lj = lj.get_two_particle_ic(separation=1.5, velocity=0.3)

print("   Running simulation...")
h_lj = 0.005
n_steps_lj = 10000
lj_results = lennard_jones_simulation(lj, q0_lj, p0_lj, h_lj, n_steps_lj)

print("   Creating animation object...")
anim3 = create_molecular_animation(lj_results, lj,
                                   title="Lennard-Jones Two-Particle Dynamics",
                                   interval=50, skip=50, max_frames=200)
save_animation(anim3, '03_lj_2_particle', fps=20, dpi_mp4=150, dpi_gif=100)

# ============================================================================
# 4. THREE-PARTICLE LENNARD-JONES ANIMATION
# ============================================================================
print("\n[4/4] Generating three-particle Lennard-Jones animation...")
lj3 = LennardJonesSystem(n_particles=3, epsilon=1.0, sigma=1.0, dim=2)
q0_lj3, p0_lj3 = lj3.get_three_particle_ic(separation=1.5, velocity=0.2)

print("   Running simulation...")
lj3_results = lennard_jones_simulation(lj3, q0_lj3, p0_lj3, h=0.002, n_steps=20000)

print("   Creating animation object...")
anim4 = create_molecular_animation(lj3_results, lj3,
                                   title="Lennard-Jones Three-Particle Dynamics",
                                   interval=50, skip=100, max_frames=200)
save_animation(anim4, '04_lj_3_particle', fps=20, dpi_mp4=150, dpi_gif=100)

print("\n" + "="*80)
print("ALL ANIMATIONS GENERATED SUCCESSFULLY!")
print(f"Output directory: {OUTPUT_DIR}/")
if FFMPEG_AVAILABLE:
    print("Formats: MP4 (high quality) and GIF (for web)")
else:
    print("Formats: GIF (install ffmpeg for MP4 support)")
print("="*80)
