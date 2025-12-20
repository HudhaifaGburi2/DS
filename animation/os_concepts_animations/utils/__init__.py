"""
OS Concepts Animation Utilities
===============================

Helper functions for animations, layout, and text.
"""

from .animations import (
    create_thread_execution,
    create_lock_sequence,
    create_conflict_animation,
    create_rollback_sequence,
    AnimationSequencer,
)

from .layout import (
    calculate_thread_lanes,
    calculate_lock_positions,
    calculate_timeline_positions,
    distribute_horizontal,
    distribute_vertical,
)

from .text_helpers import (
    create_bilingual,
    create_step_label,
    create_state_badge,
    create_code_snippet,
)

__all__ = [
    # Animations
    "create_thread_execution",
    "create_lock_sequence",
    "create_conflict_animation",
    "create_rollback_sequence",
    "AnimationSequencer",
    # Layout
    "calculate_thread_lanes",
    "calculate_lock_positions",
    "calculate_timeline_positions",
    "distribute_horizontal",
    "distribute_vertical",
    # Text
    "create_bilingual",
    "create_step_label",
    "create_state_badge",
    "create_code_snippet",
]
