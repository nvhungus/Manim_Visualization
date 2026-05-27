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
#  HELPER: sinh đường loss có spike
# ───────────────────────────────────────────────────────────────────────────────
def make_loss(seed, n=600, start=3.5, decay=0.9933, sigma=0.018,
              spike_steps=None, spike_mags=None):
    np.random.seed(seed)
    sp = dict(zip(spike_steps or [], spike_mags or []))
    vals = [start]
    for i in range(1, n):
        v = vals[-1] * decay + np.random.normal(0, sigma)
        v = max(v, 0.10)
        if i in sp:
            v += sp[i]
        vals.append(v)
    return np.array(vals)


# ═══════════════════════════════════════════════════════════════════════════════
#  SCENE 1 – TITLE CARD
# ═══════════════════════════════════════════════════════════════════════════════
class S1_Title(Scene):
    def construct(self):

        badge = Text("NeurIPS 2025 Tutorial", font_size=22,
                     color=C_BLUE, weight=BOLD)
        badge.to_edge(UP, buff=0.9)

        line1 = Text("Theoretical Insights on", font_size=40, color=C_WHITE)
        line2 = Text("Training Instability",    font_size=58, color=C_GOLD, weight=BOLD)
        line3 = Text("in Deep Learning",        font_size=40, color=C_WHITE)
        title = VGroup(line1, line2, line3).arrange(DOWN, buff=0.15)
        title.move_to(ORIGIN + UP * 0.25)

        uline = Line(line2.get_left(), line2.get_right(),
                     color=C_GOLD, stroke_width=2.5
                     ).next_to(line2, DOWN, buff=0.08)

        authors = Text(
            "Jingfeng Wu  ·  Yu-Xiang Wang  ·  Maryam Fazel",
            font_size=22, color=C_GRAY,
        ).next_to(title, DOWN, buff=0.65)
        insts = Text(
            "UC Berkeley  ·  UC San Diego  ·  U Washington",
            font_size=18, color=C_GRAY,
        ).next_to(authors, DOWN, buff=0.2)

        # ── Animate ──────────────────────────────────────────────────────────
        self.play(FadeIn(badge, shift=DOWN * 0.15), run_time=0.7)
        self.wait(0.15)
        self.play(Write(line1), Write(line3), run_time=1.1)
        self.play(Write(line2), run_time=0.9)
        self.play(Create(uline), run_time=0.5)
        self.play(
            FadeIn(authors, shift=UP * 0.12),
            FadeIn(insts,   shift=UP * 0.12),
            run_time=0.9,
        )
        self.wait(2.5)
        self.play(FadeOut(VGroup(badge, title, uline, authors, insts)))


