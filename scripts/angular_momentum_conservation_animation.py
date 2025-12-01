#!/usr/bin/env python3
"""
角運動量保存則（ケプラーの第2法則）を視覚化するアニメーション

太陽を回る地球の楕円軌道を描き、1秒ごとに掃く面積が
一定であることを扇形で示す。面積速度一定の法則を視覚的に表現する。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection

# 軌道パラメータ
e = 0.7  # 離心率
a = 4.0  # 長半径
b = a * np.sqrt(1 - e**2)  # 短半径
c = a * e  # 焦点距離

# 周期設定（8秒で1周）
T = 8.0  # 周期 [秒]

# アニメーション設定
fps = 60
n_frames = int(T * fps) + 1
dt = 1.0 / fps

# 時間配列
t_array = np.linspace(0, T, n_frames)


def mean_anomaly_to_eccentric_anomaly(M, e, tol=1e-8):
    """平均近点角から離心近点角を計算（ニュートン法）"""
    E = M  # 初期値
    for _ in range(100):
        E_new = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
        if abs(E_new - E) < tol:
            return E_new
        E = E_new
    return E


def get_position_at_time(t):
    """時刻tにおける位置を計算"""
    # 平均近点角
    M = 2 * np.pi * t / T
    # 離心近点角
    E = mean_anomaly_to_eccentric_anomaly(M, e)
    # 位置（焦点を原点とする）
    x = a * (np.cos(E) - e)
    y = b * np.sin(E)
    return x, y


def get_true_anomaly_at_time(t):
    """時刻tにおける真近点角を計算"""
    M = 2 * np.pi * t / T
    E = mean_anomaly_to_eccentric_anomaly(M, e)
    # 真近点角
    theta = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                           np.sqrt(1 - e) * np.cos(E / 2))
    return theta


# 図の設定
fig = plt.figure(figsize=(12, 10), facecolor='black')
ax = fig.add_subplot(111, facecolor='black')

# 軸の設定
margin = 1.5
ax.set_xlim(-a - c - margin, a - c + margin)
ax.set_ylim(-b - margin, b + margin)
ax.set_aspect('equal')
ax.axis('off')

# 楕円軌道の描画
theta_orbit = np.linspace(0, 2 * np.pi, 200)
x_orbit = a * np.cos(theta_orbit) - c  # 焦点を原点に
y_orbit = b * np.sin(theta_orbit)
orbit_line, = ax.plot(x_orbit, y_orbit, 'gray', linewidth=1, alpha=0.5)

# 太陽（焦点に配置）
sun = Circle((0, 0), 0.3, color='yellow', zorder=10)
ax.add_patch(sun)
ax.text(0, -0.6, 'Sun', color='yellow', ha='center', fontsize=10)

# 地球の初期位置
x0, y0 = get_position_at_time(0)
earth = Circle((x0, y0), 0.15, color='dodgerblue', zorder=10)
ax.add_patch(earth)

# 扇形の色リスト（8つの異なる色）
sector_colors = [
    '#FF6B6B',  # 赤
    '#4ECDC4',  # シアン
    '#45B7D1',  # 青
    '#96CEB4',  # 緑
    '#FFEAA7',  # 黄
    '#DDA0DD',  # プラム
    '#98D8C8',  # ミント
    '#F7DC6F',  # ゴールド
]

# 扇形を保持するリスト
sector_patches = []

# 式の表示
ax.text(0, b + 1.0, 'Kepler\'s 2nd Law: Equal Areas in Equal Times',
        color='white', ha='center', fontsize=14, weight='bold')
ax.text(0, b + 0.5, '$\\frac{dA}{dt} = \\frac{L}{2m} = const.$',
        color='white', ha='center', fontsize=12)

# 現在の扇形（成長中）
current_sector = None
current_start_time = 0


def create_sector_polygon(t_start, t_end, n_points=50):
    """t_startからt_endまでの扇形を作成"""
    times = np.linspace(t_start, t_end, n_points)
    points = [(0, 0)]  # 焦点から開始
    for t in times:
        x, y = get_position_at_time(t)
        points.append((x, y))
    points.append((0, 0))  # 焦点に戻る
    return Polygon(points, closed=True)


def init():
    """アニメーションの初期化"""
    return [earth]


def animate(frame):
    """各フレームの更新"""
    global current_sector, current_start_time, sector_patches

    t = t_array[frame]

    # 地球の位置更新
    x, y = get_position_at_time(t)
    earth.center = (x, y)

    # 現在の秒数（0-7）
    current_second = int(t)
    time_in_second = t - current_second

    # 新しい秒が始まったら、前の扇形を確定して新しい扇形を開始
    if current_second > int(current_start_time) or (frame == 0):
        # 前の扇形を確定（最初のフレーム以外）
        if frame > 0 and current_second > 0:
            prev_second = current_second - 1
            completed_sector = create_sector_polygon(prev_second, current_second)
            completed_sector.set_facecolor(sector_colors[prev_second % len(sector_colors)])
            completed_sector.set_alpha(0.5)
            completed_sector.set_edgecolor('white')
            completed_sector.set_linewidth(1)
            completed_sector.set_zorder(2)
            ax.add_patch(completed_sector)
            sector_patches.append(completed_sector)

        current_start_time = current_second

    # 現在成長中の扇形を更新（既存のものを削除して再作成）
    if current_sector is not None:
        current_sector.remove()

    if time_in_second > 0.01:  # 少し経過してから描画開始
        current_sector = create_sector_polygon(current_second, t)
        current_sector.set_facecolor(sector_colors[current_second % len(sector_colors)])
        current_sector.set_alpha(0.7)
        current_sector.set_edgecolor('white')
        current_sector.set_linewidth(1)
        current_sector.set_zorder(3)
        ax.add_patch(current_sector)
    else:
        current_sector = None

    return [earth] + sector_patches + ([current_sector] if current_sector else [])


# アニメーションの作成（blit=Falseで確実に更新）
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=n_frames, interval=dt * 1000,
                               blit=False, repeat=False)

# MP4として保存
print("アニメーションを生成しています...")
print(f"周期: {T}秒")
print(f"離心率: {e}")
print(f"扇形の数: {int(T)}個")
print(f"フレーム数: {n_frames}")
print(f"フレームレート: {fps} fps")

writer = animation.FFMpegWriter(fps=fps, bitrate=2400,
                                extra_args=['-vcodec', 'libx264'])
anim.save('angular_momentum_conservation.mp4', writer=writer, dpi=150)

print("完成！ファイル: angular_momentum_conservation.mp4")
plt.close()
