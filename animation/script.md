"""
Manim Animation Script for Chapter 1: From Files to Databases
============================================================

This script creates educational animations explaining database concepts
using the Manim Community library.

Installation:
pip install manim

Usage:
manim -pql this_file.py Scene1_InPlaceUpdate
manim -pql this_file.py Scene2_AtomicRename
manim -pql this_file.py Scene3_AppendOnlyLog
manim -pql this_file.py CompleteChapter
"""

from manim import *

class Scene1_InPlaceUpdate(Scene):
    """
    Animation showing the problem with in-place file updates
    Demonstrates data loss during crash scenarios
    """
    def construct(self):
        # Title
        title = Text("1.1 التحديث في نفس المكان", font="Arial").scale(0.8)
        subtitle = Text("In-Place File Updates", font="Arial", color=GRAY).scale(0.5)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        title_group.to_edge(UP)
        self.play(Write(title_group))
        self.wait()

        # Show file representation
        file_box = Rectangle(width=3, height=2, color=BLUE)
        file_label = Text("data.txt", font="Arial").scale(0.5).next_to(file_box, UP)
        old_data = Text("Old Data\n(1024 bytes)", font="Arial", color=WHITE).scale(0.4)
        old_data.move_to(file_box.get_center())
        
        file_group = VGroup(file_box, file_label, old_data)
        file_group.shift(LEFT * 3)
        
        self.play(Create(file_box), Write(file_label), Write(old_data))
        self.wait()

        # Show new data coming
        new_data_box = Rectangle(width=2, height=1.5, color=GREEN)
        new_data_text = Text("New Data\n(2048 bytes)", font="Arial", color=WHITE).scale(0.4)
        new_data_text.move_to(new_data_box.get_center())
        new_data_group = VGroup(new_data_box, new_data_text)
        new_data_group.shift(RIGHT * 3)
        
        self.play(Create(new_data_box), Write(new_data_text))
        self.wait()

        # Show O_TRUNC flag
        trunc_label = Text("O_TRUNC", font="Arial", color=RED).scale(0.6)
        trunc_label.next_to(file_box, DOWN, buff=0.5)
        self.play(Write(trunc_label))
        
        # Truncate animation - file becomes empty
        empty_text = Text("EMPTY!", font="Arial", color=RED).scale(0.5)
        empty_text.move_to(file_box.get_center())
        self.play(
            FadeOut(old_data),
            file_box.animate.set_color(RED),
            Write(empty_text)
        )
        self.wait()

        # Show crash symbol
        crash_icon = Text("💥", font="Arial").scale(2)
        crash_icon.move_to(ORIGIN)
        crash_text = Text("CRASH!", font="Arial", color=RED).scale(0.8)
        crash_text.next_to(crash_icon, DOWN)
        
        self.play(
            FadeIn(crash_icon, scale=0.5),
            Write(crash_text)
        )
        self.wait()

        # Show result: lost data
        result_text = Text("نتيجة: بيانات مفقودة!", font="Arial", color=RED).scale(0.7)
        result_text2 = Text("Result: Data Lost!", font="Arial", color=RED).scale(0.5)
        result_group = VGroup(result_text, result_text2).arrange(DOWN, buff=0.2)
        result_group.to_edge(DOWN)
        
        self.play(Write(result_group))
        self.wait(2)


