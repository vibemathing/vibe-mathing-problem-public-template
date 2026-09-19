# Chapter 6: AI for PDEs (Numerical Computation)

## Core Idea
Physics-Informed Neural Networks (PINNs) turn a PDE into an optimization problem by parameterizing the solution with a neural network and putting the differential equation plus boundary/initial/data constraints into the loss. Their usefulness depends on the problem regime; classical numerical methods remain essential baselines and often remain preferable. Reliable practice requires method selection, loss/sampling design, error-source diagnosis, and cross-validation.

## Frameworks Introduced

### Classical Numerical Method Selector
- **When to use**: Always establish a conventional baseline before committing to a neural PDE solver.
- **How**:
  - **FDM**: use derivative stencils on regular grids; simplest for regular domains and low dimensions.
  - **FEM**: use weak/variational form and local basis functions on flexible meshes; strong for complex geometry.
  - **FVM**: integrate conservation laws over control volumes and compute interface fluxes; strong when conservation/shocks matter.
  - **Spectral**: expand globally in Fourier/Chebyshev-like bases; excellent for smooth solutions/simple geometry where global dense operations are acceptable.
- **Selection principle**: match the numerical representation to geometry, regularity, conservation requirements, dimensionality, and desired accuracy.

### PINN Composite-Loss Solver
- **When to use**: The PDE residual can be evaluated through automatic differentiation and a meshless global function representation has advantages.
- **How**:
  1. Parameterize `u(x,t)` as `u_theta(x,t)` with a differentiable network.
  2. Use AutoDiff to compute needed spatial/time derivatives.
  3. Define the PDE residual on interior collocation points.
  4. Add boundary and initial losses; add observation/data loss for data assimilation or inverse problems.
  5. Optimize
     `L = λ_f L_f + λ_b L_b + λ_i L_i + λ_d L_d`.
  6. Validate on independent points and against known physics/reference solvers.
- **Why it works**: the network supplies a continuous global approximation while the physics residual provides supervision without requiring solution labels throughout the domain.

### PINN Error Triad
- **When to use**: Training stalls, residual loss is misleading, or solution quality is inconsistent.
- **How**: diagnose three different sources.
  1. **Approximation error**: network/activation cannot represent the solution efficiently (high frequency, sharp fronts, multiscale structure).
  2. **Optimization error**: representable solution exists but nonconvex training, initialization, learning rates, or loss imbalance prevent reaching it.
  3. **Generalization/discretization error**: loss is low on finite collocation points but the PDE is violated between/away from samples.
- **Recovery**: change architecture/features for approximation error; optimizer/weighting/staging for optimization error; sampling density/adaptivity/validation for generalization error.

### PINN Validation Gate
- **When to use**: Before reporting a serious scientific/engineering result.
- **How**:
  1. Compare against a high-precision classical solution when feasible.
  2. Increase residual/collocation density and check convergence.
  3. Evaluate on an independent dense point set.
  4. Check physical plausibility: symmetry, monotonicity, positivity, mass/energy/conservation laws as applicable.
  5. For inverse problems, vary sensors/noise/regularization and examine identifiability.
- **Failure condition**: decreasing training loss alone is insufficient evidence.

## Key Concepts

### Traditional methods
**FDM** approximates derivatives by finite differences. For a `d`-dimensional grid with `N` interior points per axis, degrees of freedom scale as `N^d`, exposing the curse of dimensionality. The 2D Poisson stencil yields a sparse structured linear system; iterative solvers such as conjugate gradient/multigrid exploit that sparsity. Central differences can achieve `O(h^2)` truncation error under suitable smoothness.

**FEM** derives a weak form, divides the domain into elements, uses local piecewise-polynomial basis functions, assembles a global sparse stiffness matrix, applies boundary conditions, and solves for nodal coefficients. Its mesh flexibility is a major advantage for complex domains. For smooth solutions and first-order elements, the chapter gives the standard qualitative convergence pattern: `L2` error behaves like `O(h^2)` and `H1` error like `O(h)`.

