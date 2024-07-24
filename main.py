import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

st.title("테스트 앱")

# 간단한 테스트 데이터
data = pd.DataFrame({
    '행정구역': ['서울', '부산', '대구'],
    '2024년06월_계_0세': [100, 200, 150],
    '2024년06월_계_30세': [300, 400, 350]
})

regions = st.multiselect("비교할 지역을 선택하세요:", data['행정구역'].unique())

if not regions:
    st.warning("비교할 지역을 선택해주세요.")
else:
    region_data = data[data['행정구역'].isin(regions)]

    children_ages = ['2024년06월_계_0세']
    parents_ages = ['2024년06월_계_30세']

    region_data[children_ages] = region_data[children_ages].apply(pd.to_numeric, errors='coerce')
    region_data[parents_ages] = region_data[parents_ages].apply(pd.to_numeric, errors='coerce')

    region_data['자녀 인구수'] = region_data[children_ages].sum(axis=1)
    region_data['학부모 인구수'] = region_data[parents_ages].sum(axis=1)

    fig, ax = plt.subplots()

    for region in regions:
        region_subset = region_data[region_data['행정구역'] == region]
        if not region_subset.empty:
            ax.plot(['자녀 인구수', '학부모 인구수'], 
                    [region_subset['자녀 인구수'].values[0], region_subset['학부모 인구수'].values[0]], 
                    label=region)
    
    ax.set_xlabel('인구 구분')
    ax.set_ylabel('인구수')
    ax.legend()
    ax.set_title('지역별 학부모와 자녀 인구 비교')

    st.pyplot(fig)
