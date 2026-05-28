from manim import *
import numpy as np

# ═══════════════════════════════════════════════════════════════════════════════
#  GLOBAL PALETTE  (3Blue1Brown-inspired dark theme)
# ═══════════════════════════════════════════════════════════════════════════════
BG       = "#0D0D1A"
C_BLUE   = "#58C4DD"
C_GOLD   = "#FFD60A"
C_GREEN  = "#5DD39E"
C_RED    = "#FF6B6B"
C_WHITE  = "#E8E8E8"
C_GRAY   = "#7A7A8C"
C_PURPLE = "#C77DFF"
C_ORANGE = "#FF9F43"

config.background_color = BG


# ═══════════════════════════════════════════════════════════════════════════════
#  G1 – PART 2 OVERVIEW: 3 KEY QUESTIONS  (slides 1–6)
# ═══════════════════════════════════════════════════════════════════════════════
class G1_Part2Overview(Scene):
    def construct(self):
        badge = Text("Part 2: Generalization", font_size=26,
                     color=C_GREEN, weight=BOLD)
        badge.to_edge(UP, buff=0.55)

        title = Text("Rethinking Generalization",
                     font_size=44, color=C_WHITE, weight=BOLD)
        title.next_to(badge, DOWN, buff=0.28)
        uline = Line(LEFT * 3.8, RIGHT * 3.8,
                     color=C_GREEN, stroke_width=2.5).next_to(title, DOWN, buff=0.1)

        premise = Text(
            "Deep learning models are NOT capacity limited —",
            font_size=22, color=C_GOLD,
        )
        premise_sub = Text(
            "generalization depends on the optimizer's implicit bias!",
            font_size=20, color=C_GOLD,
        )
        premise_sub.next_to(premise, DOWN, buff=0.08)
        premise_grp = VGroup(premise, premise_sub).next_to(uline, DOWN, buff=0.35)

        # ── 3 Questions ────────────────────────────────────────────────────────
        q_data = [
            ("Q1:", "Does GD with large stepsize find generalizing solutions?",
             "Clean labels — many interpolating solutions exist.", C_BLUE),
            ("Q2:", "What solutions does GD find when labels are noisy?",
             "Benign / tempered / catastrophic overfitting?", C_ORANGE),
            ("Q3:", "How does large stepsize interact with other 'forces of nature'?",
             "Architecture, data distribution, augmentation...", C_PURPLE),
        ]

        cards = VGroup()
        for qid, qtxt, sub, col in q_data:
            q_t  = Text(qid, font_size=22, color=col, weight=BOLD)
            qt_t = Text(qtxt, font_size=21, color=C_WHITE)
            qt_t.next_to(q_t, RIGHT, buff=0.2)
            sub_t = Text(sub, font_size=17, color=C_GRAY)
            sub_t.next_to(qt_t, DOWN, buff=0.06, aligned_edge=LEFT)
            cards.add(VGroup(q_t, qt_t, sub_t))

        cards.arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        cards.next_to(premise_grp, DOWN, buff=0.38)
        cards.shift(LEFT * 0.4)

        self.play(FadeIn(badge, shift=DOWN * 0.1), run_time=0.7)
        self.play(Write(title), Create(uline), run_time=0.9)
        self.play(FadeIn(premise_grp, shift=UP * 0.1), run_time=0.8)
        self.wait(0.2)
        for card in cards:
            self.play(FadeIn(card, shift=RIGHT * 0.2), run_time=0.65)
            self.wait(0.12)

        focus_box = SurroundingRectangle(
            cards[0], color=C_BLUE, stroke_width=1.8,
            buff=0.18, corner_radius=0.1
        )
        self.wait(0.4)
        self.play(Create(focus_box), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  G2 – STEPSIZE EFFECT ON LEARNED FUNCTIONS  (slides 8–14)
# ═══════════════════════════════════════════════════════════════════════════════
class G2_StepsizeEffect(Scene):
    def construct(self):
        title = Text("Effect of Stepsize on Learned Functions",
                     font_size=32, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.40)
        uline = Line(LEFT * 5.5, RIGHT * 5.5,
                     color=C_BLUE, stroke_width=1.8).next_to(title, DOWN, buff=0.08)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.15)

        # ── Experiment setup ───────────────────────────────────────────────────
        setup_txt = Text(
            "2-layer ReLU NN  ·  30 data points  ·  Noisy labels  ·  Square loss",
            font_size=19, color=C_GRAY,
        )
        setup_txt.next_to(uline, DOWN, buff=0.22)
        self.play(FadeIn(setup_txt), run_time=0.5)

        # ── True function: tent f_0(x) = max(0, 1 - |x|/0.4) ─────────────────
        def true_fn(x):
            return np.maximum(0.0, 1.0 - np.abs(x) / 0.4)

        # ── Mini axes factory ──────────────────────────────────────────────────
        def make_mini(shift_vec):
            ax = Axes(
                x_range=[-0.55, 0.55, 0.25],
                y_range=[-0.8, 1.8, 0.5],
                x_length=2.8, y_length=2.2,
                axis_config={"color": C_GRAY, "stroke_width": 1,
                             "include_tip": False},
            )
            ax.shift(shift_vec)
            return ax

        # ── Data points (same seed) ───────────────────────────────────────────
        np.random.seed(42)
        n_pts = 30
        x_d = np.random.uniform(-0.5, 0.5, n_pts)
        y_d = true_fn(x_d) + np.random.randn(n_pts) * 0.3

        # ── 4 scenarios ───────────────────────────────────────────────────────
        scenarios = [
            (r"\eta = 0.5",  C_BLUE,
             lambda x: np.full_like(x, 0.50),
             "Constant\n(underfits)", UP * 3.0 + LEFT * 4.6),
            (r"\eta = 0.4",  C_GREEN,
             lambda x: np.clip(1.0 - np.abs(x) / 0.38, 0, 1.05),
             "Matches truth\n(generalizes!)", UP * 3.0 + LEFT * 1.5),
            (r"\eta = 0.3",  C_GOLD,
             lambda x: np.clip(1.0 - np.abs(x) / 0.38, -0.2, 1.1) + 0.15 * np.sin(8 * x),
             "Slightly spiky\n(ok)", DOWN * 0.6 + LEFT * 4.6),
            (r"\eta = 0.01", C_RED,
             lambda x: true_fn(x) + 0.45 * np.sin(20 * x) + 0.3 * np.sin(35 * x),
             "Many kinks\n(overfits!)", DOWN * 0.6 + LEFT * 1.5),
        ]

        all_grps = VGroup()
        for eta_tex, col, fn, desc_txt, pos in scenarios:
            ax = make_mini(pos)

            # True function
            true_curve = ax.plot(
                lambda x, f=true_fn: f(x),
                x_range=[-0.5, 0.5, 0.01],
                color=C_WHITE, stroke_width=1.5, stroke_opacity=0.5,
            )
            # Fitted function
            fitted_curve = ax.plot(
                lambda x, f=fn: float(np.clip(f(np.array([x])), -1.5, 2.5)[0]),
                x_range=[-0.5, 0.5, 0.01],
                color=col, stroke_width=2.5,
            )
            # Data dots
            dots = VGroup(*[
                Dot(ax.c2p(xi, yi), radius=0.045,
                    color=C_GRAY, fill_opacity=0.7)
                for xi, yi in zip(x_d, y_d)
                if -0.52 < xi < 0.52 and -0.8 < yi < 1.8
            ])

            eta_lbl = MathTex(eta_tex, font_size=22, color=col)
            eta_lbl.next_to(ax, UP, buff=0.12)
            desc = Text(desc_txt, font_size=14, color=col)
            desc.next_to(ax, DOWN, buff=0.12)

            all_grps.add(VGroup(ax, true_curve, fitted_curve, dots, eta_lbl, desc))

        for grp in all_grps:
            self.play(FadeIn(grp, shift=UP * 0.15), run_time=0.75)
            self.wait(0.1)

        self.wait(0.4)

        # ── Key observation ────────────────────────────────────────────────────
        obs = Text(
            "Larger stepsize  →  fewer linear pieces  →  simpler function  →  better generalization",
            font_size=20, color=C_GOLD,
        )
        obs.to_edge(DOWN, buff=0.45)
        obs_box = SurroundingRectangle(
            obs, color=C_GOLD, stroke_width=1.8, buff=0.18, corner_radius=0.1
        )
        self.play(Write(obs), Create(obs_box), run_time=1.0)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  G3 – FLAT MINIMA, EDGE OF STABILITY & NESTED SETS  (slides 15–16)