class Scene2_AtomicRename(Scene):
    """
    Animation showing atomic file rename operation
    Demonstrates the safety of rename-based updates
    """
    def construct(self):
        # Title
        title = Text("1.2 إعادة التسمية الذرية", font="Arial").scale(0.8)
        subtitle = Text("Atomic Rename", font="Arial", color=GRAY).scale(0.5)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        title_group.to_edge(UP)
        self.play(Write(title_group))
        self.wait()

        # Step 1: Original file
        original_file = self.create_file("data.txt", "Old\nData", BLUE, LEFT * 4)
        self.play(FadeIn(original_file))
        self.wait()

        # Step 2: Create temporary file
        temp_file = self.create_file("data.tmp", "New\nData", GREEN, RIGHT * 1)
        
        step1_label = Text("Step 1: إنشاء ملف مؤقت", font="Arial", color=YELLOW).scale(0.5)
        step1_label.to_edge(DOWN, buff=1)
        
        self.play(
            FadeIn(temp_file),
            Write(step1_label)
        )
        self.wait()

        # Step 2: fsync
        fsync_circle = Circle(radius=0.3, color=YELLOW)
        fsync_circle.move_to(temp_file[0].get_center())
        fsync_text = Text("fsync", font="Arial", color=YELLOW).scale(0.4)
        fsync_text.move_to(fsync_circle.get_center())
        
        step2_label = Text("Step 2: fsync للديمومة", font="Arial", color=YELLOW).scale(0.5)
        step2_label.to_edge(DOWN, buff=1)
        
        self.play(
            FadeOut(step1_label),
            Create(fsync_circle),
            Write(fsync_text),
            Write(step2_label)
        )
        self.play(
            fsync_circle.animate.scale(1.5).set_opacity(0),
            run_time=1
        )
        self.play(FadeOut(fsync_text))
        self.wait()

        # Step 3: Atomic rename
        step3_label = Text("Step 3: إعادة تسمية ذرية", font="Arial", color=YELLOW).scale(0.5)
        step3_label.to_edge(DOWN, buff=1)
        
        arrow = Arrow(temp_file.get_center(), original_file.get_center(), color=YELLOW)
        rename_text = Text("rename()", font="Arial", color=YELLOW).scale(0.5)
        rename_text.next_to(arrow, UP)
        
        self.play(
            FadeOut(step2_label),
            Create(arrow),
            Write(rename_text),
            Write(step3_label)
        )
        self.wait()

        # Perform the rename
        new_file = self.create_file("data.txt", "New\nData", GREEN, LEFT * 4)
        
        self.play(
            FadeOut(original_file),
            FadeOut(arrow),
            FadeOut(rename_text),
            temp_file.animate.move_to(original_file.get_center()),
            Transform(temp_file[1], new_file[1])
        )
        self.wait()

        # Show atomicity guarantee
        atomic_text = Text("✓ ذري للقراء والكاتب", font="Arial", color=GREEN).scale(0.6)
        atomic_text.to_edge(DOWN, buff=1)
        
        self.play(
            FadeOut(step3_label),
            Write(atomic_text)
        )
        self.wait(2)

    def create_file(self, name, content, color, position):
        """Helper function to create file representation"""
        box = Rectangle(width=2, height=1.5, color=color)
        label = Text(name, font="Arial").scale(0.4).next_to(box, UP, buff=0.1)
        data = Text(content, font="Arial").scale(0.4).move_to(box.get_center())
        file_group = VGroup(box, label, data)
        file_group.move_to(position)
        return file_group


class Scene3_AppendOnlyLog(Scene):
    """
    Animation showing append-only log with checksums
    Demonstrates how logs handle crashes safely
    """
    def construct(self):
        # Title
        title = Text("1.3 سجلات الإلحاق فقط", font="Arial").scale(0.8)
        subtitle = Text("Append-Only Logs", font="Arial", color=GRAY).scale(0.5)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        title_group.to_edge(UP)
        self.play(Write(title_group))
        self.wait()

        # Create log structure
        log_entries = []
        operations = [
            ("set a=1", GREEN, "✓"),
            ("set b=2", GREEN, "✓"),
            ("set a=3", GREEN, "✓"),
            ("del b", GREEN, "✓")
        ]

        # Draw each log entry
        for i, (op, color, check) in enumerate(operations):
            entry = self.create_log_entry(op, i, color, check)
            log_entries.append(entry)
            
            if i == 0:
                self.play(FadeIn(entry))
            else:
                self.play(entry.animate.shift(RIGHT * 0))
            self.wait(0.5)

        self.wait()

        # Show checksum structure
        checksum_title = Text("بنية الإدخال", font="Arial", color=YELLOW).scale(0.6)
        checksum_title.to_edge(DOWN, buff=2)
        
        # Detailed entry structure
        header_box = Rectangle(width=1.5, height=0.6, color=BLUE)
        header_box.shift(DOWN * 2 + LEFT * 2)
        header_text = Text("Header\nSize+Hash", font="Arial").scale(0.3)
        header_text.move_to(header_box.get_center())
        
        data_box = Rectangle(width=2, height=0.6, color=GREEN)
        data_box.next_to(header_box, RIGHT, buff=0)
        data_text = Text("Data\nset a=1", font="Arial").scale(0.3)
        data_text.move_to(data_box.get_center())
        
        entry_structure = VGroup(header_box, header_text, data_box, data_text)
        
        self.play(
            Write(checksum_title),
            Create(entry_structure)
        )
        self.wait()

        # Show crash scenario
        self.play(FadeOut(entry_structure), FadeOut(checksum_title))
        
        # Add corrupted entry
        corrupted_entry = self.create_log_entry("set c=???", 4, RED, "✗")
        self.play(FadeIn(corrupted_entry))
        
        crash_text = Text("💥 Crash!", font="Arial", color=RED).scale(0.8)
        crash_text.next_to(corrupted_entry, DOWN)
        self.play(Write(crash_text))
        self.wait()

        # Show recovery
        recovery_text = Text("الاسترداد: فحص الإدخال الأخير", font="Arial", color=YELLOW).scale(0.5)
        recovery_text.to_edge(DOWN, buff=1)
        self.play(Write(recovery_text))
        
        # Highlight corrupted entry
        highlight = SurroundingRectangle(corrupted_entry, color=YELLOW, buff=0.1)
        self.play(Create(highlight))
        self.wait()

        # Discard corrupted entry
        discard_text = Text("تجاهل الإدخال الفاسد", font="Arial", color=GREEN).scale(0.5)
        discard_text.to_edge(DOWN, buff=1)
        
        self.play(
            FadeOut(recovery_text),
            Write(discard_text)
        )
        self.play(
            FadeOut(corrupted_entry),
            FadeOut(crash_text),
            FadeOut(highlight)
        )
        self.wait()

        # Show final state
        final_text = Text("الحالة النهائية: a=3", font="Arial", color=GREEN).scale(0.7)
        final_text.to_edge(DOWN, buff=1)
        
        self.play(
            FadeOut(discard_text),
            Write(final_text)
        )
        self.wait(2)

    def create_log_entry(self, text, index, color, checkmark):
        """Helper function to create log entry"""
        box = Rectangle(width=1.8, height=0.8, color=color)
        box.shift(LEFT * 4 + RIGHT * index * 2)
        
        entry_text = Text(text, font="Arial").scale(0.35)
        entry_text.move_to(box.get_center())
        
        check = Text(checkmark, font="Arial", color=color).scale(0.5)
        check.next_to(box, DOWN, buff=0.1)
        
        index_text = Text(str(index), font="Arial", color=GRAY).scale(0.4)
        index_text.next_to(box, UP, buff=0.1)
        
        return VGroup(box, entry_text, check, index_text)


