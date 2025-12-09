#!/usr/bin/env python3
"""
相対論とゲージ対称性のアニメーション（manim版）

セクション8「より広い世界へ」用。
1. 光円錐（ミンコフスキー時空図）
2. U(1)ゲージ対称性（位相の回転）
"""

from manim import *
import numpy as np


class LightConeAnimation(ThreeDScene):
    """光円錐を描くシーン（3D版）- OpenGLレンダラー用"""

    def construct(self):
        # 色の設定
        FUTURE_COLOR = YELLOW
        PAST_COLOR = BLUE_C
        AXIS_COLOR = WHITE

        # カメラ設定
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        # ========== 1. 座標軸 ==========
        # 時間軸（ct）
        t_axis = Arrow3D(
            start=[0, 0, -2.5],
            end=[0, 0, 2.5],
            color=AXIS_COLOR,
            thickness=0.02
        )

        # x軸
        x_axis = Arrow3D(
            start=[-2.5, 0, 0],
            end=[2.5, 0, 0],
            color=AXIS_COLOR,
            thickness=0.02
        )

        # y軸
        y_axis = Arrow3D(
            start=[0, -2.5, 0],
            end=[0, 2.5, 0],
            color=AXIS_COLOR,
            thickness=0.02
        )

        self.play(
            Create(t_axis), Create(x_axis), Create(y_axis),
            run_time=1.0
        )

        # ========== 2. 光円錐の表面 ==========
        # 未来光円錐（上向きの円錐）
        future_cone = Surface(
            lambda u, v: np.array([
                v * np.cos(u),
                v * np.sin(u),
                v  # ct = r（光速で進む）
            ]),
            u_range=[0, TAU],
            v_range=[0, 2],
            resolution=(32, 16),
            fill_opacity=0.3,
            stroke_width=0.5,
            stroke_color=FUTURE_COLOR,
            fill_color=FUTURE_COLOR,
        )

        # 過去光円錐（下向きの円錐）
        past_cone = Surface(
            lambda u, v: np.array([
                v * np.cos(u),
                v * np.sin(u),
                -v  # ct = -r
            ]),
            u_range=[0, TAU],
            v_range=[0, 2],
            resolution=(32, 16),
            fill_opacity=0.3,
            stroke_width=0.5,
            stroke_color=PAST_COLOR,
            fill_color=PAST_COLOR,
        )

        self.play(Create(future_cone), run_time=1.5)
        self.play(Create(past_cone), run_time=1.5)

        # ========== 3. 原点（イベント） ==========
        origin_dot = Sphere(radius=0.1, color=RED)
        origin_dot.move_to(ORIGIN)
        self.play(Create(origin_dot), run_time=0.5)

        # ========== 4. カメラ回転 ==========
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()

        self.wait(1)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


class LightCone2D(Scene):
    """光円錐を描くシーン（2D版 - シンプル）"""

    def construct(self):
        # 色の設定
        FUTURE_COLOR = YELLOW
        PAST_COLOR = BLUE_C
        LIGHTLIKE_COLOR = ORANGE
        AXIS_COLOR = WHITE

        # ========== 1. タイトル ==========
        title = Text("光円錐 — 時空の因果構造", font_size=32, color=WHITE)
        title.to_edge(UP, buff=0.5)

        self.play(Write(title), run_time=0.8)

        # ========== 2. 座標軸 ==========
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": AXIS_COLOR, "include_tip": True},
        )

        x_label = MathTex("x", font_size=36, color=AXIS_COLOR)
        x_label.next_to(axes.x_axis.get_end(), RIGHT)

        t_label = MathTex("ct", font_size=36, color=AXIS_COLOR)
        t_label.next_to(axes.y_axis.get_end(), UP)

        self.play(Create(axes), run_time=1.0)
        self.play(Write(x_label), Write(t_label), run_time=0.5)

        # ========== 3. 光円錐の線（45度の線） ==========
        # 光の世界線: ct = x と ct = -x
        light_line1 = axes.plot(lambda x: x, x_range=[-2.5, 2.5], color=LIGHTLIKE_COLOR, stroke_width=3)
        light_line2 = axes.plot(lambda x: -x, x_range=[-2.5, 2.5], color=LIGHTLIKE_COLOR, stroke_width=3)

        self.play(Create(light_line1), Create(light_line2), run_time=1.0)

        # ========== 4. 未来と過去の領域 ==========
        # 未来領域（上の三角形）
        future_region = Polygon(
            axes.c2p(0, 0),
            axes.c2p(-2.5, 2.5),
            axes.c2p(2.5, 2.5),
            fill_color=FUTURE_COLOR,
            fill_opacity=0.3,
            stroke_width=0,
        )

        # 過去領域（下の三角形）
        past_region = Polygon(
            axes.c2p(0, 0),
            axes.c2p(-2.5, -2.5),
            axes.c2p(2.5, -2.5),
            fill_color=PAST_COLOR,
            fill_opacity=0.3,
            stroke_width=0,
        )

        self.play(FadeIn(future_region), FadeIn(past_region), run_time=1.0)

        # ========== 5. ラベル ==========
        future_label = Text("未来", font_size=28, color=FUTURE_COLOR)
        future_label.move_to(axes.c2p(0, 1.8))

        past_label = Text("過去", font_size=28, color=PAST_COLOR)
        past_label.move_to(axes.c2p(0, -1.8))

        space_right = Text("空間的", font_size=20, color=GREEN_C)
        space_right.move_to(axes.c2p(2, 0))

        space_left = Text("空間的", font_size=20, color=GREEN_C)
        space_left.move_to(axes.c2p(-2, 0))

        self.play(
            Write(future_label), Write(past_label),
            Write(space_right), Write(space_left),
            run_time=0.8
        )

        # ========== 6. 原点 ==========
        origin_dot = Dot(axes.c2p(0, 0), color=RED, radius=0.1)
        origin_label = Text("現在", font_size=20, color=RED)
        origin_label.next_to(origin_dot, DOWN + LEFT, buff=0.2)

        self.play(Create(origin_dot), Write(origin_label), run_time=0.5)

        # ========== 7. 光の世界線ラベル ==========
        light_label = MathTex(r"v = c", font_size=28, color=LIGHTLIKE_COLOR)
        light_label.move_to(axes.c2p(1.8, 2.2))

        self.play(Write(light_label), run_time=0.5)

        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


