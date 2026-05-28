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


# ───────────────────────────────────────────────────────────────────────────────
#  HELPER: simulate logistic regression GD loss
# ───────────────────────────────────────────────────────────────────────────────
def sim_logistic_gd(eta, T=8192, n=20, seed=42):
    """1-D multi-point separable logistic regression: y_i = x_i = positive."""
    np.random.seed(seed)
    x = np.abs(np.random.randn(n)) + 0.5   # positive features
    theta = 0.0
    losses = []
    for _ in range(T):
        margins = np.clip(x * theta, -500, 500)
        L = float(np.mean(np.log1p(np.exp(-margins))))
        losses.append(max(L, 1e-15))
        grad = -float(np.mean(x / (1.0 + np.exp(np.clip(margins, -500, 500)))))
        theta -= eta * grad
    return np.array(losses)


# ═══════════════════════════════════════════════════════════════════════════════
#  P1 – PART 1 OUTLINE  (slide 17)
# ═══════════════════════════════════════════════════════════════════════════════
class P1_Overview(Scene):
    def construct(self):
        badge = Text("Part 1: Optimization", font_size=26, color=C_BLUE, weight=BOLD)
        badge.to_edge(UP, buff=0.55)

        title = Text("What we'll cover", font_size=48, color=C_WHITE, weight=BOLD)
        title.next_to(badge, DOWN, buff=0.28)
        uline = Line(LEFT * 3.0, RIGHT * 3.0, color=C_GOLD, stroke_width=2.5)
        uline.next_to(title, DOWN, buff=0.1)

        entries = [
            ("①",
             "Review: Classical optimization theory",
             "Descent Lemma  ·  Convergence rates  ·  Acceleration",
             C_GREEN),
            ("②",
             "A modern take:",
             "Acceleration via large stepsizes",
             C_GOLD),
            ("③",
             "Summary, open problems, Q&A",
             "",
             C_BLUE),
        ]

        cards = VGroup()
        for icon, head, sub, col in entries:
            num_t = Text(icon, font_size=42, color=col, weight=BOLD)
            hd_t  = Text(head, font_size=27, color=C_WHITE, weight=BOLD)
            hd_t.next_to(num_t, RIGHT, buff=0.22)
            row = VGroup(num_t, hd_t)
            if sub:
                sub_t = Text(sub, font_size=20, color=C_GRAY)
                sub_t.next_to(hd_t, DOWN, buff=0.08, aligned_edge=LEFT)
                row.add(sub_t)
            cards.add(row)

        cards.arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        cards.next_to(uline, DOWN, buff=0.58)
        cards.shift(LEFT * 0.4)

        self.play(FadeIn(badge, shift=DOWN * 0.1), run_time=0.7)
        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.15)
        for card in cards:
            self.play(FadeIn(card, shift=RIGHT * 0.2), run_time=0.65)
            self.wait(0.12)

        focus_box = SurroundingRectangle(
            cards[1], color=C_GOLD, stroke_width=2, buff=0.2, corner_radius=0.1
        )
        focus_lbl = Text("← Main focus of this part",
                          font_size=19, color=C_GOLD)
        focus_lbl.next_to(focus_box, RIGHT, buff=0.22)

        self.wait(0.4)
        self.play(Create(focus_box), FadeIn(focus_lbl), run_time=0.8)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  P2 – DESCENT LEMMA (step-by-step proof)  (slide 18)
