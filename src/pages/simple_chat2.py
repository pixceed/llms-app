from typing import Any, Dict, List

import streamlit as st

from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackManager
# from langchain.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from langchain_community.callbacks import get_openai_callback

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from components.button_right import align_button_right
from components.sidebar import sidebar_view

from modules.CostCalc import CostCalculateCallbackHandler

# class WrapStreamlitCallbackHandler(StreamlitCallbackHandler):
#     def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
#         pass

token_cost = {
    'GPT-3.5': {
        'input': 0.5 / 1000000,
        'output': 1.5 / 1000000,
    },
    'GPT-4': {
        'input': 10 / 1000000,
        'output': 30 / 1000000,
    },
    'Haiku': {
        'input': 0.25 / 1000000,
        'output': 1.25 / 1000000,
    },
    'Sonnet': {
        'input': 3 / 1000000,
        'output': 15 / 1000000,
    },
    'Opus': {
        'input': 15 / 1000000,
        'output': 75 / 1000000,
    },


}

@st.cache_resource
def load_conversation(model_type):
    template = """
    The following is a friendly conversation between a human and an AI. 
    The AI is talkative and provides lots of specific details from its context. 
    If the AI does not know the answer to a question, it truthfully says it does not know.
    回答の最後に"もっと詳しく知りたいことがあれば、遠慮なく聞いてほしい"という内容の文章を絶対に出力しないでください。

    AIの口調は、必ず語尾に「～のだ！」「～なのだ！」をつけます。
    口調例：詳しく説明させていただくのだ！
    口調例：変更することも可能なのだ！

    Current conversation:
    {history}
    Human: {input}
    AI Assistant:"""
    PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)

    handler = CostCalculateCallbackHandler()

    if model_type == "GPT-3.5":
        chat_model = ChatOpenAI(model='gpt-3.5-turbo-0125', temperature=0, streaming=True, callbacks=[handler])
    elif model_type == "GPT-4":
        chat_model = ChatOpenAI(model='gpt-4-0125-preview', temperature=0, streaming=True, callbacks=[handler])
    elif model_type == "Haiku":
        chat_model = ChatAnthropic(model='claude-3-haiku-20240307', temperature=0, streaming=True, callbacks=[handler])
    elif model_type == "Sonnet":
        chat_model = ChatAnthropic(model='claude-3-sonnet-20240229', temperature=0, streaming=True, callbacks=[handler])
    elif model_type == "Opus":
        chat_model = ChatAnthropic(model='claude-3-opus-20240229', temperature=0, streaming=True, callbacks=[handler])
    
    conversation = ConversationChain(
                prompt=PROMPT, 
                llm=chat_model, 
                verbose=False, 
                memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
                callbacks=[handler]
            )
    
    return conversation, handler

def main():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "token_total" not in st.session_state:
        st.session_state.token_total = {}

    st.set_page_config(layout="wide", page_title="LLMS-APP", page_icon="👾")
    st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    # with open( "style.css" ) as css:
    #     st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

    def reset():
        st.session_state.messages = []
        st.session_state.token_total = {}
        load_conversation.clear()

    align_button_right()
    sidebar_view()
    with st.sidebar:
        st.divider()
        select_llms = st.radio("LLMを選択", ["ChatGPT", "Claude"], label_visibility="collapsed", on_change=reset)    
        if select_llms == "ChatGPT":
            with st.container(border=True):
                model_type = st.radio("モデルを選択", ["GPT-3.5", "GPT-4"], horizontal=True, label_visibility="collapsed", on_change=reset)   

        elif select_llms == "Claude":
            with st.container(border=True):
                model_type = st.radio("モデルを選択", ["Haiku", "Sonnet", "Opus"], horizontal=True, label_visibility="collapsed", on_change=reset)

        

        if st.session_state.token_total != {}:
            st.divider()
            st.markdown("### Tokens Result")
            with st.container(border=True):
                st.write(f"Total Tokens: {st.session_state.token_total['total_tokens']}")
                st.write(f"Prompt Tokens: {st.session_state.token_total['prompt_tokens']}")
                st.write(f"Completion Tokens: {st.session_state.token_total['completion_tokens']}")
                st.write(f"Total Cost (USD): ${st.session_state.token_total['total_cost']:.4f}")

    # st.markdown("<h1 style='text-align: center; color: red;'>Some title</h1>", unsafe_allow_html=True)
    
    
    st.write("<p style='font-size:50px;font-weight:900;text-align: center;'>💬 CHAT</p>",  unsafe_allow_html=True)

    
    # with st.container(border=True):
    #     col1, col2 = st.columns([5, 1])
    #     col2.button("新規チャット", on_click=reset)
    col1, col2 = st.columns([2, 1])
    with col1.chat_message("ai"):
        st.markdown("なんでも聞くのだ！")
    col2.markdown(" ")
    col2.button("新規チャット", on_click=reset)

    conversation, handler = load_conversation(model_type)
    # if st.session_state.messages == []:
    #     st.session_state.messages.append(("ai", "なんでも聞くのだ！"))

    for m in st.session_state.messages:
        if m[0] == "ai":
            with st.chat_message("ai"):
                st.markdown(m[1])
        elif m[0] == "user":
            with st.chat_message("user"):
                st.markdown(m[1])

    if input_text := st.chat_input("質問をどうぞ"):

        st.session_state.messages.append(("user", input_text))

        with st.chat_message("user"):
            
            st.markdown(input_text)

        with st.chat_message("ai"):
            
            st_callback = StreamlitCallbackHandler(st.container())

            response = conversation.invoke(
                {"input": input_text}, {"callbacks": [st_callback]}
            )

            total_tokens = handler.total_tokens
            prompt_tokens = handler.prompt_tokens
            completion_tokens = handler.completion_tokens
            total_cost = token_cost[model_type]["input"] * prompt_tokens + token_cost[model_type]["output"] * completion_tokens

            print()
            print(response)
            print(f"Total Tokens: {total_tokens}")
            print(f"Prompt Tokens: {prompt_tokens}")
            print(f"Completion Tokens: {completion_tokens}")
            print(f"Total Cost (USD): ${total_cost}")
            print()

            st.session_state.token_total = {
                "total_tokens": total_tokens,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_cost": total_cost
            }


        st.session_state.messages.append(("ai", response['response']))
        st.rerun()
        

    


if __name__ == '__main__':
    main()