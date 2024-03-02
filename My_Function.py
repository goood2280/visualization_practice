# 필요한 라이브러리 임포트
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML
from io import BytesIO
import base64
from matplotlib.colors import ListedColormap
from scipy.interpolate import griddata
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle, PathPatch
import matplotlib.patheffects as PathEffects

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


# HTML 테이블 생성 및 맵 이미지 삽입 함수 - "Map" 문자열 변경
def create_html_table_with_maps(df):
    # CSS 스타일 정의
    style = """
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-family: Arial, sans-serif;
        }
        th, td {
            padding: 8px;
            border: 1px solid #ccc;
            text-align: center;
            font-size: 16px; /* 기본 글자 크기 */
        }
        th {
            background-color: #f0f0f0;
            font-size: 16px; /* 헤더 글자 크기 */
        }
        .value {
            font-weight: bold;
            font-size: 15px; /* 'Value' 글자 크기 */
        }
        img {
            width: auto;
            height: 80px; /* 이미지 높이 조정, 셀에 꽉 차게 */
            display: block;
            margin: auto;
        }
    </style>
    """

    html_str = style + '<table>'
    cat3_values = sorted(df['cat3'].unique())
    
    # 헤더 생성
    html_str += '<tr><td class="value">Value</td>' + ''.join([f'<td>{cat3}</td>' for cat3 in cat3_values]) + '</tr>'
    
    # 각 val 컬럼에 대해 행 추가
    for i, val in enumerate([f'val{i}' for i in range(1, 6)], start=1):
        html_str += f'<tr><td class="value">{val}</td>'
        for cat3 in cat3_values:
            mean_val = df[df['cat3'] == cat3][val].mean()
            html_str += f'<td>{mean_val:.2f}</td>'
        html_str += '</tr>'
        
        # 맵 이미지 삽입, "Map" 문자열을 "valX_map"으로 변경
        html_str += f'<tr><td class="value">{val}_map</td>'
        for cat3 in cat3_values:
            subset = df[df['cat3'] == cat3]
            img_data = plot_to_base64(subset['x'], subset['y'], subset[val])
            html_str += f'<td><img src="data:image/png;base64,{img_data}"></td>'
        html_str += '</tr>'
    
    html_str += '</table>'
    return html_str