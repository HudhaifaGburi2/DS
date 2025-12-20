"""
Thread Components
=================

Visual representations of threads, processes, and CPU cores.
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import C, T, F, L, A, OS


class Thread(VGroup):
    """
    Visual thread representation.
    
    Shows thread ID, state, and execution progress.
    """
    
    def __init__(
        self,
        thread_id: int,
        color=None,
        state: str = "ready",
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.thread_id = thread_id
        self.color = color or C.THREAD_COLORS[(thread_id - 1) % len(C.THREAD_COLORS)]
        self.state = state
        
        # Thread body
        self.body = RoundedRectangle(
            width=L.THREAD_WIDTH,
            height=0.5,
            color=self.color,
            fill_opacity=0.4,
            stroke_width=A.THREAD_STROKE,
            corner_radius=0.1
        )
        
        # Thread label
        self.label = Text(
            f"T{thread_id}",
            font=F.CODE,
            color=self.color
        ).scale(F.SIZE_THREAD_ID)
        self.label.move_to(self.body.get_center())
        
        self.add(self.body, self.label)
        self._update_state_visual()
    
    def _update_state_visual(self):
        """Update visual based on state"""
        if self.state == "running":
            self.body.set_fill(opacity=0.6)
            self.body.set_stroke(color=C.RUNNING)
        elif self.state == "blocked":
            self.body.set_fill(opacity=A.BLOCKED_OPACITY)
            self.body.set_stroke(color=C.BLOCKED)
        elif self.state == "completed":
            self.body.set_fill(opacity=0.3)
            self.body.set_stroke(color=C.COMPLETED)
        else:  # ready
            self.body.set_fill(opacity=0.4)
            self.body.set_stroke(color=self.color)
    
    def set_state(self, state: str):
        """Change thread state"""
        self.state = state
        self._update_state_visual()
    
    def animate_spawn(self):
        """Animate thread creation"""
        return FadeIn(self, scale=0.5, run_time=T.THREAD_SPAWN)
    
    def animate_block(self):
        """Animate thread blocking"""
        return Succession(
            self.body.animate.set_fill(opacity=A.BLOCKED_OPACITY),
            self.body.animate.set_stroke(color=C.BLOCKED),
            run_time=T.THREAD_BLOCK
        )
    
    def animate_wake(self):
        """Animate thread waking"""
        return Succession(
            self.body.animate.set_fill(opacity=0.6),
            self.body.animate.set_stroke(color=C.RUNNING),
            run_time=T.THREAD_WAKE
        )
    
    def animate_complete(self):
        """Animate thread completion"""
        return self.animate.set_opacity(0.3)
    
    def animate_execute(self, target_pos, run_time: float = None):
        """Animate thread moving to execute"""
        run_time = run_time or T.NORMAL
        return self.animate.move_to(target_pos)


class ThreadGroup(VGroup):
    """
    Group of threads arranged in lanes or queue.
    """
    
    def __init__(
        self,
        num_threads: int = None,
        arrangement: str = "horizontal",  # "horizontal", "vertical", "lanes"
        **kwargs
    ):
        super().__init__(**kwargs)
        
        num_threads = num_threads or OS.DEFAULT_THREADS
        self.threads = []
        
        for i in range(num_threads):
            thread = Thread(thread_id=i + 1)
            self.threads.append(thread)
            self.add(thread)
        
        if arrangement == "horizontal":
            self.arrange(RIGHT, buff=L.SPACING_SM)
        elif arrangement == "vertical":
            self.arrange(DOWN, buff=L.SPACING_SM)
    
    def get_thread(self, thread_id: int) -> Thread:
        """Get thread by ID"""
        for thread in self.threads:
            if thread.thread_id == thread_id:
                return thread
        return None
    
    def animate_spawn_all(self):
        """Animate all threads spawning"""
        return LaggedStart(
            *[t.animate_spawn() for t in self.threads],
            lag_ratio=A.LAG_NORMAL
        )


class ProcessBlock(VGroup):
    """
    Visual process representation (larger than thread).
    """
    
    def __init__(
        self,
        process_id: int,
        num_threads: int = 1,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.process_id = process_id
        
        # Process container
        self.container = RoundedRectangle(
            width=2.0,
            height=1.2,
            color=C.TEXT_SECONDARY,
            fill_opacity=0.1,
            stroke_width=2,
            corner_radius=0.15
        )
        
        # Process label
        self.label = Text(
            f"Process {process_id}",
            font=F.CODE,
            color=C.TEXT_SECONDARY
        ).scale(F.SIZE_LABEL)
        self.label.next_to(self.container, UP, buff=L.SPACING_TIGHT)
        
        # Internal threads
        self.threads = VGroup()
        for i in range(num_threads):
            thread = Thread(thread_id=i + 1)
            thread.scale(0.7)
            self.threads.add(thread)
        
        self.threads.arrange(RIGHT, buff=0.1)
        self.threads.move_to(self.container.get_center())
        
        self.add(self.container, self.label, self.threads)


class CPUCore(VGroup):
    """
    Visual CPU core representation.
    """
    
    def __init__(
        self,
        core_id: int,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.core_id = core_id
        self.current_thread = None
        
        # Core body
        self.body = Square(
            side_length=1.0,
            color=C.TEXT_SECONDARY,
            fill_opacity=0.2,
            stroke_width=2
        )
        
        # Core label
        self.label = Text(
            f"CPU {core_id}",
            font=F.CODE,
            color=C.TEXT_SECONDARY
        ).scale(F.SIZE_TINY)
        self.label.next_to(self.body, UP, buff=L.SPACING_TIGHT)
        
        # Execution slot
        self.slot = RoundedRectangle(
            width=0.7,
            height=0.5,
            color=C.LOCK_FREE,
            fill_opacity=0.1,
            stroke_width=1,
            corner_radius=0.08
        )
        self.slot.move_to(self.body.get_center())
        
        self.add(self.body, self.label, self.slot)
    
    def animate_assign_thread(self, thread: Thread):
        """Animate assigning thread to core"""
        self.current_thread = thread
        return Succession(
            thread.animate.move_to(self.slot.get_center()).scale(0.8),
            self.slot.animate.set_fill(color=thread.color, opacity=0.3)
        )
    
    def animate_release_thread(self):
        """Animate releasing thread from core"""
        self.current_thread = None
        return self.slot.animate.set_fill(color=C.LOCK_FREE, opacity=0.1)
