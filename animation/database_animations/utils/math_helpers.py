"""
Database Animation Framework - Math Helpers
============================================

Mathematical utilities for positioning and scaling.
"""

from manim import *
import numpy as np
import sys
sys.path.append('..')
from config import config, C, T, F, L, A, D


# Golden ratio constant
PHI = config.PHI


def golden_position(
    center: np.ndarray = ORIGIN,
    direction: np.ndarray = RIGHT,
    level: int = 1
) -> np.ndarray:
    """
    Calculate position based on golden ratio from center.
    
    Args:
        center: Reference point
        direction: Direction to offset
        level: Multiplier level (1=φ, 2=φ², etc.)
    
    Returns:
        Position vector
    """
    distance = PHI ** level
    return center + direction * distance


def golden_scale(base_size: float = 1.0, level: int = 0) -> float:
    """
    Calculate size based on golden ratio.
    
    Args:
        base_size: Reference size
        level: Scale level (negative=smaller, positive=larger)
    
    Returns:
        Scaled size
    """
    return base_size * (PHI ** level)


def fibonacci_scale(index: int, base_size: float = 1.0) -> float:
    """
    Get scale factor from Fibonacci sequence.
    
    Args:
        index: Fibonacci index (0-indexed)
        base_size: Reference size
    
    Returns:
        Size based on Fibonacci number
    """
    fib = config.FIBONACCI
    if 0 <= index < len(fib):
        return base_size * fib[index] / fib[3]  # Normalized to fib[3]=3
    return base_size


def calculate_grid_positions(
    rows: int,
    cols: int,
    width: float = 10.0,
    height: float = 6.0,
    center: np.ndarray = ORIGIN
) -> list:
    """
    Calculate evenly spaced grid positions.
    
    Args:
        rows: Number of rows
        cols: Number of columns
        width: Total grid width
        height: Total grid height
        center: Grid center point
    
    Returns:
        2D list of positions [row][col]
    """
    positions = []
    
    # Calculate spacing
    col_spacing = width / (cols + 1)
    row_spacing = height / (rows + 1)
    
    # Starting point (top-left)
    start_x = center[0] - width / 2 + col_spacing
    start_y = center[1] + height / 2 - row_spacing
    
    for r in range(rows):
        row_positions = []
        for c in range(cols):
            x = start_x + c * col_spacing
            y = start_y - r * row_spacing
            row_positions.append(np.array([x, y, 0]))
        positions.append(row_positions)
    
    return positions


def calculate_horizontal_positions(
    count: int,
    total_width: float = 8.0,
    center: np.ndarray = ORIGIN
) -> list:
    """
    Calculate evenly spaced horizontal positions.
    
    Args:
        count: Number of items
        total_width: Total span width
        center: Center point
    
    Returns:
        List of positions
    """
    if count == 1:
        return [center.copy()]
    
    spacing = total_width / (count - 1)
    start_x = center[0] - total_width / 2
    
    return [
        np.array([start_x + i * spacing, center[1], 0])
        for i in range(count)
    ]


def calculate_vertical_positions(
    count: int,
    total_height: float = 5.0,
    center: np.ndarray = ORIGIN
) -> list:
    """
    Calculate evenly spaced vertical positions.
    
    Args:
        count: Number of items
        total_height: Total span height
        center: Center point
    
    Returns:
        List of positions
    """
    if count == 1:
        return [center.copy()]
    
    spacing = total_height / (count - 1)
    start_y = center[1] + total_height / 2
    
    return [
        np.array([center[0], start_y - i * spacing, 0])
        for i in range(count)
    ]


def interpolate_color(
    color1: str,
    color2: str,
    t: float
) -> str:
    """
    Interpolate between two colors.
    
    Args:
        color1: Starting color (hex)
        color2: Ending color (hex)
        t: Interpolation factor (0-1)
    
    Returns:
        Interpolated color (hex)
    """
    from colour import Color
    
    c1 = Color(color1)
    c2 = Color(color2)
    
    # Interpolate RGB
    r = c1.red + (c2.red - c1.red) * t
    g = c1.green + (c2.green - c1.green) * t
    b = c1.blue + (c2.blue - c1.blue) * t
    
    result = Color(rgb=(r, g, b))
    return result.hex_l


def calculate_arc_path(
    start: np.ndarray,
    end: np.ndarray,
    arc_height: float = 1.0
) -> np.ndarray:
    """
    Calculate control points for an arc path.
    
    Args:
        start: Starting position
        end: Ending position
        arc_height: Height of arc above line
    
    Returns:
        Array of control points [start, control1, control2, end]
    """
    mid = (start + end) / 2
    mid += UP * arc_height
    
    # Calculate control points for cubic bezier
    control1 = start + (mid - start) * 0.5 + UP * arc_height * 0.5
    control2 = end + (mid - end) * 0.5 + UP * arc_height * 0.5
    
    return np.array([start, control1, control2, end])


def ease_value(
    t: float,
    ease_type: str = "in_out"
) -> float:
    """
    Apply easing function to a value.
    
    Args:
        t: Input value (0-1)
        ease_type: Type of easing (in, out, in_out)
    
    Returns:
        Eased value
    """
    if ease_type == "in":
        return t * t * t
    elif ease_type == "out":
        return 1 - (1 - t) ** 3
    elif ease_type == "in_out":
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - (-2 * t + 2) ** 3 / 2
    return t


def distribute_around_circle(
    count: int,
    radius: float = 2.0,
    center: np.ndarray = ORIGIN,
    start_angle: float = 0
) -> list:
    """
    Distribute positions evenly around a circle.
    
    Args:
        count: Number of positions
        radius: Circle radius
        center: Circle center
        start_angle: Starting angle in radians
    
    Returns:
        List of positions
    """
    positions = []
    angle_step = TAU / count
    
    for i in range(count):
        angle = start_angle + i * angle_step
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        positions.append(np.array([x, y, 0]))
    
    return positions


def calculate_bezier_point(
    t: float,
    p0: np.ndarray,
    p1: np.ndarray,
    p2: np.ndarray,
    p3: np.ndarray
) -> np.ndarray:
    """
    Calculate point on cubic bezier curve.
    
    Args:
        t: Parameter (0-1)
        p0-p3: Control points
    
    Returns:
        Point on curve
    """
    t2 = t * t
    t3 = t2 * t
    mt = 1 - t
    mt2 = mt * mt
    mt3 = mt2 * mt
    
    return mt3 * p0 + 3 * mt2 * t * p1 + 3 * mt * t2 * p2 + t3 * p3