# ═══════════════════════════════════════════════════════════════════════════════
class G3_FlatMinimaEoS(Scene):
    def construct(self):
        title = Text("Flat Minima, Edge of Stability & Low-Curvature Regions",
                     font_size=28, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        uline = Line(LEFT * 5.5, RIGHT * 5.5,
                     color=C_PURPLE, stroke_width=2).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.2)

        # ── Loss landscape: flat vs sharp minimum ─────────────────────────────
        ax_land = Axes(
            x_range=[-3.5, 3.5, 1], y_range=[-0.1, 2.0, 0.5],
            x_length=5.5, y_length=2.8,
            axis_config={"color": C_GRAY, "stroke_width": 1,
                         "include_tip": True},
        ).shift(LEFT * 3.2 + DOWN * 0.5)

        def landscape(x):
            base      = 0.10 * (x + 0.2) ** 2 + 0.40
            flat_dip  = 0.38 * np.exp(-0.60 * (x + 1.8) ** 2)
            sharp_dip = 0.45 * np.exp(-9.00 * (x - 1.5) ** 2)
            hump      = 0.25 * np.exp(-2.00 * (x + 0.15) ** 2)
            return base - flat_dip - sharp_dip + hump

        land_curve = ax_land.plot(
            landscape, x_range=[-3.2, 3.2, 0.05],
            color=C_BLUE, stroke_width=2.5
        )

        # Flat minimum dot (broad basin at x≈-1.8)
        flat_x, flat_y = -1.8, landscape(-1.8)
        flat_dot = Dot(ax_land.c2p(flat_x, flat_y),
                       color=C_GREEN, radius=0.12)
        flat_lbl = Text("Flat\nminimum", font_size=17, color=C_GREEN)
        flat_lbl.next_to(flat_dot, UP + LEFT * 0.2, buff=0.12)

        # Sharp minimum dot (narrow basin at x≈1.5)
        sharp_x, sharp_y = 1.5, landscape(1.5)
        sharp_dot = Dot(ax_land.c2p(sharp_x, sharp_y),
                        color=C_RED, radius=0.12)
        sharp_lbl = Text("Sharp\nminimum", font_size=17, color=C_RED)
        sharp_lbl.next_to(sharp_dot, UP + RIGHT * 0.2, buff=0.12)

        # EoS condition below landscape
        eos_eq = MathTex(
            r"\text{EoS: }\lambda_{\max}(\nabla^2\mathcal{L}(\theta)) \approx \frac{2}{\eta}",
            font_size=22, color=C_GOLD,
        )
        eos_eq.next_to(ax_land, DOWN, buff=0.28)

        self.play(Create(ax_land), Create(land_curve), run_time=1.0)
        self.play(
            FadeIn(flat_dot), FadeIn(flat_lbl),
            FadeIn(sharp_dot), FadeIn(sharp_lbl),
            run_time=0.8,
        )
        self.play(Write(eos_eq), run_time=0.8)
        self.wait(0.3)

        # ── Nested set diagram ─────────────────────────────────────────────────
        outer_rect = RoundedRectangle(
            width=5.4, height=4.2, corner_radius=0.3,
            color=C_WHITE, fill_opacity=0.05, stroke_width=1.8
        )
        outer_lbl = Text("All functions f_θ", font_size=14, color=C_GRAY)
        outer_lbl.next_to(outer_rect.get_top(), DOWN, buff=0.18)

        mid_ellipse = Ellipse(
            width=4.2, height=2.8,
            color=C_BLUE, fill_color=C_BLUE, fill_opacity=0.18,
            stroke_width=2,
        )
        mid_lbl_1 = Text("Low-curvature regions", font_size=15, color=C_BLUE, weight=BOLD)
        mid_eq = MathTex(
            r"\{f_\theta \mid \lambda_{\max}(\nabla^2\mathcal{L}) \le 2/\eta\}",
            font_size=16, color=C_BLUE,
        )
        mid_lbl = VGroup(mid_lbl_1, mid_eq).arrange(DOWN, buff=0.08)
        mid_lbl.next_to(mid_ellipse.get_top(), DOWN, buff=0.25)

        inner_ellipse = Ellipse(
            width=2.2, height=1.2,
            color=C_GOLD, fill_color=C_GOLD, fill_opacity=0.35,
            stroke_width=2,
        ).shift(DOWN * 0.25)
        inner_lbl = Text("Flat minima", font_size=15, color=C_GOLD, weight=BOLD)
        inner_lbl.move_to(inner_ellipse)

        nested_grp = VGroup(outer_rect, outer_lbl, mid_ellipse,
                            mid_lbl, inner_ellipse, inner_lbl)
        nested_grp.shift(RIGHT * 3.0 + DOWN * 0.3)

        self.play(FadeIn(outer_rect), FadeIn(outer_lbl), run_time=0.6)
        self.play(
            FadeIn(mid_ellipse), FadeIn(mid_lbl), run_time=0.7
        )
        self.play(
            FadeIn(inner_ellipse), FadeIn(inner_lbl), run_time=0.7
        )

        # GD/SGD measures note
        meas_note_gd  = MathTex(
            r"\text{GD: } S(\theta)=\lambda_{\max}(\nabla^2\mathcal{L}),\quad C=2/\eta",
            font_size=18, color=C_BLUE,
        )
        meas_note_sgd = MathTex(
            r"\text{SGD: } S(\theta)=\mathrm{tr}(\nabla^2\mathcal{L}),\quad C=O(1/\eta)",
            font_size=18, color=C_GREEN,
        )
        meas_note = VGroup(meas_note_gd, meas_note_sgd).arrange(DOWN, buff=0.18)
        meas_note.to_edge(DOWN, buff=0.45)

        self.play(FadeIn(meas_note, shift=UP * 0.1), run_time=0.8)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  G4 – OVERPARAMETERIZATION & DOUBLE DESCENT  (slides 20–21)
