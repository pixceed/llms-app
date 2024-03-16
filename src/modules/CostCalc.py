import tiktoken

from typing import Any, Dict, List
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import BaseMessage
from langchain.schema.output import LLMResult


def num_tokens_from_messages(messages: List[BaseMessage], model="gpt-3.5-turbo-0613"):
    encoding = tiktoken.encoding_for_model(model)
    tokens_per_message = 3
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        num_tokens += len(encoding.encode(message.type))
        num_tokens += len(encoding.encode(message.content))
    num_tokens += 3
    return num_tokens


class CostCalculateCallbackHandler(BaseCallbackHandler):
    token = ""
    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        self.token += token

    def on_llm_end(
            self,
            response: LLMResult,
            **kwargs: Any,
    ) -> Any:
        self.completion_tokens = len(self.encoding.encode(self.token))
        self.total_tokens = self.completion_tokens + self.prompt_tokens

    def on_chain_end(
            self,
            outputs: Dict[str, Any],
            **kwargs: Any,
    ) -> Any:
        self.completion_tokens = len(self.encoding.encode(self.token))
        self.total_tokens = self.completion_tokens + self.prompt_tokens

    def on_chat_model_start(
            self,
            serialized: Dict[str, Any],
            messages: List[List[BaseMessage]],
            **kwargs: Any,
    ) -> Any:
        for m in messages:
            self.prompt_tokens = num_tokens_from_messages(m)