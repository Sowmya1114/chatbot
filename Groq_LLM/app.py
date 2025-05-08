import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("groq_api_key")

st.sidebar.title("Personalization")
prompt = st.sidebar.title("System Prompt: ")
model = st.sidebar.selectbox('Choose a model', ['Llama3-8b-8192', 'Llama3-70b-8192'])

#Groq client
client = Groq(api_key = groq_api_key)

#Streamlit Interface
st.title("💬 Ask Me")

#Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []
with st.form("formid"):
    user_input = st.text_input("Enter your query: ", "")
    submit=st.form_submit_button("Submit")
    if submit:
        chat_completion = client.chat.completions.create(
        messages=[
            {
                "role" : "user",
                "content" : user_input,
            }
        ],
        model = model,
        )
        response = chat_completion.choices[0].message.content
        st.session_state.history.append({"query" : user_input, "response" : response})

    #Display the response
        st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)

#Display history
st.sidebar.title("History")
for i, entry in enumerate(st.session_state.history):
    if st.sidebar.button(f'Query {i+1}: {entry["query"]}'):
        st.markdown(f'<div class="response-box">{entry["response"]}</div>', unsafe_allow_html=True)