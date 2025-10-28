import pygame
import sys
from scripts.ui_elements.ui_element import UIElement
from scripts.ui_elements.button import Button
from ui_manager import UIManager

class Demo:
    def __init__(self) -> None:
        self.width, self.height = (600, 600)
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.ui_manager = UIManager()

        button_surfaces = [pygame.Surface((200, 200)) for _ in range(3)]
        button_surfaces[0].fill((200, 200, 200))
        button_surfaces[1].fill((100, 100, 100))
        button_surfaces[2].fill((0, 0, 0))

        self.button = Button(
            pygame.Rect(100, 100, 200, 200),
            self.ui_manager,
            lambda: self.message('hello'),
            'button1',
            button_surfaces[0],
            button_surfaces[1],
            button_surfaces[2],
        )

        self.button2 = Button(
            pygame.Rect(150, 150, 30, 30),
            self.ui_manager,
            lambda: self.message('i am button 2'),
            'button2',
            pygame.transform.smoothscale(button_surfaces[1], (30, 30))
        )
        self.button.add_child(self.button2)
    
    def run(self) -> None:
        while True:
            frame_time = self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            mouse_just_pressed = False
            mouse_just_released = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN: 
                        self.button.move(0, 10)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_just_pressed = True
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_just_released = True

            self.screen.fill((255, 255, 255))

            self.ui_manager.update(mouse_pos, mouse_just_pressed, mouse_just_released, frame_time / 1000) # seconds
            self.ui_manager.render_all(self.screen)

            mouse_just_released = mouse_just_pressed = False
            pygame.display.flip()
    
    def message(self, message) -> None:
        print(message)

if __name__ == "__main__":
    Demo().run()