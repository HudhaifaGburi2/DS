"""
Data Structure Animations - Base Scene Classes
===============================================

Provides foundational scene classes for all data structure animations:
- DataStructureScene: Base for all scenes
- TreeScene: Specialized for tree-based structures
- ComparisonScene: Side-by-side comparisons

Each scene enforces visual consistency, timing standards, and narrative flow.
"""

from manim import *
from config import C, T, F, L, DS, A, PHI


class DataStructureScene(Scene):
    """
    Base scene for all data structure animations.
    
    Provides:
    - Consistent background and styling
    - Title card creation
    - Timing helpers
    - Standard transitions
    """
    
    def setup(self):
        """Initialize scene with standard configuration"""
        self.camera.background_color = C.BACKGROUND
    
    # ══════════════════════════════════════════════════════════════════════════
    # TITLE CARDS
    # ══════════════════════════════════════════════════════════════════════════
    
    def create_title_card(
        self,
        title_ar: str,
        title_en: str,
        fade_out: bool = True
    ) -> VGroup:
        """Create bilingual title card with cinematic reveal"""
        
        title_arabic = Text(
            title_ar,
            font=F.ARABIC,
            color=C.TEXT_PRIMARY
        ).scale(F.SIZE_TITLE)
        
        title_english = Text(
            title_en,
            font=F.BODY,
            color=C.TEXT_SECONDARY
        ).scale(F.SIZE_CAPTION)
        
        title_group = VGroup(title_arabic, title_english)
        title_group.arrange(DOWN, buff=L.SPACING_MD)
        
        # Animate in
        self.play(
            FadeIn(title_arabic, shift=DOWN * 0.3),
            run_time=T.SLOW
        )
        self.play(
            FadeIn(title_english, shift=UP * 0.2),
            run_time=T.FAST
        )
        
        self.wait(T.ABSORB)
        
        if fade_out:
            self.play(FadeOut(title_group), run_time=T.FAST)
        
        return title_group
    
    def create_section_header(
        self,
        text: str,
        color=None,
        position=UP * 3
    ) -> Text:
        """Create a section header"""
        color = color or C.TEXT_ACCENT
        header = Text(text, font=F.BODY, color=color).scale(F.SIZE_HEADING)
        header.move_to(position)
        return header
    
    # ══════════════════════════════════════════════════════════════════════════
    # TIMING HELPERS
    # ══════════════════════════════════════════════════════════════════════════
    
    def wait_beat(self, multiplier: float = 1.0):
        """Quick rhythmic pause"""
        self.wait(T.BEAT * multiplier)
    
    def wait_breath(self):
        """Short natural pause"""
        self.wait(T.BREATH)
    
    def wait_absorb(self, multiplier: float = 1.0):
        """Pause for content absorption"""
        self.wait(T.ABSORB * multiplier)
    
    def wait_contemplate(self):
        """Longer pause for deeper understanding"""
        self.wait(T.CONTEMPLATE)
    
    def dramatic_pause(self):
        """Dramatic pause before big reveal"""
        self.wait(T.DRAMATIC)
    
    # ══════════════════════════════════════════════════════════════════════════
    # TRANSITIONS
    # ══════════════════════════════════════════════════════════════════════════
    
    def fade_all_out(self, run_time: float = None):
        """Fade out all mobjects"""
        run_time = run_time or T.FAST
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=run_time)
    
    def scene_transition(self):
        """Standard transition between major sections"""
        self.fade_all_out()
        self.wait(T.BEAT)
    
    # ══════════════════════════════════════════════════════════════════════════
    # EMPHASIS ANIMATIONS
    # ══════════════════════════════════════════════════════════════════════════
    
    def emphasize(self, mobject: Mobject, scale: float = 1.1):
        """Pulse emphasis on a mobject"""
        self.play(
            mobject.animate.scale(scale),
            run_time=T.QUICK
        )
        self.play(
            mobject.animate.scale(1 / scale),
            run_time=T.QUICK
        )
    
    def highlight_flash(self, mobject: Mobject, color=None):
        """Quick flash highlight"""
        color = color or C.TEXT_ACCENT
        self.play(
            Flash(mobject, color=color, line_length=0.3),
            run_time=T.FAST
        )
    
    # ══════════════════════════════════════════════════════════════════════════
    # UTILITY METHODS
    # ══════════════════════════════════════════════════════════════════════════
    
    def create_label(
        self,
        text: str,
        color=None,
        scale: float = None
    ) -> Text:
        """Create a standard label"""
        color = color or C.TEXT_PRIMARY
        scale = scale or F.SIZE_LABEL
        return Text(text, font=F.BODY, color=color).scale(scale)
    
    def create_code_label(
        self,
        text: str,
        color=None,
        scale: float = None
    ) -> Text:
        """Create a code/monospace label"""
        color = color or C.TEXT_PRIMARY
        scale = scale or F.SIZE_KEY
        return Text(text, font=F.CODE, color=color).scale(scale)


