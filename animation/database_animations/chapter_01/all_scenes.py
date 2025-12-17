"""
Combined Chapter 01: All Scenes in One Video
=============================================

Renders all Chapter 01 scenes sequentially into a single animation.
"""

from manim import *
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import config, C, T, F, L, A, D


class Chapter01_AllScenes(Scene):
    """
    Complete Chapter 01 animation combining all scenes.
    Plays all sections in order with transitions.
    """
    
    def setup(self):
        self.camera.background_color = C.BACKGROUND
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # CHAPTER INTRO
        # ══════════════════════════════════════════════════════════════════════
        self.play_chapter_intro()
        
        # ══════════════════════════════════════════════════════════════════════
        # SCENE 1: IN-PLACE UPDATES
        # ══════════════════════════════════════════════════════════════════════
        self.play_scene_1_inplace()
        self.scene_transition()
        
        # ══════════════════════════════════════════════════════════════════════
        # SCENE 2: ATOMIC RENAME
        # ══════════════════════════════════════════════════════════════════════
        self.play_scene_2_rename()
        self.scene_transition()
        
        # ══════════════════════════════════════════════════════════════════════
        # SCENE 3: APPEND-ONLY LOGS
        # ══════════════════════════════════════════════════════════════════════
        self.play_scene_3_logs()
        self.scene_transition()
        
        # ══════════════════════════════════════════════════════════════════════
        # SCENE 4: FSYNC
        # ══════════════════════════════════════════════════════════════════════
        self.play_scene_4_fsync()
        self.scene_transition()
        
        # ══════════════════════════════════════════════════════════════════════
        # SCENE 5: COMPARISON
        # ══════════════════════════════════════════════════════════════════════
        self.play_scene_5_comparison()
        self.scene_transition()
        
        # ══════════════════════════════════════════════════════════════════════
        # SCENE 6: COMPLETE SUMMARY
        # ══════════════════════════════════════════════════════════════════════
        self.play_scene_6_complete()
        
        # ══════════════════════════════════════════════════════════════════════
        # CHAPTER OUTRO
        # ══════════════════════════════════════════════════════════════════════
        self.play_chapter_outro()
    
    def scene_transition(self):
        """Fade out all and brief pause"""
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.5)
        self.wait(0.3)
    
    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER INTRO
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_chapter_intro(self):
        """Chapter opening title"""
        chapter_num = Text("الفصل الأول", font="Arial", color=C.TEXT_SECONDARY).scale(0.6)
        chapter_num_en = Text("Chapter 1", font="Arial", color=C.TEXT_TERTIARY).scale(0.4)
        
        main_title = Text("من الملفات إلى قواعد البيانات", font="Arial", color=C.TEXT_PRIMARY).scale(0.9)
        main_title_en = Text("From Files to Databases", font="Arial", color=C.TEXT_SECONDARY).scale(0.5)
        
        title_group = VGroup(chapter_num, chapter_num_en, main_title, main_title_en)
        title_group.arrange(DOWN, buff=0.3)
        
        self.play(FadeIn(title_group, scale=0.8), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(title_group), run_time=0.8)
        self.wait(0.5)
    
    # ══════════════════════════════════════════════════════════════════════════
    # SCENE 1: IN-PLACE UPDATE
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_scene_1_inplace(self):
        """In-place update dangers"""
        # Title
        title = Text("1.1 التحديث في نفس المكان", font="Arial").scale(0.7)
        subtitle = Text("In-Place File Updates", font="Arial", color=GRAY).scale(0.4)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        title_group.to_edge(UP)
        
        self.play(Write(title_group))
        self.wait(0.5)
        
        # File representation
        file_box = RoundedRectangle(width=3, height=2, color=C.FILE_ORIGINAL, corner_radius=0.15)
        file_label = Text("data.txt", font="Arial").scale(0.4).next_to(file_box, UP, buff=0.1)
        old_data = Text("Old Data\n(1024 bytes)", font="Arial", color=WHITE).scale(0.35)
        old_data.move_to(file_box.get_center())
        
        file_group = VGroup(file_box, file_label, old_data)
        file_group.shift(LEFT * 3)
        
        self.play(FadeIn(file_group))
        self.wait(0.5)
        
        # New data
        new_data_box = RoundedRectangle(width=2, height=1.5, color=C.FILE_NEW, corner_radius=0.1)
        new_data_text = Text("New Data\n(2048 bytes)", font="Arial", color=WHITE).scale(0.3)
        new_data_text.move_to(new_data_box.get_center())
        new_data_group = VGroup(new_data_box, new_data_text)
        new_data_group.shift(RIGHT * 3)
        
        self.play(FadeIn(new_data_group))
        self.wait(0.5)
        
        # O_TRUNC warning
        trunc_label = Text("O_TRUNC", font="Arial", color=C.WARNING).scale(0.5)
        trunc_label.next_to(file_box, DOWN, buff=0.4)
        self.play(Write(trunc_label))
        
        # Truncate - file becomes empty
        empty_text = Text("EMPTY!", font="Arial", color=C.ERROR).scale(0.4)
        empty_text.move_to(file_box.get_center())
        
        self.play(
            FadeOut(old_data),
            file_box.animate.set_stroke(color=C.ERROR),
            FadeIn(empty_text, scale=1.3)
        )
        self.wait(0.5)
        
        # Crash!
        crash_icon = Text("💥", font="Arial").scale(1.5)
        crash_icon.move_to(ORIGIN)
        crash_text = Text("CRASH!", font="Arial", color=C.ERROR).scale(0.6)
        crash_text.next_to(crash_icon, DOWN)
        
        self.play(FadeIn(crash_icon, scale=0.5), Write(crash_text))
        self.wait(0.8)
        
        # Result
        result_text = Text("نتيجة: بيانات مفقودة!", font="Arial", color=C.ERROR).scale(0.5)
        result_text2 = Text("Result: Data Lost!", font="Arial", color=C.ERROR).scale(0.4)
        result_group = VGroup(result_text, result_text2).arrange(DOWN, buff=0.15)
        result_group.to_edge(DOWN, buff=0.8)
        
        self.play(Write(result_group))
        self.wait(1.5)
    
    # ══════════════════════════════════════════════════════════════════════════
    # SCENE 2: ATOMIC RENAME
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_scene_2_rename(self):
        """Atomic rename solution"""
        # Title
        title = Text("1.2 إعادة التسمية الذرية", font="Arial").scale(0.7)
        subtitle = Text("Atomic Rename", font="Arial", color=GRAY).scale(0.4)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        title_group.to_edge(UP)
        
        self.play(Write(title_group))
        self.wait(0.5)
        
        # Original file
        orig_box = RoundedRectangle(width=2.5, height=1.8, color=C.FILE_ORIGINAL, corner_radius=0.12)
        orig_label = Text("data.txt", font="Arial").scale(0.35).next_to(orig_box, UP, buff=0.08)
        orig_data = Text("Old\nData", font="Arial").scale(0.35).move_to(orig_box)
        orig_file = VGroup(orig_box, orig_label, orig_data)
        orig_file.shift(LEFT * 4)
        
        self.play(FadeIn(orig_file))
        self.wait(0.3)
        
        # Step 1: Create temp file
        step1 = Text("Step 1: إنشاء ملف مؤقت", font="Arial", color=C.PRIMARY_YELLOW).scale(0.4)
        step1.to_edge(DOWN, buff=0.8)
        
        temp_box = RoundedRectangle(width=2.5, height=1.8, color=C.FILE_NEW, corner_radius=0.12)
        temp_label = Text("data.tmp", font="Arial").scale(0.35).next_to(temp_box, UP, buff=0.08)
        temp_data = Text("New\nData", font="Arial").scale(0.35).move_to(temp_box)
        temp_file = VGroup(temp_box, temp_label, temp_data)
        temp_file.shift(RIGHT * 1)
        
        self.play(Write(step1), FadeIn(temp_file))
        self.wait(0.8)
        
        # Step 2: fsync
        step2 = Text("Step 2: fsync للديمومة", font="Arial", color=C.PRIMARY_YELLOW).scale(0.4)
        step2.to_edge(DOWN, buff=0.8)
        
        fsync_circle = Circle(radius=0.25, color=C.PRIMARY_YELLOW)
        fsync_circle.move_to(temp_box.get_center())
        fsync_text = Text("fsync", font="Arial", color=C.PRIMARY_YELLOW).scale(0.3)
        fsync_text.move_to(fsync_circle)
        
        self.play(FadeOut(step1), Write(step2), Create(fsync_circle), Write(fsync_text))
        self.play(fsync_circle.animate.scale(1.5).set_opacity(0), run_time=0.8)
        self.play(FadeOut(fsync_text))
        self.wait(0.5)
        
        # Step 3: Atomic rename
        step3 = Text("Step 3: إعادة تسمية ذرية", font="Arial", color=C.PRIMARY_YELLOW).scale(0.4)
        step3.to_edge(DOWN, buff=0.8)
        
        arrow = Arrow(temp_file.get_left(), orig_file.get_right(), color=C.PRIMARY_YELLOW)
        rename_text = Text("rename()", font="Arial", color=C.PRIMARY_YELLOW).scale(0.4)
        rename_text.next_to(arrow, UP, buff=0.1)
        
        self.play(FadeOut(step2), Write(step3), Create(arrow), Write(rename_text))
        self.wait(0.5)
        
        # Perform rename
        new_label = Text("data.txt", font="Arial").scale(0.35)
        new_label.next_to(temp_box, UP, buff=0.08)
        
        self.play(
            FadeOut(orig_file),
            FadeOut(arrow),
            FadeOut(rename_text),
            temp_file.animate.move_to(orig_file.get_center()),
            Transform(temp_label, new_label)
        )
        self.wait(0.5)
        
        # Success
        temp_box.set_stroke(color=C.SUCCESS)
        success = Text("✓ ذري للقراء والكاتب", font="Arial", color=C.SUCCESS).scale(0.5)
        success.to_edge(DOWN, buff=0.8)
        
        self.play(FadeOut(step3), Write(success))
        self.wait(1.5)
    
    # ══════════════════════════════════════════════════════════════════════════
    # SCENE 3: APPEND-ONLY LOGS
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_scene_3_logs(self):
        """Append-only logs with checksums"""
        # Title
        title = Text("1.3 سجلات الإلحاق فقط", font="Arial").scale(0.7)
        subtitle = Text("Append-Only Logs", font="Arial", color=GRAY).scale(0.4)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        title_group.to_edge(UP)
        
        self.play(Write(title_group))
        self.wait(0.5)
        
        # Log entries
        operations = [
            ("set a=1", C.SUCCESS, "✓"),
            ("set b=2", C.SUCCESS, "✓"),
            ("set a=3", C.SUCCESS, "✓"),
            ("del b", C.SUCCESS, "✓")
        ]
        
        entries = VGroup()
        for i, (op, color, check) in enumerate(operations):
            box = RoundedRectangle(width=1.6, height=0.7, color=color, corner_radius=0.08)
            box.shift(LEFT * 3 + RIGHT * i * 1.8)
            
            op_text = Text(op, font="Arial").scale(0.3)
            op_text.move_to(box)
            
            check_text = Text(check, font="Arial", color=color).scale(0.35)
            check_text.next_to(box, DOWN, buff=0.08)
            
            idx_text = Text(str(i), font="Arial", color=GRAY).scale(0.3)
            idx_text.next_to(box, UP, buff=0.08)
            
            entry = VGroup(box, op_text, check_text, idx_text)
            entries.add(entry)
            
            self.play(FadeIn(entry, shift=LEFT * 0.2), run_time=0.4)
        
        self.wait(0.8)
        
        # Add corrupted entry
        corrupt_box = RoundedRectangle(width=1.6, height=0.7, color=C.ERROR, corner_radius=0.08)
        corrupt_box.shift(LEFT * 3 + RIGHT * 4 * 1.8)
        corrupt_text = Text("set c=???", font="Arial").scale(0.3)
        corrupt_text.move_to(corrupt_box)
        corrupt_check = Text("✗", font="Arial", color=C.ERROR).scale(0.35)
        corrupt_check.next_to(corrupt_box, DOWN, buff=0.08)
        corrupt_entry = VGroup(corrupt_box, corrupt_text, corrupt_check)
        
        self.play(FadeIn(corrupt_entry))
        
        crash_text = Text("💥 Crash!", font="Arial", color=C.ERROR).scale(0.5)
        crash_text.next_to(corrupt_entry, DOWN, buff=0.3)
        self.play(Write(crash_text))
        self.wait(0.5)
        
        # Recovery
        recovery_text = Text("الاسترداد: تجاهل الإدخال الفاسد", font="Arial", color=C.PRIMARY_YELLOW).scale(0.4)
        recovery_text.to_edge(DOWN, buff=0.8)
        self.play(Write(recovery_text))
        
        highlight = SurroundingRectangle(corrupt_entry, color=C.PRIMARY_YELLOW, buff=0.1)
        self.play(Create(highlight))
        self.wait(0.3)
        
        self.play(FadeOut(corrupt_entry), FadeOut(highlight), FadeOut(crash_text))
        
        # Final state
        final_text = Text("الحالة النهائية: a=3", font="Arial", color=C.SUCCESS).scale(0.5)
        final_text.to_edge(DOWN, buff=0.8)
        self.play(FadeOut(recovery_text), Write(final_text))
        self.wait(1.5)
    
    # ══════════════════════════════════════════════════════════════════════════
    # SCENE 4: FSYNC
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_scene_4_fsync(self):
        """fsync and storage layers"""
        # Title
        title = Text("fsync: ضمان الديمومة", font="Arial").scale(0.7)
        subtitle = Text("Ensuring Durability", font="Arial", color=GRAY).scale(0.4)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        title_group.to_edge(UP)
        
        self.play(Write(title_group))
        self.wait(0.5)
        
        # Storage layers
        layers = []
        layer_data = [
            ("Application", C.LAYER_APP),
            ("OS Page Cache", C.LAYER_OS),
            ("Device RAM", C.LAYER_DEVICE),
            ("Disk Storage", C.LAYER_DISK),
        ]
        
        for i, (name, color) in enumerate(layer_data):
            box = RoundedRectangle(width=5, height=0.8, color=color, corner_radius=0.1, fill_opacity=0.15)
            box.shift(UP * (1.2 - i * 1.0))
            text = Text(name, font="Arial").scale(0.4)
            text.move_to(box)
            layer = VGroup(box, text)
            layers.append(layer)
            self.play(FadeIn(layer, shift=DOWN * 0.2), run_time=0.3)
        
        self.wait(0.5)
        
        # Without fsync - data stops at cache
        no_fsync = Text("Write() بدون fsync", font="Arial", color=C.ERROR).scale(0.4)
        no_fsync.to_edge(LEFT, buff=0.5)
        self.play(Write(no_fsync))
        
        data_dot = Dot(color=C.ERROR, radius=0.1)
        data_dot.move_to(layers[0][0].get_center())
        self.play(Create(data_dot))
        self.play(data_dot.animate.move_to(layers[1][0].get_center()))
        
        stop_text = Text("STOPS!", font="Arial", color=C.ERROR).scale(0.3)
        stop_text.next_to(layers[1], RIGHT, buff=0.3)
        self.play(Write(stop_text))
        
        crash = Text("💥", font="Arial").scale(1)
        crash.next_to(stop_text, RIGHT, buff=0.2)
        self.play(FadeIn(crash, scale=0.5))
        self.play(FadeOut(data_dot), run_time=0.3)
        self.wait(0.5)
        
        self.play(FadeOut(no_fsync), FadeOut(stop_text), FadeOut(crash))
        
        # With fsync - data reaches disk
        with_fsync = Text("Write() + fsync()", font="Arial", color=C.SUCCESS).scale(0.4)
        with_fsync.to_edge(LEFT, buff=0.5)
        self.play(Write(with_fsync))
        
        data_dot2 = Dot(color=C.SUCCESS, radius=0.1)
        data_dot2.move_to(layers[0][0].get_center())
        self.play(Create(data_dot2))
        
        for i in range(1, 4):
            self.play(data_dot2.animate.move_to(layers[i][0].get_center()), run_time=0.4)
        
        durable = Text("✓ DURABLE", font="Arial", color=C.SUCCESS).scale(0.4)
        durable.next_to(layers[3], RIGHT, buff=0.3)
        self.play(Write(durable))
        self.wait(1.5)
    
    # ══════════════════════════════════════════════════════════════════════════
    # SCENE 5: COMPARISON TABLE
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_scene_5_comparison(self):
        """Comparison of approaches"""
        # Title
        title = Text("مقارنة الطرق", font="Arial").scale(0.7)
        subtitle = Text("Comparison of Approaches", font="Arial", color=GRAY).scale(0.4)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        title_group.to_edge(UP)
        
        self.play(Write(title_group))
        self.wait(0.5)
        
        # Simple comparison
        methods = [
            ("In-Place", "✗", "✗", "✗", C.ERROR),
            ("Rename", "✗*", "✓", "✗", C.WARNING),
            ("Append-Only Log", "✓", "✓", "✓", C.SUCCESS),
        ]
        
        headers = ["Method", "Power-Loss", "Reader-Writer", "Incremental"]
        
        # Create headers
        header_group = VGroup()
        for i, h in enumerate(headers):
            text = Text(h, font="Arial", color=C.TEXT_SECONDARY).scale(0.35)
            text.shift(LEFT * 3 + RIGHT * i * 2.5)
            header_group.add(text)
        header_group.shift(UP * 1.5)
        
        self.play(FadeIn(header_group))
        
        # Create rows
        for row_idx, (method, p1, p2, p3, color) in enumerate(methods):
            row_items = [method, p1, p2, p3]
            row_group = VGroup()
            
            for col_idx, item in enumerate(row_items):
                item_color = color if col_idx > 0 else C.TEXT_PRIMARY
                text = Text(item, font="Arial", color=item_color).scale(0.35)
                text.shift(LEFT * 3 + RIGHT * col_idx * 2.5)
                row_group.add(text)
            
            row_group.shift(UP * (0.5 - row_idx * 0.8))
            self.play(FadeIn(row_group, shift=LEFT * 0.2), run_time=0.4)
        
        self.wait(0.5)
        
        # Highlight winner
        winner_text = Text("✓ BEST: Append-Only Logs", font="Arial", color=C.SUCCESS).scale(0.5)
        winner_text.to_edge(DOWN, buff=0.8)
        self.play(Write(winner_text))
        self.wait(1.5)
    
    # ══════════════════════════════════════════════════════════════════════════
    # SCENE 6: COMPLETE SUMMARY
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_scene_6_complete(self):
        """Chapter summary"""
        # Title
        title = Text("من الملفات إلى قواعد البيانات", font="Arial").scale(0.8)
        subtitle = Text("From Files to Databases", font="Arial", color=GRAY).scale(0.5)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        
        self.play(FadeIn(title_group, scale=0.8))
        self.wait(1)
        self.play(title_group.animate.scale(0.5).to_edge(UP, buff=0.5))
        
        # Three concepts
        concepts = [
            ("1. In-Place\nUpdates", C.ERROR, "❌"),
            ("2. Atomic\nRename", C.WARNING, "🔄"),
            ("3. Append-Only\nLogs", C.SUCCESS, "✅"),
        ]
        
        boxes = VGroup()
        for i, (text, color, icon) in enumerate(concepts):
            box = RoundedRectangle(width=2.2, height=1.8, color=color, corner_radius=0.15, fill_opacity=0.1)
            box.shift(LEFT * 3.5 + RIGHT * i * 3.5)
            
            icon_text = Text(icon, font="Arial").scale(0.5)
            label = Text(text, font="Arial").scale(0.35)
            content = VGroup(icon_text, label).arrange(DOWN, buff=0.15)
            content.move_to(box)
            
            concept = VGroup(box, content)
            boxes.add(concept)
        
        self.play(LaggedStart(*[FadeIn(b, scale=0.8) for b in boxes], lag_ratio=0.2))
        self.wait(0.5)
        
        # Arrows
        arrow1 = Arrow(boxes[0].get_right(), boxes[1].get_left(), color=WHITE, buff=0.1)
        arrow2 = Arrow(boxes[1].get_right(), boxes[2].get_left(), color=WHITE, buff=0.1)
        self.play(Create(arrow1), Create(arrow2))
        
        # Final message
        final = Text("الأساس لبناء قواعد البيانات القوية", font="Arial", color=C.SUCCESS).scale(0.5)
        final.to_edge(DOWN, buff=0.8)
        self.play(Write(final))
        self.wait(2)
    
    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER OUTRO
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_chapter_outro(self):
        """Chapter ending"""
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)
        
        end_text = Text("نهاية الفصل الأول", font="Arial", color=C.TEXT_PRIMARY).scale(0.7)
        end_text_en = Text("End of Chapter 1", font="Arial", color=C.TEXT_SECONDARY).scale(0.4)
        
        next_text = Text("القادم: الفهرسة والتزامن", font="Arial", color=C.PRIMARY_PURPLE).scale(0.5)
        next_text_en = Text("Next: Indexing & Concurrency", font="Arial", color=C.TEXT_TERTIARY).scale(0.35)
        
        end_group = VGroup(end_text, end_text_en, next_text, next_text_en)
        end_group.arrange(DOWN, buff=0.3)
        
        self.play(FadeIn(end_group, scale=0.8))
        self.wait(3)
        self.play(FadeOut(end_group))
        self.wait(0.5)