# ═══════════════════════════════════════════════════════════════════════════════
#  SCENE 2 – LOSS SPIKES (hook chính)
# ═══════════════════════════════════════════════════════════════════════════════
class S2_LossSpikes(Scene):
    def construct(self):
        N  = 600
        xs = np.arange(N, dtype=float)

        specs = [
            (0, 3.4, 0.9932, [110, 295, 465], [1.25, 0.95, 0.75], "LLaMA 7B",   C_BLUE),
            (1, 3.6, 0.9928, [145, 335],       [1.50, 1.15],        "LLaMA 13B",  C_GREEN),
            (2, 3.8, 0.9924, [195, 375, 515],  [1.10, 1.35, 0.85],  "LLaMA 33B",  C_GOLD),
            (3, 4.0, 0.9920, [90, 255, 425, 550],[0.85,1.45,1.05,0.65],"LLaMA 65B",C_RED),
        ]

        ys = {lbl: make_loss(s, N, st, dc, spike_steps=sp, spike_mags=sm)
              for s, st, dc, sp, sm, lbl, _ in specs}

        # ── Axes ─────────────────────────────────────────────────────────────
        ax = Axes(
            x_range=[0, N, 100],
            y_range=[0, 5.5, 1],
            x_length=9.5, y_length=4.8,
            axis_config={"color": C_GRAY, "stroke_width": 1.5},
            x_axis_config={"include_tip": True},
            y_axis_config={"include_tip": True},
        ).shift(DOWN * 0.45 + LEFT * 0.1)

        x_lab = Text("Training Steps", font_size=19, color=C_GRAY)
        x_lab.next_to(ax.x_axis, DOWN, buff=0.28)
        y_lab = Text("Loss", font_size=19, color=C_GRAY)
        y_lab.rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.35)

        title = Text("Loss Spikes in LLM Pre-training",
                     font_size=34, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.32)

        # ── Vẽ các đường loss ─────────────────────────────────────────────────
        curves = {}
        for s, st, dc, sp, sm, lbl, col in specs:
            arr = ys[lbl]
            curves[lbl] = ax.plot(
                lambda x, a=arr: float(np.interp(x, xs, a)),
                x_range=[0, N - 1, 1],
                color=col,
                stroke_width=2.3,
            )

        # ── Legend ───────────────────────────────────────────────────────────
        leg_items = []
        for *_, lbl, col in specs:
            dot = Dot(color=col, radius=0.07)
            txt = Text(lbl, font_size=18, color=col)
            txt.next_to(dot, RIGHT, buff=0.12)
            leg_items.append(VGroup(dot, txt))
        legend = VGroup(*leg_items).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        legend.to_corner(UR, buff=0.5)

        # ── Animation ────────────────────────────────────────────────────────
        self.play(Write(title), run_time=0.8)
        self.play(Create(ax), FadeIn(x_lab), FadeIn(y_lab), run_time=1.2)
        self.play(FadeIn(legend), run_time=0.5)
        self.wait(0.2)

        # Vẽ tất cả đường cùng lúc từ trái sang phải
        self.play(
            *[Create(c, rate_func=linear) for c in curves.values()],
            run_time=4.5,
        )
        self.wait(0.5)

        # Highlight spike trên LLaMA 13B
        sp_step = 335
        sp_y    = float(np.interp(sp_step, xs, ys["LLaMA 13B"]))
        sp_pt   = ax.coords_to_point(sp_step, sp_y)

        ring  = Circle(radius=0.30, color=C_GOLD, stroke_width=2.5).move_to(sp_pt)
        lbl   = Text("Loss Spike!", font_size=24, color=C_GOLD, weight=BOLD)
        lbl.next_to(sp_pt, UR, buff=0.38)
        arr = Arrow(
            lbl.get_bottom() + LEFT * 0.1, sp_pt + UP * 0.18,
            color=C_GOLD, stroke_width=2, buff=0.06,
            max_tip_length_to_length_ratio=0.18,
        )

        self.play(Create(ring), Write(lbl), GrowArrow(arr), run_time=0.9)
        self.wait(0.3)

        # Flash các spike khác trên 3 đường còn lại
        other_pts = [
            ax.coords_to_point(110, ys["LLaMA 7B"][110]),
            ax.coords_to_point(195, ys["LLaMA 33B"][195]),
            ax.coords_to_point(90,  ys["LLaMA 65B"][90]),
        ]
        self.play(
            *[Flash(pt, color=C_GOLD, flash_radius=0.22, line_length=0.10)
              for pt in other_pts],
            run_time=0.8,
        )
        self.wait(0.5)

        # Câu hỏi kết scene
        question = Text(
            "Why does this happen?  Is it avoidable — or even useful?",
            font_size=24, color=C_BLUE,
            t2c={"useful": C_GREEN},
        )
        question.to_edge(DOWN, buff=0.32)
        self.play(Write(question), run_time=1.4)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  SCENE 3 – 4 NGUYÊN NHÂN GÂY BẤT ỔN ĐỊNH
