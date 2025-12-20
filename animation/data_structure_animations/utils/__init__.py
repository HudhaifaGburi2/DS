"""
Data Structure Animation Utilities
==================================

Helper functions for animations, layout, and text.
"""

from .animations import (
    create_staggered_animation,
    create_emphasis_sequence,
    create_highlight_flash,
    create_path_trace,
    create_comparison_reveal,
    AnimationSequencer,
)

from .layout import (
    calculate_tree_positions,
    calculate_level_positions,
    golden_position,
    golden_scale,
    distribute_horizontal,
    distribute_vertical,
    calculate_bezier_path,
)

from .text_helpers import (
    create_bilingual,
    create_step_label,
    create_metric_label,
    create_code_snippet,
    wrap_text,
)

__all__ = [
    # Animations
    "create_staggered_animation",
    "create_emphasis_sequence",
    "create_highlight_flash",
    "create_path_trace",
    "create_comparison_reveal",
    "AnimationSequencer",
    # Layout
    "calculate_tree_positions",
    "calculate_level_positions",
    "golden_position",
    "golden_scale",
    "distribute_horizontal",
    "distribute_vertical",
    "calculate_bezier_path",
    # Text
    "create_bilingual",
    "create_step_label",
    "create_metric_label",
    "create_code_snippet",
    "wrap_text",
]
