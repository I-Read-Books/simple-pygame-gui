import pygame
from warnings import warn
from enum import Enum
from typing import Callable, Optional, Type
from scripts.ui_elements.ui_element import UIElement

class ButtonStates(Enum):
    HOLDING = 0
    HOVERED = 1
    DEFAULT = 2

class SimpleButtonSurface:
    def __init__(self, default_surf: pygame.Surface, pressed_surf: Optional[pygame.Surface]=None, hovered_surf: Optional[pygame.Surface]=None) -> None:
        self.default_surf = default_surf
        self.pressed_surf = pressed_surf if pressed_surf else default_surf
        self.hovered_surf = hovered_surf if hovered_surf else default_surf
        
    def get_current_surf(self, state: ButtonStates) -> pygame.Surface:
        match state:
            case ButtonStates.DEFAULT:
                return self.default_surf
            case ButtonStates.HOLDING:
                return self.pressed_surf
            case ButtonStates.HOVERED:
                return self.hovered_surf
            case err:
                warn(f'Unknown button state: {err}')
                return self.default_surf
                
class Button(UIElement):
    def __init__(
            self, 
            position_rect: pygame.Rect,
            ui_manager,
            callback: Callable,
            element_id: str,
            default_surf: Optional[pygame.Surface]=None,
            hovered_surf: Optional[pygame.Surface]=None,
            pressed_surf: Optional[pygame.Surface]=None,
            render_layer: Optional[str]=None,
            children: list[UIElement]=[],
        ) -> None:

        super().__init__(
            position_rect,
            ui_manager,
            element_id,
            render_layer,
            surface=default_surf,
            children=children
        )

        self.surface_finder = SimpleButtonSurface(
            default_surf if default_surf else pygame.Surface(self.position_rect.size), 
            pressed_surf, 
            hovered_surf
        )

        self.state = ButtonStates.DEFAULT

        self.callback = callback
        self.held_last_frame = False 

    def _update(self, mouse_pos: tuple, just_pressed: bool, just_released: bool, delta_time: float) -> None:
        if self.held_last_frame and self.metrics.hovering and self.metrics.just_released:
            self.callback()
        self.held_last_frame = self.metrics.holding

        if self.metrics.holding:
            self.state = ButtonStates.HOLDING
        elif self.metrics.hovering:
            self.state = ButtonStates.HOVERED
        else:
            self.state = ButtonStates.DEFAULT

        self.surface = self.surface_finder.get_current_surf(self.state)
    
    