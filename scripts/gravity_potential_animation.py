#!/usr/bin/env python3
"""
重力ポテンシャルの等ポテンシャル線と勾配方向を視覚化するアニメーション

地球を平面近似した場合の重力場を表示し、
等ポテンシャル線（水平な破線）と勾配方向（鉛直下向きの矢印）を
順番に描画することで、空間が鉛直方向に一様でないことを示す。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyArrowPatch
import matplotlib

# 日本語フォントの設定（macOS）
matplotlib.rcParams['font.family'] = 'Hiragino Sans'

# アニメーション設定
fps = 60
duration = 15.0  # 15秒
n_frames = int(fps * duration)

# 等ポテンシャル線の設定
n_lines = 6  # 等ポテンシャル線の本数
line_heights = np.linspace(1.5, 9.0, n_lines)  # 各線の高さ

# 矢印の設定
n_arrows = 5  # 矢印の本数
arrow_x_positions = np.linspace(1.5, 10.5, n_arrows)  # 矢印のx位置

# タイミング設定（フレーム数で管理）
frames_per_line = int(n_frames * 0.4 / n_lines)  # 各線を引く時間（全体の40%を線描画に使用）
line_start_frames = [int(n_frames * 0.05) + i * frames_per_line for i in range(n_lines)]
arrow_start_frame = line_start_frames[-1] + frames_per_line + int(n_frames * 0.05)  # 線が終わって少し間を置く
arrow_duration = int(n_frames * 0.25)  # 矢印を伸ばす時間
label_start_frame = int(n_frames * 0.02)  # ラベル表示開始

# 図の設定
fig, ax = plt.subplots(figsize=(14, 8), facecolor='black')
ax.set_facecolor('black')
ax.set_xlim(0, 12)
ax.set_ylim(-1.5, 11)
ax.set_aspect('equal')
ax.axis('off')

# タイトル
title_text = ax.text(6, 10.3, '重力ポテンシャルと勾配', color='white',
                     ha='center', fontsize=20, weight='bold')

# 地面の描画
ground_line = plt.Line2D([0.5, 11.5], [0, 0], color='#8B4513', linewidth=4)
ax.add_line(ground_line)

# 地面のハッチング（茶色）
for i in range(23):
    hatch = plt.Line2D([0.5 + i * 0.5, 0.7 + i * 0.5], [0, -0.4],
                       color='#8B4513', linewidth=2)
    ax.add_line(hatch)

# 地面ラベル
ax.text(6, -1.0, '地面 (h = 0)', color='#DEB887', ha='center', fontsize=12)

# 等ポテンシャル線のオブジェクトを格納するリスト
potential_lines = []
for i, h in enumerate(line_heights):
    # 各等ポテンシャル線（最初は見えない）
    line, = ax.plot([], [], color='#00BFFF', linewidth=2, linestyle='--', alpha=0.8)
    potential_lines.append(line)

# 勾配方向の矢印を格納するリスト
gradient_arrows = []
for x in arrow_x_positions:
    # 矢印の始点と終点
    arrow = FancyArrowPatch((x, 8.5), (x, 8.5),  # 最初は長さ0
                            arrowstyle='->', mutation_scale=20,
                            color='#FF6347', linewidth=3, alpha=0.9)
    ax.add_patch(arrow)
    gradient_arrows.append(arrow)

# ラベルテキスト
energy_label = ax.text(11.5, 5.5, '', color='#FFD700', ha='right', fontsize=16,
                       weight='bold')

# 高さ方向の矢印（位置エネルギーが高さで変わることを示す）
# 地面から上向きに伸びる片矢印
height_indicator = ax.annotate('', xy=(0.8, 9.0), xytext=(0.8, 0),
                               arrowprops=dict(arrowstyle='->', color='#FFD700',
                                             lw=2, mutation_scale=15),
                               fontsize=12, color='#FFD700')
height_label = ax.text(0.5, 4.5, 'h', color='#FFD700', ha='center', fontsize=16,
                       weight='bold', rotation=90, alpha=0)


def init():
    """アニメーションの初期化"""
    for line in potential_lines:
        line.set_data([], [])
    for arrow in gradient_arrows:
        arrow.set_positions((arrow_x_positions[0], 8.5), (arrow_x_positions[0], 8.5))
        arrow.set_alpha(0)
    energy_label.set_text('')
    height_label.set_alpha(0)
    height_indicator.set_visible(False)
    return potential_lines + gradient_arrows + [energy_label, height_label, height_indicator]


def animate(frame):
    """各フレームの更新"""

    # ========== ラベル表示 ==========
    if frame >= label_start_frame:
        energy_label.set_text('位置エネルギー\n= mgh')
        height_label.set_alpha(1.0)
        height_indicator.set_visible(True)

    # ========== 等ポテンシャル線の描画 ==========
    for i, (line, h) in enumerate(zip(potential_lines, line_heights)):
        start_frame = line_start_frames[i]
        end_frame = start_frame + frames_per_line

        if frame < start_frame:
            # まだ描画開始前
            line.set_data([], [])
        elif frame < end_frame:
            # 描画中（左から右へ）
            progress = (frame - start_frame) / frames_per_line
            x_end = 0.5 + progress * 11.0  # 0.5から11.5まで
            x_data = [0.5, x_end]
            y_data = [h, h]
            line.set_data(x_data, y_data)
        else:
            # 描画完了
            line.set_data([0.5, 11.5], [h, h])

    # ========== 勾配方向の矢印の描画 ==========
    if frame >= arrow_start_frame:
        arrow_progress = min(1.0, (frame - arrow_start_frame) / arrow_duration)
        # イージング関数（スムーズな動き）
        eased_progress = 1 - (1 - arrow_progress) ** 2

        arrow_length = eased_progress * 6.5  # 最大長さ

        for i, (arrow, x) in enumerate(zip(gradient_arrows, arrow_x_positions)):
            arrow.set_alpha(0.9)
            # 矢印の位置を更新（上から下へ伸びる）
            start_y = 9.0
            end_y = start_y - arrow_length
            if end_y < 1.0:
                end_y = 1.0
            arrow.set_positions((x, start_y), (x, end_y))

    return potential_lines + gradient_arrows + [energy_label, height_label, height_indicator]


# アニメーションの作成
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=n_frames, interval=1000/fps,
                               blit=False, repeat=True)

# MP4として保存
print("アニメーションを生成しています...")
print(f"等ポテンシャル線: {n_lines}本")
print(f"勾配矢印: {n_arrows}本")
print(f"アニメーション時間: {duration}秒")
print(f"フレーム数: {n_frames}")
print(f"フレームレート: {fps} fps")

writer = animation.FFMpegWriter(fps=fps, bitrate=2000,
                                extra_args=['-vcodec', 'libx264'])
anim.save('gravity_potential.mp4', writer=writer, dpi=150)

print("完成！ファイル: gravity_potential.mp4")
plt.close()
