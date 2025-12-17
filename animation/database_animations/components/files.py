"""
Database Animation Framework - File Components
===============================================

Reusable file visualization components.
These provide consistent file representations across all scenes.
"""

from manim import *
import sys
sys.path.append('..')
from config import config, C, T, F, L, A, D


class FileBox(VGroup):
    """
    Standard file representation used throughout all chapters.
    Ensures visual consistency for file concepts.
    
    Features:
    - Rounded rectangle with glow effect
    - Filename label above
    - Content display with optional icon
    - State change animations (corrupt, empty, success)
    """
    
    def __init__(
        self,
        filename: str,
        content_text: str = "",
        color=None,
        width: float = None,
        height: float = None,
        show_icon: bool = True,
        icon: str = "📄",
        fill_opacity: float = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # Defaults
        if color is None:
            color = C.FILE_ORIGINAL
        if width is None:
            width = D.FILE_WIDTH
        if height is None:
            height = D.FILE_HEIGHT
        if fill_opacity is None:
            fill_opacity = D.FILE_FILL_OPACITY
        
        self.base_color = color
        self.filename = filename
        
        # Main rectangle with rounded corners
        self.rect = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=D.FILE_CORNER_RADIUS,
            stroke_width=D.FILE_STROKE_WIDTH,
            stroke_color=color,
            fill_color=color,
            fill_opacity=fill_opacity
        )
        
        # Filename label
        self.label = Text(
            filename, 
            font=F.CODE,
            color=C.TEXT_SECONDARY
        ).scale(F.SIZE_CAPTION)
        self.label.next_to(self.rect, UP, buff=L.SPACING_SM)
        
        # Content area
        if show_icon and content_text:
            self.icon = Text(icon, font=F.EMOJI).scale(0.5)
            self.content_text = Text(
                content_text, 
                font=F.BODY,
                color=color
            ).scale(F.SIZE_BODY)
            self.content = VGroup(self.icon, self.content_text)
            self.content.arrange(DOWN, buff=L.SPACING_SM)
        elif content_text:
            self.content = Text(
                content_text, 
                font=F.BODY,
                color=color
            ).scale(F.SIZE_BODY)
        else:
            self.content = VGroup()
        
        self.content.move_to(self.rect.get_center())
        
        # Add all elements
        self.add(self.rect, self.label, self.content)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ENTRANCE ANIMATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def animate_create(self) -> AnimationGroup:
        """Standard creation animation for files"""
        return AnimationGroup(
            FadeIn(self.rect, scale=0.9),
            FadeIn(self.label, shift=DOWN * 0.2),
            FadeIn(self.content),
            lag_ratio=0.2,
            run_time=T.NORMAL
        )
    
    def animate_write(self) -> Succession:
        """Typing-style creation (more dramatic)"""
        return Succession(
            Create(self.rect, run_time=T.FAST),
            Write(self.label, run_time=T.QUICK),
            FadeIn(self.content, scale=0.8, run_time=T.QUICK)
        )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STATE CHANGE ANIMATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def animate_corrupt(self) -> AnimationGroup:
        """Show file corruption"""
        return AnimationGroup(
            self.rect.animate.set_stroke(color=C.FILE_CORRUPT),
            self.rect.animate.set_fill(color=C.FILE_CORRUPT, opacity=0.1),
            Flash(self.rect.get_center(), color=C.FILE_CORRUPT, line_length=0.2),
            self.content.animate.set_opacity(0.3),
            run_time=T.FAST
        )
    
    def animate_truncate(self, empty_label: str = "EMPTY!") -> AnimationGroup:
        """Show file being truncated"""
        empty_text = Text(
            empty_label, 
            font=F.BODY,
            color=C.ERROR
        ).scale(F.SIZE_BODY)
        empty_text.move_to(self.rect.get_center())
        
        return AnimationGroup(
            FadeOut(self.content),
            self.rect.animate.set_stroke(color=C.ERROR),
            self.rect.animate.set_fill(color=C.ERROR, opacity=0.05),
            FadeIn(empty_text, scale=1.2),
            run_time=T.FAST
        )
    
    def animate_success(self) -> AnimationGroup:
        """Show file success state"""
        return AnimationGroup(
            self.rect.animate.set_stroke(color=C.SUCCESS),
            self.rect.animate.set_fill(color=C.SUCCESS, opacity=0.15),
            Flash(self.rect.get_center(), color=C.SUCCESS, line_length=0.3),
            run_time=T.FAST
        )
    
    def animate_highlight(self, color=None) -> Animation:
        """Highlight the file temporarily"""
        if color is None:
            color = C.PRIMARY_YELLOW
        return Indicate(self, color=color, scale_factor=1.1)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STATE SETTERS (NON-ANIMATED)
    # ═══════════════════════════════════════════════════════════════════════════
    
    def set_corrupt(self):
        """Set to corrupt state immediately"""
        self.rect.set_stroke(color=C.FILE_CORRUPT)
        self.rect.set_fill(color=C.FILE_CORRUPT, opacity=0.1)
        self.content.set_opacity(0.3)
        return self
    
    def set_success(self):
        """Set to success state immediately"""
        self.rect.set_stroke(color=C.SUCCESS)
        self.rect.set_fill(color=C.SUCCESS, opacity=0.15)
        return self
    
    def set_color(self, color):
        """Change file color"""
        self.rect.set_stroke(color=color)
        self.rect.set_fill(color=color, opacity=D.FILE_FILL_OPACITY)
        self.base_color = color
        return self