# ═══════════════════════════════════════════════════════════════════════════════
class G4_OverparamDoubleDescent(Scene):
    def construct(self):
        title = Text("Overparameterization → Many Solutions",
                     font_size=34, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        uline = Line(LEFT * 4.8, RIGHT * 4.8,
                     color=C_GOLD, stroke_width=2).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.2)

        # ── Overparameterized setup ────────────────────────────────────────────
        setup_eq = MathTex(
            r"\min_{\theta\in\mathbb{R}^d}\;\mathcal{L}(\theta)"
            r":=\frac{1}{n}\sum_{i=1}^n\ell(y_i,\,f_\theta(x_i))",
            font_size=28, color=C_WHITE,
        )
        setup_eq.next_to(uline, DOWN, buff=0.32)

        ratio = MathTex(
            r"\underbrace{d}_{\#\text{params}} \;\gg\; \underbrace{n}_{\#\text{samples}}",
            font_size=26, color=C_BLUE,
        )
        ratio.next_to(setup_eq, DOWN, buff=0.22)

        key_q = Text(
            "Overparameterization → many zero-loss solutions.  Which one does GD find?",
            font_size=20, color=C_GOLD,
        )
        key_q.next_to(ratio, DOWN, buff=0.3)

        self.play(Write(setup_eq), run_time=0.9)
        self.play(FadeIn(ratio, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(key_q, shift=UP * 0.1), run_time=0.7)
        self.wait(0.3)

        # ── Double descent curve ───────────────────────────────────────────────
        ax = Axes(
            x_range=[0, 5.5, 1], y_range=[-0.1, 2.2, 0.5],
            x_length=6.5, y_length=2.8,
            axis_config={"color": C_GRAY, "stroke_width": 1.2,
                         "include_tip": True},
        ).to_edge(DOWN, buff=0.55)

        def train_risk(x):
            return max(0.0, 0.6 * np.exp(-1.2 * x) + 0.04)

        def test_risk(x):
            if x < 2.0:
                return 0.35 * (x - 1.0) ** 2 + 0.25
            elif x < 2.25:
                # sharp spike at interpolation threshold
                return 2.0 * np.exp(-40 * (x - 2.1) ** 2) + 0.25
            else:
                return 0.55 * np.exp(-0.8 * (x - 2.25)) + 0.18

        train_curve = ax.plot(train_risk, x_range=[0.1, 5.3, 0.05],
                              color=C_GREEN, stroke_width=2.2)
        test_curve  = ax.plot(test_risk,  x_range=[0.1, 5.3, 0.05],
                              color=C_BLUE, stroke_width=2.2)

        # Labels
        thresh_line = DashedLine(
            ax.c2p(2.1, -0.1), ax.c2p(2.1, 2.1),
            color=C_RED, stroke_width=1.5, dash_length=0.12
        )
        thresh_lbl = Text("Interpolation\nthreshold", font_size=13, color=C_RED)
        thresh_lbl.next_to(ax.c2p(2.1, 2.1), UP, buff=0.1)

        tr_lbl = Text("Training risk", font_size=14, color=C_GREEN)
        tr_lbl.next_to(train_curve.get_end(), RIGHT, buff=0.1)
        te_lbl = Text("Test risk", font_size=14, color=C_BLUE)
        te_lbl.next_to(ax.c2p(4.5, test_risk(4.5)), UP, buff=0.1)

        x_ax_lbl = Text("Model capacity", font_size=14, color=C_GRAY)
        x_ax_lbl.next_to(ax.x_axis, DOWN, buff=0.22)
        y_ax_lbl = Text("Risk", font_size=14, color=C_GRAY)
        y_ax_lbl.rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.25)

        classic_lbl = Text('"classical" regime', font_size=12, color=C_GRAY)
        classic_lbl.next_to(ax.c2p(0.9, 1.9), UP, buff=0.05)
        modern_lbl  = Text('"modern" interpolating regime', font_size=12, color=C_GRAY)
        modern_lbl.next_to(ax.c2p(3.8, 0.55), UP, buff=0.05)

        self.play(Create(ax), FadeIn(x_ax_lbl), FadeIn(y_ax_lbl), run_time=0.8)
        self.play(
            Create(train_curve, rate_func=linear),
            Create(test_curve,  rate_func=linear),
            run_time=2.5,
        )
        self.play(
            Create(thresh_line), FadeIn(thresh_lbl),
            FadeIn(tr_lbl), FadeIn(te_lbl),
            FadeIn(classic_lbl), FadeIn(modern_lbl),
            run_time=0.9,
        )

        # Flatness arrow
        answer_lbl = Text("Flat minima → generalizing solutions!",
                           font_size=20, color=C_GOLD, weight=BOLD)
        answer_lbl.next_to(key_q, DOWN, buff=0.28)
        self.play(FadeIn(answer_lbl, shift=UP * 0.1), run_time=0.7)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  G5 – MATRIX SENSING: SETUP & FLATNESS MEASURE  (slides 24–26)
