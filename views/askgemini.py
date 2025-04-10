import streamlit as st
from sql_nlp_response import get_natural_language_result

st.title("🔍 Database Query Chatbot")

# Initialize components

# Chat UI session state
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask a question about the database...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    response = get_natural_language_result(user_input)
    
    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})