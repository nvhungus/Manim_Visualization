from manim import *

class TestScene(Scene):
    def construct(self):
        formula = MathTex(r"L(\theta) = \frac{1}{n}\sum_{i=1}^n \ell(y_i x_i^\top \theta)")
        self.play(Write(formula))
        self.wait(2)
