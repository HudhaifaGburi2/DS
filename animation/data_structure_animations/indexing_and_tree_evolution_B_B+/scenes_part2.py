"""
B-Tree Evolution Animation - Scenes E-H
========================================

Part 2: M-Way Trees and B-Tree Growth
- Scene E: Relationship to M-Way Trees
- Scene F: From Index Blocks to M-Way Tree
- Scene G: B-Tree Bottom-Up Growth
- Scene H: Propagating Splits Upward
"""

from manim import *
from config import C, T, S, F, A, L
from components import BTreeNode, IndexEntry, NarrationBox


class BTreeBaseScene(Scene):
    """Base scene with common utilities"""
    
    def setup(self):
        self.camera.background_color = C.BACKGROUND
    
    def create_title(self, text: str, arabic: str = None):
        title = Text(text, font=F.MAIN_FONT, font_size=F.TITLE, color=C.TEXT_PRIMARY)
        title.to_edge(UP, buff=0.4)
        if arabic:
            arabic_text = Text(arabic, font=F.ARABIC_FONT, font_size=F.HEADING, color=C.TEXT_SECONDARY)
            arabic_text.next_to(title, DOWN, buff=0.15)
            return VGroup(title, arabic_text)
        return title
    
    def narrate(self, *lines, position=DOWN * 3, wait_time=None):
        narration = VGroup()
        for line in lines:
            text = Text(line, font=F.MAIN_FONT, font_size=F.BODY, color=C.TEXT_NARRATION)
            narration.add(text)
        narration.arrange(DOWN, buff=F.NARRATION_SPACING, aligned_edge=LEFT)
        narration.move_to(position)
        if narration.width > 12:
            narration.scale(12 / narration.width)
        anims = [FadeIn(line, shift=UP * 0.2) for line in narration]
        self.play(LaggedStart(*anims, lag_ratio=0.3))
        if wait_time:
            self.wait(wait_time)
        else:
            self.wait(len(lines) * T.NARRATION_LINE)
        return narration
    
    def scene_transition(self):
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=T.SCENE_TRANSITION)
        self.wait(0.2)


# ══════════════════════════════════════════════════════════════════════════════
# SCENE E — Relationship to M-Way Trees
# ══════════════════════════════════════════════════════════════════════════════

