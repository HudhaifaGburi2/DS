"""
Scene 03: Rollback and Retry
============================

Shows what happens on conflict:
- Abort transaction
- Discard local changes
- Retry from beginning

Narrative: The cost of optimism when conflicts happen.
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from config import C, T, F, L, A, OS
from base_scenes import ConcurrencyScene
from components.threads import Thread
from components.critical_sections import SharedResource
from components.effects import RollbackWave, RetryArrow, ValidationCheckmark
from utils.text_helpers import create_bilingual


class Scene03_Retry(ConcurrencyScene):
    """
    Demonstrates rollback and retry on conflict.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "التراجع وإعادة المحاولة",
            "Rollback & Retry"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: SETUP CONFLICT SCENARIO
        # ══════════════════════════════════════════════════════════════════════
        
        section = self.create_section_header("Conflict Resolution")
        self.play(Write(section))
        
        # Shared data
        data = SharedResource(name="balance", initial_value="100")
        data.move_to(UP * 0.5)
        
        # Thread
        thread = Thread(thread_id=1)
        thread.move_to(LEFT * 4)
        
        # Phases indicator
        phases = VGroup(
            Text("READ", font=F.CODE, color=C.INFO).scale(F.SIZE_TINY),
            Text("→", font=F.CODE, color=C.TEXT_TERTIARY).scale(F.SIZE_TINY),
            Text("WORK", font=F.CODE, color=C.WARNING).scale(F.SIZE_TINY),
            Text("→", font=F.CODE, color=C.TEXT_TERTIARY).scale(F.SIZE_TINY),
            Text("VALIDATE", font=F.CODE, color=C.ERROR).scale(F.SIZE_TINY),
        )
        phases.arrange(RIGHT, buff=0.15)
        phases.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(FadeIn(data), thread.animate_spawn(), FadeIn(phases))
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: FIRST ATTEMPT - READ PHASE
        # ══════════════════════════════════════════════════════════════════════
        
        attempt_label = Text("Attempt #1", font=F.CODE, color=C.TEXT_ACCENT).scale(F.SIZE_CAPTION)
        attempt_label.to_edge(UP, buff=L.MARGIN_SM).shift(DOWN * 0.5)
        
        self.play(Write(attempt_label))
        
        # Highlight READ phase
        self.play(phases[0].animate.set_color(C.INFO).scale(1.2))
        
        # Thread reads
        self.play(thread.animate.move_to(data.get_left() + LEFT * 0.8))
        self.play(data.animate_read(C.THREAD_1))
        
        local_copy = Text("local = 100", font=F.CODE, color=C.THREAD_1).scale(F.SIZE_TINY)
        local_copy.next_to(thread, DOWN, buff=L.SPACING_SM)
        self.play(FadeIn(local_copy))
        
        self.play(phases[0].animate.set_color(C.INFO).scale(1/1.2))
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: WORK PHASE (LOCAL MODIFICATIONS)
        # ══════════════════════════════════════════════════════════════════════
        
        self.play(phases[2].animate.set_color(C.WARNING).scale(1.2))
        
        work_label = Text("local = 100 + 50 = 150", font=F.CODE, color=C.THREAD_1).scale(F.SIZE_TINY)
        work_label.next_to(local_copy, DOWN, buff=0.1)
        
        self.play(Write(work_label))
        self.wait_beat()
        
        # Meanwhile, another transaction commits!
        meanwhile = Text("⚡ Meanwhile: Another txn commits!", font=F.CODE, color=C.ERROR).scale(F.SIZE_TINY)
        meanwhile.next_to(data, UP, buff=L.SPACING_MD)
        
        self.play(FadeIn(meanwhile))
        self.play(data.animate_write("120", C.ERROR))
        
        self.play(phases[2].animate.set_color(C.WARNING).scale(1/1.2))
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: VALIDATE PHASE - CONFLICT!
        # ══════════════════════════════════════════════════════════════════════
        
        self.play(phases[4].animate.set_color(C.ERROR).scale(1.2))
        
        validate_msg = Text("Validating...", font=F.CODE, color=C.WARNING).scale(F.SIZE_TINY)
        validate_msg.next_to(thread, UP, buff=L.SPACING_SM)
        
        self.play(Write(validate_msg))
        self.wait_beat()
        
        # Conflict detected
        conflict_msg = Text("CONFLICT DETECTED!", font=F.CODE, color=C.ERROR).scale(F.SIZE_LABEL)
        conflict_msg.move_to(ORIGIN + DOWN * 2)
        
        self.play(
            FadeIn(conflict_msg, scale=0.8),
            Flash(data.container, color=C.ERROR, line_length=0.3)
        )
        
        fail = ValidationCheckmark(thread.get_center() + UP * 0.8, success=False)
        self.play(fail.animate_appear())
        
        self.play(phases[4].animate.set_color(C.ERROR).scale(1/1.2))
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 6: ROLLBACK
        # ══════════════════════════════════════════════════════════════════════
        
        rollback_label = Text("ROLLBACK", font=F.CODE, color=C.ROLLBACK).scale(F.SIZE_CAPTION)
        rollback_label.next_to(conflict_msg, DOWN, buff=L.SPACING_SM)
        
        self.play(Write(rollback_label))
        
        # Discard local work
        self.play(
            FadeOut(local_copy, shift=LEFT * 0.3),
            FadeOut(work_label, shift=LEFT * 0.3),
            FadeOut(validate_msg),
            FadeOut(fail),
            FadeOut(meanwhile)
        )
        
        # Move thread back
        self.play(thread.animate.move_to(LEFT * 4))
        
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 7: RETRY
        # ══════════════════════════════════════════════════════════════════════
        
        retry_arrow = RetryArrow(
            thread.get_center() + RIGHT * 0.5,
            thread.get_center() + UP * 0.5,
            attempt=2
        )
        
        self.play(retry_arrow.animate_retry())
        
        attempt2 = Text("Attempt #2", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_CAPTION)
        attempt2.to_edge(UP, buff=L.MARGIN_SM).shift(DOWN * 0.5)
        
        self.play(
            Transform(attempt_label, attempt2),
            FadeOut(conflict_msg),
            FadeOut(rollback_label)
        )
        
        # Second attempt - read new value
        self.play(phases[0].animate.set_color(C.INFO).scale(1.2))
        self.play(thread.animate.move_to(data.get_left() + LEFT * 0.8))
        self.play(data.animate_read(C.THREAD_1))
        
        local_copy2 = Text("local = 120 (new!)", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
        local_copy2.next_to(thread, DOWN, buff=L.SPACING_SM)
        self.play(FadeIn(local_copy2))
        
        self.play(phases[0].animate.set_color(C.INFO).scale(1/1.2))
        
        # Work with new value
        self.play(phases[2].animate.set_color(C.WARNING).scale(1.2))
        work_label2 = Text("local = 120 + 50 = 170", font=F.CODE, color=C.THREAD_1).scale(F.SIZE_TINY)
        work_label2.next_to(local_copy2, DOWN, buff=0.1)
        self.play(Write(work_label2))
        self.play(phases[2].animate.set_color(C.WARNING).scale(1/1.2))
        
        # Validate - success!
        self.play(phases[4].animate.set_color(C.SUCCESS).scale(1.2))
        success = ValidationCheckmark(thread.get_center() + UP * 0.8, success=True)
        self.play(success.animate_appear())
        
        # Commit
        self.play(data.animate_write("170", C.SUCCESS))
        self.play(phases[4].animate.set_color(C.SUCCESS).scale(1/1.2))
        
        # Success message
        success_msg = create_bilingual(
            "نجحت في المحاولة الثانية!",
            "Succeeded on second attempt!",
            color_ar=C.SUCCESS,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        success_msg.to_edge(DOWN, buff=L.MARGIN_SM)
        
        self.play(FadeOut(phases), FadeIn(success_msg))
        self.wait_contemplate()
