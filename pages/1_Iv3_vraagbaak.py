import streamlit as st
import re
import requests

# Read the text file

GEMEENTEN_TAAKVELDEN_FILE = "https://github.com/michielsd/findo_backup/raw/refs/heads/main/data/gemeenten_taakvelden.txt"
PROVINCIES_TAAKVELDEN_FILE = "https://github.com/michielsd/findo_backup/raw/refs/heads/main/data/provincies_taakvelden.txt"
CATEGORIEN_FILE = "C:/Dashboard/Werk/streamlit/Findo2/data/iv3_categorieen.txt"	
BALANSPOSTEN_FILE = "C:/Dashboard/Werk/streamlit/Findo2/data/iv3_balansposten.txt"

##############
# TAAKVELDEN #
##############
response = requests.get(GEMEENTEN_TAAKVELDEN_FILE)
taakveld_content = response.text

# Initialize variables to store the current taakveld and its description
taakveld = ""
taakveld_description = ""

# Split the content into sections based on the bold headers
taakveld_dict_gemeenten = {}
for s in taakveld_content.split("\n"):
  if s.startswith("**") and s[2].isdigit() and s[4].isdigit():
    taakveld_dict_gemeenten[taakveld] = taakveld_description

    taakveld = s
    taakveld_description = ""
  elif s.startswith("**"):
    pass
  else:
    taakveld_description += s + "\n"

response = requests.get(PROVINCIES_TAAKVELDEN_FILE)
taakveld_content = response.text

# Initialize variables to store the current taakveld and its description
taakveld = ""
taakveld_description = ""

# Split the content into sections based on the bold headers
taakveld_dict_provincies = {}
for s in taakveld_content.split("\n"):
  if len(s) >= 4 and s.startswith("**") and s[2].isdigit() and s[4].isdigit():
    taakveld_dict_provincies[taakveld] = taakveld_description

    taakveld = s
    taakveld_description = ""
  elif s.startswith("**"):
    pass
  else:
    taakveld_description += s + "\n"  


col1, col2, col3 = st.columns([2,5,2])
with col2:
  st.title("Iv3 vraagbaak")
  st.markdown("")
  
  tab1, tab2 = st.columns([1,1])
  with tab1:
    onderwerp = st.selectbox("Selecteer taakveld, categorie of balanspost", ["Taakvelden"], index=0)
  with tab2:
    overheid = st.selectbox("Selecteer gemeenten of provincies", ["Gemeenten", "Provincies"], index=0)
  input = st.text_input("Voer uw zoekterm in")
  zoek_button = st.button("Zoek")


# Trigger if either Enter was pressed (user_input not empty) OR Search button clicked
if input and (zoek_button or st.session_state.get("last_input") != input):
    st.session_state["last_input"] = input  # save last search term
    
    if onderwerp == "Taakvelden" and overheid == "Gemeenten":
      output_dict = taakveld_dict_gemeenten
    elif onderwerp == "Taakvelden" and overheid == "Provincies":
      output_dict = taakveld_dict_provincies
    
    highlighted = f"<span style='background-color: yellow'>{input}</span>"
    output = ""
    pattern = re.compile(re.escape(input), re.IGNORECASE)

    for tv, desc in output_dict.items():
        if input and (input.lower() in tv.lower() or input.lower() in desc.lower()):
            tvo = pattern.sub(highlighted, tv)
            desco = pattern.sub(highlighted, desc)
            
            output += tvo + "<br>" + desco
            output += "\n-----\n"

    if output:
      st.markdown("")
      st.markdown("**Resultaten:**")
      st.markdown("---")
      st.markdown(output, unsafe_allow_html=True)
      st.write(output_dict)
    elif input and not output:
      st.write("Geen resultaten gevonden")