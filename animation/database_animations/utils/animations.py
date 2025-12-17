"""
Database Animation Framework - Animation Helpers
=================================================

Custom animation utilities and helpers.
"""

from manim import *
import sys
sys.path.append('..')
from config import config, C, T, F, L, A, D


def create_staggered_fade_in(
    mobjects: list,
    direction: np.ndarray = UP,
    lag_ratio: float = 0.15,
    scale: float = None,
    run_time: float = None
) -> LaggedStart:
    """
    Create a staggered fade-in animation for multiple objects.
    
    Args:
        mobjects: List of mobjects to animate
        direction: Direction of the shift during fade
        lag_ratio: Delay between consecutive animations
        scale: Initial scale for fade (default: config value)
        run_time: Total animation duration
    
    Returns:
        LaggedStart animation
    """
    if scale is None:
        scale = A.FADE_IN_SCALE
    if run_time is None:
        run_time = T.NORMAL
    
    return LaggedStart(
        *[FadeIn(mob, shift=direction * 0.3, scale=scale) for mob in mobjects],
        lag_ratio=lag_ratio,
        run_time=run_time
    )


def create_staggered_fade_out(
    mobjects: list,
    direction: np.ndarray = DOWN,
    lag_ratio: float = 0.1,
    run_time: float = None
) -> LaggedStart:
    """
    Create a staggered fade-out animation for multiple objects.
    """
    if run_time is None:
        run_time = T.FAST
    
    return LaggedStart(
        *[FadeOut(mob, shift=direction * 0.3) for mob in mobjects],
        lag_ratio=lag_ratio,
        run_time=run_time
    )


def create_emphasis_sequence(
    mobject: Mobject,
    color=None,
    scale: float = None,
    iterations: int = 2
) -> Succession:
    """
    Create a pulsing emphasis animation sequence.
    
    Args:
        mobject: Object to emphasize
        color: Highlight color
        scale: Scale factor for pulse
        iterations: Number of pulse cycles
    
    Returns:
        Succession of pulse animations
    """
    if color is None:
        color = C.PRIMARY_YELLOW
    if scale is None:
        scale = A.EMPHASIS_SCALE
    
    original_color = mobject.get_color() if hasattr(mobject, 'get_color') else WHITE
    
    animations = []
    for _ in range(iterations):
        animations.extend([
            mobject.animate.scale(scale).set_color(color),
            mobject.animate.scale(1/scale).set_color(original_color)
        ])
    
    return Succession(
        *animations,
        run_time=T.QUICK * iterations * 2
    )


def create_shake_animation(
    mobject: Mobject,
    amplitude: float = 0.1,
    iterations: int = 3,
    run_time: float = None
) -> Succession:
    """
    Create a shake/wiggle animation for error states.
    
    Args:
        mobject: Object to shake
        amplitude: Max displacement
        iterations: Number of shakes
        run_time: Duration per shake
    
    Returns:
        Succession of shake movements
    """
    if run_time is None:
        run_time = T.INSTANT
    
    original_pos = mobject.get_center()
    
    animations = []
    for i in range(iterations):
        direction = RIGHT if i % 2 == 0 else LEFT
        animations.extend([
            mobject.animate.shift(direction * amplitude),
            mobject.animate.move_to(original_pos)
        ])
    
    return Succession(*[a for a in animations], run_time=run_time * iterations * 2)


def create_glow_animation(
    mobject: Mobject,
    color=None,
    glow_radius: float = None,
    fade_duration: float = None
) -> AnimationGroup:
    """
    Create a glow effect around a mobject.
    
    Args:
        mobject: Object to add glow to
        color: Glow color
        glow_radius: Size of glow
        fade_duration: Duration of glow fade
    
    Returns:
        Animation group with glow effect
    """
    if color is None:
        color = C.PRIMARY_YELLOW
    if glow_radius is None:
        glow_radius = A.GLOW_RADIUS
    if fade_duration is None:
        fade_duration = T.FAST
    
    # Create glow circle
    glow = Circle(
        radius=mobject.width / 2 + glow_radius,
        color=color,
        fill_opacity=0.3,
        stroke_width=0
    )
    glow.move_to(mobject)
    
    return Succession(
        FadeIn(glow, run_time=fade_duration / 2),
        FadeOut(glow, run_time=fade_duration / 2)
    )


