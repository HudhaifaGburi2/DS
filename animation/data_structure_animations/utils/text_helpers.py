"""
Text Utilities
==============

Helper functions for text creation and formatting.
Supports bilingual (Arabic/English) text.
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
    scale_en: float = None,
    spacing: float = None
) -> VGroup:
    """
    Create bilingual text group (Arabic + English).
    
    Args:
        text_ar: Arabic text
        text_en: English text
        color_ar: Arabic text color
        color_en: English text color
        scale_ar: Arabic text scale
        scale_en: English text scale
        spacing: Spacing between texts
    
    Returns:
        VGroup containing both texts
    """
    color_ar = color_ar or C.TEXT_PRIMARY
    color_en = color_en or C.TEXT_SECONDARY
    scale_ar = scale_ar or F.SIZE_BODY
    scale_en = scale_en or F.SIZE_CAPTION
    spacing = spacing or L.SPACING_SM
    
    arabic = Text(text_ar, font=F.ARABIC, color=color_ar).scale(scale_ar)
    english = Text(text_en, font=F.BODY, color=color_en).scale(scale_en)
    
    group = VGroup(arabic, english)
    group.arrange(DOWN, buff=spacing)
    
    return group


def create_step_label(
    step_number: int,
    text_ar: str,
    text_en: str,
    color=None
) -> VGroup:
    """
    Create numbered step label.
    
    Args:
        step_number: Step number
        text_ar: Arabic description
        text_en: English description
        color: Accent color
    
    Returns:
        VGroup with step indicator
    """
    color = color or C.TEXT_ACCENT
    
    # Step number
    number = Text(
        f"Step {step_number}",
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
    
    group = VGroup(number, desc)
    group.arrange(DOWN, buff=L.SPACING_TIGHT, aligned_edge=LEFT)
    
    return group


def create_metric_label(
    metric_name: str,
    value: str,
    unit: str = "",
    color=None,
    value_color=None
) -> VGroup:
    """
    Create metric display label.
    
    Args:
        metric_name: Name of metric
        value: Metric value
        unit: Unit of measurement
        color: Name color
        value_color: Value color
    
    Returns:
        VGroup with metric display
    """
    color = color or C.TEXT_SECONDARY
    value_color = value_color or C.TEXT_PRIMARY
    
    name = Text(metric_name, font=F.BODY, color=color).scale(F.SIZE_LABEL)
    
    value_text = f"{value}{unit}"
    val = Text(value_text, font=F.CODE, color=value_color).scale(F.SIZE_BODY)
    
    group = VGroup(name, val)
    group.arrange(DOWN, buff=L.SPACING_TIGHT)
    
    return group


def create_code_snippet(
    code: str,
    language: str = "python",
    color=None,
    highlight_lines: list = None
) -> VGroup:
    """
    Create code snippet display.
    
    Args:
        code: Code string
        language: Programming language
        color: Base color
        highlight_lines: Line numbers to highlight
    
    Returns:
        VGroup containing code
    """
    color = color or C.TEXT_PRIMARY
    highlight_lines = highlight_lines or []
    
    lines = code.strip().split('\n')
    code_group = VGroup()
    
    for i, line in enumerate(lines):
        line_color = C.TEXT_ACCENT if (i + 1) in highlight_lines else color
        
        # Line number
        line_num = Text(
            f"{i + 1:2d}",
            font=F.CODE,
            color=C.TEXT_TERTIARY
        ).scale(F.SIZE_TINY)
        
        # Code text
        code_text = Text(
            line,
            font=F.CODE,
            color=line_color
        ).scale(F.SIZE_KEY)
        
        line_group = VGroup(line_num, code_text)
        line_group.arrange(RIGHT, buff=L.SPACING_SM)
        code_group.add(line_group)
    
    code_group.arrange(DOWN, buff=0.05, aligned_edge=LEFT)
    
    # Background
    bg = Rectangle(
        width=code_group.width + 0.4,
        height=code_group.height + 0.3,
        fill_color=C.BACKGROUND_ALT,
        fill_opacity=0.8,
        stroke_color=C.TEXT_TERTIARY,
        stroke_width=1,
        corner_radius=0.1
    )
    bg.move_to(code_group.get_center())
    
    return VGroup(bg, code_group)


def wrap_text(
    text: str,
    max_width: int = 40,
    font=None,
    color=None,
    scale: float = None
) -> VGroup:
    """
    Wrap text to multiple lines.
    
    Args:
        text: Text to wrap
        max_width: Maximum characters per line
        font: Font family
        color: Text color
        scale: Text scale
    
    Returns:
        VGroup of text lines
    """
    font = font or F.BODY
    color = color or C.TEXT_PRIMARY
    scale = scale or F.SIZE_CAPTION
    
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= max_width:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    text_group = VGroup()
    for line in lines:
        text_obj = Text(line, font=font, color=color).scale(scale)
        text_group.add(text_obj)
    
    text_group.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    
    return text_group


def create_comparison_header(
    left_title: str,
    right_title: str,
    left_color=None,
    right_color=None
) -> VGroup:
    """
    Create header for comparison view.
    
    Args:
        left_title: Left side title
        right_title: Right side title
        left_color: Left title color
        right_color: Right title color
    
    Returns:
        VGroup with comparison header
    """
    left_color = left_color or C.COMPARE_A
    right_color = right_color or C.COMPARE_B
    
    left = Text(left_title, font=F.BODY, color=left_color).scale(F.SIZE_HEADING)
    right = Text(right_title, font=F.BODY, color=right_color).scale(F.SIZE_HEADING)
    
    vs = Text("vs", font=F.BODY, color=C.TEXT_TERTIARY).scale(F.SIZE_CAPTION)
    
    group = VGroup(left, vs, right)
    group.arrange(RIGHT, buff=L.SPACING_LG)
    
    return group


def create_verdict_text(
    verdict_ar: str,
    verdict_en: str,
    winner: str = None,  # "left", "right", or None
    color=None
) -> VGroup:
    """
    Create verdict/conclusion text.
    
    Args:
        verdict_ar: Arabic verdict
        verdict_en: English verdict
        winner: Which side won (for color)
        color: Override color
    
    Returns:
        VGroup with verdict
    """
    if color is None:
        if winner == "left":
            color = C.COMPARE_A
        elif winner == "right":
            color = C.COMPARE_B
        else:
            color = C.SUCCESS
    
    # Verdict icon
    icon = Text("✓", font=F.BODY, color=color).scale(F.SIZE_HEADING)
    
    # Verdict text
    verdict = create_bilingual(
        verdict_ar,
        verdict_en,
        color_ar=color,
        color_en=C.TEXT_SECONDARY,
        scale_ar=F.SIZE_BODY,
        scale_en=F.SIZE_CAPTION
    )
    
    group = VGroup(icon, verdict)
    group.arrange(RIGHT, buff=L.SPACING_MD)
    
    return group


def create_title_with_icon(
    icon: str,
    title: str,
    color=None
) -> VGroup:
    """
    Create title with leading icon.
    
    Args:
        icon: Emoji or icon character
        title: Title text
        color: Title color
    
    Returns:
        VGroup with icon and title
    """
    color = color or C.TEXT_PRIMARY
    
    icon_text = Text(icon, font=F.BODY).scale(F.SIZE_HEADING)
    title_text = Text(title, font=F.BODY, color=color).scale(F.SIZE_HEADING)
    
    group = VGroup(icon_text, title_text)
    group.arrange(RIGHT, buff=L.SPACING_SM)
    
    return group
