#!/usr/bin/env python3
"""
自由落下のエネルギー保存を視覚化するアニメーション

質点の自由落下と、位置エネルギー（青）と運動エネルギー（赤）の
バー表示により、エネルギー保存則を視覚的に示す。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle

# 物理定数
g = 9.8  # 重力加速度 [m/s²]
h0 = 10.0  # 初期高さ [m]
m = 1.0  # 質量 [kg]（mは計算でキャンセルされるが、明示的に設定）

# 全エネルギー（保存される）
E_total = m * g * h0

# 落下時間の計算
t_fall = np.sqrt(2 * h0 / g)

# アニメーション設定
fps = 60  # フレームレート
dt = 1.0 / fps  # 時間刻み
n_frames = int(t_fall / dt) + 1

# 時間配列
t_array = np.linspace(0, t_fall, n_frames)

# 図の設定
fig = plt.figure(figsize=(12, 8), facecolor='black')
ax = fig.add_subplot(111, facecolor='black')

# 軸の設定
ax.set_xlim(0, 10)
ax.set_ylim(-1, 12)
ax.set_aspect('equal')
ax.axis('off')

# 地面の描画（y=0の位置）
ground_line = plt.Line2D([0.5, 3.5], [0, 0], color='white', linewidth=3)
ax.add_line(ground_line)

# 地面のハッチング（装飾）
for i in range(8):
    hatch = plt.Line2D([0.5 + i*0.4, 0.7 + i*0.4], [0, -0.3], color='white', linewidth=1)
    ax.add_line(hatch)

# 質点（円）
particle = Circle((2, h0), 0.2, color='yellow', zorder=10)
ax.add_patch(particle)

# エネルギーバーの位置設定
bar_x = 7.0
bar_width = 1.5
bar_max_height = 10.0  # バーの最大高さ（h0に対応）

# 位置エネルギーバー（青）
potential_bar = Rectangle((bar_x, 0), bar_width, bar_max_height,
                          color='blue', alpha=0.7, zorder=5)
ax.add_patch(potential_bar)

# 運動エネルギーバー（赤）
kinetic_bar = Rectangle((bar_x, bar_max_height), bar_width, 0,
                        color='red', alpha=0.7, zorder=5)
ax.add_patch(kinetic_bar)

# エネルギーバーの枠
bar_frame = Rectangle((bar_x, 0), bar_width, bar_max_height,
                      fill=False, edgecolor='white', linewidth=2, zorder=6)
ax.add_patch(bar_frame)

# ラベル
ax.text(bar_x + bar_width/2, -0.5, 'Energy',
        color='white', ha='center', fontsize=14, weight='bold')
ax.text(bar_x - 0.3, bar_max_height/2, 'PE',
        color='cyan', ha='right', fontsize=12, weight='bold')
ax.text(bar_x + bar_width + 0.3, bar_max_height/2, 'KE',
        color='orange', ha='left', fontsize=12, weight='bold')

# 初期高さの参照線（点線）
reference_line = plt.Line2D([0.5, 3.5], [h0, h0],
                           color='gray', linewidth=1, linestyle='--', alpha=0.5)
ax.add_line(reference_line)

def init():
    """アニメーションの初期化"""
    return particle, potential_bar, kinetic_bar

def animate(frame):
    """各フレームの更新"""
    t = t_array[frame]

    # 質点の位置と速度の計算
    h = h0 - 0.5 * g * t**2
    v = g * t

    # 地面に到達したら停止
    if h < 0:
        h = 0
        v = np.sqrt(2 * g * h0)  # 地面到達時の速度

    # エネルギーの計算
    U = m * g * h  # 位置エネルギー
    K = 0.5 * m * v**2  # 運動エネルギー

    # バーの高さを正規化（E_totalを基準にbar_max_heightにスケール）
    U_height = (U / E_total) * bar_max_height
    K_height = (K / E_total) * bar_max_height

    # 質点の位置更新
    particle.center = (2, h)

    # 位置エネルギーバーの更新（下から積む）
    potential_bar.set_height(U_height)

    # 運動エネルギーバーの更新（位置エネルギーの上に積む）
    kinetic_bar.set_y(U_height)
    kinetic_bar.set_height(K_height)

    return particle, potential_bar, kinetic_bar

# アニメーションの作成
anim = animation.FuncAnimation(fig, animate, init_func=init,
                              frames=n_frames, interval=dt*1000,
                              blit=True, repeat=True)

# MP4として保存
print("アニメーションを生成しています...")
print(f"落下時間: {t_fall:.2f}秒")
print(f"フレーム数: {n_frames}")
print(f"フレームレート: {fps} fps")

writer = animation.FFMpegWriter(fps=fps, bitrate=1800,
                                extra_args=['-vcodec', 'libx264'])
anim.save('free_fall_energy.mp4', writer=writer, dpi=150)

print("完成！ファイル: free_fall_energy.mp4")
plt.close()