class TreeScene(DataStructureScene):
    """
    Specialized scene for tree-based data structure animations.
    
    Provides:
    - Tree layout management
    - Node positioning helpers
    - Level-based animations
    - Rebalancing hooks
    """
    
    def setup(self):
        super().setup()
        self.tree_root = None
        self.tree_nodes = {}
        self.tree_edges = {}
    
    # ══════════════════════════════════════════════════════════════════════════
    # TREE LAYOUT
    # ══════════════════════════════════════════════════════════════════════════
    
    def calculate_node_positions(
        self,
        root,
        start_pos=ORIGIN + UP * 2,
        level_height: float = None,
        horizontal_spacing: float = None
    ) -> dict:
        """
        Calculate positions for all nodes in a tree.
        Returns dict mapping node_id -> position
        """
        level_height = level_height or L.TREE_LEVEL_HEIGHT
        horizontal_spacing = horizontal_spacing or L.TREE_NODE_SPACING
        
        positions = {}
        
        def traverse(node, level, left_bound, right_bound):
            if node is None:
                return
            
            x = (left_bound + right_bound) / 2
            y = start_pos[1] - level * level_height
            positions[id(node)] = np.array([x, y, 0])
            
            if hasattr(node, 'children') and node.children:
                num_children = len(node.children)
                width = right_bound - left_bound
                child_width = width / num_children
                
                for i, child in enumerate(node.children):
                    child_left = left_bound + i * child_width
                    child_right = child_left + child_width
                    traverse(child, level + 1, child_left, child_right)
        
        traverse(root, 0, -L.TREE_MAX_WIDTH / 2, L.TREE_MAX_WIDTH / 2)
        return positions
    
    def get_level_nodes(self, level: int) -> list:
        """Get all nodes at a specific level"""
        return [
            node for node_id, node in self.tree_nodes.items()
            if node.level == level
        ]
    
    def animate_level(self, level: int, animation_func, **kwargs):
        """Apply animation to all nodes at a level"""
        nodes = self.get_level_nodes(level)
        if nodes:
            self.play(
                LaggedStart(
                    *[animation_func(node, **kwargs) for node in nodes],
                    lag_ratio=A.LAG_NORMAL
                )
            )
    
    # ══════════════════════════════════════════════════════════════════════════
    # TREE OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════
    
    def animate_search_path(
        self,
        path: list,
        highlight_color=None
    ):
        """Animate traversing a search path"""
        highlight_color = highlight_color or C.BTREE_KEY_ACTIVE
        
        for node in path:
            self.play(
                node.animate.set_stroke(color=highlight_color, width=3),
                run_time=T.KEY_SEARCH
            )
            self.wait_beat(0.5)
    
    def animate_insert_path(
        self,
        path: list,
        key_value
    ):
        """Animate insertion traversal"""
        for node in path:
            self.emphasize(node)
            self.wait_beat(0.3)


