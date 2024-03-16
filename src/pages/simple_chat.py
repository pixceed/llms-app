import streamlit as st
from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from components.button_right import align_button_right
from components.sidebar import sidebar_view



def main():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.set_page_config(layout='wide', page_title="LLMS-APP", page_icon="👾")
    st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

    align_button_right()
    sidebar_view()

    st.markdown("# チャット")

    system_template = """
    会話履歴を踏まえて、質問に回答してください。
    回答はできるだけ簡潔にしてください。

    [会話履歴]
    {messages}

    [回答]
    """
    human_template = "{question}"

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", human_template),
    ])
    
    with st.container(border=True):
        col1, col2 = st.columns([1, 1])
        def change_model():
            st.session_state.messages = []
        model_type = col1.radio("モデルを選択", ["GPT-3.5", "GPT-4"], horizontal=True, label_visibility="collapsed", on_change=change_model)
        if model_type == "GPT-3.5":
            chat_model = ChatOpenAI(model='gpt-3.5-turbo-0125', temperature=0)
        elif model_type == "GPT-4":
            chat_model = ChatOpenAI(model='gpt-4-0125-preview', temperature=0)
        else:
            chat_model = ChatOpenAI(model='gpt-3.5-turbo-0125', temperature=0)
        
        # chat_chain = chat_prompt | chat_model

        # col2.markdown(" ")
        def reset():
            st.session_state.messages = []
        col2.button("会話をリセット", on_click=reset)

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
        # past_messages = ChatPromptTemplate.from_messages(st.session_state.messages).format_messages()
        with st.chat_message("assistant"):
            llm_result = st.write_stream(chat_model.stream(chat_prompt))
            # llm_result = st.write_stream(chat_chain.stream({"messages":past_messages, "question":input_text}))
        
        # st.session_state.messages.append(("user", input_text))
        st.session_state.messages.append(("assistant", llm_result))

    


if __name__ == '__main__':
    main()