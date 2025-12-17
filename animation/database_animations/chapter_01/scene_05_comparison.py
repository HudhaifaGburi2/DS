"""
Scene 5: Comparison Table
==========================

Compares the three approaches:
- In-Place Updates
- Atomic Rename
- Append-Only Logs

Shows which properties each approach provides.
"""

import sys
sys.path.insert(0, '..')

from manim import *
from config import config, C, T, F, L, A, D
from base_scenes import ComparisonScene
from components.effects import SuccessCheckmark
from utils.text_helpers import create_bilingual


class Scene5_ComparisonTable(ComparisonScene):
    """
    Chapter 1, Section 5: Comparing Approaches
    
    Visual: Clean comparison table that builds up,
    with the winner highlighted at the end.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        # Title card
        title = self.create_title_card(
            "مقارنة الطرق",
            "Comparison of Approaches"
        )
        self.wait_beat()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: BUILD THE TABLE
        # ══════════════════════════════════════════════════════════════════════
        
        # Table data
        headers = ["Method", "Power-Loss\nAtomic", "Reader-Writer\nAtomic", "Incremental"]
        
        rows = [
            ["In-Place", "✗", "✗", "✗"],
            ["Rename", "✗*", "✓", "✗"],
            ["Append-Only\nLog", "✓", "✓", "✓"]
        ]
        
        # Create table manually for better control
        table_group = VGroup()
        
        # Create header row
        header_cells = VGroup()
        for i, header in enumerate(headers):
            cell = self.create_cell(header, is_header=True)
            cell.shift(RIGHT * i * 2.2)
            header_cells.add(cell)
        
        header_cells.move_to(ORIGIN + UP * 1.5)
        table_group.add(header_cells)
        
        # Create data rows
        row_groups = []
        for row_idx, row in enumerate(rows):
            row_cells = VGroup()
            for col_idx, cell_text in enumerate(row):
                is_first_col = col_idx == 0
                is_check = cell_text == "✓"
                is_cross = cell_text in ["✗", "✗*"]
                
                cell = self.create_cell(
                    cell_text,
                    is_header=is_first_col,
                    is_success=is_check,
                    is_error=is_cross
                )
                cell.shift(RIGHT * col_idx * 2.2)
                row_cells.add(cell)
            
            row_cells.move_to(ORIGIN + UP * (0.5 - row_idx * 1.0))
            row_groups.append(row_cells)
            table_group.add(row_cells)
        
        # Center the table
        table_group.move_to(ORIGIN)
        
        # Animate table building
        # First headers
        self.play(
            LaggedStart(
                *[FadeIn(cell, shift=DOWN * 0.2) for cell in header_cells],
                lag_ratio=0.1
            )
        )
        self.wait_beat()
        
        # Then each row
        for row_cells in row_groups:
            self.play(
                LaggedStart(
                    *[FadeIn(cell, shift=LEFT * 0.2) for cell in row_cells],
                    lag_ratio=0.1
                )
            )
            self.wait_beat(0.5)
        
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: HIGHLIGHT THE WINNER
        # ══════════════════════════════════════════════════════════════════════
        
        # Highlight the append-only log row (index 2)
        winner_row = row_groups[2]
        winner_box = SurroundingRectangle(
            winner_row,
            color=C.SUCCESS,
            buff=0.15,
            corner_radius=0.1,
            stroke_width=3
        )
        
        self.play(Create(winner_box))
        
        # Add "WINNER" badge
        winner_badge = Text(
            "✓ BEST",
            font=F.CODE,
            color=C.SUCCESS
        ).scale(F.SIZE_CAPTION)
        winner_badge.next_to(winner_row, RIGHT, buff=L.SPACING_MD)
        
        self.play(Write(winner_badge))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: ADD FOOTNOTE
        # ══════════════════════════════════════════════════════════════════════
        
        # Note about rename needing directory fsync
        footnote = create_bilingual(
            "* يحتاج fsync على الدليل",
            "* Needs fsync on directory",
            color_ar=C.WARNING,
            color_en=C.TEXT_TERTIARY,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        footnote.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(FadeIn(footnote))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: SUMMARY
        # ══════════════════════════════════════════════════════════════════════
        
        # Clear and show summary
        self.play(
            FadeOut(table_group),
            FadeOut(winner_box),
            FadeOut(winner_badge),
            FadeOut(footnote)
        )
        
        summary = create_bilingual(
            "سجلات الإلحاق توفر أفضل ضمانات",
            "Append-only logs provide best guarantees",
            color_ar=C.SUCCESS,
            scale_ar=F.SIZE_HEADING,
            scale_en=F.SIZE_BODY
        )
        
        self.play(FadeIn(summary, scale=0.8))
        
        # Add final checkmark
        check = SuccessCheckmark(scale_factor=1.0)
        check.next_to(summary, DOWN, buff=L.SPACING_LG)
        
        self.play(check.animate_appear())
        self.wait_absorb(2)
    
    def create_cell(
        self, 
        text: str, 
        is_header: bool = False,
        is_success: bool = False,
        is_error: bool = False
    ) -> VGroup:
        """Create a styled table cell"""
        
        # Determine colors
        if is_header:
            text_color = C.TEXT_PRIMARY
            bg_color = C.BACKGROUND_ALT
        elif is_success:
            text_color = C.SUCCESS
            bg_color = C.SUCCESS
        elif is_error:
            text_color = C.ERROR
            bg_color = C.ERROR
        else:
            text_color = C.TEXT_PRIMARY
            bg_color = C.TEXT_TERTIARY
        
        # Cell background
        cell_bg = Rectangle(
            width=2.0,
            height=0.8,
            fill_color=bg_color,
            fill_opacity=0.1 if not is_header else 0.2,
            stroke_color=C.TEXT_TERTIARY,
            stroke_width=1
        )
        
        # Cell text
        cell_text = Text(
            text,
            font=F.CODE if not is_header else F.BODY,
            color=text_color
        ).scale(F.SIZE_CAPTION if is_header else F.SIZE_CODE)
        
        cell_text.move_to(cell_bg)
        
        return VGroup(cell_bg, cell_text)
