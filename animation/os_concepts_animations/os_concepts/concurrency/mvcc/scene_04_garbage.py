"""
Scene 04: Garbage Collection
============================

Shows version cleanup:
- Track active snapshots
- Identify unreachable versions
- Reclaim space

Narrative: We can't keep versions forever.
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from config import C, T, F, L, A, OS
from base_scenes import TimelineScene
from components.timelines import TimeAxis, VersionTimeline, VersionMarker
from utils.text_helpers import create_bilingual


class Scene04_Garbage(TimelineScene):
    """
    Demonstrates garbage collection of old versions.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "تنظيف الإصدارات",
            "Version Garbage Collection"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: THE PROBLEM - VERSION ACCUMULATION
        # ══════════════════════════════════════════════════════════════════════
        
        section = self.create_section_header("The Problem: Space Growth")
        self.play(Write(section))
        
        problem = create_bilingual(
            "الإصدارات تتراكم وتستهلك المساحة",
            "Versions accumulate and consume space",
            color_ar=C.WARNING,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        problem.move_to(UP * 0.5)
        
        self.play(FadeIn(problem))
        
        # Show accumulating versions
        versions = VGroup()
        for i in range(8):
            box = RoundedRectangle(
                width=0.8, height=0.5,
                color=C.VERSION_OLD if i < 7 else C.VERSION_CURRENT,
                fill_opacity=0.2 if i < 7 else 0.4,
                corner_radius=0.05
            )
            label = Text(f"v{i+1}", font=F.CODE, color=C.VERSION_OLD if i < 7 else C.VERSION_CURRENT).scale(F.SIZE_TINY)
            label.move_to(box.get_center())
            versions.add(VGroup(box, label))
        
        versions.arrange(RIGHT, buff=0.2)
        versions.shift(DOWN * 1)
        
        self.play(
            LaggedStart(
                *[FadeIn(v, scale=0.8) for v in versions],
                lag_ratio=0.1
            )
        )
        
        space_warning = Text("Space usage keeps growing!", font=F.CODE, color=C.ERROR).scale(F.SIZE_TINY)
        space_warning.next_to(versions, DOWN, buff=L.SPACING_SM)
        
        self.play(Write(space_warning))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: SOLUTION - GARBAGE COLLECTION
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        gc_title = self.create_section_header("Garbage Collection")
        self.play(Write(gc_title))
        
        # Time axis with active snapshots
        time_axis = self.create_time_axis(y_pos=-2.5)
        self.play(time_axis.animate_create())
        
        # Version timeline
        obj_timeline = self.create_version_timeline("Data X", y_pos=0, color=C.SHARED_RESOURCE)
        self.play(FadeIn(obj_timeline))
        
        # Add versions
        v1 = obj_timeline.add_version("v1", -4, "old")
        v2 = obj_timeline.add_version("v2", -2, "old")
        v3 = obj_timeline.add_version("v3", 0, "old")
        v4 = obj_timeline.add_version("v4", 2, "current")
        
        self.play(FadeIn(v1), FadeIn(v2), FadeIn(v3), FadeIn(v4))
        
        # Active snapshot indicator
        active_snapshot = Text("Active snapshot @ t=-1", font=F.CODE, color=C.SNAPSHOT).scale(F.SIZE_TINY)
        active_snapshot.move_to(UP * 1.5 + LEFT * 1)
        
        snapshot_line = DashedLine(
            active_snapshot.get_bottom(),
            v2.get_top() + UP * 0.1,
            color=C.SNAPSHOT,
            stroke_width=1.5
        )
        
        self.play(Write(active_snapshot), Create(snapshot_line))
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: IDENTIFY GARBAGE
        # ══════════════════════════════════════════════════════════════════════
        
        gc_rule = Text(
            "Rule: Can GC versions older than oldest active snapshot",
            font=F.CODE,
            color=C.TEXT_ACCENT
        ).scale(F.SIZE_TINY)
        gc_rule.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(Write(gc_rule))
        
        # v1 can be collected (older than snapshot at -1)
        garbage_indicator = Text("GARBAGE", font=F.CODE, color=C.GARBAGE).scale(F.SIZE_TINY)
        garbage_indicator.next_to(v1, DOWN, buff=L.SPACING_TIGHT)
        
        self.play(
            v1.box.animate.set_color(C.GARBAGE).set_fill(opacity=0.1),
            v1.id_label.animate.set_color(C.GARBAGE),
            FadeIn(garbage_indicator)
        )
        
        # v2, v3, v4 are still needed
        needed = VGroup()
        for v in [v2, v3, v4]:
            needed_label = Text("needed", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
            needed_label.next_to(v, DOWN, buff=L.SPACING_TIGHT)
            needed.add(needed_label)
        
        self.play(LaggedStart(*[FadeIn(n) for n in needed], lag_ratio=0.1))
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: PERFORM GC
        # ══════════════════════════════════════════════════════════════════════
        
        gc_action = Text("Running GC...", font=F.CODE, color=C.GARBAGE).scale(F.SIZE_CAPTION)
        gc_action.to_edge(UP, buff=L.MARGIN_SM).shift(DOWN * 0.8)
        
        self.play(Write(gc_action))
        
        # Sweep animation
        sweep_line = Line(
            LEFT * 5.5 + UP * 0.5,
            LEFT * 5.5 + DOWN * 0.5,
            color=C.GARBAGE,
            stroke_width=3
        )
        
        self.play(
            sweep_line.animate.move_to(v1.get_center()),
            run_time=T.NORMAL
        )
        
        # Remove v1
        self.play(
            v1.animate.set_opacity(0).shift(DOWN * 0.5),
            garbage_indicator.animate.set_opacity(0),
            FadeOut(sweep_line)
        )
        
        # Show space reclaimed
        reclaimed = Text("✓ Space reclaimed!", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL)
        reclaimed.next_to(gc_rule, UP, buff=L.SPACING_SM)
        
        self.play(FadeIn(reclaimed, scale=0.8))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 6: MVCC SUMMARY
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        summary_title = self.create_section_header("MVCC Summary")
        self.play(Write(summary_title))
        
        summary = VGroup(
            Text("✓ Readers see consistent snapshots", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
            Text("✓ Writers create new versions", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
            Text("✓ No read-write blocking", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
            Text("✓ GC cleans old versions", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_LABEL),
        )
        summary.arrange(DOWN, buff=L.SPACING_SM, aligned_edge=LEFT)
        summary.move_to(UP * 0.3)
        
        self.play(
            LaggedStart(*[FadeIn(s) for s in summary], lag_ratio=0.15)
        )
        
        # Used by
        used_by = VGroup(
            Text("Used by: PostgreSQL, MySQL InnoDB, Oracle, SQL Server", font=F.CODE, color=C.INFO).scale(F.SIZE_TINY),
        )
        used_by.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(FadeIn(used_by))
        
        # Final insight
        final = create_bilingual(
            "MVCC = التوازي بدون أقفال للقراءة",
            "MVCC = Concurrency without read locks",
            color_ar=C.TEXT_ACCENT,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        final.next_to(used_by, UP, buff=L.SPACING_MD)
        
        self.play(FadeIn(final))
        self.wait_contemplate()
