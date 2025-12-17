"""
Database Animation Framework - Text Helpers
============================================

Text formatting and bilingual support utilities.
"""

from manim import *
import sys
sys.path.append('..')
from config import config, C, T, F, L, A, D


def create_bilingual(
    text_ar: str,
    text_en: str,
    color_ar=None,
    color_en=None,
    scale_ar: float = None,
    scale_en: float = None,
    arrangement: str = "vertical",
    spacing: float = None
) -> VGroup:
    """
    Create a bilingual text pair (Arabic + English).
    
    Args:
        text_ar: Arabic text
        text_en: English text
        color_ar: Arabic text color
        color_en: English text color
        scale_ar: Arabic text scale
        scale_en: English text scale
        arrangement: vertical or horizontal
        spacing: Space between texts
    
    Returns:
        VGroup with both texts
    """
    if color_ar is None:
        color_ar = C.TEXT_PRIMARY
    if color_en is None:
        color_en = C.TEXT_SECONDARY
    if scale_ar is None:
        scale_ar = F.SIZE_BODY
    if scale_en is None:
        scale_en = F.SIZE_CAPTION
    if spacing is None:
        spacing = L.SPACING_SM
    
    ar_text = Text(text_ar, font=F.ARABIC, color=color_ar).scale(scale_ar)
    en_text = Text(text_en, font=F.BODY, color=color_en).scale(scale_en)
    
    group = VGroup(ar_text, en_text)
    
    if arrangement == "vertical":
        group.arrange(DOWN, buff=spacing)
    else:
        group.arrange(RIGHT, buff=spacing)
    
    return group


def format_step_label(
    step_num: int,
    text_ar: str,
    text_en: str = None,
    color=None
) -> VGroup:
    """
    Format a step label with number.
    
    Args:
        step_num: Step number
        text_ar: Arabic description
        text_en: English description (optional)
        color: Label color
    
    Returns:
        VGroup with formatted step label
    """
    if color is None:
        color = C.PRIMARY_YELLOW
    
    # Arabic step
    step_ar = Text(
        f"الخطوة {step_num}: {text_ar}",
        font=F.ARABIC,
        color=color
    ).scale(F.SIZE_BODY)
    
    if text_en:
        step_en = Text(
            f"Step {step_num}: {text_en}",
            font=F.BODY,
            color=C.TEXT_SECONDARY
        ).scale(F.SIZE_CAPTION)
        
        return VGroup(step_ar, step_en).arrange(DOWN, buff=L.SPACING_TIGHT)
    
    return step_ar


def create_bullet_list(
    items: list,
    bullet: str = "•",
    color=None,
    bullet_color=None,
    alignment: str = "left",
    spacing: float = None
) -> VGroup:
    """
    Create a bullet point list.
    
    Args:
        items: List of text items
        bullet: Bullet character
        color: Text color
        bullet_color: Bullet color
        alignment: Text alignment
        spacing: Space between items
    
    Returns:
        VGroup with bullet list
    """
    if color is None:
        color = C.TEXT_PRIMARY
    if bullet_color is None:
        bullet_color = C.PRIMARY_YELLOW
    if spacing is None:
        spacing = L.SPACING_MD
    
    list_group = VGroup()
    
    for item in items:
        # Bullet
        bullet_text = Text(bullet, font=F.BODY, color=bullet_color).scale(F.SIZE_BODY)
        
        # Item text
        item_text = Text(item, font=F.ARABIC, color=color).scale(F.SIZE_BODY)
        
        # Line
        line = VGroup(bullet_text, item_text).arrange(RIGHT, buff=L.SPACING_SM)
        list_group.add(line)
    
    list_group.arrange(DOWN, aligned_edge=LEFT, buff=spacing)
    
    return list_group


