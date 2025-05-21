#!/usr/bin/env python
"""Assignment 4 Part 2"""
print(__doc__)

import random
from typing import IO, List, Tuple

class PyArtConfig:
    """PyArtConfig class"""
    # Class variables for ranges
    MIN_X = 0
    MAX_X = 500
    MIN_Y = 0
    MAX_Y = 300
    MIN_RADIUS = 10
    MAX_RADIUS = 100
    MIN_RX = 10
    MAX_RX = 30
    MIN_RY = 10
    MAX_RY = 30
    MIN_WIDTH = 10
    MAX_WIDTH = 100
    MIN_HEIGHT = 10
    MAX_HEIGHT = 100
    MIN_RGB = 0
    MAX_RGB = 255
    MIN_OPACITY = 0.1
    MAX_OPACITY = 1.0
    
    def __init__(self, 
                 x_range: Tuple[int, int] = None,
                 y_range: Tuple[int, int] = None,
                 radius_range: Tuple[int, int] = None,
                 rx_range: Tuple[int, int] = None,
                 ry_range: Tuple[int, int] = None,
                 width_range: Tuple[int, int] = None,
                 height_range: Tuple[int, int] = None,
                 red_range: Tuple[int, int] = None,
                 green_range: Tuple[int, int] = None,
                 blue_range: Tuple[int, int] = None,
                 opacity_range: Tuple[float, float] = None) -> None:
        """__init__ method"""
        # Use default class values if parameters are not provided
        self.x_range = x_range if x_range else (self.MIN_X, self.MAX_X)
        self.y_range = y_range if y_range else (self.MIN_Y, self.MAX_Y)
        self.radius_range = radius_range if radius_range else (self.MIN_RADIUS, self.MAX_RADIUS)
        self.rx_range = rx_range if rx_range else (self.MIN_RX, self.MAX_RX)
        self.ry_range = ry_range if ry_range else (self.MIN_RY, self.MAX_RY)
        self.width_range = width_range if width_range else (self.MIN_WIDTH, self.MAX_WIDTH)
        self.height_range = height_range if height_range else (self.MIN_HEIGHT, self.MAX_HEIGHT)
        self.red_range = red_range if red_range else (self.MIN_RGB, self.MAX_RGB)
        self.green_range = green_range if green_range else (self.MIN_RGB, self.MAX_RGB)
        self.blue_range = blue_range if blue_range else (self.MIN_RGB, self.MAX_RGB)
        self.opacity_range = opacity_range if opacity_range else (self.MIN_OPACITY, self.MAX_OPACITY)

class RandomShape:
    """RandomShape class"""
    # Shape type constants
    CIRCLE = 0
    RECTANGLE = 1
    ELLIPSE = 2
    
    def __init__(self, config: PyArtConfig, shape_type: int = None) -> None:
        """__init__ method"""
        self.config = config
        self.shape_type = shape_type if shape_type is not None else random.randint(0, 2)
        self.count_id = 0 
        
        # Random shape properties
        self.x = random.randint(config.x_range[0], config.x_range[1])
        self.y = random.randint(config.y_range[0], config.y_range[1])
        self.radius = random.randint(config.radius_range[0], config.radius_range[1])
        self.rx = random.randint(config.rx_range[0], config.rx_range[1])
        self.ry = random.randint(config.ry_range[0], config.ry_range[1])
        self.width = random.randint(config.width_range[0], config.width_range[1])
        self.height = random.randint(config.height_range[0], config.height_range[1])
        self.red = random.randint(config.red_range[0], config.red_range[1])
        self.green = random.randint(config.green_range[0], config.green_range[1])
        self.blue = random.randint(config.blue_range[0], config.blue_range[1])
        self.opacity = round(random.uniform(config.opacity_range[0], config.opacity_range[1]), 1)
    
    def __str__(self) -> str:
        """__str__ method"""
        shape_names = {0: "Circle", 1: "Rectangle", 2: "Ellipse"}
        shape_name = shape_names.get(self.shape_type, "Unknown")
        
        result = f"Shape #{self.count_id}: {shape_name}\n"
        result += f"  Position: ({self.x}, {self.y})\n"
        
        if self.shape_type == self.CIRCLE:
            result += f"  Radius: {self.radius}\n"
        elif self.shape_type == self.RECTANGLE:
            result += f"  Size: {self.width} x {self.height}\n"
        elif self.shape_type == self.ELLIPSE:
            result += f"  Radii: {self.rx} x {self.ry}\n"
            
        result += f"  Color: RGB({self.red}, {self.green}, {self.blue}), Opacity: {self.opacity}\n"
        return result
    
    def as_Part2_line (self) -> str:
        """as_Part2_line method"""
        return f"{self.count_id:>3} {self.shape_type:>3} {self.x:>3} {self.y:>3} {self.radius:>3} {self.rx:>3} {self.ry:>3} {self.width:>3} {self.height:>3} {self.red:>3} {self.green:>3} {self.blue:>3} {self.opacity:>3.1f}"
    
    def as_svg(self) -> str:
        """as_svg method"""
        if self.shape_type == self.CIRCLE:
            return f'<circle cx="{self.x}" cy="{self.y}" r="{self.radius}" ' \
                   f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.opacity}"></circle>'
        elif self.shape_type == self.RECTANGLE:
            return f'<rect x="{self.x}" y="{self.y}" width="{self.width}" height="{self.height}" ' \
                   f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.opacity}"></rect>'
        elif self.shape_type == self.ELLIPSE:
            return f'<ellipse cx="{self.x}" cy="{self.y}" rx="{self.rx}" ry="{self.ry}" ' \
                   f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.opacity}"></ellipse>'
        return ""  # Empty string for unknown shape types

def generate_shapes(config: PyArtConfig, count: int) -> List[RandomShape]:
    """generate_shapes method"""
    shapes = []
    for i in range(count):
        shape = RandomShape(config)
        shape.count_id = i
        shapes.append(shape)
    return shapes

def print_table_header() -> None:
    """print_table_header method"""
    print(f"{'CNT':>3} {'SHA':>3} {'X':>3} {'Y':>3} {'RAD':>3} {'RX':>3} {'RY':>3} {'W':>3} {'H':>3} {'R':>3} {'G':>3} {'B':>3} {'OP':>3}")

def main() -> None:
    """main method"""
    config = PyArtConfig()
    
    shapes = generate_shapes(config, 10)

    print_table_header()
    
    for shape in shapes:
        print(shape.as_Part2_line())

if __name__ == "__main__":
    main()