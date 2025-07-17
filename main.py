# 파일명: app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="centered")
st.title("🦟 GM 모기 역확산 시뮬레이션 (애니메이션)")

# 설정 슬라이더
grid_size = 30
steps = st.slider("시뮬레이션 세대 수", 1, 50, 20)
init_density = st.slider("초기 감염 개체 밀도 (셀당 평균)", 0, 20, 5)
release_amount = st.slider("역확산 살포 강도 (셀당 개체 수)", 0, 50, 20)
speed = st.slider("프레임 간 시간 (초)", 0.01, 0.5, 0.1)

# 초기 감염 상태
gm_grid = np.random.poisson(lam=init_density, size=(grid_size, grid_size))

# 고정된 역확산 방사 지점 (예: 중앙 3지점)
release_points = [(10, 10), (15, 15), (20, 20)]

# Streamlit figure 준비
plot_spot = st.empty()

for step in range(steps):
    new_grid = np.zeros_like(gm_grid)

    # 감염 모기 확산 (8방향 중 하나로 이동)
    for i in range(grid_size):
        for j in range(grid_size):
            count = gm_grid[i, j]
            for _ in range(count):
                dx, dy = np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])
                ni, nj = i + dx, j + dy
                if 0 <= ni < grid_size and 0 <= nj < grid_size:
                    new_grid[ni, nj] += 1

    # 역확산 모기 살포
    for (i, j) in release_points:
        new_grid[i, j] += release_amount

    gm_grid = new_grid

    # 시각화 갱신 (실시간 애니메이션)
    fig, ax = plt.subplots()
    ax.imshow(gm_grid, cmap='hot', interpolation='nearest')
    ax.set_title(f"{step+1}세대 GM 모기 분포")
    ax.axis('off')
    plot_spot.pyplot(fig)
    time.sleep(speed)
