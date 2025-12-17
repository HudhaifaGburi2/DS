"""
Scene 6: Complete Flow & Chapter Summary
=========================================

Provides a complete overview of Chapter 1:
- The journey from simple files to databases
- Key concepts learned
- What's coming next

Two versions:
- Scene6_CompleteFlow: Detailed journey recap
- CompleteChapter: Quick visual summary
"""

import sys
sys.path.insert(0, '..')

from manim import *
from config import config, C, T, F, L, A, D
from base_scenes import DatabaseScene
from components.diagrams import ConceptBox
from components.effects import SuccessCheckmark
from utils.text_helpers import create_bilingual, create_bullet_list


class Scene6_CompleteFlow(DatabaseScene):
    """
    Chapter 1, Section 6: The Complete Journey
    
    A reflective scene that ties together everything learned.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # ACT 1: CHAPTER TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        # Big chapter title
        chapter_title = create_bilingual(
            "الرحلة الكاملة",
            "The Complete Journey",
            scale_ar=F.SIZE_HERO,
            scale_en=F.SIZE_SUBTITLE
        )
        
        self.play(FadeIn(chapter_title, scale=0.8))
        self.wait_absorb()
        
        self.play(
            chapter_title.animate.scale(0.6).to_edge(UP, buff=L.MARGIN_MD)
        )
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 2: THE PROBLEM
        # ══════════════════════════════════════════════════════════════════════
        
        problem_title = create_bilingual(
            "المشكلة",
            "The Problem",
            color_ar=C.ERROR,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        problem_title.shift(UP * 2)
        
        self.play(Write(problem_title))
        
        problem_text = create_bilingual(
            "كيف نحفظ بيانات بشكل دائم وذري؟",
            "How to save data durably and atomically?",
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        problem_text.next_to(problem_title, DOWN, buff=L.SPACING_MD)
        
        self.play(FadeIn(problem_text, shift=UP * 0.2))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 3: CHALLENGES DISCOVERED
        # ══════════════════════════════════════════════════════════════════════
        
        # Move problem up
        self.play(
            VGroup(problem_title, problem_text).animate.shift(UP * 0.5)
        )
        
        challenges_title = create_bilingual(
            "التحديات المكتشفة",
            "Challenges Discovered",
            color_ar=C.WARNING,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        challenges_title.shift(UP * 0.5)
        
        self.play(Write(challenges_title))
        
        # List of challenges
        challenges = [
            "تحديثات في نفس المكان خطيرة",
            "fsync ضروري لكن بطيء",
            "الدلائل تحتاج fsync أيضاً",
            "نحتاج طريقة للتحديثات التدريجية",
        ]
        
        challenge_items = VGroup()
        for i, challenge in enumerate(challenges):
            item = Text(f"• {challenge}", font=F.ARABIC, color=C.TEXT_PRIMARY)
            item.scale(F.SIZE_CAPTION)
            challenge_items.add(item)
        
        challenge_items.arrange(DOWN, aligned_edge=RIGHT, buff=L.SPACING_SM)
        challenge_items.next_to(challenges_title, DOWN, buff=L.SPACING_MD)
        
        self.play(
            LaggedStart(
                *[FadeIn(item, shift=LEFT * 0.2) for item in challenge_items],
                lag_ratio=0.2
            )
        )
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 4: SOLUTIONS LEARNED
        # ══════════════════════════════════════════════════════════════════════
        
        # Clear challenges
        self.play(
            FadeOut(problem_title),
            FadeOut(problem_text),
            FadeOut(challenges_title),
            FadeOut(challenge_items)
        )
        
        solutions_title = create_bilingual(
            "الحلول المكتسبة",
            "Solutions Learned",
            color_ar=C.SUCCESS,
            scale_ar=F.SIZE_HEADING,
            scale_en=F.SIZE_BODY
        )
        solutions_title.shift(UP * 2)
        
        self.play(Write(solutions_title))
        
        # Three solution boxes
        solutions = [
            ("1. إعادة التسمية\nالذرية", "Atomic\nRename", C.PRIMARY_YELLOW),
            ("2. fsync\nللديمومة", "fsync for\nDurability", C.PRIMARY_BLUE),
            ("3. سجلات\nالإلحاق", "Append-Only\nLogs", C.SUCCESS),
        ]
        
        solution_boxes = VGroup()
        for i, (ar, en, color) in enumerate(solutions):
            box = self.create_solution_box(ar, en, color)
            solution_boxes.add(box)
        
        solution_boxes.arrange(RIGHT, buff=L.SPACING_XL)
        solution_boxes.next_to(solutions_title, DOWN, buff=L.SPACING_LG)
        
        self.play(
            LaggedStart(
                *[FadeIn(box, scale=0.8) for box in solution_boxes],
                lag_ratio=0.2
            )
        )
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # ACT 5: WHAT'S NEXT
        # ══════════════════════════════════════════════════════════════════════
        
        next_title = create_bilingual(
            "الخطوات القادمة",
            "What's Next",
            color_ar=C.PRIMARY_PURPLE,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        next_title.to_edge(DOWN, buff=L.MARGIN_XL)
        
        self.play(Write(next_title))
        
        next_items = create_bilingual(
            "الفهرسة + التزامن + المعاملات",
            "Indexing + Concurrency + Transactions",
            color_ar=C.TEXT_SECONDARY,
            scale_ar=F.SIZE_CAPTION,
            scale_en=F.SIZE_LABEL
        )
        next_items.next_to(next_title, UP, buff=L.SPACING_SM)
        
        self.play(FadeIn(next_items, shift=DOWN * 0.2))
        
        self.dramatic_pause()
    
    def create_solution_box(self, text_ar: str, text_en: str, color) -> VGroup:
        """Create a solution summary box"""
        box = Rectangle(
            width=3,
            height=2,
            color=color,
            fill_opacity=0.1,
            stroke_width=2
        )
        
        ar = Text(text_ar, font=F.ARABIC, color=color).scale(F.SIZE_CAPTION)
        en = Text(text_en, font=F.BODY, color=C.TEXT_SECONDARY).scale(F.SIZE_LABEL)
        
        content = VGroup(ar, en).arrange(DOWN, buff=L.SPACING_SM)
        content.move_to(box)
        
        return VGroup(box, content)


class CompleteChapter(DatabaseScene):
    """
    Quick visual summary of Chapter 1.
    Shows the three main concepts with evolution arrows.
    """
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # MAIN TITLE
        # ══════════════════════════════════════════════════════════════════════
        
        main_title = create_bilingual(
            "من الملفات إلى قواعد البيانات",
            "From Files to Databases",
            scale_ar=F.SIZE_HERO,
            scale_en=F.SIZE_SUBTITLE
        )
        
        self.play(FadeIn(main_title, scale=0.8))
        self.wait_absorb()
        
        self.play(main_title.animate.scale(0.5).to_edge(UP, buff=L.MARGIN_MD))
        
        # ══════════════════════════════════════════════════════════════════════
        # THREE CONCEPTS
        # ══════════════════════════════════════════════════════════════════════
        
        # Concept boxes
        concept1 = ConceptBox(
            title="1. In-Place\nUpdates",
            color=C.ERROR,
            icon="❌"
        )
        concept1.shift(LEFT * 4)
        
        concept2 = ConceptBox(
            title="2. Atomic\nRename",
            color=C.WARNING,
            icon="🔄"
        )
        
        concept3 = ConceptBox(
            title="3. Append-Only\nLogs",
            color=C.SUCCESS,
            icon="✅"
        )
        concept3.shift(RIGHT * 4)
        
        concepts = VGroup(concept1, concept2, concept3)
        
        # Animate concepts appearing
        self.play(
            LaggedStart(
                concept1.animate_appear(),
                concept2.animate_appear(),
                concept3.animate_appear(),
                lag_ratio=0.3
            )
        )
        self.wait_beat()
        
        # Evolution arrows
        arrow1 = Arrow(
            concept1.get_right() + RIGHT * 0.1,
            concept2.get_left() + LEFT * 0.1,
            color=C.TEXT_SECONDARY,
            stroke_width=2
        )
        arrow2 = Arrow(
            concept2.get_right() + RIGHT * 0.1,
            concept3.get_left() + LEFT * 0.1,
            color=C.TEXT_SECONDARY,
            stroke_width=2
        )
        
        self.play(Create(arrow1), Create(arrow2))
        self.wait_absorb()
        
        # ══════════════════════════════════════════════════════════════════════
        # FINAL MESSAGE
        # ══════════════════════════════════════════════════════════════════════
        
        # Highlight the winner
        winner_highlight = SurroundingRectangle(
            concept3,
            color=C.SUCCESS,
            buff=0.2,
            corner_radius=0.15,
            stroke_width=3
        )
        
        self.play(Create(winner_highlight))
        
        # Final message
        final_msg = create_bilingual(
            "الأساس لبناء قواعد البيانات القوية",
            "The foundation for building robust databases",
            color_ar=C.SUCCESS,
            scale_ar=F.SIZE_BODY,
            scale_en=F.SIZE_CAPTION
        )
        final_msg.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(Write(final_msg))
        
        # Success checkmark
        check = SuccessCheckmark(scale_factor=1.0)
        check.next_to(final_msg, RIGHT, buff=L.SPACING_MD)
        
        self.play(check.animate_appear())
        
        self.dramatic_pause()
