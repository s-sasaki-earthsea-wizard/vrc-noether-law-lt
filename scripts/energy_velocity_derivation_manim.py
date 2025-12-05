#!/usr/bin/env python3
"""
エネルギー保存則から速度の式を導出するアニメーション（manim版）

mgh = 1/2 mv^2 から v = √(2gh) を導出する過程を
簡潔に視覚化するアニメーション（約15秒）
"""

from manim import *


class EnergyVelocityDerivation(Scene):
    """エネルギー保存則から速度の式を導出するシーン"""

    def construct(self):
        # 色の設定
        ENERGY_COLOR = BLUE_C
        RESULT_COLOR = TEAL_C

        # ========== 1. エネルギー保存則 ==========
        energy_eq = MathTex(
            r"mgh",
            r"=",
            r"\frac{1}{2}mv^2",
            font_size=56,
            color=ENERGY_COLOR
        )
        energy_eq.move_to(UP * 1.5)

        self.play(Write(energy_eq), run_time=1.5)
        self.wait(0.5)

        # ========== 2. 変形の矢印と説明 ==========
        arrow1 = MathTex(r"\Downarrow", font_size=40, color=WHITE)
        arrow1.next_to(energy_eq, DOWN, buff=0.3)

        step_text = Text("m で割り、整理", font_size=20, color=GRAY)
        step_text.next_to(arrow1, RIGHT, buff=0.3)

        self.play(Write(arrow1), Write(step_text), run_time=0.6)

        # 中間式
        mid_eq = MathTex(
            r"v^2 = 2gh",
            font_size=52,
            color=YELLOW
        )
        mid_eq.next_to(arrow1, DOWN, buff=0.3)

        self.play(Write(mid_eq), run_time=1.0)
        self.wait(0.3)

        # ========== 3. 平方根を取る ==========
        arrow2 = MathTex(r"\Downarrow", font_size=40, color=WHITE)
        arrow2.next_to(mid_eq, DOWN, buff=0.3)

        sqrt_text = Text("平方根", font_size=20, color=GRAY)
        sqrt_text.next_to(arrow2, RIGHT, buff=0.3)

        self.play(Write(arrow2), Write(sqrt_text), run_time=0.6)

        # ========== 4. 最終結果 ==========
        final_result = MathTex(
            r"v = \sqrt{2gh}",
            font_size=64,
            color=RESULT_COLOR
        )
        final_result.next_to(arrow2, DOWN, buff=0.4)

        final_box = SurroundingRectangle(
            final_result,
            color=RESULT_COLOR,
            buff=0.2,
            stroke_width=3
        )

        self.play(
            Write(final_result),
            Create(final_box),
            run_time=1.5
        )
        self.wait(0.5)

        # ========== 5. 補足 ==========
        note = Text("落下速度は質量に依存しない", font_size=22, color=PINK)
        note.next_to(final_box, DOWN, buff=0.5)

        self.play(Write(note), run_time=0.8)
        self.wait(1.5)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


if __name__ == "__main__":
    # manim -pql energy_velocity_derivation_manim.py EnergyVelocityDerivation
    pass
