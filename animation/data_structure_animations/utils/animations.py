"""
Animation Utilities
===================

Helper functions for creating complex animations.
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import C, T, F, L, A


def create_staggered_animation(
    mobjects: list,
    animation_func,
    lag_ratio: float = None,
    **kwargs
) -> LaggedStart:
    """
    Create staggered animation for multiple mobjects.
    
    Args:
        mobjects: List of mobjects to animate
        animation_func: Animation function or class (e.g., FadeIn)
        lag_ratio: Delay between animations
        **kwargs: Additional arguments for animation
    
    Returns:
        LaggedStart animation
    """
    lag_ratio = lag_ratio or A.LAG_NORMAL
    
    animations = []
    for mob in mobjects:
        if callable(animation_func):
            if isinstance(animation_func, type):
                # It's a class like FadeIn
                anim = animation_func(mob, **kwargs)
            else:
                # It's a function
                anim = animation_func(mob, **kwargs)
            animations.append(anim)
    
    return LaggedStart(*animations, lag_ratio=lag_ratio)


def create_emphasis_sequence(
    mobject: Mobject,
    color=None,
    scale: float = 1.15,
    num_pulses: int = 2
) -> Succession:
    """
    Create emphasis animation sequence.
    
    Args:
        mobject: Mobject to emphasize
        color: Highlight color
        scale: Scale factor for pulse
        num_pulses: Number of pulse cycles
    
    Returns:
        Succession animation
    """
    color = color or C.TEXT_ACCENT
    
    animations = []
    for _ in range(num_pulses):
        animations.extend([
            mobject.animate.scale(scale),
            mobject.animate.scale(1 / scale)
        ])
    
    return Succession(*animations, run_time=T.FAST * num_pulses)


def create_highlight_flash(
    mobject: Mobject,
    color=None,
    line_length: float = 0.3
) -> Flash:
    """
    Create flash highlight effect.
    
    Args:
        mobject: Target mobject
        color: Flash color
        line_length: Length of flash lines
    
    Returns:
        Flash animation
    """
    color = color or C.TEXT_ACCENT
    return Flash(
        mobject,
        color=color,
        line_length=line_length,
        run_time=T.FAST
    )


def create_path_trace(
    path_points: list,
    color=None,
    stroke_width: float = None
) -> Succession:
    """
    Create path tracing animation.
    
    Args:
        path_points: List of points defining path
        color: Path color
        stroke_width: Line width
    
    Returns:
        Succession of line creations
    """
    color = color or C.IO_READ
    stroke_width = stroke_width or A.PATH_STROKE
    
    animations = []
    for i in range(len(path_points) - 1):
        line = Line(
            path_points[i],
            path_points[i + 1],
            color=color,
            stroke_width=stroke_width
        )
        animations.append(Create(line, run_time=T.FAST))
    
    return Succession(*animations)


def create_comparison_reveal(
    left_mobject: Mobject,
    right_mobject: Mobject,
    direction: str = "both"  # "left", "right", "both"
) -> Animation:
    """
    Create comparison reveal animation.
    
    Args:
        left_mobject: Left side mobject
        right_mobject: Right side mobject
        direction: Which side(s) to reveal
    
    Returns:
        Animation for comparison reveal
    """
    if direction == "left":
        return FadeIn(left_mobject, shift=RIGHT * 0.5)
    elif direction == "right":
        return FadeIn(right_mobject, shift=LEFT * 0.5)
    else:
        return AnimationGroup(
            FadeIn(left_mobject, shift=RIGHT * 0.3),
            FadeIn(right_mobject, shift=LEFT * 0.3)
        )


class AnimationSequencer:
    """
    Helper class for building complex animation sequences.
    
    Usage:
        seq = AnimationSequencer(scene)
        seq.add(FadeIn(obj1))
        seq.add(FadeIn(obj2), parallel=True)
        seq.wait(0.5)
        seq.add(FadeOut(obj1))
        seq.play_all()
    """
    
    def __init__(self, scene: Scene):
        self.scene = scene
        self.sequence = []
        self._current_parallel = []
    
    def add(self, animation: Animation, parallel: bool = False):
        """
        Add animation to sequence.
        
        Args:
            animation: Animation to add
            parallel: If True, run in parallel with previous
        """
        if parallel:
            self._current_parallel.append(animation)
        else:
            self._flush_parallel()
            self.sequence.append(animation)
    
    def wait(self, duration: float):
        """Add wait to sequence"""
        self._flush_parallel()
        self.sequence.append(Wait(duration))
    
    def _flush_parallel(self):
        """Flush parallel animations"""
        if self._current_parallel:
            self.sequence.append(AnimationGroup(*self._current_parallel))
            self._current_parallel = []
    
    def play_all(self):
        """Play entire sequence"""
        self._flush_parallel()
        for anim in self.sequence:
            self.scene.play(anim)
    
    def clear(self):
        """Clear sequence"""
        self.sequence = []
        self._current_parallel = []


def create_io_animation(
    start_pos,
    end_pos,
    io_type: str = "read",
    run_time: float = None
) -> Succession:
    """
    Create I/O operation animation.
    
    Args:
        start_pos: Starting position
        end_pos: Ending position
        io_type: "read" or "write"
        run_time: Animation duration
    
    Returns:
        Succession animation for I/O
    """
    color = C.IO_READ if io_type == "read" else C.IO_WRITE
    run_time = run_time or T.IO_ARROW
    
    # Create animated dot
    dot = Dot(color=color, radius=0.08)
    dot.move_to(start_pos)
    
    # Create path
    path = Line(start_pos, end_pos)
    
    return Succession(
        FadeIn(dot, scale=0.5),
        MoveAlongPath(dot, path, run_time=run_time),
        FadeOut(dot, scale=0.5)
    )


def create_split_animation(
    source: Mobject,
    left_target: Mobject,
    right_target: Mobject,
    up_key: Mobject = None
) -> Succession:
    """
    Create node split animation.
    
    Args:
        source: Source node being split
        left_target: Left result node
        right_target: Right result node
        up_key: Key being promoted (optional)
    
    Returns:
        Animation sequence for split
    """
    animations = [
        source.animate.set_stroke(color=C.BTREE_SPLIT, width=3),
    ]
    
    if up_key:
        animations.append(up_key.animate.shift(UP * 0.5))
    
    animations.extend([
        AnimationGroup(
            FadeIn(left_target, shift=LEFT * 0.3),
            FadeIn(right_target, shift=RIGHT * 0.3)
        ),
        FadeOut(source)
    ])
    
    return Succession(*animations)


def create_merge_animation(
    left_source: Mobject,
    right_source: Mobject,
    target: Mobject,
    down_key: Mobject = None
) -> Succession:
    """
    Create node merge animation.
    
    Args:
        left_source: Left node being merged
        right_source: Right node being merged
        target: Merged result node
        down_key: Key being demoted (optional)
    
    Returns:
        Animation sequence for merge
    """
    animations = [
        AnimationGroup(
            left_source.animate.set_stroke(color=C.BTREE_MERGE),
            right_source.animate.set_stroke(color=C.BTREE_MERGE)
        )
    ]
    
    if down_key:
        animations.append(down_key.animate.shift(DOWN * 0.5))
    
    animations.extend([
        AnimationGroup(
            left_source.animate.move_to(target.get_center()),
            right_source.animate.move_to(target.get_center())
        ),
        AnimationGroup(
            FadeOut(left_source),
            FadeOut(right_source),
            FadeIn(target)
        )
    ])
    
    return Succession(*animations)
