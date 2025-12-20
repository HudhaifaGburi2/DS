"""
Animation Utilities for OS Concepts
===================================

Helper functions for creating complex concurrency animations.
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import C, T, F, L, A


def create_thread_execution(
    thread,
    path_points: list,
    run_time: float = None
) -> Succession:
    """
    Create thread execution animation along a path.
    
    Args:
        thread: Thread mobject
        path_points: List of positions
        run_time: Total animation time
    """
    run_time = run_time or T.NORMAL * len(path_points)
    segment_time = run_time / len(path_points)
    
    animations = []
    for point in path_points:
        animations.append(
            thread.animate.move_to(point)
        )
    
    return Succession(*animations, run_time=segment_time)


def create_lock_sequence(
    lock,
    thread,
    action: str = "acquire"  # "acquire" or "release"
) -> Succession:
    """
    Create lock acquire/release animation sequence.
    """
    if action == "acquire":
        return Succession(
            thread.animate.move_to(lock.get_left() + LEFT * 0.5),
            lock.animate_acquire(thread.thread_id),
            thread.animate.set_state("running")
        )
    else:
        return Succession(
            lock.animate_release(),
            thread.animate.move_to(lock.get_right() + RIGHT * 0.5)
        )


def create_conflict_animation(
    target: Mobject,
    flash_color=None
) -> Succession:
    """
    Create conflict detection animation.
    """
    flash_color = flash_color or C.CONFLICT
    
    return Succession(
        target.animate.set_stroke(color=flash_color, width=A.HIGHLIGHT_STROKE),
        Flash(target, color=flash_color, line_length=0.3),
        target.animate.set_stroke(color=C.TEXT_SECONDARY, width=2)
    )


def create_rollback_sequence(
    thread,
    start_pos,
    rollback_pos,
    affected_objects: list = None
) -> Succession:
    """
    Create transaction rollback animation.
    """
    animations = [
        thread.animate.move_to(rollback_pos),
    ]
    
    if affected_objects:
        for obj in affected_objects:
            animations.append(
                obj.animate.set_opacity(A.GHOST_OPACITY)
            )
    
    return Succession(*animations)


class AnimationSequencer:
    """
    Helper class for building complex animation sequences.
    """
    
    def __init__(self, scene: Scene):
        self.scene = scene
        self.sequence = []
        self._parallel_group = []
    
    def add(self, animation: Animation, parallel: bool = False):
        """Add animation to sequence"""
        if parallel:
            self._parallel_group.append(animation)
        else:
            self._flush_parallel()
            self.sequence.append(animation)
    
    def wait(self, duration: float = None):
        """Add wait to sequence"""
        duration = duration or T.BEAT
        self._flush_parallel()
        self.sequence.append(Wait(duration))
    
    def _flush_parallel(self):
        """Flush parallel group"""
        if self._parallel_group:
            self.sequence.append(AnimationGroup(*self._parallel_group))
            self._parallel_group = []
    
    def play_all(self):
        """Execute all animations"""
        self._flush_parallel()
        for anim in self.sequence:
            self.scene.play(anim)
    
    def clear(self):
        """Clear sequence"""
        self.sequence = []
        self._parallel_group = []


def create_staggered_spawn(
    threads: list,
    lag_ratio: float = None
) -> LaggedStart:
    """Create staggered thread spawn animation"""
    lag_ratio = lag_ratio or A.LAG_NORMAL
    return LaggedStart(
        *[FadeIn(t, scale=0.5) for t in threads],
        lag_ratio=lag_ratio
    )


def create_contention_wave(
    center,
    num_waves: int = 3,
    color=None
) -> Succession:
    """Create expanding contention waves"""
    color = color or C.CONTENTION_HIGH
    
    waves = []
    for i in range(num_waves):
        ring = Circle(
            radius=0.2,
            color=color,
            stroke_width=2,
            stroke_opacity=0.8
        )
        ring.move_to(center)
        waves.append(ring)
    
    animations = []
    for ring in waves:
        animations.append(
            Succession(
                FadeIn(ring),
                ring.animate.scale(2).set_opacity(0),
                FadeOut(ring)
            )
        )
    
    return LaggedStart(*animations, lag_ratio=0.3)


def create_version_transition(
    old_version,
    new_version
) -> Succession:
    """Animate version transition (MVCC)"""
    return Succession(
        old_version.animate.set_opacity(A.GHOST_OPACITY),
        FadeIn(new_version, shift=RIGHT * 0.3),
        new_version.animate.set_stroke(color=C.VERSION_NEW, width=2)
    )
