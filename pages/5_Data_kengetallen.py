import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
import io
import openpyxl

@st.cache_resource
def get_data():
    FILEPATH = "C:/Dashboard/Werk/streamlit/Findo2/data/kengetallen.pickle"
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

    alle_gemeenten = sorted(get_unique_values(data, "Gemeenten"))
    alle_begrotingen = get_unique_values(data, "Begroting")
    alle_jaren = ["Alle jaren"] + get_unique_values(data, "Jaar")
    alle_kengetallen = get_unique_values(data, "Kengetal")
    alle_type_ramingen = get_unique_values(data, "Type raming")
    
    col1, col2, col3 = st.columns([2,3,2])
    with col2:
        st.title("Data kengetallen")
        gemeenten = st.multiselect("Selecteer gemeenten",
                               alle_gemeenten,
                               default=None)
        kengetallen = st.multiselect("Selecteer kengetallen",
                                  alle_kengetallen,
                                  default=None)
        begrotingen = st.multiselect("Selecteer begrotingen",
                               alle_begrotingen,
                               default=alle_begrotingen[-1])
        jaren = st.multiselect("Selecteer jaren", alle_jaren, default=alle_jaren[-6:])
        separate_type_ramingen = st.toggle("Jaarrekening-, begroting- en meerjarenramingen apart", value=False)
        if separate_type_ramingen:
            type_ramingen = st.multiselect("Selecteer type raming", alle_type_ramingen, default=alle_type_ramingen)
        
    if not gemeenten:
        gemeenten = alle_gemeenten
    if "Alle jaren" in jaren:
        jaren = alle_jaren
    if not kengetallen:
        kengetallen = alle_kengetallen
    if separate_type_ramingen:
        data = data[data["Gemeenten"].isin(gemeenten) & data["Jaar"].isin(jaren)
                & data["Type raming"].isin(type_ramingen)
                & data["Kengetal"].isin(kengetallen) & data["Begroting"].isin(begrotingen)]
    else:
        data = data.drop(columns=["Type raming"])
        data = data[data["Gemeenten"].isin(gemeenten) & data["Jaar"].isin(jaren)
                & data["Kengetal"].isin(kengetallen) & data["Begroting"].isin(begrotingen)]

    col1, col2, col3 = st.columns([2,2,3])
    with col1:
        excel_buffer = io.BytesIO()
        data.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        st.download_button(
            label="Download data als Excelbestand",
            data=excel_buffer,
            file_name="kengetallen_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col3:
        pivot_to = st.selectbox("Verplaats naar kolommen",
                                ["Gemeenten", "Jaar", "Kengetal", "Begroting"],
                                placeholder="Kies een categorie",
                                index=None)
    if pivot_to:
        data = data.pivot(index=[col for col in data.columns if col != pivot_to and col !="Waarde"],
                          columns=pivot_to,
                          values="Waarde")
        data = data.reset_index()

with table_container:
    AgGrid(data)
    
