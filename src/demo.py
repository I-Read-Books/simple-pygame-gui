import pygame
import sys
from scripts.ui_elements.ui_element import UIElement
from scripts.ui_elements.element_functions import ButtonFunction
from ui_manager import UIManager

class Demo:
    def __init__(self) -> None:
        self.width, self.height = (600, 600)
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.ui_manager = UIManager()
        self.element = UIElement(pygame.Rect(200, 200, 200, 200), self.ui_manager, 'box')
        self.element.add_functionality(ButtonFunction(self.message, ['hello']))

        self.element2 = UIElement(pygame.Rect(20, 20, 20, 20), self.ui_manager, 'ron', surface=pygame.Surface((20, 20), masks=(20, 20, 20)))
    
    def run(self) -> None:
        while True:
            frame_time = self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            mouse_just_pressed = False
            mouse_just_released = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                mouse_just_pressed = event.type == pygame.MOUSEBUTTONDOWN
                mouse_just_released = event.type == pygame.MOUSEBUTTONUP

            self.screen.fill((255, 255, 255))
            
            self.ui_manager.update(mouse_pos, mouse_just_pressed, mouse_just_released, frame_time / 1000) # seconds
            self.ui_manager.render_all(self.screen)

            pygame.display.flip()
    
    def message(self, message) -> None:
        print(message)

if __name__ == "__main__":
    Demo().run()