def wrap_text(
    text: str,
    max_chars: int = 40,
    font=None,
    color=None,
    scale: float = None
) -> Text:
    """
    Wrap long text to multiple lines.
    
    Args:
        text: Text to wrap
        max_chars: Maximum characters per line
        font: Font family
        color: Text color
        scale: Text scale
    
    Returns:
        Text mobject with wrapped text
    """
    if font is None:
        font = F.BODY
    if color is None:
        color = C.TEXT_PRIMARY
    if scale is None:
        scale = F.SIZE_BODY
    
    # Simple word wrapping
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= max_chars:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    wrapped = '\n'.join(lines)
    return Text(wrapped, font=font, color=color).scale(scale)


def create_title_with_subtitle(
    title_ar: str,
    title_en: str,
    subtitle_ar: str = None,
    subtitle_en: str = None
) -> VGroup:
    """
    Create a title with optional subtitle.
    
    Args:
        title_ar: Main Arabic title
        title_en: Main English title
        subtitle_ar: Optional Arabic subtitle
        subtitle_en: Optional English subtitle
    
    Returns:
        VGroup with title composition
    """
    title = create_bilingual(
        title_ar, title_en,
        scale_ar=F.SIZE_TITLE,
        scale_en=F.SIZE_SUBTITLE
    )
    
    if subtitle_ar or subtitle_en:
        subtitle = create_bilingual(
            subtitle_ar or "",
            subtitle_en or "",
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION,
            color_ar=C.TEXT_SECONDARY,
            color_en=C.TEXT_TERTIARY
        )
        return VGroup(title, subtitle).arrange(DOWN, buff=L.SPACING_LG)
    
    return title


def create_code_comment(
    code: str,
    comment: str,
    comment_lang: str = "ar"
) -> VGroup:
    """
    Create code with inline comment.
    
    Args:
        code: Code text
        comment: Comment text
        comment_lang: Comment language (ar/en)
    
    Returns:
        VGroup with code and comment
    """
    code_text = Text(code, font=F.CODE, color=C.TEXT_CODE).scale(F.SIZE_CODE)
    
    font = F.ARABIC if comment_lang == "ar" else F.BODY
    comment_text = Text(
        f"// {comment}",
        font=font,
        color=C.TEXT_TERTIARY
    ).scale(F.SIZE_CAPTION)
    
    comment_text.next_to(code_text, RIGHT, buff=L.SPACING_MD)
    
    return VGroup(code_text, comment_text)


def create_key_value(
    key: str,
    value: str,
    key_color=None,
    value_color=None,
    separator: str = ":"
) -> VGroup:
    """
    Create a key-value pair display.
    
    Args:
        key: Key text
        value: Value text
        key_color: Key color
        value_color: Value color
        separator: Separator character
    
    Returns:
        VGroup with key-value pair
    """
    if key_color is None:
        key_color = C.TEXT_SECONDARY
    if value_color is None:
        value_color = C.TEXT_PRIMARY
    
    key_text = Text(
        f"{key}{separator}",
        font=F.CODE,
        color=key_color
    ).scale(F.SIZE_CODE)
    
    value_text = Text(
        value,
        font=F.CODE,
        color=value_color
    ).scale(F.SIZE_CODE)
    
    value_text.next_to(key_text, RIGHT, buff=L.SPACING_SM)
    
    return VGroup(key_text, value_text)


def create_status_badge(
    text: str,
    status: str = "neutral"
) -> VGroup:
    """
    Create a status badge (success/warning/error/neutral).
    
    Args:
        text: Badge text
        status: Status type
    
    Returns:
        VGroup with badge
    """
    colors = {
        "success": C.SUCCESS,
        "warning": C.WARNING,
        "error": C.ERROR,
        "neutral": C.TEXT_SECONDARY
    }
    color = colors.get(status, C.TEXT_SECONDARY)
    
    badge_text = Text(text, font=F.CODE, color=color).scale(F.SIZE_LABEL)
    
    badge_bg = RoundedRectangle(
        width=badge_text.width + 0.3,
        height=badge_text.height + 0.15,
        corner_radius=0.1,
        fill_color=color,
        fill_opacity=0.15,
        stroke_color=color,
        stroke_width=1
    )
    badge_bg.move_to(badge_text)
    
    return VGroup(badge_bg, badge_text)