# ═══════════════════════════════════════════════════════════════════════════════
class S3_WhyUnstable(Scene):
    def construct(self):

        title = Text("What causes training instability?",
                     font_size=34, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.45)

        causes = [
            ("①", "Data randomness",    "Unlucky mini-batches",                  C_BLUE),
            ("②", "Numerical overflow", "Insufficient floating-point precision",  C_RED),
            ("③", "Loss landscape",     "Varying layer-wise curvature",           C_PURPLE),
            ("④", "Large stepsize",     "Inherent optimization instability",      C_GOLD),
        ]

        cards = VGroup()
        for icon, head, sub, col in causes:
            num_txt  = Text(icon, font_size=36, color=col, weight=BOLD)
            head_txt = Text(head, font_size=26, color=C_WHITE, weight=BOLD)
            sub_txt  = Text(sub,  font_size=20, color=C_GRAY)
            head_txt.next_to(num_txt, RIGHT, buff=0.20)
            sub_txt.next_to(head_txt, DOWN, buff=0.08, aligned_edge=LEFT)
            cards.add(VGroup(num_txt, head_txt, sub_txt))

        cards.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        cards.shift(LEFT * 0.5 + DOWN * 0.2)

        # Box đánh dấu nguyên nhân ④ là trọng tâm
        focus_box = SurroundingRectangle(
            cards[3], color=C_GOLD, stroke_width=2.5, buff=0.18, corner_radius=0.1
        )
        focus_note = Text("← Focus of this tutorial",
                          font_size=20, color=C_GOLD)
        focus_note.next_to(focus_box, RIGHT, buff=0.25)

        # ── Animate ──────────────────────────────────────────────────────────
        self.play(Write(title), run_time=0.8)
        self.wait(0.2)

        for card in cards:
            self.play(FadeIn(card, shift=RIGHT * 0.25), run_time=0.6)
            self.wait(0.12)

        self.wait(0.4)
        self.play(Create(focus_box), Write(focus_note), run_time=0.9)
        self.wait(0.4)

        # Mờ 3 nguyên nhân trên, giữ ④ sáng
        self.play(
            VGroup(*[cards[i] for i in range(3)]).animate.set_opacity(0.22),
            run_time=0.9,
        )
        self.wait(2.2)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  SCENE 4 – GD VỚI STEPSIZE NHỎ vs LỚN (1D parabola demo)
