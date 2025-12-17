"""
Scene 1: In-Place Update Problem
=================================

Demonstrates the danger of in-place file updates
and how crashes can lead to data loss.

Narrative Arc:
1. Introduce a file with valuable data
2. Show new data arriving
3. Demonstrate O_TRUNC truncating the file
4. Crash occurs before write completes
5. Reveal: DATA LOST!

This is the "problem" scene that sets up the need for atomic operations.
"""

import sys
sys.path.insert(0, '..')

from manim import *
from config import config, C, T, F, L, A, D
from base_scenes import DatabaseScene
from components.files import FileBox, DataBlock
from components.effects import CrashEffect, CorruptionEffect, WarningBadge
from components.code_display import CodeBlock, FunctionSignature
from utils.text_helpers import create_bilingual, format_step_label


class Scene1_InPlaceUpdate(DatabaseScene):
    """
    Chapter 1, Section 1: The Danger of In-Place Updates
    
    Visual metaphor: The file is a living organism that gets
    violently disrupted during the update process.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: INTRODUCE THE PROTAGONIST (THE FILE)
        # ══════════════════════════════════════════════════════════════════════
        
        # Title card
        title = self.create_title_card(
            "التحديث في نفس المكان",
            "In-Place File Updates"
        )
        self.wait_beat()
        
        # Create the file - our protagonist
        file = FileBox(
            filename="data.txt",
            content_text="Old Data\n1024 bytes",
            color=C.FILE_ORIGINAL
        )
        file.shift(LEFT * 3)
        
        # Dramatic introduction
        self.play(file.animate_create())
        self.wait_absorb()
        
        # Add a gentle glow to show it's valuable
        self.emphasis_pulse(file, color=C.PRIMARY_BLUE, iterations=1)
        
        # Label explaining the file's value
        value_label = create_bilingual(
            "ملفك الثمين",
            "Your precious data"
        )
        value_label.next_to(file, DOWN, buff=L.SPACING_LG)
        self.play(FadeIn(value_label, shift=UP * 0.2))
        self.wait_beat(2)
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: INTRODUCE THE CONFLICT (NEW DATA)
        # ══════════════════════════════════════════════════════════════════════
        
        # Fade out value label
        self.play(FadeOut(value_label))
        
        # New data block arrives
        new_data = DataBlock(
            label="New Data",
            size_label="2048 bytes",
            color=C.FILE_NEW
        )
        new_data.shift(RIGHT * 3 + UP * 1)
        
        self.play(FadeIn(new_data, shift=LEFT * 0.5))
        self.wait_beat()
        
        # Show the update intent
        update_label = create_bilingual(
            "تحديث البيانات...",
            "Updating data..."
        )
        update_label.to_edge(DOWN, buff=L.MARGIN_LG)
        self.play(Write(update_label))
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: THE DANGEROUS OPERATION (O_TRUNC)
        # ══════════════════════════════════════════════════════════════════════
        
        # Show the dangerous code
        code = FunctionSignature(
            "open",
            params=["data.txt", "O_WRONLY | O_TRUNC"]
        )
        code.to_edge(UP, buff=L.MARGIN_LG).shift(RIGHT * 2)
        
        self.play(
            FadeOut(update_label),
            FadeIn(code)
        )
        self.wait_beat()
        
        # Highlight O_TRUNC - THE DANGER
        trunc_warning = WarningBadge(
            text="⚠️",
            label="O_TRUNC"
        )
        trunc_warning.next_to(file, DOWN, buff=L.SPACING_MD)
        
        self.play(
            FadeIn(trunc_warning, scale=0.5),
            file.rect.animate.set_stroke(color=C.WARNING),
            run_time=T.FAST
        )
        self.wait_beat()
        
        # THE TRUNCATION - file becomes empty!
        empty_text = Text(
            "EMPTY!",
            font=F.BODY,
            color=C.ERROR,
            weight=BOLD
        ).scale(F.SIZE_BODY)
        empty_text.move_to(file.rect.get_center())
        
        # Dramatic truncation animation
        self.play(
            # File content fades
            file.content.animate.set_opacity(0),
            # Box turns red
            file.rect.animate.set_stroke(color=C.ERROR).set_fill(color=C.ERROR, opacity=0.1),
            # Empty label appears
            FadeIn(empty_text, scale=1.5),
            # Warning shakes
            Wiggle(trunc_warning, scale_value=1.2, rotation_angle=0.1),
            run_time=T.NORMAL
        )
        self.wait_beat()
        
        # Show step indicator
        step1_label = format_step_label(1, "الملف فارغ الآن!", "File is now empty!")
        step1_label.to_edge(DOWN, buff=L.MARGIN_LG)
        self.play(Write(step1_label))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: THE CATASTROPHE (CRASH!)
        # ══════════════════════════════════════════════════════════════════════
        
        # Show data trying to move in
        arrow = Arrow(
            new_data.get_center(),
            file.get_center(),
            color=C.PRIMARY_YELLOW,
            stroke_width=3
        )
        write_label = Text("write()", font=F.CODE, color=C.PRIMARY_YELLOW).scale(F.SIZE_CAPTION)
        write_label.next_to(arrow, UP, buff=L.SPACING_TIGHT)
        
        self.play(
            FadeOut(step1_label),
            Create(arrow),
            Write(write_label)
        )
        self.wait_beat()
        
        # Data starts moving
        self.play(
            new_data.animate.shift(LEFT * 1.5),
            run_time=T.FAST
        )
        
        # CRASH!!!
        crash = CrashEffect(
            text="CRASH!",
            position=ORIGIN
        )
        
        # Clear the scene partially and show crash
        self.play(
            FadeOut(arrow),
            FadeOut(write_label),
            FadeOut(code),
            FadeOut(trunc_warning),
            crash.animate_appear()
        )
        
        # Shake effect on remaining elements
        self.play(
            Wiggle(file, scale_value=1.05, rotation_angle=0.02),
            Wiggle(new_data, scale_value=1.05, rotation_angle=0.02),
            run_time=T.FAST
        )
        
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: THE TRAGIC RESULT (DATA LOST)
        # ══════════════════════════════════════════════════════════════════════
        
        # Fade out crash and new data (it never made it)
        self.play(
            FadeOut(crash),
            FadeOut(new_data, shift=UP),
            run_time=T.FAST
        )
        
        # Result text - bilingual
        result_ar = Text(
            "نتيجة: بيانات مفقودة!",
            font=F.ARABIC,
            color=C.ERROR
        ).scale(F.SIZE_HEADING)
        
        result_en = Text(
            "Result: DATA LOST!",
            font=F.BODY,
            color=C.ERROR
        ).scale(F.SIZE_BODY)
        
        result_group = VGroup(result_ar, result_en).arrange(DOWN, buff=L.SPACING_SM)
        result_group.to_edge(DOWN, buff=L.MARGIN_LG)
        
        # Dramatic reveal
        self.play(Write(result_ar, run_time=T.NORMAL))
        self.play(Write(result_en, run_time=T.FAST))
        
        # Final emphasis on the empty file
        self.highlight_box(file, color=C.ERROR)
        
        self.dramatic_pause()
        
        # ══════════════════════════════════════════════════════════════════════
        # CODA: THE LESSON
        # ══════════════════════════════════════════════════════════════════════
        
        # Clear and show lesson
        self.play(
            FadeOut(file),
            FadeOut(empty_text),
            FadeOut(result_group),
            *[FadeOut(mob) for mob in self.mobjects if mob not in [title]],
            run_time=T.FAST
        )
        
        # Lesson text
        lesson = create_bilingual(
            "التحديثات في نفس المكان خطيرة!",
            "In-place updates are dangerous!",
            color_ar=C.WARNING,
            color_en=C.TEXT_SECONDARY,
            scale_ar=F.SIZE_HEADING,
            scale_en=F.SIZE_BODY
        )
        
        self.play(FadeIn(lesson, scale=0.8))
        self.wait_absorb(1.5)
        
        # Hint at solution
        next_hint = create_bilingual(
            "الحل: العمليات الذرية",
            "Solution: Atomic Operations",
            color_ar=C.SUCCESS,
            color_en=C.TEXT_SECONDARY,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        next_hint.next_to(lesson, DOWN, buff=L.SPACING_LG)
        
        self.play(FadeIn(next_hint, shift=UP * 0.3))
        self.wait_absorb(2)
