import pygame
from typing import NamedTuple

class UIManager:
    def __init__(self) -> None:
        from scripts.ui_elements.ui_element import UIElement
        from scripts.ui_elements.ui_interactive_element import UIInteractiveElement

        self.elements: dict[str, UIElement]= {}
        self._interactive_elements: list[UIInteractiveElement] = []
        self._render_order_elements: list[UIElement] = []
    
        self.render_layers = {}
        self.render_layers['default'] = []
        # higher index = rendered later
        self.render_layer_order = ['default']

        self.element_ids = []

        self.update(0)
    
    def update(self, delta_time: float) -> None:
        for element in self.elements.values():
            element.update(delta_time)
        self._render_order_elements = self.elements.values() #type: ignore
    
    def _update_element_subcategories(self) -> None:
        from scripts.ui_elements.ui_interactive_element import UIInteractiveElement
        self._interactive_elements = list(filter(lambda element: isinstance(element, UIInteractiveElement), self.elements.values())) # type: ignore

    def add_element(self, element) -> None:
        if element.id in self.element_ids:
            raise ValueError(f'Element id already in use: {element.id}')

        self.element_ids.append(element.id)
        self.elements[element.id] = element
        self.render_layers[element.render_layer if element.render_layer else 'default'].append(element.id)

        self._update_element_subcategories()
        
    def remove_element(self, element_id) -> None:
        self.elements.pop(element_id)
    
    def handle_mouse_event(self, mouse_pos: tuple, just_pressed: bool, just_released: bool) -> None:
        for element in self._interactive_elements:
            element.handle_mouse_event(mouse_pos, just_pressed, just_released)
        
    def render_all(self, dest_surf: pygame.Surface) -> None:
        for layer in self.render_layer_order:
            for element in self.render_layers[layer]:
                element.render(dest_surf)