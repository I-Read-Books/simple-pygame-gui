from __future__ import annotations
import pygame
from warnings import warn
from typing import Optional
from scripts.ui_elements.element_metrics import ElementMetrics

class UIElement:
    def __init__(
            self, 
            position_rect: pygame.Rect,
            ui_manager,
            element_id: str,
            render_layer: Optional[str]=None,
            surface: Optional[pygame.Surface]=None,
            children: list[UIElement]=[],
        ) -> None:

        self.position_rect = position_rect

        self.metrics = ElementMetrics(self.position_rect)

        self.surface = surface if surface else pygame.Surface(self.position_rect.size)
        if surface and surface.get_size() != self.position_rect.size:
            warn(f'Surface of element {element_id} does not match rect size... \n resizing to fit')
            self.surface = pygame.transform.smoothscale(surface, self.position_rect.size)
        
        self.children = children.copy()

        self.id = element_id
        self.render_layer = render_layer

        self.ui_manager = ui_manager
        self.ui_manager.add_element(self)

        self.collision_function = self.position_rect.collidepoint
        
    @property
    def topleft(self) -> tuple:
        return self.position_rect.topleft
    @topleft.setter
    def topleft(self, new_topleft: tuple) -> None:
        self._move_children(self.position_rect.topleft[0] - new_topleft[0], new_topleft[1] - self.position_rect.topleft[1])
        self.position_rect.topleft = new_topleft
    
    @property
    def center(self) -> tuple:
        return self.position_rect.center
    @center.setter
    def center(self, new_center: tuple) -> None:
        self._move_children(self.position_rect.center[0] - new_center[0], self.position_rect.center[1] - new_center[1])
        self.position_rect.center = new_center

    @property
    def size(self) -> tuple:
        return self.position_rect.size
    @property
    def right(self) -> int:
        return self.position_rect.right
    @property
    def bottom(self) -> int:
        return self.position_rect.bottom
    @property
    def left(self) -> int:
        return self.position_rect.left
    @property
    def top(self) -> int:
        return self.position_rect.top
    
    def move(self, delta_x: int, delta_y: int) -> None:
        self.topleft = (self.position_rect.topleft[0] + delta_x, self.position_rect.topleft[1] + delta_y)
    
    def _move_children(self, delta_x: int, delta_y: int) -> None:
        for child in self.children:
            child.move(delta_x, delta_y)
    
    def add_child(self, element: UIElement) -> None:
        self.children.append(element)
        
    def set_color(self, rgb: tuple) -> None:
        self.color = rgb

    def _handle_mouse(self, mouse_pos: tuple, just_pressed: bool, just_released: bool) -> None:
        mouse_collides = self.collide_point(mouse_pos)

        if mouse_collides and just_pressed:
            self.metrics.holding = True
        if just_pressed:
            #print('pressed')
            ...
        if just_released:
            #print('released')
            self.metrics.holding = False

        self.metrics.prev_mouse_pos = self.metrics.curr_mouse_pos
        self.metrics.curr_mouse_pos = mouse_pos
        
        self.metrics.prev_mouse_col_pos = self.metrics.curr_mouse_col_pos
        self.metrics.curr_mouse_col_pos = mouse_pos if mouse_collides else None

        self.metrics.hovering = mouse_collides
        self.metrics.just_pressed = mouse_collides and just_pressed
        self.metrics.just_released = mouse_collides and just_released

    def collide_point(self, point: tuple) -> bool:
        return self.collision_function(point)

    def update(self, mouse_pos: tuple, just_pressed: bool, just_released: bool, delta_time: float) -> None:
        self._handle_mouse(mouse_pos, just_pressed, just_released)

        self.metrics.time_holding += delta_time if self.metrics.holding else -self.metrics.time_holding
        self.metrics.time_hovering += delta_time if self.metrics.hovering else -self.metrics.time_hovering

        self._update(mouse_pos, just_pressed, just_released, delta_time)

    def _update(self, mouse_pos: tuple, just_pressed: bool, just_released: bool, delta_time: float) -> None:
        ...
            
    def render(self, dest_surf: pygame.Surface) -> None:
        dest_surf.blit(self.surface, self.topleft)

    def __repr__(self) -> str:
        return f'UiElement id \'{self.id}\' at topleft {self.topleft}'
        
