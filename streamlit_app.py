import streamlit as st
import json
import pkg.selenium as selenium_service
import pkg.openai as openai_service

if 'selenium' not in st.session_state:
  st.session_state['selenium'] = selenium_service.Selenium()

if 'messages' not in st.session_state:
  st.session_state.messages = []

st.set_page_config(page_title='Linkedin Profiler', initial_sidebar_state='auto')

## Stremalit App
st.title('Linkedin Profiler')

with st.sidebar:
  # inputs de user e senha e botão de login
  user = st.text_input('Usuário')
  password = st.text_input('Senha', type='password')
  if st.button('Login'):
    selenium = st.session_state['selenium']
    selenium.login(user, password)
    st.success('Login realizado com sucesso!', icon="✅")
  else:
    st.info('Por favor, adicione as informações de login')


text_template = st.text_area('Quais os parâmetros de avaliação ?', height=200)

for message in st.session_state.messages:
  with st.chat_message(message['role'], avatar=message['role'] == 'assistant' and '👨‍💻' or '🧑🏻‍🏫'):    
    st.markdown(message['content'])

if profile_url := st.chat_input('url do perfil do linkedin'):
  if not user or not password:
    st.info('Por favor, adicione as informações de login')
    st.stop()
  if profile_url:
    with st.chat_message('user', avatar='🧑🏻‍🏫'):
      st.markdown(profile_url)
    with st.chat_message('assistant', avatar='👨‍💻'):
      with st.spinner('Consultando 🔍 ...'):
        selenium = st.session_state['selenium']
        selenium.set_page_source(profile_url)
        profile = selenium.get_profile()
        about = selenium.get_about()
        experience = selenium.get_experience()
        linkedin = f"Profile: {profile}, About: {about}, Experience: {experience}"

        openai = openai_service.Openai()
        summary = openai.summarize_profile(linkedin, text_template)
        st.markdown(summary)

    st.session_state.messages.append({'role': 'assistant', 'content': summary})
