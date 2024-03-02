# 맵 이미지를 Base64 문자열로 인코딩하는 함수 - 수정된 버전
def plot_to_base64(x, y, values):
    # 격자(grid) 데이터 준비
    xi = np.linspace(0, 10, 100)  # 가로세로 10에 맞춤
    yi = np.linspace(0, 10, 100)
    xi, yi = np.meshgrid(xi, yi)
    
    # 데이터 보간
    zi = griddata((x, y), values, (xi, yi), method='cubic')
    
    # 색상 맵 생성: 0에서 빨간색, 0.5에서 회색, 1에서 파란색
    cdict = {'red':   ((0.0, 1.0, 1.0),
                       (0.5, 0.5, 0.5),
                       (1.0, 0.0, 0.0)),
             'green': ((0.0, 0.0, 0.0),
                       (0.5, 0.5, 0.5),
                       (1.0, 0.0, 0.0)),
             'blue':  ((0.0, 0.0, 0.0),
                       (0.5, 0.5, 0.5),
                       (1.0, 1.0, 1.0))}
    cmap = LinearSegmentedColormap('custom_cmap', cdict)
    
    fig, ax = plt.subplots(figsize=(2, 2), dpi=100)
    
    # 등고선 맵 생성
    contourf = ax.contourf(xi, yi, zi, levels=np.linspace(0, 1, 4), cmap=cmap)
    
    # 원 추가
    circle = Circle((5, 5), 5, edgecolor='black', facecolor='none', linewidth=2)
    ax.add_patch(circle)
    
    # 원 바깥의 등고선 맵 가리기
    for contour in contourf.collections:
        contour.set_clip_path(circle)
    
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()

# 아래 scatter shape rect
# 맵 이미지를 Base64 문자열로 인코딩하는 함수 - 수정된 버전
def plot_to_base64(x, y, values):
    # 색상을 결정하기 위한 조건 설정
    colors = np.where(values < 0.3, 'red', np.where(values > 0.3, 'blue', 'gray'))
    
    fig, ax = plt.subplots(figsize=(2, 2), dpi=100)
    # 사각형 마커와 조건에 따른 색상 사용
    scatter = ax.scatter(x, y, s=100, c=colors, marker='s', edgecolor='black')
    ax.axis('off')
    
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()

# 폴더 생성
folder_name = 'cat1_cat2'
os.makedirs(folder_name, exist_ok=True)

# cat1과 cat2로 그룹화하고 각 그룹을 'cat1_cat2' 폴더 안에 parquet 파일로 저장
for (cat1, cat2), group_df in df.groupby(['cat1', 'cat2']):
    file_path = f'{folder_name}/{cat1}_{cat2}.parquet'
    group_df.to_parquet(file_path)

print("파일 저장 완료.")