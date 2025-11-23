#!/usr/bin/env python3
"""
2つの異なる高さからの自由落下を比較するアニメーション

10mと11mから同時に落下する2つのボールを並べて表示し、
それぞれの位置エネルギー（青）と運動エネルギー（赤）をバー表示。
高い位置から落としたボールの方が全エネルギーが大きいことを視覚的に示す。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle

# 物理定数
g = 9.8  # 重力加速度 [m/s²]
h0_left = 10.0  # 左側のボールの初期高さ [m]
h0_right = 11.0  # 右側のボールの初期高さ [m]
m = 1.0  # 質量 [kg]

# 各ボールの全エネルギー
E_left = m * g * h0_left
E_right = m * g * h0_right

# 落下時間の計算
t_fall_left = np.sqrt(2 * h0_left / g)
t_fall_right = np.sqrt(2 * h0_right / g)
t_max = t_fall_right  # 長い方に合わせる

# アニメーション設定
fps = 60
dt = 1.0 / fps
n_frames = int(t_max / dt) + 1

# 時間配列
t_array = np.linspace(0, t_max, n_frames)

# 図の設定
fig = plt.figure(figsize=(14, 8), facecolor='black')
ax = fig.add_subplot(111, facecolor='black')

# 軸の設定
ax.set_xlim(0, 14)
ax.set_ylim(-1, 13)
ax.set_aspect('equal')
ax.axis('off')

# 地面の描画（y=0の位置、全体に渡る）
ground_line = plt.Line2D([0.5, 13.5], [0, 0], color='white', linewidth=3)
ax.add_line(ground_line)

# 地面のハッチング（装飾）
for i in range(30):
    hatch = plt.Line2D([0.5 + i*0.45, 0.7 + i*0.45], [0, -0.3], color='white', linewidth=1)
    ax.add_line(hatch)

# ========== 左側のボール（10m） ==========
# 質点（円）
particle_left = Circle((2, h0_left), 0.2, color='yellow', zorder=10)
ax.add_patch(particle_left)

# 初期高さの参照線
reference_line_left = plt.Line2D([0.5, 3.5], [h0_left, h0_left],
                                color='gray', linewidth=1, linestyle='--', alpha=0.5)
ax.add_line(reference_line_left)

# エネルギーバーの位置設定
bar_x_left = 4.5
bar_width = 1.0
bar_scale = 0.1  # エネルギー値を高さに変換するスケール（視覚化のため）

# 位置エネルギーバー（青）
potential_bar_left = Rectangle((bar_x_left, 0), bar_width, E_left * bar_scale,
                               color='blue', alpha=0.7, zorder=5)
ax.add_patch(potential_bar_left)

# 運動エネルギーバー（赤）
kinetic_bar_left = Rectangle((bar_x_left, E_left * bar_scale), bar_width, 0,
                             color='red', alpha=0.7, zorder=5)
ax.add_patch(kinetic_bar_left)

# ラベル
ax.text(2, -0.7, '10m', color='yellow', ha='center', fontsize=14, weight='bold')
ax.text(bar_x_left + bar_width/2, -0.5, 'Energy',
        color='white', ha='center', fontsize=12, weight='bold')

# ========== 右側のボール（11m） ==========
# 質点（円）
particle_right = Circle((9, h0_right), 0.2, color='lime', zorder=10)
ax.add_patch(particle_right)

# 初期高さの参照線
reference_line_right = plt.Line2D([7.5, 10.5], [h0_right, h0_right],
                                 color='gray', linewidth=1, linestyle='--', alpha=0.5)
ax.add_line(reference_line_right)

# エネルギーバーの位置設定
bar_x_right = 11.5

# 位置エネルギーバー（青）
potential_bar_right = Rectangle((bar_x_right, 0), bar_width, E_right * bar_scale,
                                color='blue', alpha=0.7, zorder=5)
ax.add_patch(potential_bar_right)

# 運動エネルギーバー（赤）
kinetic_bar_right = Rectangle((bar_x_right, E_right * bar_scale), bar_width, 0,
                              color='red', alpha=0.7, zorder=5)
ax.add_patch(kinetic_bar_right)

# ラベル
ax.text(9, -0.7, '11m', color='lime', ha='center', fontsize=14, weight='bold')
ax.text(bar_x_right + bar_width/2, -0.5, 'Energy',
        color='white', ha='center', fontsize=12, weight='bold')

# 中央の区切り線
divider = plt.Line2D([7, 7], [-0.5, 12], color='white', linewidth=1,
                    linestyle=':', alpha=0.3)
ax.add_line(divider)

def init():
    """アニメーションの初期化"""
    # 左側のボールの初期状態（t=0）
    particle_left.center = (2, h0_left)
    potential_bar_left.set_height(E_left * bar_scale)
    kinetic_bar_left.set_y(E_left * bar_scale)
    kinetic_bar_left.set_height(0)

    # 右側のボールの初期状態（t=0）
    particle_right.center = (9, h0_right)
    potential_bar_right.set_height(E_right * bar_scale)
    kinetic_bar_right.set_y(E_right * bar_scale)
    kinetic_bar_right.set_height(0)

    return (particle_left, potential_bar_left, kinetic_bar_left,
            particle_right, potential_bar_right, kinetic_bar_right)

def animate(frame):
    """各フレームの更新"""
    t = t_array[frame]

    # ========== 左側のボール（10m）の更新 ==========
    if t <= t_fall_left:
        # 落下中
        h_left = h0_left - 0.5 * g * t**2
        v_left = g * t
    else:
        # 地面に到達後は停止
        h_left = 0
        v_left = np.sqrt(2 * g * h0_left)

    # 地面チェック
    if h_left < 0:
        h_left = 0
        v_left = np.sqrt(2 * g * h0_left)

    # エネルギーの計算
    U_left = m * g * h_left
    K_left = 0.5 * m * v_left**2

    # 質点の位置更新
    particle_left.center = (2, h_left)

    # エネルギーバーの更新（絶対値で表示）
    U_height_left = U_left * bar_scale
    K_height_left = K_left * bar_scale

    potential_bar_left.set_height(U_height_left)
    kinetic_bar_left.set_y(U_height_left)
    kinetic_bar_left.set_height(K_height_left)

    # ========== 右側のボール（11m）の更新 ==========
    if t <= t_fall_right:
        # 落下中
        h_right = h0_right - 0.5 * g * t**2
        v_right = g * t
    else:
        # 地面に到達後は停止
        h_right = 0
        v_right = np.sqrt(2 * g * h0_right)

    # 地面チェック
    if h_right < 0:
        h_right = 0
        v_right = np.sqrt(2 * g * h0_right)

    # エネルギーの計算
    U_right = m * g * h_right
    K_right = 0.5 * m * v_right**2

    # 質点の位置更新
    particle_right.center = (9, h_right)

    # エネルギーバーの更新（絶対値で表示）
    U_height_right = U_right * bar_scale
    K_height_right = K_right * bar_scale

    potential_bar_right.set_height(U_height_right)
    kinetic_bar_right.set_y(U_height_right)
    kinetic_bar_right.set_height(K_height_right)

    return (particle_left, potential_bar_left, kinetic_bar_left,
            particle_right, potential_bar_right, kinetic_bar_right)

# アニメーションの作成
anim = animation.FuncAnimation(fig, animate, init_func=init,
                              frames=n_frames, interval=dt*1000,
                              blit=False, repeat=True)

# MP4として保存
print("アニメーションを生成しています...")
print(f"左側のボール: {h0_left:.1f}m (落下時間: {t_fall_left:.2f}秒)")
print(f"右側のボール: {h0_right:.1f}m (落下時間: {t_fall_right:.2f}秒)")
print(f"フレーム数: {n_frames}")
print(f"フレームレート: {fps} fps")

writer = animation.FFMpegWriter(fps=fps, bitrate=1800,
                                extra_args=['-vcodec', 'libx264'])
anim.save('free_fall_two_heights.mp4', writer=writer, dpi=150)

print("完成！ファイル: free_fall_two_heights.mp4")
plt.close()
