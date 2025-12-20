"""
B-Tree Evolution Animation - Scenes M and Final
================================================

Part 4: Range Queries and Evolution Summary
- Scene M: Range Query Efficiency
- Scene Final: Evolution Timeline
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
# SCENE M — Range Query Efficiency
# ══════════════════════════════════════════════════════════════════════════════

class SceneM_RangeQuery(BTreeBaseScene):
    """
    Animation: Efficient range queries in B+ Trees.
    
    Key concepts:
    - Single tree traversal to first key
    - Sequential leaf scan
    - Minimal disk reads
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════════════
        title = self.create_title("Range Query Efficiency", "كفاءة استعلام النطاق")
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # B+ TREE SETUP
        # ══════════════════════════════════════════════════════════════════════
        
        # Root
        root = BTreeNode([40], is_leaf=False)
        root.shift(UP * 1.8)
        
        # Leaves
        leaves = VGroup()
        leaf_configs = [
            ([10, 20, 30], LEFT * 3),
            ([40, 50, 60], RIGHT * 3),
        ]
        
        for keys, x_offset in leaf_configs:
            leaf = BTreeNode(keys, is_leaf=True)
            leaf.shift(DOWN * 0.5 + x_offset)
            leaves.add(leaf)
        
        # Edges
        edge_left = Line(root.get_pointer_position(0), leaves[0].bg.get_top(), color=C.EDGE, stroke_width=2)
        edge_right = Line(root.get_pointer_position(1), leaves[1].bg.get_top(), color=C.EDGE, stroke_width=2)
        edges = VGroup(edge_left, edge_right)
        
        # Leaf link
        leaf_link = Arrow(
            leaves[0].bg.get_right(),
            leaves[1].bg.get_left(),
            color=C.LEAF_LINK,
            stroke_width=2,
            buff=0.1
        )
        
        tree = VGroup(root, leaves, edges, leaf_link)
        self.play(FadeIn(tree))
        
        # ══════════════════════════════════════════════════════════════════════
        # RANGE QUERY
        # ══════════════════════════════════════════════════════════════════════
        query = VGroup(
            Text("Range Query:", font=F.MAIN_FONT, font_size=F.LABEL, color=C.TEXT_SECONDARY),
            Text("25 to 55", font=F.CODE_FONT, font_size=F.HEADING, color=C.RANGE_QUERY)
        )
        query.arrange(RIGHT, buff=0.3)
        query.to_corner(UR, buff=0.5)
        
        self.play(FadeIn(query, scale=0.8))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # STEP 1: FIND FIRST LEAF
        # ══════════════════════════════════════════════════════════════════════
        narration1 = self.narrate(
            "To scan a range of keys,",
            "the database finds the first leaf once."
        )
        self.play(FadeOut(narration1))
        
        step1 = Text("Step 1: Find first key (25)", font=F.CODE_FONT, font_size=F.CAPTION, color=C.SEARCH_PATH)
        step1.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(step1))
        
        # Highlight root traversal
        self.play(root.bg.animate.set_stroke(color=C.SEARCH_PATH, width=4))
        
        # Compare at root
        compare = Text("25 < 40 → go left", font=F.CODE_FONT, font_size=F.CAPTION, color=C.TEXT_ACCENT)
        compare.next_to(root, RIGHT, buff=0.3)
        self.play(FadeIn(compare))
        self.wait(T.BEAT)
        
        # Go to left leaf
        self.play(
            edge_left.animate.set_color(C.SEARCH_PATH).set_stroke(width=4),
            leaves[0].bg.animate.set_stroke(color=C.SEARCH_PATH, width=4),
            FadeOut(compare)
        )
        
        # Find key 30 (first key >= 25)
        self.play(
            leaves[0].key_texts[2].animate.set_color(C.RANGE_QUERY).scale(1.2),
            run_time=T.FAST
        )
        
        # Disk read counter
        read_counter = VGroup(
            Text("Disk Reads:", font=F.MAIN_FONT, font_size=F.LABEL, color=C.TEXT_SECONDARY),
            Text("2", font=F.CODE_FONT, font_size=F.HEADING, color=C.SUCCESS)
        )
        read_counter.arrange(RIGHT, buff=0.2)
        read_counter.to_corner(DL, buff=0.5)
        self.play(FadeIn(read_counter))
        
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # STEP 2: SEQUENTIAL SCAN
        # ══════════════════════════════════════════════════════════════════════
        self.play(FadeOut(step1))
        
        narration2 = self.narrate(
            "After that, it follows leaf pointers sequentially.",
            "No repeated tree traversal is needed."
        )
        self.play(FadeOut(narration2))
        
        step2 = Text("Step 2: Sequential leaf scan", font=F.CODE_FONT, font_size=F.CAPTION, color=C.LEAF_LINK)
        step2.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(step2))
        
        # Highlight matching keys: 30, 40, 50
        # Key 30 already highlighted
        
        # Follow link to next leaf
        self.play(
            leaf_link.animate.set_color(C.RANGE_QUERY).set_stroke(width=4),
            run_time=T.NORMAL
        )
        
        # Move to second leaf
        self.play(
            leaves[1].bg.animate.set_stroke(color=C.RANGE_QUERY, width=3)
        )
        
        # Highlight keys 40, 50 (within range)
        for i in range(2):
            self.play(
                leaves[1].key_texts[i].animate.set_color(C.RANGE_QUERY).scale(1.2),
                run_time=T.FAST
            )
        
        # Key 60 is out of range - stop
        stop_indicator = Text("60 > 55 → Stop", font=F.CODE_FONT, font_size=F.CAPTION, color=C.ERROR)
        stop_indicator.next_to(leaves[1], RIGHT, buff=0.3)
        self.play(FadeIn(stop_indicator))
        
        # Update disk reads
        new_count = Text("3", font=F.CODE_FONT, font_size=F.HEADING, color=C.SUCCESS)
        new_count.move_to(read_counter[1])
        self.play(Transform(read_counter[1], new_count))
        
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # RESULTS
        # ══════════════════════════════════════════════════════════════════════
        self.play(FadeOut(step2), FadeOut(stop_indicator))
        
        results = VGroup(
            Text("Results: 30, 40, 50", font=F.CODE_FONT, font_size=F.LABEL, color=C.RANGE_QUERY),
            Text("Only 3 disk reads!", font=F.MAIN_FONT, font_size=F.LABEL, color=C.SUCCESS)
        )
        results.arrange(DOWN, buff=0.15)
        results.to_edge(DOWN, buff=0.5)
        
        self.play(FadeIn(results, scale=0.8))
        
        # ══════════════════════════════════════════════════════════════════════
        # WHY B+ TREES DOMINATE
        # ══════════════════════════════════════════════════════════════════════
        narration3 = self.narrate(
            "This is why B+ Trees dominate",
            "modern database indexing."
        )
        
        self.wait(T.CONTEMPLATE)
        self.play(FadeOut(narration3))
        self.scene_transition()


