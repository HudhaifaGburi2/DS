"""
B-Tree Evolution - Complete Animation
=====================================

Professional all-in-one animation covering:
1. Disk Storage & Indexing
2. Index Tables & Binary Search
3. M-Way Tree Evolution
4. B-Tree Bottom-Up Growth
5. B+ Tree Optimization
6. Range Query Efficiency

Duration: ~8-10 minutes
"""

from manim import *
from config import C, T, S, F, A, L
from components import DiskBlock, IndexEntry, BTreeNode, DiskSurface

# ══════════════════════════════════════════════════════════════════════════════
# COMPLETE B-TREE EVOLUTION ANIMATION
# ══════════════════════════════════════════════════════════════════════════════

class BTreeEvolution_Complete(Scene):
    """
    Complete professional animation of B-Tree evolution.
    Smooth transitions between all concepts.
    """
    
    def setup(self):
        self.camera.background_color = C.BACKGROUND
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # OPENING
        # ══════════════════════════════════════════════════════════════════════
        self.play_opening()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: DISK STORAGE
        # ══════════════════════════════════════════════════════════════════════
        self.play_disk_storage()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: INDEX TABLE
        # ══════════════════════════════════════════════════════════════════════
        self.play_index_table()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: BINARY SEARCH
        # ══════════════════════════════════════════════════════════════════════
        self.play_binary_search()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: INDEX GROWTH PROBLEM
        # ══════════════════════════════════════════════════════════════════════
        self.play_index_growth()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: M-WAY TREE EVOLUTION
        # ══════════════════════════════════════════════════════════════════════
        self.play_mway_evolution()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 6: B-TREE GROWTH
        # ══════════════════════════════════════════════════════════════════════
        self.play_btree_growth()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 7: B+ TREE OPTIMIZATION
        # ══════════════════════════════════════════════════════════════════════
        self.play_bplus_tree()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 8: RANGE QUERIES
        # ══════════════════════════════════════════════════════════════════════
        self.play_range_query()
        
        # ══════════════════════════════════════════════════════════════════════
        # FINALE: EVOLUTION TIMELINE
        # ══════════════════════════════════════════════════════════════════════
        self.play_finale()
    
    # ══════════════════════════════════════════════════════════════════════════
    # HELPERS
    # ══════════════════════════════════════════════════════════════════════════
    
    def smooth_transition(self):
        """Smooth fade transition between scenes"""
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.6)
        self.wait(0.3)
    
    def show_chapter(self, number: int, title: str, arabic: str = None):
        """Show chapter card"""
        chapter = VGroup(
            Text(f"Part {number}", font_size=24, color=C.TEXT_SECONDARY),
            Text(title, font_size=36, color=C.TEXT_PRIMARY),
        )
        if arabic:
            chapter.add(Text(arabic, font_size=28, color=C.TEXT_ACCENT))
        chapter.arrange(DOWN, buff=0.3)
        
        self.play(FadeIn(chapter, scale=0.9))
        self.wait(1.5)
        self.play(FadeOut(chapter, shift=UP * 0.3))
        self.wait(0.3)
    
    def narrate(self, *lines):
        """Show narration text"""
        narration = VGroup(*[
            Text(line, font_size=24, color=C.TEXT_NARRATION)
            for line in lines
        ])
        narration.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        narration.to_edge(DOWN, buff=0.6)
        
        if narration.width > 12:
            narration.scale(12 / narration.width)
        
        self.play(FadeIn(narration, shift=UP * 0.2))
        self.wait(len(lines) * 1.8)
        return narration
    
    # ══════════════════════════════════════════════════════════════════════════
    # OPENING
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_opening(self):
        """Opening title sequence"""
        # Main title
        title = Text("B-Tree Evolution", font_size=52, color=C.TEXT_PRIMARY)
        subtitle = Text("From Index Tables to B+ Trees", font_size=28, color=C.TEXT_SECONDARY)
        arabic = Text("تطور أشجار البحث في قواعد البيانات", font_size=32, color=C.TEXT_ACCENT)
        
        titles = VGroup(title, subtitle, arabic).arrange(DOWN, buff=0.4)
        
        self.play(FadeIn(titles, scale=0.85), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(titles, shift=UP * 0.5), run_time=0.8)
        self.wait(0.5)
    
    # ══════════════════════════════════════════════════════════════════════════
    # ACT 1: DISK STORAGE
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_disk_storage(self):
        """Disk storage visualization"""
        self.show_chapter(1, "Writing Data to Disk", "كتابة البيانات إلى القرص")
        
        # Disk surface
        disk_bg = RoundedRectangle(
            width=10, height=2.5,
            color=C.DISK_SURFACE,
            fill_opacity=0.2,
            corner_radius=0.15
        )
        disk_bg.shift(DOWN * 0.5)
        
        disk_label = Text("DISK", font_size=20, color=C.TEXT_SECONDARY)
        disk_label.next_to(disk_bg, UP, buff=0.1)
        
        # Create blocks
        blocks = VGroup()
        for i in range(4):
            block = RoundedRectangle(
                width=1.8, height=1.6,
                color=C.DISK_BLOCK,
                fill_opacity=0.3,
                corner_radius=0.1
            )
            block.shift(LEFT * 4.5 + RIGHT * i * 2.5 + DOWN * 0.5)
            
            addr = Text(f"Block {i+1}", font_size=14, color=C.POINTER)
            addr.next_to(block, DOWN, buff=0.1)
            
            blocks.add(VGroup(block, addr))
        
        self.play(FadeIn(disk_bg), Write(disk_label))
        self.play(LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.15))
        
        # Narration
        narration = self.narrate(
            "When a record is inserted into a database,",
            "it is written to disk in blocks."
        )
        
        # Records falling into blocks
        records = [
            (101, 0), (205, 0),
            (312, 1), (450, 1),
            (523, 2), (611, 2),
            (720, 3), (835, 3),
        ]
        
        self.play(FadeOut(narration))
        
        for record_id, block_idx in records:
            rec = Text(str(record_id), font_size=18, color=C.DATA)
            rec.move_to(UP * 3)
            
            # Target position in block
            block = blocks[block_idx][0]
            offset = UP * 0.3 if len([r for r, b in records[:records.index((record_id, block_idx))] if b == block_idx]) == 0 else DOWN * 0.2
            target = block.get_center() + offset
            
            self.play(
                FadeIn(rec),
                rec.animate.move_to(target),
                run_time=0.5,
                rate_func=rate_functions.ease_out_cubic
            )
        
        narration2 = self.narrate(
            "The database remembers the block address",
            "where each record is stored."
        )
        
        # Highlight addresses
        self.play(
            *[blocks[i][1].animate.set_color(C.HIGHLIGHT).scale(1.2) for i in range(4)],
            run_time=0.6
        )
        self.wait(0.8)
        self.play(
            *[blocks[i][1].animate.set_color(C.POINTER).scale(1/1.2) for i in range(4)],
            run_time=0.4
        )
        
        self.play(FadeOut(narration2))
        self.smooth_transition()
    
    # ══════════════════════════════════════════════════════════════════════════
    # ACT 2: INDEX TABLE
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_index_table(self):
        """Index table creation"""
        self.show_chapter(2, "Building the Index", "بناء الفهرس")
        
        # Header
        header = VGroup(
            Text("Key", font_size=22, color=C.KEY),
            Text("Block", font_size=22, color=C.POINTER)
        )
        header.arrange(RIGHT, buff=1.5)
        header.shift(UP * 2.5)
        
        self.play(Write(header))
        
        # Index entries
        index_data = [(100, 1), (200, 1), (300, 2), (400, 2), (500, 3), (600, 3)]
        
        entries = VGroup()
        for i, (key, block) in enumerate(index_data):
            key_box = Rectangle(width=1.2, height=0.5, color=C.KEY, fill_opacity=0.2)
            key_text = Text(str(key), font_size=18, color=C.KEY)
            key_text.move_to(key_box)
            
            ptr_box = Rectangle(width=1.2, height=0.5, color=C.POINTER, fill_opacity=0.1)
            ptr_box.next_to(key_box, RIGHT, buff=0)
            ptr_text = Text(f"→{block}", font_size=16, color=C.POINTER)
            ptr_text.move_to(ptr_box)
            
            entry = VGroup(key_box, key_text, ptr_box, ptr_text)
            entry.shift(UP * (1.8 - i * 0.6))
            entries.add(entry)
        
        self.play(LaggedStart(*[FadeIn(e) for e in entries], lag_ratio=0.12))
        
        narration = self.narrate(
            "The database builds an indexing table:",
            "each entry has a key and a pointer to a disk block."
        )
        
        self.wait(1)
        self.play(FadeOut(narration))
        
        # Show sorted property
        narration2 = self.narrate("The index is always kept sorted by key.")
        
        for entry in entries:
            self.play(
                entry[0].animate.set_stroke(color=C.SUCCESS, width=3),
                entry[1].animate.set_color(C.SUCCESS),
                run_time=0.2
            )
        
        self.wait(1)
        self.play(FadeOut(narration2))
        self.smooth_transition()
    
    # ══════════════════════════════════════════════════════════════════════════
    # ACT 3: BINARY SEARCH
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_binary_search(self):
        """Binary search visualization"""
        self.show_chapter(3, "Binary Search in Index", "البحث الثنائي")
        
        # Create index
        keys = [100, 200, 300, 400, 500, 600, 700, 800]
        entries = VGroup()
        
        for i, key in enumerate(keys):
            box = Rectangle(width=1.5, height=0.45, color=C.KEY, fill_opacity=0.2)
            text = Text(str(key), font_size=18, color=C.KEY)
            text.move_to(box)
            entry = VGroup(box, text)
            entry.shift(LEFT * 3.5 + UP * (2 - i * 0.55))
            entries.add(entry)
        
        self.play(FadeIn(entries))
        
        # Query
        query = VGroup(
            Text("Search:", font_size=20, color=C.TEXT_SECONDARY),
            Text("500", font_size=28, color=C.SELECTED)
        )
        query.arrange(RIGHT, buff=0.3)
        query.to_corner(UR, buff=0.6)
        
        self.play(FadeIn(query, scale=0.8))
        
        narration = self.narrate(
            "Because the index is sorted,",
            "binary search finds keys efficiently."
        )
        self.play(FadeOut(narration))
        
        # Binary search animation
        # Step 1: highlight middle (400)
        range_box = SurroundingRectangle(entries, color=C.SEARCH_PATH, buff=0.1)
        self.play(Create(range_box))
        
        self.play(
            entries[3][0].animate.set_fill(color=C.SELECTED, opacity=0.5),
            entries[3][1].animate.set_color(WHITE),
            run_time=0.5
        )
        
        compare1 = Text("400 < 500 → go right", font_size=16, color=C.TEXT_ACCENT)
        compare1.next_to(entries[3], RIGHT, buff=0.5)
        self.play(FadeIn(compare1))
        self.wait(0.8)
        
        # Reset and narrow
        self.play(
            entries[3][0].animate.set_fill(color=C.KEY, opacity=0.2),
            entries[3][1].animate.set_color(C.KEY),
            FadeOut(compare1),
            FadeOut(range_box)
        )
        
        # Step 2: highlight 600
        range_box2 = SurroundingRectangle(VGroup(*entries[4:]), color=C.SEARCH_PATH, buff=0.1)
        self.play(Create(range_box2))
        
        self.play(
            entries[5][0].animate.set_fill(color=C.SELECTED, opacity=0.5),
            entries[5][1].animate.set_color(WHITE),
            run_time=0.5
        )
        
        compare2 = Text("600 > 500 → go left", font_size=16, color=C.TEXT_ACCENT)
        compare2.next_to(entries[5], RIGHT, buff=0.5)
        self.play(FadeIn(compare2))
        self.wait(0.8)
        
        self.play(
            entries[5][0].animate.set_fill(color=C.KEY, opacity=0.2),
            entries[5][1].animate.set_color(C.KEY),
            FadeOut(compare2),
            FadeOut(range_box2)
        )
        
        # Step 3: Found 500!
        self.play(
            entries[4][0].animate.set_fill(color=C.SUCCESS, opacity=0.6),
            entries[4][1].animate.set_color(WHITE).scale(1.2),
            run_time=0.6
        )
        
        found = Text("✓ Found!", font_size=20, color=C.SUCCESS)
        found.next_to(entries[4], RIGHT, buff=0.5)
        self.play(FadeIn(found, scale=0.8))
        
        # Disk read
        disk_icon = Text("💾 1 Disk Read", font_size=20, color=C.SUCCESS)
        disk_icon.to_corner(DR, buff=0.6)
        self.play(FadeIn(disk_icon))
        
        self.wait(1.5)
        self.smooth_transition()
    
    # ══════════════════════════════════════════════════════════════════════════
    # ACT 4: INDEX GROWTH PROBLEM
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_index_growth(self):
        """Index growth problem"""
        self.show_chapter(4, "The Growth Problem", "مشكلة النمو")
        
        # Memory boundary
        memory_line = Line(LEFT * 6, RIGHT * 6, color=C.MEMORY, stroke_width=3)
        memory_label = Text("MEMORY", font_size=18, color=C.MEMORY)
        memory_label.next_to(memory_line, UL, buff=0.1)
        
        disk_label = Text("DISK", font_size=18, color=C.DISK_BLOCK)
        disk_label.next_to(memory_line, DL, buff=0.1)
        
        self.play(Create(memory_line), Write(memory_label), Write(disk_label))
        
        # Small index
        index = RoundedRectangle(
            width=2, height=1.2,
            color=C.SUCCESS,
            fill_opacity=0.3,
            corner_radius=0.1
        )
        index.shift(UP * 1.5)
        index_label = Text("Index", font_size=18, color=C.SUCCESS)
        index_label.move_to(index)
        
        self.play(FadeIn(VGroup(index, index_label)))
        
        narration = self.narrate(
            "As data grows, the index grows with it."
        )
        
        # Grow index
        for _ in range(3):
            self.play(
                index.animate.scale(1.4),
                index_label.animate.scale(1.1),
                run_time=0.8
            )
        
        self.play(FadeOut(narration))
        
        narration2 = self.narrate(
            "Eventually, the index no longer fits in memory.",
            "Now reading the index requires disk I/O too!"
        )
        
        # Index falls to disk
        self.play(
            VGroup(index, index_label).animate.shift(DOWN * 2.5).set_color(C.ERROR),
            run_time=1.2
        )
        
        warning = Text("⚠ Too many disk accesses!", font_size=22, color=C.ERROR)
        warning.next_to(index, RIGHT, buff=0.5)
        self.play(FadeIn(warning, scale=1.1))
        
        self.wait(1.5)
        self.play(FadeOut(narration2))
        self.smooth_transition()
    
    # ══════════════════════════════════════════════════════════════════════════
    # ACT 5: M-WAY TREE EVOLUTION
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_mway_evolution(self):
        """M-way tree evolution"""
        self.show_chapter(5, "Index Becomes a Tree", "الفهرس يصبح شجرة")
        
        # Index blocks
        blocks = VGroup()
        block_keys = [[100, 200, 300], [400, 500, 600], [700, 800, 900]]
        
        for i, keys in enumerate(block_keys):
            block = RoundedRectangle(
                width=2.2, height=0.8,
                color=C.INTERNAL_NODE,
                fill_opacity=0.3,
                corner_radius=0.08
            )
            block.shift(LEFT * 3 + RIGHT * i * 2.8)
            
            keys_text = Text(" ".join(map(str, keys)), font_size=16, color=C.KEY)
            keys_text.move_to(block)
            
            blocks.add(VGroup(block, keys_text))
        
        self.play(LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.2))
        
        narration = self.narrate(
            "Index blocks hold multiple keys.",
            "Each becomes an M-way search node."
        )
        
        # Transform to tree nodes
        tree_nodes = VGroup()
        for i, keys in enumerate(block_keys):
            node = RoundedRectangle(
                width=2.2, height=0.7,
                color=C.INTERNAL_NODE,
                fill_opacity=0.4,
                corner_radius=0.08
            )
            keys_text = Text(" ".join(map(str, keys)), font_size=16, color=C.KEY)
            keys_text.move_to(node)
            
            # Add pointer dots
            dots = VGroup()
            for j in range(4):
                dot = Dot(radius=0.06, color=C.POINTER)
                dot.move_to(node.get_bottom() + LEFT * 0.8 + RIGHT * j * 0.55)
                dots.add(dot)
            
            tree_node = VGroup(node, keys_text, dots)
            tree_node.shift(LEFT * 3 + RIGHT * i * 2.8 + DOWN * 1)
            tree_nodes.add(tree_node)
        
        self.play(
            *[Transform(blocks[i], tree_nodes[i]) for i in range(3)],
            run_time=1.2
        )
        
        self.play(FadeOut(narration))
        
        narration2 = self.narrate(
            "When index blocks point to each other,",
            "a tree naturally forms."
        )
        
        # Create parent node
        parent = RoundedRectangle(
            width=2, height=0.6,
            color=C.ROOT_NODE,
            fill_opacity=0.4,
            corner_radius=0.08
        )
        parent.shift(UP * 1.5)
        parent_keys = Text("400 700", font_size=16, color=C.KEY)
        parent_keys.move_to(parent)
        parent_group = VGroup(parent, parent_keys)
        
        self.play(FadeIn(parent_group, shift=DOWN * 0.3))
        
        # Edges
        edges = VGroup()
        for i, block in enumerate(blocks):
            edge = Line(
                parent.get_bottom() + LEFT * 0.5 + RIGHT * i * 0.5,
                block[0].get_top(),
                color=C.EDGE,
                stroke_width=2
            )
            edges.add(edge)
        
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.15))
        
        self.wait(1.5)
        self.play(FadeOut(narration2))
        self.smooth_transition()
    
    # ══════════════════════════════════════════════════════════════════════════
    # ACT 6: B-TREE GROWTH
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_btree_growth(self):
        """B-Tree growth and splitting"""
        self.show_chapter(6, "B-Tree: Bottom-Up Growth", "النمو من الأسفل")
        
        # Initial leaf node
        leaf = RoundedRectangle(
            width=3, height=0.8,
            color=C.LEAF_NODE,
            fill_opacity=0.4,
            corner_radius=0.08
        )
        leaf_keys = Text("10  20  30", font_size=20, color=C.KEY)
        leaf_keys.move_to(leaf)
        leaf_group = VGroup(leaf, leaf_keys)
        
        order_text = Text("Order = 4 (max 3 keys)", font_size=16, color=C.TEXT_SECONDARY)
        order_text.to_corner(DR, buff=0.5)
        
        self.play(FadeIn(leaf_group), FadeIn(order_text))
        
        narration = self.narrate(
            "Records are inserted into leaf nodes.",
            "When a node overflows, it splits."
        )
        
        # Insert 40 - overflow!
        insert_label = Text("Insert: 40", font_size=20, color=C.PROMOTED)
        insert_label.to_corner(UL, buff=0.5)
        
        self.play(FadeIn(insert_label))
        self.play(FadeOut(narration))
        
        new_key = Text("40", font_size=20, color=C.PROMOTED)
        new_key.move_to(UP * 2)
        
        self.play(FadeIn(new_key))
        self.play(new_key.animate.next_to(leaf, RIGHT, buff=0.2))
        
        # Overflow indicator
        overflow = SurroundingRectangle(VGroup(leaf_group, new_key), color=C.ERROR, buff=0.1)
        overflow_text = Text("OVERFLOW!", font_size=18, color=C.ERROR)
        overflow_text.next_to(overflow, UP, buff=0.1)
        
        self.play(Create(overflow), FadeIn(overflow_text))
        self.wait(0.8)
        
        # Split animation
        self.play(FadeOut(overflow), FadeOut(overflow_text), FadeOut(new_key))
        
        # Left leaf
        left_leaf = RoundedRectangle(
            width=1.8, height=0.7,
            color=C.LEAF_NODE,
            fill_opacity=0.4,
            corner_radius=0.08
        )
        left_leaf.shift(DOWN * 1 + LEFT * 2)
        left_keys = Text("10  20", font_size=18, color=C.KEY)
        left_keys.move_to(left_leaf)
        
        # Right leaf
        right_leaf = RoundedRectangle(
            width=1.8, height=0.7,
            color=C.LEAF_NODE,
            fill_opacity=0.4,
            corner_radius=0.08
        )
        right_leaf.shift(DOWN * 1 + RIGHT * 2)
        right_keys = Text("30  40", font_size=18, color=C.KEY)
        right_keys.move_to(right_leaf)
        
        self.play(
            FadeOut(leaf_group),
            FadeIn(VGroup(left_leaf, left_keys)),
            FadeIn(VGroup(right_leaf, right_keys)),
            run_time=0.8
        )
        
        # Promote middle key
        promoted = Text("30", font_size=22, color=C.PROMOTED)
        promoted.move_to(ORIGIN)
        
        self.play(FadeIn(promoted))
        self.play(promoted.animate.shift(UP * 1.5), run_time=0.8)
        
        # Create parent
        parent = RoundedRectangle(
            width=1.5, height=0.6,
            color=C.INTERNAL_NODE,
            fill_opacity=0.4,
            corner_radius=0.08
        )
        parent.move_to(promoted)
        
        self.play(
            FadeIn(parent),
            promoted.animate.move_to(parent)
        )
        
        # Edges
        edge_l = Line(parent.get_bottom() + LEFT * 0.3, left_leaf.get_top(), color=C.EDGE, stroke_width=2)
        edge_r = Line(parent.get_bottom() + RIGHT * 0.3, right_leaf.get_top(), color=C.EDGE, stroke_width=2)
        
        self.play(Create(edge_l), Create(edge_r))
        
        success = Text("✓ B-Tree property maintained", font_size=18, color=C.SUCCESS)
        success.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(success))
        
        self.wait(1.5)
        self.smooth_transition()
    
    # ══════════════════════════════════════════════════════════════════════════
    # ACT 7: B+ TREE
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_bplus_tree(self):
        """B+ Tree structure"""
        self.show_chapter(7, "B+ Tree Optimization", "تحسين شجرة B+")
        
        narration = self.narrate(
            "In a B+ Tree, internal nodes store only keys.",
            "All data records are in leaf nodes only."
        )
        
        self.play(FadeOut(narration))
        
        # Root
        root = RoundedRectangle(
            width=2, height=0.6,
            color=C.INTERNAL_NODE,
            fill_opacity=0.4,
            corner_radius=0.08
        )
        root.shift(UP * 2)
        root_keys = Text("30  60", font_size=18, color=C.KEY)
        root_keys.move_to(root)
        
        root_label = Text("Keys only", font_size=14, color=C.INTERNAL_NODE)
        root_label.next_to(root, UP, buff=0.1)
        
        self.play(FadeIn(VGroup(root, root_keys, root_label)))
        
        # Leaves with data
        leaves = VGroup()
        leaf_data = [
            ("10  20", LEFT * 3.5),
            ("30  40", LEFT * 1),
            ("50  55", RIGHT * 1.5),
            ("60  70", RIGHT * 4),
        ]
        
        for keys, x_offset in leaf_data:
            leaf = RoundedRectangle(
                width=1.6, height=0.6,
                color=C.LEAF_NODE,
                fill_opacity=0.4,
                corner_radius=0.08
            )
            leaf.shift(DOWN * 0.5 + x_offset)
            keys_text = Text(keys, font_size=14, color=C.KEY)
            keys_text.move_to(leaf)
            leaves.add(VGroup(leaf, keys_text))
        
        leaf_label = Text("Data here!", font_size=14, color=C.LEAF_NODE)
        leaf_label.next_to(leaves, DOWN, buff=0.2)
        
        # Edges
        edges = VGroup()
        positions = [LEFT * 0.5, ORIGIN, RIGHT * 0.3, RIGHT * 0.6]
        for i, leaf in enumerate(leaves):
            edge = Line(
                root.get_bottom() + positions[min(i, 2)] * 0.5,
                leaf[0].get_top(),
                color=C.EDGE,
                stroke_width=2
            )
            edges.add(edge)
        
        self.play(FadeIn(leaves), FadeIn(leaf_label), Create(edges))
        
        # Leaf links
        narration2 = self.narrate("Leaf nodes are linked for range queries.")
        
        links = VGroup()
        for i in range(len(leaves) - 1):
            link = Arrow(
                leaves[i][0].get_right(),
                leaves[i + 1][0].get_left(),
                color=C.LEAF_LINK,
                stroke_width=2,
                buff=0.08,
                max_tip_length_to_length_ratio=0.2
            )
            links.add(link)
        
        self.play(LaggedStart(*[GrowArrow(l) for l in links], lag_ratio=0.25))
        
        self.wait(1.5)
        self.play(FadeOut(narration2))
        self.smooth_transition()
    
    # ══════════════════════════════════════════════════════════════════════════
    # ACT 8: RANGE QUERIES
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_range_query(self):
        """Range query demonstration"""
        self.show_chapter(8, "Range Query Efficiency", "كفاءة استعلام النطاق")
        
        # Simple B+ tree
        root = RoundedRectangle(width=1.5, height=0.5, color=C.INTERNAL_NODE, fill_opacity=0.4, corner_radius=0.08)
        root.shift(UP * 1.5)
        root_key = Text("40", font_size=18, color=C.KEY)
        root_key.move_to(root)
        
        left_leaf = RoundedRectangle(width=2.2, height=0.5, color=C.LEAF_NODE, fill_opacity=0.4, corner_radius=0.08)
        left_leaf.shift(DOWN * 0.3 + LEFT * 2)
        left_keys = Text("10  20  30", font_size=16, color=C.KEY)
        left_keys.move_to(left_leaf)
        
        right_leaf = RoundedRectangle(width=2.2, height=0.5, color=C.LEAF_NODE, fill_opacity=0.4, corner_radius=0.08)
        right_leaf.shift(DOWN * 0.3 + RIGHT * 2)
        right_keys = Text("40  50  60", font_size=16, color=C.KEY)
        right_keys.move_to(right_leaf)
        
        edge_l = Line(root.get_bottom() + LEFT * 0.2, left_leaf.get_top(), color=C.EDGE, stroke_width=2)
        edge_r = Line(root.get_bottom() + RIGHT * 0.2, right_leaf.get_top(), color=C.EDGE, stroke_width=2)
        
        leaf_link = Arrow(
            left_leaf.get_right(), right_leaf.get_left(),
            color=C.LEAF_LINK, stroke_width=2, buff=0.08
        )
        
        tree = VGroup(root, root_key, left_leaf, left_keys, right_leaf, right_keys, edge_l, edge_r, leaf_link)
        self.play(FadeIn(tree))
        
        # Query
        query = Text("Range: 25 to 55", font_size=22, color=C.RANGE_QUERY)
        query.to_corner(UR, buff=0.5)
        self.play(FadeIn(query, scale=0.8))
        
        narration = self.narrate(
            "Find first key once, then scan leaves sequentially.",
            "No repeated tree traversal needed!"
        )
        
        # Search path
        self.play(root.animate.set_stroke(color=C.SEARCH_PATH, width=3))
        self.play(edge_l.animate.set_color(C.SEARCH_PATH).set_stroke(width=3))
        self.play(left_leaf.animate.set_stroke(color=C.SEARCH_PATH, width=3))
        
        # Cursor scanning
        cursor = Dot(radius=0.1, color=C.RANGE_QUERY)
        cursor.move_to(left_leaf.get_center() + LEFT * 0.6)
        self.play(FadeIn(cursor))
        
        # Scan left leaf (find 30)
        self.play(cursor.animate.move_to(left_leaf.get_center() + RIGHT * 0.6), run_time=0.6)
        
        # Follow link
        self.play(cursor.animate.move_to(leaf_link.get_center()), run_time=0.4)
        self.play(leaf_link.animate.set_color(C.RANGE_QUERY).set_stroke(width=3))
        
        # Scan right leaf
        self.play(cursor.animate.move_to(right_leaf.get_center() + LEFT * 0.6), run_time=0.4)
        self.play(right_leaf.animate.set_stroke(color=C.RANGE_QUERY, width=3))
        self.play(cursor.animate.move_to(right_leaf.get_center() + RIGHT * 0.2), run_time=0.5)
        
        # Result
        result = Text("Results: 30, 40, 50  |  Only 3 disk reads!", font_size=18, color=C.SUCCESS)
        result.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(result, scale=0.9))
        
        self.wait(1.5)
        self.play(FadeOut(narration))
        self.smooth_transition()
    
    # ══════════════════════════════════════════════════════════════════════════
    # FINALE
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_finale(self):
        """Evolution timeline and closing"""
        # Timeline
        timeline = Line(LEFT * 5.5, RIGHT * 5.5, color=C.TEXT_TERTIARY, stroke_width=3)
        timeline.shift(UP * 0.5)
        
        self.play(Create(timeline))
        
        stages = [
            ("Index Table", C.KEY, LEFT * 4.5),
            ("Multi-Level", C.POINTER, LEFT * 2),
            ("M-Way Tree", C.INTERNAL_NODE, RIGHT * 0.5),
            ("B-Tree", C.LEAF_NODE, RIGHT * 3),
            ("B+ Tree", C.SUCCESS, RIGHT * 5.5),
        ]
        
        prev_dot = None
        for name, color, pos in stages:
            dot = Dot(radius=0.12, color=color)
            dot.move_to(timeline.get_start() + RIGHT * (pos[0] + 5.5) / 11 * 11)
            
            label = Text(name, font_size=16, color=color)
            label.next_to(dot, UP, buff=0.25)
            
            self.play(FadeIn(dot, scale=0.5), FadeIn(label, shift=UP * 0.2), run_time=0.6)
            
            if prev_dot:
                arrow = Arrow(
                    prev_dot.get_right(), dot.get_left(),
                    color=C.TEXT_TERTIARY, stroke_width=1.5, buff=0.1
                )
                self.play(GrowArrow(arrow), run_time=0.3)
            
            prev_dot = dot
            self.wait(0.5)
        
        self.wait(1)
        self.smooth_transition()
        
        # Closing quote
        closing1 = Text("B-Trees balance the structure.", font_size=32, color=C.LEAF_NODE)
        closing2 = Text("B+ Trees optimize the disk.", font_size=32, color=C.SUCCESS)
        closing = VGroup(closing1, closing2).arrange(DOWN, buff=0.4)
        
        self.play(FadeIn(closing1, shift=UP * 0.3))
        self.wait(1)
        self.play(FadeIn(closing2, shift=UP * 0.3))
        self.wait(0.5)
        self.play(closing2.animate.scale(1.1).set_color(WHITE), run_time=0.6)
        
        self.wait(2)
        self.play(FadeOut(closing), run_time=1)
        
        # Final thank you
        thanks = Text("Thank you for watching", font_size=28, color=C.TEXT_PRIMARY)
        self.play(FadeIn(thanks, scale=0.8))
        self.wait(2)
        self.play(FadeOut(thanks))
