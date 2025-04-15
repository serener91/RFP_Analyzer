import streamlit as st
from openai import OpenAI
from search_engine.utils import parse_config, get_character, convert_to_sentences, db_pipeline
from dotenv import load_dotenv
import os


load_dotenv()

import torch
torch.classes.__path__ = []


chara_nm = "rag_answer"
prompt, infos, description = parse_config(chara_nm, character_configs=get_character())
model_nm, temp, test_query = infos["model"]["name"], infos["model"]["temperature"], infos["query"]


client = OpenAI(
    # api_key=os.getenv("OPENAI_API_KEY", None),
    api_key="test123",
    base_url="http://175.196.78.7:30000/v1"
)


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": prompt}]

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)


if prompt := st.chat_input("Search your pdf"):
    with st.spinner("searching contexts"):
        contexts, context_ids, sources = db_pipeline(search_query=prompt, collection_name="gto", update_index=False)
        search_result = convert_to_sentences(context_ids, sources, contexts)

        source_list = ""
        for idx, i in enumerate(zip(sources, context_ids)):
            source_list += f"(p{i[1]}) from {i[0]} <br>"

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        messages = []
        for m in st.session_state.messages:
            if m["role"] == "user":
                messages.append({"role": m["role"], "content": m["content"] + search_result})
            else:
                messages.append({"role": m["role"], "content": m["content"]})

        client_response = client.chat.completions.create(
            model="vllm",  #st.session_state["openai_model"],
            messages=messages,
            stream=True,
            temperature=1.2
        )

        full_response = ""
        for chunk in client_response:
            if chunk:
                text = chunk.choices[0].delta.content
                if text is not None:
                    full_response += text
            message_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)  # animated typing effect
        message_placeholder.markdown(full_response + f"\n\n<strong>Sources:</strong> <br> {source_list}", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    print(full_response)
