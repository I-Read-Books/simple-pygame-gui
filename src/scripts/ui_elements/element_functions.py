import pygame
from scripts.ui_elements.element_metrics import ElementMetrics
from abc import ABC, abstractmethod
from typing import Callable, Optional, Any

class ElementFunction(ABC):
    @abstractmethod
    def execute(self, metrics: ElementMetrics) -> Any:
        ...

class ButtonFunction(ElementFunction):
    def __init__(self, callback: Callable, callback_args: Optional[list[Any]]=None) -> None:
        self.callback = callback
        self.callback_args = callback_args

        # ugly work around to make sure it only activates when held and just 
        # released becuase held and just released will never be true on same frame
        self.held_last_frame = False

    def execute(self, metrics: ElementMetrics) -> None:
        if self.held_last_frame and metrics.hovering and metrics.just_released:
            if self.callback_args is not None:
                self.callback(*self.callback_args)
            else:
                self.callback()
        self.held_last_frame = metrics.holding