class Scene4_FSyncDiagram(Scene):
    """
    Animation showing fsync operation and buffering layers
    Demonstrates why fsync is necessary
    """
    def construct(self):
        # Title
        title = Text("fsync: ضمان الديمومة", font="Arial").scale(0.8)
        subtitle = Text("Ensuring Durability", font="Arial", color=GRAY).scale(0.5)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        title_group.to_edge(UP)
        self.play(Write(title_group))
        self.wait()

        # Create layers
        app_layer = self.create_layer("Application", BLUE, UP * 2)
        os_cache_layer = self.create_layer("OS Page Cache", YELLOW, UP * 0.5)
        device_ram_layer = self.create_layer("Device RAM", ORANGE, DOWN * 1)
        disk_layer = self.create_layer("Disk Storage", GREEN, DOWN * 2.5)

        layers = VGroup(app_layer, os_cache_layer, device_ram_layer, disk_layer)
        
        self.play(FadeIn(layers))
        self.wait()

        # Show data flow without fsync
        write_label = Text("Write() بدون fsync", font="Arial", color=RED).scale(0.5)
        write_label.to_edge(LEFT)
        self.play(Write(write_label))

        # Data stops at OS cache
        data_dot = Dot(color=RED)
        data_dot.move_to(app_layer[0].get_bottom())
        
        self.play(Create(data_dot))
        self.play(data_dot.animate.move_to(os_cache_layer[0].get_center()))
        self.wait()

        crash_icon = Text("💥", font="Arial").scale(1.5)
        crash_icon.next_to(os_cache_layer, RIGHT)
        self.play(FadeIn(crash_icon))
        self.play(FadeOut(data_dot), crash_icon.animate.scale(2).set_opacity(0))
        self.wait()

        # Clear and show with fsync
        self.play(FadeOut(write_label), FadeOut(crash_icon))
        
        fsync_label = Text("Write() + fsync()", font="Arial", color=GREEN).scale(0.5)
        fsync_label.to_edge(LEFT)
        self.play(Write(fsync_label))

        # Data goes all the way to disk
        data_dot2 = Dot(color=GREEN)
        data_dot2.move_to(app_layer[0].get_bottom())
        
        self.play(Create(data_dot2))
        self.play(data_dot2.animate.move_to(os_cache_layer[0].get_center()))
        self.wait(0.3)
        self.play(data_dot2.animate.move_to(device_ram_layer[0].get_center()))
        self.wait(0.3)
        self.play(data_dot2.animate.move_to(disk_layer[0].get_center()))
        self.wait()

        # Show checkmark
        check = Text("✓ Durable", font="Arial", color=GREEN).scale(0.8)
        check.next_to(disk_layer, RIGHT)
        self.play(Write(check))
        self.wait(2)

    def create_layer(self, name, color, position):
        """Helper function to create storage layer"""
        box = Rectangle(width=6, height=1, color=color)
        text = Text(name, font="Arial").scale(0.5)
        text.move_to(box.get_center())
        layer = VGroup(box, text)
        layer.move_to(position)
        return layer