**FVM** enforces integrated conservation on each control volume. Interface fluxes are the central numerical object; upwinding improves stability for convection-dominated flow but low-order schemes add numerical diffusion. The method remains natural for conservation laws and weak/discontinuous solutions.

**Spectral methods** use global smooth basis functions. For smooth solutions they can converge dramatically faster than algebraic-order grid methods; Chebyshev collocation mitigates endpoint interpolation problems. Their global differentiation matrices are dense, and discontinuities cause Gibbs-like difficulties.

### Why PINNs are attractive
- meshless treatment of irregular geometry;
- direct fusion of PDE constraints with sparse observations;
- natural treatment of unknown parameters/functions as trainable quantities;
- possible advantages in high-dimensional problems where tensor-product grids explode;
- one learned function can be evaluated continuously at arbitrary points.

These are scenario advantages, not a universal performance guarantee.

### Loss balancing
The PDE residual may have a very different magnitude/gradient scale from boundary or initial losses. Setting all `λ` values to 1 can let easy BC/IC terms dominate, producing a network that looks trained while still violating the PDE.

Use:
- initial magnitude balancing so weighted terms begin at comparable effective scales;
- adaptive weights based on current losses or descent rates;
- gradient-norm balancing when one objective dominates parameter updates;
- trainable uncertainty-like weights where justified.

### Sampling and architecture
Collocation-point distribution acts like a discretization. Uniform random samples are simple; adaptive sampling should concentrate on high-residual or rapidly changing regions, especially shocks/boundaries. In high dimensions, sparse/low-discrepancy structures and specialized architectures may be necessary.

Architecture cues:
- **MLP**: default coordinate-to-value map, simple and AutoDiff-friendly; suffers spectral bias.
- **CNN**: useful when fields lie on regular grids with local correlations; less natural for irregular domains.
- **RNN/LSTM**: temporal/sequence structure; hard to parallelize and train deeply.
- **Transformer**: long-range/global interactions and point clouds; high memory/compute and data demands.
- **KAN**: promising parameter efficiency/interpretability but described as still exploratory.

## Application Patterns

### Forward Poisson / complex geometry
Use a coordinate MLP, interior residual samples, and boundary loss. Hard-enforcing simple boundary conditions can improve reliability when a transformation can satisfy them exactly. For singular/high-frequency regions, increase local sampling or decompose the domain.

### Burgers equation / shocks
Standard smooth PINNs may locate the shock without spurious numerical oscillation, yet can smooth it excessively, especially at very low viscosity. Use dense/adaptive samples around the front, shock-aware features or domain decomposition. A conventional upwind/TVD reference remains valuable.

### Parameter inversion
Treat an unknown scalar such as diffusion coefficient `κ` as a trainable parameter alongside network weights. Add observation loss at sensor points. Sparse/noisy data can still identify parameters when the problem is informative, but ill-posedness/multiple solutions require priors or regularization. Place sensors where the solution is sensitive to the parameter.

### Source/function inversion
Use two networks: one for `u(x)` and another for unknown source `f(x)`. Couple them through the PDE residual and data. Because a whole function is being inferred, non-uniqueness is severe; impose justified priors (smoothness, sparsity, positivity, support) or add data.

### High-dimensional structured PDEs
For option-pricing-like problems, exploit separable/low-rank structure. SPINN-style separable representations reduce complexity; domain decomposition (cPINN/XPINN families) enforces interface continuity/flux; Fourier features help high-frequency components; adaptive sampling focuses budget. Do not extrapolate success on separable/low-rank cases to arbitrary hundred-dimensional PDEs.

### Multiphysics coupling
Use separate outputs/subnetworks for fields and explicitly include interface coupling conditions (kinematic/dynamic continuity, conservation, etc.) in the objective. Nondimensionalize and adapt weights because different physical residuals may have incompatible scales. Staged training can reduce interference.

