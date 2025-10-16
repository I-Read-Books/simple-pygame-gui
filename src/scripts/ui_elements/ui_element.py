from __future__ import annotations
import pygame
from warnings import warn
from abc import ABC, abstractmethod
from typing import Optional

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
        self._match_self_to_rect()

        if surface and surface.size != position_rect.size:
            warn(f'Surface size does not match rect size: id={element_id}')
        self.surface = surface if surface is not None else pygame.Surface(self.size)
            
        self.children = children

        self.id = element_id
        self.render_layer = render_layer

        self.ui_manager = ui_manager
        self.ui_manager.add_element(self)

    def _match_self_to_rect(self) -> None:
        # just sets all element's position/size values to the rect's
        self._topleft = self.position_rect.topleft

        self._center = self.position_rect.center
        self.center_x, self.center_y = self._center

        self.size = self.position_rect.size
        self.width, self.height = self.size
    
    @property
    def topleft(self) -> tuple:
        return self._topleft
    @topleft.setter
    def topleft(self, new_topleft: tuple) -> None:
        self._move_children(self._topleft[0] - new_topleft[0], self._topleft[1] - new_topleft[1])
        self.position_rect.topleft = new_topleft
        self._match_self_to_rect()
    
    @property
    def center(self) -> tuple:
        return self._center
    @center.setter
    def center(self, new_center: tuple) -> None:
        self._move_children(self.center[0] - new_center[0], self.center[1] - new_center[1])
        self.position_rect.center = new_center
        self._match_self_to_rect()

    def move(self, delta_x: int, delta_y: int) -> None:
        self.topleft = (self.topleft[0] + delta_x, self.topleft[1] + delta_y)
    
    def _move_children(self, delta_x: int, delta_y: int) -> None:
        for child in self.children:
            child.move(delta_x, delta_y)

    def relative_point(self, point: tuple) -> tuple:
        return (point[0] - self.topleft[0], point[1] - self.topleft[1])
    
    def anti_relative_point(self, point: tuple) -> tuple:
        return (point[0] + self.topleft[0], point[1] + self._topleft[1])

    @abstractmethod
    def update(self, delta_time: float) -> None:
        pass 

    def render(self, dest_surf: pygame.Surface) -> None:
        dest_surf.blit(self.surface, self._topleft)
        
