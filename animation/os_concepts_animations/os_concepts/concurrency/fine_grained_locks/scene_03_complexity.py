"""
Scene 03: Complexity and Deadlock Risk
======================================

Shows the downside of fine-grained locking:
- Increased complexity
- Deadlock possibility
- Lock ordering requirements
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from config import C, T, F, L, A, OS
from base_scenes import ConcurrencyScene
from components.threads import Thread
from components.locks import Mutex
from components.effects import DeadlockCycle
from utils.text_helpers import create_bilingual


class Scene03_Complexity(ConcurrencyScene):
    """
    Demonstrates deadlock risk with fine-grained locks.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "تعقيد وخطر الجمود",
            "Complexity & Deadlock Risk"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: DEADLOCK SCENARIO SETUP
        # ══════════════════════════════════════════════════════════════════════
        
        section = self.create_section_header("The Deadlock Problem")
        self.play(Write(section))
        
        # Two locks
        lock_a = Mutex(label="Lock A")
        lock_b = Mutex(label="Lock B")
        
        lock_a.move_to(LEFT * 2 + UP * 0.5)
        lock_b.move_to(RIGHT * 2 + UP * 0.5)
        
        # Two threads
        thread1 = Thread(thread_id=1)
        thread2 = Thread(thread_id=2)
        
        thread1.move_to(LEFT * 4 + DOWN * 1)
        thread2.move_to(RIGHT * 4 + DOWN * 1)
        
        self.play(FadeIn(lock_a), FadeIn(lock_b))
        self.play(thread1.animate_spawn(), thread2.animate_spawn())
        
        # Scenario explanation
        scenario = VGroup(
            Text("T1 needs: Lock A → Lock B", font=F.CODE, color=C.THREAD_1).scale(F.SIZE_TINY),
            Text("T2 needs: Lock B → Lock A", font=F.CODE, color=C.THREAD_2).scale(F.SIZE_TINY),
        )
        scenario.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        scenario.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(Write(scenario))
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: T1 ACQUIRES A, T2 ACQUIRES B
        # ══════════════════════════════════════════════════════════════════════
        
        step1 = Text("Step 1: Each acquires first lock", font=F.CODE, color=C.INFO).scale(F.SIZE_CAPTION)
        step1.to_edge(UP, buff=L.MARGIN_SM).shift(DOWN * 0.8)
        
        self.play(Write(step1))
        
        # T1 acquires A
        self.play(thread1.animate.move_to(lock_a.get_bottom() + DOWN * 0.5))
        self.play(lock_a.animate_acquire(1))
        
        # T2 acquires B
        self.play(thread2.animate.move_to(lock_b.get_bottom() + DOWN * 0.5))
        self.play(lock_b.animate_acquire(2))
        
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: DEADLOCK - BOTH TRY SECOND LOCK
        # ══════════════════════════════════════════════════════════════════════
        
        step2 = Text("Step 2: Each tries to acquire second lock...", font=F.CODE, color=C.WARNING).scale(F.SIZE_CAPTION)
        step2.to_edge(UP, buff=L.MARGIN_SM).shift(DOWN * 0.8)
        
        self.play(Transform(step1, step2))
        
        # T1 wants B (held by T2)
        want_b = Arrow(
            thread1.get_right(),
            lock_b.get_left(),
            color=C.THREAD_1,
            stroke_width=2
        )
        want_b_label = Text("wants", font=F.CODE, color=C.THREAD_1).scale(F.SIZE_TINY)
        want_b_label.next_to(want_b, UP, buff=0.05)
        
        # T2 wants A (held by T1)
        want_a = Arrow(
            thread2.get_left(),
            lock_a.get_right(),
            color=C.THREAD_2,
            stroke_width=2
        )
        want_a_label = Text("wants", font=F.CODE, color=C.THREAD_2).scale(F.SIZE_TINY)
        want_a_label.next_to(want_a, UP, buff=0.05)
        
        self.play(
            Create(want_b), Write(want_b_label),
            Create(want_a), Write(want_a_label)
        )
        
        # Both get blocked
        thread1.set_state("blocked")
        thread2.set_state("blocked")
        
        self.play(
            thread1.body.animate.set_fill(opacity=A.BLOCKED_OPACITY),
            thread2.body.animate.set_fill(opacity=A.BLOCKED_OPACITY)
        )
        
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: DEADLOCK VISUALIZATION
        # ══════════════════════════════════════════════════════════════════════
        
        deadlock_text = Text(
            "⚠ DEADLOCK!",
            font=F.CODE,
            color=C.ERROR
        ).scale(F.SIZE_HEADING)
        deadlock_text.move_to(UP * 2.5)
        
        self.play(FadeIn(deadlock_text, scale=0.8))
        self.play(Flash(deadlock_text, color=C.ERROR, line_length=0.4))
        
        # Show cycle
        cycle_positions = [
            thread1.get_center(),
            lock_b.get_center(),
            thread2.get_center(),
            lock_a.get_center(),
        ]
        
        cycle = DeadlockCycle(cycle_positions)
        cycle.warning.set_opacity(0)  # Hide duplicate warning
        
        self.play(cycle.animate_show())
        
        explanation = create_bilingual(
            "كلاهما ينتظر الآخر للأبد!",
            "Both wait for each other forever!",
            color_ar=C.ERROR,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        explanation.next_to(scenario, UP, buff=L.SPACING_SM)
        
        self.play(FadeIn(explanation))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 6: SOLUTION - LOCK ORDERING
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        solution_title = self.create_section_header("Solution: Lock Ordering")
        self.play(Write(solution_title))
        
        rule = VGroup(
            Text("Rule: Always acquire locks in the SAME order", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
            Text("e.g., Always A before B", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_TINY),
        )
        rule.arrange(DOWN, buff=0.1)
        rule.move_to(UP * 0.5)
        
        self.play(FadeIn(rule))
        
        # Tradeoff summary
        tradeoffs = VGroup(
            Text("Fine-Grained Locking Trade-offs:", font=F.CODE, color=C.TEXT_ACCENT).scale(F.SIZE_LABEL),
            Text("✓ Better parallelism", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY),
            Text("✓ Higher throughput", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY),
            Text("✗ More complex code", font=F.CODE, color=C.ERROR).scale(F.SIZE_TINY),
            Text("✗ Deadlock risk", font=F.CODE, color=C.ERROR).scale(F.SIZE_TINY),
            Text("✗ Harder to reason about", font=F.CODE, color=C.ERROR).scale(F.SIZE_TINY),
        )
        tradeoffs.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        tradeoffs.shift(DOWN * 1.5)
        
        self.play(
            LaggedStart(*[FadeIn(t) for t in tradeoffs], lag_ratio=0.1)
        )
        
        # Tease next topic
        next_hint = create_bilingual(
            "هل يمكننا تجنب الأقفال تماماً؟",
            "Can we avoid locks entirely?",
            color_ar=C.TEXT_ACCENT,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        next_hint.to_edge(DOWN, buff=L.MARGIN_SM)
        
        self.play(FadeIn(next_hint))
        self.wait_contemplate()
