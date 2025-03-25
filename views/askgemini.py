import streamlit as st
from sql_nlp_response import initialize_components, generate_natural_language_response

st.title("🔍 Database Query Chatbot")

# Initialize components
llm, db = initialize_components()

# Chat UI
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
    
    with st.chat_message("assistant"):
        response = generate_natural_language_response(llm, db, user_input)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})