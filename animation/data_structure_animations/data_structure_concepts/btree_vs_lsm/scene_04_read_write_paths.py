"""
Scene 04: Read/Write Paths Comparison
=====================================

Side-by-side comparison of read and write operations:
- B-Tree: In-place updates, direct reads
- LSM-Tree: Append writes, multi-level reads

Narrative Arc:
1. Split-screen setup
2. Write operation comparison
3. Read operation comparison
4. I/O cost analysis
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import C, T, F, L, DS, A
from base_scenes import ComparisonScene
from components.nodes import BTreeNode
from components.disk import SSTable
from components.effects import IOFlowDot, ReadWriteIndicator
from utils.text_helpers import create_bilingual


class Scene04_ReadWritePaths(ComparisonScene):
    """
    Side-by-side comparison of read and write operations.
    
    Visual: Split screen with synchronized animations
    showing the different approaches.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "مسارات القراءة والكتابة",
            "Read & Write Paths"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: SPLIT SCREEN SETUP
        # ══════════════════════════════════════════════════════════════════════
        
        left_title, right_title = self.create_split_screen(
            "B-Tree",
            "LSM-Tree",
            left_color=C.BTREE_NODE,
            right_color=C.LSM_MEMTABLE
        )
        
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: WRITE PATH COMPARISON
        # ══════════════════════════════════════════════════════════════════════
        
        # Section header
        write_header = Text("WRITE Operation", font=F.CODE, color=C.IO_WRITE).scale(F.SIZE_CAPTION)
        write_header.to_edge(UP, buff=L.MARGIN_SM)
        
        self.play(Write(write_header))
        
        # B-Tree side: Show tree with in-place update
        btree_node = BTreeNode(keys=[10, 20, 30], max_keys=4)
        btree_node.scale(0.8)
        btree_node.move_to(LEFT * L.COMPARE_LEFT_CENTER + UP * 0.5)
        
        btree_label = Text("Disk Page", font=F.CODE, color=C.BTREE_NODE).scale(F.SIZE_TINY)
        btree_label.next_to(btree_node, UP, buff=L.SPACING_TIGHT)
        
        # LSM side: Show MemTable + SSTables
        memtable = RoundedRectangle(
            width=2.5, height=0.8,
            color=C.LSM_MEMTABLE,
            fill_opacity=0.2,
            corner_radius=0.1
        )
        memtable.move_to(RIGHT * L.COMPARE_RIGHT_CENTER + UP * 1.5)
        
        mem_label = Text("MemTable (RAM)", font=F.CODE, color=C.LSM_MEMTABLE).scale(F.SIZE_TINY)
        mem_label.next_to(memtable, UP, buff=L.SPACING_TIGHT)
        
        sstables = VGroup()
        for i in range(3):
            sst = RoundedRectangle(
                width=2.2, height=0.4,
                color=C.LSM_SSTABLE_L0,
                fill_opacity=0.2,
                corner_radius=0.05
            )
            sst.move_to(RIGHT * L.COMPARE_RIGHT_CENTER + DOWN * (0.3 + i * 0.55))
            sstables.add(sst)
        
        disk_label = Text("SSTables (Disk)", font=F.CODE, color=C.LSM_SSTABLE_L0).scale(F.SIZE_TINY)
        disk_label.next_to(sstables, UP, buff=L.SPACING_TIGHT)
        
        # Animate setup
        self.play(
            FadeIn(btree_node),
            FadeIn(btree_label),
            FadeIn(memtable),
            FadeIn(mem_label),
            FadeIn(sstables),
            FadeIn(disk_label)
        )
        self.wait_beat()
        
        # Write operation - B-Tree
        btree_write_label = Text("Random write to page", font=F.CODE, color=C.IO_RANDOM).scale(F.SIZE_TINY)
        btree_write_label.next_to(btree_node, DOWN, buff=L.SPACING_MD)
        
        write_dot_btree = Dot(color=C.IO_WRITE, radius=0.08)
        write_dot_btree.move_to(btree_node.get_top() + UP * 0.5)
        
        # Write operation - LSM
        lsm_write_label = Text("Sequential to memory", font=F.CODE, color=C.IO_SEQUENTIAL).scale(F.SIZE_TINY)
        lsm_write_label.next_to(memtable, DOWN, buff=L.SPACING_MD)
        
        write_dot_lsm = Dot(color=C.IO_WRITE, radius=0.08)
        write_dot_lsm.move_to(memtable.get_top() + UP * 0.5)
        
        # Animate writes simultaneously
        self.play(
            FadeIn(write_dot_btree, scale=0.5),
            FadeIn(write_dot_lsm, scale=0.5)
        )
        
        self.sync_animate(
            Succession(
                write_dot_btree.animate.move_to(btree_node.get_center()),
                FadeOut(write_dot_btree),
                Write(btree_write_label)
            ),
            Succession(
                write_dot_lsm.animate.move_to(memtable.get_center()),
                FadeOut(write_dot_lsm),
                Write(lsm_write_label)
            ),
            run_time=T.NORMAL
        )
        
        # I/O counts
        btree_io = Text("Disk I/O: 1 (random)", font=F.CODE, color=C.IO_RANDOM).scale(F.SIZE_TINY)
        btree_io.next_to(btree_write_label, DOWN, buff=L.SPACING_SM)
        
        lsm_io = Text("Disk I/O: 0 (memory)", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
        lsm_io.next_to(lsm_write_label, DOWN, buff=L.SPACING_SM)
        
        self.play(Write(btree_io), Write(lsm_io))
        
        # Winner indicator
        lsm_win = Text("✓ FASTER", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
        lsm_win.next_to(lsm_io, DOWN, buff=L.SPACING_TIGHT)
        
        self.play(FadeIn(lsm_win, scale=0.8))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: READ PATH COMPARISON
        # ══════════════════════════════════════════════════════════════════════
        
        # Clear write annotations
        self.play(
            FadeOut(write_header),
            FadeOut(btree_write_label),
            FadeOut(lsm_write_label),
            FadeOut(btree_io),
            FadeOut(lsm_io),
            FadeOut(lsm_win)
        )
        
        read_header = Text("READ Operation", font=F.CODE, color=C.IO_READ).scale(F.SIZE_CAPTION)
        read_header.to_edge(UP, buff=L.MARGIN_SM)
        
        self.play(Write(read_header))
        
        # B-Tree read
        btree_read_label = Text("Direct lookup in tree", font=F.CODE, color=C.IO_READ).scale(F.SIZE_TINY)
        btree_read_label.next_to(btree_node, DOWN, buff=L.SPACING_MD)
        
        read_dot_btree = Dot(color=C.IO_READ, radius=0.08)
        read_dot_btree.move_to(btree_node.get_top() + UP * 0.5)
        
        # LSM read - must check multiple levels
        lsm_read_label = Text("Check all levels!", font=F.CODE, color=C.WARNING).scale(F.SIZE_TINY)
        lsm_read_label.next_to(memtable, LEFT, buff=L.SPACING_SM)
        
        read_dot_lsm = Dot(color=C.IO_READ, radius=0.08)
        read_dot_lsm.move_to(memtable.get_top() + UP * 0.5)
        
        # Animate reads
        self.play(
            FadeIn(read_dot_btree, scale=0.5),
            FadeIn(read_dot_lsm, scale=0.5)
        )
        
        # B-Tree: direct hit
        self.play(
            read_dot_btree.animate.move_to(btree_node.key_cells[1].get_center()),
            run_time=T.FAST
        )
        self.play(
            Flash(btree_node.key_cells[1], color=C.SUCCESS, line_length=0.15),
            FadeOut(read_dot_btree),
            Write(btree_read_label)
        )
        
        # LSM: check each level
        self.play(Write(lsm_read_label))
        
        # Check memtable
        self.play(read_dot_lsm.animate.move_to(memtable.get_center()), run_time=T.QUICK)
        miss1 = Text("miss", font=F.CODE, color=C.ERROR).scale(F.SIZE_TINY)
        miss1.next_to(memtable, RIGHT, buff=L.SPACING_TIGHT)
        self.play(FadeIn(miss1))
        
        # Check each SSTable
        for i, sst in enumerate(sstables):
            self.play(read_dot_lsm.animate.move_to(sst.get_center()), run_time=T.QUICK)
            if i < 2:
                miss = Text("miss", font=F.CODE, color=C.ERROR).scale(F.SIZE_TINY)
                miss.next_to(sst, RIGHT, buff=L.SPACING_TIGHT)
                self.play(FadeIn(miss))
            else:
                # Found in last SSTable
                self.play(
                    Flash(sst, color=C.SUCCESS, line_length=0.15),
                    FadeOut(read_dot_lsm)
                )
                found = Text("found!", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
                found.next_to(sst, RIGHT, buff=L.SPACING_TIGHT)
                self.play(FadeIn(found))
        
        # I/O counts
        btree_read_io = Text("Disk I/O: 1", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
        btree_read_io.next_to(btree_read_label, DOWN, buff=L.SPACING_SM)
        
        lsm_read_io = Text("Disk I/O: 3 (worst case)", font=F.CODE, color=C.WARNING).scale(F.SIZE_TINY)
        lsm_read_io.to_edge(DOWN, buff=L.MARGIN_MD).shift(RIGHT * L.COMPARE_RIGHT_CENTER)
        
        self.play(Write(btree_read_io), Write(lsm_read_io))
        
        # Winner indicator
        btree_win = Text("✓ FASTER", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
        btree_win.next_to(btree_read_io, DOWN, buff=L.SPACING_TIGHT)
        
        self.play(FadeIn(btree_win, scale=0.8))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: SUMMARY
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        summary_title = Text("Operation Comparison", font=F.CODE, color=C.TEXT_ACCENT).scale(F.SIZE_HEADING)
        summary_title.to_edge(UP, buff=L.MARGIN_MD)
        
        self.play(Write(summary_title))
        
        # Summary table
        table_data = [
            ("", "B-Tree", "LSM-Tree"),
            ("Write", "O(log n) random", "O(1) sequential"),
            ("Read", "O(log n)", "O(L × log n)"),
            ("Best for", "Read-heavy", "Write-heavy"),
        ]
        
        table = VGroup()
        for row_idx, row in enumerate(table_data):
            row_group = VGroup()
            for col_idx, cell in enumerate(row):
                if row_idx == 0:
                    # Header row
                    if col_idx == 1:
                        color = C.BTREE_NODE
                    elif col_idx == 2:
                        color = C.LSM_MEMTABLE
                    else:
                        color = C.TEXT_TERTIARY
                    text = Text(cell, font=F.CODE, color=color).scale(F.SIZE_CAPTION)
                else:
                    if col_idx == 0:
                        color = C.TEXT_SECONDARY
                    elif col_idx == 1:
                        color = C.BTREE_NODE
                    else:
                        color = C.LSM_MEMTABLE
                    text = Text(cell, font=F.CODE, color=color).scale(F.SIZE_LABEL)
                
                text.move_to(RIGHT * (col_idx - 1) * 3)
                row_group.add(text)
            
            row_group.move_to(DOWN * (row_idx - 1.5) * 0.8)
            table.add(row_group)
        
        self.play(
            LaggedStart(
                *[FadeIn(row, shift=LEFT * 0.2) for row in table],
                lag_ratio=0.2
            )
        )
        
        # Conclusion
        conclusion = create_bilingual(
            "لا يوجد فائز مطلق - يعتمد على حالة الاستخدام",
            "No absolute winner - depends on use case",
            color_ar=C.TEXT_ACCENT,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        conclusion.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(FadeIn(conclusion))
        self.wait_contemplate()
