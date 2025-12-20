"""
Combined OS Concurrency: All Scenes in One Video
=================================================

Complete concurrency comparison:
1. Mutex - The basic solution
2. Fine-Grained Locks - Better parallelism
3. Optimistic Concurrency - No locks during work
4. MVCC - Multi-version for reads
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import C, T, F, L, A


class ConcurrencyComparison_AllScenes(Scene):
    """
    Complete concurrency control comparison in one video.
    """
    
    def setup(self):
        self.camera.background_color = C.BACKGROUND
    
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        # INTRO
        # ══════════════════════════════════════════════════════════════════════
        self.play_intro()
        
        # ══════════════════════════════════════════════════════════════════════
        # PART 1: THE PROBLEM
        # ══════════════════════════════════════════════════════════════════════
        self.play_problem()
        self.scene_transition()
        
        # ══════════════════════════════════════════════════════════════════════
        # PART 2: MUTEX SOLUTION
        # ══════════════════════════════════════════════════════════════════════
        self.play_mutex()
        self.scene_transition()
        
        # ══════════════════════════════════════════════════════════════════════
        # PART 3: FINE-GRAINED LOCKS
        # ══════════════════════════════════════════════════════════════════════
        self.play_fine_grained()
        self.scene_transition()
        
        # ══════════════════════════════════════════════════════════════════════
        # PART 4: OPTIMISTIC CONCURRENCY
        # ══════════════════════════════════════════════════════════════════════
        self.play_optimistic()
        self.scene_transition()
        
        # ══════════════════════════════════════════════════════════════════════
        # PART 5: MVCC
        # ══════════════════════════════════════════════════════════════════════
        self.play_mvcc()
        self.scene_transition()
        
        # ══════════════════════════════════════════════════════════════════════
        # COMPARISON TABLE
        # ══════════════════════════════════════════════════════════════════════
        self.play_comparison()
        
        # ══════════════════════════════════════════════════════════════════════
        # OUTRO
        # ══════════════════════════════════════════════════════════════════════
        self.play_outro()
    
    def scene_transition(self):
        """Standard transition"""
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.5)
        self.wait(0.3)
    
    # ══════════════════════════════════════════════════════════════════════════
    # INTRO
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_intro(self):
        """Opening title"""
        title_ar = Text("التحكم في التزامن", font="Arial", color=C.TEXT_PRIMARY).scale(0.9)
        title_en = Text("Concurrency Control", font="Arial", color=C.TEXT_SECONDARY).scale(0.5)
        subtitle = Text("4 Approaches Compared", font="Arial", color=C.TEXT_ACCENT).scale(0.4)
        
        titles = VGroup(title_ar, title_en, subtitle).arrange(DOWN, buff=0.3)
        
        self.play(FadeIn(titles, scale=0.8), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(titles), run_time=0.8)
    
    # ══════════════════════════════════════════════════════════════════════════
    # PART 1: THE PROBLEM
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_problem(self):
        """Race condition problem"""
        title = Text("1. The Problem: Race Condition", font="Arial", color=C.ERROR).scale(0.6)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Shared counter
        counter_box = RoundedRectangle(width=2, height=1, color=C.SHARED_RESOURCE, fill_opacity=0.2)
        counter_label = Text("counter = 0", font="Arial", color=WHITE).scale(0.4)
        counter_label.move_to(counter_box)
        counter = VGroup(counter_box, counter_label)
        
        self.play(FadeIn(counter))
        
        # Two threads
        t1 = RoundedRectangle(width=0.8, height=0.5, color=C.THREAD_1, fill_opacity=0.4)
        t1_label = Text("T1", font="Arial", color=C.THREAD_1).scale(0.3)
        t1_label.move_to(t1)
        thread1 = VGroup(t1, t1_label)
        thread1.shift(LEFT * 3 + UP * 1)
        
        t2 = RoundedRectangle(width=0.8, height=0.5, color=C.THREAD_2, fill_opacity=0.4)
        t2_label = Text("T2", font="Arial", color=C.THREAD_2).scale(0.3)
        t2_label.move_to(t2)
        thread2 = VGroup(t2, t2_label)
        thread2.shift(LEFT * 3 + DOWN * 1)
        
        self.play(FadeIn(thread1), FadeIn(thread2))
        
        # Both read 0
        self.play(
            thread1.animate.shift(RIGHT * 2),
            thread2.animate.shift(RIGHT * 2)
        )
        
        read_t1 = Text("reads 0", font="Arial", color=C.THREAD_1).scale(0.25)
        read_t1.next_to(thread1, RIGHT, buff=0.1)
        read_t2 = Text("reads 0", font="Arial", color=C.THREAD_2).scale(0.25)
        read_t2.next_to(thread2, RIGHT, buff=0.1)
        
        self.play(Write(read_t1), Write(read_t2))
        self.wait(0.5)
        
        # Both write 1
        self.play(
            thread1.animate.shift(RIGHT * 2),
            thread2.animate.shift(RIGHT * 2)
        )
        
        # Update counter to 1 (lost update!)
        new_label = Text("counter = 1", font="Arial", color=C.ERROR).scale(0.4)
        new_label.move_to(counter_box)
        
        self.play(Transform(counter_label, new_label))
        
        # Expected vs Actual
        expected = Text("Expected: 2", font="Arial", color=C.SUCCESS).scale(0.35)
        actual = Text("Actual: 1 ✗", font="Arial", color=C.ERROR).scale(0.35)
        results = VGroup(expected, actual).arrange(DOWN, buff=0.2)
        results.to_edge(DOWN, buff=0.8)
        
        self.play(Write(expected), Write(actual))
        self.play(Flash(counter_box, color=C.ERROR, line_length=0.3))
        self.wait(1)
    
    # ══════════════════════════════════════════════════════════════════════════
    # PART 2: MUTEX
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_mutex(self):
        """Mutex solution"""
        title = Text("2. Solution: Mutex Lock", font="Arial", color=C.LOCK_HELD).scale(0.6)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Lock
        lock = Circle(radius=0.4, color=C.LOCK_FREE, fill_opacity=0.3)
        lock_icon = Text("🔓", font="Arial").scale(0.4)
        lock_icon.move_to(lock)
        lock_group = VGroup(lock, lock_icon)
        lock_group.shift(LEFT * 2)
        
        # Counter
        counter = RoundedRectangle(width=1.5, height=0.8, color=C.SHARED_RESOURCE, fill_opacity=0.2)
        counter_val = Text("0", font="Arial", color=WHITE).scale(0.4)
        counter_val.move_to(counter)
        counter_group = VGroup(counter, counter_val)
        counter_group.shift(RIGHT * 2)
        
        self.play(FadeIn(lock_group), FadeIn(counter_group))
        
        # T1 acquires lock
        t1 = RoundedRectangle(width=0.6, height=0.4, color=C.THREAD_1, fill_opacity=0.5)
        t1.shift(LEFT * 4)
        self.play(FadeIn(t1))
        
        self.play(t1.animate.move_to(lock.get_center() + LEFT * 0.8))
        
        # Lock acquired
        new_icon = Text("🔒", font="Arial").scale(0.4)
        new_icon.move_to(lock)
        self.play(
            lock.animate.set_color(C.LOCK_HELD),
            Transform(lock_icon, new_icon)
        )
        
        # T1 increments
        self.play(t1.animate.move_to(counter.get_center() + LEFT * 1))
        new_val = Text("1", font="Arial", color=WHITE).scale(0.4)
        new_val.move_to(counter)
        self.play(Transform(counter_val, new_val))
        
        # T1 releases
        self.play(t1.animate.shift(RIGHT * 2))
        unlock_icon = Text("🔓", font="Arial").scale(0.4)
        unlock_icon.move_to(lock)
        self.play(
            lock.animate.set_color(C.LOCK_FREE),
            Transform(lock_icon, unlock_icon)
        )
        
        # T2's turn
        t2 = RoundedRectangle(width=0.6, height=0.4, color=C.THREAD_2, fill_opacity=0.5)
        t2.shift(LEFT * 4 + DOWN * 0.5)
        self.play(FadeIn(t2))
        
        self.play(t2.animate.move_to(lock.get_center() + LEFT * 0.8))
        
        relock = Text("🔒", font="Arial").scale(0.4)
        relock.move_to(lock)
        self.play(
            lock.animate.set_color(C.LOCK_HELD),
            Transform(lock_icon, relock)
        )
        
        self.play(t2.animate.move_to(counter.get_center() + LEFT * 1))
        final_val = Text("2", font="Arial", color=C.SUCCESS).scale(0.4)
        final_val.move_to(counter)
        self.play(Transform(counter_val, final_val))
        
        # Success
        success = Text("counter = 2 ✓", font="Arial", color=C.SUCCESS).scale(0.4)
        success.to_edge(DOWN, buff=0.8)
        self.play(Write(success))
        self.wait(1)
    
    # ══════════════════════════════════════════════════════════════════════════
    # PART 3: FINE-GRAINED LOCKS
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_fine_grained(self):
        """Fine-grained locking"""
        title = Text("3. Better: Fine-Grained Locks", font="Arial", color=C.SUCCESS).scale(0.6)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Multiple data cells with individual locks
        cells = VGroup()
        for i in range(4):
            cell = Square(side_length=0.8, color=C.SHARED_RESOURCE, fill_opacity=0.2)
            lock = Circle(radius=0.15, color=C.LOCK_FREE, fill_opacity=0.3)
            lock.next_to(cell, UP, buff=0.1)
            label = Text(f"D{i}", font="Arial", color=WHITE).scale(0.25)
            label.move_to(cell)
            cells.add(VGroup(cell, lock, label))
        
        cells.arrange(RIGHT, buff=0.5)
        self.play(FadeIn(cells))
        
        # Two threads access DIFFERENT cells (parallel!)
        t1 = RoundedRectangle(width=0.5, height=0.35, color=C.THREAD_1, fill_opacity=0.5)
        t2 = RoundedRectangle(width=0.5, height=0.35, color=C.THREAD_2, fill_opacity=0.5)
        
        t1.move_to(cells[0][0].get_center() + UP * 1.2)
        t2.move_to(cells[3][0].get_center() + UP * 1.2)
        
        self.play(FadeIn(t1), FadeIn(t2))
        
        # Both lock their own cells
        self.play(
            cells[0][1].animate.set_color(C.THREAD_1),
            cells[3][1].animate.set_color(C.THREAD_2)
        )
        
        # Both work in parallel
        self.play(
            t1.animate.move_to(cells[0][0].get_center()),
            t2.animate.move_to(cells[3][0].get_center())
        )
        
        parallel = Text("PARALLEL! No blocking!", font="Arial", color=C.SUCCESS).scale(0.4)
        parallel.to_edge(DOWN, buff=0.8)
        self.play(Write(parallel))
        self.wait(1)
    
    # ══════════════════════════════════════════════════════════════════════════
    # PART 4: OPTIMISTIC CONCURRENCY
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_optimistic(self):
        """Optimistic concurrency control"""
        title = Text("4. Optimistic: No Locks During Work", font="Arial", color=C.INFO).scale(0.6)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Three phases
        phases = VGroup(
            self._make_phase_box("READ", "Read data", C.INFO),
            self._make_phase_box("WORK", "Compute locally", C.WARNING),
            self._make_phase_box("VALIDATE", "Check conflicts", C.SUCCESS),
        )
        phases.arrange(RIGHT, buff=0.8)
        phases.shift(UP * 0.5)
        
        # Arrows
        arrow1 = Arrow(phases[0].get_right(), phases[1].get_left(), color=C.TEXT_TERTIARY, stroke_width=2)
        arrow2 = Arrow(phases[1].get_right(), phases[2].get_left(), color=C.TEXT_TERTIARY, stroke_width=2)
        
        self.play(
            LaggedStart(
                FadeIn(phases[0]), Create(arrow1),
                FadeIn(phases[1]), Create(arrow2),
                FadeIn(phases[2]),
                lag_ratio=0.3
            )
        )
        
        # Key point
        key = Text("No locks until validation!", font="Arial", color=C.SUCCESS).scale(0.4)
        key.to_edge(DOWN, buff=1)
        
        conflict = Text("If conflict → Rollback & Retry", font="Arial", color=C.WARNING).scale(0.35)
        conflict.next_to(key, DOWN, buff=0.2)
        
        self.play(Write(key))
        self.play(Write(conflict))
        self.wait(1)
    
    def _make_phase_box(self, title, desc, color):
        box = RoundedRectangle(width=2.2, height=1.4, color=color, fill_opacity=0.15, corner_radius=0.1)
        title_text = Text(title, font="Arial", color=color).scale(0.35)
        title_text.next_to(box.get_top(), DOWN, buff=0.15)
        desc_text = Text(desc, font="Arial", color=C.TEXT_SECONDARY).scale(0.25)
        desc_text.move_to(box.get_center() + DOWN * 0.15)
        return VGroup(box, title_text, desc_text)
    
    # ══════════════════════════════════════════════════════════════════════════
    # PART 5: MVCC
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_mvcc(self):
        """Multi-Version Concurrency Control"""
        title = Text("5. MVCC: Multiple Versions", font="Arial", color=C.VERSION_CURRENT).scale(0.6)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Version chain
        versions = VGroup()
        labels = ["v1", "v2", "v3"]
        colors = [C.VERSION_OLD, C.VERSION_OLD, C.VERSION_CURRENT]
        opacities = [0.2, 0.3, 0.5]
        
        for i, (label, color, opacity) in enumerate(zip(labels, colors, opacities)):
            box = RoundedRectangle(width=1, height=0.7, color=color, fill_opacity=opacity, corner_radius=0.08)
            text = Text(label, font="Arial", color=color).scale(0.3)
            text.move_to(box)
            versions.add(VGroup(box, text))
        
        versions.arrange(RIGHT, buff=0.4)
        
        # Arrows between versions
        arrows = VGroup()
        for i in range(len(versions) - 1):
            arrow = Arrow(
                versions[i].get_right(), versions[i+1].get_left(),
                color=C.TEXT_TERTIARY, stroke_width=1.5, buff=0.1
            )
            arrows.add(arrow)
        
        version_group = VGroup(versions, arrows)
        
        self.play(FadeIn(version_group))
        
        # Reader and Writer
        reader = Text("Reader → sees v2", font="Arial", color=C.SNAPSHOT).scale(0.35)
        reader.shift(UP * 1.5 + LEFT * 1)
        
        writer = Text("Writer → creates v4", font="Arial", color=C.VERSION_NEW).scale(0.35)
        writer.shift(DOWN * 1.5 + RIGHT * 1)
        
        self.play(Write(reader), Write(writer))
        
        # Key benefit
        benefit = Text("Readers NEVER block Writers!", font="Arial", color=C.SUCCESS).scale(0.4)
        benefit.to_edge(DOWN, buff=0.8)
        self.play(Write(benefit))
        self.wait(1)
    
    # ══════════════════════════════════════════════════════════════════════════
    # COMPARISON
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_comparison(self):
        """Final comparison table"""
        title = Text("Comparison: Which to Use?", font="Arial", color=C.TEXT_ACCENT).scale(0.6)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Comparison data
        methods = ["Mutex", "Fine-Grained", "Optimistic", "MVCC"]
        colors = [C.LOCK_HELD, C.SUCCESS, C.INFO, C.VERSION_CURRENT]
        
        read_perf = ["Medium", "Good", "Best", "Best"]
        write_perf = ["Medium", "Good", "Variable", "Good"]
        complexity = ["Simple", "Medium", "Medium", "Complex"]
        use_case = ["General", "Partitioned", "Low conflict", "Read-heavy"]
        
        # Create table
        table = VGroup()
        
        # Header row
        headers = VGroup(
            Text("Method", font="Arial", color=C.TEXT_TERTIARY).scale(0.3),
            Text("Reads", font="Arial", color=C.TEXT_TERTIARY).scale(0.3),
            Text("Writes", font="Arial", color=C.TEXT_TERTIARY).scale(0.3),
            Text("Complexity", font="Arial", color=C.TEXT_TERTIARY).scale(0.3),
            Text("Best For", font="Arial", color=C.TEXT_TERTIARY).scale(0.3),
        )
        headers.arrange(RIGHT, buff=0.8)
        headers.shift(UP * 1.5)
        table.add(headers)
        
        # Data rows
        for i, (method, color) in enumerate(zip(methods, colors)):
            row = VGroup(
                Text(method, font="Arial", color=color).scale(0.28),
                Text(read_perf[i], font="Arial", color=C.TEXT_SECONDARY).scale(0.25),
                Text(write_perf[i], font="Arial", color=C.TEXT_SECONDARY).scale(0.25),
                Text(complexity[i], font="Arial", color=C.TEXT_SECONDARY).scale(0.25),
                Text(use_case[i], font="Arial", color=C.TEXT_SECONDARY).scale(0.25),
            )
            row.arrange(RIGHT, buff=0.8)
            row.shift(UP * (0.8 - i * 0.6))
            table.add(row)
        
        self.play(
            LaggedStart(*[FadeIn(row) for row in table], lag_ratio=0.2)
        )
        
        # Conclusion
        conclusion = Text(
            "Choose based on YOUR workload!",
            font="Arial",
            color=C.TEXT_ACCENT
        ).scale(0.45)
        conclusion.to_edge(DOWN, buff=0.6)
        
        self.play(FadeIn(conclusion, scale=0.8))
        self.wait(2)
    
    # ══════════════════════════════════════════════════════════════════════════
    # OUTRO
    # ══════════════════════════════════════════════════════════════════════════
    
    def play_outro(self):
        """Closing"""
        self.scene_transition()
        
        title = Text("Concurrency Control", font="Arial", color=C.TEXT_PRIMARY).scale(0.7)
        subtitle = Text("4 Approaches Compared", font="Arial", color=C.TEXT_SECONDARY).scale(0.4)
        
        methods = VGroup(
            Text("1. Mutex - Simple & Safe", font="Arial", color=C.LOCK_HELD).scale(0.3),
            Text("2. Fine-Grained - Better Parallelism", font="Arial", color=C.SUCCESS).scale(0.3),
            Text("3. Optimistic - Low Conflict", font="Arial", color=C.INFO).scale(0.3),
            Text("4. MVCC - Read-Heavy", font="Arial", color=C.VERSION_CURRENT).scale(0.3),
        )
        methods.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        
        outro = VGroup(title, subtitle, methods).arrange(DOWN, buff=0.4)
        
        self.play(FadeIn(outro, scale=0.8))
        self.wait(3)
        self.play(FadeOut(outro))