# ═══════════════════════════════════════════════════════════════════════════════
class S4_GDDemo(Scene):
    def construct(self):

        title = Text("Gradient Descent: small vs large stepsize",
                     font_size=30, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.38)

        # ── Axes & parabola ───────────────────────────────────────────────────
        ax = Axes(
            x_range=[-4, 4, 1],
            y_range=[-0.5, 8, 2],
            x_length=8, y_length=4.5,
            axis_config={"color": C_GRAY, "stroke_width": 1.5},
            x_axis_config={"include_tip": True},
            y_axis_config={"include_tip": True},
        ).shift(DOWN * 0.35)

        parabola = ax.plot(lambda x: x ** 2,
                           x_range=[-2.9, 2.9],
                           color=C_BLUE, stroke_width=3)

        f_label = MathTex(r"L(\theta) = \theta^2",
                          font_size=30, color=C_BLUE)
        f_label.to_corner(UR, buff=0.7)

        self.play(Write(title), run_time=0.7)
        self.play(Create(ax), Create(parabola), Write(f_label), run_time=1.2)
        self.wait(0.3)

        # ── Helper: animate GD trajectory ────────────────────────────────────
        def run_gd(x0, eta, color, label_str, n_steps=12):
            x = x0
            dot = Dot(ax.coords_to_point(x, x**2), color=color, radius=0.12)
            lbl = Text(label_str, font_size=20, color=color, weight=BOLD)
            lbl.next_to(dot, UP, buff=0.2)

            self.play(FadeIn(dot, scale=0.4), Write(lbl), run_time=0.6)

            path_pts   = [ax.coords_to_point(x, x**2)]
            step_lines = VGroup()

            for _ in range(n_steps):
                grad    = 2 * x
                x_new   = x - eta * grad
                # clamp để tránh ra ngoài axes
                x_new   = np.clip(x_new, -3.8, 3.8)
                pt_old  = ax.coords_to_point(x, x**2)
                pt_new  = ax.coords_to_point(x_new, x_new**2)
                # đường thẳng đứng từ điểm cũ lên/xuống trên parabola
                step_lines.add(
                    Line(pt_old, pt_new, color=color,
                         stroke_width=1.2, stroke_opacity=0.5)
                )
                path_pts.append(pt_new)
                self.play(
                    dot.animate.move_to(pt_new),
                    lbl.animate.next_to(pt_new, UP, buff=0.2),
                    run_time=0.25,
                )
                x = x_new
                if abs(x) < 0.05:
                    break

            trail = VMobject(color=color, stroke_width=1.5, stroke_opacity=0.45)
            trail.set_points_as_corners(path_pts)
            self.add(trail)
            return dot, lbl, trail

        # Small stepsize η = 0.15
        eta_small_lbl = MathTex(r"\eta = 0.15\ \text{(small)}",
                                 font_size=24, color=C_GREEN)
        eta_small_lbl.to_corner(UL, buff=0.6)
        self.play(Write(eta_small_lbl), run_time=0.5)

        d1, l1, t1 = run_gd(x0=3.2, eta=0.15, color=C_GREEN,
                             label_str="η small", n_steps=18)
        converge_txt = Text("✓ Converges smoothly", font_size=20, color=C_GREEN)
        converge_txt.next_to(eta_small_lbl, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(converge_txt, shift=RIGHT * 0.1), run_time=0.5)
        self.wait(0.5)

        # Large stepsize η = 0.95 (oscillates but converges)
        eta_large_lbl = MathTex(r"\eta = 0.95\ \text{(large)}",
                                 font_size=24, color=C_GOLD)
        eta_large_lbl.next_to(eta_small_lbl, DOWN, buff=0.8, aligned_edge=LEFT)
        self.play(Write(eta_large_lbl), run_time=0.5)

        d2, l2, t2 = run_gd(x0=3.2, eta=0.95, color=C_GOLD,
                             label_str="η large", n_steps=14)
        oscillate_txt = Text("⚡ Oscillates — but still converges!",
                              font_size=20, color=C_GOLD)
        oscillate_txt.next_to(eta_large_lbl, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(oscillate_txt, shift=RIGHT * 0.1), run_time=0.5)
        self.wait(0.5)

        # Too large: η = 1.05 → diverges
        eta_huge_lbl = MathTex(r"\eta = 1.05\ \text{(too large)}",
                                font_size=24, color=C_RED)
        eta_huge_lbl.next_to(eta_large_lbl, DOWN, buff=0.8, aligned_edge=LEFT)
        self.play(Write(eta_huge_lbl), run_time=0.5)

        x = 3.2
        dot_div = Dot(ax.coords_to_point(x, x**2), color=C_RED, radius=0.12)
        lbl_div = Text("η too large", font_size=20, color=C_RED, weight=BOLD)
        lbl_div.next_to(dot_div, UP, buff=0.2)
        self.play(FadeIn(dot_div, scale=0.4), Write(lbl_div), run_time=0.5)

        for _ in range(5):
            grad  = 2 * x
            x_new = x - 1.05 * grad
            if abs(x_new) > 3.8:
                x_new = np.sign(x_new) * 3.8
                pt_new = ax.coords_to_point(x_new, x_new**2)
                self.play(dot_div.animate.move_to(pt_new),
                          lbl_div.animate.next_to(pt_new, UP, buff=0.2),
                          run_time=0.22)
                break
            pt_new = ax.coords_to_point(x_new, x_new**2)
            self.play(dot_div.animate.move_to(pt_new),
                      lbl_div.animate.next_to(pt_new, UP, buff=0.2),
                      run_time=0.22)
            x = x_new

        diverge_txt = Text("✗ Diverges!", font_size=20, color=C_RED, weight=BOLD)
        diverge_txt.next_to(eta_huge_lbl, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(diverge_txt, shift=RIGHT * 0.1), run_time=0.5)
        self.wait(2.2)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  SCENE 5 – ĐIỀU KIỆN ỔN ĐỊNH: DESCENT LEMMA & EDGE OF STABILITY
