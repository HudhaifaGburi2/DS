"""
Scene 03: Mutex Costs
=====================

Shows the downsides of mutex:
- Blocking overhead
- Contention under high load
- Serialization reduces parallelism

Narrative: Mutex works, but at what cost?
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from config import C, T, F, L, A, OS
from base_scenes import ConcurrencyScene
from components.threads import Thread, ThreadGroup
from components.locks import Mutex
from components.critical_sections import CriticalSection
from components.effects import ContentionPulse
from utils.text_helpers import create_bilingual, create_metric_display


class Scene03_MutexCosts(ConcurrencyScene):
    """
    Demonstrates the costs of mutex synchronization.
    
    Visual: Multiple threads piling up, throughput metrics,
    contention visualization.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "تكلفة القفل",
            "The Cost of Locking"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: SETUP - MANY THREADS
        # ══════════════════════════════════════════════════════════════════════
        
        section = self.create_section_header("High Contention Scenario")
        self.play(Write(section))
        
        # Critical section (small)
        critical = CriticalSection(label="Critical Section", width=2.5, height=1.5)
        critical.move_to(RIGHT * 2)
        
        # Mutex
        mutex = Mutex(label="lock")
        mutex.move_to(ORIGIN)
        
        # Many threads
        threads = []
        for i in range(6):
            thread = Thread(thread_id=i + 1)
            thread.move_to(LEFT * 5 + UP * (1.5 - i * 0.6))
            threads.append(thread)
        
        self.play(FadeIn(critical), FadeIn(mutex))
        self.play(
            LaggedStart(
                *[t.animate_spawn() for t in threads],
                lag_ratio=0.1
            )
        )
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: THREADS PILE UP
        # ══════════════════════════════════════════════════════════════════════
        
        pile_label = Text("All threads want the lock...", font=F.CODE, color=C.WARNING).scale(F.SIZE_CAPTION)
        pile_label.to_edge(DOWN, buff=L.MARGIN_MD)
        
        self.play(Write(pile_label))
        
        # All threads move toward lock
        self.play(
            LaggedStart(
                *[t.animate.move_to(mutex.get_left() + LEFT * (0.5 + i * 0.4) + UP * (0.3 - i * 0.15))
                  for i, t in enumerate(threads)],
                lag_ratio=0.1
            )
        )
        
        # First thread acquires
        self.play(mutex.animate_acquire(1))
        self.play(threads[0].animate.move_to(critical.background.get_center()))
        
        # Others get blocked
        for t in threads[1:]:
            t.set_state("blocked")
        
        self.play(
            *[t.body.animate.set_fill(opacity=A.BLOCKED_OPACITY) for t in threads[1:]]
        )
        
        # Contention visualization
        contention = ContentionPulse(mutex.get_center(), color=C.CONTENTION_HIGH)
        self.play(FadeIn(contention))
        self.play(contention.animate_pulse(2))
        self.play(FadeOut(contention))
        
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: SHOW WAITING TIME
        # ══════════════════════════════════════════════════════════════════════
        
        self.play(FadeOut(pile_label))
        
        # Waiting time indicator
        wait_times = VGroup()
        for i, t in enumerate(threads[1:], 1):
            wait_text = Text(
                f"T{i+1}: waiting {i}×",
                font=F.CODE,
                color=t.color
            ).scale(F.SIZE_TINY)
            wait_text.next_to(t, RIGHT, buff=L.SPACING_TIGHT)
            wait_times.add(wait_text)
        
        self.play(
            LaggedStart(
                *[FadeIn(w) for w in wait_times],
                lag_ratio=0.1
            )
        )
        
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: THROUGHPUT IMPACT
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        throughput_title = self.create_section_header("Throughput Impact")
        self.play(Write(throughput_title))
        
        # Comparison: No lock vs With lock
        # No lock (parallel) - theoretical
        no_lock_label = Text("Without Lock (Parallel)", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL)
        no_lock_label.move_to(LEFT * 3 + UP * 1.5)
        
        no_lock_bar = Rectangle(
            width=4.5,
            height=0.5,
            fill_color=C.SUCCESS,
            fill_opacity=0.5,
            stroke_width=0
        )
        no_lock_bar.next_to(no_lock_label, DOWN, buff=L.SPACING_SM)
        
        no_lock_value = Text("6× throughput", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
        no_lock_value.next_to(no_lock_bar, RIGHT, buff=L.SPACING_TIGHT)
        
        # With lock (serial)
        with_lock_label = Text("With Mutex (Serial)", font=F.CODE, color=C.WARNING).scale(F.SIZE_LABEL)
        with_lock_label.move_to(LEFT * 3 + DOWN * 0.5)
        
        with_lock_bar = Rectangle(
            width=0.75,
            height=0.5,
            fill_color=C.WARNING,
            fill_opacity=0.5,
            stroke_width=0
        )
        with_lock_bar.next_to(with_lock_label, DOWN, buff=L.SPACING_SM)
        with_lock_bar.align_to(no_lock_bar, LEFT)
        
        with_lock_value = Text("1× throughput", font=F.CODE, color=C.WARNING).scale(F.SIZE_TINY)
        with_lock_value.next_to(with_lock_bar, RIGHT, buff=L.SPACING_TIGHT)
        
        # Animate comparison
        self.play(Write(no_lock_label))
        self.play(FadeIn(no_lock_bar), Write(no_lock_value))
        self.wait_beat()
        
        self.play(Write(with_lock_label))
        self.play(FadeIn(with_lock_bar), Write(with_lock_value))
        
        # Loss indicator
        loss = Text(
            "5× throughput LOST!",
            font=F.CODE,
            color=C.ERROR
        ).scale(F.SIZE_CAPTION)
        loss.move_to(DOWN * 2)
        
        self.play(FadeIn(loss, scale=0.8))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 6: MUTEX COSTS SUMMARY
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        costs_title = self.create_section_header("Mutex Trade-offs")
        self.play(Write(costs_title))
        
        pros = VGroup(
            Text("✓ Guarantees correctness", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
            Text("✓ Simple to understand", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
            Text("✓ No race conditions", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
        )
        pros.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        pros.move_to(LEFT * 3 + UP * 0.5)
        
        cons = VGroup(
            Text("✗ Threads block (waste CPU)", font=F.CODE, color=C.ERROR).scale(F.SIZE_LABEL),
            Text("✗ Serializes execution", font=F.CODE, color=C.ERROR).scale(F.SIZE_LABEL),
            Text("✗ Contention limits scaling", font=F.CODE, color=C.ERROR).scale(F.SIZE_LABEL),
        )
        cons.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        cons.move_to(RIGHT * 3 + UP * 0.5)
        
        self.play(
            LaggedStart(*[FadeIn(p) for p in pros], lag_ratio=0.15)
        )
        self.play(
            LaggedStart(*[FadeIn(c) for c in cons], lag_ratio=0.15)
        )
        
        # Tease solutions
        solutions = create_bilingual(
            "حلول محتملة",
            "Possible Solutions",
            color_ar=C.TEXT_ACCENT,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        solutions.to_edge(DOWN, buff=L.MARGIN_LG)
        
        solution_list = VGroup(
            Text("1. Fine-Grained Locks", font=F.CODE, color=C.INFO).scale(F.SIZE_TINY),
            Text("2. Optimistic Concurrency", font=F.CODE, color=C.INFO).scale(F.SIZE_TINY),
            Text("3. MVCC", font=F.CODE, color=C.INFO).scale(F.SIZE_TINY),
        )
        solution_list.arrange(RIGHT, buff=L.SPACING_LG)
        solution_list.next_to(solutions, DOWN, buff=L.SPACING_SM)
        
        self.play(FadeIn(solutions))
        self.play(FadeIn(solution_list))
        self.wait_contemplate()
