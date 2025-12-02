#!/usr/bin/env python3
"""
ネーターチャージの統一アニメーション（manim版）

セクション7-8: 3つの対称性から生まれる保存量が
すべて「ネーターチャージ」として統一されることを視覚化する。

時間をずらす → エネルギー
横にずらす   → 運動量
回転させる   → 角運動量

これらがすべてネーターチャージ Q の具体例であることを示す。
"""

from manim import *


class NoetherChargeUnification(Scene):
    """ネーターチャージの統一を示すシーン"""

    def construct(self):
        # 色の設定（既存スクリプトと統一）
        SYMMETRY_COLOR = GREEN_C
        CONSERVED_COLOR = YELLOW
        HIGHLIGHT_COLOR = RED_C
        BOX_COLOR = TEAL_C

        # ========== 1. 3つの「ずらす操作」を表示 ==========

        # タイトル
        title = Text("ずらす操作と保存量", font_size=32, color=WHITE)
        title.to_edge(UP, buff=0.5)

        self.play(Write(title), run_time=0.8)
        self.wait(0.3)

        # 3つの対称性（横並び）
        symmetry_time = Text("時間をずらす", font_size=28, color=SYMMETRY_COLOR)
        symmetry_space = Text("横にずらす", font_size=28, color=SYMMETRY_COLOR)
        symmetry_rotation = Text("回転させる", font_size=28, color=SYMMETRY_COLOR)

        symmetries = VGroup(symmetry_time, symmetry_space, symmetry_rotation)
        symmetries.arrange(RIGHT, buff=1.5)
        symmetries.next_to(title, DOWN, buff=0.8)

        self.play(
            Write(symmetry_time),
            Write(symmetry_space),
            Write(symmetry_rotation),
            run_time=1.5
        )
        self.wait(0.5)

        # ========== 2. 矢印と保存量を表示 ==========

        # 下向き矢印
        arrow1 = MathTex(r"\Downarrow", font_size=36, color=WHITE)
        arrow2 = MathTex(r"\Downarrow", font_size=36, color=WHITE)
        arrow3 = MathTex(r"\Downarrow", font_size=36, color=WHITE)

        arrow1.next_to(symmetry_time, DOWN, buff=0.3)
        arrow2.next_to(symmetry_space, DOWN, buff=0.3)
        arrow3.next_to(symmetry_rotation, DOWN, buff=0.3)

        self.play(
            Write(arrow1),
            Write(arrow2),
            Write(arrow3),
            run_time=0.5
        )

        # 保存量（テキストで表示）
        conserved_energy = Text("エネルギー", font_size=28, color=CONSERVED_COLOR)
        conserved_momentum = Text("運動量", font_size=28, color=CONSERVED_COLOR)
        conserved_angular = Text("角運動量", font_size=28, color=CONSERVED_COLOR)

        conserved_energy.next_to(arrow1, DOWN, buff=0.3)
        conserved_momentum.next_to(arrow2, DOWN, buff=0.3)
        conserved_angular.next_to(arrow3, DOWN, buff=0.3)

        self.play(
            Write(conserved_energy),
            Write(conserved_momentum),
            Write(conserved_angular),
            run_time=1.0
        )
        self.wait(1.0)

        # ========== 3. 統一へ向かうアニメーション ==========

        # 上部をフェードアウト
        self.play(
            FadeOut(title),
            FadeOut(symmetries),
            FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow3),
            run_time=0.5
        )

        # 3つの保存量を中央上部に移動
        conserved_group = VGroup(conserved_energy, conserved_momentum, conserved_angular)

        self.play(
            conserved_group.animate.arrange(RIGHT, buff=0.8).move_to(ORIGIN + UP * 2.0),
            run_time=1.0
        )
        self.wait(0.3)

        # 「すべて同じ構造」のテキスト
        same_structure = Text("すべて同じ構造から生まれる", font_size=24, color=WHITE)
        same_structure.next_to(conserved_group, DOWN, buff=0.5)

        self.play(Write(same_structure), run_time=0.8)
        self.wait(0.5)

        # 下向き矢印
        arrow_unify = MathTex(r"\Downarrow", font_size=48, color=WHITE)
        arrow_unify.next_to(same_structure, DOWN, buff=0.3)

        self.play(Write(arrow_unify), run_time=0.3)

        # ========== 4. 一般形の式を表示 ==========

        # ネーターチャージの一般形
        general_formula = MathTex(
            r"Q = \frac{\partial L}{\partial \dot{q}} \cdot \delta q",
            font_size=44,
            color=CONSERVED_COLOR
        )
        general_formula.next_to(arrow_unify, DOWN, buff=0.4)

        self.play(Write(general_formula), run_time=1.5)
        self.wait(0.8)

        # ========== 5. シンプルな意味を表示 ==========

        # 「= 一定」を追加（日本語はTextで表示）
        const_text = Text("= 一定", font_size=36, color=CONSERVED_COLOR)
        const_text.next_to(general_formula, RIGHT, buff=0.2)

        self.play(Write(const_text), run_time=0.5)
        self.wait(0.3)

        # 式全体をグループ化
        formula_group = VGroup(general_formula, const_text)

        # ネーターチャージのラベル
        charge_label = Text("ネーターチャージ", font_size=32, color=BOX_COLOR)
        charge_label.next_to(formula_group, DOWN, buff=0.5)

        # ボックスで囲む
        formula_with_label = VGroup(formula_group, charge_label)
        box = SurroundingRectangle(
            formula_with_label,
            color=BOX_COLOR,
            buff=0.3,
            stroke_width=3
        )

        self.play(
            Write(charge_label),
            Create(box),
            run_time=1.0
        )
        self.wait(0.5)

        # ========== 6. 最終メッセージ ==========

        # 上部の要素をフェードアウトしてすっきりさせる
        self.play(
            FadeOut(conserved_group),
            FadeOut(same_structure),
            FadeOut(arrow_unify),
            VGroup(formula_with_label, box).animate.move_to(ORIGIN + UP * 0.5),
            run_time=0.8
        )

        # 最終メッセージ
        final_message = Text(
            "エネルギーも運動量も角運動量も\nすべてネーターチャージの具体例",
            font_size=26,
            color=WHITE,
            line_spacing=1.2
        )
        final_message.next_to(box, DOWN, buff=0.6)

        self.play(Write(final_message), run_time=1.5)

        # ボックスを点滅
        for _ in range(2):
            self.play(
                box.animate.set_stroke(color=WHITE, width=5),
                run_time=0.2
            )
            self.play(
                box.animate.set_stroke(color=BOX_COLOR, width=3),
                run_time=0.2
            )

        self.wait(1.5)

        # 全体をフェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


if __name__ == "__main__":
    # コマンドラインから実行する場合
    # manim -pql noether_charge_unification.py NoetherChargeUnification
    # 高品質版: manim -pqh noether_charge_unification.py NoetherChargeUnification
    pass
