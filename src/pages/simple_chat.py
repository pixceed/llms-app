import streamlit as st
from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.components.sidebar import sidebar_view



def main():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # if "chat_history" not in st.session_state:
    #     st.session_state.chat_history = []

    chat_model = ChatOpenAI()
    

    st.set_page_config(layout='wide', page_title="LLMS-APP", page_icon="👾")
    st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

    sidebar_view()

    st.markdown("# チャット")

    def reset():
        st.session_state.messages = []
    st.button("会話をリセット", on_click=reset)

    for m in st.session_state.messages:
        with st.chat_message(m[0]):
            st.markdown(m[1])

    if input_text := st.chat_input("質問をどうぞ"):

        st.session_state.messages.append(("user", input_text))

        with st.chat_message("user"):
            st.markdown(input_text)
        

        # with st.spinner("生成中..."):
        #     chat_template = ChatPromptTemplate.from_messages(st.session_state.messages)
        #     chat_prompt = chat_template.format_messages()
        #     llm_result = chat_model.invoke(chat_prompt)
            
            # with st.chat_message("assistant"):
            #     st.markdown(llm_result.content)

        chat_template = ChatPromptTemplate.from_messages(st.session_state.messages)
        chat_prompt = chat_template.format_messages()
        with st.chat_message("assistant"):
            llm_result = st.write_stream(chat_model.stream(chat_prompt))
        
        st.session_state.messages.append(("assistant", llm_result))

    


if __name__ == '__main__':
    main()