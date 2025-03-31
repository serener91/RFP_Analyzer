import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from common.pdf_extract import get_relevant_texts, extract_pdf
from common.utils import inference, fetch_prompt, convert_to_html
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os


load_dotenv()

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


# Define an async inference function
async def inference_async(gpt=False, system_msg="", query="", model="gpt-4o-mini", temperature=0.2):
    if gpt:
        client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY", None),
        )

        message = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": query}
        ]

        # Await the response
        chat_response = await client.chat.completions.create(
            model=model,
            messages=message,
            temperature=temperature,
            max_completion_tokens=8192,
            stream=False
        )

        return chat_response.choices[0].message.content


async def process_pdf_async():
    with st.spinner("Processing your PDF"):

        data = extract_pdf(uploaded_file)
        budget_texts, budget_ids = get_relevant_texts(data, filter_name="budget_extractor")
        time_texts, time_ids = get_relevant_texts(data, filter_name="time_extractor")
        mar_points, mar_ids = get_relevant_texts(data, filter_name="mar_summary")
        sfr_points, sfr_ids = get_relevant_texts(data, filter_name="sfr_summary")

    with st.spinner("Generating Summary"):

        # allows all inference_async calls to run in parallel,
        budget_info, time_info, mar_text, sfr_text = await asyncio.gather(
            inference_async(gpt=True, system_msg=fetch_prompt("budget_extractor"), query=budget_texts),
            inference_async(gpt=True, system_msg=fetch_prompt("time_extractor"), query=time_texts),
            inference_async(gpt=True, model="gpt-4o", system_msg=fetch_prompt("mar_summary"), query=mar_points),
            inference_async(gpt=True, model="gpt-4o", system_msg=fetch_prompt("sfr_summary"), query=sfr_points),
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

# Function to process PDF
def process_pdf():
    with st.spinner("Processing your PDF"):

        data = extract_pdf(uploaded_file)
        budget_texts, budget_ids = get_relevant_texts(data, filter_name="budget_extractor")
        time_texts, time_ids = get_relevant_texts(data, filter_name="time_extractor")
        mar_points, mar_ids = get_relevant_texts(data, filter_name="mar_summary")
        sfr_points, sfr_ids = get_relevant_texts(data, filter_name="sfr_summary")

    with st.spinner("Generating Summary"):

        budget_info = inference(
            gpt=True,
            system_msg=fetch_prompt("budget_extractor"),
            query=budget_texts
        )

        time_info = inference(
            gpt=True,
            system_msg=fetch_prompt("time_extractor"),
            query=time_texts
        )

        mar_text = inference(
            gpt=True,
            model="gpt-4o",
            system_msg=fetch_prompt("mar_summary"),
            query=mar_points,
        )

        sfr_text = inference(
            gpt=True,
            model="gpt-4o",
            system_msg=fetch_prompt("sfr_summary"),
            query=sfr_points
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
        # process_pdf()  # Process only when enabling columns
        asyncio.run(process_pdf_async())  # Process only when enabling columns
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
