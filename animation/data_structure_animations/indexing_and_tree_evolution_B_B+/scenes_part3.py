"""
B-Tree Evolution Animation - Scenes I-L
========================================

Part 3: B-Tree Balance and B+ Tree Introduction
- Scene I: Balanced Tree Guarantee
- Scene J: Transition from B-Tree to B+ Tree
- Scene K: B+ Tree Structure
- Scene L: Leaf Node Linking
"""

from manim import *
from config import C, T, S, F, A, L
from components import BTreeNode, NarrationBox


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
# SCENE I — Balanced Tree Guarantee
# ══════════════════════════════════════════════════════════════════════════════

class SceneI_Balance(BTreeBaseScene):
    """
    Animation: B-Tree self-balancing property.
    
    Key concepts:
    - All leaves at same depth
    - Predictable disk access
    - Balanced by construction
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════════════
        title = self.create_title("Balanced Tree Guarantee", "ضمان توازن الشجرة")
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # NARRATION
        # ══════════════════════════════════════════════════════════════════════
        narration1 = self.narrate(
            "Because splits move upward,",
            "and all insertions start at the leaves,"
        )
        self.play(FadeOut(narration1))
        
        # ══════════════════════════════════════════════════════════════════════
        # BALANCED B-TREE
        # ══════════════════════════════════════════════════════════════════════
        
        # Root
        root = BTreeNode([40], is_leaf=False)
        root.shift(UP * 2)
        
        # Level 1
        internal1 = BTreeNode([20], is_leaf=False)
        internal1.shift(LEFT * 3)
        
        internal2 = BTreeNode([60], is_leaf=False)
        internal2.shift(RIGHT * 3)
        
        # Level 2 (leaves) - all at same depth
        leaves = VGroup()
        leaf_data = [
            ([10, 15], LEFT * 4.5 + DOWN * 1.5),
            ([25, 30], LEFT * 1.5 + DOWN * 1.5),
            ([45, 55], RIGHT * 1.5 + DOWN * 1.5),
            ([70, 80], RIGHT * 4.5 + DOWN * 1.5),
        ]
        
        for keys, pos in leaf_data:
            leaf = BTreeNode(keys, is_leaf=True)
            leaf.move_to(pos)
            leaves.add(leaf)
        
        # Edges
        edges = VGroup()
        # Root to internals
        edges.add(Line(root.get_pointer_position(0), internal1.bg.get_top(), color=C.EDGE, stroke_width=S.EDGE_STROKE))
        edges.add(Line(root.get_pointer_position(1), internal2.bg.get_top(), color=C.EDGE, stroke_width=S.EDGE_STROKE))
        # Internal1 to leaves
        edges.add(Line(internal1.get_pointer_position(0), leaves[0].bg.get_top(), color=C.EDGE, stroke_width=S.EDGE_STROKE))
        edges.add(Line(internal1.get_pointer_position(1), leaves[1].bg.get_top(), color=C.EDGE, stroke_width=S.EDGE_STROKE))
        # Internal2 to leaves
        edges.add(Line(internal2.get_pointer_position(0), leaves[2].bg.get_top(), color=C.EDGE, stroke_width=S.EDGE_STROKE))
        edges.add(Line(internal2.get_pointer_position(1), leaves[3].bg.get_top(), color=C.EDGE, stroke_width=S.EDGE_STROKE))
        
        # Show tree
        self.play(FadeIn(root))
        self.play(FadeIn(VGroup(internal1, internal2)), Create(edges[:2]))
        self.play(FadeIn(leaves), Create(edges[2:]))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL ALIGNMENT VISUALIZATION
        # ══════════════════════════════════════════════════════════════════════
        narration2 = self.narrate(
            "the tree remains perfectly balanced.",
            "All leaf nodes stay at the same depth."
        )
        self.play(FadeOut(narration2))
        
        # Draw horizontal level lines
        level_lines = VGroup()
        level_labels = VGroup()
        
        levels = [
            (UP * 2, "Level 0 (Root)"),
            (ORIGIN, "Level 1"),
            (DOWN * 1.5, "Level 2 (Leaves)"),
        ]
        
        for y_pos, label_text in levels:
            line = DashedLine(
                LEFT * 6 + y_pos,
                RIGHT * 6 + y_pos,
                color=C.TEXT_TERTIARY,
                stroke_width=1,
                dash_length=0.1
            )
            label = Text(label_text, font=F.CODE_FONT, font_size=F.CAPTION, color=C.TEXT_SECONDARY)
            label.next_to(line, LEFT, buff=0.1)
            level_lines.add(line)
            level_labels.add(label)
        
        self.play(
            LaggedStart(*[Create(line) for line in level_lines], lag_ratio=0.2),
            LaggedStart(*[FadeIn(label) for label in level_labels], lag_ratio=0.2)
        )
        
        # Highlight all leaves at same level
        self.play(
            *[leaf.bg.animate.set_stroke(color=C.SUCCESS, width=4) for leaf in leaves],
            run_time=T.NORMAL
        )
        
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # PREDICTABLE ACCESS
        # ══════════════════════════════════════════════════════════════════════
        narration3 = self.narrate(
            "This guarantees",
            "predictable disk access time."
        )
        
        # Show O(log n) guarantee
        complexity = VGroup(
            Text("Disk Accesses:", font=F.MAIN_FONT, font_size=F.LABEL, color=C.TEXT_SECONDARY),
            Text("O(log n)", font=F.CODE_FONT, font_size=F.HEADING, color=C.SUCCESS)
        )
        complexity.arrange(RIGHT, buff=0.3)
        complexity.to_corner(DR, buff=0.5)
        
        self.play(FadeIn(complexity, scale=0.8))
        
        self.wait(T.CONTEMPLATE)
        self.play(FadeOut(narration3))
        self.scene_transition()


# ══════════════════════════════════════════════════════════════════════════════
# SCENE J — Transition to B+ Tree
# ══════════════════════════════════════════════════════════════════════════════

class SceneJ_BPlusTransition(BTreeBaseScene):
    """
    Animation: Why B+ Trees improve on B-Trees.
    
    Key concepts:
    - B-Tree stores data everywhere
    - Wasted space in internal nodes
    - B+ Tree optimization
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════════════
        title = self.create_title("From B-Tree to B+ Tree", "من شجرة B إلى شجرة B+")
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # B-TREE WITH DATA IN ALL NODES
        # ══════════════════════════════════════════════════════════════════════
        narration1 = self.narrate(
            "The B-Tree works well.",
            "But it stores data records in both internal and leaf nodes."
        )
        self.play(FadeOut(narration1))
        
        # B-Tree with data icons
        btree_label = Text("B-Tree", font=F.MAIN_FONT, font_size=F.SUBHEADING, color=C.INTERNAL_NODE)
        btree_label.shift(UP * 2.8)
        
        root = BTreeNode([40], is_leaf=False, has_data=True)
        root.shift(UP * 1.5)
        
        # Add data indicator to root
        root_data = Text("📄", font_size=16)
        root_data.next_to(root.key_texts[0], RIGHT, buff=0.05)
        
        internal1 = BTreeNode([20], is_leaf=False, has_data=True)
        internal1.shift(LEFT * 2.5 + DOWN * 0.3)
        int1_data = Text("📄", font_size=16)
        int1_data.next_to(internal1.key_texts[0], RIGHT, buff=0.05)
        
        internal2 = BTreeNode([60], is_leaf=False, has_data=True)
        internal2.shift(RIGHT * 2.5 + DOWN * 0.3)
        int2_data = Text("📄", font_size=16)
        int2_data.next_to(internal2.key_texts[0], RIGHT, buff=0.05)
        
        leaf1 = BTreeNode([10], is_leaf=True)
        leaf1.shift(LEFT * 4 + DOWN * 2)
        leaf1_data = Text("📄", font_size=16)
        leaf1_data.next_to(leaf1.key_texts[0], RIGHT, buff=0.05)
        
        leaf2 = BTreeNode([30], is_leaf=True)
        leaf2.shift(LEFT * 1 + DOWN * 2)
        leaf2_data = Text("📄", font_size=16)
        leaf2_data.next_to(leaf2.key_texts[0], RIGHT, buff=0.05)
        
        leaf3 = BTreeNode([50], is_leaf=True)
        leaf3.shift(RIGHT * 1 + DOWN * 2)
        leaf3_data = Text("📄", font_size=16)
        leaf3_data.next_to(leaf3.key_texts[0], RIGHT, buff=0.05)
        
        leaf4 = BTreeNode([70], is_leaf=True)
        leaf4.shift(RIGHT * 4 + DOWN * 2)
        leaf4_data = Text("📄", font_size=16)
        leaf4_data.next_to(leaf4.key_texts[0], RIGHT, buff=0.05)
        
        nodes = VGroup(root, internal1, internal2, leaf1, leaf2, leaf3, leaf4)
        data_icons = VGroup(root_data, int1_data, int2_data, leaf1_data, leaf2_data, leaf3_data, leaf4_data)
        
        # Edges
        edges = VGroup(
            Line(root.bg.get_bottom() + LEFT * 0.3, internal1.bg.get_top(), color=C.EDGE, stroke_width=2),
            Line(root.bg.get_bottom() + RIGHT * 0.3, internal2.bg.get_top(), color=C.EDGE, stroke_width=2),
            Line(internal1.bg.get_bottom() + LEFT * 0.2, leaf1.bg.get_top(), color=C.EDGE, stroke_width=2),
            Line(internal1.bg.get_bottom() + RIGHT * 0.2, leaf2.bg.get_top(), color=C.EDGE, stroke_width=2),
            Line(internal2.bg.get_bottom() + LEFT * 0.2, leaf3.bg.get_top(), color=C.EDGE, stroke_width=2),
            Line(internal2.bg.get_bottom() + RIGHT * 0.2, leaf4.bg.get_top(), color=C.EDGE, stroke_width=2),
        )
        
        self.play(FadeIn(btree_label), FadeIn(nodes), Create(edges), FadeIn(data_icons))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # HIGHLIGHT WASTED SPACE
        # ══════════════════════════════════════════════════════════════════════
        narration2 = self.narrate(
            "This wastes space in internal nodes.",
            "We can do better."
        )
        self.play(FadeOut(narration2))
        
        # Highlight internal node data as wasteful
        waste_boxes = VGroup()
        for data_icon in [root_data, int1_data, int2_data]:
            box = SurroundingRectangle(data_icon, color=C.ERROR, buff=0.05)
            waste_boxes.add(box)
        
        self.play(
            LaggedStart(*[Create(box) for box in waste_boxes], lag_ratio=0.2)
        )
        
        waste_label = Text("Wasted space!", font=F.CODE_FONT, font_size=F.CAPTION, color=C.ERROR)
        waste_label.next_to(root, RIGHT, buff=0.5)
        self.play(FadeIn(waste_label))
        
        self.wait(T.ABSORB)
        
        # ══════════════════════════════════════════════════════════════════════
        # FADE DATA FROM INTERNAL NODES
        # ══════════════════════════════════════════════════════════════════════
        narration3 = self.narrate(
            "In a B+ Tree,",
            "internal nodes store only keys."
        )
        
        # Fade out internal data icons
        self.play(
            FadeOut(root_data),
            FadeOut(int1_data),
            FadeOut(int2_data),
            FadeOut(waste_boxes),
            FadeOut(waste_label),
            FadeOut(narration3)
        )
        
        # Update label
        bplus_label = Text("B+ Tree", font=F.MAIN_FONT, font_size=F.SUBHEADING, color=C.SUCCESS)
        bplus_label.move_to(btree_label)
        
        self.play(Transform(btree_label, bplus_label))
        
        # Keys only label for internal
        keys_only = Text("Keys only!", font=F.CODE_FONT, font_size=F.CAPTION, color=C.SUCCESS)
        keys_only.next_to(root, RIGHT, buff=0.3)
        self.play(FadeIn(keys_only))
        
        # Data in leaves label
        data_here = Text("Data here!", font=F.CODE_FONT, font_size=F.CAPTION, color=C.DATA)
        data_here.next_to(VGroup(leaf1, leaf4), DOWN, buff=0.2)
        self.play(FadeIn(data_here))
        
        self.wait(T.CONTEMPLATE)
        self.scene_transition()


