"""
Scene 02: Validation Phase
==========================

Shows conflict detection at commit time:
- Read set / Write set tracking
- Validation rules
- Conflict detection

Narrative: How do we know if there was a conflict?
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from config import C, T, F, L, A, OS
from base_scenes import TimelineScene
from components.threads import Thread
from components.timelines import TransactionSpan, TimeAxis
from components.effects import ValidationCheckmark, ConflictFlash
from utils.text_helpers import create_bilingual


class Scene02_Validation(TimelineScene):
    """
    Demonstrates conflict detection at validation time.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "مرحلة التحقق",
            "The Validation Phase"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: TRANSACTION TIMELINE
        # ══════════════════════════════════════════════════════════════════════
        
        section = self.create_section_header("Tracking Read & Write Sets")
        self.play(Write(section))
        
        # Time axis
        time_axis = self.create_time_axis(y_pos=-2)
        self.play(time_axis.animate_create())
        
        # Transaction T1
        t1_span = TransactionSpan("T1", start_x=-4, end_x=1, y_pos=1, color=C.THREAD_1)
        
        # T1's read set
        t1_reads = Text("Reads: {X, Y}", font=F.CODE, color=C.INFO).scale(F.SIZE_TINY)
        t1_reads.next_to(t1_span.bar, UP, buff=0.3)
        
        # T1's write set
        t1_writes = Text("Writes: {X}", font=F.CODE, color=C.WARNING).scale(F.SIZE_TINY)
        t1_writes.next_to(t1_reads, UP, buff=0.1)
        
        self.play(t1_span.animate_create())
        self.play(Write(t1_reads), Write(t1_writes))
        self.wait_beat()
        
        # Transaction T2 (overlapping)
        t2_span = TransactionSpan("T2", start_x=-2, end_x=3, y_pos=-0.5, color=C.THREAD_2)
        
        t2_reads = Text("Reads: {Y, Z}", font=F.CODE, color=C.INFO).scale(F.SIZE_TINY)
        t2_reads.next_to(t2_span.bar, DOWN, buff=0.3)
        
        t2_writes = Text("Writes: {Y}", font=F.CODE, color=C.WARNING).scale(F.SIZE_TINY)
        t2_writes.next_to(t2_reads, DOWN, buff=0.1)
        
        self.play(t2_span.animate_create())
        self.play(Write(t2_reads), Write(t2_writes))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: VALIDATION RULE
        # ══════════════════════════════════════════════════════════════════════
        
        self.play(FadeOut(section))
        
        rule_title = self.create_section_header("Validation Rule")
        self.play(Write(rule_title))
        
        rule = VGroup(
            Text("For each concurrent transaction T:", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_LABEL),
            Text("T's write set ∩ my read set = ∅", font=F.CODE, color=C.TEXT_ACCENT).scale(F.SIZE_LABEL),
        )
        rule.arrange(DOWN, buff=L.SPACING_SM)
        rule.to_edge(UP, buff=L.MARGIN_LG * 2)
        
        self.play(FadeIn(rule))
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: T1 VALIDATES - SUCCESS
        # ══════════════════════════════════════════════════════════════════════
        
        validate_t1 = Text("T1 validates...", font=F.CODE, color=C.THREAD_1).scale(F.SIZE_CAPTION)
        validate_t1.move_to(RIGHT * 3.5 + UP * 1)
        
        self.play(Write(validate_t1))
        
        # T1 commits before T2 writes, so no conflict
        check1 = Text("T2.writes ∩ T1.reads = {Y} ∩ {X,Y}", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_TINY)
        check1.next_to(validate_t1, DOWN, buff=L.SPACING_SM)
        
        self.play(Write(check1))
        
        # T2 hasn't committed yet when T1 validates
        result1 = Text("= {} (T2 not committed yet) ✓", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
        result1.next_to(check1, DOWN, buff=0.1)
        
        self.play(Write(result1))
        
        # Commit T1
        self.play(t1_span.animate_commit())
        
        success1 = ValidationCheckmark(t1_span.end_marker.get_center() + UP * 0.5, success=True)
        self.play(success1.animate_appear())
        
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: T2 VALIDATES - CONFLICT!
        # ══════════════════════════════════════════════════════════════════════
        
        validate_t2 = Text("T2 validates...", font=F.CODE, color=C.THREAD_2).scale(F.SIZE_CAPTION)
        validate_t2.move_to(RIGHT * 3.5 + DOWN * 0.5)
        
        self.play(Write(validate_t2))
        
        # T2 reads Y, but T1 wrote X (and committed)
        # Let's say T1 also wrote Y for conflict
        check2 = Text("T1.writes ∩ T2.reads = {X} ∩ {Y,Z}", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_TINY)
        check2.next_to(validate_t2, DOWN, buff=L.SPACING_SM)
        
        self.play(Write(check2))
        
        result2 = Text("= {} → No conflict ✓", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
        result2.next_to(check2, DOWN, buff=0.1)
        
        self.play(Write(result2))
        
        # T2 also commits successfully
        self.play(t2_span.animate_commit())
        
        success2 = ValidationCheckmark(t2_span.end_marker.get_center() + DOWN * 0.5, success=True)
        self.play(success2.animate_appear())
        
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 6: CONFLICT EXAMPLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        conflict_title = self.create_section_header("When Validation Fails")
        self.play(Write(conflict_title))
        
        # New time axis
        time_axis2 = self.create_time_axis(y_pos=-2)
        self.play(time_axis2.animate_create())
        
        # T3 reads X
        t3_span = TransactionSpan("T3", start_x=-4, end_x=2, y_pos=0.5, color=C.THREAD_3)
        t3_info = Text("T3 reads X", font=F.CODE, color=C.THREAD_3).scale(F.SIZE_TINY)
        t3_info.next_to(t3_span.bar, UP, buff=0.2)
        
        # T4 writes X and commits first
        t4_span = TransactionSpan("T4", start_x=-2, end_x=0, y_pos=-0.8, color=C.THREAD_4)
        t4_info = Text("T4 writes X (commits!)", font=F.CODE, color=C.THREAD_4).scale(F.SIZE_TINY)
        t4_info.next_to(t4_span.bar, DOWN, buff=0.2)
        
        self.play(t3_span.animate_create(), Write(t3_info))
        self.play(t4_span.animate_create(), Write(t4_info))
        
        # T4 commits first
        self.play(t4_span.animate_commit())
        self.wait_beat()
        
        # T3 tries to validate
        conflict_check = Text(
            "T4.writes ∩ T3.reads = {X} ∩ {X} = {X} ≠ ∅",
            font=F.CODE,
            color=C.ERROR
        ).scale(F.SIZE_LABEL)
        conflict_check.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(Write(conflict_check))
        
        # CONFLICT!
        conflict_flash = ConflictFlash(t3_span.bar)
        self.play(conflict_flash.animate_flash())
        
        self.play(t3_span.animate_abort())
        
        fail = ValidationCheckmark(t3_span.end_marker.get_center() + UP * 0.5, success=False)
        self.play(fail.animate_appear())
        
        explanation = create_bilingual(
            "T3 قرأ بيانات قديمة - يجب إعادة المحاولة",
            "T3 read stale data - must retry",
            color_ar=C.ERROR,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        explanation.next_to(conflict_check, UP, buff=L.SPACING_SM)
        
        self.play(FadeIn(explanation))
        self.wait_contemplate()
