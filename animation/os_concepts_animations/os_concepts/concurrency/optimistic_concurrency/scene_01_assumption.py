"""
Scene 01: The Optimistic Assumption
===================================

Introduces optimistic concurrency control:
- Assume conflicts are rare
- Don't lock during execution
- Check for conflicts at the end

Narrative: What if we're optimistic about contention?
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from config import C, T, F, L, A, OS
from base_scenes import ConcurrencyScene
from components.threads import Thread
from components.critical_sections import SharedResource
from utils.text_helpers import create_bilingual


class Scene01_Assumption(ConcurrencyScene):
    """
    Introduces the optimistic concurrency model.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "التحكم التفاؤلي",
            "Optimistic Concurrency Control"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: THE PESSIMISTIC VS OPTIMISTIC MINDSET
        # ══════════════════════════════════════════════════════════════════════
        
        section = self.create_section_header("Two Approaches")
        self.play(Write(section))
        
        # Pessimistic box
        pess_box = RoundedRectangle(
            width=4.5, height=2.5,
            color=C.WARNING,
            fill_opacity=0.1,
            corner_radius=0.15
        )
        pess_box.shift(LEFT * 3)
        
        pess_title = Text("Pessimistic", font=F.CODE, color=C.WARNING).scale(F.SIZE_HEADING)
        pess_title.next_to(pess_box, UP, buff=L.SPACING_TIGHT)
        
        pess_points = VGroup(
            Text('"Conflicts are likely"', font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_TINY),
            Text("→ Lock BEFORE access", font=F.CODE, color=C.WARNING).scale(F.SIZE_TINY),
            Text("→ Block if locked", font=F.CODE, color=C.WARNING).scale(F.SIZE_TINY),
        )
        pess_points.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        pess_points.move_to(pess_box.get_center())
        
        # Optimistic box
        opt_box = RoundedRectangle(
            width=4.5, height=2.5,
            color=C.SUCCESS,
            fill_opacity=0.1,
            corner_radius=0.15
        )
        opt_box.shift(RIGHT * 3)
        
        opt_title = Text("Optimistic", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_HEADING)
        opt_title.next_to(opt_box, UP, buff=L.SPACING_TIGHT)
        
        opt_points = VGroup(
            Text('"Conflicts are rare"', font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_TINY),
            Text("→ No locks during work", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY),
            Text("→ Validate at commit", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY),
        )
        opt_points.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        opt_points.move_to(opt_box.get_center())
        
        self.play(
            FadeIn(pess_box), Write(pess_title),
            FadeIn(opt_box), Write(opt_title)
        )
        self.play(
            FadeIn(pess_points),
            FadeIn(opt_points)
        )
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: OCC PHASES
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        phases_title = self.create_section_header("OCC Three Phases")
        self.play(Write(phases_title))
        
        # Phase boxes
        phase1 = self._create_phase_box("1. READ", "Work on local copy", C.INFO)
        phase2 = self._create_phase_box("2. VALIDATE", "Check for conflicts", C.WARNING)
        phase3 = self._create_phase_box("3. WRITE", "Commit if valid", C.SUCCESS)
        
        phases = VGroup(phase1, phase2, phase3)
        phases.arrange(RIGHT, buff=L.SPACING_LG)
        
        # Arrows between phases
        arrow1 = Arrow(phase1.get_right(), phase2.get_left(), color=C.TEXT_TERTIARY, stroke_width=2)
        arrow2 = Arrow(phase2.get_right(), phase3.get_left(), color=C.TEXT_TERTIARY, stroke_width=2)
        
        self.play(
            LaggedStart(
                FadeIn(phase1),
                Create(arrow1),
                FadeIn(phase2),
                Create(arrow2),
                FadeIn(phase3),
                lag_ratio=0.3
            )
        )
        self.wait_beat()
        
        # Key insight
        insight = create_bilingual(
            "لا أقفال أثناء العمل!",
            "No locks during work!",
            color_ar=C.SUCCESS,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        insight.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(FadeIn(insight, scale=0.8))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: WHEN IT WORKS WELL
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        works_title = self.create_section_header("When OCC Works Best")
        self.play(Write(works_title))
        
        scenarios = VGroup(
            Text("✓ Low contention workloads", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
            Text("✓ Mostly read operations", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
            Text("✓ Short transactions", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
            Text("✓ Conflicts easily detected", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
        )
        scenarios.arrange(DOWN, buff=L.SPACING_SM, aligned_edge=LEFT)
        scenarios.move_to(LEFT * 2.5)
        
        bad_scenarios = VGroup(
            Text("✗ High contention", font=F.CODE, color=C.ERROR).scale(F.SIZE_LABEL),
            Text("✗ Many writes to same data", font=F.CODE, color=C.ERROR).scale(F.SIZE_LABEL),
            Text("✗ Long transactions", font=F.CODE, color=C.ERROR).scale(F.SIZE_LABEL),
        )
        bad_scenarios.arrange(DOWN, buff=L.SPACING_SM, aligned_edge=LEFT)
        bad_scenarios.move_to(RIGHT * 2.5)
        
        good_label = Text("Good for:", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_CAPTION)
        good_label.next_to(scenarios, UP, buff=L.SPACING_SM)
        
        bad_label = Text("Bad for:", font=F.CODE, color=C.ERROR).scale(F.SIZE_CAPTION)
        bad_label.next_to(bad_scenarios, UP, buff=L.SPACING_SM)
        
        self.play(Write(good_label), Write(bad_label))
        self.play(
            LaggedStart(*[FadeIn(s) for s in scenarios], lag_ratio=0.1),
            LaggedStart(*[FadeIn(s) for s in bad_scenarios], lag_ratio=0.1)
        )
        
        self.wait_contemplate()
    
    def _create_phase_box(self, title: str, desc: str, color) -> VGroup:
        """Create a phase box"""
        box = RoundedRectangle(
            width=2.8, height=1.8,
            color=color,
            fill_opacity=0.15,
            corner_radius=0.1
        )
        
        title_text = Text(title, font=F.CODE, color=color).scale(F.SIZE_LABEL)
        title_text.next_to(box.get_top(), DOWN, buff=L.SPACING_SM)
        
        desc_text = Text(desc, font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_TINY)
        desc_text.move_to(box.get_center() + DOWN * 0.2)
        
        return VGroup(box, title_text, desc_text)