# ═══════════════════════════════════════════════════════════════════════════════
class S5_StabilityCondition(Scene):
    def construct(self):

        title = Text("When is Gradient Descent stable?",
                     font_size=34, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.42)

        # ── Ba chế độ stepsize ────────────────────────────────────────────────
        bar_bg = Rectangle(width=0.5, height=5.5, color=C_GRAY,
                           fill_opacity=0.15, stroke_width=1)
        bar_bg.shift(LEFT * 3.8 + DOWN * 0.3)

        seg_stable   = Rectangle(width=0.5, height=1.5,
                                  color=C_GREEN,  fill_opacity=0.8, stroke_width=0)
        seg_unstable = Rectangle(width=0.5, height=1.8,
                                  color=C_PURPLE, fill_opacity=0.8, stroke_width=0)
        seg_diverge  = Rectangle(width=0.5, height=2.0,
                                  color=C_RED,    fill_opacity=0.8, stroke_width=0)

        # Xếp từ dưới lên (stable → unstable → diverge)
        segs = VGroup(seg_stable, seg_unstable, seg_diverge)
        segs.arrange(UP, buff=0)
        segs.move_to(bar_bg)

        arrow_up = Arrow(bar_bg.get_bottom() + DOWN * 0.3,
                         bar_bg.get_top()    + UP   * 0.3,
                         color=C_GRAY, stroke_width=2, buff=0.05)
        arrow_up.move_to(bar_bg).shift(LEFT * 0.0)

        eta_label = MathTex(r"\eta", font_size=32, color=C_WHITE)
        eta_label.next_to(arrow_up, UP, buff=0.12)
        eta_zero = Text("η → 0\n(gradient flow)", font_size=16, color=C_GRAY)
        eta_zero.next_to(bar_bg, DOWN, buff=0.12)
        eta_inf = MathTex(r"\eta = \infty", font_size=20, color=C_RED)
        eta_inf.next_to(bar_bg, UP, buff=0.12)

        regime_labels = VGroup(
            Text("Stable\nconvergent",   font_size=20, color=C_GREEN),
            Text("Unstable\nconvergent", font_size=20, color=C_PURPLE),
            Text("Divergent",            font_size=20, color=C_RED),
        )
        for lbl, seg in zip(regime_labels, segs):
            lbl.next_to(seg, RIGHT, buff=0.3)

        bar_group = VGroup(bar_bg, segs, arrow_up, eta_label,
                           eta_zero, eta_inf, regime_labels)
        bar_group.shift(LEFT * 3.5)

        # ── Công thức điều kiện ổn định ────────────────────────────────────────
        cond_title = Text("Classical stability condition:", font_size=24,
                          color=C_WHITE).shift(RIGHT * 1.2 + UP * 2.0)

        descent_lemma = MathTex(
            r"\eta < \frac{2}{\lambda_{\max}(\nabla^2 L(\theta))}",
            font_size=38, color=C_GOLD,
        ).next_to(cond_title, DOWN, buff=0.3)

        box1 = SurroundingRectangle(descent_lemma, color=C_GOLD,
                                    stroke_width=1.8, buff=0.2, corner_radius=0.1)

        eos_title = Text("But in practice — Edge of Stability:", font_size=24,
                         color=C_WHITE).next_to(box1, DOWN, buff=0.55)

        eos_formula = MathTex(
            r"\lambda_{\max}(\nabla^2 L(\theta)) \approx \frac{2}{\eta}",
            font_size=38, color=C_PURPLE,
        ).next_to(eos_title, DOWN, buff=0.3)

        box2 = SurroundingRectangle(eos_formula, color=C_PURPLE,
                                    stroke_width=1.8, buff=0.2, corner_radius=0.1)

        note = Text("GD operates right at the boundary!", font_size=22,
                    color=C_ORANGE).next_to(box2, DOWN, buff=0.4)

        # ── Animate ──────────────────────────────────────────────────────────
        self.play(Write(title), run_time=0.8)
        self.wait(0.2)

        self.play(FadeIn(bar_bg), Create(arrow_up),
                  FadeIn(eta_label), FadeIn(eta_zero), FadeIn(eta_inf),
                  run_time=0.9)
        self.play(
            FadeIn(seg_stable,   shift=UP * 0.1),
            FadeIn(regime_labels[0]), run_time=0.5,
        )
        self.play(
            FadeIn(seg_unstable, shift=UP * 0.1),
            FadeIn(regime_labels[1]), run_time=0.5,
        )
        self.play(
            FadeIn(seg_diverge,  shift=UP * 0.1),
            FadeIn(regime_labels[2]), run_time=0.5,
        )
        self.wait(0.4)

        self.play(Write(cond_title), run_time=0.6)
        self.play(Write(descent_lemma), run_time=1.1)
        self.play(Create(box1), run_time=0.5)
        self.wait(0.5)

        self.play(Write(eos_title), run_time=0.7)
        self.play(Write(eos_formula), run_time=1.1)
        self.play(Create(box2), run_time=0.5)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.wait(2.2)
        self.play(FadeOut(*self.mobjects))


