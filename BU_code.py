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


# 박스플롯 생성 및 Base64 인코딩
def create_boxplot_base64_for_val1_by_cat3(df, val_column='val1'):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='cat3', y=val_column, data=df)
    plt.title(f'Boxplot of {val_column} by cat3')
    plt.xlabel('cat3')
    plt.ylabel(val_column)
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    return base64.b64encode(buf.getvalue()).decode()

# 각 cat3 값에 대한 val1의 통계치 계산
def calculate_stats_for_val1_by_cat3(df, val_column='val1'):
    stats_df = df.groupby('cat3')[val_column].describe(percentiles=[0.1, 0.5, 0.9])
    stats_df['<0.5 count'] = df[df[val_column] < 0.5].groupby('cat3')[val_column].count()
    return stats_df[['mean', 'std', '10%', '50%', '90%', '<0.5 count']].round(2)

# 박스플롯 및 통계치를 HTML로 포맷팅
def format_boxplot_and_stats_to_html(boxplot_img_data, stats_df):
    boxplot_html = f'<img src="data:image/png;base64,{boxplot_img_data}" style="max-width:100%; display: block; margin-left: auto; margin-right: auto;">'
    stats_html = stats_df.to_html(classes='table table-striped', justify='center')
    
    return boxplot_html + '<br>' + stats_html

# 'ProductA'와 'cat3' 기준으로 데이터 필터링
filtered_productA_df = df[df['cat1'] == 'ProductA']

# 박스플롯 생성
boxplot_img_data = create_boxplot_base64_for_val1_by_cat3(filtered_productA_df)

# 통계치 계산
stats_df = calculate_stats_for_val1_by_cat3(filtered_productA_df)

# HTML 컨텐츠 포맷팅 및 출력
html_content = format_boxplot_and_stats_to_html(boxplot_img_data, stats_df)
HTML(html_content)