# ═══════════════════════════════════════════════════════════════════════════════
class P2_DescentLemma(Scene):
    def construct(self):
        title = Text("Descent Lemma", font_size=40, color=C_GOLD, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        uline = Line(title.get_left(), title.get_right(),
                     color=C_GOLD, stroke_width=2).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.2)

        # ── Step labels + equations ────────────────────────────────────────────
        label_kw = dict(weight=BOLD)

        lbl0 = Text("GD step:", font_size=20, color=C_GREEN, **label_kw)
        eq0  = MathTex(
            r"\theta_{+} = \theta - \eta \nabla L(\theta)",
            font_size=36, color=C_WHITE,
        )

        lbl1 = Text("Taylor remainder:", font_size=20, color=C_BLUE, **label_kw)
        eq1  = MathTex(
            r"L(\theta_{+}) \le L(\theta)"
            r"+ \nabla L(\theta)^\top(\theta_{+}-\theta)"
            r"+ \tfrac{1}{2}\|\theta_{+}-\theta\|^2\|\nabla^2 L(\nu)\|",
            font_size=24, color=C_WHITE,
        )

        lbl2 = Text("Substitute GD step:", font_size=20, color=C_PURPLE, **label_kw)
        eq2  = MathTex(
            r"= L(\theta) - \eta\|\nabla L(\theta)\|^2"
            r"+ \tfrac{\eta^2}{2}\|\nabla L(\theta)\|^2\|\nabla^2 L(\nu)\|",
            font_size=24, color=C_WHITE,
        )

        lbl3 = Text("Factor out:", font_size=20, color=C_ORANGE, **label_kw)
        eq3  = MathTex(
            r"= L(\theta) - \eta\|\nabla L(\theta)\|^2"
            r"\!\left(1 - \tfrac{\eta}{2}\|\nabla^2 L(\nu)\|\right)",
            font_size=26, color=C_WHITE,
        )

        steps = VGroup()
        for lbl, eq in [(lbl0, eq0), (lbl1, eq1), (lbl2, eq2), (lbl3, eq3)]:
            eq.next_to(lbl, RIGHT, buff=0.28)
            steps.add(VGroup(lbl, eq))

        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        steps.next_to(uline, DOWN, buff=0.5)
        steps.shift(LEFT * 1.1)

        for step in steps:
            self.play(FadeIn(step[0], shift=RIGHT * 0.15),
                      Write(step[1]), run_time=0.95)
            self.wait(0.22)

        self.wait(0.3)

        # ── Key condition ──────────────────────────────────────────────────────
        cond_eq = MathTex(
            r"\eta < \frac{2}{\sup_\theta\|\nabla^2 L(\theta)\|}",
            font_size=40, color=C_GOLD,
        )
        cond_eq.to_edge(DOWN, buff=0.82)
        cond_box = SurroundingRectangle(
            cond_eq, color=C_GOLD, stroke_width=2.2, buff=0.28, corner_radius=0.1
        )
        cond_note = Text("⟹  guaranteed descent at every step!",
                          font_size=21, color=C_GREEN)
        cond_note.next_to(cond_box, RIGHT, buff=0.3)

        self.play(Write(cond_eq), Create(cond_box), run_time=1.0)
        self.play(FadeIn(cond_note, shift=LEFT * 0.1), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  P3 – CONVERGENCE RATES (classical)  (slide 19)
# ═══════════════════════════════════════════════════════════════════════════════
class P3_ConvergenceRates(Scene):
    def construct(self):
        title = Text("Convergence Rates of Gradient Descent",
                     font_size=34, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        uline = Line(LEFT * 5.5, RIGHT * 5.5,
                     color=C_BLUE, stroke_width=2).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.25)

        # ── Column headers ─────────────────────────────────────────────────────
        hdr_asmp = Text("Assumption", font_size=24, color=C_GOLD, weight=BOLD)
        hdr_rate = Text("Iterations to reach ε", font_size=24,
                         color=C_GOLD, weight=BOLD)
        hdr_asmp.move_to(LEFT * 2.8 + UP * 1.55)
        hdr_rate.move_to(RIGHT * 2.2 + UP * 1.55)

        hdr_line = Line(LEFT * 5.5, RIGHT * 5.5,
                        color=C_GRAY, stroke_width=1.2)
        hdr_line.next_to(hdr_asmp, DOWN, buff=0.22)

        self.play(FadeIn(hdr_asmp), FadeIn(hdr_rate), Create(hdr_line), run_time=0.8)

        # ── Table rows ─────────────────────────────────────────────────────────
        row_data = [
            (r"L\text{-smooth (non-convex)}",
             r"O\!\left(\tfrac{1}{\epsilon}\right)",
             C_BLUE),
            (r"L\text{-smooth + convex}",
             r"O\!\left(\tfrac{1}{\epsilon}\right)",
             C_GREEN),
            (r"L\text{-smooth} + \alpha\text{-strongly convex}\ \left(\kappa=\tfrac{L}{\alpha}\right)",
             r"O\!\left(\kappa\log\tfrac{1}{\epsilon}\right)",
             C_PURPLE),
        ]

        rows_grp = VGroup()
        y_base = hdr_line.get_center()[1]
        for i, (asmp_tex, rate_tex, col) in enumerate(row_data):
            a_eq = MathTex(asmp_tex, font_size=23, color=col)
            r_eq = MathTex(rate_tex, font_size=28, color=col)
            a_eq.move_to([hdr_asmp.get_center()[0], y_base - 0.80 - 0.92 * i, 0])
            r_eq.move_to([hdr_rate.get_center()[0], y_base - 0.80 - 0.92 * i, 0])
            rows_grp.add(VGroup(a_eq, r_eq))

        for row in rows_grp:
            self.play(Write(row[0]), Write(row[1]), run_time=0.9)
            self.wait(0.2)

        # Highlight κ log(1/ε) row
        sc_box = SurroundingRectangle(
            rows_grp[2], color=C_PURPLE, stroke_width=1.8,
            buff=0.18, corner_radius=0.08
        )
        sc_note = Text("Linear convergence — exponential speedup over non-strongly-convex!",
                        font_size=19, color=C_PURPLE)
        sc_note.next_to(sc_box, DOWN, buff=0.25)

        self.play(Create(sc_box), FadeIn(sc_note), run_time=0.8)
        self.wait(0.4)

        # ── Nesterov acceleration ──────────────────────────────────────────────
        nesterov_title = Text("Nesterov Acceleration:", font_size=24,
                               color=C_GOLD, weight=BOLD)
        nesterov_title.to_edge(DOWN, buff=1.75)

        na_convex = MathTex(
            r"\text{convex} \;\Rightarrow\; O\!\left(\tfrac{1}{\sqrt{\epsilon}}\right)",
            font_size=25, color=C_GREEN,
        )
        na_sc = MathTex(
            r"\alpha\text{-strongly convex} \;\Rightarrow\; "
            r"O\!\left(\sqrt{\kappa}\log\tfrac{1}{\epsilon}\right)",
            font_size=25, color=C_PURPLE,
        )
        na_group = VGroup(na_convex, na_sc).arrange(RIGHT, buff=0.8)
        na_group.next_to(nesterov_title, RIGHT, buff=0.5)

        self.play(FadeIn(nesterov_title), FadeIn(na_group), run_time=0.9)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  P4 – NESTEROV ACCELERATION  (slide 21)
# ═══════════════════════════════════════════════════════════════════════════════
class P4_Acceleration(Scene):
    def construct(self):
        title = Text("Nesterov Acceleration", font_size=38,
                     color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        uline = Line(LEFT * 3.5, RIGHT * 3.5,
                     color=C_PURPLE, stroke_width=2).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.25)

        # ── Algorithm boxes ────────────────────────────────────────────────────
        gd_title = Text("Gradient Descent (GD)", font_size=24,
                         color=C_BLUE, weight=BOLD)
        gd_eq = MathTex(
            r"\theta_{t+1} = \theta_t - \eta \nabla L(\theta_t)",
            font_size=30, color=C_WHITE,
        )
        gd_rate = MathTex(
            r"\text{convex: } O\!\left(\tfrac{1}{\epsilon}\right)\;"
            r"\text{s.c.: } O\!\left(\kappa\log\tfrac{1}{\epsilon}\right)",
            font_size=22, color=C_BLUE,
        )
        gd_box_inner = VGroup(gd_title, gd_eq, gd_rate).arrange(DOWN, buff=0.25)
        gd_box = SurroundingRectangle(
            gd_box_inner, color=C_BLUE, fill_opacity=0.06,
            stroke_width=2, buff=0.3, corner_radius=0.15
        )
        gd_group = VGroup(gd_box, gd_box_inner)
        gd_group.shift(LEFT * 3.2 + DOWN * 0.2)

        nes_title = Text("Nesterov Momentum", font_size=24,
                          color=C_PURPLE, weight=BOLD)
        nes_eq1 = MathTex(
            r"\theta_{t+1} = \nu_t - \eta \nabla L(\nu_t)",
            font_size=28, color=C_WHITE,
        )
        nes_eq2 = MathTex(
            r"\nu_{t+1} = \theta_{t+1} + \beta_t(\theta_{t+1} - \theta_t)",
            font_size=26, color=C_WHITE,
        )
        nes_rate = MathTex(
            r"\text{convex: } O\!\left(\tfrac{1}{\sqrt{\epsilon}}\right)\;"
            r"\text{s.c.: } O\!\left(\sqrt{\kappa}\log\tfrac{1}{\epsilon}\right)",
            font_size=22, color=C_PURPLE,
        )
        nes_box_inner = VGroup(nes_title, nes_eq1, nes_eq2, nes_rate
                               ).arrange(DOWN, buff=0.22)
        nes_box = SurroundingRectangle(
            nes_box_inner, color=C_PURPLE, fill_opacity=0.06,
            stroke_width=2, buff=0.3, corner_radius=0.15
        )
        nes_group = VGroup(nes_box, nes_box_inner)
        nes_group.shift(RIGHT * 3.0 + DOWN * 0.2)

        # ── VS label ──────────────────────────────────────────────────────────
        vs_txt = Text("vs", font_size=28, color=C_GRAY)
        vs_txt.move_to(ORIGIN + DOWN * 0.2)

        self.play(FadeIn(gd_group, shift=RIGHT * 0.3), run_time=0.9)
        self.wait(0.2)
        self.play(FadeIn(vs_txt), run_time=0.4)
        self.play(FadeIn(nes_group, shift=LEFT * 0.3), run_time=0.9)
        self.wait(0.4)

        # ── Speedup annotations ────────────────────────────────────────────────
        speedup_arr = Arrow(
            gd_rate.get_right() + RIGHT * 0.1,
            nes_rate.get_left()  + LEFT  * 0.1,
            color=C_GOLD, stroke_width=2.5, buff=0.05,
            max_tip_length_to_length_ratio=0.2,
        )
        speedup_arr.move_to(ORIGIN + DOWN * 1.8)

        speedup_lbl = Text("√κ speedup!", font_size=22, color=C_GOLD, weight=BOLD)
        speedup_lbl.next_to(speedup_arr, UP, buff=0.15)

        self.play(GrowArrow(speedup_arr), FadeIn(speedup_lbl), run_time=0.9)
        self.wait(0.4)

        # ── "Hard case" note ──────────────────────────────────────────────────
        note = Text('Hard case: quadratics in high dimensions',
                    font_size=21, color=C_ORANGE)
        note.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  P5 – FROM SMALL TO LARGE STEPSIZE  (slide 22)
# ═══════════════════════════════════════════════════════════════════════════════
class P5_LargeStepsize(Scene):
    def construct(self):
        title = Text("From Small to Large Stepsize",
                     font_size=36, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        uline = Line(LEFT * 4.0, RIGHT * 4.0,
                     color=C_GOLD, stroke_width=2).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.2)

        # ── Stepsize axis ──────────────────────────────────────────────────────
        eta_axis = Arrow(LEFT * 5.0, RIGHT * 5.0,
                         color=C_GRAY, stroke_width=2.5, buff=0)
        eta_axis.shift(UP * 1.0)
        eta_lbl = MathTex(r"\eta", font_size=32, color=C_WHITE)
        eta_lbl.next_to(eta_axis, RIGHT, buff=0.15)

        zero_lbl = Text("0", font_size=18, color=C_GRAY)
        zero_lbl.next_to(eta_axis.get_left(), DOWN, buff=0.15)

        threshold_line = DashedLine(
            eta_axis.get_center() + DOWN * 1.8,
            eta_axis.get_center() + UP   * 0.2,
            color=C_RED, stroke_width=2, dash_length=0.12,
        )
        threshold_lbl = MathTex(
            r"\frac{2}{\lambda_{\max}}",
            font_size=26, color=C_RED
        )
        threshold_lbl.next_to(threshold_line, UP, buff=0.1)

        # Left box: theory
        theory_box = RoundedRectangle(
            width=4.2, height=2.4, corner_radius=0.2,
            color=C_BLUE, fill_opacity=0.08, stroke_width=2
        )
        theory_box.shift(LEFT * 3.3 + DOWN * 1.0)
        theory_hd   = Text("Classical Theory", font_size=22,
                            color=C_BLUE, weight=BOLD)
        theory_hd.next_to(theory_box.get_top(), DOWN, buff=0.22)
        theory_cond = MathTex(
            r"\eta < \frac{2}{\lambda_{\max}(\nabla^2 L)}",
            font_size=24, color=C_WHITE,
        )
        theory_cond.next_to(theory_hd, DOWN, buff=0.22)
        theory_items = BulletedList(
            "Guaranteed descent",
            r"Rate $O(\kappa/t)$",
            font_size=18, color=C_WHITE, buff=0.2,
        )
        theory_items.next_to(theory_cond, DOWN, buff=0.18)

        # Right box: practice
        prac_box = RoundedRectangle(
            width=4.2, height=2.4, corner_radius=0.2,
            color=C_GREEN, fill_opacity=0.08, stroke_width=2
        )
        prac_box.shift(RIGHT * 3.3 + DOWN * 1.0)
        prac_hd = Text("Practice (EoS)", font_size=22,
                        color=C_GREEN, weight=BOLD)
        prac_hd.next_to(prac_box.get_top(), DOWN, buff=0.22)
        prac_cond = MathTex(
            r"\eta > \frac{2}{\lambda_{\max}(\nabla^2 L)}",
            font_size=24, color=C_WHITE,
        )
        prac_cond.next_to(prac_hd, DOWN, buff=0.22)
        prac_items = BulletedList(
            "Edge of Stability",
            r"Rate $\tilde{O}(1/(\eta t))$",
            font_size=18, color=C_WHITE, buff=0.2,
        )
        prac_items.next_to(prac_cond, DOWN, buff=0.18)

        # Gap arrow
        gap_arr = DoubleArrow(
            theory_box.get_right(), prac_box.get_left(),
            color=C_GOLD, stroke_width=2.2, buff=0.1,
            max_tip_length_to_length_ratio=0.15,
        )
        gap_lbl = Text("Theory gap", font_size=19, color=C_GOLD)
        gap_lbl.next_to(gap_arr, UP, buff=0.12)

        # "Does not exist for quadratics" note
        quad_note = Text(
            "For quadratic loss: no extra benefit from large η!",
            font_size=20, color=C_RED
        )
        quad_note.to_edge(DOWN, buff=0.38)

        self.play(
            Create(eta_axis), FadeIn(eta_lbl),
            FadeIn(zero_lbl), run_time=0.8
        )
        self.play(
            Create(threshold_line), FadeIn(threshold_lbl), run_time=0.7
        )
        self.play(
            FadeIn(VGroup(theory_box, theory_hd, theory_cond, theory_items),
                   shift=RIGHT * 0.2),
            run_time=0.9,
        )
        self.play(
            FadeIn(VGroup(prac_box, prac_hd, prac_cond, prac_items),
                   shift=LEFT * 0.2),
            run_time=0.9,
        )
        self.play(GrowArrow(gap_arr), FadeIn(gap_lbl), run_time=0.8)
        self.wait(0.4)
        self.play(FadeIn(quad_note, shift=UP * 0.1), run_time=0.7)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  P6 – MENTAL MODEL SPECTRUM  (slide 23)
# ═══════════════════════════════════════════════════════════════════════════════
class P6_MentalModel(Scene):
    def construct(self):
        title = Text("Alternative Mental Model", font_size=36,
                     color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        uline = Line(LEFT * 3.8, RIGHT * 3.8,
                     color=C_BLUE, stroke_width=2).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.2)

        # ── Spectrum arrow ─────────────────────────────────────────────────────
        spec_arr = Arrow(LEFT * 5.2, RIGHT * 5.2,
                         color=C_GRAY, stroke_width=2, buff=0)
        spec_arr.shift(UP * 0.7)
        spec_lbl = Text("Complexity / Non-linearity", font_size=19, color=C_GRAY)
        spec_lbl.next_to(spec_arr, RIGHT, buff=0.1)

        # ── 3 models ───────────────────────────────────────────────────────────
        models = [
            (LEFT * 4.0,  "Linear\nRegression",   C_BLUE,
             "Quadratic loss\nη < 2/λ_max strictly needed",
             lambda x: x**2),
            (ORIGIN,      "Logistic\nRegression",  C_GOLD,
             "Self-bounded:\n‖∇²L‖ ≤ L(θ)\nLarge η → 2-phase!",
             lambda x: np.log1p(np.exp(-x*3))),
            (RIGHT * 4.0, "Deep\nLearning",        C_GREEN,
             "Complex landscape\nEoS observed empirically",
             lambda x: 0.4*np.sin(2*x)*np.exp(-0.1*x**2) + 0.8*x**2*0.05),
        ]

        x_vals = np.linspace(-2, 2, 100)
        model_groups = VGroup()

        for center, label, col, desc, fn in models:
            # Mini axes
            mini_ax = Axes(
                x_range=[-2.2, 2.2, 1], y_range=[-0.1, 1.5, 0.5],
                x_length=2.6, y_length=1.6,
                axis_config={"color": C_GRAY, "stroke_width": 1},
                x_axis_config={"include_tip": False},
                y_axis_config={"include_tip": False},
            )
            y_vals = fn(x_vals)
            y_min, y_max = y_vals.min(), y_vals.max()
            if y_max > y_min:
                y_norm = (y_vals - y_min) / (y_max - y_min) * 1.3 + 0.05
            else:
                y_norm = np.ones_like(y_vals) * 0.5

            curve = mini_ax.plot(
                lambda x, fv=fn, ymin=y_min, ymax=y_max: (
                    (fv(x) - ymin) / (ymax - ymin) * 1.3 + 0.05
                    if ymax > ymin else 0.5
                ),
                x_range=[-2.0, 2.0, 0.05],
                color=col, stroke_width=2.5,
            )
            name_txt = Text(label, font_size=20, color=col, weight=BOLD)
            name_txt.next_to(mini_ax, UP, buff=0.18)
            desc_txt = Text(desc, font_size=15, color=C_WHITE)
            desc_txt.next_to(mini_ax, DOWN, buff=0.18)

            g = VGroup(mini_ax, curve, name_txt, desc_txt)
            g.move_to(center + DOWN * 0.5)
            model_groups.add(g)

        self.play(Create(spec_arr), FadeIn(spec_lbl), run_time=0.8)
        for g in model_groups:
            self.play(FadeIn(g, shift=UP * 0.2), run_time=0.85)
            self.wait(0.15)

        # Highlight logistic
        focus = SurroundingRectangle(
            model_groups[1], color=C_GOLD, stroke_width=2.2,
            buff=0.2, corner_radius=0.12
        )
        focus_note = Text("Our case study", font_size=19, color=C_GOLD)
        focus_note.next_to(focus, DOWN, buff=0.15)
        self.play(Create(focus), FadeIn(focus_note), run_time=0.7)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  P7 – LOGISTIC REGRESSION SETUP  (slides 24–25)
# ═══════════════════════════════════════════════════════════════════════════════
class P7_LogisticSetup(Scene):
    def construct(self):
        title = Text("Case Study: Logistic Regression",
                     font_size=34, color=C_GOLD, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        uline = Line(LEFT * 4.5, RIGHT * 4.5,
                     color=C_GOLD, stroke_width=2).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.2)

        # ── Loss definition ────────────────────────────────────────────────────
        loss_lbl = Text("Loss function:", font_size=22,
                         color=C_WHITE, weight=BOLD)
        loss_eq  = MathTex(
            r"L(\theta) = \frac{1}{n}\sum_{i=1}^{n}"
            r"\ln\!\left(1 + e^{-y_i x_i^\top \theta}\right)",
            font_size=34, color=C_BLUE,
        )
        loss_lbl.shift(LEFT * 4.5 + UP * 1.6)
        loss_eq.next_to(loss_lbl, RIGHT, buff=0.3)

        # ── Key properties ─────────────────────────────────────────────────────
        prop1_lbl = Text("Self-bounded curvature:", font_size=20,
                          color=C_GREEN, weight=BOLD)
        prop1_eq  = MathTex(
            r"\|\nabla^2 L(\theta)\| \le L(\theta)",
            font_size=30, color=C_WHITE,
        )
        prop1_lbl.next_to(loss_lbl, DOWN, buff=0.7, aligned_edge=LEFT)
        prop1_eq.next_to(prop1_lbl, RIGHT, buff=0.28)

        prop2_lbl = Text("Minimizer at infinity:", font_size=20,
                          color=C_PURPLE, weight=BOLD)
        prop2_eq  = MathTex(
            r"\theta^* \to \infty \quad \text{(separable data)}",
            font_size=28, color=C_WHITE,
        )
        prop2_lbl.next_to(prop1_lbl, DOWN, buff=0.6, aligned_edge=LEFT)
        prop2_eq.next_to(prop2_lbl, RIGHT, buff=0.28)

        prop3_lbl = Text("Classical theory:", font_size=20,
                          color=C_BLUE, weight=BOLD)
        prop3_eq  = MathTex(
            r"\text{Rate } O\!\left(\tfrac{1}{t}\right)"
            r"\text{ for small } \eta",
            font_size=28, color=C_WHITE,
        )
        prop3_lbl.next_to(prop2_lbl, DOWN, buff=0.6, aligned_edge=LEFT)
        prop3_eq.next_to(prop3_lbl, RIGHT, buff=0.28)

        # ── Key insight box ────────────────────────────────────────────────────
        insight = MathTex(
            r"\|\nabla^2 L(\theta)\| \le L(\theta)"
            r"\;\Rightarrow\;"
            r"\text{stepsize adapts as loss decreases!}",
            font_size=26, color=C_GOLD,
        )
        insight.to_edge(DOWN, buff=0.82)
        insight_box = SurroundingRectangle(
            insight, color=C_GOLD, stroke_width=2, buff=0.22, corner_radius=0.1
        )

        self.play(FadeIn(loss_lbl, shift=RIGHT * 0.15),
                  Write(loss_eq), run_time=1.0)
        self.wait(0.2)
        self.play(FadeIn(prop1_lbl, shift=RIGHT * 0.15),
                  Write(prop1_eq), run_time=0.9)
        self.wait(0.2)
        self.play(FadeIn(prop2_lbl, shift=RIGHT * 0.15),
                  Write(prop2_eq), run_time=0.9)
        self.wait(0.2)
        self.play(FadeIn(prop3_lbl, shift=RIGHT * 0.15),
                  Write(prop3_eq), run_time=0.9)
        self.wait(0.3)
        self.play(Write(insight), Create(insight_box), run_time=1.0)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  P8 – TWO-PHASE BEHAVIOR (log-log loss curves)  (slides 25–26)
# ═══════════════════════════════════════════════════════════════════════════════
class P8_TwoPhases(Scene):
    def construct(self):
        title = Text("Two-Phase Behavior of GD on Logistic Regression",
                     font_size=28, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.38)

        self.play(Write(title), run_time=0.8)
        self.wait(0.2)

        # ── Pre-compute losses (log2 scale) ────────────────────────────────────
        T = 8192
        etas = [1.0, 0.25, 0.0625, 0.015625]  # 2^0, 2^{-2}, 2^{-4}, 2^{-6}
        eta_labels = [r"\eta=2^{0}", r"\eta=2^{-2}",
                      r"\eta=2^{-4}", r"\eta=2^{-6}"]
        colors = [C_RED, C_ORANGE, C_GREEN, C_BLUE]

        log2_losses = {}
        for eta in etas:
            raw = sim_logistic_gd(eta, T=T)
            log2_losses[eta] = np.log2(np.maximum(raw, 1e-15))

        # Sample at t = 2^k for k in [1..13]
        k_vals = np.arange(1, 14)
        t_samples = (2 ** k_vals).astype(int) - 1  # 0-indexed

        # ── Axes (log-log scale displayed as linear in k and j) ───────────────
        ax = Axes(
            x_range=[1, 13, 2],
            y_range=[-14, 7, 7],
            x_length=9.5, y_length=5.0,
            axis_config={"color": C_GRAY, "stroke_width": 1.5},
            x_axis_config={"include_tip": True},
            y_axis_config={"include_tip": True},
        ).shift(DOWN * 0.5 + LEFT * 0.3)

        # Custom tick labels for x
        x_tick_labs = VGroup(*[
            MathTex(f"2^{{{k}}}", font_size=14, color=C_GRAY)
            .next_to(ax.c2p(k, -14), DOWN, buff=0.15)
            for k in [1, 3, 5, 7, 9, 11, 13]
        ])
        # Custom tick labels for y
        y_tick_labs = VGroup(*[
            MathTex(f"2^{{{j}}}", font_size=14, color=C_GRAY)
            .next_to(ax.c2p(1, j), LEFT, buff=0.15)
            for j in [-14, -7, 0, 7]
        ])

        x_axis_lbl = Text("Iterations t", font_size=18, color=C_GRAY)
        x_axis_lbl.next_to(ax.x_axis, DOWN, buff=0.5)
        y_axis_lbl = Text("Loss L(θ_t)", font_size=18, color=C_GRAY)
        y_axis_lbl.rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.55)

        self.play(
            Create(ax),
            FadeIn(x_tick_labs), FadeIn(y_tick_labs),
            FadeIn(x_axis_lbl), FadeIn(y_axis_lbl),
            run_time=1.2,
        )

        # ── Plot each curve ────────────────────────────────────────────────────
        legend_items = []
        curves = VGroup()
        for eta, col, eta_lbl in zip(etas, colors, eta_labels):
            y_vals = log2_losses[eta][t_samples]
            pts = [ax.c2p(k, float(y)) for k, y in zip(k_vals, y_vals)]
            curve = VMobject(color=col, stroke_width=2.5)
            curve.set_points_as_corners(pts)
            curves.add(curve)

            dot = Dot(color=col, radius=0.07)
            lbl = MathTex(eta_lbl, font_size=20, color=col)
            lbl.next_to(dot, RIGHT, buff=0.12)
            legend_items.append(VGroup(dot, lbl))

        legend = VGroup(*legend_items).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        legend.to_corner(UR, buff=0.5)

        self.play(FadeIn(legend), run_time=0.5)
        self.play(
            *[Create(c, rate_func=linear) for c in curves],
            run_time=4.0,
        )
        self.wait(0.4)

        # ── Annotate two phases ────────────────────────────────────────────────
        # Unstable phase bracket (for large η red curve)
        tau_k = 6  # approximate phase transition for η=1 around t=2^6
        phase_line = DashedLine(
            ax.c2p(tau_k, -14), ax.c2p(tau_k, 7),
            color=C_GRAY, stroke_width=1.5, dash_length=0.15
        )
        unstable_lbl = Text("Unstable\nphase", font_size=17, color=C_ORANGE)
        unstable_lbl.next_to(ax.c2p(3, 6), ORIGIN, buff=0)
        stable_lbl = Text("Stable\nphase", font_size=17, color=C_GREEN)
        stable_lbl.next_to(ax.c2p(10, 6), ORIGIN, buff=0)

        self.play(
            Create(phase_line),
            FadeIn(unstable_lbl), FadeIn(stable_lbl),
            run_time=0.9,
        )
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  P9 – MAIN THEOREM: phase transition + rates  (slides 26–28)
# ═══════════════════════════════════════════════════════════════════════════════
class P9_MainTheorem(Scene):
    def construct(self):
        title = Text("Main Theorem: Large Stepsize on Logistic Regression",
                     font_size=28, color=C_GOLD, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        uline = Line(LEFT * 5.5, RIGHT * 5.5,
                     color=C_GOLD, stroke_width=2).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.2)

        # ── Phase transition ───────────────────────────────────────────────────
        pt_lbl = Text("Phase transition time:", font_size=22,
                       color=C_WHITE, weight=BOLD)
        pt_eq  = MathTex(
            r"\tau = \Theta\!\left(\max\left\{\eta,\,n,\,"
            r"\frac{n}{\eta}\ln\frac{n}{\eta}\right\}\right)",
            font_size=32, color=C_ORANGE,
        )
        pt_lbl.shift(LEFT * 3.0 + UP * 1.55)
        pt_eq.next_to(pt_lbl, RIGHT, buff=0.3)

        # ── Unstable phase ─────────────────────────────────────────────────────
        un_lbl = Text("Unstable phase  (t ≤ τ):", font_size=22,
                       color=C_RED, weight=BOLD)
        un_eq  = MathTex(
            r"L(\theta_t) = \tilde{O}\!\left(\frac{1+\eta^2}{\eta\,t}\right)",
            font_size=30, color=C_WHITE,
        )
        un_lbl.next_to(pt_lbl, DOWN, buff=0.72, aligned_edge=LEFT)
        un_eq.next_to(un_lbl, RIGHT, buff=0.3)

        # ── Stable phase ───────────────────────────────────────────────────────
        st_lbl = Text("Stable phase  (t > τ):", font_size=22,
                       color=C_GREEN, weight=BOLD)
        st_eq  = MathTex(
            r"L(\theta_{\tau+t}) = \tilde{O}\!\left(\frac{1}{\eta\,t}\right)",
            font_size=30, color=C_WHITE,
        )
        st_lbl.next_to(un_lbl, DOWN, buff=0.72, aligned_edge=LEFT)
        st_eq.next_to(st_lbl, RIGHT, buff=0.3)

        # ── Box around stable-phase rate ──────────────────────────────────────
        st_box = SurroundingRectangle(
            VGroup(st_lbl, st_eq), color=C_GREEN,
            stroke_width=2, buff=0.2, corner_radius=0.1
        )

        self.play(FadeIn(pt_lbl, shift=RIGHT * 0.15),
                  Write(pt_eq), run_time=1.0)
        self.wait(0.3)
        self.play(FadeIn(un_lbl, shift=RIGHT * 0.15),
                  Write(un_eq), run_time=0.9)
        self.wait(0.3)
        self.play(FadeIn(st_lbl, shift=RIGHT * 0.15),
                  Write(st_eq), run_time=0.9)
        self.play(Create(st_box), run_time=0.6)
        self.wait(0.4)

        # ── 3 Key effects ──────────────────────────────────────────────────────
        effects_title = Text("Effects of large stepsize:", font_size=22,
                              color=C_WHITE, weight=BOLD)
        effects_title.shift(LEFT * 3.2 + DOWN * 2.0)

        effects = [
            ("① ",
             r"\tilde{O}(1/(\eta t))\text{ stable rate — faster for larger }\eta",
             C_GREEN),
            ("② ",
             r"\text{Phase transition } \tau = \Theta(\eta)\text{ (longer for larger }\eta\text{)}",
             C_ORANGE),
            ("③ ",
             r"\text{Lower bound: } \Omega(1/t)\text{ — cannot do better!}",
             C_RED),
        ]

        eff_group = VGroup()
        for icon, tex, col in effects:
            icon_t = Text(icon, font_size=20, color=col, weight=BOLD)
            eq     = MathTex(tex, font_size=20, color=col)
            eq.next_to(icon_t, RIGHT, buff=0.08)
            eff_group.add(VGroup(icon_t, eq))
        eff_group.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        eff_group.next_to(effects_title, DOWN, buff=0.28)

        self.play(FadeIn(effects_title), run_time=0.6)
        for eff in eff_group:
            self.play(FadeIn(eff, shift=RIGHT * 0.15), run_time=0.6)
            self.wait(0.15)

        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  P10 – ADAPTIVE GRADIENT DESCENT  (slides 30–32)
