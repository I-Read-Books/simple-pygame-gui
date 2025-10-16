import pygame
from time import time
from typing import Optional
from scripts.ui_elements.ui_element import UIElement

class UIInteractiveElement(UIElement):
    def __init__(
            self, 
            position_rect: pygame.Rect,
            ui_manager,
            element_id: str, 
            render_layer: Optional[str]=None,
            surface: Optional[pygame.Surface]=None, 
            children: list[UIElement]=[],
        ) -> None:

        # user's mouse is over object
        self.hovering = False
        self.time_hovering = 0

        # user is currently clicking/dragging object
        self.holding = False
        self.time_holding = 0

        super().__init__(position_rect, ui_manager, element_id, render_layer, surface, children)

    def handle_mouse_event(self, mouse_pos: tuple, just_pressed: bool, just_released: bool) -> None:
        mouse_collides = self.collide_point(mouse_pos)
        self.hovering = mouse_collides

        if mouse_collides and just_pressed:
            self._on_mouse_press()
            self.holding = True
        elif mouse_collides and just_released:
            self._on_mouse_release()

        if just_released:
            self.holding = False
    
    def _on_mouse_press(self) -> None:
        pass
    def _on_mouse_release(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        self.time_holding = self.time_holding + delta_time if self.holding else 0
        self.time_hovering = self.time_hovering + delta_time if self.hovering else 0

        self.surface.fill((min(int(self.time_holding * 80), 255), min(int(self.time_hovering * 80), 255), 0))

    def collide_point(self, point: tuple) -> bool:
        return self.position_rect.collidepoint(point) 
    

