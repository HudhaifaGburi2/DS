"""
Scene 01: Why Disk-Based Indexing?
==================================

Introduction to the problem:
- Memory is fast but limited and volatile
- Disk is persistent but slow (especially random I/O)
- Need data structures optimized for disk access patterns

Narrative Arc:
1. Show memory vs disk speed gap
2. Introduce the indexing problem
3. Tease the two approaches: B-Tree and LSM-Tree
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import C, T, F, L, DS, A
from base_scenes import DataStructureScene
from components.memory import RAMRegion
from components.disk import DiskRegion
from components.effects import MetricBar
from utils.text_helpers import create_bilingual, create_title_with_icon


class Scene01_WhyDiskIndexing(DataStructureScene):
    """
    Introduction: The disk indexing problem.
    
    Visual metaphor: Speed gap between RAM and Disk,
    leading to need for smart data structures.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "لماذا الفهرسة على القرص؟",
            "Why Disk-Based Indexing?"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: THE STORAGE HIERARCHY
        # ══════════════════════════════════════════════════════════════════════
        
        # Section header
        section = self.create_section_header("The Speed Gap")
        self.play(Write(section))
        self.wait_beat()
        
        # RAM representation
        ram_box = RoundedRectangle(
            width=3, height=1.5,
            color=C.MEMORY_RAM,
            fill_opacity=0.2,
            corner_radius=0.15
        )
        ram_box.shift(LEFT * 3 + UP * 0.5)
        
        ram_label = Text("RAM", font=F.CODE, color=C.MEMORY_RAM).scale(F.SIZE_HEADING)
        ram_label.next_to(ram_box, UP, buff=L.SPACING_TIGHT)
        
        ram_speed = Text("~100 ns", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_CAPTION)
        ram_speed.move_to(ram_box.get_center())
        
        ram_group = VGroup(ram_box, ram_label, ram_speed)
        
        # Disk representation
        disk_box = RoundedRectangle(
            width=3, height=1.5,
            color=C.DISK_SSD,
            fill_opacity=0.2,
            corner_radius=0.15
        )
        disk_box.shift(RIGHT * 3 + UP * 0.5)
        
        disk_label = Text("SSD", font=F.CODE, color=C.DISK_SSD).scale(F.SIZE_HEADING)
        disk_label.next_to(disk_box, UP, buff=L.SPACING_TIGHT)
        
        disk_speed = Text("~100 μs", font=F.CODE, color=C.WARNING).scale(F.SIZE_CAPTION)
        disk_speed.move_to(disk_box.get_center())
        
        disk_group = VGroup(disk_box, disk_label, disk_speed)
        
        # Animate appearance
        self.play(
            FadeIn(ram_group, shift=UP * 0.3),
            FadeIn(disk_group, shift=UP * 0.3)
        )
        self.wait_absorb()
        
        # Show the 1000x gap
        gap_arrow = DoubleArrow(
            ram_box.get_right() + RIGHT * 0.2,
            disk_box.get_left() + LEFT * 0.2,
            color=C.ERROR,
            stroke_width=3
        )
        
        gap_label = Text("1000× slower!", font=F.CODE, color=C.ERROR).scale(F.SIZE_BODY)
        gap_label.next_to(gap_arrow, UP, buff=L.SPACING_TIGHT)
        
        self.play(
            Create(gap_arrow),
            FadeIn(gap_label, scale=0.8)
        )
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: THE PROBLEM
        # ══════════════════════════════════════════════════════════════════════
        
        # Clear and show problem
        self.play(
            FadeOut(section),
            VGroup(ram_group, disk_group, gap_arrow, gap_label).animate.shift(UP * 1.5).scale(0.7)
        )
        
        problem_title = create_bilingual(
            "المشكلة",
            "The Problem",
            color_ar=C.WARNING,
            scale_ar=F.SIZE_HEADING,
            scale_en=F.SIZE_CAPTION
        )
        problem_title.shift(DOWN * 0.5)
        
        self.play(FadeIn(problem_title))
        self.wait_beat()
        
        # Problem statement
        problems = [
            ("الذاكرة سريعة لكن محدودة ومتقلبة", "RAM: Fast but limited & volatile"),
            ("القرص بطيء خصوصاً للقراءة العشوائية", "Disk: Slow, especially random I/O"),
            ("نحتاج هياكل بيانات ذكية", "Need smart data structures"),
        ]
        
        problem_group = VGroup()
        for ar, en in problems:
            item = create_bilingual(
                f"• {ar}",
                f"  {en}",
                scale_ar=F.SIZE_CAPTION,
                scale_en=F.SIZE_LABEL
            )
            problem_group.add(item)
        
        problem_group.arrange(DOWN, buff=L.SPACING_MD, aligned_edge=RIGHT)
        problem_group.next_to(problem_title, DOWN, buff=L.SPACING_LG)
        
        self.play(
            LaggedStart(
                *[FadeIn(p, shift=LEFT * 0.2) for p in problem_group],
                lag_ratio=0.3
            )
        )
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: I/O PATTERNS
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        io_title = self.create_section_header("I/O Access Patterns")
        self.play(Write(io_title))
        
        # Sequential vs Random
        # Sequential I/O
        seq_blocks = VGroup()
        for i in range(5):
            block = Square(
                side_length=0.5,
                fill_color=C.IO_SEQUENTIAL,
                fill_opacity=0.3,
                stroke_color=C.IO_SEQUENTIAL,
                stroke_width=2
            )
            block.shift(LEFT * 3 + RIGHT * i * 0.55)
            seq_blocks.add(block)
        
        seq_blocks.shift(UP * 0.5)
        seq_label = Text("Sequential: FAST ✓", font=F.CODE, color=C.IO_SEQUENTIAL).scale(F.SIZE_CAPTION)
        seq_label.next_to(seq_blocks, DOWN, buff=L.SPACING_SM)
        
        seq_arrow = Arrow(
            seq_blocks[0].get_left() + LEFT * 0.3,
            seq_blocks[-1].get_right() + RIGHT * 0.3,
            color=C.IO_SEQUENTIAL,
            stroke_width=2
        )
        seq_arrow.next_to(seq_blocks, UP, buff=L.SPACING_TIGHT)
        
        # Random I/O
        rand_positions = [
            LEFT * 2.5 + DOWN * 1.5,
            RIGHT * 0.5 + DOWN * 2,
            LEFT * 1 + DOWN * 2.5,
            RIGHT * 2 + DOWN * 1.8,
            LEFT * 0.5 + DOWN * 1.2,
        ]
        
        rand_blocks = VGroup()
        for pos in rand_positions:
            block = Square(
                side_length=0.5,
                fill_color=C.IO_RANDOM,
                fill_opacity=0.3,
                stroke_color=C.IO_RANDOM,
                stroke_width=2
            )
            block.move_to(pos)
            rand_blocks.add(block)
        
        rand_label = Text("Random: SLOW ✗", font=F.CODE, color=C.IO_RANDOM).scale(F.SIZE_CAPTION)
        rand_label.next_to(rand_blocks, DOWN, buff=L.SPACING_SM)
        
        # Random arrows (zigzag)
        rand_path = VGroup()
        for i in range(len(rand_blocks) - 1):
            arrow = Arrow(
                rand_blocks[i].get_center(),
                rand_blocks[i + 1].get_center(),
                color=C.IO_RANDOM,
                stroke_width=1.5,
                buff=0.3
            )
            rand_path.add(arrow)
        
        # Animate
        self.play(
            LaggedStart(
                *[FadeIn(b, scale=0.8) for b in seq_blocks],
                lag_ratio=0.1
            ),
            Create(seq_arrow)
        )
        self.play(Write(seq_label))
        self.wait_beat()
        
        self.play(
            LaggedStart(
                *[FadeIn(b, scale=0.8) for b in rand_blocks],
                lag_ratio=0.1
            )
        )
        self.play(
            LaggedStart(
                *[Create(a) for a in rand_path],
                lag_ratio=0.15
            )
        )
        self.play(Write(rand_label))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: TWO SOLUTIONS TEASER
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        solutions_title = create_bilingual(
            "حلان مختلفان",
            "Two Different Approaches",
            color_ar=C.TEXT_ACCENT,
            scale_ar=F.SIZE_HEADING,
            scale_en=F.SIZE_CAPTION
        )
        solutions_title.shift(UP * 2.5)
        
        self.play(FadeIn(solutions_title))
        
        # B-Tree box
        btree_box = RoundedRectangle(
            width=4, height=2.5,
            color=C.BTREE_NODE,
            fill_opacity=0.1,
            corner_radius=0.2
        )
        btree_box.shift(LEFT * 3)
        
        btree_title = Text("B-Tree", font=F.CODE, color=C.BTREE_NODE).scale(F.SIZE_HEADING)
        btree_title.next_to(btree_box, UP, buff=L.SPACING_TIGHT)
        
        btree_desc = VGroup(
            Text("✓ Read-optimized", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
            Text("✓ In-place updates", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_LABEL),
            Text("• Since 1970s", font=F.CODE, color=C.TEXT_TERTIARY).scale(F.SIZE_LABEL),
        )
        btree_desc.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        btree_desc.move_to(btree_box.get_center())
        
        # LSM-Tree box
        lsm_box = RoundedRectangle(
            width=4, height=2.5,
            color=C.LSM_MEMTABLE,
            fill_opacity=0.1,
            corner_radius=0.2
        )
        lsm_box.shift(RIGHT * 3)
        
        lsm_title = Text("LSM-Tree", font=F.CODE, color=C.LSM_MEMTABLE).scale(F.SIZE_HEADING)
        lsm_title.next_to(lsm_box, UP, buff=L.SPACING_TIGHT)
        
        lsm_desc = VGroup(
            Text("✓ Write-optimized", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
            Text("✓ Append-only", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_LABEL),
            Text("• Modern (1996+)", font=F.CODE, color=C.TEXT_TERTIARY).scale(F.SIZE_LABEL),
        )
        lsm_desc.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        lsm_desc.move_to(lsm_box.get_center())
        
        # Animate
        self.play(
            FadeIn(btree_box),
            FadeIn(btree_title),
            FadeIn(lsm_box),
            FadeIn(lsm_title)
        )
        self.wait_beat()
        
        self.play(
            FadeIn(btree_desc, shift=UP * 0.2),
            FadeIn(lsm_desc, shift=UP * 0.2)
        )
        self.wait_absorb()
        
        # VS indicator
        vs_circle = Circle(radius=0.4, color=C.TEXT_TERTIARY, fill_opacity=0.2)
        vs_text = Text("VS", font=F.CODE, color=C.TEXT_ACCENT).scale(F.SIZE_CAPTION)
        vs_text.move_to(vs_circle.get_center())
        vs_group = VGroup(vs_circle, vs_text)
        
        self.play(FadeIn(vs_group, scale=0.5))
        
        # Final question
        question = create_bilingual(
            "أيهما الأفضل؟",
            "Which one is better?",
            color_ar=C.TEXT_ACCENT,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        question.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(FadeIn(question, shift=UP * 0.2))
        self.wait_contemplate()
