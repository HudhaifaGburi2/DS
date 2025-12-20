"""
Critical Section Components
===========================

Visual representations of shared resources and protected regions.
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import C, T, F, L, A, OS


class CriticalSection(VGroup):
    """
    Visual critical section / danger zone.
    
    Shows protected region that requires synchronization.
    """
    
    def __init__(
        self,
        label: str = "Critical Section",
        width: float = None,
        height: float = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.section_label = label
        self.width = width or L.CRITICAL_WIDTH
        self.height = height or L.CRITICAL_HEIGHT
        self.occupant = None
        
        # Danger zone background
        self.background = RoundedRectangle(
            width=self.width,
            height=self.height,
            color=C.CRITICAL_SECTION,
            fill_opacity=0.12,
            stroke_width=2,
            corner_radius=0.15
        )
        
        # Warning stripes (diagonal lines)
        self.stripes = VGroup()
        stripe_spacing = 0.4
        for i in range(-5, 6):
            stripe = Line(
                self.background.get_corner(DL) + RIGHT * i * stripe_spacing + UP * 0.1,
                self.background.get_corner(DL) + RIGHT * (i * stripe_spacing + self.height) + UP * self.height - UP * 0.1,
                color=C.CRITICAL_SECTION,
                stroke_width=1,
                stroke_opacity=0.15
            )
            self.stripes.add(stripe)
        
        # Clip stripes to background
        self.stripes.set_clip_path(self.background)
        
        # Label
        self.label = Text(
            label,
            font=F.CODE,
            color=C.CRITICAL_SECTION
        ).scale(F.SIZE_LABEL)
        self.label.next_to(self.background, UP, buff=L.SPACING_TIGHT)
        
        # Warning icon
        self.warning = Text("⚠", font=F.BODY, color=C.WARNING).scale(0.3)
        self.warning.next_to(self.label, LEFT, buff=L.SPACING_TIGHT)
        
        self.add(self.background, self.stripes, self.label, self.warning)
    
    def animate_enter(self, thread):
        """Animate thread entering critical section"""
        self.occupant = thread
        return AnimationGroup(
            thread.animate.move_to(self.background.get_center()),
            self.background.animate.set_fill(color=C.LOCK_HELD, opacity=0.2),
            self.background.animate.set_stroke(color=C.LOCK_HELD)
        )
    
    def animate_exit(self, thread, exit_pos):
        """Animate thread exiting critical section"""
        self.occupant = None
        return AnimationGroup(
            thread.animate.move_to(exit_pos),
            self.background.animate.set_fill(color=C.CRITICAL_SECTION, opacity=0.12),
            self.background.animate.set_stroke(color=C.CRITICAL_SECTION)
        )
    
    def animate_violation(self):
        """Animate race condition violation"""
        return Succession(
            self.background.animate.set_fill(color=C.ERROR, opacity=0.4),
            Flash(self.background, color=C.ERROR, line_length=0.3),
            self.background.animate.set_fill(color=C.CRITICAL_SECTION, opacity=0.12)
        )


class SharedResource(VGroup):
    """
    Visual shared resource (counter, data structure, etc).
    """
    
    def __init__(
        self,
        name: str = "counter",
        initial_value: str = "0",
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.name = name
        self.value = initial_value
        
        # Resource container
        self.container = RoundedRectangle(
            width=1.8,
            height=1.0,
            color=C.SHARED_RESOURCE,
            fill_opacity=0.15,
            stroke_width=2,
            corner_radius=0.1
        )
        
        # Name label
        self.name_label = Text(
            name,
            font=F.CODE,
            color=C.SHARED_RESOURCE
        ).scale(F.SIZE_TINY)
        self.name_label.next_to(self.container, UP, buff=L.SPACING_TIGHT)
        
        # Value display
        self.value_display = Text(
            initial_value,
            font=F.CODE,
            color=C.TEXT_PRIMARY
        ).scale(F.SIZE_BODY)
        self.value_display.move_to(self.container.get_center())
        
        self.add(self.container, self.name_label, self.value_display)
    
    def animate_read(self, reader_color=None):
        """Animate read access"""
        color = reader_color or C.INFO
        return Succession(
            self.container.animate.set_stroke(color=color, width=3),
            self.container.animate.set_stroke(color=C.SHARED_RESOURCE, width=2),
            run_time=T.FAST
        )
    
    def animate_write(self, new_value: str, writer_color=None):
        """Animate write access"""
        color = writer_color or C.WARNING
        self.value = new_value
        
        new_display = Text(
            new_value,
            font=F.CODE,
            color=C.TEXT_PRIMARY
        ).scale(F.SIZE_BODY)
        new_display.move_to(self.container.get_center())
        
        return Succession(
            self.container.animate.set_fill(color=color, opacity=0.3),
            Transform(self.value_display, new_display),
            self.container.animate.set_fill(color=C.SHARED_RESOURCE, opacity=0.15),
            run_time=T.NORMAL
        )
    
    def animate_corrupt(self):
        """Animate data corruption due to race"""
        corrupt_display = Text(
            "???",
            font=F.CODE,
            color=C.ERROR
        ).scale(F.SIZE_BODY)
        corrupt_display.move_to(self.container.get_center())
        
        return Succession(
            Flash(self.container, color=C.ERROR, line_length=0.2),
            self.container.animate.set_fill(color=C.ERROR, opacity=0.3),
            Transform(self.value_display, corrupt_display)
        )


class ProtectedRegion(VGroup):
    """
    Region protected by a specific lock.
    """
    
    def __init__(
        self,
        resources: list,
        lock_label: str = "Lock",
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.resources = VGroup(*resources)
        
        # Calculate bounding box
        self.resources.arrange(RIGHT, buff=L.SPACING_MD)
        
        # Protection boundary
        padding = 0.3
        self.boundary = RoundedRectangle(
            width=self.resources.width + padding * 2,
            height=self.resources.height + padding * 2,
            color=C.SAFE_SECTION,
            fill_opacity=0.05,
            stroke_width=1,
            stroke_opacity=0.5,
            corner_radius=0.1
        )
        self.boundary.move_to(self.resources.get_center())
        
        # Lock indicator
        self.lock_indicator = Text(
            f"🔒 {lock_label}",
            font=F.CODE,
            color=C.SAFE_SECTION
        ).scale(F.SIZE_TINY)
        self.lock_indicator.next_to(self.boundary, UP, buff=L.SPACING_TIGHT)
        
        self.add(self.boundary, self.resources, self.lock_indicator)


class DataCell(VGroup):
    """
    Single data cell (for fine-grained locking demos).
    """
    
    def __init__(
        self,
        cell_id: str,
        value: str = "",
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.cell_id = cell_id
        self.value = value
        self.locked_by = None
        
        # Cell body
        self.body = Square(
            side_length=0.6,
            color=C.TEXT_SECONDARY,
            fill_opacity=0.1,
            stroke_width=1
        )
        
        # Cell ID
        self.id_label = Text(
            cell_id,
            font=F.CODE,
            color=C.TEXT_TERTIARY
        ).scale(F.SIZE_TINY)
        self.id_label.next_to(self.body, UP, buff=0.05)
        
        # Value
        self.value_text = Text(
            value,
            font=F.CODE,
            color=C.TEXT_PRIMARY
        ).scale(F.SIZE_LABEL)
        self.value_text.move_to(self.body.get_center())
        
        self.add(self.body, self.id_label, self.value_text)
    
    def animate_lock(self, thread_color):
        """Animate locking this cell"""
        return self.body.animate.set_stroke(color=thread_color, width=3)
    
    def animate_unlock(self):
        """Animate unlocking this cell"""
        return self.body.animate.set_stroke(color=C.TEXT_SECONDARY, width=1)
    
    def animate_access(self, color, is_write: bool = False):
        """Animate access to cell"""
        if is_write:
            return self.body.animate.set_fill(color=color, opacity=0.4)
        else:
            return self.body.animate.set_fill(color=color, opacity=0.2)
