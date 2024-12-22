import os
import threading
import time
from functools import lru_cache

import ipywidgets as widgets
from IPython.display import HTML, display
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage


@lru_cache(maxsize=1)
def get_chat_model() -> BaseChatModel:
    return ChatAnthropic(
        model="claude-3-opus-20240229",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        temperature=0.0,
    )


class LoadingAnimation:
    def __init__(self):
        self.is_running = False
        self.frames = ["-", "\\", "|", "/"]
        self.output = widgets.Output()

    def animate(self):
        frame_idx = 0
        while self.is_running:
            with self.output:
                self.output.clear_output(wait=True)  # Important: use wait=True
                display(HTML(f"<b>Thinking {self.frames[frame_idx]}</b>"))
            frame_idx = (frame_idx + 1) % len(self.frames)
            time.sleep(0.1)

    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self.animate)
        self.thread.start()

    def stop(self):
        self.is_running = False
        self.thread.join()
        self.output.clear_output()


class ChatInterface:
    def __init__(self):
        self.chat_history: list[BaseMessage] = []
        self.input = widgets.Text(placeholder="What's up?")
        self.input.continuous_update = False
        self.input.observe(self.handler, names="value")
        self.output = widgets.Output(layout=widgets.Layout(border="1px solid black"))
        self.loading_bar = LoadingAnimation()
        self.chat_model = get_chat_model()

    def handler(self, change: dict):
        if change["new"].strip() == "":
            return
        q_msg = HumanMessage(content=change["new"])
        self.input.value = ""

        with self.output:
            display(HTML(f"<b>You:</b> {q_msg.content}"))

        try:
            self.loading_bar.start()
            a_msg = self.chat_model.invoke(self.chat_history + [q_msg])
            self.chat_history.extend([q_msg, a_msg])
            self.loading_bar.stop()
            with self.output:
                display(HTML(f"<b>Assistant:</b> {a_msg.content}"))

        except Exception as e:
            self.loading_bar.stop()
            with self.output:
                display(HTML(f"<b>Error:</b> {str(e)}"))

    def display(self):
        return widgets.VBox(
            [
                self.output,
                self.loading_bar.output,
                self.input,
            ]
        )
