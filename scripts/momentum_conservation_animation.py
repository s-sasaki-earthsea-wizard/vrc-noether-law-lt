#!/usr/bin/env python3
"""
運動量保存則を視覚化するアニメーション

同じ質量の2つの物体が異なる速度で正面衝突し、
弾性衝突により速度が交換される様子を示す。
運動量バーにより、全運動量が保存されることを視覚的に表現する。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle

# 物理パラメータ
m = 1.0  # 質量（両方同じ）

# 速度設定（Bは静止、Aが衝突）
v_A_initial = 3.0  # 物体Aの初速度（右向き正）
v_B_initial = 0.0  # 物体Bは静止

# 弾性衝突で同じ質量の場合、速度が交換される
v_A_final = v_B_initial  # 衝突後のAの速度 = 0
v_B_final = v_A_initial  # 衝突後のBの速度 = 3.0

# 初期位置
x_A_initial = 2.0
x_B_initial = 8.0

# 衝突位置と時刻の計算
# x_A + v_A * t = x_B + v_B * t
# t_collision = (x_B - x_A) / (v_A - v_B)
t_collision = (x_B_initial - x_A_initial) / (v_A_initial - v_B_initial)
x_collision = x_A_initial + v_A_initial * t_collision

# アニメーション設定
fps = 60
total_time = t_collision * 2.5  # 衝突後も少し表示
dt = 1.0 / fps
n_frames = int(total_time / dt) + 1

# 時間配列
t_array = np.linspace(0, total_time, n_frames)

# 全運動量（保存される）
p_total = m * v_A_initial + m * v_B_initial

# 図の設定
fig = plt.figure(figsize=(12, 8), facecolor='black')
ax = fig.add_subplot(111, facecolor='black')

# 軸の設定
ax.set_xlim(-1, 11)
ax.set_ylim(-3, 8)
ax.set_aspect('equal')
ax.axis('off')

# 物体のサイズ
radius = 0.4

# 物体A（青）
particle_A = Circle((x_A_initial, 2), radius, color='dodgerblue', zorder=10)
ax.add_patch(particle_A)

# 物体B（赤）
particle_B = Circle((x_B_initial, 2), radius, color='tomato', zorder=10)
ax.add_patch(particle_B)

# 物体ラベル
label_A = ax.text(x_A_initial, 2, 'A', color='white', ha='center', va='center',
                  fontsize=14, weight='bold', zorder=11)
label_B = ax.text(x_B_initial, 2, 'B', color='white', ha='center', va='center',
                  fontsize=14, weight='bold', zorder=11)

# 速度ベクトル（矢印）
arrow_scale = 0.3
arrow_A = ax.annotate('', xy=(x_A_initial + v_A_initial * arrow_scale, 2),
                      xytext=(x_A_initial, 2),
                      arrowprops=dict(arrowstyle='->', color='cyan', lw=2),
                      zorder=9)
arrow_B = ax.annotate('', xy=(x_B_initial + v_B_initial * arrow_scale, 2),
                      xytext=(x_B_initial, 2),
                      arrowprops=dict(arrowstyle='->', color='orange', lw=2),
                      zorder=9)

# 運動量バーの設定（横向き、下に配置）
bar_y = -1.5  # バーのy座標
bar_height = 0.8  # バーの高さ（縦方向）
bar_half_width = 4.0  # バーの半分の幅（中央が原点）
bar_center_x = 5.0  # バーの中央のx座標

# 最大運動量（スケーリング用）
p_max = abs(m * v_A_initial) * 1.2  # 少し余裕を持たせる

# 物体Aの運動量バー（青）- 横向き
momentum_bar_A = Rectangle((bar_center_x, bar_y), 0, bar_height,
                            color='dodgerblue', alpha=0.7, zorder=5)
ax.add_patch(momentum_bar_A)

# 物体Bの運動量バー（赤）- Aの先端から伸びる
momentum_bar_B = Rectangle((bar_center_x, bar_y), 0, bar_height,
                            color='tomato', alpha=0.7, zorder=5)
ax.add_patch(momentum_bar_B)

# バーの枠（中央が原点、横向き）
bar_frame = Rectangle((bar_center_x - bar_half_width, bar_y), bar_half_width * 2, bar_height,
                       fill=False, edgecolor='white', linewidth=2, zorder=6)
ax.add_patch(bar_frame)

# 中央線（p = 0）
zero_line = plt.Line2D([bar_center_x, bar_center_x],
                       [bar_y - 0.2, bar_y + bar_height + 0.2],
                       color='gray', linewidth=1, linestyle='-', zorder=4)
ax.add_line(zero_line)

# 全運動量の参照線（保存されることを示す）
p_total_width = (p_total / p_max) * bar_half_width
total_line = plt.Line2D([bar_center_x + p_total_width, bar_center_x + p_total_width],
                        [bar_y - 0.2, bar_y + bar_height + 0.2],
                        color='yellow', linewidth=2, linestyle='--', zorder=7)
ax.add_line(total_line)

# ラベル
ax.text(bar_center_x - bar_half_width - 0.3, bar_y + bar_height / 2, '-p',
        color='white', ha='right', va='center', fontsize=10)
ax.text(bar_center_x + bar_half_width + 0.3, bar_y + bar_height / 2, '+p',
        color='white', ha='left', va='center', fontsize=10)
ax.text(bar_center_x + p_total_width, bar_y + bar_height + 0.4, 'Total',
        color='yellow', ha='center', va='bottom', fontsize=11, weight='bold')
ax.text(bar_center_x, bar_y - 0.4, '0',
        color='gray', ha='center', va='top', fontsize=10)

# 運動量の数値表示
momentum_text = ax.text(bar_center_x, bar_y + bar_height + 0.8, '',
                        color='white', ha='center', fontsize=10)

# 式の表示
ax.text(5, 6.5, '$m v_A + m v_B = const.$',
        color='white', ha='center', fontsize=16, weight='bold')


def get_positions_and_velocities(t):
    """時刻tにおける位置と速度を計算"""
    if t < t_collision:
        # 衝突前
        x_A = x_A_initial + v_A_initial * t
        x_B = x_B_initial + v_B_initial * t
        v_A = v_A_initial
        v_B = v_B_initial
    else:
        # 衝突後（速度が交換される）
        dt_after = t - t_collision
        x_A = x_collision + v_A_final * dt_after
        x_B = x_collision + v_B_final * dt_after
        v_A = v_A_final
        v_B = v_B_final

    return x_A, x_B, v_A, v_B


def init():
    """アニメーションの初期化"""
    return (particle_A, particle_B, label_A, label_B,
            momentum_bar_A, momentum_bar_B, momentum_text)


def animate(frame):
    """各フレームの更新"""
    t = t_array[frame]

    # 位置と速度の取得
    x_A, x_B, v_A, v_B = get_positions_and_velocities(t)

    # 物体の位置更新
    particle_A.center = (x_A, 2)
    particle_B.center = (x_B, 2)

    # ラベルの位置更新
    label_A.set_position((x_A, 2))
    label_B.set_position((x_B, 2))

    # 速度ベクトルの更新
    arrow_A.xy = (x_A + v_A * arrow_scale, 2)
    arrow_A.xyann = (x_A, 2)
    arrow_B.xy = (x_B + v_B * arrow_scale, 2)
    arrow_B.xyann = (x_B, 2)

    # 運動量の計算
    p_A = m * v_A
    p_B = m * v_B

    # バーの幅を計算（中央が原点、正は右、負は左）
    p_A_width = (p_A / p_max) * bar_half_width
    p_B_width = (p_B / p_max) * bar_half_width

    # バーの更新（積み上げ式、中央が原点、横向き）
    # Aのバー：中央から開始
    if p_A >= 0:
        momentum_bar_A.set_x(bar_center_x)
        momentum_bar_A.set_width(p_A_width)
        base_for_B = bar_center_x + p_A_width
    else:
        momentum_bar_A.set_x(bar_center_x + p_A_width)
        momentum_bar_A.set_width(-p_A_width)
        base_for_B = bar_center_x + p_A_width

    # Bのバー：Aの先端から開始
    if p_B >= 0:
        momentum_bar_B.set_x(base_for_B)
        momentum_bar_B.set_width(p_B_width)
    else:
        momentum_bar_B.set_x(base_for_B + p_B_width)
        momentum_bar_B.set_width(-p_B_width)

    # 数値表示の更新
    momentum_text.set_text(f'$p_A$={p_A:.1f}, $p_B$={p_B:.1f}')

    return (particle_A, particle_B, label_A, label_B,
            momentum_bar_A, momentum_bar_B, momentum_text)


# アニメーションの作成
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=n_frames, interval=dt * 1000,
                               blit=True, repeat=True)

# MP4として保存
print("アニメーションを生成しています...")
print(f"衝突時刻: {t_collision:.2f}秒")
print(f"衝突位置: x = {x_collision:.2f}")
print(f"全運動量: {p_total:.2f} (保存される)")
print(f"フレーム数: {n_frames}")
print(f"フレームレート: {fps} fps")

writer = animation.FFMpegWriter(fps=fps, bitrate=1800,
                                extra_args=['-vcodec', 'libx264'])
anim.save('momentum_conservation.mp4', writer=writer, dpi=150)

print("完成！ファイル: momentum_conservation.mp4")
plt.close()
