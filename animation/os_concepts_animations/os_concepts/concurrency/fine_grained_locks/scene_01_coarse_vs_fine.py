"""
Scene 01: Coarse vs Fine-Grained Locking
========================================

Compares single lock vs multiple locks:
- Coarse: One lock for everything
- Fine: Lock per resource/partition

Narrative: Why one big lock isn't always best.
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from config import C, T, F, L, A, OS
from base_scenes import ComparisonScene
from components.threads import Thread
from components.locks import Mutex, FineGrainedLock
from components.critical_sections import DataCell
from utils.text_helpers import create_bilingual


class Scene01_CoarseVsFine(ComparisonScene):
    """
    Side-by-side comparison of coarse vs fine-grained locking.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "القفل الخشن مقابل الدقيق",
            "Coarse vs Fine-Grained Locking"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: SETUP COMPARISON
        # ══════════════════════════════════════════════════════════════════════
        
        left_title, right_title = self.create_split_screen(
            "Coarse-Grained",
            "Fine-Grained",
            left_color=C.WARNING,
            right_color=C.SUCCESS
        )
        
        # LEFT: Coarse - one lock for all data
        coarse_lock = Mutex(label="global_lock")
        coarse_lock.move_to(LEFT * L.COMPARE_LEFT_CENTER + UP * 1)
        
        coarse_data = VGroup()
        for i in range(4):
            cell = DataCell(f"D{i}", str(i * 10))
            cell.scale(0.8)
            coarse_data.add(cell)
        coarse_data.arrange(RIGHT, buff=0.2)
        coarse_data.move_to(LEFT * L.COMPARE_LEFT_CENTER + DOWN * 0.5)
        
        # Protection boundary around all data
        coarse_boundary = RoundedRectangle(
            width=coarse_data.width + 0.5,
            height=coarse_data.height + 0.5,
            color=C.WARNING,
            fill_opacity=0.1,
            stroke_width=2,
            corner_radius=0.1
        )
        coarse_boundary.move_to(coarse_data.get_center())
        
        # RIGHT: Fine - lock per partition
        fine_locks = FineGrainedLock(num_locks=4, labels=["L0", "L1", "L2", "L3"])
        fine_locks.scale(0.7)
        fine_locks.move_to(RIGHT * L.COMPARE_RIGHT_CENTER + UP * 1)
        
        fine_data = VGroup()
        for i in range(4):
            cell = DataCell(f"D{i}", str(i * 10))
            cell.scale(0.8)
            fine_data.add(cell)
        fine_data.arrange(RIGHT, buff=0.4)
        fine_data.move_to(RIGHT * L.COMPARE_RIGHT_CENTER + DOWN * 0.5)
        
        # Individual boundaries
        fine_boundaries = VGroup()
        for i, (lock, cell) in enumerate(zip(fine_locks.locks, fine_data)):
            boundary = RoundedRectangle(
                width=cell.width + 0.2,
                height=cell.height + 0.2,
                color=C.SUCCESS,
                fill_opacity=0.1,
                stroke_width=1,
                corner_radius=0.05
            )
            boundary.move_to(cell.get_center())
            fine_boundaries.add(boundary)
        
        # Animate setup
        self.play(
            FadeIn(coarse_lock),
            FadeIn(coarse_data),
            FadeIn(coarse_boundary)
        )
        self.play(
            FadeIn(fine_locks),
            FadeIn(fine_data),
            FadeIn(fine_boundaries)
        )
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: TWO THREADS ACCESS DIFFERENT DATA
        # ══════════════════════════════════════════════════════════════════════
        
        scenario = Text(
            "Scenario: T1 accesses D0, T2 accesses D3",
            font=F.CODE,
            color=C.TEXT_ACCENT
        ).scale(F.SIZE_CAPTION)
        scenario.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(Write(scenario))
        
        # Coarse side threads
        t1_coarse = Thread(thread_id=1)
        t2_coarse = Thread(thread_id=2)
        t1_coarse.scale(0.7)
        t2_coarse.scale(0.7)
        t1_coarse.move_to(LEFT * 5.5 + UP * 1.5)
        t2_coarse.move_to(LEFT * 5.5 + DOWN * 1.5)
        
        # Fine side threads
        t1_fine = Thread(thread_id=1)
        t2_fine = Thread(thread_id=2)
        t1_fine.scale(0.7)
        t2_fine.scale(0.7)
        t1_fine.move_to(RIGHT * 1 + UP * 1.5)
        t2_fine.move_to(RIGHT * 1 + DOWN * 1.5)
        
        self.play(
            t1_coarse.animate_spawn(),
            t2_coarse.animate_spawn(),
            t1_fine.animate_spawn(),
            t2_fine.animate_spawn()
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: COARSE - T1 BLOCKS T2
        # ══════════════════════════════════════════════════════════════════════
        
        coarse_label = Text("T1 locks ALL data", font=F.CODE, color=C.WARNING).scale(F.SIZE_TINY)
        coarse_label.next_to(coarse_lock, UP, buff=L.SPACING_SM)
        
        # T1 acquires global lock
        self.play(
            t1_coarse.animate.move_to(coarse_lock.get_left() + LEFT * 0.3),
            Write(coarse_label)
        )
        self.play(coarse_lock.animate_acquire(1))
        self.play(t1_coarse.animate.move_to(coarse_data[0].get_center() + UP * 0.4))
        
        # T2 tries - blocked!
        self.play(t2_coarse.animate.move_to(coarse_lock.get_left() + LEFT * 0.3 + DOWN * 0.3))
        t2_coarse.set_state("blocked")
        self.play(t2_coarse.body.animate.set_fill(opacity=A.BLOCKED_OPACITY))
        
        blocked_text = Text("BLOCKED!", font=F.CODE, color=C.ERROR).scale(F.SIZE_TINY)
        blocked_text.next_to(t2_coarse, DOWN, buff=0.1)
        self.play(FadeIn(blocked_text))
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: FINE - BOTH PROCEED
        # ══════════════════════════════════════════════════════════════════════
        
        fine_label = Text("Each locks only its data", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
        fine_label.next_to(fine_locks, UP, buff=L.SPACING_SM)
        
        # T1 acquires L0
        self.play(
            t1_fine.animate.move_to(fine_locks.locks[0].get_top() + UP * 0.3),
            Write(fine_label)
        )
        self.play(fine_locks.locks[0].animate_acquire(1))
        self.play(t1_fine.animate.move_to(fine_data[0].get_center() + UP * 0.4))
        
        # T2 acquires L3 - no conflict!
        self.play(t2_fine.animate.move_to(fine_locks.locks[3].get_top() + UP * 0.3))
        self.play(fine_locks.locks[3].animate_acquire(2))
        self.play(t2_fine.animate.move_to(fine_data[3].get_center() + UP * 0.4))
        
        parallel_text = Text("PARALLEL!", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
        parallel_text.next_to(fine_data, DOWN, buff=L.SPACING_SM)
        self.play(FadeIn(parallel_text))
        
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 6: SUMMARY
        # ══════════════════════════════════════════════════════════════════════
        
        summary = create_bilingual(
            "الأقفال الدقيقة تسمح بتوازي أكثر",
            "Fine-grained locks allow more parallelism",
            color_ar=C.SUCCESS,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        summary.to_edge(DOWN, buff=L.MARGIN_SM)
        
        self.play(
            FadeOut(scenario),
            FadeOut(blocked_text),
            FadeOut(parallel_text),
            FadeIn(summary)
        )
        self.wait_contemplate()
