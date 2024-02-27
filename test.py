import pandas as pd
import numpy as np

# 기본 데이터 프레임 설정
np.random.seed(0)  # 결과 일관성을 위해
data = {
    'cat1': np.random.choice(['ProductA', 'ProductB'], 100),
    'cat2': np.random.choice(['Setting1', 'Setting2'], 100),
    'cat3': np.random.randint(1, 31, 100),
    'x': np.random.randint(1, 21, 100),
    'y': np.random.randint(1, 21, 100),
    'datetime': pd.date_range(start='2021-01-01', periods=100, freq='D')
}

df = pd.DataFrame(data)

# val1~val200까지의 값을 가지는 열을 한 번에 추가
vals = {f'val{val_num}': np.random.random(100) for val_num in range(1, 201)}
vals_df = pd.DataFrame(vals)

# 원래 DataFrame과 새로운 열을 합치기
df = pd.concat([df, vals_df], axis=1)
