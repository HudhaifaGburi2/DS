"""
Scene 05: Trade-offs Analysis
=============================

Final comparison of trade-offs:
- Read amplification
- Write amplification
- Space amplification
- Real-world use cases

Narrative Arc:
1. Define amplification metrics
2. Compare amplification factors
3. Real-world database examples
4. Decision framework
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import C, T, F, L, DS, A
from base_scenes import ComparisonScene
from components.effects import MetricBar, WriteAmplification
from utils.text_helpers import create_bilingual, create_verdict_text


class Scene05_Tradeoffs(ComparisonScene):
    """
    Final trade-offs analysis and decision framework.
    
    Visual: Metric comparisons, amplification visualizations,
    and real-world database examples.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        self.create_title_card(
            "المقايضات",
            "Trade-offs Analysis"
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: AMPLIFICATION METRICS
        # ══════════════════════════════════════════════════════════════════════
        
        metrics_title = self.create_section_header("Amplification Metrics")
        self.play(Write(metrics_title))
        
        # Define the three amplifications
        amp_definitions = [
            ("Read Amplification", "عدد القراءات لكل استعلام", 
             "# of reads per query", C.READ_AMP),
            ("Write Amplification", "عدد الكتابات لكل تحديث",
             "# of writes per update", C.WRITE_AMP),
            ("Space Amplification", "المساحة الفعلية / المساحة المنطقية",
             "Actual space / Logical space", C.SPACE_AMP),
        ]
        
        amp_group = VGroup()
        for name, desc_ar, desc_en, color in amp_definitions:
            box = RoundedRectangle(
                width=3.5, height=1.8,
                color=color,
                fill_opacity=0.1,
                corner_radius=0.12
            )
            
            title = Text(name, font=F.CODE, color=color).scale(F.SIZE_LABEL)
            title.next_to(box.get_top(), DOWN, buff=L.SPACING_SM)
            
            desc = Text(desc_en, font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_TINY)
            desc.move_to(box.get_center())
            
            item = VGroup(box, title, desc)
            amp_group.add(item)
        
        amp_group.arrange(RIGHT, buff=L.SPACING_MD)
        amp_group.shift(UP * 0.3)
        
        self.play(
            LaggedStart(
                *[FadeIn(amp, scale=0.9) for amp in amp_group],
                lag_ratio=0.2
            )
        )
        self.wait_absorb()
        
        # Key insight
        insight = create_bilingual(
            "لا يمكن تحسين الثلاثة معاً!",
            "Cannot optimize all three simultaneously!",
            color_ar=C.WARNING,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        insight.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(FadeIn(insight, shift=UP * 0.2))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: COMPARISON BARS
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        compare_title = self.create_section_header("B-Tree vs LSM-Tree")
        self.play(Write(compare_title))
        
        # Headers
        btree_header = Text("B-Tree", font=F.CODE, color=C.BTREE_NODE).scale(F.SIZE_CAPTION)
        btree_header.move_to(LEFT * 2 + UP * 2)
        
        lsm_header = Text("LSM-Tree", font=F.CODE, color=C.LSM_MEMTABLE).scale(F.SIZE_CAPTION)
        lsm_header.move_to(RIGHT * 2 + UP * 2)
        
        self.play(Write(btree_header), Write(lsm_header))
        
        # Comparison metrics
        comparisons = [
            ("Read Amp", 1, 3, "lower is better", C.READ_AMP),
            ("Write Amp", 3, 10, "varies by workload", C.WRITE_AMP),
            ("Space Amp", 1.5, 1.1, "lower is better", C.SPACE_AMP),
        ]
        
        bar_group = VGroup()
        for i, (name, btree_val, lsm_val, note, color) in enumerate(comparisons):
            y_pos = 0.8 - i * 1.2
            
            # Label
            label = Text(name, font=F.CODE, color=color).scale(F.SIZE_LABEL)
            label.move_to(LEFT * 5 + UP * y_pos)
            
            # B-Tree bar
            max_val = max(btree_val, lsm_val)
            btree_width = (btree_val / max_val) * 2.5
            btree_bar = Rectangle(
                width=btree_width,
                height=0.35,
                fill_color=C.BTREE_NODE,
                fill_opacity=0.6,
                stroke_width=0
            )
            btree_bar.move_to(LEFT * 2 + UP * y_pos)
            
            btree_value = Text(f"{btree_val}×", font=F.CODE, color=C.BTREE_NODE).scale(F.SIZE_TINY)
            btree_value.next_to(btree_bar, RIGHT, buff=L.SPACING_TIGHT)
            
            # LSM bar
            lsm_width = (lsm_val / max_val) * 2.5
            lsm_bar = Rectangle(
                width=lsm_width,
                height=0.35,
                fill_color=C.LSM_MEMTABLE,
                fill_opacity=0.6,
                stroke_width=0
            )
            lsm_bar.move_to(RIGHT * 2 + UP * y_pos)
            
            lsm_value = Text(f"{lsm_val}×", font=F.CODE, color=C.LSM_MEMTABLE).scale(F.SIZE_TINY)
            lsm_value.next_to(lsm_bar, RIGHT, buff=L.SPACING_TIGHT)
            
            # Note
            note_text = Text(f"({note})", font=F.CODE, color=C.TEXT_TERTIARY).scale(F.SIZE_TINY)
            note_text.move_to(UP * y_pos + DOWN * 0.4)
            
            row = VGroup(label, btree_bar, btree_value, lsm_bar, lsm_value, note_text)
            bar_group.add(row)
        
        for row in bar_group:
            self.play(FadeIn(row, shift=LEFT * 0.2), run_time=T.FAST)
        
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: REAL-WORLD EXAMPLES
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        examples_title = self.create_section_header("Real-World Usage")
        self.play(Write(examples_title))
        
        # B-Tree databases
        btree_dbs = VGroup(
            Text("B-Tree Databases", font=F.CODE, color=C.BTREE_NODE).scale(F.SIZE_CAPTION),
            Text("• PostgreSQL", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_LABEL),
            Text("• MySQL (InnoDB)", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_LABEL),
            Text("• Oracle", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_LABEL),
            Text("• SQL Server", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_LABEL),
        )
        btree_dbs.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        btree_dbs.move_to(LEFT * 3.5)
        
        btree_use = Text("Best for: OLTP, random reads", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
        btree_use.next_to(btree_dbs, DOWN, buff=L.SPACING_SM)
        
        # LSM databases
        lsm_dbs = VGroup(
            Text("LSM-Tree Databases", font=F.CODE, color=C.LSM_MEMTABLE).scale(F.SIZE_CAPTION),
            Text("• RocksDB", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_LABEL),
            Text("• LevelDB", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_LABEL),
            Text("• Cassandra", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_LABEL),
            Text("• HBase", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_LABEL),
        )
        lsm_dbs.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        lsm_dbs.move_to(RIGHT * 3.5)
        
        lsm_use = Text("Best for: Write-heavy, time-series", font=F.CODE, color=C.SUCCESS).scale(F.SIZE_TINY)
        lsm_use.next_to(lsm_dbs, DOWN, buff=L.SPACING_SM)
        
        self.play(
            LaggedStart(
                *[FadeIn(item, shift=RIGHT * 0.1) for item in btree_dbs],
                lag_ratio=0.1
            ),
            LaggedStart(
                *[FadeIn(item, shift=LEFT * 0.1) for item in lsm_dbs],
                lag_ratio=0.1
            )
        )
        
        self.play(Write(btree_use), Write(lsm_use))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: DECISION FRAMEWORK
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        decision_title = self.create_section_header("How to Choose?")
        self.play(Write(decision_title))
        
        # Decision flowchart simplified as questions
        questions = VGroup()
        
        q1 = self._create_decision_box(
            "Read-heavy workload?",
            "→ B-Tree",
            C.BTREE_NODE
        )
        q1.shift(UP * 1.5)
        
        q2 = self._create_decision_box(
            "Write-heavy workload?",
            "→ LSM-Tree",
            C.LSM_MEMTABLE
        )
        q2.shift(UP * 0)
        
        q3 = self._create_decision_box(
            "Mixed workload?",
            "→ Consider hybrid or B-Tree",
            C.TEXT_ACCENT
        )
        q3.shift(DOWN * 1.5)
        
        questions.add(q1, q2, q3)
        
        self.play(
            LaggedStart(
                *[FadeIn(q, shift=LEFT * 0.3) for q in questions],
                lag_ratio=0.3
            )
        )
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 6: FINAL VERDICT
        # ══════════════════════════════════════════════════════════════════════
        
        self.scene_transition()
        
        # Final summary
        final_title = create_bilingual(
            "الخلاصة",
            "Conclusion",
            color_ar=C.TEXT_ACCENT,
            scale_ar=F.SIZE_HEADING,
            scale_en=F.SIZE_CAPTION
        )
        final_title.shift(UP * 2.5)
        
        self.play(FadeIn(final_title))
        
        # Summary points
        summary_points = VGroup(
            self._create_summary_point("B-Tree", "Read-optimized, in-place updates", C.BTREE_NODE),
            self._create_summary_point("LSM-Tree", "Write-optimized, append-only", C.LSM_MEMTABLE),
        )
        summary_points.arrange(DOWN, buff=L.SPACING_LG)
        summary_points.shift(UP * 0.5)
        
        self.play(
            LaggedStart(
                *[FadeIn(p, scale=0.9) for p in summary_points],
                lag_ratio=0.3
            )
        )
        self.wait_beat()
        
        # Final message
        verdict = create_verdict_text(
            "اختر بناءً على نمط الاستخدام",
            "Choose based on your workload pattern",
            color=C.SUCCESS
        )
        verdict.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(FadeIn(verdict, shift=UP * 0.2))
        
        # Both structures are valuable
        both_valid = Text(
            "Both are excellent solutions for their intended use cases!",
            font=F.CODE,
            color=C.TEXT_ACCENT
        ).scale(F.SIZE_CAPTION)
        both_valid.next_to(verdict, UP, buff=L.SPACING_MD)
        
        self.play(FadeIn(both_valid))
        self.wait_contemplate()
    
    def _create_decision_box(self, question: str, answer: str, color) -> VGroup:
        """Create a decision box with question and answer"""
        box = RoundedRectangle(
            width=7, height=0.9,
            color=color,
            fill_opacity=0.1,
            corner_radius=0.1
        )
        
        q_text = Text(question, font=F.CODE, color=C.TEXT_PRIMARY).scale(F.SIZE_LABEL)
        q_text.move_to(box.get_left() + RIGHT * 2.5)
        
        a_text = Text(answer, font=F.CODE, color=color).scale(F.SIZE_LABEL)
        a_text.move_to(box.get_right() + LEFT * 1.5)
        
        return VGroup(box, q_text, a_text)
    
    def _create_summary_point(self, name: str, desc: str, color) -> VGroup:
        """Create summary point with icon"""
        icon = Circle(
            radius=0.25,
            color=color,
            fill_opacity=0.2,
            stroke_width=2
        )
        
        name_text = Text(name, font=F.CODE, color=color).scale(F.SIZE_CAPTION)
        name_text.next_to(icon, RIGHT, buff=L.SPACING_SM)
        
        desc_text = Text(desc, font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_LABEL)
        desc_text.next_to(name_text, RIGHT, buff=L.SPACING_MD)
        
        return VGroup(icon, name_text, desc_text)
