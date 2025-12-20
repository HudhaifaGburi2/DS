"""
Scene 02: Snapshot Reads
========================

Shows how readers get consistent snapshots:
- Readers pin to a timestamp
- See consistent view of data
- Never blocked by writers

Narrative: Readers always see a consistent world.
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from config import C, T, F, L, A, OS
from base_scenes import TimelineScene
from components.threads import Thread
from components.timelines import TimeAxis, VersionTimeline, SnapshotPointer
from utils.text_helpers import create_bilingual


class Scene02_Reads(TimelineScene):
    """
    Demonstrates snapshot isolation for readers.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "قراءة اللقطات",
            "Snapshot Reads"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: SETUP TIMELINE WITH VERSIONS
        # ══════════════════════════════════════════════════════════════════════
        
        section = self.create_section_header("Reader Gets Snapshot")
        self.play(Write(section))
        
        # Time axis
        time_axis = self.create_time_axis(y_pos=-2.5)
        self.play(time_axis.animate_create())
        
        # Object timeline with versions
        obj_timeline = self.create_version_timeline("Account", y_pos=0, color=C.SHARED_RESOURCE)
        self.play(FadeIn(obj_timeline))
        
        # Pre-existing versions
        v1 = obj_timeline.add_version("v1", -4, "old", "$100")
        v2 = obj_timeline.add_version("v2", -1, "current", "$150")
        
        self.play(FadeIn(v1), FadeIn(v2))
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: READER STARTS TRANSACTION
        # ══════════════════════════════════════════════════════════════════════
        
        reader = Thread(thread_id=1)
        reader.move_to(LEFT * 5 + UP * 2)
        
        reader_label = Text("Reader T1", font=F.CODE, color=C.THREAD_1).scale(F.SIZE_TINY)
        reader_label.next_to(reader, UP, buff=0.1)
        
        self.play(reader.animate_spawn(), FadeIn(reader_label))
        
        # Reader pins to snapshot at t=-0.5 (sees v2)
        snapshot_time = Text("Snapshot @ t=now", font=F.CODE, color=C.SNAPSHOT).scale(F.SIZE_TINY)
        snapshot_time.next_to(reader, DOWN, buff=0.1)
        
        self.play(Write(snapshot_time))
        
        # Create snapshot pointer to v2
        snapshot_ptr = SnapshotPointer("T1", v2, y_offset=0.8)
        self.play(snapshot_ptr.animate_pin())
        
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: WRITER CREATES NEW VERSION
        # ══════════════════════════════════════════════════════════════════════
        
        writer = Thread(thread_id=2)
        writer.move_to(RIGHT * 4 + UP * 2)
        
        writer_label = Text("Writer T2", font=F.CODE, color=C.THREAD_2).scale(F.SIZE_TINY)
        writer_label.next_to(writer, UP, buff=0.1)
        
        self.play(writer.animate_spawn(), FadeIn(writer_label))
        
        # Writer creates v3
        write_indicator = Text("Creating v3...", font=F.CODE, color=C.THREAD_2).scale(F.SIZE_TINY)
        write_indicator.next_to(writer, DOWN, buff=0.1)
        
        self.play(Write(write_indicator))
        
        v3 = obj_timeline.add_version("v3", 2, "new", "$200")
        self.play(obj_timeline.animate_add_version(v3))
        
        # Mark v2 as old
        self.play(v2.animate_mark_old())
        
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: READER STILL SEES OLD SNAPSHOT
        # ══════════════════════════════════════════════════════════════════════
        
        key_point = Text(
            "T1 still sees v2 ($150)!",
            font=F.CODE,
            color=C.SUCCESS
        ).scale(F.SIZE_CAPTION)
        key_point.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(FadeIn(key_point, scale=0.8))
        
        # Highlight the snapshot still pointing to v2
        self.play(
            v2.box.animate.set_stroke(color=C.THREAD_1, width=3),
            Flash(v2.box, color=C.THREAD_1, line_length=0.2)
        )
        
        # Reader reads value
        read_result = Text("T1 reads: $150 ✓", font=F.CODE, color=C.THREAD_1).scale(F.SIZE_TINY)
        read_result.next_to(snapshot_ptr.reader, RIGHT, buff=L.SPACING_SM)
        
        self.play(Write(read_result))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 6: NO BLOCKING
        # ══════════════════════════════════════════════════════════════════════
        
        self.play(FadeOut(key_point))
        
        no_block = create_bilingual(
            "لا حظر! القارئ والكاتب يعملان معاً",
            "No blocking! Reader and writer work concurrently",
            color_ar=C.SUCCESS,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        no_block.to_edge(DOWN, buff=L.MARGIN_MD)
        
        self.play(FadeIn(no_block))
        
        # Show both active
        self.play(
            reader.body.animate.set_stroke(color=C.SUCCESS, width=3),
            writer.body.animate.set_stroke(color=C.SUCCESS, width=3)
        )
        
        parallel_label = Text(
            "Both running in PARALLEL!",
            font=F.CODE,
            color=C.SUCCESS
        ).scale(F.SIZE_LABEL)
        parallel_label.move_to(UP * 2.8)
        
        self.play(FadeIn(parallel_label))
        self.wait_contemplate()
