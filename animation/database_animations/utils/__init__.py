"""
Database Animation Framework - Utilities Package
=================================================

Helper functions and utilities for animations.
"""

from utils.animations import (
    create_staggered_fade_in,
    create_emphasis_sequence,
    create_shake_animation,
    create_glow_animation,
    smooth_path
)
from utils.math_helpers import (
    golden_position,
    fibonacci_scale,
    calculate_grid_positions,
    interpolate_color
)
from utils.text_helpers import (
    create_bilingual,
    format_step_label,
    create_bullet_list,
    wrap_text
)

__all__ = [
    # Animations
    'create_staggered_fade_in',
    'create_emphasis_sequence',
    'create_shake_animation',
    'create_glow_animation',
    'smooth_path',
    
    # Math
    'golden_position',
    'fibonacci_scale',
    'calculate_grid_positions',
    'interpolate_color',
    
    # Text
    'create_bilingual',
    'format_step_label',
    'create_bullet_list',
    'wrap_text',
]