class SceneE_MWayRelation(BTreeBaseScene):
    """
    Animation: Index blocks become M-way nodes.
    
    Key concepts:
    - Index chunking into blocks
    - Multiple keys per block
    - Block = M-way node
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════════════
        title = self.create_title("From Indexing to M-Way Trees", "من الفهرسة إلى أشجار M")
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # NARRATION: Index splitting
        # ══════════════════════════════════════════════════════════════════════
        narration1 = self.narrate(
            "At this point,",
            "the indexing table is split into blocks."
        )
        self.play(FadeOut(narration1))
        
        # ══════════════════════════════════════════════════════════════════════
        # INDEX TABLE (linear)
        # ══════════════════════════════════════════════════════════════════════
        index_entries = VGroup()
        keys = [100, 200, 300, 400, 500, 600, 700, 800, 900]
        
        for i, key in enumerate(keys):
            entry = IndexEntry(key, (i // 3) + 1)
            entry.scale(0.6)
            index_entries.add(entry)
        
        index_entries.arrange(DOWN, buff=0.08)
        index_entries.shift(LEFT * 4)
        
        self.play(FadeIn(index_entries))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # CHUNK INTO BLOCKS
        # ══════════════════════════════════════════════════════════════════════
        narration2 = self.narrate(
            "Each block holds many keys."
        )
        self.play(FadeOut(narration2))
        
        # Group into 3 blocks of 3 entries each
        block_boxes = VGroup()
        for i in range(3):
            box = SurroundingRectangle(
                VGroup(*index_entries[i*3:(i+1)*3]),
                color=[C.SPLIT_LEFT, C.PROMOTED, C.SPLIT_RIGHT][i],
                buff=0.1,
                stroke_width=2
            )
            block_boxes.add(box)
        
        self.play(LaggedStart(*[Create(box) for box in block_boxes], lag_ratio=0.3))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # TRANSFORM TO M-WAY NODES
        # ══════════════════════════════════════════════════════════════════════
        narration3 = self.narrate(
            "This structure is no longer a table.",
            "It is an M-way search node."
        )
        self.play(FadeOut(narration3))
        
        # Create M-way nodes
        m_way_nodes = VGroup()
        for i in range(3):
            node_keys = keys[i*3:(i+1)*3]
            node = BTreeNode(node_keys, is_leaf=False)
            node.shift(RIGHT * 2 + UP * (1.5 - i * 1.5))
            m_way_nodes.add(node)
        
        # Transform animation
        for i in range(3):
            block_group = VGroup(
                *index_entries[i*3:(i+1)*3],
                block_boxes[i]
            )
            self.play(
                Transform(block_group, m_way_nodes[i]),
                run_time=T.SLOW
            )
        
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # SHOW POINTERS
        # ══════════════════════════════════════════════════════════════════════
        narration4 = self.narrate(
            "A block contains many keys and many pointers."
        )
        
        # Highlight pointer positions
        for node in m_way_nodes:
            if hasattr(node, 'pointer_slots'):
                self.play(
                    *[slot.animate.scale(1.5).set_color(C.POINTER) for slot in node.pointer_slots],
                    run_time=T.FAST
                )
                self.play(
                    *[slot.animate.scale(1/1.5).set_color(C.POINTER) for slot in node.pointer_slots],
                    run_time=T.FAST
                )
        
        self.wait(T.ABSORB)
        self.play(FadeOut(narration4))
        self.scene_transition()


# ══════════════════════════════════════════════════════════════════════════════
# SCENE F — From Index Blocks to M-Way Tree
# ══════════════════════════════════════════════════════════════════════════════

class SceneF_TreeFormation(BTreeBaseScene):
    """
    Animation: Index blocks forming a tree structure.
    
    Key concepts:
    - Block linking creates tree
    - Height reduction
    - Tree navigation
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════════════
        title = self.create_title("Index Blocks Form a Tree", "كتل الفهرس تشكل شجرة")
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # NARRATION
        # ══════════════════════════════════════════════════════════════════════
        narration1 = self.narrate(
            "When index blocks point to other index blocks,",
            "a tree naturally forms."
        )
        self.play(FadeOut(narration1))
        
        # ══════════════════════════════════════════════════════════════════════
        # CREATE TREE STRUCTURE
        # ══════════════════════════════════════════════════════════════════════
        
        # Root node
        root = BTreeNode([300, 600], is_leaf=False)
        root.shift(UP * 2)
        
        # Child nodes (internal)
        child1 = BTreeNode([100, 200], is_leaf=False)
        child1.shift(LEFT * 3.5)
        
        child2 = BTreeNode([400, 500], is_leaf=False)
        
        child3 = BTreeNode([700, 800], is_leaf=False)
        child3.shift(RIGHT * 3.5)
        
        children = VGroup(child1, child2, child3)
        
        # Leaf nodes
        leaves = VGroup()
        leaf_positions = [
            LEFT * 5 + DOWN * 2,
            LEFT * 3 + DOWN * 2,
            LEFT * 1 + DOWN * 2,
            RIGHT * 1 + DOWN * 2,
            RIGHT * 3 + DOWN * 2,
            RIGHT * 5 + DOWN * 2,
        ]
        leaf_keys = [[50], [150], [350], [450], [650], [750]]
        
        for pos, keys in zip(leaf_positions, leaf_keys):
            leaf = BTreeNode(keys, is_leaf=True)
            leaf.move_to(pos)
            leaves.add(leaf)
        
        # Show root first
        self.play(FadeIn(root))
        self.wait(T.BEAT)
        
        # Show children with edges
        edges_to_children = VGroup()
        for i, child in enumerate(children):
            edge = Line(
                root.get_pointer_position(i),
                child.bg.get_top(),
                color=C.EDGE,
                stroke_width=S.EDGE_STROKE
            )
            edges_to_children.add(edge)
        
        self.play(
            LaggedStart(*[FadeIn(c) for c in children], lag_ratio=0.2),
            LaggedStart(*[Create(e) for e in edges_to_children], lag_ratio=0.2)
        )
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # NARRATION: Navigation
        # ══════════════════════════════════════════════════════════════════════
        narration2 = self.narrate(
            "Each node can guide the search",
            "to one of many children."
        )
        self.play(FadeOut(narration2))
        
        # Show search path animation
        search_target = Text("Find: 450", font=F.CODE_FONT, font_size=F.LABEL, color=C.SELECTED)
        search_target.to_corner(UR, buff=0.5)
        self.play(FadeIn(search_target))
        
        # Highlight path: root -> child2
        self.play(root.bg.animate.set_stroke(color=C.SEARCH_PATH, width=4))
        self.wait(T.BEAT)
        
        # Compare at root: 450 > 300, 450 < 600 -> middle child
        compare = Text("300 < 450 < 600", font=F.CODE_FONT, font_size=F.CAPTION, color=C.TEXT_ACCENT)
        compare.next_to(root, RIGHT, buff=0.3)
        self.play(FadeIn(compare))
        self.wait(T.BEAT)
        
        self.play(
            edges_to_children[1].animate.set_color(C.SEARCH_PATH).set_stroke(width=4),
            child2.bg.animate.set_stroke(color=C.SEARCH_PATH, width=4),
            FadeOut(compare)
        )
        
        self.wait(T.ABSORB)
        
        # ══════════════════════════════════════════════════════════════════════
        # HEIGHT BENEFIT
        # ══════════════════════════════════════════════════════════════════════
        narration3 = self.narrate(
            "This is the core idea behind M-way search trees.",
            "The index has become a tree."
        )
        
        # Height indicator
        height_label = VGroup(
            Text("Height: 2", font=F.CODE_FONT, font_size=F.LABEL, color=C.SUCCESS),
            Text("(vs 9 levels in linear index)", font=F.MAIN_FONT, font_size=F.CAPTION, color=C.TEXT_SECONDARY)
        )
        height_label.arrange(DOWN, buff=0.1)
        height_label.to_corner(DL, buff=0.5)
        
        self.play(FadeIn(height_label))
        self.wait(T.CONTEMPLATE)
        
        self.play(FadeOut(narration3))
        self.scene_transition()


