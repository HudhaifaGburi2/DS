"""
Scene 2: Atomic Rename Operation
=================================

Demonstrates the safe atomic rename pattern:
1. Create temp file with new data
2. fsync the temp file
3. Atomic rename to replace original

Narrative Arc:
- Show the problem recap (brief)
- Introduce the solution pattern
- Step through the safe process
- Show crash resilience
- Celebrate success!
"""

import sys
sys.path.insert(0, '..')

from manim import *
from config import config, C, T, F, L, A, D
from base_scenes import FlowScene
from components.files import FileBox, TempFile
from components.effects import FsyncEffect, AtomicEffect, SuccessCheckmark, CrashEffect
from components.diagrams import Arrow
from utils.text_helpers import create_bilingual, format_step_label


class Scene2_AtomicRename(FlowScene):
    """
    Chapter 1, Section 2: The Atomic Rename Solution
    
    Visual metaphor: A careful, methodical process where
    each step is verified before proceeding.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: SET THE STAGE
        # ══════════════════════════════════════════════════════════════════════
        
        # Title card
        title = self.create_title_card(
            "إعادة التسمية الذرية",
            "Atomic Rename"
        )
        self.wait_beat()
        
        # Show original file
        original_file = FileBox(
            filename="data.txt",
            content_text="Old\nData",
            color=C.FILE_ORIGINAL
        )
        original_file.shift(LEFT * 4)
        
        self.play(original_file.animate_create())
        self.wait_beat()
        
        # Label it
        original_label = Text(
            "الملف الأصلي",
            font=F.ARABIC,
            color=C.TEXT_SECONDARY
        ).scale(F.SIZE_CAPTION)
        original_label.next_to(original_file, DOWN, buff=L.SPACING_SM)
        self.play(FadeIn(original_label))
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: STEP 1 - CREATE TEMP FILE
        # ══════════════════════════════════════════════════════════════════════
        
        # Step label
        step1 = self.advance_step("إنشاء ملف مؤقت", "Create temporary file")
        
        # Create temp file (appears with different styling)
        temp_file = TempFile(
            filename="data.tmp",
            content_text="New\nData"
        )
        temp_file.shift(RIGHT * 1)
        
        self.play(temp_file.animate_create())
        self.wait_beat()
        
        # Show the new data being written
        write_progress = self.create_write_indicator(temp_file)
        self.play(Create(write_progress))
        self.play(
            write_progress.animate.set_fill(opacity=1),
            run_time=T.SLOW
        )
        self.wait_beat()
        self.play(FadeOut(write_progress))
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: STEP 2 - FSYNC FOR DURABILITY
        # ══════════════════════════════════════════════════════════════════════
        
        step2 = self.advance_step("fsync للديمومة", "fsync for durability")
        
        # Create fsync effect
        fsync = FsyncEffect(
            position=temp_file.get_center(),
            label="fsync()"
        )
        
        self.play(FadeIn(fsync))
        self.play(fsync.animate_sync())
        
        # Show success
        fsync_check = SuccessCheckmark(scale_factor=0.5)
        fsync_check.next_to(temp_file, RIGHT, buff=L.SPACING_SM)
        
        self.play(
            FadeOut(fsync),
            fsync_check.animate_appear()
        )
        self.wait_beat()
        
        # Explain why this matters
        durability_note = create_bilingual(
            "البيانات آمنة على القرص",
            "Data safely on disk",
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        durability_note.next_to(fsync_check, RIGHT, buff=L.SPACING_SM)
        self.play(FadeIn(durability_note, shift=LEFT * 0.2))
        self.wait_absorb()
        
        # Clean up notes
        self.play(FadeOut(durability_note), FadeOut(fsync_check))
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: STEP 3 - THE ATOMIC RENAME
        # ══════════════════════════════════════════════════════════════════════
        
        step3 = self.advance_step("إعادة تسمية ذرية", "Atomic rename")
        
        # Show rename arrow
        rename_arrow = Arrow(
            start=temp_file.get_left() + LEFT * 0.3,
            end=original_file.get_right() + RIGHT * 0.3,
            color=C.PRIMARY_YELLOW,
            stroke_width=D.ARROW_STROKE_WIDTH
        )
        
        rename_label = Text(
            "rename()",
            font=F.CODE,
            color=C.PRIMARY_YELLOW
        ).scale(F.SIZE_CAPTION)
        rename_label.next_to(rename_arrow, UP, buff=L.SPACING_SM)
        
        self.play(
            Create(rename_arrow),
            Write(rename_label)
        )
        self.wait_beat()
        
        # Show atomic indicator
        atomic = AtomicEffect(position=ORIGIN + DOWN * 0.5)
        self.play(atomic.animate_lock())
        self.wait_beat()
        
        # THE RENAME HAPPENS
        # - Original file fades
        # - Temp file moves to original position
        # - Temp file changes name
        
        new_file = FileBox(
            filename="data.txt",
            content_text="New\nData",
            color=C.SUCCESS
        )
        new_file.move_to(original_file)
        
        # Dramatic transformation
        self.play(
            FadeOut(original_file),
            FadeOut(original_label),
            FadeOut(rename_arrow),
            FadeOut(rename_label),
            temp_file.animate.move_to(original_file.get_center()),
            run_time=T.NORMAL
        )
        
        # Update the label
        self.play(
            Transform(temp_file.label, new_file.label),
            temp_file.rect.animate.set_stroke(color=C.SUCCESS),
            temp_file.rect.animate.set_fill(color=C.SUCCESS, opacity=D.FILE_FILL_OPACITY),
            run_time=T.FAST
        )
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: DEMONSTRATE CRASH SAFETY
        # ══════════════════════════════════════════════════════════════════════
        
        # Clean up step labels
        self.play(FadeOut(self.step_labels[-1]), FadeOut(atomic))
        
        # Show crash scenarios
        crash_title = create_bilingual(
            "ماذا لو حدث انهيار؟",
            "What if crash happens?",
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        crash_title.to_edge(DOWN, buff=L.MARGIN_XL)
        
        self.play(Write(crash_title))
        self.wait_beat()
        
        # Scenario 1: Crash during temp file write
        scenario1 = create_bilingual(
            "قبل rename: الملف الأصلي سليم ✓",
            "Before rename: Original file intact",
            color_ar=C.SUCCESS,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        scenario1.next_to(crash_title, UP, buff=L.SPACING_LG)
        
        self.play(FadeIn(scenario1, shift=UP * 0.2))
        self.wait_beat()
        
        # Scenario 2: Crash after rename
        scenario2 = create_bilingual(
            "بعد rename: البيانات الجديدة آمنة ✓",
            "After rename: New data is safe",
            color_ar=C.SUCCESS,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        scenario2.next_to(scenario1, UP, buff=L.SPACING_MD)
        
        self.play(FadeIn(scenario2, shift=UP * 0.2))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 6: VICTORY!
        # ══════════════════════════════════════════════════════════════════════
        
        # Clear explanations
        self.play(
            FadeOut(crash_title),
            FadeOut(scenario1),
            FadeOut(scenario2)
        )
        
        # Final success message
        success = SuccessCheckmark(
            text="ذري للقراء والكاتب",
            scale_factor=1.2
        )
        success.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(success.animate_appear())
        
        # Highlight the successful file
        self.flash_emphasis(temp_file, color=C.SUCCESS)
        
        self.dramatic_pause()
        
        # ══════════════════════════════════════════════════════════════════════
        # CODA: IMPORTANT NOTE
        # ══════════════════════════════════════════════════════════════════════
        
        # Note about directory fsync
        note = create_bilingual(
            "ملاحظة: fsync على الدليل أيضاً للأمان الكامل",
            "Note: fsync on directory too for full safety",
            color_ar=C.WARNING,
            color_en=C.TEXT_TERTIARY,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        note.next_to(success, DOWN, buff=L.SPACING_MD)
        
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait_absorb(2)
    
    def create_write_indicator(self, target: Mobject) -> Rectangle:
        """Create a progress bar for write operation"""
        bar_bg = Rectangle(
            width=target.width * 0.8,
            height=0.15,
            stroke_color=C.TEXT_TERTIARY,
            fill_color=C.SUCCESS,
            fill_opacity=0,
            stroke_width=1
        )
        bar_bg.next_to(target, DOWN, buff=L.SPACING_SM)
        return bar_bg