## Mental Models

### Collocation Points Are a Mesh in Disguise
PINNs avoid a fixed mesh, yet they still approximate a continuous constraint using finitely many samples. Poor sampling produces a discretization/generalization problem analogous to a bad mesh.

### Training Loss Is a Weighted Treaty
Each physical/boundary/data term competes for parameter updates. Loss coefficients determine which constraints the optimizer honors first; inspect gradients/residuals per term rather than only the total.

### PINN as Specialist, Classical Solver as Reference
Use PINNs where their representation solves a real bottleneck. Keep classical solvers for comparison, sanity checks, and regimes where numerical analysis already provides superior accuracy/cost guarantees.

## Anti-patterns
- **PINN by default**: selecting a neural solver for a low-dimensional regular PDE where FDM/FEM/spectral methods are simpler and better validated.
- **Loss-only validation**: interpreting a small training objective as solution accuracy.
- **Equal weights by habit**: allowing BC/IC terms to dominate the PDE residual.
- **Uniform sampling through a shock**: undersampling exactly where the solution is hardest.
- **Universal approximation as convergence theory**: approximation existence gives no guarantee that optimization finds the right function or that collocation generalizes.
- **Inverse problem without identifiability analysis**: producing one fitted parameter/source while many alternatives explain the data.
- **No convergence/reference study**: reporting a scientific result without denser sampling or comparison against a trusted method.

## Reference Table: Method Selection
| Method | Best fit | Strength | Main limitation |
|---|---|---|---|
| FDM | simple regular grids | simple sparse stencils | geometry + dimensional curse |
| FEM | complex geometry/variational PDEs | flexible mesh, strong theory | meshing/assembly cost |
| FVM | conservation laws/shocks | discrete conservation | high-order flux design complexity |
| Spectral | smooth solution/simple domain | very high accuracy per DOF | discontinuities, dense/global operations |
| PINN | inverse/data fusion, some high-dim/meshless cases | unified differentiable physics/data objective | training instability, error guarantees, hyperparameters |

## Worked Example: Diagnosing a Bad PINN
A PINN for a Poisson problem reaches total loss `1e-6`, yet comparison with FEM shows a large interior error.

1. **Approximation test**: inspect whether the source/solution is highly oscillatory. If yes, increase representation capacity or use sinusoidal/Fourier features.
2. **Optimization test**: report `L_f`, `L_b`, and their gradient norms separately. If boundary loss is tiny while PDE residual dominates or vice versa, rebalance `λ` or stage training.
3. **Generalization test**: evaluate residual on a dense independent grid. If training points look good but holes are bad, increase/adapt collocation density in those regions.
4. **Reference test**: rerun FEM with mesh refinement to ensure the comparison baseline itself is converged.
5. **Convergence test**: increase PINN residual-point density and check whether solution error decreases. If not, do not report the small training loss as evidence of PDE accuracy.

## Key Takeaways
1. Classical PDE methods remain the first comparison set and often the preferred solver.
2. PINNs encode physics by placing equation and constraint residuals in the loss through AutoDiff.
3. Loss weighting and collocation sampling are core numerical design choices.
4. Diagnose approximation, optimization, and generalization/discretization errors separately.
5. PINNs are strongest in selected inverse, data-assimilation, meshless, and structured high-dimensional regimes.
6. Serious use requires independent validation, convergence checks, and physical plausibility tests.

## Connects To
- **Ch 1**: applies the problem-first rule to numerical mathematics.
- **Ch 2**: draws on neural approximation, optimization, regularization, and generalization.
- **Ch 3**: shares representation/inductive-bias and adaptive search principles.
- **Ch 4–5**: shares the broader generator-versus-verifier discipline: a trained model proposes a numerical solution, while independent mathematics/numerics assess trust.
