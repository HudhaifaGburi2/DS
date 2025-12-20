"""
Scene 03: LSM-Tree Structure
============================

Deep dive into LSM-Tree architecture:
- MemTable (in-memory sorted buffer)
- SSTables (immutable sorted files)
- Levels and size ratios
- Write path: buffer → flush → compact

Narrative Arc:
1. Show memory vs disk separation
2. Write path demonstration
3. Compaction explanation
4. Level structure
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import C, T, F, L, DS, A
from base_scenes import DataStructureScene
from components.memory import MemTable
from components.disk import SSTable, StorageLevel, DiskRegion
from components.effects import WriteAmplification, CompactionWave
from utils.text_helpers import create_bilingual, create_step_label


class Scene03_LSMStructure(DataStructureScene):
    """
    LSM-Tree architecture and write path.
    
    Visual focus: Memory buffer flowing to disk levels,
    compaction merging data downward.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "بنية LSM-Tree",
            "LSM-Tree Structure"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: THE KEY INSIGHT
        # ══════════════════════════════════════════════════════════════════════
        
        insight_title = self.create_section_header("The Key Insight")
        self.play(Write(insight_title))
        
        # Key insight
        insight = create_bilingual(
            "الكتابة العشوائية على القرص بطيئة",
            "Random writes to disk are slow",
            color_ar=C.ERROR,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        insight.shift(UP * 0.5)
        
        self.play(FadeIn(insight))
        self.wait_absorb()
        
        solution = create_bilingual(
            "الحل: تحويل الكتابات العشوائية إلى تسلسلية",
            "Solution: Convert random writes to sequential",
            color_ar=C.SUCCESS,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        solution.next_to(insight, DOWN, buff=L.SPACING_LG)
        
        self.play(FadeIn(solution, shift=UP * 0.2))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: ARCHITECTURE OVERVIEW
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        arch_title = self.create_section_header("LSM Architecture")
        self.play(Write(arch_title))
        
        # Memory section
        mem_label = Text("Memory (RAM)", font=F.CODE, color=C.MEMORY_RAM).scale(F.SIZE_LABEL)
        mem_label.move_to(UP * 3 + LEFT * 5)
        
        mem_region = RoundedRectangle(
            width=10, height=1.8,
            color=C.MEMORY_RAM,
            fill_opacity=0.05,
            stroke_width=1,
            corner_radius=0.15
        )
        mem_region.move_to(UP * 2)
        
        # MemTable
        memtable = MemTable(width=3.5, height=1.2)
        memtable.move_to(UP * 2)
        
        self.play(
            Write(mem_label),
            FadeIn(mem_region),
            FadeIn(memtable)
        )
        self.wait_beat()
        
        # Disk section
        disk_label = Text("Disk (SSD)", font=F.CODE, color=C.DISK_SSD).scale(F.SIZE_LABEL)
        disk_label.move_to(DOWN * 0.3 + LEFT * 5)
        
        disk_region = RoundedRectangle(
            width=10, height=3.5,
            color=C.DISK_SSD,
            fill_opacity=0.03,
            stroke_width=1,
            corner_radius=0.15
        )
        disk_region.move_to(DOWN * 2)
        
        self.play(
            Write(disk_label),
            FadeIn(disk_region)
        )
        
        # Levels
        levels = []
        level_labels = ["L0 (Hot)", "L1", "L2", "L3 (Cold)"]
        level_colors = [C.LSM_SSTABLE_L0, C.LSM_SSTABLE_L1, C.LSM_SSTABLE_L2, C.LSM_SSTABLE_L3]
        
        for i, (label, color) in enumerate(zip(level_labels, level_colors)):
            level_container = RoundedRectangle(
                width=9,
                height=0.7,
                color=color,
                fill_opacity=0.1,
                corner_radius=0.1
            )
            level_container.move_to(DOWN * (0.7 + i * 0.85))
            
            level_text = Text(label, font=F.CODE, color=color).scale(F.SIZE_TINY)
            level_text.move_to(level_container.get_left() + RIGHT * 0.6)
            
            levels.append(VGroup(level_container, level_text))
        
        self.play(
            LaggedStart(
                *[FadeIn(level, shift=DOWN * 0.2) for level in levels],
                lag_ratio=0.15
            )
        )
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: WRITE PATH DEMONSTRATION
        # ══════════════════════════════════════════════════════════════════════
        
        write_title = Text("Write Path", font=F.CODE, color=C.IO_WRITE).scale(F.SIZE_CAPTION)
        write_title.to_edge(RIGHT, buff=L.MARGIN_MD).shift(UP * 2.5)
        
        self.play(Write(write_title))
        
        # Step 1: Write to MemTable
        step1_label = Text("1. Write to MemTable", font=F.CODE, color=C.TEXT_ACCENT).scale(F.SIZE_TINY)
        step1_label.next_to(memtable, RIGHT, buff=L.SPACING_MD)
        
        self.play(Write(step1_label))
        
        # Simulate writes
        write_dot = Dot(color=C.IO_WRITE, radius=0.1)
        write_dot.move_to(memtable.get_top() + UP * 0.5)
        
        for i in range(3):
            self.play(
                FadeIn(write_dot, scale=0.5),
                run_time=T.QUICK
            )
            self.play(
                write_dot.animate.move_to(memtable.get_center()),
                run_time=T.FAST
            )
            self.play(
                Flash(memtable.container, color=C.LSM_MEMTABLE_HOT, line_length=0.2),
                FadeOut(write_dot),
                run_time=T.QUICK
            )
        
        self.wait_beat()
        
        # Step 2: Flush to L0
        step2_label = Text("2. Flush to L0 (when full)", font=F.CODE, color=C.TEXT_ACCENT).scale(F.SIZE_TINY)
        step2_label.next_to(step1_label, DOWN, buff=L.SPACING_SM)
        
        self.play(Write(step2_label))
        
        # Create flush arrow
        flush_arrow = Arrow(
            memtable.get_bottom() + DOWN * 0.1,
            levels[0][0].get_top() + UP * 0.1,
            color=C.IO_WRITE,
            stroke_width=3
        )
        
        self.play(Create(flush_arrow))
        
        # Create SSTable in L0
        sstable_l0 = RoundedRectangle(
            width=1.5, height=0.4,
            color=C.LSM_SSTABLE_L0,
            fill_opacity=0.4,
            corner_radius=0.05
        )
        sstable_l0.move_to(levels[0][0].get_center() + LEFT * 2)
        
        sstable_label = Text("SST", font=F.CODE, color=C.LSM_SSTABLE_L0).scale(F.SIZE_TINY)
        sstable_label.move_to(sstable_l0.get_center())
        
        self.play(
            FadeIn(sstable_l0, shift=DOWN * 0.3),
            FadeIn(sstable_label)
        )
        
        self.play(
            FadeOut(flush_arrow),
            memtable.container.animate.set_fill(opacity=0.1)
        )
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: COMPACTION
        # ══════════════════════════════════════════════════════════════════════
        
        # Add more SSTables to L0
        more_sstables = VGroup()
        for i in range(3):
            sst = RoundedRectangle(
                width=1.5, height=0.4,
                color=C.LSM_SSTABLE_L0,
                fill_opacity=0.4,
                corner_radius=0.05
            )
            sst.move_to(levels[0][0].get_center() + LEFT * (0.5 - i * 1.7))
            more_sstables.add(sst)
        
        self.play(
            LaggedStart(
                *[FadeIn(sst, scale=0.8) for sst in more_sstables],
                lag_ratio=0.2
            )
        )
        
        # Compaction trigger
        compact_label = Text("3. Compaction (merge & sort)", font=F.CODE, color=C.LSM_COMPACTION).scale(F.SIZE_TINY)
        compact_label.next_to(step2_label, DOWN, buff=L.SPACING_SM)
        
        self.play(Write(compact_label))
        
        # Highlight compaction source
        self.play(
            sstable_l0.animate.set_stroke(color=C.LSM_COMPACTION, width=3),
            *[sst.animate.set_stroke(color=C.LSM_COMPACTION, width=3) for sst in more_sstables]
        )
        
        # Compaction arrow
        compact_arrow = Arrow(
            levels[0][0].get_bottom() + DOWN * 0.05,
            levels[1][0].get_top() + UP * 0.05,
            color=C.LSM_COMPACTION,
            stroke_width=3
        )
        
        self.play(Create(compact_arrow))
        
        # Create merged SSTable in L1
        merged_sst = RoundedRectangle(
            width=3, height=0.45,
            color=C.LSM_SSTABLE_L1,
            fill_opacity=0.4,
            corner_radius=0.05
        )
        merged_sst.move_to(levels[1][0].get_center())
        
        merged_label = Text("Merged SST", font=F.CODE, color=C.LSM_SSTABLE_L1).scale(F.SIZE_TINY)
        merged_label.move_to(merged_sst.get_center())
        
        # Animate merge
        self.play(
            FadeOut(sstable_l0),
            FadeOut(sstable_label),
            FadeOut(more_sstables),
            FadeIn(merged_sst, shift=DOWN * 0.2),
            FadeIn(merged_label)
        )
        
        self.play(FadeOut(compact_arrow))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 6: KEY PROPERTIES
        # ══════════════════════════════════════════════════════════════════════
        
        # Clear annotations
        self.play(
            FadeOut(step1_label),
            FadeOut(step2_label),
            FadeOut(compact_label),
            FadeOut(write_title)
        )
        
        # Properties
        props_title = Text("LSM-Tree Properties", font=F.CODE, color=C.TEXT_ACCENT).scale(F.SIZE_CAPTION)
        props_title.to_edge(RIGHT, buff=L.MARGIN_MD).shift(UP * 2)
        
        props = VGroup(
            Text("✓ Sequential writes only", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY),
            Text("✓ Immutable SSTables", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY),
            Text("✓ High write throughput", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY),
            Text("⚠ Read amplification", font=F.CODE, color=C.WARNING).scale(F.SIZE_TINY),
            Text("⚠ Write amplification", font=F.CODE, color=C.WARNING).scale(F.SIZE_TINY),
        )
        props.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        props.next_to(props_title, DOWN, buff=L.SPACING_SM)
        
        self.play(Write(props_title))
        self.play(
            LaggedStart(
                *[FadeIn(p, shift=LEFT * 0.1) for p in props],
                lag_ratio=0.15
            )
        )
        
        # Summary
        summary = create_bilingual(
            "تحسين الكتابة على حساب القراءة",
            "Optimized for writes at cost of reads",
            color_ar=C.LSM_MEMTABLE,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        summary.to_edge(DOWN, buff=L.MARGIN_MD)
        
        self.play(FadeIn(summary))
        self.wait_contemplate()