# ══════════════════════════════════════════════════════════════════════════════
# SCENE K — B+ Tree Structure
# ══════════════════════════════════════════════════════════════════════════════

class SceneK_BPlusStructure(BTreeBaseScene):
    """
    Animation: B+ Tree structure in detail.
    
    Key concepts:
    - Internal nodes: keys only
    - Leaf nodes: all data
    - Higher fanout
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════════════
        title = self.create_title("B+ Tree Structure", "هيكل شجرة B+")
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # NARRATION
        # ══════════════════════════════════════════════════════════════════════
        narration1 = self.narrate(
            "In a B+ Tree,",
            "internal nodes store only keys."
        )
        self.play(FadeOut(narration1))
        
        # ══════════════════════════════════════════════════════════════════════
        # BUILD B+ TREE
        # ══════════════════════════════════════════════════════════════════════
        
        # Root (internal)
        root = BTreeNode([30, 60], is_leaf=False)
        root.shift(UP * 2)
        root_label = Text("INTERNAL", font=F.CODE_FONT, font_size=F.TINY, color=C.INTERNAL_NODE)
        root_label.next_to(root, UP, buff=0.1)
        
        self.play(FadeIn(root), FadeIn(root_label))
        
        # Internal nodes
        int1 = BTreeNode([15], is_leaf=False)
        int1.shift(LEFT * 3.5 + UP * 0.3)
        
        int2 = BTreeNode([45], is_leaf=False)
        int2.shift(UP * 0.3)
        
        int3 = BTreeNode([75], is_leaf=False)
        int3.shift(RIGHT * 3.5 + UP * 0.3)
        
        internals = VGroup(int1, int2, int3)
        
        # Edges to internals
        root_edges = VGroup(
            Line(root.bg.get_bottom() + LEFT * 0.4, int1.bg.get_top(), color=C.EDGE, stroke_width=2),
            Line(root.bg.get_bottom(), int2.bg.get_top(), color=C.EDGE, stroke_width=2),
            Line(root.bg.get_bottom() + RIGHT * 0.4, int3.bg.get_top(), color=C.EDGE, stroke_width=2),
        )
        
        self.play(FadeIn(internals), Create(root_edges))
        self.wait(T.BEAT)
        
        # Leaf nodes with data
        narration2 = self.narrate(
            "All actual data records",
            "are stored only in leaf nodes."
        )
        self.play(FadeOut(narration2))
        
        leaves = VGroup()
        leaf_data = [
            ([10, 20], LEFT * 5 + DOWN * 1.5),
            ([30, 40], LEFT * 2 + DOWN * 1.5),
            ([50, 55], RIGHT * 1 + DOWN * 1.5),
            ([60, 70], RIGHT * 4 + DOWN * 1.5),
        ]
        
        for keys, pos in leaf_data:
            leaf = BTreeNode(keys, is_leaf=True)
            leaf.move_to(pos)
            leaves.add(leaf)
        
        # Leaf label
        leaf_label = Text("LEAF (Data)", font=F.CODE_FONT, font_size=F.TINY, color=C.LEAF_NODE)
        leaf_label.next_to(leaves, DOWN, buff=0.2)
        
        # Edges to leaves
        leaf_edges = VGroup(
            Line(int1.bg.get_bottom() + LEFT * 0.15, leaves[0].bg.get_top(), color=C.EDGE, stroke_width=2),
            Line(int1.bg.get_bottom() + RIGHT * 0.15, leaves[1].bg.get_top(), color=C.EDGE, stroke_width=2),
            Line(int2.bg.get_bottom() + LEFT * 0.15, leaves[1].bg.get_top(), color=C.EDGE, stroke_width=2),
            Line(int2.bg.get_bottom() + RIGHT * 0.15, leaves[2].bg.get_top(), color=C.EDGE, stroke_width=2),
            Line(int3.bg.get_bottom() + LEFT * 0.15, leaves[2].bg.get_top(), color=C.EDGE, stroke_width=2),
            Line(int3.bg.get_bottom() + RIGHT * 0.15, leaves[3].bg.get_top(), color=C.EDGE, stroke_width=2),
        )
        
        self.play(FadeIn(leaves), FadeIn(leaf_label), Create(leaf_edges))
        
        # ══════════════════════════════════════════════════════════════════════
        # FANOUT BENEFIT
        # ══════════════════════════════════════════════════════════════════════
        narration3 = self.narrate(
            "This makes internal nodes smaller,",
            "allowing more keys per disk block."
        )
        
        # Fanout indicator
        fanout = VGroup(
            Text("Higher Fanout", font=F.MAIN_FONT, font_size=F.LABEL, color=C.SUCCESS),
            Text("→ Shorter Tree", font=F.MAIN_FONT, font_size=F.LABEL, color=C.SUCCESS),
            Text("→ Fewer Disk Reads", font=F.MAIN_FONT, font_size=F.LABEL, color=C.SUCCESS),
        )
        fanout.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        fanout.to_corner(DR, buff=0.5)
        
        self.play(LaggedStart(*[FadeIn(f) for f in fanout], lag_ratio=0.3))
        
        self.wait(T.CONTEMPLATE)
        self.play(FadeOut(narration3))
        self.scene_transition()


# ══════════════════════════════════════════════════════════════════════════════
# SCENE L — Leaf Node Linking
# ══════════════════════════════════════════════════════════════════════════════

class SceneL_LeafLinking(BTreeBaseScene):
    """
    Animation: B+ Tree leaf linking for range queries.
    
    Key concepts:
    - Horizontal leaf links
    - Sorted leaf order
    - Sequential scan capability
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════════════
        title = self.create_title("Leaf Node Linking", "ربط العقد الورقية")
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # NARRATION
        # ══════════════════════════════════════════════════════════════════════
        narration1 = self.narrate(
            "B+ Trees add one more optimization.",
            "All leaf nodes are linked together in sorted order."
        )
        self.play(FadeOut(narration1))
        
        # ══════════════════════════════════════════════════════════════════════
        # B+ TREE WITH LEAVES
        # ══════════════════════════════════════════════════════════════════════
        
        # Simplified tree - just root and leaves
        root = BTreeNode([30, 60], is_leaf=False)
        root.shift(UP * 1.5)
        
        leaves = VGroup()
        leaf_configs = [
            ([10, 20], LEFT * 4.5),
            ([30, 40], LEFT * 1.5),
            ([50, 55], RIGHT * 1.5),
            ([60, 70], RIGHT * 4.5),
        ]
        
        for keys, x_offset in leaf_configs:
            leaf = BTreeNode(keys, is_leaf=True)
            leaf.shift(DOWN * 0.8 + x_offset)
            leaves.add(leaf)
        
        # Edges
        edges = VGroup()
        for i in range(4):
            start = root.bg.get_bottom() + LEFT * 0.5 + RIGHT * i * 0.35
            edge = Line(start, leaves[i].bg.get_top(), color=C.EDGE, stroke_width=2)
            edges.add(edge)
        
        self.play(FadeIn(root), FadeIn(leaves), Create(edges))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # ADD LEAF LINKS
        # ══════════════════════════════════════════════════════════════════════
        
        leaf_links = VGroup()
        for i in range(len(leaves) - 1):
            link = Arrow(
                leaves[i].bg.get_right(),
                leaves[i + 1].bg.get_left(),
                color=C.LEAF_LINK,
                stroke_width=3,
                buff=0.1,
                max_tip_length_to_length_ratio=0.2
            )
            leaf_links.add(link)
        
        # Animate links appearing
        self.play(
            LaggedStart(*[GrowArrow(link) for link in leaf_links], lag_ratio=0.3),
            run_time=T.SLOW
        )
        
        # Highlight the chain
        self.play(
            *[link.animate.set_color(C.SUCCESS) for link in leaf_links],
            *[leaf.bg.animate.set_stroke(color=C.SUCCESS, width=3) for leaf in leaves],
            run_time=T.NORMAL
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # SEQUENTIAL TRAVERSAL DEMO
        # ══════════════════════════════════════════════════════════════════════
        narration2 = self.narrate(
            "This makes range queries extremely efficient."
        )
        self.play(FadeOut(narration2))
        
        # Cursor moving through leaves
        cursor = Dot(radius=0.12, color=C.RANGE_QUERY)
        cursor.move_to(leaves[0].bg.get_center())
        
        self.play(FadeIn(cursor, scale=0.5))
        
        # Move through all leaves
        for i in range(len(leaves)):
            if i > 0:
                # Move along link
                self.play(
                    cursor.animate.move_to(leaf_links[i-1].get_center()),
                    run_time=T.FAST
                )
                self.play(
                    cursor.animate.move_to(leaves[i].bg.get_center()),
                    run_time=T.FAST
                )
            
            # Highlight current leaf
            self.play(
                leaves[i].bg.animate.set_fill(color=C.RANGE_QUERY, opacity=A.DIMMED),
                run_time=T.FAST
            )
        
        # Sequential scan complete
        scan_complete = Text(
            "✓ Sequential Scan Complete",
            font=F.MAIN_FONT,
            font_size=F.LABEL,
            color=C.SUCCESS
        )
        scan_complete.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(scan_complete, scale=0.8))
        
        self.wait(T.CONTEMPLATE)
        self.scene_transition()
