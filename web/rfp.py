import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from common.pdf_extract import (
    mar_filter,
    sfr_filter,
    budget_filter,
    time_filter,
    extract_pdf
)
from common.utils import inference, fetch_prompt, convert_to_html

#import torch
#torch.classes.__path__ = []

st.set_page_config(layout="wide")

with st.sidebar:
    uploaded_file = st.file_uploader('Upload your PDF', type="pdf")
    if uploaded_file is not None:
        st.markdown(f"Uploaded PDF:\n\n{uploaded_file.name}")

# Initialize session state
if "show_columns" not in st.session_state:
    st.session_state.show_columns = False
if "summary" not in st.session_state:
    st.session_state.summary = None
if "relevant_pages" not in st.session_state:
    st.session_state.relevant_pages = []


# Function to process PDF
def process_pdf():
    with st.spinner("Processing your PDF"):
        data = extract_pdf(uploaded_file)

    with st.spinner("Generating Summary"):
        texts = data["texts"]
        pg_nums = data["page_numbers"]
        budget_texts, budget_ids = budget_filter(texts, pg_nums)
        time_texts, time_ids = time_filter(texts, pg_nums)
        mar_points, mar_ids = mar_filter(texts, pg_nums)
        sfr_points, sfr_ids = sfr_filter(texts, pg_nums)

        budget_info = inference(
            gpt=True,
            system_msg=fetch_prompt("budget_extractor"),
            query=" ".join(budget_texts)
        )

        time_info = inference(
            gpt=True,
            system_msg=fetch_prompt("time_extractor"),
            query=" ".join(time_texts)
        )

        mar_text = inference(
            gpt=True,
            system_msg=fetch_prompt("mar_summary", version=2),
            query=" ".join(mar_points),
        )

        sfr_text = inference(
            gpt=True,
            system_msg=fetch_prompt("sfr_summary"),
            query=" ".join(sfr_points)
        )

    with st.spinner("Summing up"):
        st.session_state.summary = convert_to_html(
            file_name=uploaded_file.name,
            budget_text=budget_info,
            time_text=time_info,
            mar_text=mar_text,
            sfr_text=sfr_text
        )

    st.session_state.relevant_pages = list(set(budget_ids + time_ids + mar_ids + sfr_ids))


# Function to toggle columns and process PDF if needed
def toggle_columns():
    if not st.session_state.show_columns:
        process_pdf()  # Process only when enabling columns
    st.session_state.show_columns = not st.session_state.show_columns


# Button to trigger processing
st.button(
    label="Clear" if st.session_state.show_columns else "Analyze",
    on_click=toggle_columns,
    icon=":material/mood:" if st.session_state.show_columns else "😃",
    use_container_width=True
)

# Show columns if processing is complete
if st.session_state.show_columns and st.session_state.summary:
    col1, col2 = st.columns(2, gap="large", border=True)

    with col1:
        st.header("Summary")
        st.html(st.session_state.summary)

    with col2:
        st.header("PDF")
        pdf_viewer(
            uploaded_file.getvalue(),  # AttributeError
            width=800,
            pages_to_render=[int(i) for i in st.session_state.relevant_pages]
        )
