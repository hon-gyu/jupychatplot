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
    def __init__(
        self,
        tally_choice: int = 0,
        append_tally: bool = False,
    ):
        self.is_running = False
        self.output = widgets.Output()
        self.frames = self.tallies[tally_choice][0]
        self.tally = self.tallies[tally_choice][1]
        self.append_tally = append_tally

    @property
    def tallies(self) -> list[tuple[list[str], str]]:
        return [
            (["-", "\\", "|", "/"], "x"),
            (["一", "丄", "上", "止", "正"], "正"),
        ]

    def get_frame(self, frame_idx: int) -> str:
        d, r = divmod(frame_idx, len(self.frames))
        if not self.append_tally:
            frame = self.frames[r]
        else:
            frame = f"{self.tally * d}{self.frames[r]}"
        return frame

    def animate(self):
        frame_idx = 0
        while self.is_running:
            with self.output:
                self.output.clear_output(wait=True)
                display(HTML(f"Thinking: {self.get_frame(frame_idx)}"))
            frame_idx += 1
            time.sleep(1 / len(self.frames))

    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self.animate)
        self.thread.start()

    def stop(self):
        self.is_running = False
        self.thread.join()
        self.output.clear_output()

    def display(self):
        return self.output


class ChatInterface:
    def __init__(self):
        self.chat_history: list[BaseMessage] = []
        self.input = widgets.Text(placeholder="What's up?")
        self.input.continuous_update = False
        self.input.observe(self.handler, names="value")
        self.output = widgets.Output(layout=widgets.Layout(border="1px solid black"))
        self.loading_bar = LoadingAnimation(0, False)
        self.chat_model = get_chat_model()

    def format_message(self, role: str, content: str) -> str:
        return f'<div style="font-size: 1.2em"><b>{role}:</b> {content}</div>'

    def handler(self, change: dict):
        if change["new"].strip() == "":
            return
        q_msg = HumanMessage(content=change["new"])
        self.input.value = ""

        with self.output:
            display(HTML(self.format_message("You", q_msg.content)))

        try:
            self.loading_bar.start()
            a_msg = self.chat_model.invoke(self.chat_history + [q_msg])
            self.chat_history.extend([q_msg, a_msg])
            self.loading_bar.stop()
            with self.output:
                display(HTML(self.format_message("Assistant", a_msg.content)))

        except Exception as e:
            self.loading_bar.stop()
            with self.output:
                display(HTML(self.format_message("Error", str(e))))

    def display(self):
        return widgets.VBox(
            [
                self.output,
                self.loading_bar.output,
                self.input,
            ]
        )
