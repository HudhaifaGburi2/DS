"""
Lock Components
===============

Visual representations of synchronization primitives.
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import C, T, F, L, A, OS


class Mutex(VGroup):
    """
    Mutex lock visualization.
    
    States: free (green), held (red), contested (amber)
    """
    
    def __init__(
        self,
        label: str = "Mutex",
        size: float = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.lock_label = label
        self.size = size or L.LOCK_SIZE
        self.state = "free"
        self.holder = None
        self.waiters = []
        
        # Lock body (circle with keyhole)
        self.body = Circle(
            radius=self.size / 2,
            color=C.LOCK_FREE,
            fill_opacity=0.3,
            stroke_width=A.LOCK_STROKE
        )
        
        # Lock icon
        self.icon = Text(
            OS.UNLOCK_ICON,
            font=F.BODY
        ).scale(0.4)
        self.icon.move_to(self.body.get_center())
        
        # Label
        self.label = Text(
            label,
            font=F.CODE,
            color=C.TEXT_SECONDARY
        ).scale(F.SIZE_TINY)
        self.label.next_to(self.body, DOWN, buff=L.SPACING_TIGHT)
        
        self.add(self.body, self.icon, self.label)
    
    def _update_visual(self):
        """Update visual based on state"""
        if self.state == "free":
            self.body.set_color(C.LOCK_FREE)
            self.body.set_fill(opacity=0.3)
            self.icon.become(
                Text(OS.UNLOCK_ICON, font=F.BODY).scale(0.4).move_to(self.body.get_center())
            )
        elif self.state == "held":
            self.body.set_color(C.LOCK_HELD)
            self.body.set_fill(opacity=0.5)
            self.icon.become(
                Text(OS.LOCK_ICON, font=F.BODY).scale(0.4).move_to(self.body.get_center())
            )
        elif self.state == "contested":
            self.body.set_color(C.LOCK_WAITING)
            self.body.set_fill(opacity=0.5)
    
    def animate_acquire(self, thread_id: int = None):
        """Animate lock acquisition"""
        self.state = "held"
        self.holder = thread_id
        
        new_icon = Text(OS.LOCK_ICON, font=F.BODY).scale(0.4)
        new_icon.move_to(self.body.get_center())
        
        return Succession(
            self.body.animate.set_color(C.LOCK_HELD).set_fill(opacity=0.5),
            Transform(self.icon, new_icon),
            run_time=T.LOCK_ACQUIRE
        )
    
    def animate_release(self):
        """Animate lock release"""
        self.state = "free"
        self.holder = None
        
        new_icon = Text(OS.UNLOCK_ICON, font=F.BODY).scale(0.4)
        new_icon.move_to(self.body.get_center())
        
        return Succession(
            self.body.animate.set_color(C.LOCK_FREE).set_fill(opacity=0.3),
            Transform(self.icon, new_icon),
            run_time=T.LOCK_RELEASE
        )
    
    def animate_contention(self):
        """Animate contention state"""
        self.state = "contested"
        return self.body.animate.set_color(C.LOCK_WAITING)


class RWLock(VGroup):
    """
    Read-Write lock visualization.
    
    Allows multiple readers or single writer.
    """
    
    def __init__(
        self,
        label: str = "RW Lock",
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.readers = 0
        self.writer = None
        
        # Lock body (wider to show R/W sections)
        self.body = RoundedRectangle(
            width=1.2,
            height=0.6,
            color=C.LOCK_FREE,
            fill_opacity=0.2,
            stroke_width=A.LOCK_STROKE,
            corner_radius=0.1
        )
        
        # Read section
        self.read_section = Rectangle(
            width=0.5,
            height=0.4,
            color=C.INFO,
            fill_opacity=0.2,
            stroke_width=1
        )
        self.read_section.move_to(self.body.get_left() + RIGHT * 0.35)
        
        self.read_label = Text("R", font=F.CODE, color=C.INFO).scale(F.SIZE_TINY)
        self.read_label.move_to(self.read_section.get_center())
        
        # Write section
        self.write_section = Rectangle(
            width=0.5,
            height=0.4,
            color=C.ERROR,
            fill_opacity=0.2,
            stroke_width=1
        )
        self.write_section.move_to(self.body.get_right() + LEFT * 0.35)
        
        self.write_label = Text("W", font=F.CODE, color=C.ERROR).scale(F.SIZE_TINY)
        self.write_label.move_to(self.write_section.get_center())
        
        # Counter
        self.counter = Text("0", font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_TINY)
        self.counter.next_to(self.read_section, UP, buff=0.05)
        
        # Label
        self.label = Text(label, font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_TINY)
        self.label.next_to(self.body, DOWN, buff=L.SPACING_TIGHT)
        
        self.add(self.body, self.read_section, self.read_label,
                 self.write_section, self.write_label, self.counter, self.label)
    
    def animate_read_acquire(self):
        """Animate read lock acquisition"""
        self.readers += 1
        new_counter = Text(str(self.readers), font=F.CODE, color=C.INFO).scale(F.SIZE_TINY)
        new_counter.next_to(self.read_section, UP, buff=0.05)
        
        return AnimationGroup(
            self.read_section.animate.set_fill(opacity=0.4),
            Transform(self.counter, new_counter)
        )
    
    def animate_read_release(self):
        """Animate read lock release"""
        self.readers = max(0, self.readers - 1)
        new_counter = Text(str(self.readers), font=F.CODE, color=C.INFO).scale(F.SIZE_TINY)
        new_counter.next_to(self.read_section, UP, buff=0.05)
        
        opacity = 0.4 if self.readers > 0 else 0.2
        return AnimationGroup(
            self.read_section.animate.set_fill(opacity=opacity),
            Transform(self.counter, new_counter)
        )
    
    def animate_write_acquire(self):
        """Animate write lock acquisition"""
        self.writer = True
        return AnimationGroup(
            self.write_section.animate.set_fill(opacity=0.6),
            self.body.animate.set_color(C.LOCK_HELD)
        )
    
    def animate_write_release(self):
        """Animate write lock release"""
        self.writer = None
        return AnimationGroup(
            self.write_section.animate.set_fill(opacity=0.2),
            self.body.animate.set_color(C.LOCK_FREE)
        )


class SpinLock(VGroup):
    """
    Spinlock visualization with spinning indicator.
    """
    
    def __init__(
        self,
        label: str = "Spinlock",
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.state = "free"
        
        # Lock body
        self.body = Circle(
            radius=0.3,
            color=C.LOCK_FREE,
            fill_opacity=0.3,
            stroke_width=A.LOCK_STROKE
        )
        
        # Spin indicator (arc that rotates when spinning)
        self.spinner = Arc(
            radius=0.35,
            angle=PI/2,
            color=C.WARNING,
            stroke_width=3
        )
        self.spinner.set_opacity(0)
        
        # Label
        self.label = Text(label, font=F.CODE, color=C.TEXT_SECONDARY).scale(F.SIZE_TINY)
        self.label.next_to(self.body, DOWN, buff=L.SPACING_TIGHT)
        
        self.add(self.body, self.spinner, self.label)
    
    def animate_spin(self, duration: float = 1.0):
        """Animate spinning while waiting"""
        self.spinner.set_opacity(1)
        return Rotate(self.spinner, angle=TAU * 2, about_point=self.body.get_center(), run_time=duration)


class LockQueue(VGroup):
    """
    Queue of threads waiting for a lock.
    """
    
    def __init__(
        self,
        lock: Mutex,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.lock = lock
        self.waiting_threads = VGroup()
        
        # Queue indicator
        self.queue_line = Line(
            lock.get_left() + LEFT * 0.3,
            lock.get_left() + LEFT * 2.5,
            color=C.LOCK_WAITING,
            stroke_width=1,
            stroke_opacity=0.5
        )
        
        # Queue label
        self.queue_label = Text(
            "Wait Queue",
            font=F.CODE,
            color=C.TEXT_TERTIARY
        ).scale(F.SIZE_TINY)
        self.queue_label.next_to(self.queue_line, UP, buff=0.05)
        
        self.add(self.queue_line, self.queue_label, self.waiting_threads)
    
    def add_waiter(self, thread):
        """Add thread to wait queue"""
        thread.set_state("blocked")
        pos = self.queue_line.get_right() + LEFT * (0.5 + len(self.waiting_threads) * 0.7)
        thread.move_to(pos)
        self.waiting_threads.add(thread)
        return FadeIn(thread, shift=LEFT * 0.3)
    
    def remove_waiter(self):
        """Remove first thread from queue"""
        if len(self.waiting_threads) > 0:
            thread = self.waiting_threads[0]
            self.waiting_threads.remove(thread)
            return thread
        return None


class FineGrainedLock(VGroup):
    """
    Multiple fine-grained locks on sub-resources.
    """
    
    def __init__(
        self,
        num_locks: int = 4,
        labels: list = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.locks = []
        labels = labels or [f"L{i}" for i in range(num_locks)]
        
        for i, label in enumerate(labels):
            lock = Mutex(label=label, size=0.4)
            self.locks.append(lock)
            self.add(lock)
        
        self.arrange(RIGHT, buff=L.LOCK_SPACING)
    
    def get_lock(self, index: int) -> Mutex:
        """Get lock by index"""
        if 0 <= index < len(self.locks):
            return self.locks[index]
        return None
    
    def animate_acquire_subset(self, indices: list):
        """Animate acquiring a subset of locks"""
        animations = []
        for i in indices:
            if 0 <= i < len(self.locks):
                animations.append(self.locks[i].animate_acquire())
        return AnimationGroup(*animations, lag_ratio=0.1)
    
    def animate_release_all(self):
        """Animate releasing all locks"""
        return AnimationGroup(
            *[lock.animate_release() for lock in self.locks],
            lag_ratio=0.05
        )
