import pandas as pd
from langchain_core.messages import AIMessage, BaseMessage

from jupychatplot.chat_widget import ChatInterface


class DataFrameChat(ChatInterface):
    def __init__(self, df: pd.DataFrame, metadata: dict):
        """
        Args:
            df: The DataFrame to chat with.
            metadata: The metadata of the DataFrame.
        """
        super().__init__()
        self.df = df
        self.metadata = metadata

    def chat(self, messages: list[BaseMessage]) -> AIMessage:
        return super().chat(messages)
