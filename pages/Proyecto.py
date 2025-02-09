import streamlit as st
from openai import OpenAI


st.title("ChatGpt")
cliente = OpenAI(api_key="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")

# creamos la variable de historia del chat

if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Mostrar la Historia
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# Entrada de chat        
if prompt := st.chat_input("Escribe tu mensaje aqui..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    # Añadimos el mensaje del user a la historia del chat
    st.session_state.messages.append({"role":"user","content":prompt})
    
    # obtener la respuesta de openai
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            stream = cliente.chat.completions.create(
                model="gpt-4o-mini", 
                messages=[
                {"role":"system",
                 "content":"Eres un asistente amable y servicial, que proporciona respuestas clara y concisas. Tu eres un asistente humano y te llamas OSCAR"},
                *[{"role":m["role"], "content": m["content"]} for m in st.session_state.messages]
            ], 
            stream = True     
            )
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    message_placeholder.markdown(full_response + " ")
            message_placeholder.markdown(full_response)        
            st.session_state.messages.append({"role":"assistant", "content": full_response}) 
                
                
        except Exception as e:
            st.error(f"Error: {str(e)}")    
