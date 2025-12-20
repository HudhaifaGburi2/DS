"""
B-Tree Evolution Animation - Reusable Components
=================================================

Modular visual components for disk blocks, index entries, and tree nodes.
"""

from manim import *
from config import C, T, S, F, A

# ══════════════════════════════════════════════════════════════════════════════
# DISK BLOCK COMPONENT
# ══════════════════════════════════════════════════════════════════════════════

class DiskBlock(VGroup):
    """
    Visual representation of a disk block with records.
    
    Features:
    - Block container with address label
    - Record slots that can be filled
    - Write animation with "heavy" disk feel
    - Read animation with highlight
    """
    
    def __init__(
        self,
        block_id: int,
        records: list = None,
        max_records: int = 3,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.block_id = block_id
        self.max_records = max_records
        self.record_objects = []
        
        # Block container
        self.container = RoundedRectangle(
            width=S.DISK_BLOCK_WIDTH,
            height=S.DISK_BLOCK_HEIGHT,
            color=C.DISK_BLOCK,
            fill_opacity=A.DIMMED,
            corner_radius=0.1,
            stroke_width=2
        )
        
        # Block address label
        self.address_label = Text(
            f"Block {block_id}",
            font=F.CODE_FONT,
            font_size=F.CAPTION,
            color=C.POINTER
        )
        self.address_label.next_to(self.container, DOWN, buff=0.1)
        
        # Record slots
        self.slots = VGroup()
        slot_height = (S.DISK_BLOCK_HEIGHT - 0.3) / max_records
        for i in range(max_records):
            slot = Rectangle(
                width=S.DISK_BLOCK_WIDTH - 0.2,
                height=slot_height - 0.05,
                color=C.DISK_SURFACE,
                fill_opacity=A.GHOST,
                stroke_width=1
            )
            y_pos = (S.DISK_BLOCK_HEIGHT / 2 - 0.15) - i * slot_height - slot_height / 2
            slot.move_to(self.container.get_center() + UP * y_pos)
            self.slots.add(slot)
        
        self.add(self.container, self.slots, self.address_label)
        
        # Add initial records
        if records:
            for rec in records:
                self._add_record_internal(rec)
    
    def _add_record_internal(self, record_value):
        """Add record without animation"""
        if len(self.record_objects) >= self.max_records:
            return
        
        slot_idx = len(self.record_objects)
        record = Text(
            str(record_value),
            font=F.CODE_FONT,
            font_size=F.DATA_SIZE,
            color=C.DATA
        )
        record.move_to(self.slots[slot_idx].get_center())
        self.record_objects.append(record)
        self.add(record)
    
    def animate_write(self, record_value) -> AnimationGroup:
        """Animate writing a record to disk (heavy, slow feel)"""
        if len(self.record_objects) >= self.max_records:
            return Wait(0)
        
        slot_idx = len(self.record_objects)
        
        record = Text(
            str(record_value),
            font=F.CODE_FONT,
            font_size=F.DATA_SIZE,
            color=C.DATA
        )
        record.move_to(UP * 3)  # Start from top
        
        target_pos = self.slots[slot_idx].get_center()
        self.record_objects.append(record)
        self.add(record)
        
        return AnimationGroup(
            record.animate.move_to(target_pos),
            self.slots[slot_idx].animate.set_fill(color=C.DATA, opacity=A.DIMMED),
            run_time=T.DISK_WRITE,
            rate_func=A.EASE_OUT
        )
    
    def animate_read(self) -> AnimationGroup:
        """Animate reading from disk"""
        return AnimationGroup(
            self.container.animate.set_stroke(color=C.HIGHLIGHT, width=S.HIGHLIGHT_STROKE),
            Flash(self.container, color=C.HIGHLIGHT, line_length=0.2),
            run_time=T.DISK_READ
        )
    
    def animate_highlight(self) -> Animation:
        """Highlight this block"""
        return self.container.animate.set_stroke(color=C.SELECTED, width=S.HIGHLIGHT_STROKE)


# ══════════════════════════════════════════════════════════════════════════════
# INDEX ENTRY COMPONENT
# ══════════════════════════════════════════════════════════════════════════════

class IndexEntry(VGroup):
    """
    Index table entry with key and block pointer.
    
    Features:
    - Key cell with value
    - Pointer cell with block address
    - Highlight animations
    - Pointer arrow animation
    """
    
    def __init__(
        self,
        key: int,
        block_addr: int,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.key = key
        self.block_addr = block_addr
        
        # Key cell
        self.key_cell = Rectangle(
            width=S.INDEX_CELL_WIDTH,
            height=S.INDEX_CELL_HEIGHT,
            color=C.KEY,
            fill_opacity=A.FADED,
            stroke_width=1
        )
        self.key_text = Text(
            str(key),
            font=F.CODE_FONT,
            font_size=F.KEY_SIZE,
            color=C.KEY
        )
        self.key_text.move_to(self.key_cell)
        
        # Pointer cell
        self.ptr_cell = Rectangle(
            width=S.INDEX_CELL_WIDTH,
            height=S.INDEX_CELL_HEIGHT,
            color=C.POINTER,
            fill_opacity=A.GHOST,
            stroke_width=1
        )
        self.ptr_cell.next_to(self.key_cell, RIGHT, buff=0)
        
        self.ptr_text = Text(
            f"→{block_addr}",
            font=F.CODE_FONT,
            font_size=F.POINTER_SIZE,
            color=C.POINTER
        )
        self.ptr_text.move_to(self.ptr_cell)
        
        self.add(self.key_cell, self.key_text, self.ptr_cell, self.ptr_text)
    
    def animate_highlight(self, color=None) -> Animation:
        """Highlight this entry"""
        color = color or C.HIGHLIGHT
        return AnimationGroup(
            self.key_cell.animate.set_fill(color=color, opacity=A.NORMAL),
            self.key_text.animate.set_color(WHITE),
            run_time=T.FAST
        )
    
    def animate_unhighlight(self) -> Animation:
        """Remove highlight"""
        return AnimationGroup(
            self.key_cell.animate.set_fill(color=C.KEY, opacity=A.FADED),
            self.key_text.animate.set_color(C.KEY),
            run_time=T.QUICK
        )
    
    def animate_pointer_jump(self, target: DiskBlock) -> AnimationGroup:
        """Animate pointer jumping to disk block"""
        arrow = Arrow(
            self.ptr_cell.get_right(),
            target.container.get_left(),
            color=C.POINTER,
            stroke_width=S.ARROW_STROKE,
            buff=0.1
        )
        return AnimationGroup(
            GrowArrow(arrow),
            target.animate_highlight(),
            run_time=T.NORMAL
        )


# ══════════════════════════════════════════════════════════════════════════════
# INDEX TABLE COMPONENT
# ══════════════════════════════════════════════════════════════════════════════

class IndexTable(VGroup):
    """
    Complete index table with header and sorted entries.
    
    Features:
    - Header row
    - Sorted entry rows
    - Binary search animation
    """
    
    def __init__(
        self,
        entries: list,  # List of (key, block_addr) tuples
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # Sort entries by key
        self.entries_data = sorted(entries, key=lambda x: x[0])
        
        # Header
        self.header = VGroup(
            Text("Key", font=F.MAIN_FONT, font_size=F.LABEL, color=C.KEY),
            Text("Block", font=F.MAIN_FONT, font_size=F.LABEL, color=C.POINTER)
        )
        self.header.arrange(RIGHT, buff=0.8)
        
        # Entry objects
        self.entries = VGroup()
        for i, (key, addr) in enumerate(self.entries_data):
            entry = IndexEntry(key, addr)
            entry.shift(DOWN * (i + 1) * (S.INDEX_CELL_HEIGHT + S.INDEX_ROW_SPACING))
            self.entries.add(entry)
        
        # Align entries under header
        entries_group = VGroup(self.header, self.entries)
        entries_group.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        
        self.add(self.header, self.entries)
    
    def animate_binary_search(self, target_key: int, scene) -> IndexEntry:
        """
        Perform animated binary search.
        Returns the found entry or None.
        """
        low, high = 0, len(self.entries) - 1
        found_entry = None
        
        while low <= high:
            mid = (low + high) // 2
            mid_entry = self.entries[mid]
            
            # Highlight search range
            range_indicator = SurroundingRectangle(
                VGroup(*[self.entries[i] for i in range(low, high + 1)]),
                color=C.SEARCH_PATH,
                buff=0.1
            )
            scene.play(Create(range_indicator), run_time=T.FAST)
            
            # Highlight middle
            scene.play(mid_entry.animate_highlight(C.SELECTED))
            scene.wait(T.BEAT)
            
            if mid_entry.key == target_key:
                found_entry = mid_entry
                scene.play(FadeOut(range_indicator))
                break
            elif mid_entry.key < target_key:
                low = mid + 1
            else:
                high = mid - 1
            
            scene.play(
                mid_entry.animate_unhighlight(),
                FadeOut(range_indicator),
                run_time=T.FAST
            )
        
        return found_entry


# ══════════════════════════════════════════════════════════════════════════════
# B-TREE NODE COMPONENT
# ══════════════════════════════════════════════════════════════════════════════

class BTreeNode(VGroup):
    """
    B-Tree/B+ Tree node with multiple keys.
    
    Features:
    - Variable number of keys
    - Leaf vs internal styling
    - Split animation
    - Key promotion animation
    - Child pointer slots
    """
    
    def __init__(
        self,
        keys: list,
        is_leaf: bool = False,
        order: int = 4,
        show_pointers: bool = True,
        has_data: bool = None,  # For B+ trees: only leaves have data
        **kwargs
    ):
        super().__init__(**kwargs)
        self.keys = list(keys)
        self.is_leaf = is_leaf
        self.order = order
        self.show_pointers = show_pointers
        self.has_data = has_data if has_data is not None else is_leaf
        self.children = []
        self.child_edges = []
        
        self._build_node()
    
    def _build_node(self):
        """Build visual representation"""
        num_keys = len(self.keys)
        
        # Calculate width
        key_width = S.NODE_KEY_WIDTH
        total_width = num_keys * key_width + (num_keys - 1) * S.NODE_KEY_SPACING + 2 * S.NODE_PADDING
        
        # Background
        node_color = C.LEAF_NODE if self.is_leaf else C.INTERNAL_NODE
        self.bg = RoundedRectangle(
            width=total_width,
            height=S.NODE_KEY_HEIGHT + S.NODE_PADDING,
            color=node_color,
            fill_opacity=A.DIMMED,
            corner_radius=0.08,
            stroke_width=2
        )
        self.add(self.bg)
        
        # Key cells and values
        self.key_cells = VGroup()
        self.key_texts = VGroup()
        
        start_x = -total_width / 2 + S.NODE_PADDING + key_width / 2
        
        for i, key in enumerate(self.keys):
            # Cell
            cell = Rectangle(
                width=key_width,
                height=S.NODE_KEY_HEIGHT,
                color=C.KEY,
                fill_opacity=A.GHOST,
                stroke_width=1
            )
            x_pos = start_x + i * (key_width + S.NODE_KEY_SPACING)
            cell.move_to(self.bg.get_center() + RIGHT * x_pos)
            self.key_cells.add(cell)
            
            # Key text
            key_text = Text(
                str(key),
                font=F.CODE_FONT,
                font_size=F.KEY_SIZE,
                color=C.KEY
            )
            key_text.move_to(cell)
            self.key_texts.add(key_text)
        
        self.add(self.key_cells, self.key_texts)
        
        # Leaf indicator
        if self.is_leaf:
            self.leaf_indicator = Text(
                "●",
                font_size=F.TINY,
                color=C.DATA
            )
            self.leaf_indicator.next_to(self.bg, DOWN, buff=0.05)
            self.add(self.leaf_indicator)
        
        # Pointer slots (for internal nodes)
        if not self.is_leaf and self.show_pointers:
            self.pointer_slots = VGroup()
            for i in range(num_keys + 1):
                slot = Dot(radius=0.08, color=C.POINTER, fill_opacity=A.NORMAL)
                if i == 0:
                    slot.move_to(self.bg.get_bottom() + LEFT * (total_width / 2 - 0.15))
                elif i == num_keys:
                    slot.move_to(self.bg.get_bottom() + RIGHT * (total_width / 2 - 0.15))
                else:
                    # Between keys
                    x_pos = start_x + (i - 0.5) * (key_width + S.NODE_KEY_SPACING)
                    slot.move_to(self.bg.get_bottom() + RIGHT * x_pos)
                self.pointer_slots.add(slot)
            self.add(self.pointer_slots)
    
    def get_pointer_position(self, index: int) -> np.ndarray:
        """Get position of pointer slot at given index"""
        if hasattr(self, 'pointer_slots') and index < len(self.pointer_slots):
            return self.pointer_slots[index].get_center()
        return self.bg.get_bottom()
    
    def animate_insert_key(self, key: int, position: int = None) -> AnimationGroup:
        """Animate inserting a key"""
        if position is None:
            position = len(self.keys)
        
        # Create new key visual
        new_key = Text(
            str(key),
            font=F.CODE_FONT,
            font_size=F.KEY_SIZE,
            color=C.PROMOTED
        )
        new_key.move_to(UP * 2)
        
        # Target position (will need to rebuild node after)
        target = self.bg.get_center()
        
        return AnimationGroup(
            FadeIn(new_key),
            new_key.animate.move_to(target),
            self.bg.animate.set_stroke(color=C.HIGHLIGHT),
            run_time=T.INSERT
        )
    
    def animate_overflow(self) -> Animation:
        """Show overflow state"""
        return AnimationGroup(
            self.bg.animate.set_stroke(color=C.ERROR, width=S.HIGHLIGHT_STROKE),
            Flash(self.bg, color=C.ERROR, line_length=0.2),
            run_time=T.FAST
        )
    
    def animate_highlight_key(self, index: int) -> Animation:
        """Highlight a specific key"""
        if index < len(self.key_cells):
            return AnimationGroup(
                self.key_cells[index].animate.set_fill(color=C.SELECTED, opacity=A.NORMAL),
                self.key_texts[index].animate.set_color(WHITE).scale(A.HIGHLIGHT_SCALE),
                run_time=T.FAST
            )
        return Wait(0)


# ══════════════════════════════════════════════════════════════════════════════
# B-TREE STRUCTURE
# ══════════════════════════════════════════════════════════════════════════════

class BTree(VGroup):
    """
    Complete B-Tree structure with automatic layout.
    
    Features:
    - Tree building and layout
    - Edge management
    - Split animations
    - Search path highlighting
    """
    
    def __init__(
        self,
        order: int = 4,
        is_bplus: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.order = order
        self.is_bplus = is_bplus
        self.root = None
        self.nodes = VGroup()
        self.edges = VGroup()
        self.leaf_links = VGroup()
        
        self.add(self.edges, self.nodes, self.leaf_links)
    
    def set_root(self, node: BTreeNode):
        """Set the root node"""
        self.root = node
        self.nodes.add(node)
    
    def add_node(self, node: BTreeNode):
        """Add a node to the tree"""
        self.nodes.add(node)
    
    def add_edge(self, parent: BTreeNode, child: BTreeNode, pointer_index: int):
        """Add edge from parent to child"""
        edge = Line(
            parent.get_pointer_position(pointer_index),
            child.bg.get_top(),
            color=C.EDGE,
            stroke_width=S.EDGE_STROKE
        )
        self.edges.add(edge)
        return edge
    
    def add_leaf_link(self, left_leaf: BTreeNode, right_leaf: BTreeNode):
        """Add horizontal link between leaf nodes (B+ tree)"""
        if self.is_bplus:
            link = Arrow(
                left_leaf.bg.get_right(),
                right_leaf.bg.get_left(),
                color=C.LEAF_LINK,
                stroke_width=S.EDGE_STROKE,
                buff=0.1,
                max_tip_length_to_length_ratio=0.15
            )
            self.leaf_links.add(link)
            return link
        return None
    
    def layout_tree(self, root_pos=ORIGIN + UP * 2):
        """
        Automatically layout tree nodes.
        Uses level-order traversal for positioning.
        """
        if not self.root:
            return
        
        self.root.move_to(root_pos)
        
        # Layout would involve recursive positioning
        # For now, manual positioning in scenes


# ══════════════════════════════════════════════════════════════════════════════
# NARRATION BOX
# ══════════════════════════════════════════════════════════════════════════════

class NarrationBox(VGroup):
    """
    Styled narration text box for script lines.
    """
    
    def __init__(
        self,
        text: str,
        width: float = 12,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.text_obj = Text(
            text,
            font=F.MAIN_FONT,
            font_size=F.NARRATION_SIZE,
            color=C.TEXT_NARRATION
        )
        
        # Wrap long text
        if self.text_obj.width > width:
            self.text_obj.scale(width / self.text_obj.width)
        
        self.add(self.text_obj)
    
    @staticmethod
    def create_multiline(lines: list, spacing: float = 0.3) -> VGroup:
        """Create multiple narration lines"""
        narrations = VGroup()
        for line in lines:
            narration = NarrationBox(line)
            narrations.add(narration)
        narrations.arrange(DOWN, buff=spacing, aligned_edge=LEFT)
        return narrations


# ══════════════════════════════════════════════════════════════════════════════
# DISK SURFACE
# ══════════════════════════════════════════════════════════════════════════════

class DiskSurface(VGroup):
    """
    Visual representation of disk storage area.
    """
    
    def __init__(
        self,
        num_blocks: int = 4,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # Disk surface background
        self.surface = RoundedRectangle(
            width=num_blocks * (S.DISK_BLOCK_WIDTH + S.DISK_BLOCK_SPACING) + 0.5,
            height=S.DISK_BLOCK_HEIGHT + 0.8,
            color=C.DISK_SURFACE,
            fill_opacity=A.FADED,
            corner_radius=0.15
        )
        
        # Disk label
        self.label = Text(
            "DISK",
            font=F.MAIN_FONT,
            font_size=F.LABEL,
            color=C.TEXT_SECONDARY
        )
        self.label.next_to(self.surface, UP, buff=0.1)
        
        self.add(self.surface, self.label)
        
        # Block slots
        self.blocks = VGroup()
        for i in range(num_blocks):
            block = DiskBlock(i + 1)
            x_pos = -self.surface.width / 2 + 0.5 + i * (S.DISK_BLOCK_WIDTH + S.DISK_BLOCK_SPACING) + S.DISK_BLOCK_WIDTH / 2
            block.move_to(self.surface.get_center() + RIGHT * x_pos)
            self.blocks.add(block)
        
        self.add(self.blocks)


# ══════════════════════════════════════════════════════════════════════════════
# MEMORY REGION
# ══════════════════════════════════════════════════════════════════════════════

class MemoryRegion(VGroup):
    """
    Visual representation of memory area.
    """
    
    def __init__(
        self,
        width: float = 6,
        height: float = 2,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.region = RoundedRectangle(
            width=width,
            height=height,
            color=C.MEMORY,
            fill_opacity=A.GHOST,
            corner_radius=0.1,
            stroke_width=2
        )
        
        self.label = Text(
            "MEMORY",
            font=F.MAIN_FONT,
            font_size=F.LABEL,
            color=C.MEMORY
        )
        self.label.next_to(self.region, UP, buff=0.1)
        
        self.add(self.region, self.label)
