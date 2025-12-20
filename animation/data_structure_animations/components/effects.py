"""
Visual Effects for Data Structure Animations
=============================================

Provides dramatic visual effects:
- HighlightPulse: Emphasis pulse effect
- WriteAmplification: Visualize write amplification
- CompactionWave: LSM compaction sweep
- IOFlowDot: Data flow indicator
- SearchBeam: Search path highlight
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import C, T, F, L, DS, A


class HighlightPulse(VGroup):
    """
    Pulsing highlight effect for emphasis.
    
    Visual: Expanding ring with fade.
    """
    
    def __init__(
        self,
        target: Mobject,
        color=None,
        num_pulses: int = 2,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.target = target
        self.color = color or C.TEXT_ACCENT
        self.num_pulses = num_pulses
        
        # Create pulse rings
        self.rings = VGroup()
        for i in range(num_pulses):
            ring = Circle(
                radius=0.1,
                color=self.color,
                stroke_width=3,
                stroke_opacity=1 - i * 0.3
            )
            ring.move_to(target.get_center())
            self.rings.add(ring)
        
        self.add(self.rings)
    
    def animate_pulse(self, scale: float = 2.0):
        """Animate pulsing effect"""
        animations = []
        for i, ring in enumerate(self.rings):
            anim = Succession(
                Wait(i * 0.15),  # Stagger
                AnimationGroup(
                    ring.animate.scale(scale),
                    ring.animate.set_stroke(opacity=0)
                )
            )
            animations.append(anim)
        
        return AnimationGroup(*animations)


class WriteAmplification(VGroup):
    """
    Visualize write amplification effect.
    
    Shows multiple writes being generated from single write.
    """
    
    def __init__(
        self,
        origin,
        amplification_factor: int = 3,
        color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.origin = origin
        self.factor = amplification_factor
        self.color = color or C.WRITE_AMP
        
        # Original write indicator
        self.original = Dot(
            point=origin,
            color=C.IO_WRITE,
            radius=0.12
        )
        self.add(self.original)
        
        # Amplified writes
        self.amplified = VGroup()
        for i in range(amplification_factor):
            dot = Dot(
                color=self.color,
                radius=0.08
            )
            angle = -PI/2 + (i - (amplification_factor-1)/2) * 0.4
            dot.move_to(origin + DOWN * 0.8 + RIGHT * np.sin(angle) * 0.6)
            self.amplified.add(dot)
        
        self.add(self.amplified)
        
        # Connecting lines
        self.lines = VGroup()
        for dot in self.amplified:
            line = Line(
                origin,
                dot.get_center(),
                color=self.color,
                stroke_width=1.5,
                stroke_opacity=0.6
            )
            self.lines.add(line)
        
        self.add(self.lines)
        
        # Factor label
        self.label = Text(
            f"×{amplification_factor}",
            font=F.CODE,
            color=self.color
        ).scale(F.SIZE_LABEL)
        self.label.next_to(self.amplified, DOWN, buff=0.15)
        self.add(self.label)
    
    def animate_amplify(self):
        """Animate the amplification effect"""
        return Succession(
            # Original write appears
            FadeIn(self.original, scale=0.5),
            # Splits into multiple
            AnimationGroup(
                *[Create(line) for line in self.lines]
            ),
            LaggedStart(
                *[FadeIn(dot, scale=0.5) for dot in self.amplified],
                lag_ratio=0.1
            ),
            # Show factor
            FadeIn(self.label, shift=UP * 0.1)
        )


class CompactionWave(VGroup):
    """
    LSM compaction sweep visualization.
    
    Shows data being merged and rewritten.
    """
    
    def __init__(
        self,
        start_pos,
        end_pos,
        width: float = 0.3,
        color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width
        self.color = color or C.LSM_COMPACTION
        
        # Wave bar
        self.wave = Rectangle(
            width=width,
            height=abs(end_pos[1] - start_pos[1]) + 0.5,
            fill_color=self.color,
            fill_opacity=0.4,
            stroke_color=self.color,
            stroke_width=2
        )
        self.wave.move_to(start_pos)
        self.add(self.wave)
        
        # "Compacting" label
        self.label = Text(
            "Compacting",
            font=F.CODE,
            color=self.color
        ).scale(F.SIZE_TINY)
        self.label.next_to(self.wave, UP, buff=0.1)
        self.add(self.label)
    
    def animate_sweep(self, run_time: float = None):
        """Animate compaction sweep across data"""
        run_time = run_time or T.COMPACTION
        
        return Succession(
            FadeIn(self, shift=LEFT * 0.2),
            self.animate.move_to(self.end_pos),
            FadeOut(self, shift=RIGHT * 0.2)
        )


class IOFlowDot(VGroup):
    """
    Animated dot showing data flow.
    
    Visual: Dot traveling along a path.
    """
    
    def __init__(
        self,
        color=None,
        radius: float = 0.08,
        trail: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.color = color or C.IO_WRITE
        self.radius = radius
        self.trail = trail
        
        # Main dot
        self.dot = Dot(
            color=self.color,
            radius=radius
        )
        self.add(self.dot)
        
        # Glow effect
        self.glow = Dot(
            color=self.color,
            radius=radius * 2,
            fill_opacity=0.3
        )
        self.add(self.glow)
    
    def animate_along_path(self, path: VMobject, run_time: float = None):
        """Animate dot moving along path"""
        run_time = run_time or T.IO_ARROW
        
        return MoveAlongPath(self, path, run_time=run_time)
    
    def animate_to(self, target_pos, run_time: float = None):
        """Animate dot moving to position"""
        run_time = run_time or T.IO_ARROW
        
        return self.animate.move_to(target_pos)


class SearchBeam(VGroup):
    """
    Search path highlight beam.
    
    Visual: Glowing line tracing search path.
    """
    
    def __init__(
        self,
        path_points: list,
        color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.path_points = path_points
        self.color = color or C.IO_READ
        
        # Create path segments
        self.segments = VGroup()
        for i in range(len(path_points) - 1):
            segment = Line(
                path_points[i],
                path_points[i + 1],
                color=self.color,
                stroke_width=A.PATH_STROKE,
                stroke_opacity=0.8
            )
            self.segments.add(segment)
        
        self.add(self.segments)
        
        # Glow overlay
        self.glow_segments = VGroup()
        for i in range(len(path_points) - 1):
            glow = Line(
                path_points[i],
                path_points[i + 1],
                color=self.color,
                stroke_width=A.PATH_STROKE * 3,
                stroke_opacity=0.2
            )
            self.glow_segments.add(glow)
        
        self.add(self.glow_segments)
    
    def animate_trace(self):
        """Animate tracing the search path"""
        animations = []
        
        for i, (seg, glow) in enumerate(zip(self.segments, self.glow_segments)):
            animations.append(
                AnimationGroup(
                    Create(seg),
                    Create(glow)
                )
            )
        
        return LaggedStart(*animations, lag_ratio=0.3)
    
    def animate_fade(self):
        """Fade out the search beam"""
        return FadeOut(self)


class ReadWriteIndicator(VGroup):
    """
    Visual indicator for read/write operations.
    
    Shows operation type with icon and animation.
    """
    
    def __init__(
        self,
        operation: str = "read",  # "read" or "write"
        position=ORIGIN,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.operation = operation
        
        if operation == "read":
            self.color = C.IO_READ
            self.icon_text = "R"
            self.label_text = "READ"
        else:
            self.color = C.IO_WRITE
            self.icon_text = "W"
            self.label_text = "WRITE"
        
        # Icon circle
        self.icon_bg = Circle(
            radius=0.25,
            fill_color=self.color,
            fill_opacity=0.2,
            stroke_color=self.color,
            stroke_width=2
        )
        
        # Icon letter
        self.icon = Text(
            self.icon_text,
            font=F.CODE,
            color=self.color
        ).scale(F.SIZE_BODY)
        self.icon.move_to(self.icon_bg.get_center())
        
        # Label
        self.label = Text(
            self.label_text,
            font=F.CODE,
            color=self.color
        ).scale(F.SIZE_TINY)
        self.label.next_to(self.icon_bg, DOWN, buff=0.1)
        
        self.add(self.icon_bg, self.icon, self.label)
        self.move_to(position)
    
    def animate_activate(self):
        """Show operation activation"""
        return Succession(
            FadeIn(self, scale=0.8),
            self.icon_bg.animate.set_fill(opacity=0.5),
            self.icon_bg.animate.set_fill(opacity=0.2)
        )


class MetricBar(VGroup):
    """
    Animated metric comparison bar.
    
    Visual: Horizontal bar with value label.
    """
    
    def __init__(
        self,
        label: str,
        value: float,
        max_value: float = 100,
        width: float = 3.0,
        height: float = 0.3,
        color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.label_text = label
        self.value = value
        self.max_value = max_value
        self.width = width
        self.height = height
        self.color = color or C.INFO
        
        # Background bar
        self.bg = Rectangle(
            width=width,
            height=height,
            fill_color=C.TEXT_TERTIARY,
            fill_opacity=0.1,
            stroke_color=C.TEXT_TERTIARY,
            stroke_width=1
        )
        self.add(self.bg)
        
        # Value bar
        value_width = (value / max_value) * width
        self.value_bar = Rectangle(
            width=value_width,
            height=height - 0.05,
            fill_color=self.color,
            fill_opacity=0.6,
            stroke_width=0
        )
        self.value_bar.align_to(self.bg, LEFT)
        self.add(self.value_bar)
        
        # Label
        self.label = Text(label, font=F.BODY, color=C.TEXT_PRIMARY).scale(F.SIZE_LABEL)
        self.label.next_to(self.bg, LEFT, buff=L.SPACING_SM)
        self.add(self.label)
        
        # Value text
        self.value_text = Text(
            f"{value:.1f}",
            font=F.CODE,
            color=self.color
        ).scale(F.SIZE_TINY)
        self.value_text.next_to(self.bg, RIGHT, buff=L.SPACING_TIGHT)
        self.add(self.value_text)
    
    def animate_fill(self):
        """Animate bar filling"""
        target_width = self.value_bar.width
        self.value_bar.stretch_to_fit_width(0.01)
        self.value_bar.align_to(self.bg, LEFT)
        
        return self.value_bar.animate.stretch_to_fit_width(target_width).align_to(self.bg, LEFT)
    
    def update_value(self, new_value: float):
        """Update the bar value"""
        self.value = new_value
        new_width = (new_value / self.max_value) * self.width
        
        # Update value text
        new_text = Text(
            f"{new_value:.1f}",
            font=F.CODE,
            color=self.color
        ).scale(F.SIZE_TINY)
        new_text.next_to(self.bg, RIGHT, buff=L.SPACING_TIGHT)
        
        return AnimationGroup(
            self.value_bar.animate.stretch_to_fit_width(new_width).align_to(self.bg, LEFT),
            Transform(self.value_text, new_text)
        )
