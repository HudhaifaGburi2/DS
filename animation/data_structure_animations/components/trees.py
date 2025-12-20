"""
Tree Structure Visualizations
=============================

Complete tree visualizations:
- BTreeVisual: Full B-Tree with operations
- LSMTreeVisual: Full LSM-Tree architecture
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import C, T, F, L, DS, A
from .nodes import BTreeNode, KeyCell
from .edges import TreeEdge, FlowArrow
from .memory import MemTable
from .disk import SSTable, StorageLevel, DiskRegion


class BTreeVisual(VGroup):
    """
    Complete B-Tree visualization with operations.
    
    Provides visual representation of B-Tree structure
    with search, insert, split, and delete animations.
    """
    
    def __init__(
        self,
        order: int = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.order = order or DS.BTREE_ORDER
        self.max_keys = self.order - 1
        self.root = None
        self.nodes = {}  # id -> BTreeNode
        self.edges = {}  # (parent_id, child_idx) -> TreeEdge
        
        # Visual containers
        self.node_group = VGroup()
        self.edge_group = VGroup()
        self.add(self.edge_group, self.node_group)
    
    def create_root(self, keys: list) -> BTreeNode:
        """Create root node with given keys"""
        node = BTreeNode(keys=keys, max_keys=self.max_keys)
        node.level = 0
        node.move_to(UP * 2)
        
        self.root = node
        self.nodes[id(node)] = node
        self.node_group.add(node)
        
        return node
    
    def add_child(
        self,
        parent: BTreeNode,
        child_keys: list,
        pointer_index: int,
        is_leaf: bool = True
    ) -> BTreeNode:
        """Add child node to parent at specified pointer"""
        child = BTreeNode(
            keys=child_keys,
            max_keys=self.max_keys,
            is_leaf=is_leaf
        )
        child.level = parent.level + 1
        
        # Calculate position
        parent_pos = parent.get_center()
        num_pointers = len(parent.keys) + 1
        spread = 3.0  # Horizontal spread at this level
        
        x_offset = -spread/2 + (pointer_index / (num_pointers - 1)) * spread if num_pointers > 1 else 0
        child_pos = parent_pos + DOWN * L.TREE_LEVEL_HEIGHT + RIGHT * x_offset
        
        child.move_to(child_pos)
        
        # Create edge
        edge = TreeEdge(
            parent.get_pointer_position(pointer_index) if parent.pointer_cells else parent.get_bottom(),
            child.get_top(),
            color=C.BTREE_POINTER
        )
        
        self.nodes[id(child)] = child
        self.edges[(id(parent), pointer_index)] = edge
        parent.children.append(child)
        
        self.node_group.add(child)
        self.edge_group.add(edge)
        
        return child
    
    def animate_build(self):
        """Animate building the entire tree"""
        animations = []
        
        # First edges
        for edge in self.edge_group:
            animations.append(edge.animate_create())
        
        # Then nodes by level
        nodes_by_level = {}
        for node in self.node_group:
            level = node.level
            if level not in nodes_by_level:
                nodes_by_level[level] = []
            nodes_by_level[level].append(node)
        
        for level in sorted(nodes_by_level.keys()):
            for node in nodes_by_level[level]:
                animations.append(node.animate_create())
        
        return LaggedStart(*animations, lag_ratio=A.LAG_NORMAL)
    
    def animate_search(self, key, path: list = None):
        """Animate searching for a key"""
        if path is None:
            path = self._find_path(key)
        
        animations = []
        for node, key_idx in path:
            # Highlight node
            animations.append(node.animate_highlight())
            
            # Highlight comparison key if found
            if key_idx is not None and key_idx < len(node.key_cells):
                animations.append(node.animate_key_highlight(key_idx))
        
        return Succession(*animations)
    
    def _find_path(self, key) -> list:
        """Find search path for key (returns list of (node, key_idx))"""
        path = []
        current = self.root
        
        while current:
            # Binary search within node
            key_idx = current.find_key_index(key)
            path.append((current, key_idx))
            
            # Check if found or go to child
            if key_idx < len(current.keys) and current.keys[key_idx] == key:
                break
            
            if current.children and key_idx < len(current.children):
                current = current.children[key_idx]
            else:
                break
        
        return path
    
    def get_height(self) -> int:
        """Get tree height"""
        if not self.root:
            return 0
        
        height = 1
        current = self.root
        while current.children:
            height += 1
            current = current.children[0]
        
        return height


class LSMTreeVisual(VGroup):
    """
    Complete LSM-Tree architecture visualization.
    
    Shows MemTable, multiple levels, and compaction flow.
    """
    
    def __init__(
        self,
        num_levels: int = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.num_levels = num_levels or DS.LSM_MAX_LEVELS
        
        # Memory layer
        self.memtable = MemTable()
        self.memtable.move_to(UP * 2.5)
        self.add(self.memtable)
        
        # Disk region
        self.disk_region = DiskRegion(width=7, height=4)
        self.disk_region.move_to(DOWN * 1)
        self.add(self.disk_region)
        
        # Storage levels
        self.levels = []
        for i in range(self.num_levels):
            level = StorageLevel(
                level=i,
                width=6.0,
                height=0.7,
                max_tables=4 * (i + 1)  # More tables at lower levels
            )
            y_pos = 0.8 - i * DS.LSM_LEVEL_SPACING
            level.move_to(RIGHT * 0.3 + UP * y_pos)
            self.levels.append(level)
            self.add(level)
        
        # Arrows
        self.flow_arrows = VGroup()
        self._create_flow_arrows()
        self.add(self.flow_arrows)
    
    def _create_flow_arrows(self):
        """Create data flow arrows"""
        # MemTable to L0
        flush_arrow = FlowArrow(
            self.memtable.get_bottom() + DOWN * 0.2,
            self.levels[0].get_top() + UP * 0.2,
            color=C.IO_WRITE,
            label="flush"
        )
        self.flow_arrows.add(flush_arrow)
        
        # Level to level compaction arrows
        for i in range(len(self.levels) - 1):
            compact_arrow = FlowArrow(
                self.levels[i].get_bottom() + DOWN * 0.1,
                self.levels[i + 1].get_top() + UP * 0.1,
                color=C.LSM_COMPACTION,
                dashed=True
            )
            self.flow_arrows.add(compact_arrow)
    
    def animate_build(self):
        """Animate building the LSM structure"""
        return LaggedStart(
            FadeIn(self.memtable),
            FadeIn(self.disk_region),
            LaggedStart(
                *[FadeIn(level) for level in self.levels],
                lag_ratio=0.2
            ),
            LaggedStart(
                *[Create(arrow) for arrow in self.flow_arrows],
                lag_ratio=0.1
            ),
            lag_ratio=0.3
        )
    
    def animate_write(self, key: str, value: str = None):
        """Animate write operation"""
        return self.memtable.animate_insert(key, value)
    
    def animate_flush(self):
        """Animate MemTable flush to L0"""
        # Create new SSTable in L0
        new_table = self.levels[0].add_sstable()
        
        return Succession(
            # Flush animation
            self.flow_arrows[0].animate_flow(),
            # MemTable clear
            self.memtable.animate_flush(),
            # SSTable appear
            new_table.animate_create()
        )
    
    def animate_compaction(self, from_level: int, to_level: int):
        """Animate compaction between levels"""
        if from_level >= len(self.levels) - 1:
            return Wait(0)
        
        # Get tables from source level
        source_tables = list(self.levels[from_level].tables)
        
        # Create merged table in target level
        merged_table = self.levels[to_level].add_sstable(
            table_id=f"M{len(self.levels[to_level].tables)}"
        )
        
        return Succession(
            # Highlight compaction
            AnimationGroup(
                *[table.animate_compact() for table in source_tables]
            ),
            # Flow to next level
            self.flow_arrows[from_level + 1].animate_flow() if from_level + 1 < len(self.flow_arrows) else Wait(0),
            # Remove old, show new
            AnimationGroup(
                *[table.animate_delete() for table in source_tables]
            ),
            merged_table.animate_create()
        )
    
    def animate_read(self, key: str, found_level: int = 0):
        """Animate read operation searching through levels"""
        animations = []
        
        # Check MemTable first
        animations.append(
            self.memtable.container.animate.set_stroke(color=C.IO_READ, width=3)
        )
        
        # Search through levels until found
        for i in range(found_level + 1):
            level = self.levels[i]
            animations.append(
                level.container.animate.set_stroke(color=C.IO_READ, width=2)
            )
            
            if i == found_level:
                # Found - highlight
                animations.append(
                    level.container.animate.set_fill(color=C.SUCCESS, opacity=0.2)
                )
        
        return Succession(*animations)
    
    def get_write_amplification(self) -> float:
        """Calculate approximate write amplification"""
        # Simplified: each level adds ~size_ratio writes
        return sum(DS.LSM_SIZE_RATIO ** i for i in range(self.num_levels))
    
    def get_space_amplification(self) -> float:
        """Calculate approximate space amplification"""
        # During compaction, can temporarily use 2x space
        return 1.0 + 1.0 / DS.LSM_SIZE_RATIO
