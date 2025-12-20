"""
Edge Components for Tree Visualizations
=======================================

Provides connection and flow components:
- TreeEdge: Standard parent-child connection
- SplitArrow: Node split visualization
- MergeArrow: Node merge visualization
- FlowArrow: Data flow indicator
"""

from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import C, T, F, L, DS, A


class TreeEdge(VGroup):
    """
    Connection between parent and child nodes.
    
    Visual: Curved or straight line with optional animation.
    """
    
    def __init__(
        self,
        start_pos,
        end_pos,
        color=None,
        stroke_width: float = 2,
        curved: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color or C.BTREE_POINTER
        self.stroke_width = stroke_width
        
        if curved:
            # Bezier curve
            control = (np.array(start_pos) + np.array(end_pos)) / 2
            control[1] = start_pos[1]  # Keep control point at parent level
            
            self.line = CubicBezier(
                start_pos,
                control + LEFT * 0.5,
                control + RIGHT * 0.5,
                end_pos,
                color=self.color,
                stroke_width=self.stroke_width
            )
        else:
            # Straight line
            self.line = Line(
                start_pos,
                end_pos,
                color=self.color,
                stroke_width=self.stroke_width
            )
        
        self.add(self.line)
    
    def animate_create(self):
        """Animation to draw edge"""
        return Create(self.line, run_time=T.FAST)
    
    def animate_highlight(self, color=None):
        """Highlight the edge"""
        color = color or C.BTREE_KEY_ACTIVE
        return self.line.animate.set_color(color).set_stroke(width=4)
    
    def animate_traverse(self, color=None):
        """Show traversal along edge"""
        color = color or C.BTREE_KEY_ACTIVE
        dot = Dot(color=color, radius=0.08)
        dot.move_to(self.start_pos)
        
        return Succession(
            FadeIn(dot, scale=0.5),
            MoveAlongPath(dot, self.line, run_time=T.FAST),
            FadeOut(dot, scale=0.5)
        )


class SplitArrow(VGroup):
    """
    Visual for node split operation.
    
    Shows key moving up and node dividing.
    """
    
    def __init__(
        self,
        origin,
        left_target,
        right_target,
        up_target,
        color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.origin = origin
        self.left_target = left_target
        self.right_target = right_target
        self.up_target = up_target
        self.color = color or C.BTREE_SPLIT
        
        # Arrow going up (median key promotion)
        self.up_arrow = Arrow(
            origin,
            up_target,
            color=self.color,
            stroke_width=A.ARROW_STROKE,
            buff=0.1
        )
        
        # Arrows going left and right (split)
        self.left_arrow = Arrow(
            origin + LEFT * 0.2,
            left_target,
            color=self.color,
            stroke_width=A.ARROW_STROKE,
            buff=0.1
        )
        
        self.right_arrow = Arrow(
            origin + RIGHT * 0.2,
            right_target,
            color=self.color,
            stroke_width=A.ARROW_STROKE,
            buff=0.1
        )
        
        self.add(self.up_arrow, self.left_arrow, self.right_arrow)
    
    def animate_split(self):
        """Animate the split operation"""
        return LaggedStart(
            Create(self.up_arrow),
            AnimationGroup(
                Create(self.left_arrow),
                Create(self.right_arrow)
            ),
            lag_ratio=0.3
        )


class MergeArrow(VGroup):
    """
    Visual for node merge operation.
    
    Shows two nodes combining into one.
    """
    
    def __init__(
        self,
        left_source,
        right_source,
        target,
        color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.left_source = left_source
        self.right_source = right_source
        self.target = target
        self.color = color or C.BTREE_MERGE
        
        # Converging arrows
        self.left_arrow = Arrow(
            left_source,
            target + LEFT * 0.2,
            color=self.color,
            stroke_width=A.ARROW_STROKE,
            buff=0.1
        )
        
        self.right_arrow = Arrow(
            right_source,
            target + RIGHT * 0.2,
            color=self.color,
            stroke_width=A.ARROW_STROKE,
            buff=0.1
        )
        
        self.add(self.left_arrow, self.right_arrow)
    
    def animate_merge(self):
        """Animate the merge operation"""
        return AnimationGroup(
            Create(self.left_arrow),
            Create(self.right_arrow)
        )


class FlowArrow(VGroup):
    """
    Data flow arrow for showing I/O operations.
    
    Visual: Animated arrow with optional pulsing dots.
    """
    
    def __init__(
        self,
        start,
        end,
        color=None,
        label: str = None,
        dashed: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.start = start
        self.end = end
        self.color = color or C.IO_WRITE
        
        # Arrow
        if dashed:
            self.arrow = DashedLine(
                start,
                end,
                color=self.color,
                stroke_width=A.ARROW_STROKE,
                dash_length=A.PATH_DASH_LENGTH
            )
            # Add arrowhead manually
            direction = np.array(end) - np.array(start)
            direction = direction / np.linalg.norm(direction)
            self.arrowhead = Triangle(
                fill_color=self.color,
                fill_opacity=1,
                stroke_width=0
            ).scale(0.1)
            self.arrowhead.rotate(np.arctan2(direction[1], direction[0]) - PI/2)
            self.arrowhead.move_to(end)
            self.add(self.arrowhead)
        else:
            self.arrow = Arrow(
                start,
                end,
                color=self.color,
                stroke_width=A.ARROW_STROKE,
                buff=0.1
            )
        
        self.add(self.arrow)
        
        # Optional label
        if label:
            self.label = Text(label, font=F.CODE, color=self.color).scale(F.SIZE_LABEL)
            mid = (np.array(start) + np.array(end)) / 2
            self.label.next_to(mid, UP, buff=0.1)
            self.add(self.label)
    
    def animate_flow(self, run_time: float = None):
        """Animate data flowing along arrow"""
        run_time = run_time or T.IO_ARROW
        
        dot = Dot(color=self.color, radius=0.06)
        dot.move_to(self.start)
        
        path = Line(self.start, self.end)
        
        return Succession(
            FadeIn(dot, scale=0.5),
            MoveAlongPath(dot, path, run_time=run_time),
            FadeOut(dot, scale=0.5)
        )
    
    def animate_create(self):
        """Create the arrow"""
        return Create(self.arrow)


class IOArrow(VGroup):
    """
    Specialized arrow for read/write I/O visualization.
    
    Distinguishes between sequential and random I/O.
    """
    
    def __init__(
        self,
        start,
        end,
        io_type: str = "read",  # "read", "write"
        pattern: str = "sequential",  # "sequential", "random"
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.io_type = io_type
        self.pattern = pattern
        
        # Color based on type
        if io_type == "read":
            self.color = C.IO_READ
        else:
            self.color = C.IO_WRITE
        
        # Style based on pattern
        stroke_width = A.ARROW_STROKE
        if pattern == "random":
            # Random I/O shown as dashed, thinner
            self.arrow = DashedLine(
                start, end,
                color=self.color,
                stroke_width=stroke_width * 0.7,
                dash_length=0.15
            )
        else:
            # Sequential I/O shown as solid, thicker
            self.arrow = Arrow(
                start, end,
                color=self.color,
                stroke_width=stroke_width * 1.2,
                buff=0.1
            )
        
        self.add(self.arrow)
        
        # Pattern indicator
        indicator_text = "→→" if pattern == "sequential" else "⇢⇠"
        self.indicator = Text(
            indicator_text,
            font=F.CODE,
            color=self.color
        ).scale(F.SIZE_TINY)
        mid = (np.array(start) + np.array(end)) / 2
        self.indicator.next_to(mid, UP, buff=0.05)
        self.add(self.indicator)
