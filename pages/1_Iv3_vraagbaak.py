import streamlit as st
import re

# Read the text file
GEMEENTEN_TAAKVELDEN_FILE = "C:/Dashboard/Werk/streamlit/findo2/data/gemeenten_taakvelden.txt"
with open(GEMEENTEN_TAAKVELDEN_FILE, "r", encoding="utf-8") as f:
  content = f.read()

# Initialize variables to store the current taakveld and its description
taakveld = ""
taakveld_description = ""

# Split the content into sections based on the bold headers
taakveld_dict = {}
for s in content.split("\n"):
  if s.startswith("**") and s[2].isdigit() and s[4].isdigit():
    taakveld_dict[taakveld] = taakveld_description

    taakveld = s
    taakveld_description = ""
  else:
    taakveld_description += s + "\n"


col1, col2, col3 = st.columns([2,5,2])
with col2:
  st.title("Iv3 vraagbaak")
  st.markdown("")
  input = st.text_input("Voer uw zoekterm in")
  zoek_button = st.button("Zoek")


# Trigger if either Enter was pressed (user_input not empty) OR Search button clicked
if input and (zoek_button or st.session_state.get("last_input") != input):
    st.session_state["last_input"] = input  # save last search term
    
    highlighted = f"<span style='background-color: yellow'>{input}</span>"
    output = ""
    pattern = re.compile(re.escape(input), re.IGNORECASE)

    for tv, desc in taakveld_dict.items():
        if input and (input.lower() in tv.lower() or input.lower() in desc.lower()):
            tvo = pattern.sub(highlighted, tv)
            desco = pattern.sub(highlighted, desc)
            
            output += tvo + "<br>" + desco
            output += "<br>---<br>"

    if output:
      st.markdown("")
      st.markdown("**Resultaten:**")
      st.markdown("---")
      st.markdown(output, unsafe_allow_html=True)
    elif input and not output:
      st.write("Geen resultaten gevonden")