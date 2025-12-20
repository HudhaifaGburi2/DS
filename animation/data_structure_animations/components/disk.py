"""
Disk Components for Storage Visualizations
==========================================

Provides disk and persistent storage visualizations:
- DiskPage: Single disk page/block
- SSTable: Sorted String Table (LSM)
- DiskBlock: Generic disk block
- StorageLevel: LSM level container
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import C, T, F, L, DS, A


class DiskPage(VGroup):
    """
    Single disk page visualization.
    
    Visual: Page-like rectangle with fold corner.
    """
    
    def __init__(
        self,
        page_id: str = "",
        width: float = None,
        height: float = None,
        color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.page_id = page_id
        self.width = width or DS.PAGE_WIDTH
        self.height = height or DS.PAGE_HEIGHT
        self.color = color or C.DISK_SSD
        
        # Page body
        self.body = RoundedRectangle(
            width=self.width,
            height=self.height,
            corner_radius=DS.PAGE_CORNER_RADIUS,
            fill_color=self.color,
            fill_opacity=0.15,
            stroke_color=self.color,
            stroke_width=2
        )
        self.add(self.body)
        
        # Fold corner (top-right)
        fold_size = 0.2
        fold_corner = Polygon(
            self.body.get_corner(UR),
            self.body.get_corner(UR) + LEFT * fold_size,
            self.body.get_corner(UR) + DOWN * fold_size,
            fill_color=self.color,
            fill_opacity=0.3,
            stroke_color=self.color,
            stroke_width=1
        )
        self.add(fold_corner)
        
        # Page ID label
        if page_id:
            self.label = Text(page_id, font=F.CODE, color=self.color).scale(F.SIZE_TINY)
            self.label.move_to(self.body.get_corner(DL) + RIGHT * 0.2 + UP * 0.15)
            self.add(self.label)
        
        # Content area
        self.content_area = Rectangle(
            width=self.width - 0.2,
            height=self.height - 0.4,
            fill_opacity=0,
            stroke_width=0
        )
        self.content_area.move_to(self.body.get_center() + DOWN * 0.1)
        self.entries = VGroup()
        self.add(self.entries)
    
    def add_entry(self, key: str, highlight: bool = False):
        """Add key entry to page"""
        color = C.BTREE_KEY_ACTIVE if highlight else C.TEXT_PRIMARY
        entry = Text(key, font=F.CODE, color=color).scale(F.SIZE_KEY)
        
        # Stack entries
        row = len(self.entries)
        entry.move_to(
            self.content_area.get_top() + 
            DOWN * (0.2 + row * 0.25)
        )
        self.entries.add(entry)
        return entry
    
    def animate_read(self):
        """Animate page read operation"""
        return Succession(
            self.body.animate.set_fill(color=C.IO_READ, opacity=0.4),
            Wait(T.QUICK),
            self.body.animate.set_fill(color=self.color, opacity=0.15)
        )
    
    def animate_write(self):
        """Animate page write operation"""
        return Succession(
            self.body.animate.set_fill(color=C.IO_WRITE, opacity=0.4),
            Wait(T.QUICK),
            self.body.animate.set_fill(color=self.color, opacity=0.15)
        )


class SSTable(VGroup):
    """
    Sorted String Table visualization for LSM-Tree.
    
    Visual: Horizontal block representing immutable sorted file.
    """
    
    def __init__(
        self,
        table_id: str = "",
        width: float = None,
        height: float = None,
        level: int = 0,
        key_range: tuple = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.table_id = table_id
        self.width = width or DS.LSM_SSTABLE_WIDTH
        self.height = height or DS.LSM_SSTABLE_HEIGHT
        self.level = level
        self.key_range = key_range
        
        # Color based on level
        level_colors = [
            C.LSM_SSTABLE_L0,
            C.LSM_SSTABLE_L1,
            C.LSM_SSTABLE_L2,
            C.LSM_SSTABLE_L3,
        ]
        self.color = level_colors[min(level, len(level_colors) - 1)]
        
        # SSTable body
        self.body = RoundedRectangle(
            width=self.width,
            height=self.height,
            corner_radius=0.06,
            fill_color=self.color,
            fill_opacity=0.25,
            stroke_color=self.color,
            stroke_width=2
        )
        self.add(self.body)
        
        # Table ID
        if table_id:
            self.id_label = Text(table_id, font=F.CODE, color=self.color).scale(F.SIZE_TINY)
            self.id_label.move_to(self.body.get_left() + RIGHT * 0.25)
            self.add(self.id_label)
        
        # Key range indicator
        if key_range:
            range_text = f"[{key_range[0]}..{key_range[1]}]"
            self.range_label = Text(
                range_text, 
                font=F.CODE, 
                color=C.TEXT_SECONDARY
            ).scale(F.SIZE_TINY)
            self.range_label.move_to(self.body.get_center())
            self.add(self.range_label)
        
        # Sorted indicator (ascending bars)
        self.sorted_indicator = self._create_sorted_indicator()
        self.sorted_indicator.move_to(self.body.get_right() + LEFT * 0.3)
        self.add(self.sorted_indicator)
    
    def _create_sorted_indicator(self):
        """Create visual indicating sorted data"""
        indicator = VGroup()
        for i in range(3):
            bar = Rectangle(
                width=0.06,
                height=0.1 + i * 0.08,
                fill_color=self.color,
                fill_opacity=0.5,
                stroke_width=0
            )
            bar.shift(RIGHT * i * 0.1)
            indicator.add(bar)
        indicator.arrange(RIGHT, buff=0.02, aligned_edge=DOWN)
        return indicator
    
    def animate_create(self):
        """Animate SSTable creation (flush from memory)"""
        return FadeIn(self, shift=DOWN * 0.3, scale=0.9)
    
    def animate_compact(self):
        """Animate compaction (being processed)"""
        return self.body.animate.set_fill(color=C.LSM_COMPACTION, opacity=0.5)
    
    def animate_delete(self):
        """Animate SSTable deletion after compaction"""
        return FadeOut(self, shift=DOWN * 0.2, scale=0.8)


class DiskBlock(VGroup):
    """
    Generic disk block visualization.
    
    Visual: Square block representing disk storage unit.
    """
    
    def __init__(
        self,
        block_id: str = "",
        size: float = 0.8,
        color=None,
        used: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.block_id = block_id
        self.size = size
        self.color = color or C.DISK_SSD
        self.used = used
        
        # Block
        fill_opacity = 0.3 if used else 0.05
        self.block = Square(
            side_length=size,
            fill_color=self.color,
            fill_opacity=fill_opacity,
            stroke_color=self.color,
            stroke_width=1
        )
        self.add(self.block)
        
        # Block ID
        if block_id:
            self.label = Text(block_id, font=F.CODE, color=self.color).scale(F.SIZE_TINY)
            self.label.move_to(self.block.get_center())
            self.add(self.label)
    
    def animate_allocate(self):
        """Animate block allocation"""
        self.used = True
        return self.block.animate.set_fill(opacity=0.3)
    
    def animate_free(self):
        """Animate block deallocation"""
        self.used = False
        return self.block.animate.set_fill(opacity=0.05)


class StorageLevel(VGroup):
    """
    LSM-Tree storage level visualization.
    
    Visual: Container for SSTables at a specific level.
    """
    
    def __init__(
        self,
        level: int,
        width: float = 6.0,
        height: float = 0.8,
        max_tables: int = 4,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.level = level
        self.width = width
        self.height = height
        self.max_tables = max_tables
        self.tables = VGroup()
        
        # Level colors
        level_colors = [
            C.LSM_SSTABLE_L0,
            C.LSM_SSTABLE_L1,
            C.LSM_SSTABLE_L2,
            C.LSM_SSTABLE_L3,
        ]
        self.color = level_colors[min(level, len(level_colors) - 1)]
        
        # Level container
        self.container = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.1,
            fill_color=self.color,
            fill_opacity=0.05,
            stroke_color=self.color,
            stroke_width=1,
            stroke_opacity=0.5
        )
        self.add(self.container)
        
        # Level label
        self.label = Text(f"L{level}", font=F.CODE, color=self.color).scale(F.SIZE_LABEL)
        self.label.next_to(self.container, LEFT, buff=L.SPACING_SM)
        self.add(self.label)
        
        # Size indicator
        size_ratio = DS.LSM_SIZE_RATIO ** level
        self.size_label = Text(
            f"×{size_ratio}", 
            font=F.CODE, 
            color=C.TEXT_TERTIARY
        ).scale(F.SIZE_TINY)
        self.size_label.next_to(self.label, DOWN, buff=0.05)
        self.add(self.size_label)
        
        self.add(self.tables)
    
    def add_sstable(self, table: SSTable = None, table_id: str = None):
        """Add SSTable to this level"""
        if table is None:
            table = SSTable(
                table_id=table_id or f"T{len(self.tables)}",
                level=self.level,
                width=DS.LSM_SSTABLE_WIDTH * 0.8,
                height=DS.LSM_SSTABLE_HEIGHT * 0.8
            )
        
        # Position table
        num_tables = len(self.tables)
        spacing = (self.width - 0.4) / self.max_tables
        x_offset = -self.width/2 + 0.3 + spacing/2 + num_tables * spacing
        
        table.move_to(self.container.get_center() + RIGHT * x_offset)
        self.tables.add(table)
        
        return table
    
    def get_compaction_candidates(self, threshold: int = None):
        """Get tables that should be compacted"""
        threshold = threshold or self.max_tables
        if len(self.tables) >= threshold:
            return list(self.tables)
        return []
    
    def animate_compaction_start(self):
        """Visual for starting compaction"""
        return AnimationGroup(
            *[table.animate_compact() for table in self.tables]
        )
    
    def clear_tables(self):
        """Remove all tables from level"""
        self.tables.remove(*self.tables)


class DiskRegion(VGroup):
    """
    Visual representation of disk storage region.
    
    Shows disk icon and storage area.
    """
    
    def __init__(
        self,
        label: str = "Disk",
        width: float = 5.0,
        height: float = 3.0,
        color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.color = color or C.DISK_SSD
        
        # Disk region
        self.region = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.15,
            fill_color=self.color,
            fill_opacity=0.05,
            stroke_color=self.color,
            stroke_width=2
        )
        self.add(self.region)
        
        # Disk icon
        self.disk_icon = self._create_disk_icon()
        self.disk_icon.next_to(self.region, LEFT, buff=L.SPACING_SM)
        self.add(self.disk_icon)
        
        # Label
        self.label = Text(label, font=F.BODY, color=self.color).scale(F.SIZE_CAPTION)
        self.label.next_to(self.region, UP, buff=L.SPACING_TIGHT)
        self.add(self.label)
    
    def _create_disk_icon(self):
        """Create disk/SSD icon"""
        icon = VGroup()
        
        # SSD shape
        body = RoundedRectangle(
            width=0.5,
            height=0.35,
            corner_radius=0.05,
            fill_color=self.color,
            fill_opacity=0.3,
            stroke_color=self.color,
            stroke_width=1
        )
        
        # Connector
        connector = Rectangle(
            width=0.25,
            height=0.08,
            fill_color=self.color,
            fill_opacity=0.5,
            stroke_width=0
        )
        connector.next_to(body, DOWN, buff=0)
        
        icon.add(body, connector)
        return icon