class GaugePhaseRotation(Scene):
    """U(1)ゲージ対称性 - 位相の回転を示すシーン"""

    def construct(self):
        # 色の設定
        PHASE_COLOR = TEAL_C
        ARROW_COLOR = ORANGE
        CHARGE_COLOR = YELLOW

        # ========== 1. タイトル ==========
        title = Text("ゲージ対称性 — 位相の回転", font_size=32, color=WHITE)
        title.to_edge(UP, buff=0.5)

        self.play(Write(title), run_time=0.8)

        # ========== 2. 複素平面 ==========
        plane = ComplexPlane(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=5,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
        )
        plane.shift(LEFT * 2.5)

        # 軸ラベル
        re_label = MathTex(r"\mathrm{Re}", font_size=28, color=WHITE)
        re_label.next_to(plane.get_right(), RIGHT, buff=0.1)

        im_label = MathTex(r"\mathrm{Im}", font_size=28, color=WHITE)
        im_label.next_to(plane.get_top(), UP, buff=0.1)

        self.play(Create(plane), run_time=1.0)
        self.play(Write(re_label), Write(im_label), run_time=0.5)

        # ========== 3. 単位円 ==========
        unit_circle = Circle(radius=plane.get_x_unit_size(), color=PHASE_COLOR, stroke_width=2)
        unit_circle.move_to(plane.get_origin())

        self.play(Create(unit_circle), run_time=0.8)

        # ========== 4. 波動関数を表す矢印 ==========
        # 矢印の長さ（単位円の半径）
        arrow_length = plane.get_x_unit_size()

        psi_arrow = Arrow(
            start=plane.get_origin(),
            end=plane.get_origin() + arrow_length * RIGHT,
            color=ARROW_COLOR,
            buff=0,
            stroke_width=4,
        )

        psi_label = MathTex(r"\psi", font_size=36, color=ARROW_COLOR)
        psi_label.next_to(psi_arrow.get_end(), UR, buff=0.1)

        self.play(GrowArrow(psi_arrow), Write(psi_label), run_time=0.8)

        # ========== 5. 位相の回転アニメーション ==========
        # 説明テキスト
        phase_text = MathTex(
            r"\psi \to e^{i\theta}\psi",
            font_size=36, color=PHASE_COLOR
        )
        phase_text.move_to(RIGHT * 3 + UP * 1.5)

        self.play(Write(phase_text), run_time=0.8)

        # 角度を追跡する ValueTracker
        angle_tracker = ValueTracker(0)

        # 矢印を角度に応じて更新
        def update_arrow(arrow):
            angle = angle_tracker.get_value()
            new_end = plane.get_origin() + arrow_length * np.array([
                np.cos(angle), np.sin(angle), 0
            ])
            arrow.become(Arrow(
                start=plane.get_origin(),
                end=new_end,
                color=ARROW_COLOR,
                buff=0,
                stroke_width=4,
            ))

        def update_label(label):
            angle = angle_tracker.get_value()
            new_pos = plane.get_origin() + (arrow_length + 0.3) * np.array([
                np.cos(angle), np.sin(angle), 0
            ])
            label.move_to(new_pos)

        psi_arrow.add_updater(update_arrow)
        psi_label.add_updater(update_label)

        # 1回転
        self.play(angle_tracker.animate.set_value(TAU), run_time=3, rate_func=linear)

        psi_arrow.remove_updater(update_arrow)
        psi_label.remove_updater(update_label)

        self.wait(0.5)

        # ========== 6. 「物理は変わらない」の強調 ==========
        invariance_text = Text(
            "位相を変えても物理は変わらない",
            font_size=24, color=GREEN_C
        )
        invariance_text.move_to(RIGHT * 3 + DOWN * 0.5)

        self.play(Write(invariance_text), run_time=0.8)

        # ========== 7. 電荷保存則への導出 ==========
        arrow_to_charge = Arrow(
            start=RIGHT * 3 + DOWN * 1,
            end=RIGHT * 3 + DOWN * 2,
            color=CHARGE_COLOR,
            stroke_width=3,
        )

        charge_text = Text(
            "→ 電荷保存則",
            font_size=28, color=CHARGE_COLOR
        )
        charge_text.move_to(RIGHT * 3 + DOWN * 2.5)

        self.play(GrowArrow(arrow_to_charge), run_time=0.5)
        self.play(Write(charge_text), run_time=0.8)

        # ========== 8. 式の表示 ==========
        continuity_eq = MathTex(
            r"\partial_\mu j^\mu = 0",
            font_size=36, color=CHARGE_COLOR
        )
        continuity_eq.to_edge(DOWN, buff=0.8)

        box = SurroundingRectangle(continuity_eq, color=CHARGE_COLOR, buff=0.15)

        self.play(Write(continuity_eq), Create(box), run_time=1.0)

        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


