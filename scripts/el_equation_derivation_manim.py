#!/usr/bin/env python3
"""
EL方程式から自由落下の運動方程式を導出するアニメーション（manim版）

ラグランジアン L = (1/2)mq̇² - mgq をEL方程式に代入し、
ニュートンの運動方程式 a = -g と同じ結果になることを示す。
手書き風のアニメーションで段階的に式を表示する。
"""

from manim import *


class ELEquationDerivation(Scene):
    """EL方程式から自由落下の運動方程式を導出するシーン"""

    def construct(self):
        # 色の設定
        LAGRANGIAN_COLOR = BLUE_C
        EL_COLOR = GREEN_C
        LEFT_COLOR = YELLOW
        RIGHT_COLOR = RED_C
        RESULT_COLOR = TEAL_C
        NEWTON_COLOR = PINK

        # ========== 1. ラグランジアン ==========
        lagrangian_label = Text("ラグランジアン（自由落下）", font_size=28, color=LAGRANGIAN_COLOR)
        lagrangian_label.to_edge(UP, buff=0.8)

        lagrangian = MathTex(
            r"L = \frac{1}{2}m\dot{q}^2 - mgq",
            font_size=48,
            color=LAGRANGIAN_COLOR
        )
        lagrangian.next_to(lagrangian_label, DOWN, buff=0.4)

        self.play(Write(lagrangian_label), run_time=0.8)
        self.play(Write(lagrangian), run_time=2.0)
        self.wait(1.0)

        # フェードアウト
        self.play(
            FadeOut(lagrangian_label),
            lagrangian.animate.scale(0.7).to_corner(UL, buff=0.8).shift(DOWN * 0.5),
            run_time=1.0
        )

        # ========== 2. EL方程式 ==========
        el_label = Text("オイラー・ラグランジュ方程式", font_size=28, color=EL_COLOR)
        el_label.move_to(ORIGIN + UP * 1.5)

        el_equation = MathTex(
            r"\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{q}}\right)",
            r"=",
            r"\frac{\partial L}{\partial q}",
            font_size=48,
            color=EL_COLOR
        )
        el_equation.next_to(el_label, DOWN, buff=0.4)

        self.play(Write(el_label), run_time=0.8)
        self.play(Write(el_equation), run_time=2.5)
        self.wait(1.0)

        # EL方程式を上に移動
        self.play(
            FadeOut(el_label),
            el_equation.animate.scale(0.7).next_to(lagrangian, RIGHT, buff=1.5),
            run_time=1.0
        )

        # ========== 3. 左辺の計算 ==========
        left_label = Text("【左辺】", font_size=32, color=LEFT_COLOR)
        left_label.move_to(LEFT * 3.5 + UP * 1.0)

        self.play(Write(left_label), run_time=0.5)

        # Step 1: 偏微分
        left_step1 = MathTex(
            r"\frac{\partial L}{\partial \dot{q}}",
            r"=",
            r"\frac{\partial}{\partial \dot{q}}\left(\frac{1}{2}m\dot{q}^2 - mgq\right)",
            font_size=36,
            color=LEFT_COLOR
        )
        left_step1.next_to(left_label, DOWN, buff=0.4)

        self.play(Write(left_step1), run_time=2.5)
        self.wait(0.5)

        # mgqに打ち消し線（qは速度に依存しないため）
        strikethrough1 = Line(
            left_step1[2].get_corner(DR) + LEFT * 0.8 + UP * 0.1,
            left_step1[2].get_corner(DR) + LEFT * 0.1 + UP * 0.4,
            color=GRAY,
            stroke_width=3
        )
        self.play(Create(strikethrough1), run_time=0.5)
        self.wait(0.3)

        # Step 2: 結果
        left_step2 = MathTex(
            r"= m\dot{q}",
            font_size=40,
            color=LEFT_COLOR
        )
        left_step2.next_to(left_step1, DOWN, buff=0.3, aligned_edge=LEFT).shift(RIGHT * 2.5)

        self.play(Write(left_step2), run_time=1.0)
        self.wait(0.5)

        # Step 3: 時間微分
        left_step3 = MathTex(
            r"\frac{d}{dt}\left(m\dot{q}\right)",
            r"=",
            r"m\ddot{q}",
            font_size=40,
            color=LEFT_COLOR
        )
        left_step3.next_to(left_step2, DOWN, buff=0.4, aligned_edge=LEFT).shift(LEFT * 1.0)

        self.play(Write(left_step3), run_time=2.0)
        self.wait(0.5)

        # 左辺の結果をボックスで囲む
        left_result_label = Text("左辺", font_size=28, color=YELLOW)
        left_result_eq = MathTex(r"= m\ddot{q}", font_size=36, color=YELLOW)
        left_result = VGroup(left_result_label, left_result_eq).arrange(RIGHT, buff=0.2)
        left_result.next_to(left_step3, DOWN, buff=0.5)

        left_box = SurroundingRectangle(left_result, color=LEFT_COLOR, buff=0.15, stroke_width=2)

        self.play(Write(left_result), Create(left_box), run_time=1.0)
        self.wait(0.5)

        # 左辺の計算をフェードアウト（結果のみ残す）
        left_group = VGroup(left_result, left_box)
        self.play(
            FadeOut(left_label),
            FadeOut(left_step1),
            FadeOut(strikethrough1),
            FadeOut(left_step2),
            FadeOut(left_step3),
            left_group.animate.move_to(LEFT * 3 + DOWN * 0.5),
            run_time=1.0
        )

        # ========== 4. 右辺の計算 ==========
        right_label = Text("【右辺】", font_size=32, color=RIGHT_COLOR)
        right_label.move_to(RIGHT * 3.5 + UP * 1.0)

        self.play(Write(right_label), run_time=0.5)

        # Step 1: 偏微分
        right_step1 = MathTex(
            r"\frac{\partial L}{\partial q}",
            r"=",
            r"\frac{\partial}{\partial q}\left(\frac{1}{2}m\dot{q}^2 - mgq\right)",
            font_size=36,
            color=RIGHT_COLOR
        )
        right_step1.next_to(right_label, DOWN, buff=0.4)

        self.play(Write(right_step1), run_time=2.5)
        self.wait(0.5)

        # (1/2)mq̇²に打ち消し線（速度項は位置に依存しないため）
        strikethrough2 = Line(
            right_step1[2].get_center() + LEFT * 1.0 + DOWN * 0.1,
            right_step1[2].get_center() + LEFT * 0.1 + UP * 0.3,
            color=GRAY,
            stroke_width=3
        )
        self.play(Create(strikethrough2), run_time=0.5)
        self.wait(0.3)

        # Step 2: 結果
        right_step2 = MathTex(
            r"= -mg",
            font_size=40,
            color=RIGHT_COLOR
        )
        right_step2.next_to(right_step1, DOWN, buff=0.3, aligned_edge=LEFT).shift(RIGHT * 2.5)

        self.play(Write(right_step2), run_time=1.0)
        self.wait(0.5)

        # 右辺の結果をボックスで囲む
        right_result_label = Text("右辺", font_size=28, color=RED_C)
        right_result_eq = MathTex(r"= -mg", font_size=36, color=RED_C)
        right_result = VGroup(right_result_label, right_result_eq).arrange(RIGHT, buff=0.2)
        right_result.next_to(right_step2, DOWN, buff=0.5)

        right_box = SurroundingRectangle(right_result, color=RIGHT_COLOR, buff=0.15, stroke_width=2)

        self.play(Write(right_result), Create(right_box), run_time=1.0)
        self.wait(0.5)

        # 右辺の計算をフェードアウト（結果のみ残す）
        right_group = VGroup(right_result, right_box)
        self.play(
            FadeOut(right_label),
            FadeOut(right_step1),
            FadeOut(strikethrough2),
            FadeOut(right_step2),
            right_group.animate.move_to(RIGHT * 3 + DOWN * 0.5),
            run_time=1.0
        )

        # ========== 5. 両辺を合わせる ==========
        self.wait(0.5)

        # 左辺と右辺を中央に移動
        self.play(
            left_group.animate.move_to(LEFT * 2.5 + UP * 0.5),
            right_group.animate.move_to(RIGHT * 2.5 + UP * 0.5),
            run_time=0.8
        )

        # 等号でつなげる
        combine_label = Text("【左辺 = 右辺】", font_size=32, color=RESULT_COLOR)
        combine_label.move_to(UP * 2.0)

        self.play(Write(combine_label), run_time=0.5)

        combine_eq = MathTex(
            r"m\ddot{q} = -mg",
            font_size=48,
            color=RESULT_COLOR
        )
        combine_eq.move_to(ORIGIN)

        self.play(
            FadeOut(left_group),
            FadeOut(right_group),
            Write(combine_eq),
            run_time=1.5
        )
        self.wait(0.5)

        # 矢印と説明
        arrow = MathTex(r"\Downarrow", font_size=48, color=WHITE)
        arrow.next_to(combine_eq, DOWN, buff=0.3)

        divide_text = Text("両辺を m で割る", font_size=24, color=WHITE)
        divide_text.next_to(arrow, RIGHT, buff=0.3)

        self.play(Write(arrow), Write(divide_text), run_time=0.8)
        self.wait(0.3)

        # 最終結果
        final_result = MathTex(
            r"\ddot{q} = -g",
            font_size=56,
            color=RESULT_COLOR
        )
        final_result.next_to(arrow, DOWN, buff=0.5)

        final_box = SurroundingRectangle(final_result, color=RESULT_COLOR, buff=0.2, stroke_width=3)

        self.play(Write(final_result), Create(final_box), run_time=1.5)
        self.wait(1.0)

        # ========== 6. ニュートンの運動方程式との一致 ==========
        newton_text = MathTex(
            r"\ddot{q} = a = -g",
            font_size=40,
            color=NEWTON_COLOR
        )
        newton_text.next_to(final_box, DOWN, buff=0.6)

        newton_label = Text("← ニュートンの運動方程式と一致！", font_size=24, color=NEWTON_COLOR)
        newton_label.next_to(newton_text, RIGHT, buff=0.3)

        self.play(Write(newton_text), run_time=1.0)
        self.play(Write(newton_label), run_time=1.0)
        self.wait(0.5)

        # 最終メッセージ（点滅効果）
        success_text = Text("ラグランジアンから運動方程式が導出できた！", font_size=28, color=YELLOW)
        success_text.to_edge(DOWN, buff=0.8)

        self.play(Write(success_text), run_time=1.0)

        # 点滅効果
        for _ in range(3):
            self.play(success_text.animate.set_opacity(0.3), run_time=0.3)
            self.play(success_text.animate.set_opacity(1.0), run_time=0.3)

        self.wait(2.0)

        # 全体をフェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.0)


if __name__ == "__main__":
    # コマンドラインから実行する場合
    # manim -pql el_equation_derivation_manim.py ELEquationDerivation
    pass
