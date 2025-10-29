"""Manim scene that summarizes core Uniswap v3 liquidity math formulas."""

from manim import (
    Axes,
    BLUE,
    Brace,
    Circumscribe,
    Create,
    DOWN,
    Dot,
    FadeIn,
    FadeOut,
    LEFT,
    MathTex,
    RIGHT,
    Scene,
    Tex,
    Text,
    TransformMatchingTex,
    UP,
    ValueTracker,
    VGroup,
    Write,
    YELLOW,
    always_redraw,
    linear,
)


class UniswapLiquidityBasics(Scene):
    """Visualize the key equations from the Uniswap v3 liquidity math note."""

    def construct(self) -> None:
        title = Text("Uniswap v3 Liquidity Math Basics", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        invariant_caption = Tex("Constant product invariant $xy = k$", font_size=38)
        invariant_caption.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(invariant_caption, shift=0.3 * DOWN))
        self.wait(0.3)

        k_value = 36
        axes = Axes(
            x_range=[0.6, 10, 1],
            y_range=[0.6, 10, 1],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": False, "include_numbers": True, "font_size": 26},
        )
        axes.next_to(invariant_caption, DOWN, buff=0.6)
        curve = axes.plot(lambda x: k_value / x, x_range=[0.8, 9.5], color=BLUE)

        tracker = ValueTracker(2.2)
        dot = Dot(color=YELLOW)

        def update_dot(mobject):
            x_val = tracker.get_value()
            y_val = k_value / x_val
            mobject.move_to(axes.c2p(x_val, y_val))

        dot.add_updater(update_dot)

        coordinate_label = always_redraw(
            lambda: MathTex(
                r"x \approx {x:.2f},\quad y \approx {y:.2f}".format(
                    x=tracker.get_value(),
                    y=k_value / tracker.get_value(),
                ),
                font_size=30,
            ).next_to(axes, RIGHT, buff=0.5)
        )

        self.play(Create(axes))
        self.play(Create(curve))
        self.play(FadeIn(dot), FadeIn(coordinate_label))
        self.wait(0.4)
        self.play(tracker.animate.set_value(7.5), run_time=4, rate_func=linear)
        self.wait(0.5)
        dot.remove_updater(update_dot)
        self.play(FadeOut(VGroup(axes, curve, dot, coordinate_label, invariant_caption)))
        self.wait(0.4)

        sections = [
            (
                r"Price below range: $P \leq p_a$",
                [
                    r"x = L \left(\frac{\sqrt{p_b} - \sqrt{p_a}}{\sqrt{p_a}\sqrt{p_b}}\right)",
                    r"L = x \frac{\sqrt{p_a}\sqrt{p_b}}{\sqrt{p_b} - \sqrt{p_a}}",
                ],
                "Position held entirely in token x",
            ),
            (
                r"Price above range: $P \geq p_b$",
                [
                    r"y = L \left(\sqrt{p_b} - \sqrt{p_a}\right)",
                    r"L = \frac{y}{\sqrt{p_b} - \sqrt{p_a}}",
                ],
                "All value is in token y",
            ),
            (
                r"Price inside range: $p_a < P < p_b$",
                [
                    r"x = L \left(\frac{\sqrt{p_b} - \sqrt{P}}{\sqrt{P}\sqrt{p_b}}\right)",
                    r"y = L \left(\sqrt{P} - \sqrt{p_a}\right)",
                    r"\frac{x}{y} = \frac{\sqrt{p_b} - \sqrt{P}}{\sqrt{P} \left(\sqrt{P} - \sqrt{p_a}\right)}",
                ],
                "Liquidity splits between both tokens",
            ),
            (
                r"Recovering range bounds from $L, x, y$",
                [
                    r"\sqrt{p_a} = \sqrt{P} - \frac{y}{L}",
                    r"\sqrt{p_b} = \frac{L \sqrt{P}}{L - x \sqrt{P}}",
                ],
                "Solve for ticks from observed reserves",
            ),
        ]

        for heading_tex, formula_tex_list, annotation in sections:
            heading = Tex(heading_tex, font_size=36)
            heading.next_to(title, DOWN, buff=0.8)
            self.play(FadeIn(heading, shift=0.3 * DOWN))
            self.wait(0.2)

            formula_mobjects = []
            for index, formula_tex in enumerate(formula_tex_list):
                formula = MathTex(formula_tex, font_size=34)
                if index == 0:
                    formula.next_to(heading, DOWN, aligned_edge=LEFT, buff=0.4)
                    self.play(Write(formula))
                else:
                    formula.next_to(
                        formula_mobjects[-1], DOWN, aligned_edge=LEFT, buff=0.3
                    )
                    self.play(TransformMatchingTex(formula_mobjects[-1].copy(), formula))
                self.wait(0.3)
                formula_mobjects.append(formula)

            content_group = VGroup(*formula_mobjects)
            brace = Brace(content_group, direction=LEFT, buff=0.2)
            brace_label = brace.get_text(annotation, font_size=28)
            brace_label.align_to(brace, LEFT)

            self.play(Create(brace))
            self.play(FadeIn(brace_label, shift=0.2 * RIGHT))
            self.play(Circumscribe(formula_mobjects[-1], color=YELLOW, time_width=1.2))
            self.wait(0.6)

            section_group = VGroup(heading, *formula_mobjects)
            self.play(FadeOut(brace), FadeOut(brace_label), FadeOut(section_group))
            self.wait(0.2)

        closing = Text(
            "Liquidity math keeps concentrated positions balanced.",
            font_size=34,
        )
        closing.next_to(title, DOWN, buff=0.8)
        self.play(FadeIn(closing, shift=0.3 * UP))
        self.wait(2)
