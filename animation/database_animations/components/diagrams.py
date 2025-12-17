"""
Database Animation Framework - Diagram Components
==================================================

Complex diagram components: tables, storage layers, log structures, etc.
"""

from manim import *
import sys
sys.path.append('..')
from config import config, C, T, F, L, A, D


class StorageLayer(VGroup):
    """
    Single storage layer in a storage hierarchy diagram.
    
    Represents Application, OS Cache, Device RAM, or Disk.
    """
    
    def __init__(
        self,
        name: str,
        name_ar: str = None,
        color=None,
        width: float = None,
        height: float = None,
        icon: str = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        if color is None:
            color = C.PRIMARY_BLUE
        if width is None:
            width = D.LAYER_WIDTH
        if height is None:
            height = D.LAYER_HEIGHT
        
        self.color = color
        self.name = name
        
        # Layer rectangle
        self.rect = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.1,
            color=color,
            fill_opacity=0.15,
            stroke_width=2
        )
        
        # Layer name
        self.label = Text(
            name,
            font=F.BODY,
            color=color
        ).scale(F.SIZE_BODY)
        self.label.move_to(self.rect)
        
        # Arabic name (optional)
        if name_ar:
            self.label_ar = Text(
                name_ar,
                font=F.ARABIC,
                color=C.TEXT_SECONDARY
            ).scale(F.SIZE_CAPTION)
            self.label_ar.next_to(self.label, DOWN, buff=0.05)
            self.add(self.label_ar)
        
        # Icon (optional)
        if icon:
            self.icon = Text(icon, font=F.EMOJI).scale(0.4)
            self.icon.next_to(self.label, LEFT, buff=L.SPACING_SM)
            self.add(self.icon)
        
        self.add(self.rect, self.label)
    
    def animate_highlight(self, color=None) -> Animation:
        """Highlight this layer"""
        if color is None:
            color = C.PRIMARY_YELLOW
        return Indicate(self.rect, color=color, scale_factor=1.02)
    
    def animate_data_enter(self) -> Animation:
        """Show data entering this layer"""
        return Flash(
            self.rect.get_top(),
            color=self.color,
            line_length=0.2,
            num_lines=8
        )


