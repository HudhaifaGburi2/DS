"""
Scene 02: B-Tree Structure
==========================

Deep dive into B-Tree anatomy and operations:
- Node structure (keys and pointers)
- Tree properties (balanced, sorted)
- Search operation
- Insert with split

Narrative Arc:
1. Show node anatomy
2. Build a simple B-Tree
3. Demonstrate search path
4. Show insert and split
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import C, T, F, L, DS, A
from base_scenes import TreeScene
from components.nodes import BTreeNode, KeyCell
from components.edges import TreeEdge
from components.disk import DiskPage
from utils.text_helpers import create_bilingual, create_step_label


class Scene02_BTreeStructure(TreeScene):
    """
    B-Tree structure and operations.
    
    Visual focus: Disk pages as nodes, clear key ordering,
    logarithmic search path highlighting.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "بنية B-Tree",
            "B-Tree Structure"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: NODE ANATOMY
        # ══════════════════════════════════════════════════════════════════════
        
        section = self.create_section_header("Node Anatomy")
        self.play(Write(section))
        self.wait_beat()
        
        # Create a single node for explanation
        demo_node = BTreeNode(keys=[10, 20, 30], max_keys=4)
        demo_node.scale(1.5)
        demo_node.shift(UP * 0.5)
        
        self.play(demo_node.animate_create())
        self.wait_beat()
        
        # Annotate keys
        keys_label = Text("Keys (sorted)", font=F.CODE, color=C.BTREE_KEY_ACTIVE).scale(F.SIZE_LABEL)
        keys_label.next_to(demo_node, UP, buff=L.SPACING_MD)
        
        keys_arrow = Arrow(
            keys_label.get_bottom(),
            demo_node.key_cells.get_top(),
            color=C.BTREE_KEY_ACTIVE,
            stroke_width=2
        )
        
        self.play(Write(keys_label), Create(keys_arrow))
        self.wait_beat()
        
        # Annotate pointers
        pointers_label = Text("Child Pointers", font=F.CODE, color=C.BTREE_POINTER).scale(F.SIZE_LABEL)
        pointers_label.next_to(demo_node, DOWN, buff=L.SPACING_LG)
        
        self.play(Write(pointers_label))
        
        # Show pointer regions
        pointer_regions = VGroup()
        regions_text = ["< 10", "10-20", "20-30", "> 30"]
        
        for i, text in enumerate(regions_text):
            region = Text(text, font=F.CODE, color=C.BTREE_POINTER).scale(F.SIZE_TINY)
            # Position under each pointer space
            x_offset = -1.2 + i * 0.8
            region.move_to(demo_node.get_center() + DOWN * 1.2 + RIGHT * x_offset)
            pointer_regions.add(region)
        
        self.play(
            LaggedStart(
                *[FadeIn(r, shift=UP * 0.1) for r in pointer_regions],
                lag_ratio=0.15
            )
        )
        self.wait_absorb()
        
        # Key property
        property_text = create_bilingual(
            "المفاتيح مرتبة دائماً",
            "Keys are always sorted",
            color_ar=C.SUCCESS,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        property_text.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(FadeIn(property_text))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: BUILD A TREE
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        section2 = self.create_section_header("Building a B-Tree")
        self.play(Write(section2))
        
        # Root node
        root = BTreeNode(keys=[17, 35], max_keys=3)
        root.move_to(UP * 2.5)
        
        # Level 1 nodes
        child1 = BTreeNode(keys=[5, 10], max_keys=3, is_leaf=True)
        child2 = BTreeNode(keys=[20, 25, 30], max_keys=3, is_leaf=True)
        child3 = BTreeNode(keys=[40, 45], max_keys=3, is_leaf=True)
        
        child1.move_to(LEFT * 4 + UP * 0.5)
        child2.move_to(ORIGIN + UP * 0.5)
        child3.move_to(RIGHT * 4 + UP * 0.5)
        
        # Edges
        edge1 = TreeEdge(root.get_bottom() + LEFT * 0.4, child1.get_top())
        edge2 = TreeEdge(root.get_bottom(), child2.get_top())
        edge3 = TreeEdge(root.get_bottom() + RIGHT * 0.4, child3.get_top())
        
        # Animate building
        self.play(root.animate_create())
        self.wait_beat()
        
        self.play(
            Create(edge1.line),
            Create(edge2.line),
            Create(edge3.line)
        )
        
        self.play(
            child1.animate_create(),
            child2.animate_create(),
            child3.animate_create()
        )
        self.wait_absorb()
        
        # Tree properties
        props = VGroup(
            Text("✓ Balanced: Same depth for all leaves", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
            Text("✓ Sorted: In-order traversal gives sorted keys", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
            Text("✓ Logarithmic: O(log n) search", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
        )
        props.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        props.to_edge(DOWN, buff=L.MARGIN_MD)
        
        self.play(
            LaggedStart(
                *[FadeIn(p, shift=LEFT * 0.2) for p in props],
                lag_ratio=0.2
            )
        )
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: SEARCH OPERATION
        # ══════════════════════════════════════════════════════════════════════
        
        self.play(FadeOut(props), FadeOut(section2))
        
        search_title = self.create_section_header("Search: Finding key 25")
        self.play(Write(search_title))
        
        # Step 1: Check root
        step1 = Text("1. Compare with root [17, 35]", font=F.CODE, color=C.TEXT_ACCENT).scale(F.SIZE_CAPTION)
        step1.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(Write(step1))
        self.play(root.animate_highlight(C.IO_READ))
        
        # Highlight comparison
        self.play(
            root.key_cells[0].highlight(C.BTREE_KEY_ACTIVE),
            run_time=T.FAST
        )
        self.wait_beat(0.5)
        
        compare1 = Text("25 > 17 ✓", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
        compare1.next_to(root, RIGHT, buff=L.SPACING_SM)
        self.play(FadeIn(compare1))
        
        self.play(
            root.key_cells[1].highlight(C.BTREE_KEY_ACTIVE),
            run_time=T.FAST
        )
        
        compare2 = Text("25 < 35 ✓", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
        compare2.next_to(compare1, DOWN, buff=0.1)
        self.play(FadeIn(compare2))
        self.wait_beat()
        
        # Step 2: Go to middle child
        step2 = Text("2. Follow middle pointer", font=F.CODE, color=C.TEXT_ACCENT).scale(F.SIZE_CAPTION)
        step2.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(Transform(step1, step2))
        self.play(
            edge2.line.animate.set_color(C.IO_READ).set_stroke(width=4),
            run_time=T.FAST
        )
        self.wait_beat()
        
        # Step 3: Search in leaf
        step3 = Text("3. Found! key 25 in leaf", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_CAPTION)
        step3.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(Transform(step1, step3))
        self.play(child2.animate_highlight(C.IO_READ))
        
        # Find key 25
        self.play(child2.key_cells[1].highlight(C.SUCCESS))
        
        # Flash success
        self.play(Flash(child2.key_cells[1], color=C.SUCCESS, line_length=0.3))
        
        found_label = Text("FOUND!", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_BODY)
        found_label.next_to(child2, RIGHT, buff=L.SPACING_SM)
        self.play(FadeIn(found_label, scale=0.8))
        
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: DISK I/O REALITY
        # ══════════════════════════════════════════════════════════════════════
        
        # Clear highlights
        self.play(
            FadeOut(compare1), FadeOut(compare2),
            FadeOut(found_label), FadeOut(step1),
            FadeOut(search_title)
        )
        
        io_title = self.create_section_header("Disk I/O Reality")
        self.play(Write(io_title))
        
        # Show disk I/O count
        io_counter = VGroup(
            Text("Disk Reads: ", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_CAPTION),
            Text("2", font=F.CODE, color=C.IO_READ).scale(F.SIZE_HEADING)
        )
        io_counter.arrange(RIGHT, buff=L.SPACING_SM)
        io_counter.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(FadeIn(io_counter))
        
        # B-Tree advantage
        advantage = create_bilingual(
            "عمق الشجرة = عدد عمليات القرص",
            "Tree depth = Number of disk I/Os",
            color_ar=C.BTREE_NODE,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        advantage.next_to(io_counter, UP, buff=L.SPACING_MD)
        
        self.play(FadeIn(advantage))
        
        # Complexity note
        complexity = Text(
            "Height ~ log(n) → Very few disk reads!",
            font=F.CODE,
            color=C.SUCCESS
        ).scale(F.SIZE_LABEL)
        complexity.next_to(advantage, UP, buff=L.SPACING_SM)
        
        self.play(FadeIn(complexity, shift=DOWN * 0.1))
        self.wait_contemplate()
