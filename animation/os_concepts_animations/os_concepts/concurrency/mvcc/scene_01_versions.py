"""
Scene 01: Multiple Versions
===========================

Introduces MVCC concept:
- Keep multiple versions of data
- Each write creates new version
- Readers see consistent snapshot

Narrative: What if we keep old versions around?
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from config import C, T, F, L, A, OS
from base_scenes import TimelineScene
from components.timelines import TimeAxis, VersionTimeline, VersionMarker
from components.memory import VersionChain
from utils.text_helpers import create_bilingual


class Scene01_Versions(TimelineScene):
    """
    Introduces the concept of multiple data versions.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "التحكم متعدد الإصدارات",
            "Multi-Version Concurrency Control"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: THE KEY INSIGHT
        # ══════════════════════════════════════════════════════════════════════
        
        section = self.create_section_header("The Key Insight")
        self.play(Write(section))
        
        insight = create_bilingual(
            "ماذا لو لم نحذف البيانات القديمة؟",
            "What if we don't overwrite old data?",
            color_ar=C.TEXT_ACCENT,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        insight.move_to(UP * 0.5)
        
        self.play(FadeIn(insight))
        self.wait_absorb()
        
        # Traditional vs MVCC
        trad_label = Text("Traditional: Overwrite", font=F.CODE, color=C.WARNING).scale(F.SIZE_LABEL)
        trad_label.move_to(LEFT * 3 + DOWN * 1)
        
        trad_demo = VGroup()
        trad_box = Square(side_length=0.8, color=C.WARNING, fill_opacity=0.3)
        trad_val = Text("v1", font=F.CODE, color=C.WARNING).scale(F.SIZE_TINY)
        trad_val.move_to(trad_box.get_center())
        trad_demo.add(trad_box, trad_val)
        trad_demo.next_to(trad_label, DOWN, buff=L.SPACING_SM)
        
        mvcc_label = Text("MVCC: Keep versions", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL)
        mvcc_label.move_to(RIGHT * 3 + DOWN * 1)
        
        mvcc_demo = VGroup()
        for i, (opacity, label) in enumerate([(0.2, "v1"), (0.4, "v2"), (0.6, "v3")]):
            box = Square(side_length=0.6, color=C.SUCCESS, fill_opacity=opacity)
            val = Text(label, font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
            val.move_to(box.get_center())
            box.shift(RIGHT * i * 0.8)
            val.shift(RIGHT * i * 0.8)
            mvcc_demo.add(box, val)
        mvcc_demo.next_to(mvcc_label, DOWN, buff=L.SPACING_SM)
        
        self.play(Write(trad_label), FadeIn(trad_demo))
        self.play(Write(mvcc_label), FadeIn(mvcc_demo))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: VERSION TIMELINE
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        timeline_title = self.create_section_header("Version Timeline")
        self.play(Write(timeline_title))
        
        # Time axis
        time_axis = self.create_time_axis(y_pos=-2.5)
        self.play(time_axis.animate_create())
        
        # Object X timeline
        x_timeline = self.create_version_timeline("Object X", y_pos=0.5, color=C.SHARED_RESOURCE)
        self.play(FadeIn(x_timeline))
        
        # Add versions over time
        versions = []
        version_data = [
            (-4, "v1", "100", "old"),
            (-1.5, "v2", "150", "old"),
            (1.5, "v3", "200", "current"),
        ]
        
        for x, vid, val, state in version_data:
            marker = x_timeline.add_version(vid, x, state, val)
            self.play(x_timeline.animate_add_version(marker))
            self.wait_beat(0.5)
        
        # Show version chain
        chain_label = Text("Version Chain", font=F.CODE, color=C.TEXT_ACCENT).scale(F.SIZE_TINY)
        chain_label.next_to(x_timeline.version_group, UP, buff=L.SPACING_SM)
        
        # Arrows between versions
        arrows = VGroup()
        for i in range(len(x_timeline.versions) - 1):
            arrow = Arrow(
                x_timeline.versions[i].get_right(),
                x_timeline.versions[i + 1].get_left(),
                color=C.TEXT_TERTIARY,
                stroke_width=1.5,
                buff=0.1
            )
            arrows.add(arrow)
        
        self.play(Write(chain_label), Create(arrows))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: BENEFITS
        # ══════════════════════════════════════════════════════════════════════
        
        benefits = VGroup(
            Text("✓ Readers never block writers", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
            Text("✓ Writers never block readers", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
            Text("✓ Consistent snapshots for reads", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
        )
        benefits.arrange(DOWN, buff=L.SPACING_SM, aligned_edge=LEFT)
        benefits.to_edge(DOWN, buff=L.MARGIN_MD)
        
        self.play(
            LaggedStart(*[FadeIn(b) for b in benefits], lag_ratio=0.2)
        )
        
        self.wait_contemplate()
