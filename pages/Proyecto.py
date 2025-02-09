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
