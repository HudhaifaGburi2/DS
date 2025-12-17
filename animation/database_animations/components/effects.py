"""
Database Animation Framework - Visual Effects
==============================================

Dramatic visual effects for database animations.
Crash effects, fsync visualizations, atomic operations, etc.
"""

from manim import *
import sys
sys.path.append('..')
from config import config, C, T, F, L, A, D


class CrashEffect(VGroup):
    """
    Dramatic crash/failure effect.
    
    Creates an explosion-like visual with optional text.
    Can be positioned anywhere in the scene.
    """
    
    def __init__(
        self,
        text: str = "CRASH!",
        icon: str = "💥",
        color=None,
        position=None,
        scale_factor: float = 1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        if color is None:
            color = C.ERROR
        if position is None:
            position = ORIGIN
        
        self.color = color
        
        # Explosion icon
        self.icon = Text(icon, font=F.EMOJI).scale(2 * scale_factor)
        
        # Crash text
        self.text = Text(
            text,
            font=F.BODY,
            color=color,
            weight=BOLD
        ).scale(F.SIZE_HEADING * scale_factor)
        
        self.text.next_to(self.icon, DOWN, buff=L.SPACING_MD)
        
        self.add(self.icon, self.text)
        self.move_to(position)
    
    def animate_appear(self) -> AnimationGroup:
        """Dramatic crash appearance"""
        return AnimationGroup(
            FadeIn(self.icon, scale=0.3, run_time=T.QUICK),
            Flash(
                self.icon.get_center(),
                color=self.color,
                line_length=0.5,
                num_lines=16,
                run_time=T.FAST
            ),
            Write(self.text, run_time=T.FAST),
            lag_ratio=0.2
        )
    
    def animate_shake_and_appear(self, target: Mobject = None) -> Succession:
        """Crash with screen shake effect on target"""
        shake_animations = []
        if target:
            original_pos = target.get_center()
            for i in range(3):
                offset = RIGHT * 0.1 * (1 if i % 2 == 0 else -1)
                shake_animations.extend([
                    target.animate.shift(offset),
                    target.animate.move_to(original_pos)
                ])
        
        return Succession(
            *shake_animations,
            self.animate_appear()
        )


class FsyncEffect(VGroup):
    """
    Visual representation of fsync operation.
    
    Shows a pulsing circle that indicates data being synced to disk.
    """
    
    def __init__(
        self,
        position=None,
        color=None,
        label: str = "fsync",
        **kwargs
    ):
        super().__init__(**kwargs)
        
        if color is None:
            color = C.PRIMARY_YELLOW
        if position is None:
            position = ORIGIN
        
        self.color = color
        
        # Inner circle
        self.inner_circle = Circle(
            radius=0.2,
            color=color,
            fill_opacity=0.8
        )
        
        # Outer expanding ring
        self.outer_ring = Circle(
            radius=0.2,
            color=color,
            stroke_width=3,
            fill_opacity=0
        )
        
        # Label
        self.label = Text(
            label,
            font=F.CODE,
            color=color
        ).scale(F.SIZE_CAPTION)
        self.label.next_to(self.inner_circle, DOWN, buff=L.SPACING_SM)
        
        self.add(self.inner_circle, self.outer_ring, self.label)
        self.move_to(position)
    
    def animate_sync(self, iterations: int = 2) -> Succession:
        """Pulsing sync animation"""
        animations = []
        for _ in range(iterations):
            animations.append(
                AnimationGroup(
                    self.outer_ring.animate.scale(2).set_opacity(0),
                    run_time=T.FAST
                )
            )
            # Reset ring for next pulse
            animations.append(
                self.outer_ring.animate.scale(0.5).set_opacity(1)
            )
        return Succession(*animations)
    
    def animate_complete(self) -> AnimationGroup:
        """Show sync completion"""
        checkmark = Text("✓", font=F.EMOJI, color=C.SUCCESS).scale(0.5)
        checkmark.move_to(self.inner_circle)
        
        return AnimationGroup(
            FadeOut(self.label),
            Transform(self.inner_circle, checkmark),
            run_time=T.FAST
        )


class AtomicEffect(VGroup):
    """
    Visual effect for atomic operations.
    
    Shows a shield/lock icon with glow to represent atomicity.
    """
    
    def __init__(
        self,
        text: str = "ATOMIC",
        icon: str = "🔒",
        color=None,
        position=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        if color is None:
            color = C.PRIMARY_PURPLE
        if position is None:
            position = ORIGIN
        
        self.color = color
        
        # Shield background
        self.shield = Circle(
            radius=0.5,
            color=color,
            fill_opacity=0.2,
            stroke_width=3
        )
        
        # Lock icon
        self.icon = Text(icon, font=F.EMOJI).scale(0.8)
        self.icon.move_to(self.shield)
        
        # Label
        self.label = Text(
            text,
            font=F.CODE,
            color=color,
            weight=BOLD
        ).scale(F.SIZE_CAPTION)
        self.label.next_to(self.shield, DOWN, buff=L.SPACING_SM)
        
        self.add(self.shield, self.icon, self.label)
        self.move_to(position)
    
    def animate_lock(self) -> Succession:
        """Dramatic locking animation"""
        return Succession(
            FadeIn(self.shield, scale=1.5, run_time=T.QUICK),
            FadeIn(self.icon, scale=0.5, run_time=T.QUICK),
            AnimationGroup(
                Flash(self.shield.get_center(), color=self.color),
                Write(self.label),
                run_time=T.FAST
            )
        )
    
    def animate_glow(self) -> Animation:
        """Pulsing glow effect"""
        return Indicate(
            self.shield,
            color=self.color,
            scale_factor=1.2
        )


class CorruptionEffect(VGroup):
    """
    Visual glitch/corruption effect.
    
    Creates visual noise and distortion to show data corruption.
    """
    
    def __init__(
        self,
        target_width: float = 2.0,
        target_height: float = 1.5,
        position=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        if position is None:
            position = ORIGIN
        
        # Create glitch lines
        self.glitch_lines = VGroup()
        for i in range(5):
            line = Line(
                LEFT * target_width * 0.4,
                RIGHT * target_width * 0.4,
                color=C.ERROR,
                stroke_width=2
            )
            line.shift(UP * (i - 2) * 0.2)
            line.set_opacity(0.7)
            self.glitch_lines.add(line)
        
        # Corruption symbol
        self.symbol = Text("✗", font=F.EMOJI, color=C.ERROR).scale(1.0)
        
        self.add(self.glitch_lines, self.symbol)
        self.move_to(position)
        self.set_opacity(0)  # Start invisible
    
    def animate_corrupt(self, target: Mobject = None) -> AnimationGroup:
        """Show corruption effect"""
        animations = [
            self.animate.set_opacity(1),
            Flash(self.get_center(), color=C.ERROR, line_length=0.3)
        ]
        
        if target:
            animations.extend([
                target.animate.set_opacity(0.3),
                Wiggle(target, scale_value=1.05, rotation_angle=0.02)
            ])
        
        return AnimationGroup(*animations, run_time=T.FAST)


class SuccessCheckmark(VGroup):
    """
    Animated success checkmark.
    
    Green checkmark with optional celebratory effect.
    """
    
    def __init__(
        self,
        text: str = None,
        position=None,
        scale_factor: float = 1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        if position is None:
            position = ORIGIN
        
        # Checkmark
        self.checkmark = Text("✓", font=F.EMOJI, color=C.SUCCESS)
        self.checkmark.scale(1.5 * scale_factor)
        
        # Optional text
        if text:
            self.text = Text(
                text,
                font=F.BODY,
                color=C.SUCCESS
            ).scale(F.SIZE_BODY * scale_factor)
            self.text.next_to(self.checkmark, RIGHT, buff=L.SPACING_SM)
            self.add(self.checkmark, self.text)
        else:
            self.add(self.checkmark)
        
        self.move_to(position)
    
    def animate_appear(self) -> AnimationGroup:
        """Celebratory checkmark appearance"""
        return AnimationGroup(
            FadeIn(self, scale=0.5),
            Flash(self.get_center(), color=C.SUCCESS, line_length=0.3),
            run_time=T.FAST
        )
    
    def animate_draw(self) -> Animation:
        """Draw the checkmark"""
        return Write(self, run_time=T.FAST)


class DataFlowDot(VGroup):
    """
    Animated dot representing data flow.
    
    Used to show data moving through storage layers.
    """
    
    def __init__(
        self,
        color=None,
        label: str = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        if color is None:
            color = C.DATA_COLD
        
        self.color = color
        
        # Main dot
        self.dot = Dot(radius=D.DOT_RADIUS * 1.5, color=color)
        
        # Glow effect
        self.glow = Circle(
            radius=D.DOT_RADIUS * 2,
            color=color,
            fill_opacity=0.3,
            stroke_width=0
        )
        
        # Optional label
        if label:
            self.label = Text(
                label,
                font=F.CODE,
                color=color
            ).scale(F.SIZE_TINY)
            self.label.next_to(self.dot, RIGHT, buff=L.SPACING_TIGHT)
            self.add(self.label)
        
        self.add(self.glow, self.dot)
    
    def animate_pulse(self) -> Animation:
        """Pulsing glow animation"""
        return Succession(
            self.glow.animate.scale(1.5).set_opacity(0),
            self.glow.animate.scale(0.67).set_opacity(0.3),
            run_time=T.FAST
        )
    
    def animate_move_along_path(self, path: VMobject) -> Animation:
        """Move dot along a path"""
        return MoveAlongPath(self, path, run_time=T.SLOW)
    
    def set_safe(self):
        """Mark data as safely persisted"""
        self.dot.set_color(C.DATA_SAFE)
        self.glow.set_color(C.DATA_SAFE)
        return self
    
    def set_danger(self):
        """Mark data as in danger"""
        self.dot.set_color(C.DATA_HOT)
        self.glow.set_color(C.DATA_HOT)
        return self


class WarningBadge(VGroup):
    """
    Warning indicator badge.
    
    Yellow warning triangle with optional text.
    """
    
    def __init__(
        self,
        text: str = "⚠️",
        label: str = None,
        position=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        if position is None:
            position = ORIGIN
        
        self.icon = Text(text, font=F.EMOJI).scale(1.0)
        
        if label:
            self.label = Text(
                label,
                font=F.BODY,
                color=C.WARNING
            ).scale(F.SIZE_CAPTION)
            self.label.next_to(self.icon, DOWN, buff=L.SPACING_TIGHT)
            self.add(self.icon, self.label)
        else:
            self.add(self.icon)
        
        self.move_to(position)
    
    def animate_blink(self, iterations: int = 3) -> Succession:
        """Blinking warning animation"""
        animations = []
        for _ in range(iterations):
            animations.extend([
                self.animate.set_opacity(0.3),
                self.animate.set_opacity(1.0)
            ])
        return Succession(*[a for a in animations], run_time=T.FAST * iterations)
