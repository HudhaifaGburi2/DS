"""
Database Animation Framework - Base Scene Classes
==================================================

Foundation classes for all database animations.
These classes provide consistent styling, timing, and helper methods
that ensure visual coherence across all chapters.
"""

from manim import *
from config import config, C, T, F, L, A, D


class DatabaseScene(Scene):
    """
    Base class for ALL database animations.
    
    Provides:
    - Consistent background color
    - Standard title card creation
    - Helper methods for common animations
    - Professional wait/timing controls
    """
    
    def setup(self):
        """Initialize scene with standard settings"""
        self.camera.background_color = C.BACKGROUND
        self.default_wait_time = T.PAUSE_MEDIUM
        
        # Track elements for scene management
        self._persistent_elements = []
        self._section_number = 0
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TITLE CARDS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def create_title_card(
        self, 
        main_text_ar: str, 
        main_text_en: str,
        animate_to_corner: bool = True,
        corner: np.ndarray = UL
    ) -> VGroup:
        """
        Create a standard bilingual title card with elegant entrance.
        
        Args:
            main_text_ar: Arabic title (displayed larger)
            main_text_en: English title (displayed smaller)
            animate_to_corner: Whether to move title to corner after display
            corner: Which corner to move to (default UL)
        
        Returns:
            VGroup containing title elements
        """
        # Arabic title - hero text
        title_ar = Text(
            main_text_ar, 
            font=F.ARABIC,
            color=C.TEXT_PRIMARY
        ).scale(F.SIZE_TITLE)
        
        # English subtitle
        title_en = Text(
            main_text_en, 
            font=F.TITLE,
            color=C.TEXT_SECONDARY
        ).scale(F.SIZE_SUBTITLE)
        
        # Arrange vertically
        title_group = VGroup(title_ar, title_en)
        title_group.arrange(DOWN, buff=L.SPACING_MD)
        title_group.move_to(ORIGIN)
        
        # Animate entrance with stagger
        self.play(
            FadeIn(
                title_ar, 
                shift=DOWN * 0.5, 
                scale=A.FADE_IN_SCALE
            ),
            run_time=T.NORMAL
        )
        self.play(
            Write(title_en),
            run_time=T.FAST
        )
        self.wait(T.PAUSE_LONG)
        
        # Move to corner if requested
        if animate_to_corner:
            self.play(
                title_group.animate
                    .scale(0.45)
                    .to_corner(corner, buff=L.MARGIN_MD),
                run_time=T.NORMAL
            )
            self._persistent_elements.append(title_group)
        
        return title_group
    
    def create_section_title(
        self,
        section_num: str,
        title_ar: str,
        title_en: str
    ) -> VGroup:
        """
        Create a section title with number badge.
        
        Args:
            section_num: Section number (e.g., "1.1")
            title_ar: Arabic section title
            title_en: English section title
        """
        # Number badge
        badge = self._create_badge(section_num)
        
        # Titles
        title_ar_text = Text(
            title_ar, 
            font=F.ARABIC,
            color=C.TEXT_PRIMARY
        ).scale(F.SIZE_HEADING)
        
        title_en_text = Text(
            title_en,
            font=F.BODY,
            color=C.TEXT_SECONDARY
        ).scale(F.SIZE_BODY)
        
        # Arrange
        titles = VGroup(title_ar_text, title_en_text)
        titles.arrange(DOWN, buff=L.SPACING_SM)
        
        full_group = VGroup(badge, titles)
        full_group.arrange(RIGHT, buff=L.SPACING_LG)
        
        return full_group
    
    def _create_badge(self, text: str, color=None) -> VGroup:
        """Create a circular badge with text"""
        if color is None:
            color = C.PRIMARY_PURPLE
        
        circle = Circle(
            radius=0.4,
            color=color,
            fill_opacity=0.2,
            stroke_width=2
        )
        label = Text(text, font=F.CODE).scale(F.SIZE_CAPTION)
        label.move_to(circle)
        
        return VGroup(circle, label)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TIMING & FLOW
    # ═══════════════════════════════════════════════════════════════════════════
    
    def wait_beat(self, beats: float = 1.0):
        """Wait for a standard beat (for rhythm)"""
        self.wait(T.PAUSE_SHORT * beats)
    
    def wait_absorb(self, complexity: float = 1.0):
        """Wait for viewer to absorb content (longer pause)"""
        self.wait(T.PAUSE_LONG * complexity)
    
    def dramatic_pause(self):
        """Extra long pause for "aha!" moments"""
        self.wait(T.PAUSE_DRAMATIC)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EMPHASIS ANIMATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def emphasis_pulse(
        self, 
        mobject: Mobject, 
        color=None, 
        scale: float = None,
        iterations: int = None
    ):
        """
        Create an emphasis pulse animation.
        
        Args:
            mobject: Object to emphasize
            color: Highlight color (default: yellow)
            scale: Scale factor for pulse
            iterations: Number of pulse cycles
        """
        if color is None:
            color = C.PRIMARY_YELLOW
        if scale is None:
            scale = A.EMPHASIS_SCALE
        if iterations is None:
            iterations = A.PULSE_ITERATIONS
        
        original_color = mobject.get_color()
        
        for _ in range(iterations):
            self.play(
                mobject.animate.scale(scale).set_color(color),
                run_time=T.QUICK
            )
            self.play(
                mobject.animate.scale(1/scale).set_color(original_color),
                run_time=T.QUICK
            )
    
    def flash_emphasis(self, mobject: Mobject, color=None):
        """Quick flash effect on object"""
        if color is None:
            color = C.PRIMARY_YELLOW
        
        self.play(
            Flash(
                mobject,
                color=color,
                line_length=0.3,
                num_lines=12,
                flash_radius=mobject.width * 0.6
            ),
            run_time=T.FAST
        )
    
    def highlight_box(
        self, 
        mobject: Mobject, 
        color=None,
        buff: float = 0.15
    ) -> SurroundingRectangle:
        """Create and animate a highlight box around object"""
        if color is None:
            color = C.PRIMARY_YELLOW
        
        box = SurroundingRectangle(
            mobject,
            color=color,
            buff=buff,
            corner_radius=0.1,
            stroke_width=2
        )
        self.play(Create(box), run_time=T.FAST)
        return box
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TRANSITIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def smooth_transition(self, *mobjects, lag_ratio: float = 0.15):
        """Elegant entrance for multiple objects with stagger"""
        self.play(
            LaggedStart(
                *[FadeIn(
                    mob, 
                    shift=A.FADE_IN_SHIFT_UP,
                    scale=A.FADE_IN_SCALE
                ) for mob in mobjects],
                lag_ratio=lag_ratio
            ),
            run_time=T.NORMAL
        )
    
    def smooth_exit(self, *mobjects, lag_ratio: float = 0.1):
        """Elegant exit for multiple objects with stagger"""
        self.play(
            LaggedStart(
                *[FadeOut(
                    mob, 
                    shift=A.FADE_IN_SHIFT_DOWN,
                    scale=A.FADE_IN_SCALE
                ) for mob in mobjects],
                lag_ratio=lag_ratio
            ),
            run_time=T.FAST
        )
    
    def crossfade(self, old_mobject: Mobject, new_mobject: Mobject):
        """Smooth crossfade between two objects"""
        new_mobject.move_to(old_mobject)
        self.play(
            FadeOut(old_mobject, scale=0.9),
            FadeIn(new_mobject, scale=1.1),
            run_time=T.NORMAL
        )
    
    def scene_transition(self, direction: str = "fade"):
        """Clear scene with elegant transition"""
        if direction == "fade":
            self.play(
                *[FadeOut(mob) for mob in self.mobjects],
                run_time=T.FAST
            )
        elif direction == "up":
            self.play(
                *[FadeOut(mob, shift=UP) for mob in self.mobjects],
                run_time=T.FAST
            )
        elif direction == "down":
            self.play(
                *[FadeOut(mob, shift=DOWN) for mob in self.mobjects],
                run_time=T.FAST
            )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STEP-BY-STEP LABELS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def show_step_label(
        self, 
        step_num: int, 
        text_ar: str, 
        text_en: str = None,
        position=None,
        previous_label=None
    ) -> VGroup:
        """
        Display a step label with automatic numbering.
        
        Args:
            step_num: Step number
            text_ar: Arabic step description
            text_en: English step description (optional)
            position: Position override
            previous_label: Previous label to fade out
        """
        if position is None:
            position = L.CAPTION_POSITION
        
        # Create step text
        step_text = f"Step {step_num}: {text_ar}"
        label = Text(step_text, font=F.ARABIC, color=C.PRIMARY_YELLOW)
        label.scale(F.SIZE_BODY)
        
        if text_en:
            label_en = Text(text_en, font=F.BODY, color=C.TEXT_SECONDARY)
            label_en.scale(F.SIZE_CAPTION)
            label_group = VGroup(label, label_en).arrange(DOWN, buff=L.SPACING_TIGHT)
        else:
            label_group = label
        
        label_group.move_to(position)
        
        # Animate
        animations = [Write(label_group, run_time=T.FAST)]
        if previous_label is not None:
            animations.append(FadeOut(previous_label))
        
        self.play(*animations)
        return label_group
    
    # ═══════════════════════════════════════════════════════════════════════════
    # UTILITY
    # ═══════════════════════════════════════════════════════════════════════════
    
    def create_bilingual_text(
        self, 
        text_ar: str, 
        text_en: str,
        color_ar=None,
        color_en=None,
        scale_ar: float = None,
        scale_en: float = None
    ) -> VGroup:
        """Create bilingual text pair"""
        if color_ar is None:
            color_ar = C.TEXT_PRIMARY
        if color_en is None:
            color_en = C.TEXT_SECONDARY
        if scale_ar is None:
            scale_ar = F.SIZE_BODY
        if scale_en is None:
            scale_en = F.SIZE_CAPTION
        
        ar = Text(text_ar, font=F.ARABIC, color=color_ar).scale(scale_ar)
        en = Text(text_en, font=F.BODY, color=color_en).scale(scale_en)
        
        return VGroup(ar, en).arrange(DOWN, buff=L.SPACING_TIGHT)


