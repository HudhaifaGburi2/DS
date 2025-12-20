"""
Layout Utilities for OS Concepts
================================

Helper functions for positioning threads, locks, and timelines.
"""

from manim import *
import numpy as np
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import C, T, F, L, A, OS


def calculate_thread_lanes(
    num_threads: int,
    start_y: float = 2.0,
    lane_height: float = None,
    lane_spacing: float = None
) -> list:
    """
    Calculate Y positions for thread lanes.
    
    Returns list of (y_position, thread_color) tuples.
    """
    lane_height = lane_height or L.THREAD_LANE_HEIGHT
    lane_spacing = lane_spacing or L.THREAD_LANE_SPACING
    
    lanes = []
    for i in range(num_threads):
        y = start_y - i * (lane_height + lane_spacing)
        color = C.THREAD_COLORS[i % len(C.THREAD_COLORS)]
        lanes.append((y, color))
    
    return lanes


def calculate_lock_positions(
    num_locks: int,
    center_y: float = 0,
    spacing: float = None
) -> list:
    """
    Calculate positions for multiple locks.
    """
    spacing = spacing or L.LOCK_SPACING
    
    positions = []
    total_width = (num_locks - 1) * spacing
    start_x = -total_width / 2
    
    for i in range(num_locks):
        x = start_x + i * spacing
        positions.append(np.array([x, center_y, 0]))
    
    return positions


def calculate_timeline_positions(
    num_objects: int,
    start_y: float = 1.5,
    spacing: float = None
) -> list:
    """
    Calculate Y positions for version timelines.
    """
    spacing = spacing or L.VERSION_SPACING
    
    positions = []
    for i in range(num_objects):
        y = start_y - i * spacing
        positions.append(y)
    
    return positions


def distribute_horizontal(
    mobjects: list,
    center_pos=ORIGIN,
    spacing: float = None
) -> list:
    """
    Distribute mobjects horizontally.
    """
    spacing = spacing or L.SPACING_LG
    
    if not mobjects:
        return []
    
    total_width = sum(m.width for m in mobjects) + spacing * (len(mobjects) - 1)
    start_x = center_pos[0] - total_width / 2
    
    positions = []
    current_x = start_x
    
    for mob in mobjects:
        current_x += mob.width / 2
        pos = np.array([current_x, center_pos[1], 0])
        mob.move_to(pos)
        positions.append(pos)
        current_x += mob.width / 2 + spacing
    
    return positions


def distribute_vertical(
    mobjects: list,
    center_pos=ORIGIN,
    spacing: float = None
) -> list:
    """
    Distribute mobjects vertically.
    """
    spacing = spacing or L.SPACING_LG
    
    if not mobjects:
        return []
    
    total_height = sum(m.height for m in mobjects) + spacing * (len(mobjects) - 1)
    start_y = center_pos[1] + total_height / 2
    
    positions = []
    current_y = start_y
    
    for mob in mobjects:
        current_y -= mob.height / 2
        pos = np.array([center_pos[0], current_y, 0])
        mob.move_to(pos)
        positions.append(pos)
        current_y -= mob.height / 2 + spacing
    
    return positions


def create_execution_path(
    start_pos,
    end_pos,
    num_steps: int = 5,
    style: str = "linear"  # "linear", "stepped", "curved"
) -> list:
    """
    Create path points for thread execution visualization.
    """
    if style == "linear":
        return [
            start_pos + (end_pos - start_pos) * t
            for t in np.linspace(0, 1, num_steps)
        ]
    
    elif style == "stepped":
        points = []
        for i in range(num_steps):
            t = i / (num_steps - 1)
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
            y = start_pos[1] if i % 2 == 0 else start_pos[1] + 0.2
            points.append(np.array([x, y, 0]))
        return points
    
    elif style == "curved":
        # Bezier curve
        control = (start_pos + end_pos) / 2 + UP * 0.5
        points = []
        for t in np.linspace(0, 1, num_steps):
            p = (1-t)**2 * start_pos + 2*(1-t)*t * control + t**2 * end_pos
            points.append(p)
        return points
    
    return [start_pos, end_pos]


def calculate_wait_queue_position(
    lock_pos,
    queue_index: int,
    direction: str = "left"
) -> np.ndarray:
    """
    Calculate position in wait queue.
    """
    offset = 0.6 + queue_index * 0.7
    
    if direction == "left":
        return lock_pos + LEFT * offset
    elif direction == "right":
        return lock_pos + RIGHT * offset
    elif direction == "up":
        return lock_pos + UP * offset
    else:
        return lock_pos + DOWN * offset


def create_critical_section_bounds(
    x_start: float,
    x_end: float,
    y_center: float,
    height: float = None
) -> dict:
    """
    Calculate bounds for critical section visualization.
    """
    height = height or L.CRITICAL_HEIGHT
    
    return {
        "center": np.array([(x_start + x_end) / 2, y_center, 0]),
        "width": x_end - x_start,
        "height": height,
        "entry": np.array([x_start, y_center, 0]),
        "exit": np.array([x_end, y_center, 0]),
    }