# ═══════════════════════════════════════════════════════════════════════════════
class G5_MatrixSensing(Scene):
    def construct(self):
        title = Text("Case Study: Matrix Sensing",
                     font_size=36, color=C_GOLD, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        uline = Line(LEFT * 4.5, RIGHT * 4.5,
                     color=C_GOLD, stroke_width=2).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.2)

        # ── Problem setup ──────────────────────────────────────────────────────
        prob_lbl = Text("Problem:", font_size=22, color=C_WHITE, weight=BOLD)
        prob_eq  = MathTex(
            r"\text{Recover } M_\sharp \in \mathbb{R}^{d \times d}"
            r"\text{ from } b_i = \langle A_i, M_\sharp\rangle",
            font_size=26, color=C_WHITE,
        )
        rank_eq  = MathTex(
            r"r_\sharp := \mathrm{rank}(M_\sharp) \ll d",
            font_size=24, color=C_BLUE,
        )
        prob_lbl.shift(LEFT * 5.2 + UP * 1.7)
        prob_eq.next_to(prob_lbl, RIGHT, buff=0.3)
        rank_eq.next_to(prob_eq, DOWN, buff=0.18, aligned_edge=LEFT)

        # ── Overparameterized reformulation ───────────────────────────────────
        over_lbl = Text("Overparameterized factorization:", font_size=22,
                         color=C_GREEN, weight=BOLD)
        over_lbl.next_to(prob_lbl, DOWN, buff=0.75, aligned_edge=LEFT)

        factor_eq = MathTex(
            r"X = LR^\top,\quad"
            r"\min_{L,R\in\mathbb{R}^{d\times k}}"
            r"\mathcal{L}(L,R)=\|\mathcal{A}(LR^\top)-b\|_2^2",
            font_size=26, color=C_WHITE,
        )
        factor_eq.next_to(over_lbl, RIGHT, buff=0.3)

        k_note = MathTex(
            r"k \gg \mathrm{rank}(M_\sharp):=r_\sharp",
            font_size=22, color=C_GRAY,
        )
        k_note.next_to(factor_eq, DOWN, buff=0.18, aligned_edge=LEFT)

        # ── Flatness measure ───────────────────────────────────────────────────
        flat_lbl = Text("Flatness measure:", font_size=22,
                         color=C_PURPLE, weight=BOLD)
        flat_lbl.next_to(over_lbl, DOWN, buff=0.7, aligned_edge=LEFT)

        flat_eq = MathTex(
            r"\mathrm{tr}(D^2\mathcal{L}(L,R))"
            r"\;=\; c\cdot\mathbb{E}_{U,V\sim\mathcal{N}(0,I)}"
            r"\mathcal{L}(L+U,R+V)",
            font_size=24, color=C_WHITE,
        )
        flat_eq.next_to(flat_lbl, RIGHT, buff=0.3)

        # ── Flat solution optimization ─────────────────────────────────────────
        opt_lbl = Text("Flattest solutions:", font_size=22,
                        color=C_ORANGE, weight=BOLD)
        opt_lbl.next_to(flat_lbl, DOWN, buff=0.7, aligned_edge=LEFT)

        opt_eq = MathTex(
            r"\min_{L,R\in\mathbb{R}^{d\times k}}"
            r"\underbrace{\mathrm{tr}(D^2\mathcal{L}(L,R))}_{\text{quadratic}}"
            r"\quad\text{s.t.}\quad"
            r"\underbrace{\mathcal{A}(LR^\top) = b}_{\text{quadratic}}",
            font_size=24, color=C_WHITE,
        )
        opt_eq.next_to(opt_lbl, RIGHT, buff=0.3)

        opt_box = SurroundingRectangle(
            VGroup(opt_lbl, opt_eq), color=C_ORANGE,
            stroke_width=2, buff=0.2, corner_radius=0.1
        )

        self.play(FadeIn(prob_lbl, shift=RIGHT * 0.15),
                  Write(prob_eq), run_time=1.0)
        self.play(FadeIn(rank_eq), run_time=0.5)
        self.wait(0.2)
        self.play(FadeIn(over_lbl, shift=RIGHT * 0.15),
                  Write(factor_eq), run_time=1.0)
        self.play(FadeIn(k_note), run_time=0.5)
        self.wait(0.2)
        self.play(FadeIn(flat_lbl, shift=RIGHT * 0.15),
                  Write(flat_eq), run_time=1.0)
        self.wait(0.2)
        self.play(FadeIn(opt_lbl, shift=RIGHT * 0.15),
                  Write(opt_eq), run_time=1.0)
        self.play(Create(opt_box), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  G6 – MATRIX SENSING: EXACT RECOVERY THEOREM  (slides 28–31)
# ═══════════════════════════════════════════════════════════════════════════════
class G6_MatrixSensingThm(Scene):
    def construct(self):
        title = Text("Flat Minima Exactly Recover M♯",
                     font_size=34, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        uline = Line(LEFT * 4.5, RIGHT * 4.5,
                     color=C_GREEN, stroke_width=2).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.2)

        # ── Strategy ──────────────────────────────────────────────────────────
        strat_lbl = Text("Strategy:", font_size=22,
                          color=C_BLUE, weight=BOLD)
        strat_eq  = MathTex(
            r"\text{Show } M_\sharp \text{ is the unique solution of: }"
            r"\min_{X}\|D_1 X D_2\|_*\;\text{s.t.}\;\mathcal{A}(X)=b",
            font_size=22, color=C_WHITE,
        )
        strat_lbl.shift(LEFT * 4.5 + UP * 1.7)
        strat_eq.next_to(strat_lbl, RIGHT, buff=0.28)

        # ── Main theorem ───────────────────────────────────────────────────────
        thm_title = Text("Theorem (Matrix Sensing)", font_size=22,
                          color=C_GOLD, weight=BOLD)
        thm_title.next_to(strat_lbl, DOWN, buff=0.72, aligned_edge=LEFT)

        thm_cond = MathTex(
            r"\text{When } m \gtrsim r_\sharp d,"
            r"\text{ with probability } \ge 1 - e^{-\Omega(m)},",
            font_size=22, color=C_WHITE,
        )
        thm_cond.next_to(thm_title, DOWN, buff=0.22)

        thm_exact = MathTex(
            r"L_f R_f^\top = M_\sharp",
            font_size=36, color=C_GREEN,
        )
        thm_exact.next_to(thm_cond, DOWN, buff=0.3)
        thm_exact_lbl = Text("(Exact recovery!)", font_size=18, color=C_GREEN)
        thm_exact_lbl.next_to(thm_exact, RIGHT, buff=0.3)

        thm_norm = MathTex(
            r"\|L_f\|_F^2 + \|R_f\|_F^2 \le (1+\delta)\|M_\sharp\|_*",
            font_size=22, color=C_BLUE,
        )
        thm_norm_lbl = Text("[Norm-minimal]", font_size=17, color=C_BLUE)
        thm_norm_lbl.next_to(thm_norm, RIGHT, buff=0.3)
        thm_norm.next_to(thm_exact, DOWN, buff=0.3)

        thm_bal = MathTex(
            r"\|L_f^\top L_f - R_f^\top R_f\|_* \le \delta\|M_\sharp\|_*",
            font_size=22, color=C_PURPLE,
        )
        thm_bal_lbl = Text("[Balanced]", font_size=17, color=C_PURPLE)
        thm_bal_lbl.next_to(thm_bal, RIGHT, buff=0.3)
        thm_bal.next_to(thm_norm, DOWN, buff=0.22)

        thm_box = SurroundingRectangle(
            VGroup(thm_title, thm_cond, thm_exact, thm_exact_lbl,
                   thm_norm, thm_norm_lbl, thm_bal, thm_bal_lbl),
            color=C_GOLD, stroke_width=2, buff=0.25, corner_radius=0.1
        )

        # ── Quadratic NN corollary ─────────────────────────────────────────────
        nn_note = Text(
            "Extension: Single hidden-layer NN (quadratic activation) — flat U_f recovers teacher U♯!",
            font_size=18, color=C_ORANGE,
        )
        nn_note.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(strat_lbl, shift=RIGHT * 0.15),
                  Write(strat_eq), run_time=1.0)
        self.wait(0.3)
        self.play(FadeIn(thm_title), run_time=0.5)
        self.play(Write(thm_cond), run_time=0.8)
        self.play(Write(thm_exact), FadeIn(thm_exact_lbl), run_time=0.8)
        self.play(Write(thm_norm), FadeIn(thm_norm_lbl), run_time=0.8)
        self.play(Write(thm_bal), FadeIn(thm_bal_lbl), run_time=0.8)
        self.play(Create(thm_box), run_time=0.7)
        self.play(FadeIn(nn_note, shift=UP * 0.1), run_time=0.7)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  G7 – 2-LAYER ReLU NN + GD SETUP  (slides 38–41)
