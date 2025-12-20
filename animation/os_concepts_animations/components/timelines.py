"""
Timeline Components
===================

Visual representations for time-based reasoning (MVCC, scheduling).
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import C, T, F, L, A, OS


class TimeAxis(VGroup):
    """
    Horizontal time axis for temporal animations.
    """
    
    def __init__(
        self,
        start_x: float = -5.5,
        end_x: float = 5.5,
        y_pos: float = -2.5,
        show_ticks: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.start_x = start_x
        self.end_x = end_x
        self.y_pos = y_pos
        
        # Main axis
        self.axis = Arrow(
            start=LEFT * abs(start_x) + UP * y_pos,
            end=RIGHT * abs(end_x) + UP * y_pos,
            color=C.TIME_AXIS,
            stroke_width=A.TIMELINE_STROKE,
            buff=0
        )
        
        # "Time" label
        self.time_label = Text(
            "Time →",
            font=F.CODE,
            color=C.TIME_AXIS
        ).scale(F.SIZE_TINY)
        self.time_label.next_to(self.axis, RIGHT, buff=L.SPACING_TIGHT)
        
        self.add(self.axis, self.time_label)
        
        # Tick marks
        if show_ticks:
            self.ticks = VGroup()
            tick_positions = np.arange(start_x + 1, end_x, L.TIMELINE_TICK_SPACING)
            for i, x in enumerate(tick_positions):
                tick = Line(
                    UP * 0.1 + RIGHT * x + UP * y_pos,
                    DOWN * 0.1 + RIGHT * x + UP * y_pos,
                    color=C.TIME_AXIS,
                    stroke_width=1
                )
                self.ticks.add(tick)
            self.add(self.ticks)
    
    def get_position_at_time(self, t: float) -> np.ndarray:
        """Get position on axis for time t (normalized 0-1)"""
        x = self.start_x + t * (self.end_x - self.start_x)
        return np.array([x, self.y_pos, 0])
    
    def animate_create(self):
        """Animate axis creation"""
        return Succession(
            Create(self.axis),
            FadeIn(self.time_label),
            LaggedStart(
                *[Create(tick) for tick in self.ticks],
                lag_ratio=0.05
            ) if hasattr(self, 'ticks') else Wait(0)
        )


class VersionTimeline(VGroup):
    """
    Timeline for a single object showing version history.
    """
    
    def __init__(
        self,
        object_name: str,
        y_pos: float,
        color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.object_name = object_name
        self.y_pos = y_pos
        self.color = color or C.SHARED_RESOURCE
        self.versions = []
        
        # Object label
        self.label = Text(
            object_name,
            font=F.CODE,
            color=self.color
        ).scale(F.SIZE_LABEL)
        self.label.move_to(LEFT * 6 + UP * y_pos)
        
        # Timeline line
        self.line = Line(
            LEFT * 5 + UP * y_pos,
            RIGHT * 5.5 + UP * y_pos,
            color=self.color,
            stroke_width=1,
            stroke_opacity=0.4
        )
        
        # Version markers container
        self.version_group = VGroup()
        
        self.add(self.label, self.line, self.version_group)
    
    def add_version(
        self,
        version_id: str,
        x_pos: float,
        state: str = "current",
        value: str = None
    ) -> 'VersionMarker':
        """Add version marker to timeline"""
        marker = VersionMarker(
            version_id=version_id,
            state=state,
            value=value
        )
        marker.move_to(RIGHT * x_pos + UP * self.y_pos)
        self.versions.append(marker)
        self.version_group.add(marker)
        return marker
    
    def animate_add_version(self, marker: 'VersionMarker'):
        """Animate adding a new version"""
        return FadeIn(marker, scale=0.5, shift=UP * 0.2)


class VersionMarker(VGroup):
    """
    Single version marker on a timeline.
    """
    
    def __init__(
        self,
        version_id: str,
        state: str = "current",
        value: str = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.version_id = version_id
        self.state = state
        self.value = value
        
        # Determine color by state
        if state == "current":
            self.color = C.VERSION_CURRENT
        elif state == "new":
            self.color = C.VERSION_NEW
        elif state == "old":
            self.color = C.VERSION_OLD
        else:
            self.color = C.GARBAGE
        
        # Version box
        self.box = RoundedRectangle(
            width=0.7,
            height=L.VERSION_HEIGHT,
            color=self.color,
            fill_opacity=0.35,
            stroke_width=2,
            corner_radius=0.08
        )
        
        # Version ID label
        self.id_label = Text(
            version_id,
            font=F.CODE,
            color=self.color
        ).scale(F.SIZE_TINY)
        self.id_label.move_to(self.box.get_center())
        
        self.add(self.box, self.id_label)
        
        # Optional value display
        if value:
            self.value_label = Text(
                value,
                font=F.CODE,
                color=C.TEXT_SECONDARY
            ).scale(F.SIZE_TINY)
            self.value_label.next_to(self.box, DOWN, buff=0.05)
            self.add(self.value_label)
    
    def set_state(self, new_state: str):
        """Update version state"""
        self.state = new_state
        if new_state == "current":
            self.color = C.VERSION_CURRENT
        elif new_state == "new":
            self.color = C.VERSION_NEW
        elif new_state == "old":
            self.color = C.VERSION_OLD
        else:
            self.color = C.GARBAGE
        
        self.box.set_color(self.color)
        self.id_label.set_color(self.color)
    
    def animate_mark_old(self):
        """Animate marking version as old"""
        self.state = "old"
        return AnimationGroup(
            self.box.animate.set_color(C.VERSION_OLD).set_fill(opacity=0.2),
            self.id_label.animate.set_color(C.VERSION_OLD)
        )
    
    def animate_garbage_collect(self):
        """Animate garbage collection of version"""
        return Succession(
            self.animate.set_opacity(0.3),
            self.box.animate.set_fill(color=C.GARBAGE, opacity=0.1),
            FadeOut(self, shift=DOWN * 0.3)
        )


class TransactionSpan(VGroup):
    """
    Visual span showing transaction lifetime on timeline.
    """
    
    def __init__(
        self,
        txn_id: str,
        start_x: float,
        end_x: float,
        y_pos: float,
        color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.txn_id = txn_id
        self.color = color or C.THREAD_1
        
        # Span bar
        self.bar = Rectangle(
            width=end_x - start_x,
            height=0.25,
            color=self.color,
            fill_opacity=0.4,
            stroke_width=1
        )
        self.bar.move_to(RIGHT * (start_x + end_x) / 2 + UP * y_pos)
        
        # Transaction label
        self.label = Text(
            txn_id,
            font=F.CODE,
            color=self.color
        ).scale(F.SIZE_TINY)
        self.label.next_to(self.bar, UP, buff=0.05)
        
        # Start marker
        self.start_marker = Circle(
            radius=0.08,
            color=self.color,
            fill_opacity=1
        )
        self.start_marker.move_to(RIGHT * start_x + UP * y_pos)
        
        # End marker
        self.end_marker = Circle(
            radius=0.08,
            color=self.color,
            fill_opacity=1
        )
        self.end_marker.move_to(RIGHT * end_x + UP * y_pos)
        
        self.add(self.bar, self.label, self.start_marker, self.end_marker)
    
    def animate_create(self):
        """Animate transaction span creation"""
        return Succession(
            FadeIn(self.start_marker, scale=0.5),
            Create(self.bar),
            FadeIn(self.end_marker, scale=0.5),
            FadeIn(self.label)
        )
    
    def animate_commit(self):
        """Animate successful commit"""
        return AnimationGroup(
            self.bar.animate.set_fill(color=C.SUCCESS, opacity=0.5),
            Flash(self.end_marker, color=C.SUCCESS, line_length=0.15)
        )
    
    def animate_abort(self):
        """Animate transaction abort"""
        return AnimationGroup(
            self.bar.animate.set_fill(color=C.ERROR, opacity=0.3),
            self.bar.animate.set_stroke(color=C.ERROR)
        )


class SnapshotPointer(VGroup):
    """
    Visual pointer from reader to snapshot version.
    """
    
    def __init__(
        self,
        reader_name: str,
        target_version: VersionMarker,
        y_offset: float = 0.5,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.reader_name = reader_name
        self.target = target_version
        
        # Reader label
        self.reader = Text(
            reader_name,
            font=F.CODE,
            color=C.SNAPSHOT
        ).scale(F.SIZE_TINY)
        self.reader.move_to(target_version.get_center() + UP * y_offset)
        
        # Pin line
        self.pin = DashedLine(
            self.reader.get_bottom(),
            target_version.get_top(),
            color=C.SNAPSHOT,
            stroke_width=1.5,
            dash_length=0.1
        )
        
        self.add(self.reader, self.pin)
    
    def animate_pin(self):
        """Animate pinning to snapshot"""
        return Succession(
            FadeIn(self.reader, shift=DOWN * 0.2),
            Create(self.pin)
        )
    
    def animate_release(self):
        """Animate releasing snapshot"""
        return FadeOut(self)
