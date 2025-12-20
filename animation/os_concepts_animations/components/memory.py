"""
Memory Components
=================

Visual representations of shared memory, snapshots, and versions.
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import C, T, F, L, A, OS


class MemoryCell(VGroup):
    """
    Single memory cell with address and value.
    """
    
    def __init__(
        self,
        address: str,
        value: str = "",
        width: float = 1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.address = address
        self.value = value
        
        # Cell container
        self.container = Rectangle(
            width=width,
            height=0.6,
            color=C.TEXT_SECONDARY,
            fill_opacity=0.1,
            stroke_width=1
        )
        
        # Address label
        self.addr_label = Text(
            address,
            font=F.CODE,
            color=C.TEXT_TERTIARY
        ).scale(F.SIZE_TINY)
        self.addr_label.next_to(self.container, LEFT, buff=L.SPACING_TIGHT)
        
        # Value
        self.value_text = Text(
            value,
            font=F.CODE,
            color=C.TEXT_PRIMARY
        ).scale(F.SIZE_LABEL)
        self.value_text.move_to(self.container.get_center())
        
        self.add(self.container, self.addr_label, self.value_text)
    
    def animate_write(self, new_value: str, color=None):
        """Animate writing new value"""
        color = color or C.WARNING
        self.value = new_value
        
        new_text = Text(
            new_value,
            font=F.CODE,
            color=C.TEXT_PRIMARY
        ).scale(F.SIZE_LABEL)
        new_text.move_to(self.container.get_center())
        
        return Succession(
            self.container.animate.set_fill(color=color, opacity=0.3),
            Transform(self.value_text, new_text),
            self.container.animate.set_fill(opacity=0.1)
        )
    
    def animate_read(self, color=None):
        """Animate read access"""
        color = color or C.INFO
        return Succession(
            self.container.animate.set_stroke(color=color, width=2),
            self.container.animate.set_stroke(color=C.TEXT_SECONDARY, width=1)
        )


class SnapshotView(VGroup):
    """
    Visual snapshot of memory state at a point in time.
    """
    
    def __init__(
        self,
        snapshot_id: str,
        cells: dict,  # {address: value}
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.snapshot_id = snapshot_id
        
        # Snapshot container
        self.container = RoundedRectangle(
            width=2.5,
            height=len(cells) * 0.5 + 0.6,
            color=C.SNAPSHOT,
            fill_opacity=0.1,
            stroke_width=2,
            corner_radius=0.12
        )
        
        # Snapshot label
        self.label = Text(
            f"Snapshot {snapshot_id}",
            font=F.CODE,
            color=C.SNAPSHOT
        ).scale(F.SIZE_TINY)
        self.label.next_to(self.container, UP, buff=L.SPACING_TIGHT)
        
        # Timestamp indicator
        self.timestamp = Text(
            f"@t{snapshot_id}",
            font=F.CODE,
            color=C.TIME_MARKER
        ).scale(F.SIZE_TINY)
        self.timestamp.next_to(self.label, RIGHT, buff=L.SPACING_SM)
        
        # Memory cells
        self.cells = VGroup()
        for i, (addr, val) in enumerate(cells.items()):
            cell = MemoryCell(addr, val, width=1.8)
            cell.scale(0.7)
            self.cells.add(cell)
        
        self.cells.arrange(DOWN, buff=0.1)
        self.cells.move_to(self.container.get_center())
        
        self.add(self.container, self.label, self.timestamp, self.cells)
    
    def animate_create(self):
        """Animate snapshot creation"""
        return Succession(
            FadeIn(self.container, scale=0.9),
            Write(self.label),
            Write(self.timestamp),
            LaggedStart(
                *[FadeIn(cell) for cell in self.cells],
                lag_ratio=0.1
            )
        )
    
    def animate_pin(self):
        """Animate reader pinning to snapshot"""
        return self.container.animate.set_stroke(color=C.SNAPSHOT, width=3)
    
    def animate_release(self):
        """Animate snapshot release"""
        return self.container.animate.set_stroke(color=C.SNAPSHOT, width=2).set_opacity(0.5)


class VersionChain(VGroup):
    """
    Chain of versions for a single data item (MVCC).
    """
    
    def __init__(
        self,
        item_name: str,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.item_name = item_name
        self.versions = []
        
        # Item label
        self.label = Text(
            item_name,
            font=F.CODE,
            color=C.SHARED_RESOURCE
        ).scale(F.SIZE_LABEL)
        
        # Version container
        self.version_group = VGroup()
        
        self.add(self.label, self.version_group)
    
    def add_version(
        self,
        version_num: int,
        value: str,
        is_current: bool = True
    ) -> VGroup:
        """Add a new version to the chain"""
        # Mark previous as old
        if self.versions and is_current:
            prev = self.versions[-1]
            prev.is_current = False
        
        # Version box
        color = C.VERSION_NEW if is_current else C.VERSION_OLD
        opacity = 0.4 if is_current else 0.2
        
        box = RoundedRectangle(
            width=0.8,
            height=0.5,
            color=color,
            fill_opacity=opacity,
            stroke_width=2,
            corner_radius=0.08
        )
        
        # Version number
        v_label = Text(
            f"v{version_num}",
            font=F.CODE,
            color=color
        ).scale(F.SIZE_TINY)
        v_label.next_to(box, UP, buff=0.03)
        
        # Value
        v_value = Text(
            value,
            font=F.CODE,
            color=C.TEXT_PRIMARY
        ).scale(F.SIZE_TINY)
        v_value.move_to(box.get_center())
        
        version = VGroup(box, v_label, v_value)
        version.version_num = version_num
        version.value = value
        version.is_current = is_current
        
        self.versions.append(version)
        self.version_group.add(version)
        
        # Rearrange
        self.version_group.arrange(RIGHT, buff=0.3)
        self.label.next_to(self.version_group, LEFT, buff=L.SPACING_MD)
        
        return version
    
    def animate_add_version(self, version: VGroup):
        """Animate adding new version"""
        return FadeIn(version, shift=RIGHT * 0.3, scale=0.8)
    
    def get_current_version(self) -> VGroup:
        """Get current version"""
        for v in reversed(self.versions):
            if v.is_current:
                return v
        return self.versions[-1] if self.versions else None


class SharedVariable(VGroup):
    """
    Shared variable with versioning support.
    """
    
    def __init__(
        self,
        name: str,
        initial_value: str,
        show_versions: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.name = name
        self.current_value = initial_value
        self.show_versions = show_versions
        self.version_num = 0
        
        # Variable container
        self.container = RoundedRectangle(
            width=1.5,
            height=0.8,
            color=C.SHARED_RESOURCE,
            fill_opacity=0.15,
            stroke_width=2,
            corner_radius=0.1
        )
        
        # Name
        self.name_label = Text(
            name,
            font=F.CODE,
            color=C.SHARED_RESOURCE
        ).scale(F.SIZE_LABEL)
        self.name_label.next_to(self.container, UP, buff=L.SPACING_TIGHT)
        
        # Current value
        self.value_display = Text(
            initial_value,
            font=F.CODE,
            color=C.TEXT_PRIMARY
        ).scale(F.SIZE_BODY)
        self.value_display.move_to(self.container.get_center())
        
        self.add(self.container, self.name_label, self.value_display)
        
        # Version indicator
        if show_versions:
            self.version_label = Text(
                f"v{self.version_num}",
                font=F.CODE,
                color=C.VERSION_CURRENT
            ).scale(F.SIZE_TINY)
            self.version_label.next_to(self.container, DOWN, buff=L.SPACING_TIGHT)
            self.add(self.version_label)
    
    def animate_update(self, new_value: str, writer_color=None):
        """Animate value update (with optional new version)"""
        self.current_value = new_value
        self.version_num += 1
        color = writer_color or C.IO_WRITE
        
        new_display = Text(
            new_value,
            font=F.CODE,
            color=C.TEXT_PRIMARY
        ).scale(F.SIZE_BODY)
        new_display.move_to(self.container.get_center())
        
        animations = [
            self.container.animate.set_fill(color=color, opacity=0.3),
            Transform(self.value_display, new_display),
        ]
        
        if self.show_versions:
            new_v_label = Text(
                f"v{self.version_num}",
                font=F.CODE,
                color=C.VERSION_NEW
            ).scale(F.SIZE_TINY)
            new_v_label.next_to(self.container, DOWN, buff=L.SPACING_TIGHT)
            animations.append(Transform(self.version_label, new_v_label))
        
        return Succession(
            AnimationGroup(*animations),
            self.container.animate.set_fill(opacity=0.15)
        )
    
    def animate_read_snapshot(self, snapshot_value: str, reader_color=None):
        """Show that reader sees snapshot value"""
        color = reader_color or C.SNAPSHOT
        
        # Ghost of old value
        ghost = Text(
            snapshot_value,
            font=F.CODE,
            color=color
        ).scale(F.SIZE_BODY)
        ghost.move_to(self.value_display.get_center() + UP * 0.5)
        ghost.set_opacity(0.6)
        
        return Succession(
            FadeIn(ghost, shift=DOWN * 0.2),
            Wait(T.BEAT),
            FadeOut(ghost, shift=UP * 0.2)
        )
