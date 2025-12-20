"""
Text Utilities for OS Concepts
==============================

Helper functions for text creation and formatting.
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import C, T, F, L


def create_bilingual(
    text_ar: str,
    text_en: str,
    color_ar=None,
    color_en=None,
    scale_ar: float = None,
    scale_en: float = None
) -> VGroup:
    """
    Create bilingual text (Arabic + English).
    """
    color_ar = color_ar or C.TEXT_PRIMARY
    color_en = color_en or C.TEXT_SECONDARY
    scale_ar = scale_ar or F.SIZE_BODY
    scale_en = scale_en or F.SIZE_CAPTION
    
    arabic = Text(text_ar, font=F.ARABIC, color=color_ar).scale(scale_ar)
    english = Text(text_en, font=F.BODY, color=color_en).scale(scale_en)
    
    group = VGroup(arabic, english)
    group.arrange(DOWN, buff=L.SPACING_SM)
    
    return group


def create_step_label(
    step_num: int,
    text_ar: str,
    text_en: str,
    color=None
) -> VGroup:
    """
    Create numbered step label.
    """
    color = color or C.TEXT_ACCENT
    
    # Step indicator
    step = Text(
        f"Step {step_num}",
        font=F.CODE,
        color=color
    ).scale(F.SIZE_LABEL)
    
    # Description
    desc = create_bilingual(
        text_ar,
        text_en,
        scale_ar=F.SIZE_CAPTION,
        scale_en=F.SIZE_LABEL
    )
    
    group = VGroup(step, desc)
    group.arrange(DOWN, buff=L.SPACING_TIGHT, aligned_edge=LEFT)
    
    return group


def create_state_badge(
    state: str,
    color=None
) -> VGroup:
    """
    Create state indicator badge.
    """
    state_colors = {
        "running": C.RUNNING,
        "blocked": C.BLOCKED,
        "ready": C.READY,
        "completed": C.COMPLETED,
        "locked": C.LOCK_HELD,
        "free": C.LOCK_FREE,
        "waiting": C.LOCK_WAITING,
        "conflict": C.CONFLICT,
        "success": C.SUCCESS,
        "error": C.ERROR,
    }
    
    color = color or state_colors.get(state.lower(), C.TEXT_SECONDARY)
    
    # Badge background
    bg = RoundedRectangle(
        width=1.2,
        height=0.35,
        color=color,
        fill_opacity=0.2,
        stroke_width=1,
        corner_radius=0.1
    )
    
    # State text
    text = Text(
        state.upper(),
        font=F.CODE,
        color=color
    ).scale(F.SIZE_TINY)
    text.move_to(bg.get_center())
    
    return VGroup(bg, text)


def create_code_snippet(
    code: str,
    highlight_lines: list = None,
    width: float = 4.0
) -> VGroup:
    """
    Create code snippet display.
    """
    highlight_lines = highlight_lines or []
    
    lines = code.strip().split('\n')
    code_group = VGroup()
    
    for i, line in enumerate(lines):
        is_highlighted = (i + 1) in highlight_lines
        color = C.TEXT_ACCENT if is_highlighted else C.TEXT_PRIMARY
        bg_opacity = 0.15 if is_highlighted else 0
        
        # Line background
        line_bg = Rectangle(
            width=width,
            height=0.35,
            fill_color=C.TEXT_ACCENT,
            fill_opacity=bg_opacity,
            stroke_width=0
        )
        
        # Line number
        line_num = Text(
            f"{i+1:2d}",
            font=F.CODE,
            color=C.TEXT_TERTIARY
        ).scale(F.SIZE_TINY)
        
        # Code text
        code_text = Text(
            line,
            font=F.CODE,
            color=color
        ).scale(F.SIZE_CODE)
        
        line_group = VGroup(line_bg, line_num, code_text)
        line_num.move_to(line_bg.get_left() + RIGHT * 0.3)
        code_text.move_to(line_bg.get_left() + RIGHT * 0.8)
        code_text.align_to(line_bg.get_left() + RIGHT * 0.6, LEFT)
        
        code_group.add(line_group)
    
    code_group.arrange(DOWN, buff=0.02, aligned_edge=LEFT)
    
    # Container
    container = RoundedRectangle(
        width=width + 0.4,
        height=code_group.height + 0.3,
        fill_color=C.BACKGROUND_ALT,
        fill_opacity=0.8,
        stroke_color=C.TEXT_TERTIARY,
        stroke_width=1,
        corner_radius=0.1
    )
    container.move_to(code_group.get_center())
    
    return VGroup(container, code_group)


def create_comparison_labels(
    left_label: str,
    right_label: str,
    left_color=None,
    right_color=None
) -> tuple:
    """
    Create labels for comparison view.
    """
    left_color = left_color or C.THREAD_1
    right_color = right_color or C.THREAD_2
    
    left = Text(left_label, font=F.BODY, color=left_color).scale(F.SIZE_HEADING)
    right = Text(right_label, font=F.BODY, color=right_color).scale(F.SIZE_HEADING)
    
    left.move_to(LEFT * L.COMPARE_LEFT_CENTER + UP * 3)
    right.move_to(RIGHT * L.COMPARE_RIGHT_CENTER + UP * 3)
    
    return left, right


def create_metric_display(
    label: str,
    value: str,
    color=None
) -> VGroup:
    """
    Create metric value display.
    """
    color = color or C.TEXT_ACCENT
    
    label_text = Text(label, font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_LABEL)
    value_text = Text(value, font=F.CODE, color=color).scale(F.SIZE_BODY)
    
    group = VGroup(label_text, value_text)
    group.arrange(DOWN, buff=L.SPACING_TIGHT)
    
    return group
