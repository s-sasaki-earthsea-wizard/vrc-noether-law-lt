#!/usr/bin/env python3
"""
自由落下とラグランジアンを視覚化するアニメーション

質点の自由落下と、ラグランジアン L = T - V = (1/2)mv² - mgh のグラフを
時間とともに描画し、ラグランジアンの時間発展を視覚的に示す。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import matplotlib.gridspec as gridspec

# 物理定数
g = 9.8  # 重力加速度 [m/s²]
h0 = 10.0  # 初期高さ [m]
m = 1.0  # 質量 [kg]

# 落下時間の計算
t_fall = np.sqrt(2 * h0 / g)

# アニメーション設定
fps = 60
dt = 1.0 / fps
n_frames = int(t_fall / dt) + 1

# 時間配列
t_array = np.linspace(0, t_fall, n_frames)

# ラグランジアンの計算（全時間範囲）
def lagrangian(t):
    """ラグランジアン L = T - V を計算"""
    v = g * t
    h = h0 - 0.5 * g * t**2
    if h < 0:
        h = 0
        v = np.sqrt(2 * g * h0)
    T = 0.5 * m * v**2
    V = m * g * h
    return T - V

# 全時間範囲でのラグランジアンを事前計算
L_array = np.array([lagrangian(t) for t in t_array])

# 図の設定（2つのサブプロット）
fig = plt.figure(figsize=(14, 6), facecolor='black')
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1.5], wspace=0.3)

# 左側：自由落下のアニメーション
ax_fall = fig.add_subplot(gs[0], facecolor='black')
ax_fall.set_xlim(0, 4)
ax_fall.set_ylim(-1, 12)
ax_fall.set_aspect('equal')
ax_fall.axis('off')

# 地面の描画
ground_line = plt.Line2D([0.5, 3.5], [0, 0], color='white', linewidth=3)
ax_fall.add_line(ground_line)

# 地面のハッチング
for i in range(8):
    hatch = plt.Line2D([0.5 + i*0.4, 0.7 + i*0.4], [0, -0.3], color='white', linewidth=1)
    ax_fall.add_line(hatch)

# 初期高さの参照線
reference_line = plt.Line2D([0.5, 3.5], [h0, h0],
                           color='gray', linewidth=1, linestyle='--', alpha=0.5)
ax_fall.add_line(reference_line)

# 質点（円）
particle = Circle((2, h0), 0.2, color='yellow', zorder=10)
ax_fall.add_patch(particle)

# タイトル
ax_fall.text(2, 11.5, 'Free Fall', color='white', ha='center', fontsize=16, weight='bold')

# 右側：ラグランジアンのグラフ
ax_graph = fig.add_subplot(gs[1], facecolor='black')
ax_graph.set_xlim(0, t_fall * 1.05)
ax_graph.set_ylim(L_array.min() * 1.1, L_array.max() * 1.1)
ax_graph.spines['bottom'].set_color('white')
ax_graph.spines['left'].set_color('white')
ax_graph.spines['top'].set_color('black')
ax_graph.spines['right'].set_color('black')
ax_graph.tick_params(colors='white', which='both', length=0)
ax_graph.set_xticks([])
ax_graph.set_yticks([])

# 軸ラベル
ax_graph.set_xlabel('t', color='white', fontsize=14, weight='bold')
ax_graph.set_ylabel('L', color='white', fontsize=14, weight='bold', rotation=0)
ax_graph.yaxis.set_label_coords(-0.05, 0.95)

# グラフのタイトル
ax_graph.set_title('Lagrangian: L = T - V', color='white', fontsize=16, weight='bold', pad=10)

# 原点を通る補助線
ax_graph.axhline(y=0, color='gray', linestyle='--', linewidth=2, alpha=0.8)
ax_graph.axvline(x=0, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

# ラグランジアンの曲線（初期は空）
line, = ax_graph.plot([], [], color='cyan', linewidth=2, zorder=5)

# 現在位置のマーカー
current_point, = ax_graph.plot([], [], 'o', color='yellow', markersize=8, zorder=10)

def init():
    """アニメーションの初期化"""
    particle.center = (2, h0)
    line.set_data([], [])
    current_point.set_data([], [])
    return particle, line, current_point

def animate(frame):
    """各フレームの更新"""
    t = t_array[frame]

    # 質点の位置計算
    h = h0 - 0.5 * g * t**2
    if h < 0:
        h = 0

    # 質点の位置更新
    particle.center = (2, h)

    # ラグランジアンのグラフ更新（0からframeまでの軌跡を表示）
    t_history = t_array[:frame+1]
    L_history = L_array[:frame+1]
    line.set_data(t_history, L_history)

    # 現在位置のマーカー
    current_point.set_data([t], [L_array[frame]])

    return particle, line, current_point

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
print(f"ラグランジアンの範囲: {L_array.min():.2f}J ~ {L_array.max():.2f}J")

writer = animation.FFMpegWriter(fps=fps, bitrate=1800,
                                extra_args=['-vcodec', 'libx264'])
anim.save('free_fall_lagrangian.mp4', writer=writer, dpi=150)

print("完成！ファイル: free_fall_lagrangian.mp4")
plt.close()