class ComparisonScene(DataStructureScene):
    """
    Scene for side-by-side data structure comparisons.
    
    Provides:
    - Split-screen layout
    - Synchronized animations
    - Metric overlays
    - Winner highlighting
    """
    
    def setup(self):
        super().setup()
        self.left_group = VGroup()
        self.right_group = VGroup()
        self.divider = None
    
    # ══════════════════════════════════════════════════════════════════════════
    # SPLIT SCREEN LAYOUT
    # ══════════════════════════════════════════════════════════════════════════
    
    def create_split_screen(
        self,
        left_title: str,
        right_title: str,
        left_color=None,
        right_color=None
    ):
        """Create split-screen comparison layout"""
        left_color = left_color or C.COMPARE_A
        right_color = right_color or C.COMPARE_B
        
        # Divider line
        self.divider = Line(
            UP * 3.5, DOWN * 3.5,
            color=C.TEXT_TERTIARY,
            stroke_width=1
        )
        
        # Left title
        left_label = Text(
            left_title,
            font=F.BODY,
            color=left_color
        ).scale(F.SIZE_HEADING)
        left_label.move_to(LEFT * L.COMPARE_LEFT_CENTER + UP * 3)
        
        # Right title
        right_label = Text(
            right_title,
            font=F.BODY,
            color=right_color
        ).scale(F.SIZE_HEADING)
        right_label.move_to(RIGHT * L.COMPARE_RIGHT_CENTER + UP * 3)
        
        self.play(
            Create(self.divider),
            FadeIn(left_label, shift=RIGHT * 0.3),
            FadeIn(right_label, shift=LEFT * 0.3),
            run_time=T.NORMAL
        )
        
        self.left_group.add(left_label)
        self.right_group.add(right_label)
        
        return left_label, right_label
    
    def add_to_left(self, mobject: Mobject, position=None):
        """Add mobject to left side"""
        if position is None:
            position = LEFT * L.COMPARE_LEFT_CENTER
        mobject.move_to(position)
        self.left_group.add(mobject)
        return mobject
    
    def add_to_right(self, mobject: Mobject, position=None):
        """Add mobject to right side"""
        if position is None:
            position = RIGHT * L.COMPARE_RIGHT_CENTER
        mobject.move_to(position)
        self.right_group.add(mobject)
        return mobject
    
    # ══════════════════════════════════════════════════════════════════════════
    # SYNCHRONIZED ANIMATIONS
    # ══════════════════════════════════════════════════════════════════════════
    
    def sync_animate(
        self,
        left_animation,
        right_animation,
        run_time: float = None
    ):
        """Run animations on both sides simultaneously"""
        run_time = run_time or T.NORMAL
        self.play(left_animation, right_animation, run_time=run_time)
    
    def stagger_animate(
        self,
        left_animation,
        right_animation,
        delay: float = None
    ):
        """Run left animation, then right with delay"""
        delay = delay or T.BEAT
        self.play(left_animation)
        self.wait(delay)
        self.play(right_animation)
    
    # ══════════════════════════════════════════════════════════════════════════
    # METRICS & COMPARISON
    # ══════════════════════════════════════════════════════════════════════════
    
    def create_metric_bar(
        self,
        label: str,
        left_value: float,
        right_value: float,
        position,
        max_width: float = 2.0,
        left_color=None,
        right_color=None
    ) -> VGroup:
        """Create comparison metric bars"""
        left_color = left_color or C.COMPARE_A
        right_color = right_color or C.COMPARE_B
        
        max_val = max(left_value, right_value, 1)
        
        # Label
        label_text = Text(label, font=F.BODY, color=C.TEXT_SECONDARY)
        label_text.scale(F.SIZE_LABEL)
        label_text.move_to(position)
        
        # Left bar
        left_width = (left_value / max_val) * max_width
        left_bar = Rectangle(
            width=left_width,
            height=0.25,
            fill_color=left_color,
            fill_opacity=0.8,
            stroke_width=0
        )
        left_bar.next_to(label_text, LEFT, buff=L.SPACING_SM)
        left_bar.align_to(label_text, RIGHT)
        left_bar.shift(LEFT * max_width)
        
        # Right bar
        right_width = (right_value / max_val) * max_width
        right_bar = Rectangle(
            width=right_width,
            height=0.25,
            fill_color=right_color,
            fill_opacity=0.8,
            stroke_width=0
        )
        right_bar.next_to(label_text, RIGHT, buff=L.SPACING_SM)
        
        return VGroup(label_text, left_bar, right_bar)
    
    def highlight_winner(
        self,
        winner: str,
        left_mobject: Mobject,
        right_mobject: Mobject
    ):
        """Highlight the winning side"""
        if winner == "left":
            self.play(
                left_mobject.animate.set_color(C.COMPARE_WINNER),
                right_mobject.animate.set_color(C.COMPARE_LOSER),
                run_time=T.FAST
            )
        else:
            self.play(
                left_mobject.animate.set_color(C.COMPARE_LOSER),
                right_mobject.animate.set_color(C.COMPARE_WINNER),
                run_time=T.FAST
            )
    
    # ══════════════════════════════════════════════════════════════════════════
    # VERDICT
    # ══════════════════════════════════════════════════════════════════════════
    
    def show_verdict(
        self,
        text_ar: str,
        text_en: str,
        color=None
    ):
        """Show final verdict/conclusion"""
        color = color or C.SUCCESS
        
        verdict_ar = Text(text_ar, font=F.ARABIC, color=color).scale(F.SIZE_BODY)
        verdict_en = Text(text_en, font=F.BODY, color=C.TEXT_SECONDARY).scale(F.SIZE_CAPTION)
        
        verdict = VGroup(verdict_ar, verdict_en).arrange(DOWN, buff=L.SPACING_SM)
        verdict.to_edge(DOWN, buff=L.MARGIN_LG)
        
        self.play(FadeIn(verdict, shift=UP * 0.3))
        self.wait_absorb()
        
        return verdict