# ══════════════════════════════════════════════════════════════════════════════
# SCENE G — B-Tree Bottom-Up Growth
# ══════════════════════════════════════════════════════════════════════════════

class SceneG_BTreeGrowth(BTreeBaseScene):
    """
    Animation: B-Tree insertion and leaf splitting.
    
    Key concepts:
    - Insert at leaf
    - Node overflow
    - Split and promote
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════════════
        title = self.create_title("B-Tree: Bottom-Up Growth", "شجرة B: النمو من الأسفل")
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # NARRATION
        # ══════════════════════════════════════════════════════════════════════
        narration1 = self.narrate(
            "Records are always inserted",
            "into the leaf nodes first."
        )
        self.play(FadeOut(narration1))
        
        # ══════════════════════════════════════════════════════════════════════
        # INITIAL LEAF NODE
        # ══════════════════════════════════════════════════════════════════════
        leaf = BTreeNode([10, 20, 30], is_leaf=True)
        leaf.shift(DOWN * 0.5)
        
        self.play(FadeIn(leaf))
        
        # Order indicator
        order_text = Text("Order = 4 (max 3 keys)", font=F.CODE_FONT, font_size=F.CAPTION, color=C.TEXT_SECONDARY)
        order_text.to_corner(DR, buff=0.5)
        self.play(FadeIn(order_text))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # INSERT KEY 40 (OVERFLOW)
        # ══════════════════════════════════════════════════════════════════════
        narration2 = self.narrate(
            "When a leaf node overflows,",
            "it is split into two nodes."
        )
        self.play(FadeOut(narration2))
        
        # New key coming in
        new_key = Text("40", font=F.CODE_FONT, font_size=F.KEY_SIZE, color=C.PROMOTED)
        new_key.move_to(UP * 2.5)
        
        insert_label = Text("Insert: 40", font=F.CODE_FONT, font_size=F.LABEL, color=C.PROMOTED)
        insert_label.to_corner(UL, buff=0.5)
        
        self.play(FadeIn(insert_label), FadeIn(new_key))
        self.play(new_key.animate.move_to(leaf.bg.get_right() + RIGHT * 0.3))
        
        # Show overflow
        overflow_box = SurroundingRectangle(
            VGroup(leaf, new_key),
            color=C.ERROR,
            buff=0.15,
            stroke_width=3
        )
        overflow_label = Text("OVERFLOW!", font=F.CODE_FONT, font_size=F.LABEL, color=C.ERROR)
        overflow_label.next_to(overflow_box, UP, buff=0.1)
        
        self.play(Create(overflow_box), FadeIn(overflow_label))
        self.play(Flash(overflow_box, color=C.ERROR, line_length=0.3))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # SPLIT ANIMATION
        # ══════════════════════════════════════════════════════════════════════
        
        # Fade out overflow indicators
        self.play(FadeOut(overflow_box), FadeOut(overflow_label), FadeOut(new_key))
        
        # Create split nodes
        left_leaf = BTreeNode([10, 20], is_leaf=True)
        left_leaf.shift(DOWN * 1.5 + LEFT * 2)
        
        right_leaf = BTreeNode([30, 40], is_leaf=True)
        right_leaf.shift(DOWN * 1.5 + RIGHT * 2)
        
        # Middle key for promotion
        middle_key = Text("30", font=F.CODE_FONT, font_size=F.HEADING, color=C.PROMOTED)
        middle_key.move_to(leaf.bg.get_center())
        
        # Split animation
        self.play(
            FadeOut(leaf),
            FadeIn(left_leaf),
            FadeIn(right_leaf),
            run_time=T.SPLIT
        )
        
        # Promote middle key
        narration3 = self.narrate(
            "The middle key is promoted",
            "to the parent node."
        )
        self.play(FadeOut(narration3))
        
        self.play(FadeIn(middle_key))
        self.play(
            middle_key.animate.shift(UP * 2),
            run_time=T.PROMOTE
        )
        
        # Create parent node
        parent = BTreeNode([30], is_leaf=False)
        parent.shift(UP * 1.5)
        
        self.play(Transform(middle_key, parent))
        
        # Draw edges
        edge_left = Line(
            parent.get_pointer_position(0),
            left_leaf.bg.get_top(),
            color=C.EDGE,
            stroke_width=S.EDGE_STROKE
        )
        edge_right = Line(
            parent.get_pointer_position(1),
            right_leaf.bg.get_top(),
            color=C.EDGE,
            stroke_width=S.EDGE_STROKE
        )
        
        self.play(Create(edge_left), Create(edge_right))
        
        # Success state
        success = Text("✓ B-Tree property maintained", font=F.MAIN_FONT, font_size=F.LABEL, color=C.SUCCESS)
        success.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(success))
        
        self.wait(T.CONTEMPLATE)
        self.scene_transition()


# ══════════════════════════════════════════════════════════════════════════════
# SCENE H — Propagating Splits Upward
# ══════════════════════════════════════════════════════════════════════════════

class SceneH_CascadingSplits(BTreeBaseScene):
    """
    Animation: Cascading splits up the tree.
    
    Key concepts:
    - Parent overflow
    - Recursive splitting
    - Root split creates new root
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════════════
        title = self.create_title("Propagating Splits Upward", "انتشار الانقسام للأعلى")
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # INITIAL TREE (parent almost full)
        # ══════════════════════════════════════════════════════════════════════
        
        # Root with 3 keys (max for order 4)
        root = BTreeNode([20, 40, 60], is_leaf=False)
        root.shift(UP * 1.5)
        
        # Children
        children = VGroup()
        child_keys = [[10], [30], [50], [70, 80, 90]]
        child_positions = [LEFT * 4.5, LEFT * 1.5, RIGHT * 1.5, RIGHT * 4.5]
        
        edges = VGroup()
        for i, (keys, pos) in enumerate(zip(child_keys, child_positions)):
            child = BTreeNode(keys, is_leaf=True)
            child.shift(DOWN * 0.8 + pos)
            children.add(child)
            
            edge = Line(
                root.get_pointer_position(i),
                child.bg.get_top(),
                color=C.EDGE,
                stroke_width=S.EDGE_STROKE
            )
            edges.add(edge)
        
        self.play(FadeIn(root), FadeIn(children), FadeIn(edges))
        
        # Highlight full parent
        full_label = Text("Parent is FULL", font=F.CODE_FONT, font_size=F.CAPTION, color=C.WARNING)
        full_label.next_to(root, UP, buff=0.1)
        self.play(
            root.bg.animate.set_stroke(color=C.WARNING, width=3),
            FadeIn(full_label)
        )
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # NARRATION
        # ══════════════════════════════════════════════════════════════════════
        narration1 = self.narrate(
            "Sometimes, the parent node is already full.",
            "In that case, the parent also splits."
        )
        self.play(FadeOut(narration1))
        
        # ══════════════════════════════════════════════════════════════════════
        # LEAF SPLIT (rightmost child)
        # ══════════════════════════════════════════════════════════════════════
        
        # Insert 95 into rightmost leaf
        insert_label = Text("Insert: 95", font=F.CODE_FONT, font_size=F.LABEL, color=C.PROMOTED)
        insert_label.to_corner(UL, buff=0.5)
        self.play(FadeIn(insert_label))
        
        # Rightmost leaf overflows
        self.play(
            children[3].bg.animate.set_stroke(color=C.ERROR, width=3),
            Flash(children[3].bg, color=C.ERROR, line_length=0.2)
        )
        self.wait(T.BEAT)
        
        # Leaf splits, middle key (85) needs to go up
        promoted_key = Text("85", font=F.CODE_FONT, font_size=F.LABEL, color=C.PROMOTED)
        promoted_key.move_to(children[3].bg.get_center())
        
        self.play(FadeIn(promoted_key))
        self.play(
            promoted_key.animate.move_to(root.bg.get_right() + RIGHT * 0.5),
            run_time=T.PROMOTE
        )
        
        # Parent now overflows!
        self.play(FadeOut(full_label))
        overflow_label = Text("Parent OVERFLOWS!", font=F.CODE_FONT, font_size=F.LABEL, color=C.ERROR)
        overflow_label.next_to(root, UP, buff=0.1)
        
        self.play(
            root.bg.animate.set_stroke(color=C.ERROR, width=4),
            FadeIn(overflow_label),
            Flash(root.bg, color=C.ERROR, line_length=0.3)
        )
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # ROOT SPLIT
        # ══════════════════════════════════════════════════════════════════════
        narration2 = self.narrate(
            "This splitting process can propagate upward,",
            "all the way to the root."
        )
        self.play(FadeOut(narration2), FadeOut(promoted_key), FadeOut(overflow_label))
        
        # New structure after root split
        new_root = BTreeNode([40], is_leaf=False)
        new_root.shift(UP * 2.5)
        
        left_internal = BTreeNode([20], is_leaf=False)
        left_internal.shift(UP * 0.8 + LEFT * 2.5)
        
        right_internal = BTreeNode([60, 85], is_leaf=False)
        right_internal.shift(UP * 0.8 + RIGHT * 2.5)
        
        # Clear old tree
        self.play(
            FadeOut(root),
            FadeOut(children),
            FadeOut(edges),
            FadeOut(insert_label)
        )
        
        # Show new structure
        self.play(FadeIn(new_root))
        self.wait(T.BEAT)
        
        # New edges from root
        new_edge_left = Line(
            new_root.get_pointer_position(0),
            left_internal.bg.get_top(),
            color=C.EDGE,
            stroke_width=S.EDGE_STROKE
        )
        new_edge_right = Line(
            new_root.get_pointer_position(1),
            right_internal.bg.get_top(),
            color=C.EDGE,
            stroke_width=S.EDGE_STROKE
        )
        
        self.play(
            FadeIn(left_internal),
            FadeIn(right_internal),
            Create(new_edge_left),
            Create(new_edge_right)
        )
        
        # Height increased indicator
        height_label = Text("Height increased: 2 → 3", font=F.CODE_FONT, font_size=F.LABEL, color=C.TEXT_ACCENT)
        height_label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(height_label))
        
        # New root highlight
        new_root_label = Text("NEW ROOT", font=F.CODE_FONT, font_size=F.CAPTION, color=C.SUCCESS)
        new_root_label.next_to(new_root, UP, buff=0.1)
        self.play(
            new_root.bg.animate.set_stroke(color=C.SUCCESS, width=3),
            FadeIn(new_root_label)
        )
        
        self.wait(T.CONTEMPLATE)
        self.scene_transition()
