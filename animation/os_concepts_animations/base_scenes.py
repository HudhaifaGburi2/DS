"""
OS Concepts Base Scene Classes
==============================

Foundational scene types for OS animations:
- OSScene: Global OS look & feel
- ConcurrencyScene: Thread lanes, shared resources
- TimelineScene: Time-based reasoning for MVCC
"""

from manim import *
from config import C, T, F, L, A, OS


class OSScene(Scene):
    """
    Base scene for all OS concept animations.
    
    Provides:
    - Consistent background and styling
    - Title card creation
    - Standard transitions
    - Timing helpers
    """
    
    def setup(self):
        self.camera.background_color = C.BACKGROUND
    
    def create_title_card(
        self,
        title_ar: str,
        title_en: str,
        subtitle: str = None
    ):
        """Create animated title card"""
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
        
        titles = VGroup(title_arabic, title_english)
        titles.arrange(DOWN, buff=L.SPACING_SM)
        
        if subtitle:
            sub = Text(
                subtitle,
                font=F.CODE,
                color=C.TEXT_TERTIARY
            ).scale(F.SIZE_LABEL)
            titles.add(sub)
            titles.arrange(DOWN, buff=L.SPACING_SM)
        
        self.play(FadeIn(titles, scale=0.9), run_time=T.SLOW)
        self.wait(T.ABSORB)
        self.play(FadeOut(titles), run_time=T.FAST)
        self.wait(T.BEAT)
    
    def create_section_header(self, text: str, color=None) -> Text:
        """Create section header"""
        color = color or C.TEXT_ACCENT
        header = Text(text, font=F.BODY, color=color).scale(F.SIZE_HEADING)
        header.to_edge(UP, buff=L.MARGIN_MD)
        return header
    
    def scene_transition(self):
        """Standard scene transition"""
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=T.FAST
        )
        self.wait(T.BEAT)
    
    def wait_beat(self, multiplier: float = 1.0):
        """Short rhythmic pause"""
        self.wait(T.BEAT * multiplier)
    
    def wait_absorb(self):
        """Pause for information absorption"""
        self.wait(T.ABSORB)
    
    def wait_contemplate(self):
        """Long pause for major concepts"""
        self.wait(T.CONTEMPLATE)


class ConcurrencyScene(OSScene):
    """
    Scene for concurrency and synchronization animations.
    
    Provides:
    - Thread lane management
    - Shared resource visualization
    - Lock state tracking
    - Contention detection
    """
    
    def setup(self):
        super().setup()
        self.threads = {}
        self.locks = {}
        self.critical_sections = {}
        self.thread_lanes = VGroup()
    
    def create_thread_lanes(
        self,
        num_threads: int = None,
        start_y: float = 2.0
    ) -> VGroup:
        """Create parallel thread execution lanes"""
        num_threads = num_threads or OS.DEFAULT_THREADS
        
        lanes = VGroup()
        for i in range(num_threads):
            y_pos = start_y - i * (L.THREAD_LANE_HEIGHT + L.THREAD_LANE_SPACING)
            
            # Lane background
            lane_bg = Rectangle(
                width=12,
                height=L.THREAD_LANE_HEIGHT,
                fill_color=C.BACKGROUND_ALT,
                fill_opacity=0.3,
                stroke_width=0
            )
            lane_bg.move_to(UP * y_pos)
            
            # Thread label
            thread_color = C.THREAD_COLORS[i % len(C.THREAD_COLORS)]
            label = Text(
                f"T{i+1}",
                font=F.CODE,
                color=thread_color
            ).scale(F.SIZE_THREAD_ID)
            label.move_to(LEFT * 6 + UP * y_pos)
            
            lane = VGroup(lane_bg, label)
            lane.thread_id = i + 1
            lane.color = thread_color
            lane.y_pos = y_pos
            lanes.add(lane)
        
        self.thread_lanes = lanes
        return lanes
    
    def create_critical_section(
        self,
        label: str = "Critical Section",
        width: float = None,
        height: float = None,
        position = ORIGIN
    ) -> VGroup:
        """Create visual critical section"""
        width = width or L.CRITICAL_WIDTH
        height = height or L.CRITICAL_HEIGHT
        
        # Danger zone background
        section_bg = Rectangle(
            width=width,
            height=height,
            fill_color=C.CRITICAL_SECTION,
            fill_opacity=0.15,
            stroke_color=C.CRITICAL_SECTION,
            stroke_width=2,
            corner_radius=0.1
        )
        section_bg.move_to(position)
        
        # Label
        section_label = Text(
            label,
            font=F.CODE,
            color=C.CRITICAL_SECTION
        ).scale(F.SIZE_LABEL)
        section_label.next_to(section_bg, UP, buff=L.SPACING_TIGHT)
        
        section = VGroup(section_bg, section_label)
        section.background = section_bg
        section.label = section_label
        
        return section
    
    def animate_thread_enter_critical(
        self,
        thread_mob: Mobject,
        section: VGroup
    ):
        """Animate thread entering critical section"""
        return Succession(
            thread_mob.animate.move_to(section.background.get_center()),
            section.background.animate.set_fill(color=C.LOCK_HELD, opacity=0.25)
        )
    
    def animate_thread_exit_critical(
        self,
        thread_mob: Mobject,
        exit_pos,
        section: VGroup
    ):
        """Animate thread exiting critical section"""
        return Succession(
            thread_mob.animate.move_to(exit_pos),
            section.background.animate.set_fill(color=C.CRITICAL_SECTION, opacity=0.15)
        )
    
    def create_contention_indicator(self, position) -> VGroup:
        """Create visual contention indicator"""
        indicator = VGroup()
        
        for i in range(A.CONTENTION_PARTICLES):
            angle = i * TAU / A.CONTENTION_PARTICLES
            dot = Dot(
                point=position + 0.3 * np.array([np.cos(angle), np.sin(angle), 0]),
                color=C.CONTENTION_HIGH,
                radius=0.05
            )
            indicator.add(dot)
        
        return indicator
    
    def animate_contention(self, position, run_time: float = None):
        """Animate contention effect"""
        run_time = run_time or T.CONFLICT_FLASH
        indicator = self.create_contention_indicator(position)
        
        return Succession(
            FadeIn(indicator, scale=0.5),
            indicator.animate.scale(1.5).set_opacity(0),
            FadeOut(indicator)
        )


