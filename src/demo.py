import pygame
import sys
from scripts.ui_elements.ui_element import UIElement
from scripts.ui_elements.ui_interactive_element import UIInteractiveElement
from scripts.ui_elements.button import Button
from ui_manager import UIManager

class Demo:
    def __init__(self) -> None:
        self.width, self.height = (600, 600)
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.ui_manager = UIManager()
        self.element = UIElement(pygame.Rect(200, 200, 200, 200), self.ui_manager, 'box')
        self.element2 = UIElement(pygame.Rect(20, 20, 20, 20), self.ui_manager, 'ron', surface=pygame.Surface((20, 20), masks=(20, 20, 20)))
        self.element3 = UIInteractiveElement(pygame.Rect(300, 30, 50, 50), self.ui_manager, 'interactive')
        self.button = Button(pygame.Rect(100, 100, 30, 30), self.ui_manager, 'button', self.message, ['hello'])
    
    def run(self) -> None:
        while True:
            frame_time = self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                self.ui_manager.handle_mouse_event(mouse_pos, event.type==pygame.MOUSEBUTTONDOWN, event.type==pygame.MOUSEBUTTONUP)
                    
            self.screen.fill((255, 255, 255))
            
            self.ui_manager.update(frame_time / 1000) # seconds
            self.ui_manager.render_all(self.screen)

            pygame.display.flip()
    
    def message(self, message) -> None:
        print(message)

if __name__ == "__main__":
    Demo().run()