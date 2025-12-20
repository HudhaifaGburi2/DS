"""
Layout Utilities
================

Helper functions for positioning and layout calculations.
Uses golden ratio for harmonious proportions.
"""

from manim import *
import numpy as np
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import PHI, PHI_INV, L


def golden_position(
    base_pos,
    direction,
    magnitude: float = 1.0
) -> np.ndarray:
    """
    Calculate position using golden ratio.
    
    Args:
        base_pos: Starting position
        direction: Direction vector (e.g., RIGHT, UP)
        magnitude: Base magnitude to scale by φ
    
    Returns:
        New position array
    """
    return np.array(base_pos) + direction * magnitude * PHI


def golden_scale(base_scale: float = 1.0, power: int = 1) -> float:
    """
    Calculate scale using golden ratio powers.
    
    Args:
        base_scale: Base scale value
        power: Power of φ (can be negative)
    
    Returns:
        Scaled value
    """
    return base_scale * (PHI ** power)


def calculate_tree_positions(
    num_nodes_per_level: list,
    root_pos=ORIGIN + UP * 2,
    level_height: float = None,
    max_width: float = None
) -> list:
    """
    Calculate positions for tree nodes.
    
    Args:
        num_nodes_per_level: List of node counts per level
        root_pos: Position of root node
        level_height: Vertical spacing between levels
        max_width: Maximum horizontal spread
    
    Returns:
        List of lists containing positions for each level
    """
    level_height = level_height or L.TREE_LEVEL_HEIGHT
    max_width = max_width or L.TREE_MAX_WIDTH
    
    positions = []
    
    for level, num_nodes in enumerate(num_nodes_per_level):
        level_positions = []
        
        if num_nodes == 1:
            pos = np.array([
                root_pos[0],
                root_pos[1] - level * level_height,
                0
            ])
            level_positions.append(pos)
        else:
            # Distribute horizontally
            spacing = max_width / (num_nodes + 1)
            start_x = root_pos[0] - max_width / 2 + spacing
            
            for i in range(num_nodes):
                pos = np.array([
                    start_x + i * spacing,
                    root_pos[1] - level * level_height,
                    0
                ])
                level_positions.append(pos)
        
        positions.append(level_positions)
    
    return positions


def calculate_level_positions(
    num_items: int,
    center_pos=ORIGIN,
    horizontal_spacing: float = None,
    vertical: bool = False
) -> list:
    """
    Calculate evenly distributed positions at a level.
    
    Args:
        num_items: Number of items to position
        center_pos: Center of distribution
        horizontal_spacing: Spacing between items
        vertical: If True, distribute vertically
    
    Returns:
        List of positions
    """
    horizontal_spacing = horizontal_spacing or L.SPACING_LG
    
    positions = []
    total_width = (num_items - 1) * horizontal_spacing
    start = -total_width / 2
    
    direction = UP if vertical else RIGHT
    perpendicular = RIGHT if vertical else UP
    
    for i in range(num_items):
        offset = start + i * horizontal_spacing
        pos = np.array(center_pos) + direction * offset
        positions.append(pos)
    
    return positions


def distribute_horizontal(
    mobjects: list,
    center_pos=ORIGIN,
    spacing: float = None,
    aligned_edge=None
) -> list:
    """
    Distribute mobjects horizontally.
    
    Args:
        mobjects: List of mobjects to distribute
        center_pos: Center of distribution
        spacing: Spacing between mobjects
        aligned_edge: Edge to align (e.g., UP, DOWN)
    
    Returns:
        List of positions applied
    """
    spacing = spacing or L.SPACING_LG
    
    if not mobjects:
        return []
    
    # Calculate total width
    total_width = sum(m.width for m in mobjects) + spacing * (len(mobjects) - 1)
    start_x = center_pos[0] - total_width / 2
    
    positions = []
    current_x = start_x
    
    for mob in mobjects:
        current_x += mob.width / 2
        pos = np.array([current_x, center_pos[1], 0])
        mob.move_to(pos)
        
        if aligned_edge is not None:
            # Align to edge
            target_y = center_pos[1]
            if np.array_equal(aligned_edge, UP):
                mob.align_to(center_pos + UP * 0.5, UP)
            elif np.array_equal(aligned_edge, DOWN):
                mob.align_to(center_pos + DOWN * 0.5, DOWN)
        
        positions.append(mob.get_center())
        current_x += mob.width / 2 + spacing
    
    return positions


