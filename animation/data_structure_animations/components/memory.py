"""
Memory Components for Storage Visualizations
=============================================

Provides RAM and cache visualizations:
- MemoryBuffer: Generic memory buffer
- MemTable: LSM-Tree in-memory table
- CacheBlock: Cache line/block
- RAMRegion: Labeled memory region
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import C, T, F, L, DS, A


class MemoryBuffer(VGroup):
    """
    Generic memory buffer visualization.
    
    Visual: Rectangular region with entries.
    """
    
    def __init__(
        self,
        width: float = None,
        height: float = None,
        color=None,
        label: str = "Buffer",
        num_slots: int = 5,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.width = width or DS.BUFFER_WIDTH
        self.height = height or DS.BUFFER_HEIGHT
        self.color = color or C.MEMORY_RAM
        self.num_slots = num_slots
        self.entries = []
        
        # Main container
        self.container = RoundedRectangle(
            width=self.width,
            height=self.height,
            corner_radius=0.1,
            fill_color=self.color,
            fill_opacity=0.15,
            stroke_color=self.color,
            stroke_width=2
        )
        self.add(self.container)
        
        # Label
        self.label = Text(label, font=F.BODY, color=self.color).scale(F.SIZE_LABEL)
        self.label.next_to(self.container, UP, buff=L.SPACING_TIGHT)
        self.add(self.label)
        
        # Entry slots
        self.slots = VGroup()
        slot_width = (self.width - 0.2) / num_slots
        for i in range(num_slots):
            slot = Rectangle(
                width=slot_width - 0.05,
                height=self.height - 0.2,
                fill_color=self.color,
                fill_opacity=0.05,
                stroke_color=self.color,
                stroke_width=0.5
            )
            x_offset = -self.width/2 + 0.1 + slot_width/2 + i * slot_width
            slot.move_to(self.container.get_center() + RIGHT * x_offset)
            self.slots.add(slot)
        self.add(self.slots)
    
    def add_entry(self, key: str, slot_index: int = None):
        """Add entry to buffer"""
        if slot_index is None:
            slot_index = len(self.entries)
        
        if slot_index < self.num_slots:
            entry = Text(key, font=F.CODE, color=self.color).scale(F.SIZE_KEY)
            entry.move_to(self.slots[slot_index].get_center())
            self.entries.append(entry)
            self.add(entry)
            return entry
        return None
    
    def animate_fill(self, progress: float = 1.0):
        """Animate buffer filling"""
        fill_width = self.width * progress
        fill_rect = Rectangle(
            width=fill_width,
            height=self.height - 0.1,
            fill_color=self.color,
            fill_opacity=0.3,
            stroke_width=0
        )
        fill_rect.align_to(self.container, LEFT)
        fill_rect.shift(RIGHT * 0.05)
        
        return Create(fill_rect)
    
    def animate_flush(self):
        """Animate buffer flush/clear"""
        return AnimationGroup(
            *[FadeOut(entry, shift=DOWN * 0.5) for entry in self.entries],
            self.container.animate.set_fill(opacity=0.05)
        )


class MemTable(VGroup):
    """
    LSM-Tree MemTable visualization.
    
    Visual: Sorted in-memory buffer with write indicator.
    """
    
    def __init__(
        self,
        width: float = None,
        height: float = None,
        color=None,
        max_entries: int = 8,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.width = width or DS.LSM_MEMTABLE_WIDTH
        self.height = height or DS.LSM_MEMTABLE_HEIGHT
        self.color = color or C.LSM_MEMTABLE
        self.max_entries = max_entries
        self.entries = []
        
        # Container with RAM indicator
        self.container = RoundedRectangle(
            width=self.width,
            height=self.height,
            corner_radius=0.12,
            fill_color=self.color,
            fill_opacity=0.2,
            stroke_color=self.color,
            stroke_width=2.5
        )
        self.add(self.container)
        
        # RAM chip icon
        self.ram_icon = self._create_ram_icon()
        self.ram_icon.next_to(self.container, LEFT, buff=L.SPACING_SM)
        self.add(self.ram_icon)
        
        # Label
        self.label = Text("MemTable", font=F.BODY, color=self.color).scale(F.SIZE_LABEL)
        self.label.next_to(self.container, UP, buff=L.SPACING_TIGHT)
        self.add(self.label)
        
        # Write indicator (hot zone)
        self.write_zone = Rectangle(
            width=self.width - 0.1,
            height=0.15,
            fill_color=C.LSM_MEMTABLE_HOT,
            fill_opacity=0.5,
            stroke_width=0
        )
        self.write_zone.align_to(self.container, UP).shift(DOWN * 0.1)
        self.add(self.write_zone)
        
        # Entry container
        self.entry_group = VGroup()
        self.add(self.entry_group)
    
    def _create_ram_icon(self):
        """Create simple RAM chip icon"""
        chip = VGroup()
        body = Rectangle(width=0.3, height=0.5, color=self.color, fill_opacity=0.3)
        
        # Pins
        for i in range(3):
            pin = Line(
                body.get_left() + UP * (0.15 - i * 0.15) + LEFT * 0.1,
                body.get_left() + UP * (0.15 - i * 0.15),
                color=self.color,
                stroke_width=2
            )
            chip.add(pin)
        
        chip.add(body)
        return chip
    
    def insert(self, key: str, value: str = None):
        """Insert key-value into memtable"""
        entry_text = f"{key}" if value is None else f"{key}:{value}"
        entry = Text(entry_text, font=F.CODE, color=C.TEXT_PRIMARY).scale(F.SIZE_KEY)
        
        # Position based on entry count
        row = len(self.entries)
        entry.move_to(
            self.container.get_center() + 
            UP * (self.height/2 - 0.35 - row * 0.25) +
            LEFT * 0.3
        )
        
        self.entries.append(entry)
        self.entry_group.add(entry)
        
        return entry
    
    def animate_insert(self, key: str, value: str = None):
        """Animate insertion with write flash"""
        entry = self.insert(key, value)
        
        return Succession(
            Flash(self.write_zone, color=C.LSM_MEMTABLE_HOT, line_length=0.2),
            FadeIn(entry, shift=DOWN * 0.2)
        )
    
    def is_full(self) -> bool:
        """Check if memtable is at capacity"""
        return len(self.entries) >= self.max_entries
    
    def animate_flush_to_disk(self, target_pos):
        """Animate flushing memtable to SSTable"""
        arrows = []
        for entry in self.entries:
            arrow = Arrow(
                entry.get_center(),
                target_pos,
                color=C.IO_WRITE,
                stroke_width=1.5,
                buff=0.2
            )
            arrows.append(Create(arrow))
        
        return LaggedStart(*arrows, lag_ratio=A.LAG_FAST)


class CacheBlock(VGroup):
    """
    Cache block/line visualization.
    
    Visual: Small rectangular block with hit/miss indicator.
    """
    
    def __init__(
        self,
        label: str = "",
        width: float = 0.8,
        height: float = 0.4,
        color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.label_text = label
        self.width = width
        self.height = height
        self.color = color or C.MEMORY_CACHE
        self.is_cached = False
        
        # Block
        self.block = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.05,
            fill_color=self.color,
            fill_opacity=0.1,
            stroke_color=self.color,
            stroke_width=1.5
        )
        self.add(self.block)
        
        # Label
        if label:
            self.label = Text(label, font=F.CODE, color=self.color).scale(F.SIZE_TINY)
            self.label.move_to(self.block.get_center())
            self.add(self.label)
    
    def animate_cache_hit(self):
        """Flash green for cache hit"""
        return Succession(
            self.block.animate.set_fill(color=C.SUCCESS, opacity=0.5),
            self.block.animate.set_fill(color=self.color, opacity=0.1)
        )
    
    def animate_cache_miss(self):
        """Flash red for cache miss"""
        return Succession(
            self.block.animate.set_fill(color=C.ERROR, opacity=0.5),
            self.block.animate.set_fill(color=self.color, opacity=0.1)
        )


class RAMRegion(VGroup):
    """
    Labeled RAM memory region.
    
    Visual: Large region representing allocated memory.
    """
    
    def __init__(
        self,
        label: str,
        width: float = 4.0,
        height: float = 1.5,
        color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.color = color or C.MEMORY_RAM
        
        # Region background
        self.region = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.15,
            fill_color=self.color,
            fill_opacity=0.1,
            stroke_color=self.color,
            stroke_width=2
        )
        self.add(self.region)
        
        # Label with icon
        self.label = Text(f"🔲 {label}", font=F.BODY, color=self.color).scale(F.SIZE_CAPTION)
        self.label.next_to(self.region, UP, buff=L.SPACING_TIGHT)
        self.add(self.label)
        
        # "RAM" badge
        self.badge = Text("RAM", font=F.CODE, color=self.color).scale(F.SIZE_TINY)
        self.badge.move_to(self.region.get_corner(UR) + LEFT * 0.3 + DOWN * 0.15)
        self.add(self.badge)