class TempFile(FileBox):
    """
    Temporary file representation.
    Styled differently to indicate temporary nature.
    """
    
    def __init__(
        self,
        filename: str,
        content_text: str = "",
        **kwargs
    ):
        super().__init__(
            filename=filename,
            content_text=content_text,
            color=C.FILE_TEMP,
            icon="📝",
            **kwargs
        )
        
        # Add dashed border effect
        self.rect.set_stroke(opacity=0.8)


class FileGroup(VGroup):
    """
    A group of related files displayed together.
    Useful for showing file states side by side.
    """
    
    def __init__(
        self,
        files: list,
        arrangement: str = "horizontal",
        spacing: float = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        if spacing is None:
            spacing = L.SPACING_XL
        
        self.files = files
        for f in files:
            self.add(f)
        
        if arrangement == "horizontal":
            self.arrange(RIGHT, buff=spacing)
        elif arrangement == "vertical":
            self.arrange(DOWN, buff=spacing)
    
    def animate_create_sequence(self, lag_ratio: float = 0.3) -> LaggedStart:
        """Animate files appearing in sequence"""
        return LaggedStart(
            *[f.animate_create() for f in self.files],
            lag_ratio=lag_ratio
        )


class DataBlock(VGroup):
    """
    Represents a block of data that can be transferred between files.
    Useful for visualizing data movement.
    """
    
    def __init__(
        self,
        label: str = "Data",
        size_label: str = "",
        color=None,
        width: float = 1.5,
        height: float = 1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        if color is None:
            color = C.DATA_COLD
        
        self.rect = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.1,
            stroke_color=color,
            fill_color=color,
            fill_opacity=0.3,
            stroke_width=2
        )
        
        text_content = label
        if size_label:
            text_content = f"{label}\n{size_label}"
        
        self.text = Text(
            text_content,
            font=F.CODE,
            color=color
        ).scale(F.SIZE_CAPTION)
        self.text.move_to(self.rect)
        
        self.add(self.rect, self.text)
    
    def animate_transfer_to(self, target: Mobject) -> Animation:
        """Animate data block moving to target"""
        return self.animate.move_to(target.get_center())
    
    def set_hot(self):
        """Set data to 'hot' (in-motion) state"""
        self.rect.set_stroke(color=C.DATA_HOT)
        self.rect.set_fill(color=C.DATA_HOT, opacity=0.3)
        return self
    
    def set_safe(self):
        """Set data to 'safe' (persisted) state"""
        self.rect.set_stroke(color=C.DATA_SAFE)
        self.rect.set_fill(color=C.DATA_SAFE, opacity=0.3)
        return self
