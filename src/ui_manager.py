import pygame

class UIManager:
    def __init__(self) -> None:
        from scripts.ui_elements.ui_element import UIElement

        self.elements: dict[str, UIElement]= {}
        self._render_order_elements: list[UIElement] = []
    
        self.render_layers = {}
        self.render_layers['default'] = []
        # higher index = rendered later
        self.render_layer_order = ['default']

        self.element_ids = []

    def update(self, mouse_pos: tuple, just_pressed: bool, just_released: bool, delta_time: float) -> None:
        for element in self.elements.values():
            element.update(mouse_pos, just_pressed, just_released, delta_time)
        self._render_order_elements = self.elements.values() #type: ignore
    
    def add_element(self, element) -> None:
        if element.id in self.element_ids:
            raise ValueError(f'Element id already in use: {element.id}')

        self.element_ids.append(element.id)
        self.elements[element.id] = element
        self.render_layers[element.render_layer if element.render_layer else 'default'].append(element.id)
        
    def remove_element(self, element_id) -> None:
        self.elements.pop(element_id)
        
    def render_all(self, dest_surf: pygame.Surface) -> None:
        for layer in self.render_layer_order:
            for element_id in self.render_layers[layer]:
                self.elements[element_id].render(dest_surf)