class StorageStack(VGroup):
    """
    Complete storage hierarchy stack.
    
    Application → OS Cache → Device RAM → Disk
    """
    
    def __init__(
        self,
        show_labels: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # Define layers from top to bottom
        layer_configs = [
            ("Application", "التطبيق", C.LAYER_APP, "💻"),
            ("OS Page Cache", "ذاكرة النظام", C.LAYER_OS, "📋"),
            ("Device RAM", "ذاكرة الجهاز", C.LAYER_DEVICE, "⚡"),
            ("Disk Storage", "القرص", C.LAYER_DISK, "💾"),
        ]
        
        self.layers = []
        for name, name_ar, color, icon in layer_configs:
            layer = StorageLayer(
                name=name,
                name_ar=name_ar if show_labels else None,
                color=color,
                icon=icon
            )
            self.layers.append(layer)
            self.add(layer)
        
        # Arrange vertically
        self.arrange(DOWN, buff=D.LAYER_SPACING)
        
        # Create connecting arrows
        self.arrows = VGroup()
        for i in range(len(self.layers) - 1):
            arrow = Arrow(
                self.layers[i].get_bottom(),
                self.layers[i + 1].get_top(),
                color=C.TEXT_TERTIARY,
                stroke_width=2,
                buff=0.1
            )
            self.arrows.add(arrow)
        
        self.add(self.arrows)
    
    def get_layer(self, index: int) -> StorageLayer:
        """Get layer by index (0=app, 3=disk)"""
        return self.layers[index] if 0 <= index < len(self.layers) else None
    
    def animate_build(self) -> LaggedStart:
        """Animate building the stack from top to bottom"""
        anims = []
        for layer in self.layers:
            anims.append(FadeIn(layer, shift=DOWN * 0.3))
        
        for arrow in self.arrows:
            anims.append(Create(arrow))
        
        return LaggedStart(*anims, lag_ratio=0.2)
    
    def animate_data_flow(
        self, 
        from_layer: int, 
        to_layer: int,
        color=None
    ) -> Succession:
        """Animate data flowing between layers"""
        if color is None:
            color = C.SUCCESS
        
        dot = Dot(color=color, radius=0.1)
        dot.move_to(self.layers[from_layer].get_center())
        
        return Succession(
            Create(dot),
            dot.animate.move_to(self.layers[to_layer].get_center()),
            FadeOut(dot)
        )


class LogEntry(VGroup):
    """
    Single log entry representation.
    
    Shows operation with checksum indicator.
    """
    
    def __init__(
        self,
        operation: str,
        index: int = 0,
        status: str = "valid",  # valid, invalid, pending
        color=None,
        show_checksum: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # Determine color based on status
        if color is None:
            color = {
                "valid": C.SUCCESS,
                "invalid": C.ERROR,
                "pending": C.WARNING
            }.get(status, C.PRIMARY_BLUE)
        
        self.status = status
        self.operation = operation
        
        # Entry box
        self.rect = RoundedRectangle(
            width=D.LOG_ENTRY_WIDTH,
            height=D.LOG_ENTRY_HEIGHT,
            corner_radius=0.08,
            color=color,
            fill_opacity=0.15,
            stroke_width=2
        )
        
        # Operation text
        self.op_text = Text(
            operation,
            font=F.CODE,
            color=C.TEXT_PRIMARY
        ).scale(F.SIZE_CAPTION)
        self.op_text.move_to(self.rect)
        
        # Index label
        self.index_label = Text(
            str(index),
            font=F.CODE,
            color=C.TEXT_TERTIARY
        ).scale(F.SIZE_LABEL)
        self.index_label.next_to(self.rect, UP, buff=0.05)
        
        self.add(self.rect, self.op_text, self.index_label)
        
        # Checksum indicator
        if show_checksum:
            checkmark = "✓" if status == "valid" else ("✗" if status == "invalid" else "?")
            self.checksum = Text(
                checkmark,
                font=F.EMOJI,
                color=color
            ).scale(F.SIZE_LABEL)
            self.checksum.next_to(self.rect, DOWN, buff=0.05)
            self.add(self.checksum)
    
    def animate_appear(self) -> Animation:
        """Animate entry appearing"""
        return FadeIn(self, shift=LEFT * 0.3, scale=0.9)
    
    def animate_validate(self) -> Animation:
        """Animate validation checkmark"""
        return Indicate(self.checksum, color=C.SUCCESS, scale_factor=1.5)
    
    def animate_invalidate(self) -> AnimationGroup:
        """Animate marking as invalid"""
        return AnimationGroup(
            self.rect.animate.set_stroke(color=C.ERROR),
            self.op_text.animate.set_opacity(0.3),
            Flash(self.get_center(), color=C.ERROR),
            run_time=T.FAST
        )


class LogSequence(VGroup):
    """
    Sequence of log entries.
    
    Represents an append-only log structure.
    """
    
    def __init__(
        self,
        entries: list = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.entries = []
        
        if entries:
            for i, (op, status) in enumerate(entries):
                entry = LogEntry(op, i, status)
                self.entries.append(entry)
                self.add(entry)
            
            self.arrange(RIGHT, buff=D.LOG_SPACING)
    
    def add_entry(self, operation: str, status: str = "valid") -> LogEntry:
        """Add new entry to the log"""
        index = len(self.entries)
        entry = LogEntry(operation, index, status)
        
        if self.entries:
            entry.next_to(self.entries[-1], RIGHT, buff=D.LOG_SPACING)
        
        self.entries.append(entry)
        self.add(entry)
        return entry
    
    def animate_build(self) -> LaggedStart:
        """Animate log building up"""
        return LaggedStart(
            *[entry.animate_appear() for entry in self.entries],
            lag_ratio=0.3
        )
    
    def get_entry(self, index: int) -> LogEntry:
        """Get entry by index"""
        return self.entries[index] if 0 <= index < len(self.entries) else None


class ComparisonTable(VGroup):
    """
    Comparison table for different approaches.
    
    Clean table with headers and data rows.
    """
    
    def __init__(
        self,
        headers: list,
        rows: list,
        highlight_row: int = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # Create table using Manim's Table
        all_data = [headers] + rows
        
        self.table = Table(
            all_data,
            include_outer_lines=True,
            line_config={
                "stroke_width": 2,
                "color": C.TEXT_TERTIARY
            },
            element_to_mobject_config={
                "font": F.BODY
            }
        ).scale(0.5)
        
        # Style header row
        header_cells = self.table.get_row_labels() if self.table.get_row_labels() else self.table.get_rows()[0]
        
        self.add(self.table)
        
        self.highlight_row_index = highlight_row
    
    def animate_build(self) -> Animation:
        """Animate table appearing"""
        return FadeIn(self.table, run_time=T.NORMAL)
    
    def highlight_row(self, row_index: int, color=None) -> Animation:
        """Highlight a specific row"""
        if color is None:
            color = C.SUCCESS
        
        row = self.table.get_rows()[row_index]
        box = SurroundingRectangle(row, color=color, buff=0.1)
        return Create(box)


class Arrow(VGroup):
    """
    Styled arrow for diagrams.
    
    Consistent arrow styling across all diagrams.
    """
    
    def __init__(
        self,
        start,
        end,
        color=None,
        label: str = None,
        label_position: str = "above",  # above, below, left, right
        curved: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        if color is None:
            color = C.PRIMARY_YELLOW
        
        # Create arrow
        if curved:
            self.arrow = CurvedArrow(
                start,
                end,
                color=color,
                stroke_width=D.ARROW_STROKE_WIDTH,
                angle=TAU/4
            )
        else:
            self.arrow = ManimArrow(
                start,
                end,
                color=color,
                stroke_width=D.ARROW_STROKE_WIDTH,
                tip_length=D.ARROW_TIP_LENGTH,
            )
        
        self.add(self.arrow)
        
        # Add label
        if label:
            self.label = Text(
                label,
                font=F.CODE,
                color=color
            ).scale(F.SIZE_CAPTION)
            
            # Position label
            if label_position == "above":
                self.label.next_to(self.arrow, UP, buff=L.SPACING_TIGHT)
            elif label_position == "below":
                self.label.next_to(self.arrow, DOWN, buff=L.SPACING_TIGHT)
            elif label_position == "left":
                self.label.next_to(self.arrow, LEFT, buff=L.SPACING_TIGHT)
            elif label_position == "right":
                self.label.next_to(self.arrow, RIGHT, buff=L.SPACING_TIGHT)
            
            self.add(self.label)
    
    def animate_draw(self) -> Animation:
        """Animate arrow being drawn"""
        return Create(self, run_time=T.FAST)


# Alias for Manim's Arrow to avoid conflicts
ManimArrow = Arrow


class ConceptBox(VGroup):
    """
    Box for displaying a concept with icon.
    
    Used in overview/summary scenes.
    """
    
    def __init__(
        self,
        title: str,
        color=None,
        icon: str = None,
        width: float = 2.5,
        height: float = 2.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        if color is None:
            color = C.PRIMARY_BLUE
        
        # Box
        self.rect = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.15,
            color=color,
            fill_opacity=0.1,
            stroke_width=3
        )
        
        # Content
        content_parts = []
        
        if icon:
            self.icon = Text(icon, font=F.EMOJI).scale(0.6)
            content_parts.append(self.icon)
        
        self.title = Text(
            title,
            font=F.BODY,
            color=color
        ).scale(F.SIZE_BODY)
        content_parts.append(self.title)
        
        content = VGroup(*content_parts).arrange(DOWN, buff=L.SPACING_SM)
        content.move_to(self.rect)
        
        self.add(self.rect, content)
    
    def animate_appear(self) -> Animation:
        """Animate box appearing"""
        return FadeIn(self, scale=0.9, run_time=T.NORMAL)


class EntryStructure(VGroup):
    """
    Detailed log entry structure showing header and data.
    
    Used to explain checksum/log entry format.
    """
    
    def __init__(
        self,
        header_text: str = "Header\nSize+Hash",
        data_text: str = "Data",
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # Header section
        self.header_box = Rectangle(
            width=1.8,
            height=0.7,
            color=C.PRIMARY_BLUE,
            fill_opacity=0.2,
            stroke_width=2
        )
        self.header_label = Text(
            header_text,
            font=F.CODE,
            color=C.PRIMARY_BLUE
        ).scale(F.SIZE_CAPTION)
        self.header_label.move_to(self.header_box)
        
        # Data section
        self.data_box = Rectangle(
            width=2.5,
            height=0.7,
            color=C.SUCCESS,
            fill_opacity=0.2,
            stroke_width=2
        )
        self.data_box.next_to(self.header_box, RIGHT, buff=0)
        
        self.data_label = Text(
            data_text,
            font=F.CODE,
            color=C.SUCCESS
        ).scale(F.SIZE_CAPTION)
        self.data_label.move_to(self.data_box)
        
        self.add(self.header_box, self.header_label, self.data_box, self.data_label)
    
    def animate_build(self) -> Succession:
        """Animate structure appearing"""
        return Succession(
            FadeIn(self.header_box, self.header_label),
            FadeIn(self.data_box, self.data_label),
            run_time=T.NORMAL
        )
