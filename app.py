"""Streamlit front end for the Group 1 health research prototype."""

import streamlit as st

from crew_prototype import run_research

st.set_page_config(page_title="Health Research Assistant", page_icon=":stethoscope:", layout="wide")

st.title("Health research assistant")
st.caption("COMP 248 Group 1. Prototype of the retrieval agent and the reflection agent.")

st.write(
    "A research analyst asks a general health question. "
    "The retrieval agent searches the local health notes with naive RAG. "
    "The reflection agent scores that brief and rewrites it if the score is below 4. "
    "Questions that look like an emergency are not sent to the model."
)

question = st.text_area(
    "Research question",
    placeholder="Example: How is a cold different from influenza, and when should someone seek care?",
    height=120,
)

if st.button("Run research", type="primary"):
    if not question.strip():
        st.warning("Enter a question first.")
    else:
        with st.spinner("Working through retrieval and reflection..."):
            try:
                result = run_research(question)
            except Exception as error:  # shown to the analyst; the crew can fail on a bad key
                st.error(f"The run stopped: {error}")
            else:
                st.subheader("Route")
                st.write(result["route"])
                st.subheader("Brief")
                st.write(result["answer"])
                if result["passages"]:
                    st.subheader("Passages retrieved from Chroma")
                    for passage in result["passages"]:
                        with st.expander(f"{passage['topic']}  (distance {passage['score']:.3f})"):
                            st.write(passage["text"])