class GaugePhaseMultiple(Scene):
    """複数の粒子で位相の回転を示すシーン"""

    def construct(self):
        # 色の設定
        PHASE_COLOR = TEAL_C
        COLORS = [RED, BLUE, GREEN, YELLOW]

        # ========== 1. タイトル ==========
        title = Text("ゲージ対称性 — 全ての粒子の位相を同時に回転", font_size=28, color=WHITE)
        title.to_edge(UP, buff=0.5)

        self.play(Write(title), run_time=0.8)

        # ========== 2. 複数の複素平面と矢印 ==========
        planes = []
        arrows = []
        circles = []

        positions = [LEFT * 4.5, LEFT * 1.5, RIGHT * 1.5, RIGHT * 4.5]
        initial_angles = [0, PI/4, PI/2, PI]

        for i, (pos, init_angle) in enumerate(zip(positions, initial_angles)):
            # 小さな複素平面
            plane = ComplexPlane(
                x_range=[-1.5, 1.5, 1],
                y_range=[-1.5, 1.5, 1],
                x_length=2,
                y_length=2,
                background_line_style={
                    "stroke_color": BLUE_E,
                    "stroke_width": 0.5,
                    "stroke_opacity": 0.3,
                },
            )
            plane.move_to(pos)

            # 単位円
            circle = Circle(radius=plane.get_x_unit_size() * 0.8, color=PHASE_COLOR, stroke_width=1)
            circle.move_to(plane.get_origin())

            # 矢印
            arrow_length = plane.get_x_unit_size() * 0.8
            arrow = Arrow(
                start=plane.get_origin(),
                end=plane.get_origin() + arrow_length * np.array([
                    np.cos(init_angle), np.sin(init_angle), 0
                ]),
                color=COLORS[i],
                buff=0,
                stroke_width=3,
            )

            planes.append(plane)
            circles.append(circle)
            arrows.append((arrow, plane.get_origin(), arrow_length, init_angle))

        # 表示
        self.play(
            *[Create(p) for p in planes],
            *[Create(c) for c in circles],
            run_time=1.0
        )
        self.play(*[GrowArrow(a[0]) for a in arrows], run_time=0.5)

        # ========== 3. 同時回転 ==========
        rotation_text = MathTex(
            r"\psi_i \to e^{i\theta}\psi_i \quad (\forall i)",
            font_size=32, color=PHASE_COLOR
        )
        rotation_text.move_to(DOWN * 2)

        self.play(Write(rotation_text), run_time=0.8)

        # 角度トラッカー
        angle_tracker = ValueTracker(0)

        # 各矢印のアップデーター
        for arrow_data, color in zip(arrows, COLORS):
            arrow, origin, length, init_angle = arrow_data

            def make_updater(o, l, ia, c):
                def updater(mob):
                    angle = angle_tracker.get_value()
                    new_end = o + l * np.array([
                        np.cos(ia + angle), np.sin(ia + angle), 0
                    ])
                    mob.become(Arrow(
                        start=o, end=new_end, color=c, buff=0, stroke_width=3
                    ))
                return updater

            arrow.add_updater(make_updater(origin, length, init_angle, color))

        # 1回転
        self.play(angle_tracker.animate.set_value(TAU), run_time=3, rate_func=linear)

        for arrow_data in arrows:
            arrow_data[0].clear_updaters()

        # ========== 4. 結論 ==========
        conclusion = Text(
            "大域的ゲージ対称性 → 電荷保存",
            font_size=28, color=YELLOW
        )
        conclusion.to_edge(DOWN, buff=0.5)

        self.play(
            FadeOut(rotation_text),
            Write(conclusion),
            run_time=1.0
        )

        self.wait(2)

        # フェードアウト
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


if __name__ == "__main__":
    # 実行例:
    # manim -pql scripts/relativity_gauge_animations.py LightCone2D
    # manim -pql scripts/relativity_gauge_animations.py LightConeAnimation
    # manim -pql scripts/relativity_gauge_animations.py GaugePhaseRotation
    # manim -pql scripts/relativity_gauge_animations.py GaugePhaseMultiple
    pass
