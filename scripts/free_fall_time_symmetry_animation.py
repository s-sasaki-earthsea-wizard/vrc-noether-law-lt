#!/usr/bin/env python3
"""
時間対称性を視覚化するアニメーション

同じ高さから異なる時刻に落下する2つのボールを表示し、
ラグランジアン L = T - V が「落下開始からの経過時間τ」に対して
完全に同じ軌跡を描くことを示す。

これにより ∂L/∂t = 0（ラグランジアンが時刻に陽に依存しない）の
意味を直感的に理解できる。
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

# タイミング設定
delay = 1.0  # ボール2の開始遅延（ボール1着地後からの秒数）
t_ball2_start = t_fall + delay  # ボール2の落下開始時刻
t_total = t_ball2_start + t_fall + 0.5  # 全体の時間（少し余裕を持たせる）

# アニメーション設定
fps = 60
dt = 1.0 / fps
n_frames = int(t_total / dt) + 1

# 時間配列
t_array = np.linspace(0, t_total, n_frames)

# ラグランジアンの計算関数
def calc_lagrangian(tau):
    """落下開始からの経過時間τに対するラグランジアンを計算"""
    if tau < 0:
        return None
    if tau > t_fall:
        tau = t_fall
    v = g * tau
    h = h0 - 0.5 * g * tau**2
    if h < 0:
        h = 0
        v = np.sqrt(2 * g * h0)
    T = 0.5 * m * v**2
    V = m * g * h
    return T - V

# 経過時間τの配列（グラフ用）
tau_array = np.linspace(0, t_fall, 100)
L_theoretical = np.array([calc_lagrangian(tau) for tau in tau_array])

# 図の設定
fig = plt.figure(figsize=(16, 7), facecolor='black')
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1.5], wspace=0.3)

# 左側：自由落下のアニメーション
ax_fall = fig.add_subplot(gs[0], facecolor='black')
ax_fall.set_xlim(0, 8)
ax_fall.set_ylim(-1.5, 12)
ax_fall.set_aspect('equal')
ax_fall.axis('off')

# タイトル
title_text = ax_fall.text(4, 11.5, 'Time Symmetry', color='white',
                          ha='center', fontsize=18, weight='bold')

# 地面の描画
ground_line = plt.Line2D([0.5, 7.5], [0, 0], color='white', linewidth=3)
ax_fall.add_line(ground_line)

# 地面のハッチング
for i in range(15):
    hatch = plt.Line2D([0.5 + i*0.5, 0.7 + i*0.5], [0, -0.3], color='white', linewidth=1)
    ax_fall.add_line(hatch)

# 初期高さの参照線
reference_line = plt.Line2D([0.5, 7.5], [h0, h0],
                           color='gray', linewidth=1, linestyle='--', alpha=0.5)
ax_fall.add_line(reference_line)

# ボール1（シアン）
particle1 = Circle((2.5, h0), 0.25, color='cyan', zorder=10)
ax_fall.add_patch(particle1)
label1 = ax_fall.text(2.5, -1.0, 'Ball 1\n(t = 0)', color='cyan',
                      ha='center', fontsize=11, weight='bold')

# ボール2（マゼンタ）- 最初は上空で待機
particle2 = Circle((5.5, h0), 0.25, color='magenta', zorder=10, alpha=0.3)
ax_fall.add_patch(particle2)
label2 = ax_fall.text(5.5, -1.0, f'Ball 2\n(t = {t_ball2_start:.1f}s)', color='magenta',
                      ha='center', fontsize=11, weight='bold')

# 右側：ラグランジアンのグラフ
ax_graph = fig.add_subplot(gs[1], facecolor='black')
ax_graph.set_xlim(-0.05, t_fall * 1.1)
ax_graph.set_ylim(L_theoretical.min() * 1.15, L_theoretical.max() * 1.15)
ax_graph.spines['bottom'].set_color('white')
ax_graph.spines['left'].set_color('white')
ax_graph.spines['top'].set_color('black')
ax_graph.spines['right'].set_color('black')
ax_graph.tick_params(colors='white', which='both', length=0)
ax_graph.set_xticks([])
ax_graph.set_yticks([])

# 軸ラベル
ax_graph.set_xlabel('τ (time since drop)', color='white', fontsize=13, weight='bold')
ax_graph.set_ylabel('L', color='white', fontsize=14, weight='bold', rotation=0)
ax_graph.yaxis.set_label_coords(-0.05, 0.95)

# グラフのタイトル
ax_graph.set_title('Lagrangian: L = T - V', color='white', fontsize=16, weight='bold', pad=10)

# 原点を通る補助線
ax_graph.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)

# ラグランジアンの曲線
line1, = ax_graph.plot([], [], color='cyan', linewidth=3, label='Ball 1', zorder=5)
line2, = ax_graph.plot([], [], color='magenta', linewidth=3, label='Ball 2', zorder=6)

# 現在位置のマーカー
point1, = ax_graph.plot([], [], 'o', color='cyan', markersize=10, zorder=10)
point2, = ax_graph.plot([], [], 'o', color='magenta', markersize=10, zorder=11)

# 凡例
ax_graph.legend(loc='lower right', facecolor='black', edgecolor='white',
                labelcolor='white', fontsize=11)

# 結果表示用テキスト
result_text = ax_graph.text(t_fall * 0.5, L_theoretical.max() * 0.9, '',
                            color='yellow', ha='center', fontsize=14, weight='bold')

def init():
    """アニメーションの初期化"""
    particle1.center = (2.5, h0)
    particle2.center = (5.5, h0)
    particle2.set_alpha(0.3)
    line1.set_data([], [])
    line2.set_data([], [])
    point1.set_data([], [])
    point2.set_data([], [])
    result_text.set_text('')
    return particle1, particle2, line1, line2, point1, point2, result_text

def animate(frame):
    """各フレームの更新"""
    t = t_array[frame]

    # ========== ボール1の更新 ==========
    tau1 = t  # ボール1は t=0 でスタート
    if tau1 <= t_fall:
        h1 = h0 - 0.5 * g * tau1**2
        if h1 < 0:
            h1 = 0
    else:
        h1 = 0
        tau1 = t_fall

    particle1.center = (2.5, h1)

    # ボール1のラグランジアン軌跡
    tau1_history = np.linspace(0, min(t, t_fall), max(1, int(min(t, t_fall) / dt)))
    L1_history = [calc_lagrangian(tau) for tau in tau1_history]
    line1.set_data(tau1_history, L1_history)

    # ボール1の現在位置マーカー
    if t <= t_fall:
        L1_current = calc_lagrangian(tau1)
        point1.set_data([tau1], [L1_current])
    else:
        point1.set_data([], [])

    # ========== ボール2の更新 ==========
    if t < t_ball2_start:
        # まだ落下開始前
        particle2.center = (5.5, h0)
        particle2.set_alpha(0.3)
        line2.set_data([], [])
        point2.set_data([], [])
    else:
        # 落下開始後
        particle2.set_alpha(1.0)
        tau2 = t - t_ball2_start  # ボール2の経過時間

        if tau2 <= t_fall:
            h2 = h0 - 0.5 * g * tau2**2
            if h2 < 0:
                h2 = 0
        else:
            h2 = 0
            tau2 = t_fall

        particle2.center = (5.5, h2)

        # ボール2のラグランジアン軌跡
        tau2_elapsed = min(tau2, t_fall)
        tau2_history = np.linspace(0, tau2_elapsed, max(1, int(tau2_elapsed / dt)))
        L2_history = [calc_lagrangian(tau) for tau in tau2_history]
        line2.set_data(tau2_history, L2_history)

        # ボール2の現在位置マーカー
        if tau2 <= t_fall:
            L2_current = calc_lagrangian(tau2)
            point2.set_data([tau2], [L2_current])
        else:
            point2.set_data([], [])

    # ========== 結果表示 ==========
    # ボール2も落下完了したら結果を表示
    if t >= t_ball2_start + t_fall:
        result_text.set_text('Same curve!\n∂L/∂t = 0')
    else:
        result_text.set_text('')

    return particle1, particle2, line1, line2, point1, point2, result_text

# アニメーションの作成
anim = animation.FuncAnimation(fig, animate, init_func=init,
                              frames=n_frames, interval=dt*1000,
                              blit=False, repeat=True)

# MP4として保存
print("アニメーションを生成しています...")
print(f"初期高さ: {h0:.1f}m")
print(f"落下時間: {t_fall:.2f}秒")
print(f"ボール2の開始時刻: {t_ball2_start:.2f}秒")
print(f"全体の時間: {t_total:.2f}秒")
print(f"フレーム数: {n_frames}")
print(f"フレームレート: {fps} fps")

writer = animation.FFMpegWriter(fps=fps, bitrate=1800,
                                extra_args=['-vcodec', 'libx264'])
anim.save('free_fall_time_symmetry.mp4', writer=writer, dpi=150)

print("完成！ファイル: free_fall_time_symmetry.mp4")
plt.close()
