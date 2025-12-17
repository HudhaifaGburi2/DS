"""
Scene 4: fsync and Storage Layers
==================================

Demonstrates the storage hierarchy and why fsync is necessary:
- Application writes go to OS page cache
- Without fsync, data can be lost on crash
- fsync forces data through all layers to disk

Narrative Arc:
- Show the storage stack (App → Cache → Device RAM → Disk)
- Demonstrate write without fsync (data stops at cache)
- Show crash scenario with data loss
- Demonstrate write with fsync (data reaches disk)
- Celebrate durability!
"""

import sys
sys.path.insert(0, '..')

from manim import *
from config import config, C, T, F, L, A, D
from base_scenes import DatabaseScene
from components.diagrams import StorageStack, StorageLayer
from components.effects import CrashEffect, SuccessCheckmark, DataFlowDot
from utils.text_helpers import create_bilingual


class Scene4_FSyncDiagram(DatabaseScene):
    """
    Chapter 1, Section 4: Understanding fsync
    
    Visual metaphor: Data traveling through layers,
    only safe when it reaches the bottom (disk).
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: INTRODUCE THE CONCEPT
        # ══════════════════════════════════════════════════════════════════════
        
        # Title card
        title = self.create_title_card(
            "fsync: ضمان الديمومة",
            "fsync: Ensuring Durability"
        )
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: BUILD THE STORAGE STACK
        # ══════════════════════════════════════════════════════════════════════
        
        # Create storage layers manually for more control
        layers = []
        layer_configs = [
            ("Application", "التطبيق", C.LAYER_APP),
            ("OS Page Cache", "ذاكرة النظام", C.LAYER_OS),
            ("Device RAM", "ذاكرة الجهاز", C.LAYER_DEVICE),
            ("Disk Storage", "القرص", C.LAYER_DISK),
        ]
        
        for i, (name, name_ar, color) in enumerate(layer_configs):
            layer = StorageLayer(
                name=name,
                name_ar=name_ar,
                color=color,
                width=6,
                height=0.9
            )
            layer.shift(UP * (1.5 - i * 1.2))
            layers.append(layer)
        
        # Animate layers appearing from top to bottom
        for layer in layers:
            self.play(
                FadeIn(layer, shift=DOWN * 0.3),
                run_time=T.FAST
            )
        
        self.wait_beat()
        
        # Add arrows between layers
        arrows = []
        for i in range(len(layers) - 1):
            arrow = Arrow(
                layers[i].get_bottom() + DOWN * 0.1,
                layers[i + 1].get_top() + UP * 0.1,
                color=C.TEXT_TERTIARY,
                stroke_width=2,
                buff=0.05
            )
            arrows.append(arrow)
            self.play(Create(arrow), run_time=T.QUICK)
        
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: WRITE WITHOUT FSYNC (DANGEROUS!)
        # ══════════════════════════════════════════════════════════════════════
        
        # Label for this scenario
        scenario1_label = create_bilingual(
            "Write() بدون fsync",
            "Write without fsync",
            color_ar=C.ERROR,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        scenario1_label.to_edge(LEFT, buff=L.MARGIN_LG)
        
        self.play(Write(scenario1_label))
        
        # Create data dot
        data_dot = DataFlowDot(color=C.ERROR, label="Data")
        data_dot.move_to(layers[0].get_center())
        
        self.play(FadeIn(data_dot))
        self.wait_beat()
        
        # Data moves to OS cache
        self.play(
            data_dot.animate.move_to(layers[1].get_center()),
            run_time=T.NORMAL
        )
        
        # Data STOPS here!
        stop_label = Text(
            "STOPS HERE!",
            font=F.CODE,
            color=C.ERROR
        ).scale(F.SIZE_CAPTION)
        stop_label.next_to(layers[1], RIGHT, buff=L.SPACING_MD)
        
        self.play(
            Write(stop_label),
            data_dot.animate_pulse()
        )
        self.wait_beat()
        
        # CRASH!
        crash = CrashEffect(
            text="💥",
            icon="",
            position=layers[1].get_right() + RIGHT * 1.5,
            scale_factor=0.8
        )
        crash_text = Text("CRASH!", font=F.BODY, color=C.ERROR).scale(F.SIZE_BODY)
        crash_text.next_to(crash, DOWN, buff=L.SPACING_TIGHT)
        
        self.play(
            FadeIn(crash, scale=0.5),
            Write(crash_text)
        )
        
        # Data is LOST
        self.play(
            FadeOut(data_dot, scale=0.3),
            Flash(layers[1].get_center(), color=C.ERROR, line_length=0.3),
            run_time=T.FAST
        )
        
        lost_label = create_bilingual(
            "البيانات ضاعت!",
            "Data LOST!",
            color_ar=C.ERROR,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        lost_label.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(Write(lost_label))
        self.wait_absorb()
        
        # Clean up scenario 1
        self.play(
            FadeOut(scenario1_label),
            FadeOut(stop_label),
            FadeOut(crash),
            FadeOut(crash_text),
            FadeOut(lost_label)
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: WRITE WITH FSYNC (SAFE!)
        # ══════════════════════════════════════════════════════════════════════
        
        # Label for this scenario
        scenario2_label = create_bilingual(
            "Write() + fsync()",
            "Write with fsync",
            color_ar=C.SUCCESS,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        scenario2_label.to_edge(LEFT, buff=L.MARGIN_LG)
        
        self.play(Write(scenario2_label))
        
        # Create new data dot
        data_dot2 = DataFlowDot(color=C.SUCCESS, label="Data")
        data_dot2.move_to(layers[0].get_center())
        
        self.play(FadeIn(data_dot2))
        
        # Data travels through ALL layers
        for i in range(1, len(layers)):
            # Highlight current layer
            self.play(
                layers[i].animate_highlight(),
                data_dot2.animate.move_to(layers[i].get_center()),
                run_time=T.FAST
            )
            self.wait_beat(0.3)
        
        # Data reaches disk!
        self.play(
            layers[-1].rect.animate.set_fill(color=C.SUCCESS, opacity=0.3),
            data_dot2.animate_pulse()
        )
        
        # Success indicators
        durable_label = Text(
            "✓ DURABLE",
            font=F.CODE,
            color=C.SUCCESS
        ).scale(F.SIZE_BODY)
        durable_label.next_to(layers[-1], RIGHT, buff=L.SPACING_MD)
        
        self.play(Write(durable_label))
        
        # Success message
        success_msg = create_bilingual(
            "البيانات آمنة على القرص!",
            "Data safely on disk!",
            color_ar=C.SUCCESS,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        success_msg.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(Write(success_msg))
        
        # Final checkmark
        checkmark = SuccessCheckmark(scale_factor=0.8)
        checkmark.next_to(success_msg, RIGHT, buff=L.SPACING_MD)
        
        self.play(checkmark.animate_appear())
        
        self.dramatic_pause()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: KEY TAKEAWAY
        # ══════════════════════════════════════════════════════════════════════
        
        # Clear everything except layers
        self.play(
            FadeOut(scenario2_label),
            FadeOut(data_dot2),
            FadeOut(durable_label),
            FadeOut(success_msg),
            FadeOut(checkmark),
            *[FadeOut(layer) for layer in layers],
            *[FadeOut(arrow) for arrow in arrows]
        )
        
        # Show key takeaway
        takeaway = create_bilingual(
            "fsync = ضمان وصول البيانات للقرص",
            "fsync = Guarantee data reaches disk",
            color_ar=C.PRIMARY_YELLOW,
            scale_ar=F.SIZE_HEADING,
            scale_en=F.SIZE_BODY
        )
        
        self.play(FadeIn(takeaway, scale=0.8))
        self.wait_absorb()
        
        # Warning about cost
        warning = create_bilingual(
            "⚠️ لكن fsync بطيء - استخدمه بحكمة",
            "But fsync is slow - use wisely",
            color_ar=C.WARNING,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        warning.next_to(takeaway, DOWN, buff=L.SPACING_LG)
        
        self.play(FadeIn(warning, shift=UP * 0.2))
        self.wait_absorb(2)
