import pygame
from typing import Optional, Callable
from scripts.ui_elements.ui_element import UIElement
from scripts.ui_elements.ui_interactive_element import UIInteractiveElement

class Button(UIInteractiveElement):
    def __init__(
            self, 
            position_rect: pygame.Rect,
            ui_manager,
            element_id: str, 
            callback: Callable,
            callback_args: Optional[list],
            render_layer: Optional[str]=None,
            surface: Optional[pygame.Surface]=None, 
            children: list[UIElement]=[],
        ) -> None:

        self.callback = callback
        self.callback_args = callback_args

        super().__init__(position_rect, ui_manager, element_id, render_layer, surface, children)
    
    def _on_mouse_release(self) -> None:
        if not self.holding: 
            return
        if self.callback_args:
            self.callback(*self.callback_args)
        else:
            self.callback()