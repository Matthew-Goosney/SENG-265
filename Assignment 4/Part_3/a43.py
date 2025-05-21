#!/usr/bin/env python
"""Assignment 4 Part 3 Random Art Generator"""
# Name: Matthew Goosney
# V-Number: V01040408
# Date: April 2nd-7th, 2025

print(__doc__)

import random
from typing import IO, List, Tuple, Optional
from collections import namedtuple

# Define named tuples for coordinates, dimensions, and colors
CircleData = namedtuple('CircleData', ['cx', 'cy', 'rad'])
ColorData = namedtuple('ColorData', ['red', 'green', 'blue', 'opacity'])
CanvasSize = namedtuple('CanvasSize', ['width', 'height'])
ColorRange = namedtuple('ColorRange', ['min_r', 'max_r', 'min_g', 'max_g', 'min_b', 'max_b', 'min_op', 'max_op'])

class HtmlComponent:
    """HtmlComponent class"""
    def __init__(self, indent_level: int = 0) -> None:
        self.indent_level = indent_level
    
    def get_indent(self) -> str:
        """get_indent method"""
        return "   " * self.indent_level
    
    def render(self, file: IO[str]) -> None:
        """render method"""
        pass

class CircleShape(HtmlComponent):
    """CircleShape class"""
    def __init__(self, circle_data: CircleData, color_data: ColorData, indent_level: int = 0) -> None:
        super().__init__(indent_level)
        self.circle_data = circle_data
        self.color_data = color_data
    
    def render(self, file: IO[str]) -> None:
        """render method"""
        indent = self.get_indent()
        line1 = f'<circle cx="{self.circle_data.cx}" cy="{self.circle_data.cy}" r="{self.circle_data.rad}" '
        line2 = f'fill="rgb({self.color_data.red}, {self.color_data.green}, {self.color_data.blue})" fill-opacity="{self.color_data.opacity}"></circle>'
        file.write(f"{indent}{line1+line2}\n")

class RectangleShape(HtmlComponent):
    """RectangleShape class"""
    def __init__(self, x: int, y: int, width: int, height: int, color_data: ColorData, indent_level: int = 0) -> None:
        super().__init__(indent_level)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color_data = color_data
    
    def render(self, file: IO[str]) -> None:
        """render method"""
        indent = self.get_indent()
        line1 = f'<rect x="{self.x}" y="{self.y}" width="{self.width}" height="{self.height}" '
        line2 = f'fill="rgb({self.color_data.red}, {self.color_data.green}, {self.color_data.blue})" fill-opacity="{self.color_data.opacity}"></rect>'
        file.write(f"{indent}{line1+line2}\n")

class EllipseShape(HtmlComponent):
    """EllipseShape class"""
    def __init__(self, cx: int, cy: int, rx: int, ry: int, color_data: ColorData, indent_level: int = 0) -> None:
        super().__init__(indent_level)
        self.cx = cx
        self.cy = cy
        self.rx = rx
        self.ry = ry
        self.color_data = color_data
    
    def render(self, file: IO[str]) -> None:
        """render method"""
        indent = self.get_indent()
        line1 = f'<ellipse cx="{self.cx}" cy="{self.cy}" rx="{self.rx}" ry="{self.ry}" '
        line2 = f'fill="rgb({self.color_data.red}, {self.color_data.green}, {self.color_data.blue})" fill-opacity="{self.color_data.opacity}"></ellipse>'
        file.write(f"{indent}{line1+line2}\n")

