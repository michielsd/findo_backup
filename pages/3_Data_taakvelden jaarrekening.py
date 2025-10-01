import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
import io
import openpyxl

@st.cache_resource
def get_data():
    FILEPATH = "https://github.com/michielsd/findo_backup/raw/refs/heads/main/data/rekening_batenlasten.pickle"
    data = pd.read_pickle(FILEPATH)

    return data


def get_unique_values(data, col):
    unique_values = data[col].unique().tolist()

    return unique_values


st.set_page_config(layout="wide")
search_container = st.container()
table_container = st.container()

with search_container:
    data = get_data()

    alle_gemeenten = get_unique_values(data, "Gemeenten")
    alle_jaren = ["Alle jaren"] + get_unique_values(data, "Jaar")
    alle_taakvelden = sorted(get_unique_values(data, "Taakveld"))
    blc = ["Baten", "Lasten", "Saldo"]

    col1, col2, col3 = st.columns([2,3,2])
    with col2:
        st.title("Data taakvelden jaarrekening")
        gemeenten = st.multiselect("Selecteer gemeenten",
                               alle_gemeenten,
                               default=None)
        jaren = st.multiselect("Selecteer jaren", alle_jaren, default=alle_jaren[-1])
        taakvelden = st.multiselect("Selecteer taakvelden",
                                  alle_taakvelden,
                                  default=None)
        blc = st.selectbox("Selecteer baten, lasten of saldo",
                             blc,
                             placeholder="Kies baten, lasten of saldo",
                             index=0)
        categorieen = [c for c in get_unique_values(data, "Categorie") if c.lower().startswith(blc.lower()[0])]
        subcategorie = st.multiselect("Selecteer subcategorie",
                                     categorieen,
                                     default=blc)

    if not gemeenten:
        gemeenten = alle_gemeenten
    if "Alle jaren" in jaren:
        jaren = alle_jaren
    if not taakvelden:
        taakvelden = alle_taakvelden
    
    data = data[data["Gemeenten"].isin(gemeenten) & data["Jaar"].isin(jaren)
                & data["Taakveld"].isin(taakvelden) & data["Categorie"].isin(subcategorie)]

    col1, col2, col3 = st.columns([2,2,3])
    with col1:
        excel_buffer = io.BytesIO()
        data.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        st.download_button(
            label="Download data als Excelbestand",
            data=excel_buffer,
            file_name="taakvelden_jaarrekening_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col3:
        pivot_to = st.selectbox("Verplaats naar kolommen",
                                ["Gemeenten", "Jaar", "Taakveld", "Categorie"],
                                placeholder="Kies een categorie",
                                index=None)
    if pivot_to:
        data = data.pivot(index=[col for col in data.columns if col != pivot_to and col !="Waarde"],
                          columns=pivot_to,
                          values="Waarde")
        data = data.reset_index()

with table_container:
    AgGrid(data)
    
