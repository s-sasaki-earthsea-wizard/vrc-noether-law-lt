#!/usr/bin/env python3
"""
2つのボールが同じ高さから時間差で順次落下するアニメーション

左のボールが地面に到達した後に、右のボールが落下を開始する。
約15秒のアニメーション。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

# 物理定数
g = 9.8  # 重力加速度 [m/s²]

# ボールの設定
height = 25.0  # 両ボールの初期高さ [m]
n_balls = 2

# タイミング設定
start_pause = 2.0  # 開始前のポーズ [秒]
delay = 2.0  # 左のボールが着地後、右のボールが落下開始するまでの遅延 [秒]
end_pause = 4.0  # 最後のポーズ [秒]

# 落下時間を計算
fall_time = np.sqrt(2 * height / g)

# 各ボールの落下開始時刻を計算
start_times = [
    start_pause,  # 左のボール: 開始ポーズ後に落下開始
    start_pause + fall_time + delay  # 右のボール: 左が着地してから遅延後に落下開始
]

# 総アニメーション時間
t_max = start_times[1] + fall_time + end_pause

# アニメーション設定
fps = 60
dt = 1.0 / fps
n_frames = int(t_max / dt) + 1

# 時間配列
t_array = np.linspace(0, t_max, n_frames)

# 図の設定
fig = plt.figure(figsize=(16, 10), facecolor='black')
ax = fig.add_subplot(111, facecolor='black')

# 軸の設定（高さ25mに対応）
ax.set_xlim(-20, 20)
ax.set_ylim(-3, 32)
ax.set_aspect('equal')
ax.axis('off')

# 地面の描画
ground_line = plt.Line2D([-20, 20], [0, 0], color='white', linewidth=3)
ax.add_line(ground_line)

# ボールのX座標（左と右、間隔2倍）
ball_x_positions = [-10, 10]

# ボールを作成
particles = []
for i, x in enumerate(ball_x_positions):
    particle = Circle((x, height), 0.5, color='yellow', zorder=10)
    ax.add_patch(particle)
    particles.append(particle)

# 初期高さの参照線（画面全体を通る破線）
ref_line = plt.Line2D([-20, 20], [height, height],
                      color='gray', linewidth=2, linestyle='--', alpha=0.5)
ax.add_line(ref_line)


def init():
    """アニメーションの初期化"""
    for i, particle in enumerate(particles):
        particle.center = (ball_x_positions[i], height)
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
            h = height
        elif t_elapsed <= fall_time:
            # 落下中
            h = height - 0.5 * g * t_elapsed**2
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
print(f"ボールの高さ: {height}m")
print(f"落下時間: {fall_time:.2f}秒")
print(f"開始時刻: 左={start_times[0]:.2f}秒, 右={start_times[1]:.2f}秒")
print(f"総時間: {t_max:.2f}秒")
print(f"フレーム数: {n_frames}")
print(f"フレームレート: {fps} fps")

writer = animation.FFMpegWriter(fps=fps, bitrate=1800,
                                extra_args=['-vcodec', 'libx264'])
anim.save('free_fall_two_balls_sequential.mp4', writer=writer, dpi=150)

print("完成！ファイル: free_fall_two_balls_sequential.mp4")
plt.close()
