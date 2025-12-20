"""
Combined B-Tree vs LSM-Tree: All Scenes in One Video
====================================================

Renders all comparison scenes sequentially.
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import C, T, F, L


class BTreeVsLSM_AllScenes(Scene):
    """
    Complete B-Tree vs LSM-Tree comparison in one video.
    """
    
    def setup(self):
        self.camera.background_color = C.BACKGROUND
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # INTRO
        # ══════════════════════════════════════════════════════════════════════
        self.play_intro()
        
        # ══════════════════════════════════════════════════════════════════════
        # SCENE 1: WHY DISK INDEXING
        # ══════════════════════════════════════════════════════════════════════
        self.play_scene_1()
        self.scene_transition()
        
        # ══════════════════════════════════════════════════════════════════════
        # SCENE 2: B-TREE STRUCTURE
        # ══════════════════════════════════════════════════════════════════════
        self.play_scene_2()
        self.scene_transition()
        
        # ══════════════════════════════════════════════════════════════════════
        # SCENE 3: LSM-TREE STRUCTURE
        # ══════════════════════════════════════════════════════════════════════
        self.play_scene_3()
        self.scene_transition()
        
        # ══════════════════════════════════════════════════════════════════════
        # SCENE 4: READ/WRITE COMPARISON
        # ══════════════════════════════════════════════════════════════════════
        self.play_scene_4()
        self.scene_transition()
        
        # ══════════════════════════════════════════════════════════════════════
        # SCENE 5: TRADEOFFS
        # ══════════════════════════════════════════════════════════════════════
        self.play_scene_5()
        
        # ══════════════════════════════════════════════════════════════════════
        # OUTRO
        # ══════════════════════════════════════════════════════════════════════
        self.play_outro()
    
    def scene_transition(self):
        """Standard transition"""
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.5)
        self.wait(0.3)
    
    # ══════════════════════════════════════════════════════════════════════════
    # INTRO
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_intro(self):
        """Opening title"""
        title_ar = Text("B-Tree مقابل LSM-Tree", font="Arial", color=C.TEXT_PRIMARY).scale(0.9)
        title_en = Text("B-Tree vs LSM-Tree", font="Arial", color=C.TEXT_SECONDARY).scale(0.5)
        subtitle = Text("Data Structure Comparison", font="Arial", color=C.TEXT_TERTIARY).scale(0.4)
        
        titles = VGroup(title_ar, title_en, subtitle).arrange(DOWN, buff=0.3)
        
        self.play(FadeIn(titles, scale=0.8), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(titles), run_time=0.8)
    
    # ══════════════════════════════════════════════════════════════════════════
    # SCENE 1: WHY DISK INDEXING
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_scene_1(self):
        """Why disk-based indexing matters"""
        # Title
        title = Text("1. Why Disk-Based Indexing?", font="Arial", color=C.TEXT_ACCENT).scale(0.6)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # RAM vs Disk
        ram = RoundedRectangle(width=2.5, height=1.2, color=C.MEMORY_RAM, fill_opacity=0.2)
        ram.shift(LEFT * 3 + UP * 0.5)
        ram_label = Text("RAM\n~100ns", font="Arial", color=C.MEMORY_RAM).scale(0.35)
        ram_label.move_to(ram)
        
        disk = RoundedRectangle(width=2.5, height=1.2, color=C.DISK_SSD, fill_opacity=0.2)
        disk.shift(RIGHT * 3 + UP * 0.5)
        disk_label = Text("SSD\n~100μs", font="Arial", color=C.DISK_SSD).scale(0.35)
        disk_label.move_to(disk)
        
        self.play(FadeIn(ram), FadeIn(ram_label), FadeIn(disk), FadeIn(disk_label))
        
        # 1000x gap
        gap = Text("1000× slower!", font="Arial", color=C.ERROR).scale(0.5)
        gap.move_to(ORIGIN + UP * 0.5)
        self.play(FadeIn(gap, scale=0.8))
        self.wait(1)
        
        # Problem
        problem = Text("Need smart data structures for disk!", font="Arial", color=C.WARNING).scale(0.4)
        problem.shift(DOWN * 1)
        self.play(Write(problem))
        
        # Two solutions preview
        btree_box = RoundedRectangle(width=2.5, height=1, color=C.BTREE_NODE, fill_opacity=0.1)
        btree_box.shift(LEFT * 2.5 + DOWN * 2.5)
        btree_text = Text("B-Tree\nRead-optimized", font="Arial", color=C.BTREE_NODE).scale(0.3)
        btree_text.move_to(btree_box)
        
        lsm_box = RoundedRectangle(width=2.5, height=1, color=C.LSM_MEMTABLE, fill_opacity=0.1)
        lsm_box.shift(RIGHT * 2.5 + DOWN * 2.5)
        lsm_text = Text("LSM-Tree\nWrite-optimized", font="Arial", color=C.LSM_MEMTABLE).scale(0.3)
        lsm_text.move_to(lsm_box)
        
        self.play(FadeIn(btree_box), FadeIn(btree_text), FadeIn(lsm_box), FadeIn(lsm_text))
        self.wait(2)
    
    # ══════════════════════════════════════════════════════════════════════════
    # SCENE 2: B-TREE STRUCTURE
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_scene_2(self):
        """B-Tree structure"""
        title = Text("2. B-Tree Structure", font="Arial", color=C.BTREE_NODE).scale(0.6)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Simple B-Tree
        root = RoundedRectangle(width=2, height=0.6, color=C.BTREE_NODE, fill_opacity=0.3)
        root.shift(UP * 1.5)
        root_keys = Text("[17|35]", font="Arial", color=WHITE).scale(0.35)
        root_keys.move_to(root)
        
        child1 = RoundedRectangle(width=1.8, height=0.5, color=C.BTREE_NODE, fill_opacity=0.2)
        child1.shift(LEFT * 3 + DOWN * 0.5)
        c1_keys = Text("[5|10]", font="Arial", color=WHITE).scale(0.3)
        c1_keys.move_to(child1)
        
        child2 = RoundedRectangle(width=1.8, height=0.5, color=C.BTREE_NODE, fill_opacity=0.2)
        child2.shift(DOWN * 0.5)
        c2_keys = Text("[20|25|30]", font="Arial", color=WHITE).scale(0.3)
        c2_keys.move_to(child2)
        
        child3 = RoundedRectangle(width=1.8, height=0.5, color=C.BTREE_NODE, fill_opacity=0.2)
        child3.shift(RIGHT * 3 + DOWN * 0.5)
        c3_keys = Text("[40|45]", font="Arial", color=WHITE).scale(0.3)
        c3_keys.move_to(child3)
        
        # Edges
        edge1 = Line(root.get_bottom() + LEFT * 0.4, child1.get_top(), color=C.BTREE_POINTER)
        edge2 = Line(root.get_bottom(), child2.get_top(), color=C.BTREE_POINTER)
        edge3 = Line(root.get_bottom() + RIGHT * 0.4, child3.get_top(), color=C.BTREE_POINTER)
        
        self.play(FadeIn(root), FadeIn(root_keys))
        self.play(Create(edge1), Create(edge2), Create(edge3))
        self.play(
            FadeIn(child1), FadeIn(c1_keys),
            FadeIn(child2), FadeIn(c2_keys),
            FadeIn(child3), FadeIn(c3_keys)
        )
        
        # Properties
        props = VGroup(
            Text("✓ Balanced tree", font="Arial", color=C.SUCCESS).scale(0.35),
            Text("✓ Sorted keys", font="Arial", color=C.SUCCESS).scale(0.35),
            Text("✓ O(log n) search", font="Arial", color=C.SUCCESS).scale(0.35),
        )
        props.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        props.to_edge(DOWN, buff=0.8)
        
        self.play(FadeIn(props))
        self.wait(2)
    
    # ══════════════════════════════════════════════════════════════════════════
    # SCENE 3: LSM-TREE STRUCTURE
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_scene_3(self):
        """LSM-Tree structure"""
        title = Text("3. LSM-Tree Structure", font="Arial", color=C.LSM_MEMTABLE).scale(0.6)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # MemTable
        memtable = RoundedRectangle(width=3, height=1, color=C.LSM_MEMTABLE, fill_opacity=0.3)
        memtable.shift(UP * 2)
        mem_label = Text("MemTable (RAM)", font="Arial", color=C.LSM_MEMTABLE).scale(0.35)
        mem_label.next_to(memtable, UP, buff=0.1)
        
        self.play(FadeIn(memtable), Write(mem_label))
        
        # Flush arrow
        flush_arrow = Arrow(memtable.get_bottom(), UP * 0.5, color=C.IO_WRITE)
        flush_label = Text("flush", font="Arial", color=C.IO_WRITE).scale(0.25)
        flush_label.next_to(flush_arrow, RIGHT, buff=0.1)
        
        self.play(Create(flush_arrow), Write(flush_label))
        
        # Levels
        levels = []
        level_names = ["L0", "L1", "L2"]
        level_colors = [C.LSM_SSTABLE_L0, C.LSM_SSTABLE_L1, C.LSM_SSTABLE_L2]
        
        for i, (name, color) in enumerate(zip(level_names, level_colors)):
            level = RoundedRectangle(width=5, height=0.6, color=color, fill_opacity=0.15)
            level.shift(DOWN * (0.3 + i * 0.8))
            label = Text(name, font="Arial", color=color).scale(0.3)
            label.move_to(level.get_left() + RIGHT * 0.4)
            levels.append((level, label))
        
        for level, label in levels:
            self.play(FadeIn(level), Write(label), run_time=0.4)
        
        # Properties
        props = VGroup(
            Text("✓ Sequential writes", font="Arial", color=C.SUCCESS).scale(0.35),
            Text("✓ High write throughput", font="Arial", color=C.SUCCESS).scale(0.35),
            Text("⚠ Read amplification", font="Arial", color=C.WARNING).scale(0.35),
        )
        props.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        props.to_edge(DOWN, buff=0.5)
        
        self.play(FadeIn(props))
        self.wait(2)
    
    # ══════════════════════════════════════════════════════════════════════════
    # SCENE 4: READ/WRITE COMPARISON
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_scene_4(self):
        """Read/Write comparison"""
        title = Text("4. Read vs Write Performance", font="Arial", color=C.TEXT_ACCENT).scale(0.6)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Divider
        divider = Line(UP * 2.5, DOWN * 2.5, color=C.TEXT_TERTIARY, stroke_width=1)
        self.play(Create(divider))
        
        # Headers
        btree_h = Text("B-Tree", font="Arial", color=C.BTREE_NODE).scale(0.5)
        btree_h.shift(LEFT * 3 + UP * 2)
        lsm_h = Text("LSM-Tree", font="Arial", color=C.LSM_MEMTABLE).scale(0.5)
        lsm_h.shift(RIGHT * 3 + UP * 2)
        
        self.play(Write(btree_h), Write(lsm_h))
        
        # Write comparison
        write_label = Text("WRITE:", font="Arial", color=C.IO_WRITE).scale(0.4)
        write_label.shift(LEFT * 5.5 + UP * 0.8)
        self.play(Write(write_label))
        
        btree_write = Text("Random I/O\n(slower)", font="Arial", color=C.ERROR).scale(0.3)
        btree_write.shift(LEFT * 3 + UP * 0.5)
        
        lsm_write = Text("Sequential I/O\n(faster)", font="Arial", color=C.SUCCESS).scale(0.3)
        lsm_write.shift(RIGHT * 3 + UP * 0.5)
        
        self.play(FadeIn(btree_write), FadeIn(lsm_write))
        
        # Read comparison
        read_label = Text("READ:", font="Arial", color=C.IO_READ).scale(0.4)
        read_label.shift(LEFT * 5.5 + DOWN * 0.8)
        self.play(Write(read_label))
        
        btree_read = Text("Direct lookup\n(faster)", font="Arial", color=C.SUCCESS).scale(0.3)
        btree_read.shift(LEFT * 3 + DOWN * 1.1)
        
        lsm_read = Text("Check all levels\n(slower)", font="Arial", color=C.WARNING).scale(0.3)
        lsm_read.shift(RIGHT * 3 + DOWN * 1.1)
        
        self.play(FadeIn(btree_read), FadeIn(lsm_read))
        
        # Summary
        summary = Text("No absolute winner - depends on workload!", font="Arial", color=C.TEXT_ACCENT).scale(0.4)
        summary.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(summary))
        self.wait(2)
    
    # ══════════════════════════════════════════════════════════════════════════
    # SCENE 5: TRADEOFFS
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_scene_5(self):
        """Trade-offs and conclusion"""
        title = Text("5. Trade-offs & When to Use", font="Arial", color=C.TEXT_ACCENT).scale(0.6)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Use cases
        btree_use = VGroup(
            Text("Use B-Tree for:", font="Arial", color=C.BTREE_NODE).scale(0.4),
            Text("• Read-heavy workloads", font="Arial", color=C.TEXT_SECONDARY).scale(0.3),
            Text("• OLTP databases", font="Arial", color=C.TEXT_SECONDARY).scale(0.3),
            Text("• PostgreSQL, MySQL", font="Arial", color=C.TEXT_TERTIARY).scale(0.25),
        )
        btree_use.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        btree_use.shift(LEFT * 3 + UP * 0.3)
        
        lsm_use = VGroup(
            Text("Use LSM-Tree for:", font="Arial", color=C.LSM_MEMTABLE).scale(0.4),
            Text("• Write-heavy workloads", font="Arial", color=C.TEXT_SECONDARY).scale(0.3),
            Text("• Time-series data", font="Arial", color=C.TEXT_SECONDARY).scale(0.3),
            Text("• RocksDB, Cassandra", font="Arial", color=C.TEXT_TERTIARY).scale(0.25),
        )
        lsm_use.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        lsm_use.shift(RIGHT * 3 + UP * 0.3)
        
        self.play(FadeIn(btree_use), FadeIn(lsm_use))
        self.wait(1)
        
        # Final verdict
        verdict = Text("Choose based on YOUR workload pattern!", font="Arial", color=C.SUCCESS).scale(0.5)
        verdict.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(verdict, scale=0.8))
        self.wait(2)
    
    # ══════════════════════════════════════════════════════════════════════════
    # OUTRO
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_outro(self):
        """Closing"""
        self.scene_transition()
        
        thanks = Text("B-Tree vs LSM-Tree", font="Arial", color=C.TEXT_PRIMARY).scale(0.7)
        subtitle = Text("Understanding the Trade-offs", font="Arial", color=C.TEXT_SECONDARY).scale(0.4)
        
        outro = VGroup(thanks, subtitle).arrange(DOWN, buff=0.3)
        
        self.play(FadeIn(outro, scale=0.8))
        self.wait(2)
        self.play(FadeOut(outro))
