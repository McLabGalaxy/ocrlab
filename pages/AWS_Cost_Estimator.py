from pathlib import Path
import streamlit as st

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

st.header("Cost Estimator")

# multi = '''If you end a line with two spaces,
# a soft return is used for the next line.

# Two (or more) newline characters in a row will result in a hard return.
# '''
# st.markdown(multi)

tab1, tab2, tab3 = st.tabs(["Compute", "Storage", "Network"])

with tab1:
   st.header("Compute")
   #st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
   st.header("Storage")
   #st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("Network")
   #st.image("https://static.streamlit.io/examples/owl.jpg", width=200)


intro_markdown = read_markdown_file("pages/COST_OVERVIEW.md")
st.markdown(intro_markdown, unsafe_allow_html=True)
