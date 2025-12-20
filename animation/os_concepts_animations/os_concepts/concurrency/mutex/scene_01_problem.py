"""
Scene 01: The Race Condition Problem
====================================

Shows why synchronization is needed:
- Multiple threads accessing shared data
- Interleaved execution causing corruption
- Lost updates and inconsistent state

Narrative: Start with innocent-looking code, reveal the danger.
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from config import C, T, F, L, A, OS
from base_scenes import ConcurrencyScene
from components.threads import Thread, ThreadGroup
from components.critical_sections import SharedResource, CriticalSection
from components.effects import ConflictFlash
from utils.text_helpers import create_bilingual, create_code_snippet


class Scene01_RaceCondition(ConcurrencyScene):
    """
    Demonstrates the race condition problem.
    
    Visual: Two threads incrementing a counter simultaneously,
    resulting in lost updates.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "مشكلة التنافس",
            "The Race Condition Problem"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: SETUP - INNOCENT CODE
        # ══════════════════════════════════════════════════════════════════════
        
        section = self.create_section_header("Innocent-Looking Code")
        self.play(Write(section))
        
        # Show the code
        code = """counter = 0

def increment():
    temp = counter
    temp = temp + 1
    counter = temp"""
        
        code_block = create_code_snippet(code, highlight_lines=[4, 5, 6])
        code_block.scale(0.9)
        code_block.shift(LEFT * 3.5)
        
        self.play(FadeIn(code_block))
        self.wait_absorb()
        
        # Explanation
        explanation = create_bilingual(
            "ماذا لو شغلنا هذا من خيطين؟",
            "What if we run this from 2 threads?",
            color_ar=C.WARNING,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        explanation.shift(RIGHT * 3)
        
        self.play(FadeIn(explanation))
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: SETUP CONCURRENT EXECUTION
        # ══════════════════════════════════════════════════════════════════════
        
        self.play(FadeOut(section), FadeOut(code_block), FadeOut(explanation))
        
        # Create shared counter
        counter = SharedResource(name="counter", initial_value="0")
        counter.move_to(ORIGIN)
        
        self.play(FadeIn(counter))
        self.wait_beat()
        
        # Create two threads
        thread1 = Thread(thread_id=1)
        thread2 = Thread(thread_id=2)
        
        thread1.move_to(LEFT * 4 + UP * 1.5)
        thread2.move_to(LEFT * 4 + DOWN * 1.5)
        
        # Thread labels
        t1_label = Text("Thread 1", font=F.CODE, color=C.THREAD_1).scale(F.SIZE_LABEL)
        t1_label.next_to(thread1, UP, buff=L.SPACING_TIGHT)
        
        t2_label = Text("Thread 2", font=F.CODE, color=C.THREAD_2).scale(F.SIZE_LABEL)
        t2_label.next_to(thread2, UP, buff=L.SPACING_TIGHT)
        
        self.play(
            thread1.animate_spawn(),
            thread2.animate_spawn(),
            FadeIn(t1_label),
            FadeIn(t2_label)
        )
        self.wait_beat()
        
        # Expected result
        expected = Text(
            "Expected: counter = 2",
            font=F.CODE,
            color=C.SUCCESS
        ).scale(F.SIZE_CAPTION)
        expected.to_edge(DOWN, buff=L.MARGIN_MD)
        
        self.play(Write(expected))
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: THE RACE - INTERLEAVED EXECUTION
        # ══════════════════════════════════════════════════════════════════════
        
        timeline_title = Text("Interleaved Execution", font=F.CODE, color=C.WARNING).scale(F.SIZE_CAPTION)
        timeline_title.to_edge(UP, buff=L.MARGIN_SM)
        
        self.play(Write(timeline_title))
        
        # Execution steps visualization
        steps_t1 = VGroup()
        steps_t2 = VGroup()
        
        # T1: temp = counter (reads 0)
        step1_t1 = Text("temp₁ = 0", font=F.CODE, color=C.THREAD_1).scale(F.SIZE_TINY)
        step1_t1.move_to(LEFT * 1.5 + UP * 1.5)
        
        self.play(
            thread1.animate.move_to(counter.get_left() + LEFT * 0.8),
            run_time=T.FAST
        )
        self.play(counter.animate_read(C.THREAD_1))
        self.play(Write(step1_t1))
        self.wait_beat(0.5)
        
        # T2: temp = counter (also reads 0!)
        step1_t2 = Text("temp₂ = 0", font=F.CODE, color=C.THREAD_2).scale(F.SIZE_TINY)
        step1_t2.move_to(LEFT * 1.5 + DOWN * 1.5)
        
        self.play(
            thread2.animate.move_to(counter.get_left() + LEFT * 0.8 + DOWN * 0.5),
            run_time=T.FAST
        )
        self.play(counter.animate_read(C.THREAD_2))
        self.play(Write(step1_t2))
        
        # Warning!
        warning = Text("⚠ Both read 0!", font=F.CODE, color=C.WARNING).scale(F.SIZE_TINY)
        warning.next_to(counter, RIGHT, buff=L.SPACING_MD)
        self.play(FadeIn(warning, scale=0.8))
        self.wait_beat()
        
        # T1: temp = temp + 1
        step2_t1 = Text("temp₁ = 1", font=F.CODE, color=C.THREAD_1).scale(F.SIZE_TINY)
        step2_t1.next_to(step1_t1, RIGHT, buff=L.SPACING_MD)
        self.play(Write(step2_t1))
        
        # T2: temp = temp + 1
        step2_t2 = Text("temp₂ = 1", font=F.CODE, color=C.THREAD_2).scale(F.SIZE_TINY)
        step2_t2.next_to(step1_t2, RIGHT, buff=L.SPACING_MD)
        self.play(Write(step2_t2))
        
        self.wait_beat()
        
        # T1: counter = temp (writes 1)
        step3_t1 = Text("counter = 1", font=F.CODE, color=C.THREAD_1).scale(F.SIZE_TINY)
        step3_t1.next_to(step2_t1, RIGHT, buff=L.SPACING_MD)
        
        self.play(counter.animate_write("1", C.THREAD_1))
        self.play(Write(step3_t1))
        
        # T2: counter = temp (also writes 1!)
        step3_t2 = Text("counter = 1", font=F.CODE, color=C.THREAD_2).scale(F.SIZE_TINY)
        step3_t2.next_to(step2_t2, RIGHT, buff=L.SPACING_MD)
        
        self.play(counter.animate_write("1", C.THREAD_2))
        self.play(Write(step3_t2))
        
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: THE PROBLEM - LOST UPDATE
        # ══════════════════════════════════════════════════════════════════════
        
        self.play(FadeOut(warning))
        
        # Show the problem
        actual = Text(
            "Actual: counter = 1  ✗",
            font=F.CODE,
            color=C.ERROR
        ).scale(F.SIZE_CAPTION)
        actual.next_to(expected, UP, buff=L.SPACING_SM)
        
        # Flash conflict
        self.play(
            FadeIn(actual),
            Flash(counter.container, color=C.ERROR, line_length=0.3)
        )
        
        # Lost update explanation
        lost = create_bilingual(
            "تحديث مفقود!",
            "Lost Update!",
            color_ar=C.ERROR,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        lost.next_to(counter, UP, buff=L.SPACING_LG)
        
        self.play(FadeIn(lost, scale=0.8))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 6: SUMMARY
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        summary_title = self.create_section_header("Race Condition")
        self.play(Write(summary_title))
        
        summary_points = VGroup(
            Text("• Multiple threads access shared data", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_LABEL),
            Text("• Execution order is non-deterministic", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_LABEL),
            Text("• Results depend on timing (race)", font=F.CODE, color=C.WARNING).scale(F.SIZE_LABEL),
            Text("• Solution: Synchronization needed!", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
        )
        summary_points.arrange(DOWN, buff=L.SPACING_SM, aligned_edge=LEFT)
        
        self.play(
            LaggedStart(
                *[FadeIn(p, shift=LEFT * 0.2) for p in summary_points],
                lag_ratio=0.2
            )
        )
        
        # Tease next scene
        next_hint = create_bilingual(
            "الحل: القفل المتبادل (Mutex)",
            "Solution: Mutual Exclusion Lock",
            color_ar=C.TEXT_ACCENT,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        next_hint.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(FadeIn(next_hint))
        self.wait_contemplate()
