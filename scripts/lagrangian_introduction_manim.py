#!/usr/bin/env python3
"""
ラグランジアンの導入アニメーション（manim版）

yt_script.md L182-193に対応:
- L = T - V の定義を紹介
- 自由落下のラグランジアン L = ½mv² - mgh を表示
"""

from manim import *


class LagrangianIntroduction(Scene):
    """ラグランジアンの導入シーン"""

    def construct(self):
        # 色の設定
        TITLE_COLOR = BLUE_C
        LAGRANGIAN_COLOR = YELLOW
        KINETIC_COLOR = GREEN_C
        POTENTIAL_COLOR = RED_C
        FREEFALL_COLOR = TEAL_C

        # ========== 1. タイトル ==========
        title = Text("ラグランジアン", font_size=48, color=TITLE_COLOR)
        title.to_edge(UP, buff=0.8)

        self.play(Write(title), run_time=1.0)
        self.wait(0.5)

        # ========== 2. ラグランジアンの形 L = T - V ==========
        lagrangian_def = MathTex(
            r"L", r"=", r"T", r"-", r"V",
            font_size=72,
            color=LAGRANGIAN_COLOR
        )
        lagrangian_def.next_to(title, DOWN, buff=0.6)

        # 各部分に色をつける
        lagrangian_def[0].set_color(LAGRANGIAN_COLOR)  # L
        lagrangian_def[2].set_color(KINETIC_COLOR)     # T
        lagrangian_def[4].set_color(POTENTIAL_COLOR)   # V

        self.play(Write(lagrangian_def), run_time=2.0)
        self.wait(1.0)

        # ========== 3. TとVの説明 ==========
        # Tの説明（運動エネルギー）
        t_label = Text("T : 運動エネルギー", font_size=32, color=KINETIC_COLOR)
        t_label.next_to(lagrangian_def, DOWN, buff=0.8)
        t_label.shift(LEFT * 2)

        # Vの説明（位置エネルギー）
        v_label = Text("V : 位置エネルギー", font_size=32, color=POTENTIAL_COLOR)
        v_label.next_to(t_label, RIGHT, buff=1.5)

        self.play(Write(t_label), run_time=1.0)
        self.play(Write(v_label), run_time=1.0)
        self.wait(1.0)

        # TとVをハイライト
        t_box = SurroundingRectangle(lagrangian_def[2], color=KINETIC_COLOR, buff=0.1)
        v_box = SurroundingRectangle(lagrangian_def[4], color=POTENTIAL_COLOR, buff=0.1)

        self.play(Create(t_box), Create(v_box), run_time=0.8)
        self.wait(0.5)
        self.play(FadeOut(t_box), FadeOut(v_box), run_time=0.5)

        # ========== 4. 「差」を強調 ==========
        minus_highlight = SurroundingRectangle(
            lagrangian_def[3],
            color=YELLOW,
            buff=0.15,
            stroke_width=3
        )
        minus_text = Text("引き算！", font_size=28, color=YELLOW)
        minus_text.next_to(minus_highlight, DOWN, buff=0.3)

        self.play(Create(minus_highlight), Write(minus_text), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(minus_highlight), FadeOut(minus_text), run_time=0.5)

        # ========== 5. 上部に移動 ==========
        self.play(
            FadeOut(title),
            FadeOut(t_label),
            FadeOut(v_label),
            lagrangian_def.animate.scale(0.6).to_corner(UL, buff=0.5),
            run_time=1.0
        )

        # ========== 6. 自由落下のラグランジアン ==========
        freefall_title = Text("自由落下のラグランジアン", font_size=36, color=FREEFALL_COLOR)
        freefall_title.move_to(UP * 2)

        self.play(Write(freefall_title), run_time=1.0)

        # L = T - V を再表示
        l_tv = MathTex(
            r"L", r"=", r"T", r"-", r"V",
            font_size=48
        )
        l_tv[0].set_color(LAGRANGIAN_COLOR)
        l_tv[2].set_color(KINETIC_COLOR)
        l_tv[4].set_color(POTENTIAL_COLOR)
        l_tv.next_to(freefall_title, DOWN, buff=0.6)

        self.play(Write(l_tv), run_time=1.5)
        self.wait(0.5)

        # 運動エネルギーの具体形
        kinetic_eq = MathTex(
            r"T = \frac{1}{2}mv^2",
            font_size=40,
            color=KINETIC_COLOR
        )
        kinetic_eq.next_to(l_tv, DOWN, buff=0.5)
        kinetic_eq.shift(LEFT * 2)

        kinetic_label = Text("（運動エネルギー）", font_size=20, color=KINETIC_COLOR)
        kinetic_label.next_to(kinetic_eq, DOWN, buff=0.15)

        # 位置エネルギーの具体形
        potential_eq = MathTex(
            r"V = mgh",
            font_size=40,
            color=POTENTIAL_COLOR
        )
        potential_eq.next_to(l_tv, DOWN, buff=0.5)
        potential_eq.shift(RIGHT * 2)

        potential_label = Text("（位置エネルギー）", font_size=20, color=POTENTIAL_COLOR)
        potential_label.next_to(potential_eq, DOWN, buff=0.15)

        self.play(
            Write(kinetic_eq),
            Write(kinetic_label),
            run_time=1.5
        )
        self.play(
            Write(potential_eq),
            Write(potential_label),
            run_time=1.5
        )
        self.wait(1.0)

        # ========== 7. 代入して最終形 ==========
        arrow = MathTex(r"\Downarrow", font_size=48, color=WHITE)
        arrow.next_to(VGroup(kinetic_eq, potential_eq), DOWN, buff=0.5)

        substitute_text = Text("代入すると...", font_size=24, color=WHITE)
        substitute_text.next_to(arrow, RIGHT, buff=0.3)

        self.play(Write(arrow), Write(substitute_text), run_time=0.8)
        self.wait(0.5)

        # 最終形: L = ½mv² - mgh
        final_eq = MathTex(
            r"L", r"=", r"\frac{1}{2}mv^2", r"-", r"mgh",
            font_size=56
        )
        final_eq[0].set_color(LAGRANGIAN_COLOR)
        final_eq[2].set_color(KINETIC_COLOR)
        final_eq[4].set_color(POTENTIAL_COLOR)
        final_eq.next_to(arrow, DOWN, buff=0.5)

        # 強調用のボックス
        final_box = SurroundingRectangle(
            final_eq,
            color=LAGRANGIAN_COLOR,
            buff=0.2,
            stroke_width=3
        )

        self.play(Write(final_eq), run_time=2.0)
        self.play(Create(final_box), run_time=0.8)
        self.wait(1.0)

        # ========== 8. 説明テキスト ==========
        explanation = Text(
            "物体の運動の全情報が詰まった関数",
            font_size=28,
            color=YELLOW
        )
        explanation.next_to(final_box, DOWN, buff=0.5)

        self.play(Write(explanation), run_time=1.5)

        # 点滅効果
        for _ in range(2):
            self.play(explanation.animate.set_opacity(0.3), run_time=0.3)
            self.play(explanation.animate.set_opacity(1.0), run_time=0.3)

        self.wait(2.0)

        # ========== 9. フェードアウト ==========
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.0)


if __name__ == "__main__":
    # コマンドラインから実行する場合
    # manim -pql lagrangian_introduction_manim.py LagrangianIntroduction
    pass