class TimelineScene(OSScene):
    """
    Scene for time-based animations (MVCC, scheduling).
    
    Provides:
    - Time axis creation
    - Version timeline management
    - Snapshot visualization
    - Temporal reasoning
    """
    
    def setup(self):
        super().setup()
        self.time_axis = None
        self.versions = {}
        self.snapshots = {}
    
    def create_time_axis(
        self,
        start_x: float = -5.5,
        end_x: float = 5.5,
        y_pos: float = -2.5,
        show_labels: bool = True
    ) -> VGroup:
        """Create horizontal time axis"""
        # Main axis line
        axis_line = Arrow(
            start=LEFT * abs(start_x) + UP * y_pos,
            end=RIGHT * abs(end_x) + UP * y_pos,
            color=C.TIME_AXIS,
            stroke_width=A.TIMELINE_STROKE,
            buff=0
        )
        
        # Time label
        time_label = Text("Time →", font=F.CODE, color=C.TIME_AXIS).scale(F.SIZE_TINY)
        time_label.next_to(axis_line, RIGHT, buff=L.SPACING_TIGHT)
        
        axis = VGroup(axis_line, time_label)
        
        if show_labels:
            # Add tick marks
            ticks = VGroup()
            for i, x in enumerate(np.arange(start_x + 1, end_x, L.TIMELINE_TICK_SPACING)):
                tick = Line(
                    UP * 0.1 + RIGHT * x + UP * y_pos,
                    DOWN * 0.1 + RIGHT * x + UP * y_pos,
                    color=C.TIME_AXIS,
                    stroke_width=1
                )
                tick_label = Text(f"t{i}", font=F.CODE, color=C.TIME_TERTIARY).scale(F.SIZE_TINY)
                tick_label.next_to(tick, DOWN, buff=0.05)
                ticks.add(VGroup(tick, tick_label))
            
            axis.add(ticks)
        
        self.time_axis = axis
        return axis
    
    def create_version_timeline(
        self,
        object_name: str,
        y_pos: float,
        color=None
    ) -> VGroup:
        """Create timeline for object versions"""
        color = color or C.SHARED_RESOURCE
        
        # Object label
        label = Text(object_name, font=F.CODE, color=color).scale(F.SIZE_LABEL)
        label.move_to(LEFT * 6 + UP * y_pos)
        
        # Version line
        line = Line(
            LEFT * 5 + UP * y_pos,
            RIGHT * 5 + UP * y_pos,
            color=color,
            stroke_width=1,
            stroke_opacity=0.5
        )
        
        timeline = VGroup(label, line)
        timeline.object_name = object_name
        timeline.y_pos = y_pos
        timeline.versions = VGroup()
        
        return timeline
    
    def create_version_marker(
        self,
        timeline: VGroup,
        x_pos: float,
        version_id: str,
        state: str = "current"
    ) -> VGroup:
        """Create version marker on timeline"""
        if state == "current":
            color = C.VERSION_CURRENT
        elif state == "new":
            color = C.VERSION_NEW
        elif state == "old":
            color = C.VERSION_OLD
        else:
            color = C.GARBAGE
        
        # Version box
        box = RoundedRectangle(
            width=0.6,
            height=L.VERSION_HEIGHT,
            color=color,
            fill_opacity=0.3,
            stroke_width=2,
            corner_radius=0.08
        )
        box.move_to(RIGHT * x_pos + UP * timeline.y_pos)
        
        # Version label
        label = Text(version_id, font=F.CODE, color=color).scale(F.SIZE_TINY)
        label.move_to(box.get_center())
        
        marker = VGroup(box, label)
        marker.version_id = version_id
        marker.state = state
        
        return marker
    
    def create_snapshot_read(
        self,
        reader_name: str,
        timeline: VGroup,
        x_pos: float
    ) -> VGroup:
        """Create snapshot read indicator"""
        # Reader marker
        reader = Text(reader_name, font=F.CODE, color=C.SNAPSHOT).scale(F.SIZE_TINY)
        reader.move_to(RIGHT * x_pos + UP * (timeline.y_pos + 0.6))
        
        # Pin line to timeline
        pin_line = DashedLine(
            reader.get_bottom(),
            RIGHT * x_pos + UP * timeline.y_pos,
            color=C.SNAPSHOT,
            stroke_width=1
        )
        
        snapshot = VGroup(reader, pin_line)
        return snapshot
    
    def animate_time_progress(
        self,
        start_x: float,
        end_x: float,
        y_pos: float = -2.5,
        run_time: float = None
    ):
        """Animate time progression marker"""
        run_time = run_time or T.SLOW
        
        marker = Triangle(
            color=C.TIME_NOW,
            fill_opacity=1
        ).scale(0.15)
        marker.rotate(-PI/2)
        marker.move_to(RIGHT * start_x + UP * (y_pos + 0.2))
        
        return Succession(
            FadeIn(marker),
            marker.animate.move_to(RIGHT * end_x + UP * (y_pos + 0.2)),
            run_time=run_time
        )
    
    def animate_garbage_collection(
        self,
        versions: list,
        run_time: float = None
    ):
        """Animate garbage collection of old versions"""
        run_time = run_time or T.GARBAGE_COLLECT
        
        animations = []
        for version in versions:
            animations.append(
                version.animate.set_opacity(0.2).set_color(C.GARBAGE)
            )
        
        return AnimationGroup(*animations, lag_ratio=0.1, run_time=run_time)