# ══════════════════════════════════════════════════════════════════════════════
# FINAL SCENE — Evolution Timeline
# ══════════════════════════════════════════════════════════════════════════════

class SceneFinal_Timeline(BTreeBaseScene):
    """
    Animation: Complete evolution from tables to B+ Trees.
    
    Key concepts:
    - Evolution summary
    - Timeline visualization
    - Closing statement
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════════════
        title = self.create_title("The Evolution of Database Indexing", "تطور فهرسة قواعد البيانات")
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # TIMELINE SETUP
        # ══════════════════════════════════════════════════════════════════════
        
        # Timeline axis
        timeline = Line(LEFT * 6, RIGHT * 6, color=C.TEXT_TERTIARY, stroke_width=3)
        timeline.shift(DOWN * 0.5)
        
        self.play(Create(timeline))
        
        # Evolution stages
        stages = [
            ("Index Table", LEFT * 5, C.KEY),
            ("Multi-Level", LEFT * 2, C.POINTER),
            ("M-Way Tree", RIGHT * 1, C.INTERNAL_NODE),
            ("B-Tree", RIGHT * 3.5, C.LEAF_NODE),
            ("B+ Tree", RIGHT * 6, C.SUCCESS),
        ]
        
        stage_objects = VGroup()
        
        for i, (name, x_pos, color) in enumerate(stages):
            # Dot on timeline
            dot = Dot(radius=0.15, color=color)
            dot.move_to(timeline.get_start() + RIGHT * (i + 1) * 2.2 + LEFT * 0.5)
            
            # Label
            label = Text(name, font=F.MAIN_FONT, font_size=F.LABEL, color=color)
            label.next_to(dot, UP, buff=0.3)
            
            stage = VGroup(dot, label)
            stage_objects.add(stage)
        
        # ══════════════════════════════════════════════════════════════════════
        # ANIMATE EVOLUTION
        # ══════════════════════════════════════════════════════════════════════
        
        evolution_narrations = [
            "Indexes started as tables.",
            "Tables became multi-level indexes.",
            "Multi-level indexes became trees.",
            "Trees evolved into B-Trees.",
            "And B-Trees evolved into B+ Trees."
        ]
        
        # Progressive reveal
        for i, (stage, narration_text) in enumerate(zip(stage_objects, evolution_narrations)):
            # Narration
            narration = Text(narration_text, font=F.MAIN_FONT, font_size=F.BODY, color=C.TEXT_NARRATION)
            narration.to_edge(DOWN, buff=0.8)
            
            self.play(FadeIn(narration))
            self.play(
                FadeIn(stage[0], scale=0.5),  # Dot
                FadeIn(stage[1], shift=UP * 0.2)  # Label
            )
            
            # Arrow to next stage
            if i < len(stage_objects) - 1:
                next_stage = stage_objects[i + 1]
                arrow = Arrow(
                    stage[0].get_right() + RIGHT * 0.1,
                    next_stage[0].get_left() + LEFT * 0.1,
                    color=C.TEXT_TERTIARY,
                    stroke_width=2,
                    buff=0
                )
                self.play(GrowArrow(arrow), run_time=T.FAST)
            
            self.wait(T.ABSORB)
            self.play(FadeOut(narration))
        
        self.wait(T.BEAT)
        
        # ══════════════════════════════════════════════════════════════════════
        # CLOSING STATEMENT
        # ══════════════════════════════════════════════════════════════════════
        
        # Clear timeline
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != title],
            run_time=T.SCENE_TRANSITION
        )
        
        # Final quote
        closing = VGroup(
            Text("B-Trees balance the structure.", font=F.MAIN_FONT, font_size=F.HEADING, color=C.LEAF_NODE),
            Text("B+ Trees optimize the disk.", font=F.MAIN_FONT, font_size=F.HEADING, color=C.SUCCESS),
        )
        closing.arrange(DOWN, buff=0.4)
        
        self.play(FadeIn(closing[0], shift=UP * 0.3))
        self.wait(T.ABSORB)
        self.play(FadeIn(closing[1], shift=UP * 0.3))
        
        # Final highlight
        self.play(
            closing[1].animate.scale(1.1).set_color(WHITE),
            run_time=T.NORMAL
        )
        
        self.wait(T.CONTEMPLATE)
        
        # ══════════════════════════════════════════════════════════════════════
        # FADE OUT
        # ══════════════════════════════════════════════════════════════════════
        self.play(FadeOut(title), FadeOut(closing), run_time=T.SLOW)
        self.wait(1)


# ══════════════════════════════════════════════════════════════════════════════
# COMPLETE ANIMATION (All Scenes Combined)
# ══════════════════════════════════════════════════════════════════════════════

class CompleteEvolution(BTreeBaseScene):
    """
    Complete B-Tree evolution animation combining all key concepts.
    Duration: ~8-10 minutes
    """
    
    def construct(self):
        # This scene imports and plays each subscene in sequence
        # For production, render individual scenes and concatenate
        
        # Opening
        opening = VGroup(
            Text("B-Tree Evolution", font=F.MAIN_FONT, font_size=48, color=C.TEXT_PRIMARY),
            Text("From Index Tables to B+ Trees", font=F.MAIN_FONT, font_size=28, color=C.TEXT_SECONDARY),
        )
        opening.arrange(DOWN, buff=0.4)
        
        self.play(FadeIn(opening, scale=0.8), run_time=T.SLOW)
        self.wait(T.CONTEMPLATE)
        self.play(FadeOut(opening), run_time=T.NORMAL)
        
        # Chapter markers
        chapters = [
            "Part 1: Disk Storage & Indexing",
            "Part 2: M-Way Trees",
            "Part 3: B-Tree Construction",
            "Part 4: B+ Tree Optimization",
            "Part 5: Range Queries",
        ]
        
        for chapter in chapters:
            chapter_text = Text(chapter, font=F.MAIN_FONT, font_size=F.HEADING, color=C.TEXT_ACCENT)
            self.play(FadeIn(chapter_text, shift=RIGHT * 0.5))
            self.wait(T.ABSORB)
            self.play(FadeOut(chapter_text, shift=LEFT * 0.5))
        
        # Closing
        closing = Text(
            "Thank you for watching",
            font=F.MAIN_FONT,
            font_size=F.HEADING,
            color=C.TEXT_PRIMARY
        )
        self.play(FadeIn(closing, scale=0.8))
        self.wait(T.CONTEMPLATE)
        self.play(FadeOut(closing))
