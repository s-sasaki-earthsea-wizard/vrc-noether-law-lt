#!/usr/bin/env python3
"""
発展的な保存則アニメーション（manim版）

セクション8「より広い世界へ」用。
エネルギー運動量テンソルの保存と電荷保存則を順番に表示。
"""

from manim import *


class AdvancedConservationLaws(Scene):
    """発展的な保存則を順番に表示するシーン"""

    def construct(self):
        # 色の設定
        TENSOR_COLOR = TEAL_C
        CHARGE_COLOR = ORANGE

        # ========== 1. タイトル ==========

        title = Text("ネーターの定理の広がり", font_size=32, color=WHITE)
        title.to_edge(UP, buff=0.5)

        self.play(Write(title), run_time=0.8)
        self.wait(0.3)

        # ========== 2. 左側: エネルギー運動量テンソル ==========

        # ラベル
        tensor_label = Text("相対論", font_size=28, color=WHITE)

        # 式
        tensor_eq = MathTex(
            r"\nabla_\mu T^{\mu\nu} = 0",
            font_size=44,
            color=TENSOR_COLOR
        )

        # 説明
        tensor_desc = Text("エネルギー-運動量テンソルの保存", font_size=20, color=TENSOR_COLOR)

        # グループ化して左に配置
        tensor_group = VGroup(tensor_label, tensor_eq, tensor_desc).arrange(DOWN, buff=0.3)
        tensor_group.move_to(LEFT * 2.5 + DOWN * 0.5)

        # 順番に表示
        self.play(Write(tensor_label), run_time=0.5)
        self.play(Write(tensor_eq), run_time=1.0)
        self.play(Write(tensor_desc), run_time=0.6)

        tensor_box = SurroundingRectangle(tensor_group, color=TENSOR_COLOR, buff=0.2, stroke_width=2)
        self.play(Create(tensor_box), run_time=0.4)

        self.wait(0.5)

        # ========== 3. 右側: 電荷保存則 ==========

        # ラベル
        charge_label = Text("素粒子物理学", font_size=28, color=WHITE)

        # 式
        charge_eq = MathTex(
            r"\partial_\mu j^\mu = 0",
            font_size=44,
            color=CHARGE_COLOR
        )

        # 説明
        charge_desc = Text("電荷保存則", font_size=20, color=CHARGE_COLOR)

        # グループ化して右に配置
        charge_group = VGroup(charge_label, charge_eq, charge_desc).arrange(DOWN, buff=0.3)
        charge_group.move_to(RIGHT * 2.5 + DOWN * 0.5)

        # 順番に表示
        self.play(Write(charge_label), run_time=0.5)
        self.play(Write(charge_eq), run_time=1.0)
        self.play(Write(charge_desc), run_time=0.6)

        charge_box = SurroundingRectangle(charge_group, color=CHARGE_COLOR, buff=0.2, stroke_width=2)
        self.play(Create(charge_box), run_time=0.4)

        self.wait(1.5)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


if __name__ == "__main__":
    # manim -pql advanced_conservation_laws.py AdvancedConservationLaws
    pass
