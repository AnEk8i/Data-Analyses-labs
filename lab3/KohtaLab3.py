import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Аналіз даних VCI/TCI/VHI")

provinces = {
    1: 'Vinnytsya', 2: 'Volyn', 3: "Dnipropetrovs'k", 4: "Donets'k", 5: 'Zhytomyr', 6: 'Transcarpathia',
    7: 'Zaporizhzhya', 8: "Ivano-Frankivs'k", 9: 'Kiev City',
    10: 'Kiev', 11: 'Kirovohrad', 12: "Luhans'k", 13: "L'viv", 14: 'Mykolayiv', 15: 'Odessa', 16: 'Poltava',
    17: 'Rivne', 18: "Sevastopol'",
    19: 'Sumy', 20: "Ternopil'", 21: 'Kharkiv', 22: 'Kherson', 23: "Khmel'nyts'kyy", 24: 'Cherkasy', 25: 'Chernivtsi',
    26: 'Chernihiv', 27: 'Crimea'
}


def data_loading():
    data_frame = pd.read_csv(r"D:/PYTHON/PycharmProjects/JupyterProject/forlab2/combined_df.csv")
    data_frame = data_frame.rename(columns={"year": "Рік", "week": "Тиждень", "vci": "VCI", "tci": "TCI", "vhi": "VHI", "oblast": "Область"})
    data_frame["Область"] = data_frame["Область"].map(provinces)
    return data_frame


df = data_loading()

# st.subheader("Поточний стан session_state:")
# if st.session_state:
#     for key, value in st.session_state.items():
#         st.write(f"**{key}**: {value}")
# else:
#     st.write("Session state порожній")
#
# st.divider()

if "filters_reset" not in st.session_state:
    st.session_state.filters_reset = 0

st.subheader("Аналіз")

st.sidebar.title("Фільтри")
selected_area = st.selectbox("Область", options=list(provinces.values()), index=0,
                             key=f"area_{st.session_state.filters_reset}")
selected_index = st.selectbox("Індекс", ["VCI", "TCI", "VHI"], index=0,
                                      key=f"index_{st.session_state.filters_reset}")
selected_years = st.sidebar.slider("Рік", 1982, 2024, (1982, 2024),
                                   key=f"years_{st.session_state.filters_reset}")
selected_weeks = st.sidebar.slider("Тиждень", 1, 52, (1, 52),
                                   key=f"weeks_{st.session_state.filters_reset}")

st.sidebar.subheader("-- Сортування --")
sort_asc = st.sidebar.checkbox("За зростанням", key=f"sort_a_{st.session_state.filters_reset}")
sort_desc = st.sidebar.checkbox("За спаданням", key=f"sort_b_{st.session_state.filters_reset}")

if sort_asc and sort_desc:
    st.sidebar.warning("! Обрано обидва типи сортування !")
    sort_asc = False
    sort_desc = False

if st.sidebar.button("Скинути фільтри"):
    st.session_state.filters_reset += 1
    st.rerun()

filtered_df = df[
    (df["Область"] == selected_area) &
    (df["Рік"].between(*selected_years)) &
    (df["Тиждень"].between(*selected_weeks))
]

if sort_asc:
    filtered_df = filtered_df.sort_values(by=selected_index, ascending=True)
elif sort_desc:
    filtered_df = filtered_df.sort_values(by=selected_index, ascending=False)

tab1, tab2, tab3 = st.tabs(["Таблиця", "Графік", "Порівняння"])
with tab1:
    st.subheader("Відфільтровані дані")
    columns_to_display = ["Рік", "Тиждень", "Область", selected_index]
    st.dataframe(filtered_df[columns_to_display], use_container_width=True)

with tab2:
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=filtered_df, x="Рік", y=selected_index, ax=ax, marker='o', color='orange')
    ax.set_title(f"Середнє значення {selected_index} для '{selected_area}' по роках\n")
    ax.set_xlabel("Рік")
    ax.set_ylabel(f"Середній {selected_index}")
    st.pyplot(fig)

with tab3:
    compare_df = df[
        (df["Рік"].between(*selected_years)) &
        (df["Тиждень"].between(*selected_weeks))
    ]

    avg_values = compare_df.groupby("Область")[selected_index].mean().reset_index().sort_values(by=selected_index, ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=avg_values, x=selected_index, y="Область", ax=ax, palette="rocket")
    ax.set_title(f"Середній {selected_index} по всіх областях")
    st.pyplot(fig)