def distribute_vertical(
    mobjects: list,
    center_pos=ORIGIN,
    spacing: float = None,
    aligned_edge=None
) -> list:
    """
    Distribute mobjects vertically.
    
    Args:
        mobjects: List of mobjects to distribute
        center_pos: Center of distribution
        spacing: Spacing between mobjects
        aligned_edge: Edge to align (e.g., LEFT, RIGHT)
    
    Returns:
        List of positions applied
    """
    spacing = spacing or L.SPACING_LG
    
    if not mobjects:
        return []
    
    # Calculate total height
    total_height = sum(m.height for m in mobjects) + spacing * (len(mobjects) - 1)
    start_y = center_pos[1] + total_height / 2
    
    positions = []
    current_y = start_y
    
    for mob in mobjects:
        current_y -= mob.height / 2
        pos = np.array([center_pos[0], current_y, 0])
        mob.move_to(pos)
        
        if aligned_edge is not None:
            if np.array_equal(aligned_edge, LEFT):
                mob.align_to(center_pos + LEFT * 0.5, LEFT)
            elif np.array_equal(aligned_edge, RIGHT):
                mob.align_to(center_pos + RIGHT * 0.5, RIGHT)
        
        positions.append(mob.get_center())
        current_y -= mob.height / 2 + spacing
    
    return positions


def calculate_bezier_path(
    start_pos,
    end_pos,
    control_offset=None,
    num_points: int = 50
) -> list:
    """
    Calculate points along a bezier curve.
    
    Args:
        start_pos: Starting position
        end_pos: Ending position
        control_offset: Offset for control point
        num_points: Number of points to generate
    
    Returns:
        List of points along curve
    """
    if control_offset is None:
        # Default: curve upward
        mid = (np.array(start_pos) + np.array(end_pos)) / 2
        control_offset = UP * abs(start_pos[1] - end_pos[1]) * 0.3
    
    control = (np.array(start_pos) + np.array(end_pos)) / 2 + control_offset
    
    points = []
    for t in np.linspace(0, 1, num_points):
        # Quadratic bezier
        point = (1-t)**2 * np.array(start_pos) + \
                2*(1-t)*t * control + \
                t**2 * np.array(end_pos)
        points.append(point)
    
    return points


def calculate_arc_positions(
    center_pos,
    radius: float,
    start_angle: float,
    end_angle: float,
    num_items: int
) -> list:
    """
    Calculate positions along an arc.
    
    Args:
        center_pos: Center of arc
        radius: Radius of arc
        start_angle: Starting angle in radians
        end_angle: Ending angle in radians
        num_items: Number of positions to calculate
    
    Returns:
        List of positions
    """
    positions = []
    
    if num_items == 1:
        mid_angle = (start_angle + end_angle) / 2
        pos = np.array(center_pos) + radius * np.array([
            np.cos(mid_angle),
            np.sin(mid_angle),
            0
        ])
        positions.append(pos)
    else:
        angles = np.linspace(start_angle, end_angle, num_items)
        for angle in angles:
            pos = np.array(center_pos) + radius * np.array([
                np.cos(angle),
                np.sin(angle),
                0
            ])
            positions.append(pos)
    
    return positions


def calculate_grid_positions(
    rows: int,
    cols: int,
    center_pos=ORIGIN,
    cell_width: float = 1.0,
    cell_height: float = 1.0
) -> list:
    """
    Calculate positions for a grid layout.
    
    Args:
        rows: Number of rows
        cols: Number of columns
        center_pos: Center of grid
        cell_width: Width of each cell
        cell_height: Height of each cell
    
    Returns:
        2D list of positions [row][col]
    """
    total_width = cols * cell_width
    total_height = rows * cell_height
    
    start_x = center_pos[0] - total_width / 2 + cell_width / 2
    start_y = center_pos[1] + total_height / 2 - cell_height / 2
    
    positions = []
    for row in range(rows):
        row_positions = []
        for col in range(cols):
            pos = np.array([
                start_x + col * cell_width,
                start_y - row * cell_height,
                0
            ])
            row_positions.append(pos)
        positions.append(row_positions)
    
    return positions