class ComparisonScene(OSScene):
    """
    Scene for side-by-side comparisons.
    
    Used for comparing synchronization strategies.
    """
    
    def create_split_screen(
        self,
        left_title: str,
        right_title: str,
        left_color=None,
        right_color=None
    ) -> tuple:
        """Create split-screen comparison layout"""
        left_color = left_color or C.THREAD_1
        right_color = right_color or C.THREAD_2
        
        # Divider
        divider = DashedLine(
            UP * 3.5,
            DOWN * 3.5,
            color=C.TEXT_TERTIARY,
            stroke_width=1
        )
        
        # Titles
        left_text = Text(left_title, font=F.BODY, color=left_color).scale(F.SIZE_HEADING)
        left_text.move_to(LEFT * L.COMPARE_LEFT_CENTER + UP * 3)
        
        right_text = Text(right_title, font=F.BODY, color=right_color).scale(F.SIZE_HEADING)
        right_text.move_to(RIGHT * L.COMPARE_RIGHT_CENTER + UP * 3)
        
        self.play(
            Create(divider),
            Write(left_text),
            Write(right_text)
        )
        
        return left_text, right_text
    
    def sync_animate(self, left_anim, right_anim, run_time: float = None):
        """Play synchronized animations on both sides"""
        run_time = run_time or T.NORMAL
        self.play(
            left_anim,
            right_anim,
            run_time=run_time
        )
