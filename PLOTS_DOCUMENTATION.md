# Visualization Documentation

This document provides detailed explanations for all plots and animations generated for the Geometric Numerical Integrators project. Each visualization demonstrates key properties of symplectic integrators, particularly the Störmer-Verlet method.

---

## Table of Contents

### Static Plots
1. [Kick-Drift-Kick Splitting Diagram](#1-kick-drift-kick-splitting-diagram)
2. [Störmer-Verlet vs Explicit Euler](#2-störmer-verlet-vs-explicit-euler)
3. [Störmer-Verlet vs RK2 (Critical Comparison)](#3-störmer-verlet-vs-rk2-critical-comparison)
4. [Störmer-Verlet vs RK4 Long-Term](#4-störmer-verlet-vs-rk4-long-term)
5. [Energy Crossover: When RK4 Becomes Worse](#5-energy-crossover-when-rk4-becomes-worse)
6. [Long-Term Energy Behavior - All Methods](#6-long-term-energy-behavior-all-methods)
7. [Time-Reversibility Test](#7-time-reversibility-test)
8. [Symplectic Area Preservation - Symplectic Methods](#8-symplectic-area-preservation-symplectic-methods)
9. [Symplectic Area Preservation - Non-Symplectic Methods](#9-symplectic-area-preservation-non-symplectic-methods)
10. [Splitting Flow - Single Step](#10-splitting-flow-single-step)
11. [Splitting Flow - Multiple Steps Trajectory](#11-splitting-flow-multiple-steps-trajectory)
12. [Lennard-Jones Two-Particle Simulation](#12-lennard-jones-two-particle-simulation)
13. [Lennard-Jones Three-Particle Simulation](#13-lennard-jones-three-particle-simulation)
14. [Local Error Convergence](#14-local-error-convergence)

### Animations
1. [Exact Orbit vs Störmer-Verlet](#animation-1-exact-orbit-vs-störmer-verlet)
2. [Störmer-Verlet vs RK2](#animation-2-störmer-verlet-vs-rk2)
3. [Two-Particle Lennard-Jones Dynamics](#animation-3-two-particle-lennard-jones-dynamics)
4. [Three-Particle Lennard-Jones Dynamics](#animation-4-three-particle-lennard-jones-dynamics)

---

# Static Plots

## 1. Kick-Drift-Kick Splitting Diagram

**File:** `media/plots/01_splitting_diagram.png`

### What You See
A phase space diagram showing a single Verlet step in (q, p) coordinates. The diagram shows three sequential transformations represented by colored arrows connecting four points.

### What's Happening
The Verlet method decomposes each integration step into three simple, exactly solvable sub-steps:

1. **KICK 1 (Red arrow):** Half-step momentum update
   - The potential force acts on the particle
   - Momentum changes: p → p - (h/2)∇V(q)
   - Position remains fixed (vertical arrow)

2. **DRIFT (Orange arrow):** Full-step position update
   - Free motion with the updated momentum
   - Position changes: q → q + h·p
   - Momentum remains fixed (horizontal arrow)

3. **KICK 2 (Purple arrow):** Half-step momentum update
   - Force acts again at the new position
   - Momentum changes: p → p - (h/2)∇V(q_new)
   - Position remains fixed (vertical arrow)

### Expected Result
The arrows should form a path from the initial state (q₀, p₀) to the final state (q₁, p₁). The symmetric structure (kick-drift-kick) is what makes the method:
- **Time-reversible:** Running backward exactly reverses the steps
- **Symplectic:** Each sub-step preserves the symplectic 2-form
- **Second-order accurate:** The symmetric composition gives O(h³) local error

### Key Insight
By splitting the Hamiltonian into kinetic and potential parts, we can solve each part exactly and compose them to approximate the full dynamics. This is the foundation of geometric integration.

---

## 2. Störmer-Verlet vs Explicit Euler

**File:** `media/plots/02_sv_vs_euler.png`

### What You See
A 2×2 grid of subplots comparing Störmer-Verlet (SV) and Explicit Euler methods over 10 orbital periods:
- **Top row:** Orbital trajectories in (x, y) space
- **Bottom row:** Energy error over time

### What's Happening
Both methods integrate the same Kepler problem (elliptical orbit with eccentricity e=0.6) starting from identical initial conditions with step size h=0.01.

**Störmer-Verlet (left column):**
- Maintains the closed elliptical orbit
- Energy error oscillates but remains bounded (±0.002 relative error)
- The orbit stays stable indefinitely

**Explicit Euler (right column):**
- Orbit spirals outward catastrophically
- Energy grows exponentially (reaches 50% error in just 10 orbits!)
- The method is completely unsuitable for Hamiltonian systems

### Expected Result
This dramatic difference demonstrates why symplectic integrators are essential for long-term Hamiltonian dynamics:
- **Euler** is non-symplectic → energy drifts unboundedly → orbit degrades
- **Verlet** is symplectic → energy stays bounded → orbit preserved

### Key Insight
Even though Euler is simpler and cheaper per step, it fails spectacularly for conservative systems. The geometric structure preservation of Verlet is not a luxury—it's a necessity.

---

## 3. Störmer-Verlet vs RK2 (Critical Comparison)

**File:** `media/plots/03_sv_vs_rk2.png`

### What You See
A 2×2 grid comparing two second-order methods over 250 orbital periods:
- **Top row:** Orbital trajectories
- **Bottom row:** Energy error evolution

### What's Happening
This is the **most important comparison** in the entire analysis. Both methods have the same theoretical order of accuracy (O(h²)), but produce radically different results:

**Störmer-Verlet (left column):**
- Maintains perfect elliptical orbit for all 250 periods
- Energy error oscillates with constant amplitude (~0.01 relative error)
- No secular drift—bounded forever

**RK2 (right column):**
- Orbit starts drifting almost immediately
- After 250 orbits, the trajectory has visibly precessed
- Energy error grows linearly without bound
- Despite being the same order as Verlet!

### Expected Result
The RK2 trajectory should show clear drift while Verlet remains stable. The energy plots should show:
- **Verlet:** Periodic oscillation around zero (no trend)
- **RK2:** Linear growth over time (secular drift)

### Key Insight
**This proves that order of accuracy is NOT the determining factor for long-term energy behavior.** The crucial difference is:
- **Verlet is symplectic** → preserves phase space volume → bounded energy error
- **RK2 is not symplectic** → violates Liouville's theorem → linear energy drift

Symplecticity matters more than accuracy order for Hamiltonian systems!

---

## 4. Störmer-Verlet vs RK4 Long-Term

**File:** `media/plots/04_sv_vs_rk4_long_term.png`

### What You See
A comparison over 1000 orbital periods showing:
- **Top row:** Orbital trajectories
- **Bottom row:** Energy error (linear and log scales)

### What's Happening
RK4 is a 4th-order method (more accurate per step than Verlet's 2nd order), but over long integration times:

**Short-term (first ~100 orbits):**
- RK4 has smaller error initially due to higher order
- Energy error appears negligible

**Long-term (100-1000 orbits):**
- RK4 energy drifts linearly without bound
- Verlet energy remains in a bounded oscillation
- RK4's orbit slowly precesses and drifts

### Expected Result
The energy plot should show two distinct regimes:
1. **Early times:** RK4 error < Verlet error (RK4 wins on accuracy)
2. **Later times:** RK4 error grows, Verlet error bounded (Verlet wins on stability)

The log-scale plot should show RK4's error growing as a straight line (linear drift), while Verlet's error oscillates around a constant value.

### Key Insight
Higher-order methods are not automatically better for long-term integration!
- **RK4:** Better local accuracy, but non-symplectic → fails for long times
- **Verlet:** Lower local accuracy, but symplectic → stable forever

For molecular dynamics or solar system integration over billions of steps, Verlet's geometric fidelity trumps RK4's algebraic accuracy.

---

## 5. Energy Crossover: When RK4 Becomes Worse

**File:** `media/plots/05_energy_crossover.png`

### What You See
Two subplots focusing on the crossover phenomenon:
- **Top:** Absolute energy error for both methods
- **Bottom:** Ratio of RK4 error to Verlet error

### What's Happening
This plot zooms in on the critical transition point where RK4's cumulative error overtakes Verlet's bounded error:

**Absolute error plot:**
- RK4 starts lower (4th order beats 2nd order initially)
- Both errors oscillate due to orbital periodicity
- Crossover occurs around orbit 50-100
- After crossover, RK4 error keeps growing while Verlet stays bounded

**Error ratio plot:**
- Ratio starts below 1 (RK4 better)
- Crosses 1 at the crossover point
- Ratio grows without bound (RK4 becomes arbitrarily worse)

### Expected Result
The crossover point depends on:
- Step size (larger h → earlier crossover)
- Integration time (longer T → guaranteed crossover eventually)
- System properties (stiffer systems → earlier crossover)

For the parameters used (h=0.08, Kepler orbit), crossover occurs around 50-100 orbits.

### Key Insight
This crossover illustrates the fundamental trade-off:
- **Short integrations:** Use high-order methods (RK4) for accuracy
- **Long integrations:** Use symplectic methods (Verlet) for stability
- **Very long integrations:** Symplectic methods are the only option

In practice, molecular dynamics simulations run for millions of steps, so the crossover always occurs and symplectic integrators are mandatory.

---

## 6. Long-Term Energy Behavior - All Methods

**File:** `media/plots/06_long_term_energy_all_methods.png`

### What You See
A comprehensive comparison of five integrators over 200 time units:
- **Linear scale (left):** Shows absolute magnitude of errors
- **Log scale (right):** Shows error growth rates

Methods compared:
- Störmer-Verlet (symplectic, 2nd order)
- Symplectic Euler (symplectic, 1st order)
- RK2 (non-symplectic, 2nd order)
- RK4 (non-symplectic, 4th order)
- Explicit Euler (non-symplectic, 1st order)

### What's Happening
This plot reveals the fundamental dichotomy in numerical integrators for Hamiltonian systems:

**Symplectic methods (Verlet, Symplectic Euler):**
- Energy error oscillates but remains bounded
- Amplitude of oscillation is O(h^p) where p is the order
- No secular drift—energy error doesn't grow with time
- The system never "heats up" or "cools down" artificially

**Non-symplectic methods (Euler, RK2, RK4):**
- Energy error drifts linearly (RK2, RK4) or exponentially (Euler)
- Initial accuracy doesn't prevent long-term drift
- System experiences artificial energy injection or extraction
- Physically unrealistic for conservative systems

### Expected Result
**Linear plot:**
- Euler explodes dramatically (visible exponential growth)
- Verlet and Symplectic Euler show small oscillations
- RK2 and RK4 show gradual drift

**Log plot:**
- Symplectic methods: horizontal bands (bounded error)
- RK2/RK4: upward slopes (linear drift)
- Euler: steep upward slope (exponential growth)

### Key Insight
The symplectic property creates a **qualitative difference**, not just a quantitative one:
- Symplectic → bounded error for all time (structural preservation)
- Non-symplectic → unbounded error (structural violation)

This is independent of the order of accuracy! Even 1st-order symplectic Euler behaves better than 4th-order RK4 for long times.

---

## 7. Time-Reversibility Test

**File:** `media/plots/07_time_reversibility.png`

### What You See
A log-log plot showing reversibility error vs step size for five methods. The y-axis shows the error in returning to the initial state after integrating forward, reversing momentum, and integrating forward again.

### What's Happening
This test checks a fundamental property of Hamiltonian dynamics: **time-reversal symmetry**. The Hamiltonian equations are invariant under (t → -t, p → -p).

**Test procedure:**
1. Start at (q₀, p₀)
2. Integrate forward N steps → (qₙ, pₙ)
3. Reverse momentum: (qₙ, -pₙ)
4. Integrate forward N steps → (q₂ₙ, p₂ₙ)
5. Measure ||q₂ₙ - q₀||

**Results by method:**
- **Verlet:** Error ≈ 10⁻¹⁴ (machine precision!) — truly reversible
- **Symplectic Euler:** Error ∝ h (symplectic but not reversible)
- **Euler, RK2, RK4:** Errors ∝ h, h², h⁴ respectively (not reversible)

### Expected Result
The plot should show:
- **Verlet:** Flat line near machine epsilon (~10⁻¹⁴) for all step sizes
- **Other methods:** Lines with slopes matching their order of accuracy

### Key Insight
Time-reversibility is an additional geometric property beyond symplecticity:
- **Symplectic + symmetric composition** → time-reversible (Verlet)
- **Symplectic but asymmetric** → not time-reversible (Symplectic Euler)
- **Non-symplectic** → definitely not reversible (Euler, RK)

Verlet's symmetric kick-drift-kick structure gives it both properties. This makes it ideal for:
- Hybrid Monte Carlo sampling
- Backward error analysis
- Detecting numerical instabilities (non-reversibility indicates problems)

---

## 8. Symplectic Area Preservation - Symplectic Methods

**File:** `media/plots/08_area_preservation_symplectic.png`

### What You See
A 1×2 grid showing how a circle of initial conditions evolves under symplectic integrators:
- **Left:** Verlet method
- **Right:** Symplectic Euler method

Each plot shows:
- Green circle: initial conditions
- Blue dots: evolved positions
- Title shows area ratio (final area / initial area)

### What's Happening
This tests **Liouville's theorem**: symplectic integrators preserve phase space volume. We use a 2D harmonic oscillator for clean visualization.

**Setup:**
- Initial: 100 points on a circle in phase space
- Integration: 100 steps with h=0.2
- Measurement: Area of the evolved region

**Results:**
- **Verlet:** Area ratio ≈ 1.000 (within 0.1%)
- **Symplectic Euler:** Area ratio ≈ 1.000 (within 0.1%)

The circle rotates and shears, but its area remains constant!

### Expected Result
Both symplectic methods should show:
- Area ratio very close to 1.0 (typically 0.99-1.01)
- The shape deforms but doesn't expand or contract overall
- Small deviations are due to:
  - Discrete approximation of the area
  - Finite step size effects
  - Numerical round-off

### Key Insight
Symplectic integrators preserve the symplectic 2-form ω = dq ∧ dp, which implies area preservation in 2D and volume preservation in higher dimensions. This is a direct consequence of the **symplectic property**:

φ*ω = ω

where φ is the numerical flow. This means:
- No artificial heating/cooling in molecular dynamics
- Correct statistical distributions in Monte Carlo
- Conservation of invariants in celestial mechanics

---

## 9. Symplectic Area Preservation - Non-Symplectic Methods

**File:** `media/plots/09_area_preservation_nonsymplectic.png`

### What You See
A 1×3 grid showing area distortion by non-symplectic methods:
- **Left:** Explicit Euler
- **Middle:** RK2
- **Right:** RK4

Same setup as Plot 8, but with larger step size (h=0.5) and more steps (1000) to make distortion visible.

### What's Happening
Non-symplectic methods violate Liouville's theorem, causing artificial expansion or contraction of phase space:

**Explicit Euler:**
- Area ratio ≫ 1 (dramatic expansion)
- The circle becomes a large spiral
- Energy is artificially injected into the system

**RK2:**
- Area ratio ≠ 1 (significant distortion)
- Despite being 2nd order like Verlet, it doesn't preserve area!
- The circle deforms irregularly

**RK4:**
- Area ratio ≠ 1 (distortion visible after many steps)
- Despite high accuracy per step, cumulative error distorts the area
- More steps → more distortion

### Expected Result
All three methods should show area ratios significantly different from 1.0:
- **Euler:** Typically 2-10× expansion (explosive growth)
- **RK2:** ~0.8-1.5× distortion (moderate violation)
- **RK4:** ~0.95-1.05× distortion (small but nonzero)

The exact values depend on the parameters (h, n_steps, system).

### Key Insight
This provides visual proof that **non-symplectic methods violate fundamental physics**:

In statistical mechanics, Liouville's theorem ensures that phase space volume is preserved along trajectories. If a numerical integrator doesn't preserve this volume:
- Probability densities become distorted
- Ensemble averages drift from correct values
- Long-time statistics are wrong

Even high-order methods like RK4 violate this! The violation is smaller, but it accumulates over billions of steps.

**Why separate plots for symplectic vs non-symplectic?**
We use different parameters because:
- Symplectic methods preserve area even with moderate h and n_steps
- Non-symplectic methods need large h and many steps to show clear distortion
- RK4 distortion is subtle, so we need extreme parameters to visualize it
- Using the same parameters would make either Euler explode or RK4 distortion invisible

---

## 10. Splitting Flow - Single Step

**File:** `media/plots/10_splitting_flow_single_step.png`

### What You See
A detailed phase space diagram showing one Verlet step on the Kepler orbit, with:
- Black dot: initial state
- Three colored arrows: kick-drift-kick transformations
- Intermediate states marked
- Background: potential energy contours

### What's Happening
This visualizes how the Störmer-Verlet splitting works in practice on a real physical system (Kepler problem with eccentricity 0.6).

**Kick 1 (red arrow):**
- Vertical motion in (q, p) space
- Force −∇V pulls the momentum toward the Sun
- Position doesn't change

**Drift (orange arrow):**
- Horizontal motion in (q, p) space
- Particle moves with constant momentum
- Free flight with no forces

**Kick 2 (purple arrow):**
- Another vertical motion
- Force acts at the new position
- Completes the step

### Expected Result
The three arrows should:
- Follow the structure: vertical → horizontal → vertical
- Each arrow represents an exactly solvable sub-step
- Composition approximates the true Hamiltonian flow
- With step size h=0.3, the approximation is visible but reasonable

### Key Insight
The power of splitting methods lies in decomposing a hard problem (full Hamiltonian) into easy sub-problems (kinetic and potential separately):

H = T(p) + V(q)

Each part has a simple exact solution:
- T-flow: q′ = q + hp, p′ = p (free motion)
- V-flow: q′ = q, p′ = p − h∇V(q) (force impulse)

Composing them symmetrically gives a 2nd-order approximation to the full flow.

---

## 11. Splitting Flow - Multiple Steps Trajectory

**File:** `media/plots/11_splitting_flow_trajectory.png`

### What You See
A spatial plot showing 5 complete Verlet steps along a Kepler orbit:
- Yellow star: Sun at origin
- Blue curve: trajectory connecting step endpoints
- Colored dots: endpoints of each step (colored by step number)
- Orange arrows: drift phases within each step

### What's Happening
This extends Plot 10 to show how multiple Verlet steps compose to approximate the orbital motion:

**Each step:**
- Starts at a colored dot
- Goes through kick-drift-kick internally
- Orange arrow shows the drift phase (most visible part)
- Ends at the next colored dot

**Trajectory:**
- The blue curve connects all endpoints
- Forms an approximate ellipse
- With h=0.3, 5 steps cover a significant arc
- Each step is relatively large (visible deviations)

### Expected Result
- Trajectory should roughly follow an elliptical path
- Orange drift arrows should be tangent-ish to the curve
- Steps should be non-uniform (larger near aphelion, smaller near perihelion)
- Sun should be at one focus of the approximate ellipse

### Key Insight
This shows the **multi-step composition** of the Verlet method:

One orbit ≈ [kick-drift-kick] → [kick-drift-kick] → ... → [kick-drift-kick]

Each bracket is one step. The composition of many symplectic maps is itself symplectic, so:
- Long-term energy conservation comes from each step preserving the symplectic form
- The kicks (force impulses) curve the trajectory
- The drifts (free motion) move the particle between force applications

With smaller h, the discrete steps would be less visible and the trajectory would appear smoother.

---

## 12. Lennard-Jones Two-Particle Simulation

**File:** `media/plots/12_lennard_jones_2_particle.png`

### What You See
A 2×2 grid showing two-particle molecular dynamics:
- **Top left:** Particle trajectories in space
- **Top right:** Separation distance over time
- **Bottom left:** Energy components (kinetic, potential, total)
- **Bottom right:** Relative energy error

### What's Happening
Two particles interact via the Lennard-Jones potential:

V(r) = 4ε[(σ/r)¹² - (σ/r)⁶]

**Initial conditions:**
- Particles separated by r = 1.5σ (beyond equilibrium at 2^(1/6)σ ≈ 1.122σ)
- Moving perpendicular to separation
- Initially attractive regime

**Dynamics:**
- Particles orbit each other
- Separation oscillates around equilibrium
- Energy converts between kinetic and potential
- Total energy conserved (within numerical error)

### Expected Result
**Trajectory plot:**
- Both particles orbit their center of mass
- Curved paths due to attractive/repulsive forces
- Motion should be bounded (bound state)

**Separation plot:**
- Oscillates periodically
- Minimum separation > σ (repulsive core prevents overlap)
- Average separation ≈ equilibrium distance

**Energy plot:**
- Kinetic and potential anti-correlated (conservation)
- Total energy (black) nearly constant
- Periodic oscillation as particles orbit

**Error plot:**
- Bounded oscillation (symplectic integrator!)
- Amplitude ~10⁻³ to 10⁻⁴ relative error
- No drift over 10000 steps

### Key Insight
This demonstrates Störmer-Verlet on a **realistic molecular dynamics system**:

Lennard-Jones potentials are used to model:
- Noble gases (Ar, Ne, Xe)
- Van der Waals interactions
- Molecular mechanics force fields

The simulation shows:
- Correct bound state formation
- Energy conservation (no artificial heating)
- Stable long-term dynamics

For molecular dynamics with millions of atoms over nanoseconds (10⁹ time steps), symplectic integrators are essential to prevent energy drift.

---

## 13. Lennard-Jones Three-Particle Simulation

**File:** `media/plots/13_lennard_jones_3_particle.png`

### What You See
Same 2×2 layout as Plot 12, but with three particles showing more complex dynamics.

### What's Happening
Three particles create a richer dynamical system:

**Interactions:**
- Three pairwise Lennard-Jones potentials
- Each particle feels forces from two others
- Many-body effects emerge

**Dynamics:**
- More complex trajectories than two-body
- Possible formation of transient structures
- Chaotic behavior possible depending on initial conditions
- Collective motion of the center of mass

### Expected Result
**Trajectory plot:**
- Three distinct particle paths
- More intricate patterns than two-particle case
- May form triangular configurations

**Separation plot (not shown for 3-particle):**
- Would show 3 separation distances
- Each pair oscillates differently
- More complex pattern

**Energy plot:**
- More conversion between kinetic and potential
- Total energy still conserved
- More complex oscillations

**Error plot:**
- Still bounded (symplectic!)
- Maybe slightly larger amplitude than 2-particle
- Still no secular drift

### Key Insight
This shows that Störmer-Verlet **scales to many-body systems**:

The method is:
- **O(N²)** for all-pairs interactions (3 particles → 3 pairs)
- **O(N)** for force computation on each particle
- Still symplectic despite many-body complexity
- Energy conserving for arbitrarily many particles

In production molecular dynamics:
- Systems have 10⁴ to 10⁹ atoms
- Simulations run for 10⁶ to 10⁹ time steps
- Verlet-family integrators are the only viable option
- Cutoff radii and neighbor lists reduce cost to O(N)

---

## 14. Local Error Convergence

**File:** `media/plots/14_local_error_convergence.png`

### What You See
A log-log plot showing local truncation error vs step size for three methods:
- Red circles: Euler (measured)
- Green circles: Verlet (measured)
- Blue circles: RK4 (measured)
- Dashed lines: Theoretical slopes O(h), O(h²), O(h⁴)

### What's Happening
This verifies the **order of accuracy** of each method by comparing against the exact solution of the harmonic oscillator:

**Harmonic oscillator:**
- Has analytical solution: q(t) = cos(t), p(t) = -sin(t) (for ω=1)
- Allows exact error computation
- Simplest nontrivial Hamiltonian system

**Test procedure:**
- Take one step with step size h
- Compare to exact solution
- Measure error
- Repeat for h = 0.1, 0.05, 0.025, 0.0125

**Results:**
- **Euler:** Error ∝ h¹ (first-order convergence)
- **Verlet:** Error ∝ h² (second-order convergence)
- **RK4:** Error ∝ h⁴ (fourth-order convergence)

### Expected Result
On the log-log plot:
- Each method should form a straight line
- Slope = order of convergence
- Measured data should lie on the reference lines

Specifically:
- Euler slope = -1 (line should be parallel to h)
- Verlet slope = -2 (line should be parallel to h²)
- RK4 slope = -4 (line should be parallel to h⁴)

### Key Insight
This confirms the **algebraic accuracy** of each method:

**But remember:** Higher order ≠ better for long-term integration!

- **Local error** (this plot): How accurate is one step?
  - RK4 > Verlet > Euler

- **Global error** (energy plots): How accurate after many steps?
  - Depends on symplecticity!
  - For conservative systems: Verlet >> RK4 at long times

The convergence plot shows why RK4 starts with lower error (Plot 5), but the energy plots show why Verlet wins eventually (bounded vs. unbounded error).

**Trade-off:**
- If you can afford h small enough that RK4 stays accurate, use it
- If you need long integration times, use Verlet regardless of h
- For molecular dynamics: always Verlet (billions of steps required)

---

# Animations

## Animation 1: Exact Orbit vs Störmer-Verlet

**Files:** `media/animations/01_exact_vs_sv.mp4`, `01_exact_vs_sv.gif`

### What You See
A side-by-side animation showing:
- **Left panel:** Exact Kepler orbit (analytical solution)
- **Right panel:** Störmer-Verlet numerical solution
- Both panels show the Sun (yellow star) and particle trajectory
- Time counter and energy error displayed

### What's Happening
The animation runs 500 frames showing ~250 orbital periods. It demonstrates:

**Exact solution (left):**
- Perfect ellipse for all time
- Calculated from the analytical solution to Kepler's equations
- Represents the "ground truth"

**Verlet solution (right):**
- Numerical integration with finite step size h=0.05
- Should closely track the exact orbit
- Small deviations accumulate but don't grow unboundedly

**Energy error:**
- Oscillates as the particle moves between perihelion and aphelion
- Remains bounded throughout
- Amplitude doesn't grow with time

### Expected Result
- Both trajectories should appear nearly identical
- Verlet orbit may show slight phase shift or precession
- No visible spiral outward or inward
- Energy error stays within ~1% throughout

### Key Insight
This shows **long-term stability** of symplectic integration:

Even after 250+ orbits (thousands of time steps), the Verlet trajectory:
- Stays close to the exact orbit
- Doesn't accumulate energy error
- Preserves the orbital structure

Compare this to what would happen with Euler or RK2 (see Animation 2)!

---

## Animation 2: Störmer-Verlet vs RK2

**Files:** `media/animations/02_sv_vs_rk2.mp4`, `02_sv_vs_rk2.gif`

### What You See
A side-by-side animation showing:
- **Left panel:** Störmer-Verlet
- **Right panel:** RK2 (Runge-Kutta 2nd order)
- Both integrate the same initial conditions
- Energy error displayed for each

### What's Happening
This is the **most important animation** because it compares two methods of the same order:

**First ~50 orbits:**
- Both methods track each other reasonably well
- Orbits appear similar
- Energy errors both oscillate

**50-100 orbits:**
- RK2 starts to drift noticeably
- Orbit precesses (rotates) slowly
- Energy error begins growing

**100-250 orbits:**
- RK2 drift becomes severe
- Orbital shape distorts
- Energy error grows linearly
- Verlet remains perfectly stable

### Expected Result
By the end of the animation:
- **Verlet:** Perfect closed ellipse, bounded energy error
- **RK2:** Visibly drifted orbit, large energy error

The contrast should be dramatic despite both methods having O(h²) accuracy!

### Key Insight
This animation provides **visual proof** of the symplectic advantage:

Both methods are second-order, so they have the same local error per step. But:

- **Verlet (symplectic):** Errors don't accumulate in the energy
  - Preserves the geometric structure
  - Orbit stable forever

- **RK2 (non-symplectic):** Errors accumulate linearly in energy
  - Violates the symplectic form
  - Orbit degrades over time

**The moral:** For Hamiltonian systems, symplecticity beats algebraic order!

---

## Animation 3: Two-Particle Lennard-Jones Dynamics

**Files:** `media/animations/03_lj_2_particle.mp4`, `03_lj_2_particle.gif`

### What You See
An animation showing:
- **Left panel:** Two particles moving in 2D space
  - Particles shown as colored circles
  - Trails showing recent history
  - Distance between particles indicated

- **Right panel:** Energy vs time plot
  - Blue: kinetic energy
  - Red: potential energy
  - Black: total energy (should be constant)

### What's Happening
Two atoms interact via Lennard-Jones forces and exhibit bound orbital motion:

**Initial state:**
- Separated by r = 1.5σ (beyond equilibrium)
- Moving perpendicular to separation line
- Negative total energy → bound state

**Dynamics:**
- Particles attract via r⁻⁶ term
- As they approach, KE increases, PE decreases
- When too close, r⁻¹² repulsion kicks in
- They bounce apart and orbit continues

**Energy exchange:**
- Oscillates between kinetic and potential
- Total energy constant (horizontal black line)
- Period matches the orbital period

### Expected Result
- Particles orbit their common center of mass
- Separation oscillates periodically
- Energy plot shows anti-correlated KE and PE oscillations
- Total energy stays flat (no drift)

### Key Insight
This demonstrates **molecular dynamics in action**:

Lennard-Jones potential models real atomic interactions:
- Van der Waals attraction at medium range
- Pauli repulsion at short range
- Equilibrium at r_eq = 2^(1/6)σ

The Störmer-Verlet integrator:
- Conserves energy (no artificial heating)
- Maintains bound state (no artificial dissipation)
- Stable for thousands of time steps

Real MD simulations:
- Millions of atoms
- Billions of time steps
- Same basic principle
- Verlet is the workhorse algorithm

---

## Animation 4: Three-Particle Lennard-Jones Dynamics

**Files:** `media/animations/04_lj_3_particle.mp4`, `04_lj_3_particle.gif`

### What You See
Same layout as Animation 3, but with three particles:
- **Left panel:** Three particles in complex orbital motion
- **Right panel:** Energy conservation plot

### What's Happening
Adding a third particle creates **many-body dynamics**:

**Interactions:**
- Three pairwise forces (1-2, 1-3, 2-3)
- Each particle influenced by two others
- Non-integrable system (no analytical solution)

**Possible behaviors:**
- Bound three-body orbit (all stay together)
- Two-body pair + spectator
- Chaotic motion (sensitive to initial conditions)
- Energy exchange between pairs

**Energy conservation:**
- Still exact despite complexity
- More rapid oscillations than two-body
- Total energy flat

### Expected Result
- Three particles execute complex choreography
- May form transient triangular configurations
- May see particles exchange partners
- Energy perfectly conserved throughout

### Key Insight
This shows **scaling to many-body systems**:

Going from 2 to 3 particles:
- Doubles the number of interactions (1 → 3 pairs)
- Exponentially increases dynamical complexity
- But Verlet still conserves energy perfectly!

For N particles:
- N(N-1)/2 pairwise interactions
- Still symplectic
- Still energy conserving
- Scales to N → 10⁹ in production codes

The key to large-scale molecular dynamics is:
1. Symplectic integrator (Verlet)
2. Efficient neighbor lists
3. Cutoff radii for long-range forces
4. Parallelization

But the foundation is always the simple, elegant Störmer-Verlet method!

---

## Summary Table

| Plot | Key Property Demonstrated | Expected Outcome |
|------|---------------------------|------------------|
| 1. Splitting Diagram | Decomposition structure | Kick-drift-kick symmetry |
| 2. SV vs Euler | Catastrophic failure of non-symplectic | Euler spirals, Verlet stable |
| 3. SV vs RK2 | **Symplecticity > Order** | Both O(h²), only Verlet stable |
| 4. SV vs RK4 Long-term | High order still drifts | RK4 drifts despite O(h⁴) |
| 5. Energy Crossover | When RK4 becomes worse | Crossover at ~50-100 orbits |
| 6. All Methods | Symplectic dichotomy | Symplectic bounded, others drift |
| 7. Reversibility | Time-reversal symmetry | Only Verlet at machine precision |
| 8-9. Area Preservation | Liouville's theorem | Symplectic preserves, others distort |
| 10-11. Splitting Flow | Geometric interpretation | Kick-drift-kick in phase space |
| 12-13. Lennard-Jones | Realistic molecular dynamics | Energy conserved, bound states |
| 14. Local Error | Order of accuracy | Verlet O(h²), RK4 O(h⁴) |

---

## References for Further Reading

1. **Hairer, Lubich & Wanner** (2006). *Geometric Numerical Integration*.
   - Chapter II.3: Verlet method
   - Chapter VI: Symplectic integration
   - Chapter IX: Backward error analysis

2. **Leimkuhler & Reich** (2004). *Simulating Hamiltonian Dynamics*.
   - Chapter 2: Verlet and velocity Verlet
   - Chapter 3: Symplectic methods
   - Chapter 5: Molecular dynamics applications

3. **Verlet** (1967). "Computer Experiments on Classical Fluids". *Physical Review*.
   - Original paper introducing the method

4. **Ruth** (1983). "A Canonical Integration Technique". *IEEE Trans. Nucl. Sci*.
   - Higher-order symplectic integrators

---

## Questions These Visualizations Answer

1. **Why not use Euler?** → Plot 2 shows catastrophic failure
2. **Why not use RK2/RK4?** → Plots 3-6 show energy drift despite high order
3. **What makes Verlet special?** → Plots 7-9 show symplecticity and reversibility
4. **How does Verlet work?** → Plots 1, 10-11 show the splitting structure
5. **Does it work for real systems?** → Plots 12-13 show molecular dynamics
6. **What about accuracy?** → Plot 14 shows Verlet is second-order accurate

The overarching message: **Geometric structure preservation (symplecticity) is more important than algebraic accuracy order for long-term Hamiltonian integration.**
