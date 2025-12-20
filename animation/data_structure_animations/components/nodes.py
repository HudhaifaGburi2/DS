"""
Node Components for Tree Visualizations
========================================

Provides reusable node components:
- TreeNode: Generic tree node
- BTreeNode: Multi-key B-Tree node with pointers
- KeyCell: Individual key visualization
- PointerCell: Child pointer visualization
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import C, T, F, L, DS, A


class KeyCell(VGroup):
    """
    Individual key cell within a node.
    
    Visual: Rounded rectangle with key value text.
    """
    
    def __init__(
        self,
        key: str,
        width: float = None,
        height: float = None,
        color=None,
        text_color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.key = key
        self.width = width or DS.BTREE_KEY_WIDTH
        self.height = height or DS.BTREE_KEY_HEIGHT
        self.color = color or C.BTREE_NODE
        self.text_color = text_color or C.BTREE_KEY
        
        # Key background
        self.bg = RoundedRectangle(
            width=self.width,
            height=self.height,
            corner_radius=0.05,
            fill_color=self.color,
            fill_opacity=0.9,
            stroke_color=self.color,
            stroke_width=1.5
        )
        
        # Key text
        self.text = Text(
            str(key),
            font=F.CODE,
            color=self.text_color
        ).scale(F.SIZE_KEY)
        self.text.move_to(self.bg.get_center())
        
        self.add(self.bg, self.text)
    
    def highlight(self, color=None):
        """Return animation to highlight this key"""
        color = color or C.BTREE_KEY_ACTIVE
        return AnimationGroup(
            self.bg.animate.set_fill(color=color),
            self.bg.animate.set_stroke(color=color, width=3),
        )
    
    def unhighlight(self):
        """Return animation to remove highlight"""
        return AnimationGroup(
            self.bg.animate.set_fill(color=self.color),
            self.bg.animate.set_stroke(color=self.color, width=1.5),
        )
    
    def update_key(self, new_key: str):
        """Update the key value"""
        new_text = Text(
            str(new_key),
            font=F.CODE,
            color=self.text_color
        ).scale(F.SIZE_KEY)
        new_text.move_to(self.bg.get_center())
        
        self.remove(self.text)
        self.text = new_text
        self.add(self.text)
        self.key = new_key


class PointerCell(VGroup):
    """
    Child pointer visualization.
    
    Visual: Small triangle or arrow indicator.
    """
    
    def __init__(
        self,
        size: float = None,
        color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.size = size or DS.BTREE_POINTER_SIZE
        self.color = color or C.BTREE_POINTER
        
        # Pointer triangle
        self.indicator = Triangle(
            fill_color=self.color,
            fill_opacity=0.8,
            stroke_width=0
        ).scale(self.size)
        self.indicator.rotate(-PI / 2)  # Point downward
        
        self.add(self.indicator)
    
    def activate(self, color=None):
        """Highlight pointer as active"""
        color = color or C.BTREE_KEY_ACTIVE
        return self.indicator.animate.set_fill(color=color)
    
    def deactivate(self):
        """Return to normal state"""
        return self.indicator.animate.set_fill(color=self.color)


class TreeNode(VGroup):
    """
    Generic tree node with single value.
    
    Visual: Circle or rounded rectangle with value.
    """
    
    def __init__(
        self,
        value: str,
        radius: float = 0.4,
        color=None,
        text_color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.value = value
        self.radius = radius
        self.color = color or C.BTREE_NODE
        self.text_color = text_color or C.TEXT_PRIMARY
        self.level = 0
        self.children = []
        
        # Node circle
        self.shape = Circle(
            radius=radius,
            fill_color=self.color,
            fill_opacity=0.9,
            stroke_color=self.color,
            stroke_width=2
        )
        
        # Value text
        self.text = Text(
            str(value),
            font=F.CODE,
            color=self.text_color
        ).scale(F.SIZE_KEY)
        self.text.move_to(self.shape.get_center())
        
        self.add(self.shape, self.text)
    
    def animate_create(self):
        """Animation to create node"""
        return FadeIn(self, scale=0.5)
    
    def animate_highlight(self, color=None):
        """Animation to highlight node"""
        color = color or C.BTREE_KEY_ACTIVE
        return self.shape.animate.set_stroke(color=color, width=4)


class BTreeNode(VGroup):
    """
    B-Tree node with multiple keys and pointers.
    
    Visual: Horizontal arrangement of key cells with pointer indicators.
    Structure: [P0][K1][P1][K2][P2]...[Kn][Pn]
    """
    
    def __init__(
        self,
        keys: list,
        max_keys: int = None,
        width: float = None,
        height: float = None,
        color=None,
        is_leaf: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.keys = keys
        self.max_keys = max_keys or DS.BTREE_ORDER - 1
        self.node_width = width or DS.BTREE_NODE_WIDTH
        self.node_height = height or DS.BTREE_NODE_HEIGHT
        self.color = color or C.BTREE_NODE
        self.is_leaf = is_leaf
        self.level = 0
        self.children = []
        
        self.key_cells = VGroup()
        self.pointer_cells = VGroup()
        
        self._build_node()
    
    def _build_node(self):
        """Construct the node visualization"""
        # Background rectangle
        total_width = self._calculate_width()
        self.bg = RoundedRectangle(
            width=total_width,
            height=self.node_height,
            corner_radius=0.08,
            fill_color=C.BTREE_PAGE,
            fill_opacity=0.3,
            stroke_color=self.color,
            stroke_width=2
        )
        self.add(self.bg)
        
        # Build keys and pointers
        num_keys = len(self.keys)
        key_width = DS.BTREE_KEY_WIDTH
        spacing = 0.08
        
        # Calculate starting x position
        content_width = num_keys * key_width + (num_keys - 1) * spacing
        start_x = -content_width / 2 + key_width / 2
        
        for i, key in enumerate(self.keys):
            # Create key cell
            key_cell = KeyCell(key, color=self.color)
            key_cell.move_to(
                self.bg.get_center() + RIGHT * (start_x + i * (key_width + spacing))
            )
            self.key_cells.add(key_cell)
        
        self.add(self.key_cells)
        
        # Add pointers if not leaf
        if not self.is_leaf:
            pointer_positions = self._get_pointer_positions()
            for pos in pointer_positions:
                pointer = PointerCell()
                pointer.move_to(pos + DOWN * (self.node_height / 2 + 0.1))
                self.pointer_cells.add(pointer)
            self.add(self.pointer_cells)
    
    def _calculate_width(self) -> float:
        """Calculate total node width based on keys"""
        num_keys = max(len(self.keys), 1)
        return num_keys * DS.BTREE_KEY_WIDTH + (num_keys + 1) * 0.1
    
    def _get_pointer_positions(self) -> list:
        """Get positions for child pointers"""
        positions = []
        if not self.key_cells:
            return positions
        
        # Pointer before first key
        first_key = self.key_cells[0]
        positions.append(first_key.get_left() + LEFT * 0.05)
        
        # Pointers after each key
        for key_cell in self.key_cells:
            positions.append(key_cell.get_right() + RIGHT * 0.05)
        
        return positions
    
    # ══════════════════════════════════════════════════════════════════════════
    # ANIMATIONS
    # ══════════════════════════════════════════════════════════════════════════
    
    def animate_create(self):
        """Animation to create node"""
        return FadeIn(self, scale=0.8)
    
    def animate_highlight(self, color=None):
        """Highlight entire node"""
        color = color or C.BTREE_NODE_HIGHLIGHT
        return self.bg.animate.set_stroke(color=color, width=3)
    
    def animate_key_highlight(self, key_index: int, color=None):
        """Highlight specific key"""
        if 0 <= key_index < len(self.key_cells):
            return self.key_cells[key_index].highlight(color)
        return Wait(0)
    
    def animate_overflow(self):
        """Visual indication of overflow"""
        return Succession(
            self.bg.animate.set_stroke(color=C.BTREE_SPLIT, width=4),
            self.bg.animate.scale(1.05),
        )
    
    def animate_split(self):
        """Animation for node splitting"""
        return self.bg.animate.set_fill(color=C.BTREE_SPLIT, opacity=0.5)
    
    # ══════════════════════════════════════════════════════════════════════════
    # KEY OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════
    
    def get_key_position(self, key_index: int):
        """Get center position of a key cell"""
        if 0 <= key_index < len(self.key_cells):
            return self.key_cells[key_index].get_center()
        return self.get_center()
    
    def get_pointer_position(self, pointer_index: int):
        """Get position of a pointer"""
        if 0 <= pointer_index < len(self.pointer_cells):
            return self.pointer_cells[pointer_index].get_center()
        return self.get_bottom()
    
    def is_full(self) -> bool:
        """Check if node is at capacity"""
        return len(self.keys) >= self.max_keys
    
    def find_key_index(self, key) -> int:
        """Find index where key should be inserted"""
        for i, k in enumerate(self.keys):
            if key < k:
                return i
        return len(self.keys)
