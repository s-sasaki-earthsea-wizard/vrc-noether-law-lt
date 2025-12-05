#!/usr/bin/env python3
"""
横方向の対称性を示すアニメーション

4つのボールを横に並べて同じ高さ(25m)から同時に落下させる。
横方向にずらしても落下の結果は変わらないことを視覚的に示す。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

# 物理定数
g = 9.8  # 重力加速度 [m/s²]
h0 = 25.0  # 初期高さ [m]

# 落下時間の計算
t_fall = np.sqrt(2 * h0 / g)

# アニメーション設定
fps = 60
dt = 1.0 / fps
n_frames = int(t_fall / dt) + 1

# 時間配列
t_array = np.linspace(0, t_fall, n_frames)

# 図の設定
fig = plt.figure(figsize=(12, 8), facecolor='black')
ax = fig.add_subplot(111, facecolor='black')

# 軸の設定
ax.set_xlim(-1, 13)
ax.set_ylim(-2, 28)
ax.set_aspect('equal')
ax.axis('off')

# 地面の描画
ground_line = plt.Line2D([0, 12], [0, 0], color='white', linewidth=3)
ax.add_line(ground_line)

# 地面のハッチング
for i in range(28):
    hatch = plt.Line2D([i * 0.45, 0.2 + i * 0.45], [0, -0.5], color='white', linewidth=1)
    ax.add_line(hatch)

# 4つのボールの横位置（等間隔）
x_positions = [2, 5, 8, 11]

# ボールの作成（同じ色：黄色）
particles = []
for x in x_positions:
    particle = Circle((x, h0), 0.4, color='yellow', zorder=10)
    ax.add_patch(particle)
    particles.append(particle)

# 初期高さの参照線
reference_line = plt.Line2D([0.5, 12.5], [h0, h0],
                            color='gray', linewidth=1, linestyle='--', alpha=0.5)
ax.add_line(reference_line)


def init():
    """アニメーションの初期化"""
    for i, particle in enumerate(particles):
        particle.center = (x_positions[i], h0)
    return particles


def animate(frame):
    """各フレームの更新"""
    t = t_array[frame]

    # 高さの計算
    h = h0 - 0.5 * g * t**2

    # 地面チェック
    if h < 0:
        h = 0

    # 全てのボールを同じ高さに更新
    for i, particle in enumerate(particles):
        particle.center = (x_positions[i], h)

    return particles


# アニメーションの作成
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=n_frames, interval=dt*1000,
                               blit=False, repeat=True)

# MP4として保存
print("アニメーションを生成しています...")
print(f"初期高さ: {h0:.1f}m")
print(f"落下時間: {t_fall:.2f}秒")
print(f"フレーム数: {n_frames}")
print(f"フレームレート: {fps} fps")

writer = animation.FFMpegWriter(fps=fps, bitrate=1800,
                                extra_args=['-vcodec', 'libx264'])
anim.save('free_fall_four_horizontal.mp4', writer=writer, dpi=150)

print("完成！ファイル: free_fall_four_horizontal.mp4")
plt.close()