class PyArtConfig:
    """PyArtConfig class"""

    MIN_X = 0
    MAX_X = 600
    MIN_Y = 0
    MAX_Y = 400
    MIN_RADIUS = 5
    MAX_RADIUS = 50
    MIN_RX = 10
    MAX_RX = 30
    MIN_RY = 10
    MAX_RY = 30
    MIN_WIDTH = 10
    MAX_WIDTH = 50
    MIN_HEIGHT = 10
    MAX_HEIGHT = 50
    MIN_RGB = 0
    MAX_RGB = 255
    MIN_OPACITY = 0.1
    MAX_OPACITY = 1.0
    
    def __init__(self, 
                 canvas_size: CanvasSize = CanvasSize(600, 400),
                 shape_count: int = 100,
                 x_range: Tuple[int, int] = None,
                 y_range: Tuple[int, int] = None,
                 radius_range: Tuple[int, int] = None,
                 rx_range: Tuple[int, int] = None,
                 ry_range: Tuple[int, int] = None,
                 width_range: Tuple[int, int] = None,
                 height_range: Tuple[int, int] = None,
                 color_range: ColorRange = None,
                 shape_types: List[int] = None,
                 theme_name: str = "Default") -> None:
        """__init__ method"""
        self.canvas_size = canvas_size
        self.shape_count = shape_count
        self.theme_name = theme_name
        self.x_range = x_range if x_range else (self.MIN_X, self.MAX_X)
        self.y_range = y_range if y_range else (self.MIN_Y, self.MAX_Y)
        self.radius_range = radius_range if radius_range else (self.MIN_RADIUS, self.MAX_RADIUS)
        self.rx_range = rx_range if rx_range else (self.MIN_RX, self.MAX_RX)
        self.ry_range = ry_range if ry_range else (self.MIN_RY, self.MAX_RY)
        self.width_range = width_range if width_range else (self.MIN_WIDTH, self.MAX_WIDTH)
        self.height_range = height_range if height_range else (self.MIN_HEIGHT, self.MAX_HEIGHT)
        
        if color_range is None:
            self.color_range = ColorRange(
                self.MIN_RGB, self.MAX_RGB,  # Red
                self.MIN_RGB, self.MAX_RGB,  # Green
                self.MIN_RGB, self.MAX_RGB,  # Blue
                self.MIN_OPACITY, self.MAX_OPACITY  # Opacity
            )
        else:
            self.color_range = color_range
        
        # Default to all shape types
        if shape_types is None:
            self.shape_types = [0, 1, 2]  # Circle, Rectangle, Ellipse
        else:
            self.shape_types = shape_types

class RandomShape(HtmlComponent):
    """RandomShape class"""

    CIRCLE = 0
    RECTANGLE = 1
    ELLIPSE = 2
    
    def __init__(self, config: PyArtConfig, indent_level: int = 0, shape_type: Optional[int] = None) -> None:
        """__init__ method"""
        super().__init__(indent_level)
        self.config = config
        self.shape_type = shape_type if shape_type is not None else random.choice(config.shape_types)
        self.count_id = 0 
        
        # Generate random properties for the shape
        self.x = random.randint(config.x_range[0], config.x_range[1])
        self.y = random.randint(config.y_range[0], config.y_range[1])
        self.radius = random.randint(config.radius_range[0], config.radius_range[1])
        self.rx = random.randint(config.rx_range[0], config.rx_range[1])
        self.ry = random.randint(config.ry_range[0], config.ry_range[1])
        self.width = random.randint(config.width_range[0], config.width_range[1])
        self.height = random.randint(config.height_range[0], config.height_range[1])
        self.red = random.randint(config.color_range.min_r, config.color_range.max_r)
        self.green = random.randint(config.color_range.min_g, config.color_range.max_g)
        self.blue = random.randint(config.color_range.min_b, config.color_range.max_b)
        self.opacity = round(random.uniform(config.color_range.min_op, config.color_range.max_op), 1)
    
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
    
    def as_Part2_line(self) -> str:
        """as_Part2_line method"""

        return f"{self.count_id:>3} {self.shape_type:>3} {self.x:>3} {self.y:>3} {self.radius:>3} {self.rx:>3} {self.ry:>3} {self.width:>3} {self.height:>3} {self.red:>3} {self.green:>3} {self.blue:>3} {self.opacity:>3.1f}"
    
    def render(self, file: IO[str]) -> None:
        """render method"""
        indent = self.get_indent()
        svg_code = self.as_svg()
        file.write(f"{indent}{svg_code}\n")
    
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
        return ""  

