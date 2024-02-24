from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

    
@dataclass
class Line:
    point1: Point
    point2: Point
    color: tuple
    thickness: int