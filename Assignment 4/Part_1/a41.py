#!/usr/bin/env python
"""Assignment 4 Part 1"""
print(__doc__)

from typing import IO, Tuple
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
                 shape_types: list = None,
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
        
        if shape_types is None:
            self.shape_types = [0, 1, 2]  # Circle, Rectangle, Ellipse
        else:
            self.shape_types = shape_types

class SvgCanvas(HtmlComponent):
    """SvgCanvas class"""
    def __init__(self, canvas_size: CanvasSize, indent_level: int = 0) -> None:
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
        # Red row of circles
        for i in range(5):
            x_pos = 50 + i * 100
            circle_data = CircleData(x_pos, 50, 50)
            color_data = ColorData(255, 0, 0, 1.0)
            self.add_shape(CircleShape(circle_data, color_data))
        
        # Blue row of circles
        for i in range(5):
            x_pos = 50 + i * 100
            circle_data = CircleData(x_pos, 250, 50)
            color_data = ColorData(0, 0, 255, 1.0)
            self.add_shape(CircleShape(circle_data, color_data))
    
    def gen_art(self) -> None:
        """gen_art method"""
        # Call the renamed method with a default config
        default_config = PyArtConfig()
        self.random_art(default_config)

class HtmlDocument:
    """HtmlDocument class"""
    def __init__(self, title: str) -> None:
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
            # Write HTML header
            self.write_line(file, 0, "<html>")
            self.write_line(file, 0, "<head>")
            self.write_line(file, 1, f"<title>{self.title}</title>")
            self.write_line(file, 0, "</head>")
            self.write_line(file, 0, "<body>")
            
            # Render all components
            for component in self.components:
                component.render(file)
            
            # Write HTML footer
            self.write_line(file, 0, "</body>")
            self.write_line(file, 0, "</html>")

def generate_art_file(config: PyArtConfig, filename: str) -> None:
    """generate_art_file method"""
    doc = HtmlDocument(f"Random Art - {config.theme_name}")
    canvas = SvgCanvas(config.canvas_size, indent_level=1)
    canvas.random_art(config)
    doc.add_component(canvas)
    doc.render(filename)

def writeHTMLfile() -> None:
    """writeHTMLfile method"""

    doc = HtmlDocument("Seng 265 Art! :D")
    
    canvas = SvgCanvas(CanvasSize(500, 300), indent_level=1)
    canvas.gen_art()
    
    doc.add_component(canvas)
    doc.render("a41.html")

def main() -> None:
    """main method"""
    writeHTMLfile()
    
    default_config = PyArtConfig(theme_name="Default Example")
    generate_art_file(default_config, "a41.html")

if __name__ == "__main__":
    main()