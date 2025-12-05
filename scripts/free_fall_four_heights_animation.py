#!/usr/bin/env python3
"""
4つの異なる高さからの順次自由落下アニメーション

25m, 30m, 35m, 40mの高さから順番にボールを落下させる。
左のボールが地面に到達してから0.2秒後に次のボールが落下を開始する。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

# 物理定数
g = 9.8  # 重力加速度 [m/s²]

# 各ボールの初期高さ [m]（左から順に低い順）
heights = [25.0, 30.0, 35.0, 40.0]
n_balls = len(heights)

# タイミング設定
delay = 0.2  # 次のボールが落下開始するまでの遅延 [秒]
end_pause = 1.0  # 最後のポーズ [秒]

# 各ボールの落下時間を計算
fall_times = [np.sqrt(2 * h / g) for h in heights]

# 各ボールの落下開始時刻を計算
start_times = [0.0]  # 最初のボールは t=0 で開始
for i in range(1, n_balls):
    # 前のボールの落下完了時刻 + 遅延
    start_times.append(start_times[i-1] + fall_times[i-1] + delay)

# 総アニメーション時間
t_max = start_times[-1] + fall_times[-1] + end_pause

# アニメーション設定
fps = 60
dt = 1.0 / fps
n_frames = int(t_max / dt) + 1

# 時間配列
t_array = np.linspace(0, t_max, n_frames)

# 図の設定
fig = plt.figure(figsize=(16, 10), facecolor='black')
ax = fig.add_subplot(111, facecolor='black')

# 軸の設定（最大高さ40mに対応）
ax.set_xlim(-12, 22)
ax.set_ylim(-2, 45)
ax.set_aspect('equal')
ax.axis('off')

# 地面の描画
ground_line = plt.Line2D([-12, 21.5], [0, 0], color='white', linewidth=3)
ax.add_line(ground_line)

# 地面のハッチング（装飾）
# for i in range(60):
#     hatch = plt.Line2D([0.5 + i*0.45, 0.7 + i*0.45], [0, -0.5], color='white', linewidth=1)
#     ax.add_line(hatch)

# ボールのX座標
ball_x_positions = -10, 0, 10, 20

# ボールを作成
particles = []
for i, (x, h) in enumerate(zip(ball_x_positions, heights)):
    particle = Circle((x, h), 0.8, color='yellow', zorder=10)
    ax.add_patch(particle)
    particles.append(particle)

# 初期高さの参照線（点線）
for i, (x, h) in enumerate(zip(ball_x_positions, heights)):
    ref_line = plt.Line2D([x - 0.8, x + 0.8], [h, h],
                          color='gray', linewidth=1, linestyle='--', alpha=0.4)
    ax.add_line(ref_line)


def init():
    """アニメーションの初期化"""
    for i, particle in enumerate(particles):
        particle.center = (ball_x_positions[i], heights[i])
    return particles


def animate(frame):
    """各フレームの更新"""
    t = t_array[frame]

    for i, particle in enumerate(particles):
        # このボールの落下開始時刻
        t_start = start_times[i]
        # 落下開始からの経過時間
        t_elapsed = t - t_start

        if t_elapsed < 0:
            # まだ落下開始前
            h = heights[i]
        elif t_elapsed <= fall_times[i]:
            # 落下中
            h = heights[i] - 0.5 * g * t_elapsed**2
        else:
            # 地面に到達後は停止
            h = 0

        # 地面より下に行かないようにする
        if h < 0:
            h = 0

        # 位置を更新
        particle.center = (ball_x_positions[i], h)

    return particles


# アニメーションの作成
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=n_frames, interval=dt*1000,
                               blit=False, repeat=True)

# MP4として保存
print("アニメーションを生成しています...")
print(f"ボールの高さ: {heights}")
print(f"落下時間: {[f'{t:.2f}秒' for t in fall_times]}")
print(f"開始時刻: {[f'{t:.2f}秒' for t in start_times]}")
print(f"総時間: {t_max:.2f}秒")
print(f"フレーム数: {n_frames}")
print(f"フレームレート: {fps} fps")

writer = animation.FFMpegWriter(fps=fps, bitrate=1800,
                                extra_args=['-vcodec', 'libx264'])
anim.save('free_fall_four_heights_animation.mp4', writer=writer, dpi=150)

print("完成！ファイル: free_fall_four_heights_animation.mp4")
plt.close()