class Scene5_ComparisonTable(Scene):
    """
    Animation showing comparison of different approaches
    """
    def construct(self):
        # Title
        title = Text("مقارنة الطرق", font="Arial").scale(0.8)
        subtitle = Text("Comparison of Approaches", font="Arial", color=GRAY).scale(0.5)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        title_group.to_edge(UP)
        self.play(Write(title_group))
        self.wait()

        # Create table
        table_data = [
            ["Method", "Power-Loss\nAtomic", "Reader-Writer\nAtomic", "Incremental"],
            ["In-Place", "✗", "✗", "✗"],
            ["Rename", "✗*", "✓", "✗"],
            ["Append-Only\nLog", "✓", "✓", "✓"]
        ]

        table = self.create_comparison_table(table_data)
        table.scale(0.7)
        table.move_to(ORIGIN)
        
        self.play(Create(table))
        self.wait()

        # Highlight the winner
        winner_box = SurroundingRectangle(table.get_rows()[3], color=GREEN, buff=0.1)
        self.play(Create(winner_box))
        
        note = Text("* يحتاج fsync على الدليل", font="Arial", color=YELLOW).scale(0.4)
        note.to_edge(DOWN)
        self.play(Write(note))
        self.wait(3)

    def create_comparison_table(self, data):
        """Helper to create comparison table"""
        table = Table(
            data,
            include_outer_lines=True,
            line_config={"stroke_width": 2, "color": WHITE}
        )
        return table


class CompleteChapter(Scene):
    """
    Complete overview animation combining all concepts
    """
    def construct(self):
        # Main title
        main_title = Text("من الملفات إلى قواعد البيانات", font="Arial").scale(1)
        main_subtitle = Text("From Files to Databases", font="Arial", color=GRAY).scale(0.6)
        title_group = VGroup(main_title, main_subtitle).arrange(DOWN, buff=0.3)
        
        self.play(Write(title_group))
        self.wait(2)
        self.play(title_group.animate.scale(0.5).to_edge(UP))

        # Show three main concepts
        concept1 = self.create_concept_box("1. In-Place\nUpdates", RED, LEFT * 4)
        concept2 = self.create_concept_box("2. Atomic\nRename", YELLOW, ORIGIN)
        concept3 = self.create_concept_box("3. Append-Only\nLogs", GREEN, RIGHT * 4)

        concepts = VGroup(concept1, concept2, concept3)
        
        self.play(FadeIn(concepts, lag_ratio=0.3))
        self.wait()

        # Show evolution arrow
        arrow1 = Arrow(concept1.get_right(), concept2.get_left(), color=WHITE)
        arrow2 = Arrow(concept2.get_right(), concept3.get_left(), color=WHITE)
        
        self.play(Create(arrow1), Create(arrow2))
        self.wait()

        # Show final message
        final_msg = Text("الأساس لبناء قواعد البيانات القوية", font="Arial", color=GREEN).scale(0.7)
        final_msg.to_edge(DOWN, buff=1)
        
        self.play(Write(final_msg))
        self.wait(3)

    def create_concept_box(self, text, color, position):
        """Helper to create concept box"""
        box = Rectangle(width=2.5, height=2, color=color)
        label = Text(text, font="Arial").scale(0.5)
        label.move_to(box.get_center())
        concept = VGroup(box, label)
        concept.move_to(position)
        return concept


# Additional scene showing the complete flow
class Scene6_CompleteFlow(Scene):
    """
    Shows the complete flow from simple file to database
    """
    def construct(self):
        title = Text("الرحلة الكاملة", font="Arial").scale(0.9)
        subtitle = Text("The Complete Journey", font="Arial", color=GRAY).scale(0.5)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        title_group.to_edge(UP)
        self.play(Write(title_group))
        self.wait()

        # Problem
        problem = Text("المشكلة: حفظ بيانات دائمة وذرية", font="Arial", color=RED).scale(0.6)
        problem.shift(UP * 2)
        self.play(Write(problem))
        self.wait()

        # Challenges discovered
        challenges = VGroup(
            Text("• تحديثات في نفس المكان خطيرة", font="Arial").scale(0.4),
            Text("• fsync ضروري لكن معقد", font="Arial").scale(0.4),
            Text("• الدلائل تحتاج fsync أيضاً", font="Arial").scale(0.4),
            Text("• السجلات توفر تحديثات تدريجية", font="Arial").scale(0.4)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        challenges.shift(DOWN * 0.5)
        
        self.play(Write(challenges, lag_ratio=0.5))
        self.wait()

        # Next steps
        next_steps = Text("الخطوات القادمة: الفهرسة + التزامن", font="Arial", color=YELLOW).scale(0.5)
        next_steps.to_edge(DOWN)
        self.play(Write(next_steps))
        self.wait(3)