# ═══════════════════════════════════════════════════════════════════════════════
class G7_ReLUNNSetup(Scene):
    def construct(self):
        title = Text("2-Layer ReLU Neural Network Setup",
                     font_size=34, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        uline = Line(LEFT * 4.8, RIGHT * 4.8,
                     color=C_BLUE, stroke_width=2).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.2)

        # ── Network definition ─────────────────────────────────────────────────
        nn_lbl = Text("Function class:", font_size=22,
                       color=C_WHITE, weight=BOLD)
        nn_eq  = MathTex(
            r"\mathcal{F}=\left\{f(x)=\sum_{i=1}^{k}"
            r"w_i^{(2)}\varphi\!\left(w_i^{(1)}x+b_i^{(1)}\right)+b^{(2)}"
            r"\right\}",
            font_size=25, color=C_BLUE,
        )
        nn_lbl.shift(LEFT * 4.8 + UP * 1.7)
        nn_eq.next_to(nn_lbl, RIGHT, buff=0.3)

        relu_note = MathTex(
            r"\varphi = \text{ReLU} = \max(0,x),\quad k \gg n\;"
            r"(\text{overparameterized})",
            font_size=20, color=C_GRAY,
        )
        relu_note.next_to(nn_eq, DOWN, buff=0.15, aligned_edge=LEFT)

        # ── Loss ──────────────────────────────────────────────────────────────
        loss_lbl = Text("Square loss:", font_size=22,
                         color=C_WHITE, weight=BOLD)
        loss_eq  = MathTex(
            r"\mathcal{L}(\theta)=\frac{1}{2n}"
            r"\sum_{i=1}^{n}(f_\theta(x_i)-y_i)^2",
            font_size=26, color=C_WHITE,
        )
        loss_lbl.next_to(nn_lbl, DOWN, buff=0.85, aligned_edge=LEFT)
        loss_eq.next_to(loss_lbl, RIGHT, buff=0.3)

        # ── GD update ─────────────────────────────────────────────────────────
        gd_lbl = Text("Gradient Descent:", font_size=22,
                       color=C_GOLD, weight=BOLD)
        gd_eq  = MathTex(
            r"\theta_{t+1} = \theta_t - \eta\nabla\mathcal{L}(\theta_t)",
            font_size=28, color=C_WHITE,
        )
        gd_lbl.next_to(loss_lbl, DOWN, buff=0.7, aligned_edge=LEFT)
        gd_eq.next_to(gd_lbl, RIGHT, buff=0.3)

        # ── EoS / Low-curvature region ─────────────────────────────────────────
        eos_lbl = Text("GD trajectory stays in:", font_size=22,
                        color=C_PURPLE, weight=BOLD)
        eos_eq  = MathTex(
            r"\left\{f_\theta\;\middle|\;\lambda_{\max}"
            r"(\nabla^2\mathcal{L}(\theta))\le\frac{2}{\eta}\right\}",
            font_size=28, color=C_PURPLE,
        )
        eos_lbl.next_to(gd_lbl, DOWN, buff=0.7, aligned_edge=LEFT)
        eos_eq.next_to(eos_lbl, RIGHT, buff=0.3)

        eos_box = SurroundingRectangle(
            VGroup(eos_lbl, eos_eq), color=C_PURPLE,
            stroke_width=2, buff=0.2, corner_radius=0.1
        )

        gen_note = Text(
            "Tune η  =  control how 'flat' the solutions GD finds!",
            font_size=20, color=C_GOLD,
        )
        gen_note.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(nn_lbl, shift=RIGHT * 0.15),
                  Write(nn_eq), run_time=1.0)
        self.play(FadeIn(relu_note), run_time=0.5)
        self.wait(0.2)
        self.play(FadeIn(loss_lbl, shift=RIGHT * 0.15),
                  Write(loss_eq), run_time=0.9)
        self.wait(0.2)
        self.play(FadeIn(gd_lbl, shift=RIGHT * 0.15),
                  Write(gd_eq), run_time=0.9)
        self.wait(0.2)
        self.play(FadeIn(eos_lbl, shift=RIGHT * 0.15),
                  Write(eos_eq), run_time=0.9)
        self.play(Create(eos_box), run_time=0.6)
        self.play(FadeIn(gen_note, shift=UP * 0.1), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  G8 – FLATNESS IMPLIES TV CONSTRAINT  (slides 41–45)
# ═══════════════════════════════════════════════════════════════════════════════
class G8_TVConstraint(Scene):
    def construct(self):
        title = Text("Flatness (Parameter Space) → TV Constraint (Function Space)",
                     font_size=26, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        uline = Line(LEFT * 5.5, RIGHT * 5.5,
                     color=C_ORANGE, stroke_width=2).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.2)

        # ── Weighted TV1 class ─────────────────────────────────────────────────
        tv_def_lbl = Text("Weighted TV class:", font_size=22,
                           color=C_ORANGE, weight=BOLD)
        tv_def_eq  = MathTex(
            r"\mathrm{TV}_g^{(1)}(C)"
            r":=\left\{f\;\middle|\;"
            r"\int|f''(x)|\,g(x)\,dx\le C\right\}",
            font_size=26, color=C_WHITE,
        )
        tv_def_lbl.shift(LEFT * 3.5 + UP * 1.65)
        tv_def_eq.next_to(tv_def_lbl, RIGHT, buff=0.3)

        # ── Key containment ────────────────────────────────────────────────────
        contain_lbl = Text("Key containment (Qiao et al. 2024):", font_size=22,
                            color=C_GOLD, weight=BOLD)
        contain_lbl.next_to(tv_def_lbl, DOWN, buff=0.75, aligned_edge=LEFT)

        contain_eq = MathTex(
            r"\underbrace{\left\{f_\theta\mid"
            r"\lambda_{\max}(\nabla^2\mathcal{L}(\theta))\le2/\eta\right\}}"
            r"_{\text{EoS region}}"
            r"\;\subseteq\;"
            r"\underbrace{\mathrm{TV}_g^{(1)}(C)}_{\text{TV constraint}}",
            font_size=24, color=C_WHITE,
        )
        contain_eq.next_to(contain_lbl, DOWN, buff=0.28)

        c_val = MathTex(
            r"\text{where }\; C = \frac{2}{\eta} + \tilde{O}(1)",
            font_size=22, color=C_GOLD,
        )
        c_val.next_to(contain_eq, DOWN, buff=0.2)

        # ── Main bound ─────────────────────────────────────────────────────────
        bound_lbl = Text("Precise bound (noisy labels):", font_size=22,
                          color=C_GREEN, weight=BOLD)
        bound_lbl.next_to(contain_lbl, DOWN, buff=1.7, aligned_edge=LEFT)

        bound_eq = MathTex(
            r"\int|f''(x)|\,g(x)\,dx"
            r"\le\frac{\lambda_{\max}(\nabla^2_\theta\mathcal{L})}{2}"
            r"-\frac{1}{2}"
            r"+\tilde{O}\!\left(\sigma x_{\max}\cdot\min\!\left\{1,\sqrt{\frac{k}{n}}\right\}\right)"
            r"+x_{\max}\sqrt{\mathrm{MSE}(f)}",
            font_size=20, color=C_WHITE,
        )
        bound_eq.next_to(bound_lbl, DOWN, buff=0.22)

        bound_box = SurroundingRectangle(
            VGroup(bound_lbl, bound_eq), color=C_GREEN,
            stroke_width=2, buff=0.2, corner_radius=0.1
        )

        # ── Implication ────────────────────────────────────────────────────────
        imply_note = Text(
            "Tune learning rate  =>  select smoothness of f  =>  generalization bounds!",
            font_size=19, color=C_BLUE,
        )
        imply_note.to_edge(DOWN, buff=0.45)

        self.play(FadeIn(tv_def_lbl, shift=RIGHT * 0.15),
                  Write(tv_def_eq), run_time=1.0)
        self.wait(0.3)
        self.play(FadeIn(contain_lbl, shift=RIGHT * 0.15), run_time=0.6)
        self.play(Write(contain_eq), run_time=1.2)
        self.play(FadeIn(c_val), run_time=0.5)
        self.wait(0.3)
        self.play(FadeIn(bound_lbl, shift=RIGHT * 0.15),
                  Write(bound_eq), run_time=1.2)
        self.play(Create(bound_box), run_time=0.7)
        self.play(FadeIn(imply_note, shift=UP * 0.1), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  G9 – GENERALIZATION BOUNDS & FEATURE LEARNING  (slides 46–49)
# ═══════════════════════════════════════════════════════════════════════════════
class G9_GenBounds(Scene):
    def construct(self):
        title = Text("Generalization Bounds via Edge of Stability",
                     font_size=32, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        uline = Line(LEFT * 5.5, RIGHT * 5.5,
                     color=C_GREEN, stroke_width=2).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.2)

        # ── U-shape risk curve ─────────────────────────────────────────────────
        ax = Axes(
            x_range=[0, 6.5, 1], y_range=[-0.05, 1.2, 0.5],
            x_length=5.0, y_length=2.4,
            axis_config={"color": C_GRAY, "stroke_width": 1.2,
                         "include_tip": True},
        ).shift(LEFT * 3.5 + DOWN * 0.5)

        def mse_curve(inv_eta):
            # U-shape: large η (small 1/η) = better, very large η = worse
            x = inv_eta
            return 0.18 + 0.08 * (x - 2) ** 2 / 5 if x > 2 else \
                   0.18 + 0.25 * (2 - x) ** 2 / 4

        mse_curve_plot = ax.plot(
            lambda x: mse_curve(x),
            x_range=[0.1, 6.2, 0.05],
            color=C_ORANGE, stroke_width=2.5,
        )

        opt_line = DashedLine(
            ax.c2p(2.0, -0.05), ax.c2p(2.0, mse_curve(2.0) + 0.05),
            color=C_GOLD, stroke_width=1.8, dash_length=0.1,
        )
        opt_dot  = Dot(ax.c2p(2.0, mse_curve(2.0)), color=C_GOLD, radius=0.1)
        opt_lbl  = MathTex(r"\eta^*", font_size=18, color=C_GOLD)
        opt_lbl.next_to(ax.c2p(2.0, -0.05), DOWN, buff=0.15)

        x_lbl_ax = MathTex(r"1/\eta", font_size=16, color=C_GRAY)
        x_lbl_ax.next_to(ax.x_axis, DOWN, buff=0.3)
        y_lbl_ax = Text("MSE", font_size=16, color=C_GRAY)
        y_lbl_ax.rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.3)
        u_lbl    = Text("U-shape risk curve", font_size=15, color=C_ORANGE, weight=BOLD)
        u_lbl.next_to(ax, UP, buff=0.15)

        self.play(Create(ax), FadeIn(x_lbl_ax), FadeIn(y_lbl_ax),
                  FadeIn(u_lbl), run_time=0.8)
        self.play(Create(mse_curve_plot, rate_func=linear), run_time=1.5)
        self.play(Create(opt_line), FadeIn(opt_dot), FadeIn(opt_lbl), run_time=0.7)
        self.wait(0.3)

        # ── Main theorem ───────────────────────────────────────────────────────
        thm_lbl = Text("Main generalization bound:", font_size=22,
                        color=C_GOLD, weight=BOLD)
        thm_lbl.shift(RIGHT * 1.5 + UP * 1.7)

        thm_eq = MathTex(
            r"\mathrm{MSE}_\mathcal{I}(f)"
            r"\le\tilde{O}\!\left("
            r"\left(\frac{\sigma^2}{n_\mathcal{I}}\right)^{\!4/5}"
            r"\left(\frac{x_{\max}}{\eta}+\sigma x_{\max}^2\right)^{\!2/5}"
            r"\right)",
            font_size=22, color=C_WHITE,
        )
        thm_eq.next_to(thm_lbl, DOWN, buff=0.22)

        thm_box = SurroundingRectangle(
            VGroup(thm_lbl, thm_eq), color=C_GOLD,
            stroke_width=2, buff=0.22, corner_radius=0.1
        )

        optimal_note = MathTex(
            r"\text{Optimal } \eta \Rightarrow \mathrm{MSE} = O(n^{-4/5})",
            font_size=20, color=C_GREEN,
        )
        optimal_note.next_to(thm_box, DOWN, buff=0.25)

        self.play(FadeIn(thm_lbl), Write(thm_eq), run_time=1.0)
        self.play(Create(thm_box), run_time=0.6)
        self.play(FadeIn(optimal_note), run_time=0.6)
        self.wait(0.3)

        # ── Comparison table ───────────────────────────────────────────────────
        tbl_title = Text("Comparison:", font_size=20, color=C_WHITE, weight=BOLD)
        r1_a = Text("NN (optimally tuned η)", font_size=18, color=C_GREEN)
        r1_b = MathTex(r"O(n^{-4/5})", font_size=22, color=C_GREEN)
        r2_a = Text("Kernel regression (RKHS)", font_size=18, color=C_RED)
        r2_b = MathTex(r"\Omega(n^{-3/4})", font_size=22, color=C_RED)

        r1_a.move_to(RIGHT * 1.0 + DOWN * 1.0)
        r1_b.move_to(RIGHT * 4.2 + DOWN * 1.0)
        r2_a.move_to(RIGHT * 1.0 + DOWN * 1.5)
        r2_b.move_to(RIGHT * 4.2 + DOWN * 1.5)
        tbl_title.next_to(r1_a, UP, buff=0.25, aligned_edge=LEFT)

        sep_h = Line(LEFT * 0.2 + RIGHT * 5.5, RIGHT * 5.5,
                     color=C_GRAY, stroke_width=0.8).move_to(
            (r1_a.get_center() + r2_a.get_center()) / 2 + LEFT * 1.3
        )

        better = Text("NN beats Kernel!", font_size=18, color=C_GOLD, weight=BOLD)
        better.next_to(r2_b, RIGHT, buff=0.3)

        self.play(FadeIn(tbl_title), run_time=0.4)
        self.play(Write(r1_a), Write(r1_b), Create(sep_h), run_time=0.7)
        self.play(Write(r2_a), Write(r2_b), run_time=0.7)
        self.play(FadeIn(better), run_time=0.5)

        feat_note = Text(
            "Large η → few active neurons → sparse representation (feature learning)",
            font_size=18, color=C_PURPLE,
        )
        feat_note.to_edge(DOWN, buff=0.42)
        self.play(FadeIn(feat_note, shift=UP * 0.1), run_time=0.7)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  G10 – EXTENSIONS: LOGISTIC LOSS & OPEN PROBLEMS  (slides 50–65)
# ═══════════════════════════════════════════════════════════════════════════════
class G10_OpenProblems(Scene):
    def construct(self):
        title = Text("Extensions & Open Problems",
                     font_size=36, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        uline = Line(LEFT * 4.5, RIGHT * 4.5,
                     color=C_PURPLE, stroke_width=2).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.2)

        # ── Logistic extension ─────────────────────────────────────────────────
        log_title = Text("Extension 1: Logistic Loss", font_size=24,
                          color=C_GOLD, weight=BOLD)
        log_title.shift(LEFT * 3.5 + UP * 1.6)

        log_insuf = MathTex(
            r"\{f_\theta\mid\lambda_{\max}(\nabla^2\mathcal{L})\le2/\eta\}"
            r"\;\text{insufficient for generalization}",
            font_size=20, color=C_RED,
        )
        log_insuf.next_to(log_title, DOWN, buff=0.22)

        log_fix = MathTex(
            r"\{f_\theta\mid\lambda_{\max}\le2/\eta,\;"
            r"\|\theta\|=o(n)\}\;\text{works!}",
            font_size=20, color=C_GREEN,
        )
        log_fix.next_to(log_insuf, DOWN, buff=0.18)

        log_box = SurroundingRectangle(
            log_fix, color=C_GREEN, stroke_width=1.8,
            buff=0.15, corner_radius=0.08
        )

        self.play(FadeIn(log_title, shift=RIGHT * 0.15), run_time=0.6)
        self.play(Write(log_insuf), run_time=0.8)
        self.play(Write(log_fix), Create(log_box), run_time=0.9)
        self.wait(0.3)

        # ── High-dimensional: Neural Shattering ────────────────────────────────
        ns_title = Text("Extension 2: High Dimension — Neural Shattering",
                         font_size=22, color=C_ORANGE, weight=BOLD)
        ns_title.next_to(log_title, DOWN, buff=1.2, aligned_edge=LEFT)

        ns_items = BulletedList(
            "In high-dim: each neuron can single out one data point",
            "Result: catastrophic overfitting at boundaries",
            "Fix: weight decay  or  remove 'bias' parameters",
            font_size=18, color=C_WHITE, buff=0.2,
        )
        ns_items.next_to(ns_title, DOWN, buff=0.2)

        self.play(FadeIn(ns_title, shift=RIGHT * 0.15), run_time=0.6)
        for item in ns_items:
            self.play(FadeIn(item, shift=RIGHT * 0.1), run_time=0.5)
            self.wait(0.1)

        self.wait(0.3)

        # ── Open problems ──────────────────────────────────────────────────────
        open_title = Text("Open Problems:", font_size=22,
                           color=C_BLUE, weight=BOLD)
        open_title.next_to(ns_items, DOWN, buff=0.45)

        open_items = BulletedList(
            "Multi-layer networks (L>2): denser norms, different implicit bias",
            "Non-linear activations beyond ReLU (GELU, SiLU, ...)",
            "Convolutional / attention layers",
            "How does data geometry interact with large stepsize?",
            font_size=16, color=C_WHITE, buff=0.18,
        )
        open_items.next_to(open_title, RIGHT, buff=0.4)

        self.play(FadeIn(open_title, shift=RIGHT * 0.15), run_time=0.6)
        for item in open_items:
            self.play(FadeIn(item, shift=RIGHT * 0.1), run_time=0.45)
            self.wait(0.08)

        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  G11 – PART 2 CONCLUSION  (slides 65)
# ═══════════════════════════════════════════════════════════════════════════════
class G11_Conclusion(Scene):
    def construct(self):
        title = Text("Part 2 — Take-Aways",
                     font_size=40, color=C_GREEN, weight=BOLD)
        title.to_edge(UP, buff=0.55)
        uline = Line(LEFT * 3.5, RIGHT * 3.5,
                     color=C_GREEN, stroke_width=2.5).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.2)

        takeaways = [
            ("Large stepsize  →  flat minima  →  provable generalization",
             C_GOLD),
            ("Flat minima exactly recover ground truth in matrix sensing & quadratic NNs",
             C_BLUE),
            ("For ReLU NNs: flatness implies weighted TV constraint in function space",
             C_GREEN),
            ("Optimal MSE = O(n^{-4/5})  —  better than kernel methods!",
             C_PURPLE),
            ("Neural Shattering in high-dim: weight decay or no-bias helps",
             C_ORANGE),
        ]

        cards = VGroup()
        for txt, col in takeaways:
            bullet = Text("•", font_size=28, color=col, weight=BOLD)
            body   = Text(txt, font_size=22, color=C_WHITE)
            body.next_to(bullet, RIGHT, buff=0.22)
            cards.add(VGroup(bullet, body))

        cards.arrange(DOWN, aligned_edge=LEFT, buff=0.48)
        cards.next_to(uline, DOWN, buff=0.55)
        cards.shift(LEFT * 0.3)

        for card in cards:
            self.play(FadeIn(card, shift=RIGHT * 0.2), run_time=0.65)
            self.wait(0.15)

        self.wait(0.4)

        # ── Final message ──────────────────────────────────────────────────────
        final_box = RoundedRectangle(
            width=11.0, height=1.3, corner_radius=0.2,
            color=C_GOLD, fill_opacity=0.10, stroke_width=2,
        )
        final_txt = Text(
            "Large stepsize is not just about optimization — it shapes what GD learns!",
            font_size=22, color=C_GOLD, weight=BOLD,
        )
        final_txt.move_to(final_box)
        final_grp = VGroup(final_box, final_txt)
        final_grp.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(final_grp, shift=UP * 0.15), run_time=0.9)
        self.wait(3.0)
        self.play(FadeOut(*self.mobjects))
