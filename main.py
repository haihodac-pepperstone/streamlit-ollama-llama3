import streamlit as st

from langchain_community.chat_models import ChatOllama
from langchain_community.callbacks import StreamlitCallbackHandler

model = "llama3"

st.header(f"Streamlit + Ollama + {model.capitalize()}")

st.markdown("""---""")

question_input = st.text_area("Enter question")
submit_button = st.button("Submit")

st.markdown("""---""")

answer_container = st.container()
st_callback = StreamlitCallbackHandler(answer_container)
llm = ChatOllama(model=model, callbacks=[st_callback])

if question_input and submit_button:
    response = llm.invoke(question_input)
    st_callback._current_thought._container.update(
        label="",
        state="complete",
        expanded=True,
    )
else:
    pass