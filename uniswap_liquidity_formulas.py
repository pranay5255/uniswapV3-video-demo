"""Manim scene that summarizes core Uniswap v3 liquidity math formulas."""

from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    Indicate,
    LEFT,
    MathTex,
    Scene,
    Tex,
    Text,
    UP,
    VGroup,
)


class UniswapLiquidityBasics(Scene):
    """Visualize the key equations from the Uniswap v3 liquidity math note."""

    def construct(self) -> None:
        title = Text("Uniswap v3 Liquidity Math Basics", font_size=48)
        self.play(FadeIn(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        sections = [
            (
                Tex(r"Price below range: $P \leq p_a$", font_size=36),
                [
                    MathTex(
                        r"x = L \left(\frac{\sqrt{p_b} - \sqrt{p_a}}{\sqrt{p_a}\sqrt{p_b}}\right)",
                        font_size=36,
                    ),
                    MathTex(
                        r"L = x \frac{\sqrt{p_a}\sqrt{p_b}}{\sqrt{p_b} - \sqrt{p_a}}",
                        font_size=36,
                    ),
                ],
            ),
            (
                Tex(r"Price above range: $P \geq p_b$", font_size=36),
                [
                    MathTex(
                        r"y = L \left(\sqrt{p_b} - \sqrt{p_a}\right)",
                        font_size=36,
                    ),
                    MathTex(
                        r"L = \frac{y}{\sqrt{p_b} - \sqrt{p_a}}",
                        font_size=36,
                    ),
                ],
            ),
            (
                Tex(r"Price inside range: $p_a < P < p_b$", font_size=36),
                [
                    MathTex(
                        r"x = L \left(\frac{\sqrt{p_b} - \sqrt{P}}{\sqrt{P}\sqrt{p_b}}\right)",
                        font_size=36,
                    ),
                    MathTex(
                        r"y = L \left(\sqrt{P} - \sqrt{p_a}\right)",
                        font_size=36,
                    ),
                    MathTex(
                        r"\frac{x}{y} = \frac{\sqrt{p_b} - \sqrt{P}}{\sqrt{P} \left(\sqrt{P} - \sqrt{p_a}\right)}",
                        font_size=36,
                    ),
                ],
            ),
            (
                Tex(r"Recovering range bounds from $L$, $x$, $y$", font_size=36),
                [
                    MathTex(
                        r"\sqrt{p_a} = \sqrt{P} - \frac{y}{L}",
                        font_size=36,
                    ),
                    MathTex(
                        r"\sqrt{p_b} = \frac{L \sqrt{P}}{L - x \sqrt{P}}",
                        font_size=36,
                    ),
                ],
            ),
        ]

        for heading, formulas in sections:
            group = VGroup(heading, *formulas).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            group.next_to(title, DOWN, buff=0.8)

            self.play(FadeIn(heading, shift=0.3 * UP))
            self.wait(0.2)

            for formula in formulas:
                self.play(FadeIn(formula, shift=0.3 * UP))
                self.wait(0.6)

            self.play(Indicate(formulas[-1]))
            self.wait(0.8)
            self.play(FadeOut(group))
            self.wait(0.3)

        closing = Text(
            "Amounts and liquidity stay in sync with these formulas.", font_size=32
        )
        closing.next_to(title, DOWN, buff=1)
        self.play(FadeIn(closing))
        self.wait(2)