class SvgCanvas(HtmlComponent):
    """SvgCanvas class"""
    def __init__(self, canvas_size: CanvasSize, indent_level: int = 0) -> None:
        """__init__ method"""

        super().__init__(indent_level)
        self.canvas_size = canvas_size
        self.shapes = []
    
    def add_shape(self, shape: HtmlComponent) -> None:
        """add_shape method"""

        shape.indent_level = self.indent_level + 1
        self.shapes.append(shape)
    
    def write_comment(self, file: IO[str], comment: str) -> None:
        """write_comment method"""

        indent = self.get_indent()
        file.write(f"{indent}<!--{comment}-->\n")
    
    def render(self, file: IO[str]) -> None:
        """render method"""
        indent = self.get_indent()
        
        self.write_comment(file, "Define SVG drawing box")
        file.write(f'{indent}<svg width="{self.canvas_size.width}" height="{self.canvas_size.height}">\n')
        
        for shape in self.shapes:
            shape.render(file)
        
        file.write(f"{indent}</svg>\n")
    
    def random_art(self, config: PyArtConfig) -> None:
        """random_art method"""
        for i in range(config.shape_count):
            shape = RandomShape(config)
            shape.count_id = i
            self.add_shape(shape)
    
    def gen_art(self) -> None:
        """gen_art method"""

        for i in range(5):
            x_pos = 50 + i * 100
            circle_data = CircleData(x_pos, 50, 50)
            color_data = ColorData(255, 0, 0, 1.0)
            self.add_shape(CircleShape(circle_data, color_data))
        
        for i in range(5):
            x_pos = 50 + i * 100
            circle_data = CircleData(x_pos, 250, 50)
            color_data = ColorData(0, 0, 255, 1.0)
            self.add_shape(CircleShape(circle_data, color_data))

class HtmlDocument:
    """HtmlDocument class"""

    def __init__(self, title: str) -> None:

        """__init__ method"""

        self.title = title
        self.components = []
    
    def add_component(self, component: HtmlComponent, indent_level: int = 0) -> None:
        """add_component method"""

        component.indent_level = indent_level
        self.components.append(component)
    
    def write_line(self, file: IO[str], indent_level: int, line: str) -> None:
        """write_line method"""

        indent = "   " * indent_level
        file.write(f"{indent}{line}\n")
    
    def render(self, filename: str) -> None:
        """render method"""

        with open(filename, "w") as file:

            self.write_line(file, 0, "<html>")
            self.write_line(file, 0, "<head>")
            self.write_line(file, 1, f"<title>{self.title}</title>")
            self.write_line(file, 0, "</head>")
            self.write_line(file, 0, "<body>")
            
            for component in self.components:
                component.render(file)
            
            self.write_line(file, 0, "</body>")
            self.write_line(file, 0, "</html>")

def nature_theme() -> PyArtConfig:
    """nature_theme method - Creates a green/earth-tone theme"""

    color_range = ColorRange(
        50, 150,    # Red
        100, 255,   # Green
        20, 100,    # Blue
        0.3, 0.8    # Opacity
    )
    
    return PyArtConfig(
        canvas_size=CanvasSize(600, 400),
        shape_count=200,
        radius_range=(5, 40),
        color_range=color_range,
        theme_name="Nature"
    )

def ocean_theme() -> PyArtConfig:

    """ocean_theme method - Creates a blue ocean theme"""

    color_range = ColorRange(
        0, 100,     # Red
        50, 200,    # Green
        150, 255,   # Blue
        0.2, 0.9    # Opacity
    )
    
    return PyArtConfig(
        canvas_size=CanvasSize(600, 400),
        shape_count=150,
        radius_range=(3, 30),
        color_range=color_range,
        theme_name="Ocean"
    )

def sunset_theme() -> PyArtConfig:
    """sunset_theme method - Creates a warm sunset theme"""
    color_range = ColorRange(
        180, 255,   # Red
        20, 180,    # Green
        0, 100,     # Blue
        0.4, 1.0    # Opacity
    )
    
    return PyArtConfig(
        canvas_size=CanvasSize(600, 400),
        shape_count=120,
        radius_range=(10, 60),
        color_range=color_range,
        theme_name="Sunset"
    )

def generate_art_file(config: PyArtConfig, filename: str) -> None:
    """generate_art_file method"""

    doc = HtmlDocument(f"Random Art - {config.theme_name}")
    canvas = SvgCanvas(config.canvas_size, indent_level=1)
    canvas.random_art(config)
    doc.add_component(canvas)
    doc.render(filename)

def main() -> None:
    """main method"""

    nature_config = nature_theme()
    ocean_config = ocean_theme()
    sunset_config = sunset_theme()
    
    generate_art_file(nature_config, "a431.html")
    generate_art_file(ocean_config, "a432.html")
    generate_art_file(sunset_config, "a433.html")

if __name__ == "__main__":
    main()