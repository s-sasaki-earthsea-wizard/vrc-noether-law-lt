#!/usr/bin/env python3
"""
水平方向の移動は等ポテンシャル線上を動くだけ、という説明のアニメーション

3本の等ポテンシャル線（位置エネルギーが等しい線）を表示し、
真ん中の線上でボールが水平方向に移動することで、
水平移動では位置エネルギーが変化しないことを視覚的に示す。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import matplotlib

# 日本語フォントの設定（macOS）
matplotlib.rcParams['font.family'] = 'Hiragino Sans'

# アニメーション設定
fps = 60
duration = 15.0  # 15秒
n_frames = int(fps * duration)

# 等ポテンシャル線の設定（3本）
line_heights = [5.0, 10.0, 15.0]  # 5m, 10m, 15m
middle_height = line_heights[1]  # 真ん中の線（10m）

# ボールの移動設定
ball_start_x = 1.5
ball_end_x = 10.5

# タイミング設定
line_draw_duration = int(n_frames * 0.25)  # 線を引く時間（全体の25%）
ball_start_frame = line_draw_duration + int(fps * 1.0)  # 線を引き終わって1秒後
ball_move_duration = int(n_frames * 0.55)  # ボールの移動時間（全体の55%）

# 図の設定
fig, ax = plt.subplots(figsize=(14, 8), facecolor='black')
ax.set_facecolor('black')
ax.set_xlim(0, 12)
ax.set_ylim(-2, 18)
ax.set_aspect('equal')
ax.axis('off')

# 地面の描画
ground_line = plt.Line2D([0.5, 11.5], [0, 0], color='#8B4513', linewidth=4)
ax.add_line(ground_line)

# 地面のハッチング（茶色）
for i in range(23):
    hatch = plt.Line2D([0.5 + i * 0.5, 0.7 + i * 0.5], [0, -0.5],
                       color='#8B4513', linewidth=2)
    ax.add_line(hatch)

# 地面ラベル
ax.text(6, -1.2, '地面 (h = 0)', color='#DEB887', ha='center', fontsize=12)

# 等ポテンシャル線のオブジェクトを格納するリスト
potential_lines = []
line_labels = []
for i, h in enumerate(line_heights):
    # 各等ポテンシャル線（最初は見えない）
    line, = ax.plot([], [], color='#00BFFF', linewidth=2.5, linestyle='--', alpha=0.8)
    potential_lines.append(line)

    # 高さラベル（右側に表示）
    label = ax.text(11.7, h, f'h = {int(h)}m', color='#00BFFF',
                    ha='left', va='center', fontsize=12, alpha=0)
    line_labels.append(label)

# ボール（最初は見えない）
ball = Circle((ball_start_x, middle_height), 0.4, color='yellow', zorder=10, alpha=0)
ax.add_patch(ball)

# タイトルラベル
title_label = ax.text(6, 16.5, '位置エネルギーが等しい線', color='#00BFFF',
                      ha='center', fontsize=18, weight='bold', alpha=0)

# 説明テキスト（ボール移動中に表示）
explanation_text = ax.text(6, -1.8, '', color='#FFD700',
                           ha='center', fontsize=14, weight='bold')


def init():
    """アニメーションの初期化"""
    for line in potential_lines:
        line.set_data([], [])
    for label in line_labels:
        label.set_alpha(0)
    ball.set_alpha(0)
    ball.center = (ball_start_x, middle_height)
    title_label.set_alpha(0)
    explanation_text.set_text('')
    return potential_lines + line_labels + [ball, title_label, explanation_text]


def animate(frame):
    """各フレームの更新"""

    # ========== 等ポテンシャル線の描画（同時に3本を左から右へ） ==========
    if frame < line_draw_duration:
        progress = frame / line_draw_duration
        # イージング（スムーズな動き）
        eased_progress = 1 - (1 - progress) ** 2
        x_end = 0.5 + eased_progress * 11.0  # 0.5から11.5まで

        for i, (line, h) in enumerate(zip(potential_lines, line_heights)):
            line.set_data([0.5, x_end], [h, h])

        # タイトルのフェードイン
        title_label.set_alpha(min(1.0, progress * 2))
    else:
        # 線の描画完了
        for i, (line, h) in enumerate(zip(potential_lines, line_heights)):
            line.set_data([0.5, 11.5], [h, h])
        title_label.set_alpha(1.0)

        # ラベルのフェードイン
        label_fade_progress = min(1.0, (frame - line_draw_duration) / (fps * 0.5))
        for label in line_labels:
            label.set_alpha(label_fade_progress)

    # ========== ボールの移動 ==========
    if frame >= ball_start_frame:
        ball.set_alpha(1.0)

        move_frame = frame - ball_start_frame
        if move_frame < ball_move_duration:
            # 移動中
            progress = move_frame / ball_move_duration
            # イージング（ゆっくり始まり、ゆっくり終わる）
            eased_progress = progress * progress * (3 - 2 * progress)  # smoothstep

            x = ball_start_x + eased_progress * (ball_end_x - ball_start_x)
            ball.center = (x, middle_height)

            # 説明テキスト表示
            explanation_text.set_text('水平移動 → 位置エネルギー変化なし')
        else:
            # 移動完了
            ball.center = (ball_end_x, middle_height)
            explanation_text.set_text('水平移動 → 位置エネルギー変化なし')

    return potential_lines + line_labels + [ball, title_label, explanation_text]


# アニメーションの作成
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=n_frames, interval=1000/fps,
                               blit=False, repeat=True)

# MP4として保存
print("アニメーションを生成しています...")
print(f"等ポテンシャル線: {len(line_heights)}本 (h = {line_heights})")
print(f"ボール移動: h = {middle_height}m の線上")
print(f"アニメーション時間: {duration}秒")
print(f"フレーム数: {n_frames}")
print(f"フレームレート: {fps} fps")

writer = animation.FFMpegWriter(fps=fps, bitrate=2000,
                                extra_args=['-vcodec', 'libx264'])
anim.save('equipotential_horizontal_motion.mp4', writer=writer, dpi=150)

print("完成！ファイル: equipotential_horizontal_motion.mp4")
plt.close()
