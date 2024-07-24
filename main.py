import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# Load the CSV file with 'euc-kr' encoding
file_path = '202406_202406_연령별인구현황_월간.csv'
data = pd.read_csv(file_path, encoding='euc-kr')

# Streamlit app
st.title("지역별 학부모와 자녀 인구 분석")

# Select regions for comparison
regions = st.multiselect("비교할 지역을 선택하세요:", data['행정구역'].unique())

# Check if regions are selected
if not regions:
    st.warning("비교할 지역을 선택해주세요.")
else:
    # Filter the data for the selected regions
    region_data = data[data['행정구역'].isin(regions)]

    # Define age ranges for children and parents
    children_ages = ['2024년06월_계_0세', '2024년06월_계_1세', '2024년06월_계_2세',
                     '2024년06월_계_3세', '2024년06월_계_4세', '2024년06월_계_5세',
                     '2024년06월_계_6세', '2024년06월_계_7세', '2024년06월_계_8세',
                     '2024년06월_계_9세', '2024년06월_계_10세', '2024년06월_계_11세',
                     '2024년06월_계_12세', '2024년06월_계_13세', '2024년06월_계_14세',
                     '2024년06월_계_15세', '2024년06월_계_16세', '2024년06월_계_17세', 
                     '2024년06월_계_18세']

    parents_ages = ['2024년06월_계_30세', '2024년06월_계_31세', '2024년06월_계_32세',
                    '2024년06월_계_33세', '2024년06월_계_34세', '2024년06월_계_35세',
                    '2024년06월_계_36세', '2024년06월_계_37세', '2024년06월_계_38세',
                    '2024년06월_계_39세', '2024년06월_계_40세', '2024년06월_계_41세',
                    '2024년06월_계_42세', '2024년06월_계_43세', '2024년06월_계_44세',
                    '2024년06월_계_45세', '2024년06월_계_46세', '2024년06월_계_47세',
                    '2024년06월_계_48세', '2024년06월_계_49세', '2024년06월_계_50세']

    # Ensure age columns are numeric and handle missing or malformed data
    def convert_to_numeric(column):
        return pd.to_numeric(column.replace(",", "", regex=True).fillna(0), errors='coerce')

    region_data[children_ages] = region_data[children_ages].apply(convert_to_numeric)
    region_data[parents_ages] = region_data[parents_ages].apply(convert_to_numeric)

    # Calculate the total population of children and parents in each region
    region_data['자녀 인구수'] = region_data[children_ages].sum(axis=1)
    region_data['학부모 인구수'] = region_data[parents_ages].sum(axis=1)

    # Create a line chart
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

    # Display the line chart
    st.pyplot(fig)
