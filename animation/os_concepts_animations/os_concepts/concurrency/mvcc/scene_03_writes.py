"""
Scene 03: Copy-on-Write
=======================

Shows how writers create new versions:
- Never modify existing versions
- Create new version with changes
- Atomic pointer swing

Narrative: Writers don't disturb readers.
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from config import C, T, F, L, A, OS
from base_scenes import ConcurrencyScene
from components.threads import Thread
from components.memory import SharedVariable, VersionChain
from utils.text_helpers import create_bilingual


class Scene03_Writes(ConcurrencyScene):
    """
    Demonstrates copy-on-write mechanism.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "الكتابة بالنسخ",
            "Copy-on-Write"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: CURRENT STATE
        # ══════════════════════════════════════════════════════════════════════
        
        section = self.create_section_header("Write Creates New Version")
        self.play(Write(section))
        
        # Current version
        current_box = RoundedRectangle(
            width=2, height=1.2,
            color=C.VERSION_CURRENT,
            fill_opacity=0.3,
            corner_radius=0.1
        )
        current_box.move_to(LEFT * 2)
        
        current_label = Text("v1 (current)", font=F.CODE, color=C.VERSION_CURRENT).scale(F.SIZE_TINY)
        current_label.next_to(current_box, UP, buff=L.SPACING_TIGHT)
        
        current_value = Text("balance = 100", font=F.CODE, color=C.TEXT_PRIMARY).scale(F.SIZE_LABEL)
        current_value.move_to(current_box.get_center())
        
        current_group = VGroup(current_box, current_label, current_value)
        
        # "Current" pointer
        current_ptr_label = Text("current →", font=F.CODE, color=C.TEXT_ACCENT).scale(F.SIZE_TINY)
        current_ptr_label.next_to(current_box, LEFT, buff=L.SPACING_SM)
        
        current_ptr = Arrow(
            current_ptr_label.get_right(),
            current_box.get_left(),
            color=C.TEXT_ACCENT,
            stroke_width=2,
            buff=0.1
        )
        
        self.play(FadeIn(current_group), Write(current_ptr_label), Create(current_ptr))
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: WRITER STARTS
        # ══════════════════════════════════════════════════════════════════════
        
        writer = Thread(thread_id=1)
        writer.move_to(UP * 2.5)
        
        writer_label = Text("Writer", font=F.CODE, color=C.THREAD_1).scale(F.SIZE_TINY)
        writer_label.next_to(writer, UP, buff=0.1)
        
        self.play(writer.animate_spawn(), FadeIn(writer_label))
        
        write_op = Text("UPDATE balance = 150", font=F.CODE, color=C.THREAD_1).scale(F.SIZE_TINY)
        write_op.next_to(writer, DOWN, buff=0.1)
        
        self.play(Write(write_op))
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: CREATE NEW VERSION (COPY)
        # ══════════════════════════════════════════════════════════════════════
        
        step1 = Text("Step 1: Create new version", font=F.CODE, color=C.INFO).scale(F.SIZE_CAPTION)
        step1.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(Write(step1))
        
        # New version appears
        new_box = RoundedRectangle(
            width=2, height=1.2,
            color=C.VERSION_NEW,
            fill_opacity=0.3,
            corner_radius=0.1
        )
        new_box.move_to(RIGHT * 2)
        
        new_label = Text("v2 (new)", font=F.CODE, color=C.VERSION_NEW).scale(F.SIZE_TINY)
        new_label.next_to(new_box, UP, buff=L.SPACING_TIGHT)
        
        new_value = Text("balance = 150", font=F.CODE, color=C.TEXT_PRIMARY).scale(F.SIZE_LABEL)
        new_value.move_to(new_box.get_center())
        
        new_group = VGroup(new_box, new_label, new_value)
        
        # Writer moves to create new version
        self.play(writer.animate.move_to(RIGHT * 2 + UP * 1.5))
        self.play(FadeIn(new_group, scale=0.8))
        
        # Link to previous
        version_link = Arrow(
            new_box.get_left(),
            current_box.get_right(),
            color=C.TEXT_TERTIARY,
            stroke_width=1.5,
            buff=0.1
        )
        link_label = Text("prev", font=F.CODE, color=C.TEXT_TERTIARY).scale(F.SIZE_TINY)
        link_label.next_to(version_link, UP, buff=0.05)
        
        self.play(Create(version_link), Write(link_label))
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: ATOMIC POINTER SWING
        # ══════════════════════════════════════════════════════════════════════
        
        step2 = Text("Step 2: Atomic pointer swing", font=F.CODE, color=C.WARNING).scale(F.SIZE_CAPTION)
        step2.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(Transform(step1, step2))
        
        # New current pointer
        new_ptr = Arrow(
            current_ptr_label.get_right(),
            new_box.get_left(),
            color=C.SUCCESS,
            stroke_width=3,
            buff=0.1
        )
        
        self.play(
            Transform(current_ptr, new_ptr),
            current_ptr_label.animate.set_color(C.SUCCESS),
            Flash(new_box, color=C.SUCCESS, line_length=0.2)
        )
        
        # Update labels
        self.play(
            current_label.animate.become(
                Text("v1 (old)", font=F.CODE, color=C.VERSION_OLD).scale(F.SIZE_TINY).next_to(current_box, UP, buff=L.SPACING_TIGHT)
            ),
            current_box.animate.set_color(C.VERSION_OLD).set_fill(opacity=0.15),
            new_label.animate.become(
                Text("v2 (current)", font=F.CODE, color=C.VERSION_CURRENT).scale(F.SIZE_TINY).next_to(new_box, UP, buff=L.SPACING_TIGHT)
            ),
            new_box.animate.set_color(C.VERSION_CURRENT)
        )
        
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 6: KEY PROPERTIES
        # ══════════════════════════════════════════════════════════════════════
        
        step3 = Text("Result:", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_CAPTION)
        step3.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(Transform(step1, step3))
        
        properties = VGroup(
            Text("✓ Old version still readable", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY),
            Text("✓ No in-place modification", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY),
            Text("✓ Atomic visibility", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY),
        )
        properties.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        properties.next_to(step1, UP, buff=L.SPACING_SM)
        
        self.play(FadeIn(properties))
        
        # Readers on old version unaffected
        old_reader = Text("Old readers: still see v1 ✓", font=F.CODE, color=C.INFO).scale(F.SIZE_TINY)
        old_reader.next_to(current_box, DOWN, buff=L.SPACING_MD)
        
        new_reader = Text("New readers: see v2 ✓", font=F.CODE, color=C.INFO).scale(F.SIZE_TINY)
        new_reader.next_to(new_box, DOWN, buff=L.SPACING_MD)
        
        self.play(Write(old_reader), Write(new_reader))
        self.wait_contemplate()
