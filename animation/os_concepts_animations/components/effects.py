"""
Visual Effects for OS Animations
================================

Dramatic effects for contention, conflicts, and state changes.
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import C, T, F, L, A, OS


class ContentionPulse(VGroup):
    """
    Pulsing effect showing high contention.
    """
    
    def __init__(
        self,
        center,
        color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.center = center
        self.color = color or C.CONTENTION_HIGH
        
        # Concentric circles
        self.rings = VGroup()
        for i in range(3):
            ring = Circle(
                radius=0.2 + i * 0.15,
                color=self.color,
                stroke_width=2,
                stroke_opacity=0.8 - i * 0.25,
                fill_opacity=0
            )
            ring.move_to(center)
            self.rings.add(ring)
        
        self.add(self.rings)
    
    def animate_pulse(self, num_pulses: int = 2):
        """Animate contention pulse"""
        animations = []
        for _ in range(num_pulses):
            pulse_anims = []
            for ring in self.rings:
                pulse_anims.append(
                    Succession(
                        ring.animate.scale(1.5).set_opacity(0),
                        ring.animate.scale(1/1.5).set_opacity(0.8)
                    )
                )
            animations.append(AnimationGroup(*pulse_anims))
        
        return Succession(*animations, lag_ratio=0.3)


class ConflictFlash(VGroup):
    """
    Flash effect for conflict detection.
    """
    
    def __init__(
        self,
        target: Mobject,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.target = target
        
        # Lightning bolt icon
        self.bolt = Text(
            OS.CONFLICT_ICON,
            font=F.BODY,
            color=C.CONFLICT
        ).scale(0.5)
        self.bolt.move_to(target.get_center())
        
        # Flash ring
        self.ring = Circle(
            radius=0.5,
            color=C.CONFLICT,
            stroke_width=4,
            fill_opacity=0.2
        )
        self.ring.move_to(target.get_center())
        
        self.add(self.bolt, self.ring)
    
    def animate_flash(self, count: int = None):
        """Animate conflict flash"""
        count = count or A.CONFLICT_FLASH_COUNT
        
        flashes = []
        for _ in range(count):
            flashes.append(
                Succession(
                    AnimationGroup(
                        FadeIn(self.bolt, scale=0.5),
                        self.ring.animate.scale(1.5).set_opacity(0)
                    ),
                    AnimationGroup(
                        FadeOut(self.bolt),
                        self.ring.animate.scale(1/1.5).set_opacity(0.2)
                    )
                )
            )
        
        return Succession(*flashes)


class RollbackWave(VGroup):
    """
    Wave effect for transaction rollback.
    """
    
    def __init__(
        self,
        start_pos,
        end_pos,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.start = start_pos
        self.end = end_pos
        
        # Rollback arrow
        self.arrow = Arrow(
            start_pos,
            end_pos,
            color=C.ROLLBACK,
            stroke_width=3
        )
        
        # "Rollback" label
        self.label = Text(
            "ROLLBACK",
            font=F.CODE,
            color=C.ROLLBACK
        ).scale(F.SIZE_TINY)
        self.label.next_to(self.arrow, UP, buff=L.SPACING_TIGHT)
        
        # Undo icon
        self.icon = Text(
            "↩",
            font=F.BODY,
            color=C.ROLLBACK
        ).scale(0.4)
        self.icon.next_to(self.label, LEFT, buff=L.SPACING_TIGHT)
        
        self.add(self.arrow, self.label, self.icon)
    
    def animate_rollback(self):
        """Animate rollback wave"""
        return Succession(
            Create(self.arrow, run_time=T.ROLLBACK),
            AnimationGroup(
                FadeIn(self.label),
                FadeIn(self.icon)
            ),
            Wait(T.BEAT),
            FadeOut(self)
        )


class LockAcquireEffect(VGroup):
    """
    Effect for successful lock acquisition.
    """
    
    def __init__(
        self,
        lock: Mobject,
        thread_color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.lock = lock
        self.color = thread_color or C.SUCCESS
        
        # Success ring
        self.ring = Circle(
            radius=0.4,
            color=self.color,
            stroke_width=3,
            fill_opacity=0
        )
        self.ring.move_to(lock.get_center())
        
        self.add(self.ring)
    
    def animate_acquire(self):
        """Animate lock acquisition"""
        return Succession(
            self.ring.animate.scale(1.3).set_opacity(0),
            FadeOut(self)
        )


class ValidationCheckmark(VGroup):
    """
    Checkmark for successful validation.
    """
    
    def __init__(
        self,
        position,
        success: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.success = success
        
        if success:
            self.icon = Text(
                OS.SUCCESS_ICON,
                font=F.BODY,
                color=C.VALIDATION_PASS
            ).scale(0.6)
            self.label = Text(
                "VALID",
                font=F.CODE,
                color=C.VALIDATION_PASS
            ).scale(F.SIZE_TINY)
        else:
            self.icon = Text(
                OS.FAIL_ICON,
                font=F.BODY,
                color=C.VALIDATION_FAIL
            ).scale(0.6)
            self.label = Text(
                "CONFLICT",
                font=F.CODE,
                color=C.VALIDATION_FAIL
            ).scale(F.SIZE_TINY)
        
        self.icon.move_to(position)
        self.label.next_to(self.icon, DOWN, buff=L.SPACING_TIGHT)
        
        self.add(self.icon, self.label)
    
    def animate_appear(self):
        """Animate checkmark appearance"""
        return Succession(
            FadeIn(self.icon, scale=0.5),
            FadeIn(self.label)
        )


class BlockedIndicator(VGroup):
    """
    Visual indicator that thread is blocked.
    """
    
    def __init__(
        self,
        thread: Mobject,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.thread = thread
        
        # Blocked icon
        self.icon = Text(
            OS.BLOCKED_ICON,
            font=F.BODY,
            color=C.BLOCKED
        ).scale(0.3)
        self.icon.next_to(thread, UP, buff=L.SPACING_TIGHT)
        
        # "Waiting" label
        self.waiting = Text(
            "waiting...",
            font=F.CODE,
            color=C.BLOCKED
        ).scale(F.SIZE_TINY)
        self.waiting.next_to(self.icon, UP, buff=0.05)
        
        self.add(self.icon, self.waiting)
    
    def animate_show(self):
        """Show blocked state"""
        return FadeIn(self, shift=DOWN * 0.2)
    
    def animate_hide(self):
        """Hide blocked state"""
        return FadeOut(self, shift=UP * 0.2)


class RetryArrow(VGroup):
    """
    Arrow showing retry attempt.
    """
    
    def __init__(
        self,
        start_pos,
        retry_pos,
        attempt: int = 1,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # Curved retry arrow
        self.arrow = CurvedArrow(
            start_pos,
            retry_pos,
            color=C.RETRY,
            angle=-TAU/4
        )
        
        # Attempt label
        self.label = Text(
            f"Retry #{attempt}",
            font=F.CODE,
            color=C.RETRY
        ).scale(F.SIZE_TINY)
        self.label.next_to(self.arrow, UP, buff=L.SPACING_TIGHT)
        
        self.add(self.arrow, self.label)
    
    def animate_retry(self):
        """Animate retry"""
        return Succession(
            Create(self.arrow),
            FadeIn(self.label),
            Wait(T.RETRY_DELAY),
            FadeOut(self)
        )


class DeadlockCycle(VGroup):
    """
    Visual cycle indicating deadlock.
    """
    
    def __init__(
        self,
        positions: list,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.positions = positions
        
        # Cycle arrows
        self.arrows = VGroup()
        for i in range(len(positions)):
            start = positions[i]
            end = positions[(i + 1) % len(positions)]
            
            arrow = Arrow(
                start, end,
                color=C.ERROR,
                stroke_width=3,
                buff=0.3
            )
            self.arrows.add(arrow)
        
        # Deadlock warning
        center = sum(positions) / len(positions)
        self.warning = Text(
            "⚠ DEADLOCK",
            font=F.CODE,
            color=C.ERROR
        ).scale(F.SIZE_LABEL)
        self.warning.move_to(center)
        
        self.add(self.arrows, self.warning)
    
    def animate_show(self):
        """Animate deadlock visualization"""
        return Succession(
            LaggedStart(
                *[Create(arrow) for arrow in self.arrows],
                lag_ratio=0.2
            ),
            FadeIn(self.warning, scale=0.8),
            Flash(self.warning, color=C.ERROR, line_length=0.3)
        )