def smooth_path(
    start: np.ndarray,
    end: np.ndarray,
    control_offset: np.ndarray = None
) -> CubicBezier:
    """
    Create a smooth bezier path between two points.
    
    Args:
        start: Starting position
        end: Ending position
        control_offset: Offset for control points
    
    Returns:
        CubicBezier curve
    """
    if control_offset is None:
        # Default: arc upward
        mid = (start + end) / 2
        control_offset = UP * 1.0
    
    control1 = start + control_offset
    control2 = end + control_offset
    
    return CubicBezier(start, control1, control2, end)


def create_arrow_flow(
    points: list,
    color=None,
    animate: bool = True
) -> VGroup:
    """
    Create a sequence of connected arrows.
    
    Args:
        points: List of points to connect
        color: Arrow color
        animate: Whether to return animation or just the group
    
    Returns:
        VGroup of arrows (or animation if animate=True)
    """
    if color is None:
        color = C.PRIMARY_YELLOW
    
    arrows = VGroup()
    for i in range(len(points) - 1):
        arrow = Arrow(
            points[i],
            points[i + 1],
            color=color,
            stroke_width=D.ARROW_STROKE_WIDTH
        )
        arrows.add(arrow)
    
    return arrows


def create_transform_sequence(
    mobject: Mobject,
    states: list,
    pause_between: float = None
) -> Succession:
    """
    Create a sequence of transformations.
    
    Args:
        mobject: Starting mobject
        states: List of target states to transform through
        pause_between: Pause duration between transforms
    
    Returns:
        Succession of Transform animations
    """
    if pause_between is None:
        pause_between = T.PAUSE_SHORT
    
    animations = []
    for state in states:
        animations.append(Transform(mobject, state, run_time=T.NORMAL))
        animations.append(Wait(pause_between))
    
    return Succession(*animations)


def highlight_and_explain(
    target: Mobject,
    explanation: str,
    position: str = "below",
    color=None
) -> tuple:
    """
    Create highlight box and explanation text.
    
    Args:
        target: Object to highlight
        explanation: Text to display
        position: Where to place explanation (below/above/left/right)
        color: Highlight color
    
    Returns:
        Tuple of (highlight_box, explanation_text, animation)
    """
    if color is None:
        color = C.PRIMARY_YELLOW
    
    # Create highlight
    highlight = SurroundingRectangle(
        target,
        color=color,
        buff=0.1,
        corner_radius=0.1
    )
    
    # Create explanation
    explanation_text = Text(
        explanation,
        font=F.BODY,
        color=color
    ).scale(F.SIZE_CAPTION)
    
    # Position explanation
    position_map = {
        "below": (DOWN, 0.3),
        "above": (UP, 0.3),
        "left": (LEFT, 0.5),
        "right": (RIGHT, 0.5)
    }
    direction, buff = position_map.get(position, (DOWN, 0.3))
    explanation_text.next_to(target, direction, buff=buff)
    
    # Create animation
    animation = AnimationGroup(
        Create(highlight),
        Write(explanation_text),
        run_time=T.FAST
    )
    
    return highlight, explanation_text, animation


class AnimationSequencer:
    """
    Helper class to build complex animation sequences.
    
    Usage:
        seq = AnimationSequencer(scene)
        seq.add(FadeIn(obj1))
        seq.add_wait(0.5)
        seq.add(FadeIn(obj2))
        seq.play_all()
    """
    
    def __init__(self, scene: Scene):
        self.scene = scene
        self.animations = []
    
    def add(self, *animations):
        """Add animations to sequence"""
        self.animations.extend(animations)
        return self
    
    def add_wait(self, duration: float = None):
        """Add a wait to the sequence"""
        if duration is None:
            duration = T.PAUSE_SHORT
        self.animations.append(Wait(duration))
        return self
    
    def add_parallel(self, *animations):
        """Add animations that play together"""
        self.animations.append(AnimationGroup(*animations))
        return self
    
    def play_all(self):
        """Play all accumulated animations"""
        for anim in self.animations:
            if isinstance(anim, Wait):
                self.scene.wait(anim.run_time)
            else:
                self.scene.play(anim)
        self.animations = []
    
    def clear(self):
        """Clear animation queue"""
        self.animations = []
