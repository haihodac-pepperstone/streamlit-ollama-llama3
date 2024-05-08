import ollama
from openai import OpenAI
import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain_community.callbacks import StreamlitCallbackHandler


@st.cache_resource
def list_model():
    models = [m["name"].split(":")[0] for m in ollama.list()["models"]]
    return models


st.title("Chat with Oh-🦙")
model_name = st.selectbox("Select model", list_model())

if "model_name" not in st.session_state:
    st.session_state["model_name"] = model_name

if "messages" not in st.session_state:
    st.session_state.messages = []

# Hit `New conversation to reload model and clear messages
new_conversation = st.button("New conversation")
if new_conversation:
    st.session_state["model_name"] = model_name
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


st.markdown("""---""")

client = OpenAI(
    base_url="http://localhost:11434/v1/",
    api_key="ollama",
)

if prompt := st.chat_input(f"Chat with {st.session_state['model_name']}:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