# ═══════════════════════════════════════════════════════════════════════════════
class P10_AdaptiveGD(Scene):
    def construct(self):
        title = Text("Adaptive Gradient Descent (Adaptive GD)",
                     font_size=34, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        uline = Line(LEFT * 4.8, RIGHT * 4.8,
                     color=C_PURPLE, stroke_width=2).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.2)

        # ── Algorithm ─────────────────────────────────────────────────────────
        alg_lbl = Text("Update rule:", font_size=22,
                        color=C_WHITE, weight=BOLD)
        alg_eq  = MathTex(
            r"\theta_{t+1} \approx \theta_t - "
            r"\frac{\eta}{L(\theta_t)}\nabla L(\theta_t)",
            font_size=36, color=C_PURPLE,
        )
        alg_lbl.shift(LEFT * 4.2 + UP * 1.7)
        alg_eq.next_to(alg_lbl, RIGHT, buff=0.3)

        alg_note = Text("Normalises stepsize by current loss — adapts to the landscape",
                         font_size=19, color=C_GRAY)
        alg_note.next_to(alg_eq, DOWN, buff=0.22)

        # ── Connection to GD ───────────────────────────────────────────────────
        phi_lbl = Text("Reparameterisation:", font_size=22,
                        color=C_GOLD, weight=BOLD)
        phi_eq  = MathTex(
            r"\varphi_t = \ln\!\left(\frac{1}{L(\theta_t)}\right)"
            r"\quad\Rightarrow\quad"
            r"\varphi_{t+1} \approx \varphi_t + \eta\|\nabla\varphi_t\|^2",
            font_size=26, color=C_WHITE,
        )
        phi_lbl.next_to(alg_lbl, DOWN, buff=0.9, aligned_edge=LEFT)
        phi_eq.next_to(phi_lbl, RIGHT, buff=0.3)

        # ── Main theorem ───────────────────────────────────────────────────────
        thm_lbl = Text("Theorem (exponential convergence):", font_size=22,
                        color=C_GREEN, weight=BOLD)
        thm_eq  = MathTex(
            r"L(\theta_t) \le e^{-\Theta(\eta t)} \cdot L(\theta_0)",
            font_size=32, color=C_WHITE,
        )
        thm_lbl.next_to(phi_lbl, DOWN, buff=0.9, aligned_edge=LEFT)
        thm_eq.next_to(thm_lbl, RIGHT, buff=0.3)

        thm_box = SurroundingRectangle(
            VGroup(thm_lbl, thm_eq), color=C_GREEN,
            stroke_width=2, buff=0.2, corner_radius=0.1
        )

        # ── Lower bound ────────────────────────────────────────────────────────
        lb_lbl = Text("Lower bound (minimax-optimal):", font_size=22,
                       color=C_RED, weight=BOLD)
        lb_eq  = MathTex(
            r"L(\theta_t) = \Omega\!\left(e^{-O(\eta t)}\right)",
            font_size=30, color=C_WHITE,
        )
        lb_lbl.next_to(thm_lbl, DOWN, buff=0.85, aligned_edge=LEFT)
        lb_eq.next_to(lb_lbl, RIGHT, buff=0.3)

        match_note = MathTex(
            r"\text{Matches Perceptron lower bound — Adaptive GD is optimal!}",
            font_size=20, color=C_GOLD,
        )
        match_note.to_edge(DOWN, buff=0.55)

        self.play(FadeIn(alg_lbl, shift=RIGHT * 0.15),
                  Write(alg_eq), run_time=1.0)
        self.play(FadeIn(alg_note), run_time=0.5)
        self.wait(0.3)
        self.play(FadeIn(phi_lbl, shift=RIGHT * 0.15),
                  Write(phi_eq), run_time=1.0)
        self.wait(0.3)
        self.play(FadeIn(thm_lbl, shift=RIGHT * 0.15),
                  Write(thm_eq), run_time=0.9)
        self.play(Create(thm_box), run_time=0.6)
        self.wait(0.3)
        self.play(FadeIn(lb_lbl, shift=RIGHT * 0.15),
                  Write(lb_eq), run_time=0.9)
        self.play(FadeIn(match_note, shift=UP * 0.1), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  P11 – ℓ₂-REGULARISATION  (slides 33–36)
# ═══════════════════════════════════════════════════════════════════════════════
class P11_L2Reg(Scene):
    def construct(self):
        title = Text("ℓ₂-Regularisation: Acceleration from Large Stepsize",
                     font_size=28, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        uline = Line(LEFT * 5.5, RIGHT * 5.5,
                     color=C_GREEN, stroke_width=2).next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Create(uline), run_time=0.9)
        self.wait(0.2)

        # ── Regularised loss ───────────────────────────────────────────────────
        reg_lbl = Text("Regularised objective:", font_size=22,
                        color=C_WHITE, weight=BOLD)
        reg_eq  = MathTex(
            r"L_\lambda(\theta) = L(\theta) + \frac{\lambda}{2}\|\theta\|^2",
            font_size=34, color=C_BLUE,
        )
        reg_lbl.shift(LEFT * 3.6 + UP * 1.7)
        reg_eq.next_to(reg_lbl, RIGHT, buff=0.3)

        kappa_eq = MathTex(
            r"\kappa = \frac{\text{smoothness}}{\lambda}",
            font_size=28, color=C_GRAY,
        )
        kappa_eq.next_to(reg_eq, DOWN, buff=0.22, aligned_edge=LEFT)

        self.play(FadeIn(reg_lbl, shift=RIGHT * 0.15),
                  Write(reg_eq), run_time=1.0)
        self.play(FadeIn(kappa_eq), run_time=0.5)
        self.wait(0.3)

        # ── Comparison table ───────────────────────────────────────────────────
        tbl_title = Text("Convergence comparison:", font_size=22,
                          color=C_WHITE, weight=BOLD)
        tbl_title.shift(LEFT * 3.6 + UP * 0.5)

        row1_a = MathTex(r"\text{Small stepsize GD}", font_size=24, color=C_BLUE)
        row1_b = MathTex(r"\tilde{O}(\kappa)\text{ iterations}", font_size=26,
                          color=C_BLUE)
        row2_a = MathTex(r"\text{Large stepsize GD (new!)}",
                          font_size=24, color=C_GREEN)
        row2_b = MathTex(r"\tilde{O}(\sqrt{\kappa})\text{ iterations}",
                          font_size=26, color=C_GREEN)

        row1_a.move_to(LEFT * 2.8 + UP * 0.05)
        row1_b.move_to(RIGHT * 2.0 + UP * 0.05)
        row2_a.move_to(LEFT * 2.8 + DOWN * 0.65)
        row2_b.move_to(RIGHT * 2.0 + DOWN * 0.65)

        sep = Line(LEFT * 5.5, RIGHT * 5.5, color=C_GRAY,
                   stroke_width=0.8, stroke_opacity=0.5)
        sep.move_to(ORIGIN + UP * (-0.28))

        speedup_box = SurroundingRectangle(
            VGroup(row2_a, row2_b), color=C_GREEN,
            stroke_width=2, buff=0.2, corner_radius=0.1
        )
        speedup_note = Text("Quadratic speedup in condition number!",
                             font_size=21, color=C_GREEN)
        speedup_note.next_to(speedup_box, RIGHT, buff=0.3)

        self.play(FadeIn(tbl_title), run_time=0.6)
        self.play(Write(row1_a), Write(row1_b), Create(sep), run_time=0.9)
        self.play(Write(row2_a), Write(row2_b), run_time=0.9)
        self.play(Create(speedup_box), FadeIn(speedup_note), run_time=0.7)
        self.wait(0.4)

        # ── Phase transition for regularised case ──────────────────────────────
        tau_eq = MathTex(
            r"\tau = \Theta(\sqrt{\kappa})",
            font_size=32, color=C_ORANGE,
        )
        tau_note = Text("Phase transition time:", font_size=21,
                         color=C_ORANGE, weight=BOLD)
        tau_note.shift(LEFT * 3.0 + DOWN * 1.8)
        tau_eq.next_to(tau_note, RIGHT, buff=0.3)

        self.play(FadeIn(tau_note, shift=RIGHT * 0.15),
                  Write(tau_eq), run_time=0.9)
        self.wait(0.4)

        # ── Valley + basin picture ─────────────────────────────────────────────
        self._valley_basin()

        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))

    def _valley_basin(self):
        # Valley panel (left): elongated elliptical contours
        valley_ax = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
            x_length=2.8, y_length=2.8,
            axis_config={"color": C_GRAY, "stroke_width": 1,
                         "include_tip": False},
        ).shift(LEFT * 4.2 + DOWN * 2.5)

        for r in [0.4, 0.8, 1.2]:
            ellipse = Ellipse(width=r * 0.8, height=r * 2.5,
                              color=C_BLUE, stroke_width=1.5,
                              stroke_opacity=0.7, fill_opacity=0)
            ellipse.move_to(valley_ax.get_center())
            valley_ax.add(ellipse)

        valley_lbl = Text("Valley\n(unregularised)", font_size=17, color=C_BLUE)
        valley_lbl.next_to(valley_ax, DOWN, buff=0.15)

        # Basin panel (right): circular contours
        basin_ax = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
            x_length=2.8, y_length=2.8,
            axis_config={"color": C_GRAY, "stroke_width": 1,
                         "include_tip": False},
        ).shift(RIGHT * 0.8 + DOWN * 2.5)

        for r in [0.4, 0.8, 1.2]:
            circle = Circle(radius=r * 0.6, color=C_GREEN,
                            stroke_width=1.5, stroke_opacity=0.7,
                            fill_opacity=0)
            circle.move_to(basin_ax.get_center())
            basin_ax.add(circle)

        basin_lbl = Text("Basin\n(regularised)", font_size=17, color=C_GREEN)
        basin_lbl.next_to(basin_ax, DOWN, buff=0.15)

        reg_arrow = Arrow(valley_ax.get_right(), basin_ax.get_left(),
                          color=C_GOLD, stroke_width=2, buff=0.1)
        reg_arrow_lbl = MathTex(r"+\lambda\|\theta\|^2", font_size=18, color=C_GOLD)
        reg_arrow_lbl.next_to(reg_arrow, UP, buff=0.1)

        self.play(
            FadeIn(valley_ax), FadeIn(valley_lbl),
            FadeIn(basin_ax),  FadeIn(basin_lbl),
            run_time=0.9,
        )
        self.play(GrowArrow(reg_arrow), FadeIn(reg_arrow_lbl), run_time=0.7)
