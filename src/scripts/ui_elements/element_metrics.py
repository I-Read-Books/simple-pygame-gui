from dataclasses import dataclass
from pygame import Rect
from typing import Optional

@dataclass
class ElementMetrics:
    rect: Rect
    
    holding: bool = False
    hovering: bool = False
    time_holding: float = 0
    time_hovering: float = 0
    just_pressed: bool = False
    just_released: bool = False

    prev_frame_mouse_col_pos: Optional[tuple] = None
    curr_frame_mouse_col_pos: Optional[tuple] = None