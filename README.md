# Theoretical Insights on Training Instability in Deep Learning — Manim Visualization

A Vietnamese-narrated [Manim](https://www.manim.community/) animation series that visualizes the
**NeurIPS 2025 Tutorial "Theoretical Insights on Training Instability in Deep Learning"**
(Jingfeng Wu, Yu-Xing Wang, Maryam Fazel). The animations accompany a slide deck used
for a YouTube tutorial and walk through the core ideas in two parts:

1. **Optimization** — why gradient descent with a *large* stepsize, beyond the classical
   stability threshold `η < 2/L`, can converge faster than classical theory predicts
   (Edge-of-Stability, two-phase convergence, adaptive stepsizes, ℓ₂-regularization).
2. **Generalization** — why large-stepsize GD is implicitly biased toward flat minima,
   and how that translates into provable generalization bounds (matrix sensing, ReLU
   networks, total-variation constraints in function space).

## Repository structure

```
.
├── intro.py        # 8 scenes  — intro / motivation
├── part1.py        # 16 scenes — Part 1: Optimization
├── part2.py        # 16 scenes — Part 2: Generalization
├── slides/         # Slide decks (reference + YouTube tutorial deck)
├── docs/           # Supporting notes (core formulas reference)
├── media/videos/   # Rendered output (1080p60), organized by file/scene
└── .vscode/        # Editor settings
```

## Scenes

### `intro.py` — Introduction

| Scene | Description |
|---|---|
| `S1_Title` | Title card |
| `S2_VideoObjectives` | Video objectives |
| `S2_LossSpikes` | Loss spikes — main hook |
| `S3_WhyUnstable` | Four causes of training instability |
| `S4_GDDemo` | GD with small vs. large stepsize (1D demo) |
| `S4b_GradientFlow` | The three stepsize regimes + gradient flow |
| `S5_StabilityCondition` | Descent Lemma & Edge of Stability |
| `S6_Outline` | Outline of Part 1 & Part 2 |

### `part1.py` — Part 1: Optimization

| Scene | Description |
|---|---|
| `P0_WhyLargeStepsize` | Why large stepsize helps optimization |
| `P1_Overview` | Part 1 outline |
| `P2_DescentLemma` | Descent Lemma — step-by-step proof |
| `P2b_LargeEtaPhases` | Optimization with large η — 3-phase timeline |
| `P3_ConvergenceRates` | Classical convergence rates |
| `P4_Acceleration` | Nesterov acceleration |
| `P5_LargeStepsize` | From small to large stepsize |
| `P6_MentalModel` | Mental model spectrum (linear → logistic → deep learning) |
| `P7_LogisticSetup` | Logistic regression setup |
| `P8_TwoPhases` | Two-phase behavior (log-log loss curves) |
| `P9_MainTheorem` | Main theorem: phase transition time + convergence rates |
| `P10_AdaptiveGD` | Adaptive gradient descent |
| `P11_L2Reg` | ℓ₂-regularization |
| `P11b_ValleyBasinRegimes` | Stepsize regimes: valley + basin |
| `P11c_RelatedWork` | Related work: long steps / silver stepsize |
| `P12_OptSummary` | Part 1 summary |

### `part2.py` — Part 2: Generalization

| Scene | Description |
|---|---|
| `G0_RecapPart1` | Recap of Part 1 → transition |
| `G1_Part2Overview` | Part 2 overview: three key questions |
| `G1b_ImplicitBias` | Interpolation & implicit bias of large stepsize |
| `G1c_ChaoticDynamics` | Chaotic dynamics in early-phase GD |
| `G2_StepsizeEffect` | Effect of stepsize on learned functions |
| `G3_FlatMinimaEoS` | Flat minima, Edge of Stability & nested sets |
| `G4_OverparamDoubleDescent` | Overparameterization & double descent |
| `G4b_ShuffledLabels` | Case study: fitting random labels |
| `G5_MatrixSensing` | Matrix sensing: setup & flatness measure |
| `G6_MatrixSensingThm` | Matrix sensing: exact recovery theorem |
| `G7_ReLUNNSetup` | 2-layer ReLU NN + GD setup |
| `G8_TVConstraint` | Flatness implies a total-variation constraint |
| `G8b_WeightingFunction` | Role of the weighting function g(x) |
| `G9_GenBounds` | Generalization bounds & feature learning |
| `G10_OpenProblems` | Extensions: logistic loss & open problems |
| `G11_Conclusion` | Part 2 conclusion |

## Setup

The animations were built and rendered with:

- Python 3.11
- [ManimCE](https://www.manim.community/) v0.20.1

```bash
conda create -n manim-env python=3.11
conda activate manim-env
pip install manim
```

## Rendering

Render a single scene at 1080p60:

```bash
manim part1.py P1_Overview -qh
```

Render every scene in a file:

```bash
manim part1.py -qh -a
```

Output is written to `media/videos/<file>/1080p60/<Scene>.mp4`. Other Manim quality flags
(`-ql` 480p15, `-qm` 720p30, `-qk` 4K60) and intermediate render caches
(`media/Tex/`, `media/texts/`, `media/images/`, `partial_movie_files/`) are git-ignored —
delete `media/` and re-render at any time to regenerate them.

## Slides

- `slides/youtube_tutorial_slides.pdf` — slide deck used alongside this video series
  on YouTube.
- `slides/neurips2025_original_slides.pdf` — original NeurIPS 2025 tutorial slides
  (source material).

## Docs

- `docs/formulas.tex` — reference sheet of the core mathematical formulas used across
  all scenes.

## License

MIT — see [LICENSE](LICENSE).
