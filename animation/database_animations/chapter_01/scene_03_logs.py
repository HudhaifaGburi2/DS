"""
Scene 3: Append-Only Logs
==========================

Demonstrates append-only log structure with checksums:
- Log entries are appended sequentially
- Each entry has a checksum for validation
- Corrupt entries can be detected and discarded
- Recovery is straightforward

Narrative Arc:
- Show log building up entry by entry
- Explain entry structure (header + data + checksum)
- Simulate a crash with partial write
- Demonstrate recovery process
"""

import sys
sys.path.insert(0, '..')

from manim import *
from config import config, C, T, F, L, A, D
from base_scenes import DatabaseScene
from components.diagrams import LogEntry, LogSequence, EntryStructure
from components.effects import CrashEffect, SuccessCheckmark, CorruptionEffect
from utils.text_helpers import create_bilingual, format_step_label


class Scene3_AppendOnlyLog(DatabaseScene):
    """
    Chapter 1, Section 3: Append-Only Logs
    
    Visual metaphor: A growing scroll where each entry
    is carefully verified before being accepted.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: INTRODUCE THE LOG CONCEPT
        # ══════════════════════════════════════════════════════════════════════
        
        # Title card
        title = self.create_title_card(
            "سجلات الإلحاق فقط",
            "Append-Only Logs"
        )
        self.wait_beat()
        
        # Explain the concept
        concept = create_bilingual(
            "الكتابة فقط في نهاية الملف",
            "Only write at end of file",
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        concept.move_to(ORIGIN + UP * 1)
        
        self.play(FadeIn(concept))
        self.wait_absorb()
        self.play(FadeOut(concept))
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: BUILD THE LOG
        # ══════════════════════════════════════════════════════════════════════
        
        # Create empty log area
        log_label = Text(
            "Log File",
            font=F.CODE,
            color=C.TEXT_SECONDARY
        ).scale(F.SIZE_CAPTION)
        log_label.to_edge(UP, buff=L.MARGIN_XL).shift(DOWN * 0.5)
        
        self.play(Write(log_label))
        
        # Operations to log
        operations = [
            ("set a=1", "valid"),
            ("set b=2", "valid"),
            ("set a=3", "valid"),
            ("del b", "valid"),
        ]
        
        # Create and animate log entries one by one
        log_entries = []
        
        for i, (op, status) in enumerate(operations):
            entry = LogEntry(
                operation=op,
                index=i,
                status=status
            )
            
            # Position entries in a row
            entry.shift(LEFT * 3.5 + RIGHT * i * 2.2)
            
            log_entries.append(entry)
            
            # Animate entry appearing
            self.play(entry.animate_appear())
            
            # Show validation checkmark
            self.play(entry.animate_validate())
            
            self.wait_beat(0.5)
        
        log_group = VGroup(*log_entries)
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: EXPLAIN ENTRY STRUCTURE
        # ══════════════════════════════════════════════════════════════════════
        
        # Move log up and show structure explanation
        self.play(log_group.animate.shift(UP * 1.5))
        
        structure_title = create_bilingual(
            "بنية الإدخال",
            "Entry Structure",
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        structure_title.shift(DOWN * 0.5)
        
        self.play(Write(structure_title))
        
        # Show detailed entry structure
        entry_structure = EntryStructure(
            header_text="Header\n(Size+CRC)",
            data_text="Data\nset a=1"
        )
        entry_structure.next_to(structure_title, DOWN, buff=L.SPACING_LG)
        
        self.play(entry_structure.animate_build())
        self.wait_absorb()
        
        # Explain checksum purpose
        checksum_note = create_bilingual(
            "CRC يكشف البيانات الفاسدة",
            "CRC detects corrupted data",
            color_ar=C.PRIMARY_YELLOW,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        checksum_note.next_to(entry_structure, DOWN, buff=L.SPACING_MD)
        
        self.play(FadeIn(checksum_note))
        self.wait_absorb()
        
        # Clean up structure explanation
        self.play(
            FadeOut(structure_title),
            FadeOut(entry_structure),
            FadeOut(checksum_note)
        )
        
        # Move log back to center
        self.play(log_group.animate.shift(DOWN * 1.5))
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: CRASH DURING WRITE
        # ══════════════════════════════════════════════════════════════════════
        
        crash_label = create_bilingual(
            "محاكاة الانهيار",
            "Simulating crash",
            color_ar=C.WARNING,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        crash_label.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(Write(crash_label))
        self.wait_beat()
        
        # Add a corrupted entry (partial write)
        corrupted_entry = LogEntry(
            operation="set c=???",
            index=4,
            status="invalid"
        )
        corrupted_entry.shift(LEFT * 3.5 + RIGHT * 4 * 2.2)
        
        self.play(corrupted_entry.animate_appear())
        
        # Show crash happening
        crash = CrashEffect(
            text="CRASH!",
            position=corrupted_entry.get_center() + DOWN * 1.5,
            scale_factor=0.8
        )
        
        self.play(crash.animate_appear())
        self.wait_beat()
        
        # Mark entry as corrupted
        self.play(corrupted_entry.animate_invalidate())
        
        self.wait_absorb()
        
        # Fade out crash
        self.play(FadeOut(crash), FadeOut(crash_label))
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: RECOVERY PROCESS
        # ══════════════════════════════════════════════════════════════════════
        
        recovery_label = create_bilingual(
            "عملية الاسترداد",
            "Recovery Process",
            color_ar=C.PRIMARY_YELLOW,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        recovery_label.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(Write(recovery_label))
        
        # Highlight each entry being checked
        for i, entry in enumerate(log_entries):
            check_box = SurroundingRectangle(
                entry,
                color=C.PRIMARY_YELLOW,
                buff=0.1
            )
            self.play(Create(check_box), run_time=T.QUICK)
            
            # Show validation
            self.play(
                check_box.animate.set_color(C.SUCCESS),
                run_time=T.INSTANT
            )
            self.play(FadeOut(check_box), run_time=T.INSTANT)
        
        # Check corrupted entry
        corrupt_check = SurroundingRectangle(
            corrupted_entry,
            color=C.PRIMARY_YELLOW,
            buff=0.1
        )
        self.play(Create(corrupt_check))
        
        # Detection!
        detect_label = Text(
            "CRC Mismatch!",
            font=F.CODE,
            color=C.ERROR
        ).scale(F.SIZE_CAPTION)
        detect_label.next_to(corrupted_entry, UP, buff=L.SPACING_SM)
        
        self.play(
            corrupt_check.animate.set_color(C.ERROR),
            Write(detect_label)
        )
        self.wait_beat()
        
        # Discard corrupted entry
        discard_label = create_bilingual(
            "تجاهل الإدخال الفاسد",
            "Discarding corrupt entry",
            color_ar=C.SUCCESS,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        discard_label.next_to(recovery_label, UP, buff=L.SPACING_MD)
        
        self.play(
            FadeOut(recovery_label),
            Write(discard_label)
        )
        
        self.play(
            FadeOut(corrupted_entry),
            FadeOut(corrupt_check),
            FadeOut(detect_label),
            run_time=T.NORMAL
        )
        
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 6: FINAL STATE
        # ══════════════════════════════════════════════════════════════════════
        
        self.play(FadeOut(discard_label))
        
        # Show final state
        final_label = create_bilingual(
            "الحالة النهائية",
            "Final State",
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        final_label.to_edge(DOWN, buff=L.MARGIN_XL)
        
        self.play(Write(final_label))
        
        # Show current values
        state_box = Rectangle(
            width=3,
            height=1.5,
            color=C.SUCCESS,
            fill_opacity=0.1,
            stroke_width=2
        )
        state_box.shift(DOWN * 1.5)
        
        state_text = Text(
            "a = 3\nb = (deleted)",
            font=F.CODE,
            color=C.SUCCESS
        ).scale(F.SIZE_BODY)
        state_text.move_to(state_box)
        
        self.play(
            Create(state_box),
            Write(state_text)
        )
        
        # Success checkmark
        success = SuccessCheckmark(scale_factor=0.8)
        success.next_to(state_box, RIGHT, buff=L.SPACING_MD)
        
        self.play(success.animate_appear())
        
        # Flash the valid entries
        for entry in log_entries:
            self.play(
                Indicate(entry, color=C.SUCCESS, scale_factor=1.05),
                run_time=T.INSTANT
            )
        
        self.dramatic_pause()
        
        # ══════════════════════════════════════════════════════════════════════
        # CODA: KEY ADVANTAGES
        # ══════════════════════════════════════════════════════════════════════
        
        # Clear and show advantages
        self.play(
            FadeOut(log_group),
            FadeOut(final_label),
            FadeOut(state_box),
            FadeOut(state_text),
            FadeOut(success),
            FadeOut(log_label)
        )
        
        advantages_title = create_bilingual(
            "مزايا سجلات الإلحاق",
            "Advantages of Append-Only Logs",
            scale_ar=F.SIZE_HEADING,
            scale_en=F.SIZE_BODY
        )
        advantages_title.shift(UP * 2)
        
        self.play(Write(advantages_title))
        
        advantages = [
            ("✓ ذري لانقطاع الطاقة", "Power-loss atomic"),
            ("✓ ذري للقراء والكاتب", "Reader-writer atomic"),
            ("✓ تحديثات تدريجية", "Incremental updates"),
        ]
        
        adv_group = VGroup()
        for i, (ar, en) in enumerate(advantages):
            adv = create_bilingual(
                ar, en,
                color_ar=C.SUCCESS,
                scale_ar=F.SIZE_BODY,
                scale_en=F.SIZE_CAPTION
            )
            adv.shift(DOWN * i * 0.8)
            adv_group.add(adv)
        
        adv_group.next_to(advantages_title, DOWN, buff=L.SPACING_LG)
        
        self.play(
            LaggedStart(
                *[FadeIn(adv, shift=UP * 0.2) for adv in adv_group],
                lag_ratio=0.3
            )
        )
        
        self.wait_absorb(2)