class ConceptScene(DatabaseScene):
    """
    Scene type for explaining single concepts.
    Includes automatic section numbering and progress tracking.
    """
    
    def __init__(
        self, 
        chapter: int = 1, 
        section: int = 1, 
        concept_name_ar: str = "",
        concept_name_en: str = "",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.chapter = chapter
        self.section = section
        self.concept_name_ar = concept_name_ar
        self.concept_name_en = concept_name_en
    
    def setup(self):
        super().setup()
        self.section_marker = None
    
    def show_section_marker(self) -> VGroup:
        """Display section number and name in corner"""
        marker_text = f"{self.chapter}.{self.section}"
        marker = Text(
            marker_text,
            font=F.CODE,
            color=C.TEXT_TERTIARY
        ).scale(F.SIZE_LABEL)
        marker.to_corner(UR, buff=L.MARGIN_SM)
        
        self.play(FadeIn(marker, shift=LEFT * 0.3))
        self.section_marker = marker
        return marker


class ComparisonScene(DatabaseScene):
    """
    Scene type for comparing multiple concepts/approaches.
    Optimized for tables and side-by-side comparisons.
    """
    
    def create_comparison_layout(self, num_items: int) -> list:
        """
        Create evenly spaced positions for comparison items.
        
        Args:
            num_items: Number of items to compare
        
        Returns:
            List of positions
        """
        if num_items == 2:
            return [LEFT * 3, RIGHT * 3]
        elif num_items == 3:
            return [LEFT * 4, ORIGIN, RIGHT * 4]
        elif num_items == 4:
            return [LEFT * 4.5, LEFT * 1.5, RIGHT * 1.5, RIGHT * 4.5]
        else:
            # Evenly distribute
            spacing = 8.0 / (num_items - 1) if num_items > 1 else 0
            start = -4.0
            return [RIGHT * (start + i * spacing) for i in range(num_items)]


class FlowScene(DatabaseScene):
    """
    Scene type for showing processes/flows.
    Optimized for step-by-step progressions.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_step = 0
        self.step_labels = []
    
    def advance_step(
        self, 
        text_ar: str, 
        text_en: str = None
    ) -> VGroup:
        """Advance to next step with automatic numbering"""
        self.current_step += 1
        
        # Fade out previous label if exists
        previous = self.step_labels[-1] if self.step_labels else None
        
        label = self.show_step_label(
            self.current_step,
            text_ar,
            text_en,
            previous_label=previous
        )
        
        self.step_labels.append(label)
        return label