# ═══════════════════════════════════════════════════════════════════════════════
#  SCENE 6 – OUTLINE: PART 1 & PART 2
# ═══════════════════════════════════════════════════════════════════════════════
class S6_Outline(Scene):
    def construct(self):

        title = Text("What this tutorial covers",
                     font_size=36, color=C_WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.42)

        # ── Central node ──────────────────────────────────────────────────────
        center_box = RoundedRectangle(
            width=4.2, height=1.0, corner_radius=0.2,
            color=C_WHITE, fill_opacity=0.08, stroke_width=2,
        ).move_to(ORIGIN + UP * 0.1)
        center_txt = Text("Training Instability\n(Large Stepsizes)",
                          font_size=22, color=C_WHITE).move_to(center_box)

        # ── Part 1 box ────────────────────────────────────────────────────────
        p1_box = RoundedRectangle(
            width=4.5, height=2.4, corner_radius=0.2,
            color=C_GOLD, fill_opacity=0.08, stroke_width=2,
        ).shift(LEFT * 3.5 + DOWN * 1.2)
        p1_head = Text("Part 1", font_size=24, color=C_GOLD, weight=BOLD)
        p1_sub  = Text("Optimization", font_size=20, color=C_GOLD)
        p1_items = BulletedList(
            "Accelerates convergence",
            "Phase transition behavior",
            "Minimax-optimal rates",
            font_size=17, color=C_WHITE, buff=0.25,
        )
        p1_head.next_to(p1_box.get_top(), DOWN, buff=0.2)
        p1_sub.next_to(p1_head, DOWN, buff=0.08)
        p1_items.next_to(p1_sub, DOWN, buff=0.18)
        p1_group = VGroup(p1_box, p1_head, p1_sub, p1_items)

        # ── Part 2 box ────────────────────────────────────────────────────────
        p2_box = RoundedRectangle(
            width=4.5, height=2.4, corner_radius=0.2,
            color=C_GREEN, fill_opacity=0.08, stroke_width=2,
        ).shift(RIGHT * 3.5 + DOWN * 1.2)
        p2_head = Text("Part 2", font_size=24, color=C_GREEN, weight=BOLD)
        p2_sub  = Text("Generalization", font_size=20, color=C_GREEN)
        p2_items = BulletedList(
            "Finds flatter minima",
            "Prevents overfitting",
            "Provable gen. bounds",
            font_size=17, color=C_WHITE, buff=0.25,
        )
        p2_head.next_to(p2_box.get_top(), DOWN, buff=0.2)
        p2_sub.next_to(p2_head, DOWN, buff=0.08)
        p2_items.next_to(p2_sub, DOWN, buff=0.18)
        p2_group = VGroup(p2_box, p2_head, p2_sub, p2_items)

        # ── Mũi tên nối ───────────────────────────────────────────────────────
        arr_left  = Arrow(center_box.get_left(),  p1_box.get_top(),
                          color=C_GOLD,  stroke_width=2, buff=0.1)
        arr_right = Arrow(center_box.get_right(), p2_box.get_top(),
                          color=C_GREEN, stroke_width=2, buff=0.1)

        # ── Animate ──────────────────────────────────────────────────────────
        self.play(Write(title), run_time=0.8)
        self.wait(0.2)

        self.play(
            Create(center_box),
            Write(center_txt),
            run_time=0.9,
        )
        self.wait(0.3)

        self.play(
            GrowArrow(arr_left),
            GrowArrow(arr_right),
            run_time=0.8,
        )
        self.play(
            FadeIn(p1_group, shift=LEFT * 0.3),
            FadeIn(p2_group, shift=RIGHT * 0.3),
            run_time=1.0,
        )
        self.wait(0.6)

        # Lần lượt highlight từng part
        self.play(p1_box.animate.set_stroke(color=C_GOLD, width=3.5),
                  run_time=0.5)
        self.wait(0.5)
        self.play(p1_box.animate.set_stroke(color=C_GOLD, width=2),
                  p2_box.animate.set_stroke(color=C_GREEN, width=3.5),
                  run_time=0.5)
        self.wait(0.5)
        self.play(p2_box.animate.set_stroke(color=C_GREEN, width=2),
                  run_time=0.4)

        self.wait(2.0)
        self.play(FadeOut(*self.mobjects))
