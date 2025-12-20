"""
Scene 02: Increased Parallelism
===============================

Shows throughput benefits of fine-grained locking:
- More locks = less contention
- Better CPU utilization
- Scalability with thread count
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from config import C, T, F, L, A, OS
from base_scenes import ConcurrencyScene
from components.threads import Thread
from components.locks import FineGrainedLock
from components.critical_sections import DataCell
from utils.text_helpers import create_bilingual, create_metric_display


class Scene02_Parallelism(ConcurrencyScene):
    """
    Demonstrates parallelism benefits of fine-grained locks.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "زيادة التوازي",
            "Increased Parallelism"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: SETUP 4 PARTITIONS
        # ══════════════════════════════════════════════════════════════════════
        
        section = self.create_section_header("4 Partitions, 4 Threads")
        self.play(Write(section))
        
        # Fine-grained locks
        locks = FineGrainedLock(num_locks=4, labels=["P0", "P1", "P2", "P3"])
        locks.move_to(UP * 1)
        
        # Data cells
        data_cells = VGroup()
        for i in range(4):
            cell = DataCell(f"Data{i}", "")
            data_cells.add(cell)
        data_cells.arrange(RIGHT, buff=L.LOCK_SPACING)
        data_cells.move_to(DOWN * 0.5)
        
        # Align cells under locks
        for lock, cell in zip(locks.locks, data_cells):
            cell.move_to(lock.get_center() + DOWN * 1.5)
        
        # Four threads
        threads = []
        start_positions = [
            LEFT * 5 + UP * 2,
            LEFT * 5 + UP * 0.7,
            LEFT * 5 + DOWN * 0.6,
            LEFT * 5 + DOWN * 1.9
        ]
        
        for i in range(4):
            thread = Thread(thread_id=i + 1)
            thread.move_to(start_positions[i])
            threads.append(thread)
        
        self.play(FadeIn(locks), FadeIn(data_cells))
        self.play(
            LaggedStart(
                *[t.animate_spawn() for t in threads],
                lag_ratio=0.1
            )
        )
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: ALL THREADS ACQUIRE DIFFERENT LOCKS
        # ══════════════════════════════════════════════════════════════════════
        
        parallel_label = Text(
            "All threads run in PARALLEL!",
            font=F.CODE,
            color=C.SUCCESS
        ).scale(F.SIZE_CAPTION)
        parallel_label.to_edge(DOWN, buff=L.MARGIN_MD)
        
        # Each thread moves to its partition
        move_anims = []
        for i, (thread, lock) in enumerate(zip(threads, locks.locks)):
            move_anims.append(thread.animate.move_to(lock.get_top() + UP * 0.4))
        
        self.play(AnimationGroup(*move_anims, lag_ratio=0.1))
        
        # All acquire simultaneously
        self.play(
            AnimationGroup(
                *[lock.animate_acquire(i + 1) for i, lock in enumerate(locks.locks)],
                lag_ratio=0.05
            )
        )
        
        # All work simultaneously
        work_anims = []
        for thread, cell in zip(threads, data_cells):
            work_anims.append(thread.animate.move_to(cell.get_center() + UP * 0.4))
        
        self.play(AnimationGroup(*work_anims, lag_ratio=0))
        self.play(Write(parallel_label))
        
        # Flash all data cells simultaneously
        self.play(
            AnimationGroup(
                *[Flash(cell.body, color=threads[i].color, line_length=0.15) 
                  for i, cell in enumerate(data_cells)]
            )
        )
        
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: THROUGHPUT COMPARISON
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        throughput_title = self.create_section_header("Throughput Scaling")
        self.play(Write(throughput_title))
        
        # Bar chart: Threads vs Throughput
        # Coarse (1 lock)
        coarse_bar = Rectangle(width=1, height=0.8, fill_color=C.WARNING, fill_opacity=0.6, stroke_width=0)
        coarse_bar.move_to(LEFT * 3 + DOWN * 0.6)
        coarse_label = Text("1 Lock", font=F.CODE, color=C.WARNING).scale(F.SIZE_TINY)
        coarse_label.next_to(coarse_bar, DOWN, buff=0.1)
        coarse_value = Text("1×", font=F.CODE, color=C.WARNING).scale(F.SIZE_LABEL)
        coarse_value.next_to(coarse_bar, UP, buff=0.1)
        
        # 2 locks
        two_bar = Rectangle(width=1, height=1.6, fill_color=C.INFO, fill_opacity=0.6, stroke_width=0)
        two_bar.move_to(LEFT * 1 + DOWN * 0.2)
        two_label = Text("2 Locks", font=F.CODE, color=C.INFO).scale(F.SIZE_TINY)
        two_label.next_to(two_bar, DOWN, buff=0.1)
        two_value = Text("~2×", font=F.CODE, color=C.INFO).scale(F.SIZE_LABEL)
        two_value.next_to(two_bar, UP, buff=0.1)
        
        # 4 locks
        four_bar = Rectangle(width=1, height=3.2, fill_color=C.SUCCESS, fill_opacity=0.6, stroke_width=0)
        four_bar.move_to(RIGHT * 1 + UP * 0.6)
        four_label = Text("4 Locks", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
        four_label.next_to(four_bar, DOWN, buff=0.1)
        four_value = Text("~4×", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL)
        four_value.next_to(four_bar, UP, buff=0.1)
        
        # Align bottoms
        coarse_bar.align_to(DOWN * 1, DOWN)
        two_bar.align_to(DOWN * 1, DOWN)
        four_bar.align_to(DOWN * 1, DOWN)
        
        # Reposition labels
        coarse_label.next_to(coarse_bar, DOWN, buff=0.1)
        two_label.next_to(two_bar, DOWN, buff=0.1)
        four_label.next_to(four_bar, DOWN, buff=0.1)
        coarse_value.next_to(coarse_bar, UP, buff=0.1)
        two_value.next_to(two_bar, UP, buff=0.1)
        four_value.next_to(four_bar, UP, buff=0.1)
        
        self.play(
            FadeIn(coarse_bar), Write(coarse_label), Write(coarse_value)
        )
        self.play(
            FadeIn(two_bar), Write(two_label), Write(two_value)
        )
        self.play(
            FadeIn(four_bar), Write(four_label), Write(four_value)
        )
        
        # Key insight
        insight = create_bilingual(
            "التوازي يتناسب مع عدد الأقفال",
            "Parallelism scales with number of locks",
            color_ar=C.SUCCESS,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        insight.to_edge(DOWN, buff=L.MARGIN_MD)
        
        self.play(FadeIn(insight))
        self.wait_contemplate()
