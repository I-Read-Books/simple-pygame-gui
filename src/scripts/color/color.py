from __future__ import annotations
import pygame
from typing import overload


class Color:
    def __init__(self, r: int, g: int, b: int, a: int=255) -> None:
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a
    
    @property
    def a(self) -> int:
        return self.alpha
    @property
    def r(self) -> int:
        return self.red
    @property
    def g(self) -> int:
        return self.green
    @property
    def b(self) -> int:
        return self.blue
    @property
    def rgba(self) -> tuple:
        return (self.red, self.green, self.blue, self.alpha)

    def __repr__(self) -> str:
        return f'Color({self.r}, {self.g}, {self.b})'
        
john = Color(255, 255, 255, 255)