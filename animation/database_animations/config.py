"""
Database Animation Framework - Master Configuration
====================================================

Centralized configuration for ALL chapters in the database textbook series.
This module defines visual standards, timing, colors, and mathematical constants
that ensure consistency across the entire animation collection.

Golden Ratio: φ = 1.618 is used throughout for harmonious proportions.
"""

from manim import *
import numpy as np


class DBConfig:
    """
    Master configuration class for database animation series.
    All visual and timing parameters are centralized here.
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MATHEMATICAL CONSTANTS
    # ═══════════════════════════════════════════════════════════════════════════
    
    PHI = 1.618033988749895  # Golden ratio
    PHI_INVERSE = 0.618033988749895  # 1/φ
    PHI_SQUARED = 2.618033988749895  # φ²
    
    FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    
    # Golden ratio based scale factors
    SCALE_XS = PHI_INVERSE ** 3  # 0.236
    SCALE_SM = PHI_INVERSE ** 2  # 0.382
    SCALE_MD = PHI_INVERSE       # 0.618
    SCALE_LG = 1.0               # 1.000
    SCALE_XL = PHI               # 1.618
    SCALE_XXL = PHI_SQUARED      # 2.618
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TIMING STANDARDS
    # ═══════════════════════════════════════════════════════════════════════════
    
    class Timing:
        """Animation timing based on golden ratio intervals"""
        
        # Core durations (φ-based)
        INSTANT = 0.236      # φ⁻³ - Snap changes
        QUICK = 0.382        # φ⁻² - Fast reveals
        FAST = 0.618         # φ⁻¹ - Quick transitions
        NORMAL = 1.0         # Standard timing
        SLOW = 1.618         # φ   - Deliberate reveals
        DRAMATIC = 2.618     # φ²  - Big moments
        
        # Pause durations
        PAUSE_MICRO = 0.3    # Brief acknowledgment
        PAUSE_SHORT = 0.5    # Quick beat
        PAUSE_MEDIUM = 1.0   # Standard pause
        PAUSE_LONG = 2.0     # Absorption time
        PAUSE_DRAMATIC = 3.0 # "Aha!" moments
        
        # Stagger timing for sequences
        STAGGER_FAST = 0.1
        STAGGER_NORMAL = 0.2
        STAGGER_SLOW = 0.382
        
        # Text timing
        CHAR_WRITE_RATE = 0.05   # Per character
        WORD_WRITE_RATE = 0.1    # Per word
        LINE_WRITE_RATE = 0.3    # Per line
    
    # ═══════════════════════════════════════════════════════════════════════════
    # COLOR PALETTE
    # ═══════════════════════════════════════════════════════════════════════════
    
    class Colors:
        """
        Semantic color system for database animations.
        Colors convey meaning - use consistently!
        """
        
        # Background
        BACKGROUND = "#0d1117"       # Deep dark blue-black
        BACKGROUND_ALT = "#161b22"   # Slightly lighter
        
        # ── Primary Palette ──
        PRIMARY_BLUE = "#58C4DD"     # Manim blue - original/source
        PRIMARY_GREEN = "#83C167"    # Success/new/valid
        PRIMARY_YELLOW = "#FFFF00"   # Attention/process/highlight
        PRIMARY_RED = "#FF6B6B"      # Danger/error/critical
        PRIMARY_PURPLE = "#9A72AC"   # Atomicity/special
        PRIMARY_ORANGE = "#FFAA00"   # Warning/transition
        
        # ── Semantic Colors ──
        # Status
        SUCCESS = "#4CAF50"          # Complete/valid
        SUCCESS_LIGHT = "#83C167"    # Soft success
        WARNING = "#FFC107"          # Caution
        ERROR = "#F44336"            # Critical failure
        ERROR_SOFT = "#FF6B6B"       # Soft error
        INFO = "#2196F3"             # Information
        
        # File states
        FILE_ORIGINAL = "#58C4DD"    # Original file (blue)
        FILE_NEW = "#83C167"         # New/temp file (green)
        FILE_TEMP = "#FFAA00"        # Temporary (orange)
        FILE_CORRUPT = "#FF6B6B"     # Corrupted (red)
        FILE_EMPTY = "#666666"       # Empty/truncated (gray)
        
        # Data flow
        DATA_COLD = "#58C4DD"        # Data at rest
        DATA_HOT = "#FF6B6B"         # Data in motion/danger
        DATA_SAFE = "#83C167"        # Data secured
        
        # Layers (storage hierarchy)
        LAYER_APP = "#58C4DD"        # Application layer
        LAYER_OS = "#FFAA00"         # OS/Page cache
        LAYER_DEVICE = "#FF8C00"     # Device RAM
        LAYER_DISK = "#83C167"       # Persistent storage
        
        # ── Text Colors ──
        TEXT_PRIMARY = "#ECECEC"     # Main text (high contrast)
        TEXT_SECONDARY = "#8B949E"   # Secondary (medium contrast)
        TEXT_TERTIARY = "#484F58"    # Subtle (low contrast)
        TEXT_CODE = "#A8E6CF"        # Code text
        TEXT_ARABIC = "#FFFFFF"      # Arabic text (high contrast)
        
        # ── Accent Colors ──
        ACCENT_CYAN = "#79C0FF"      # Highlights
        ACCENT_PINK = "#FF7B72"      # Special emphasis
        ACCENT_GOLD = "#FFD700"      # Achievement/success
        
        # ── Chapter-specific accents ──
        CHAPTER_01_ACCENT = "#9A72AC"  # Purple for atomicity concepts
        CHAPTER_02_ACCENT = "#58C4DD"  # Blue for data structures
        CHAPTER_03_ACCENT = "#83C167"  # Green for transactions
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TYPOGRAPHY
    # ═══════════════════════════════════════════════════════════════════════════
    
    class Fonts:
        """Font specifications for consistent typography"""
        
        # Font families (with fallbacks)
        TITLE = "SF Pro Display"
        BODY = "SF Pro Text"
        CODE = "SF Mono"
        ARABIC = "Arial"          # Best Arabic support
        EMOJI = "Apple Color Emoji"
        
        # Fallback chain for Linux
        TITLE_FALLBACK = "DejaVu Sans"
        CODE_FALLBACK = "DejaVu Sans Mono"
        
        # Scale factors (relative to base)
        SIZE_HERO = 1.5           # Big hero text
        SIZE_TITLE = 1.2          # Main titles
        SIZE_HEADING = 0.9        # Section headings
        SIZE_SUBTITLE = 0.6       # Subtitles
        SIZE_BODY = 0.5           # Body text
        SIZE_CODE = 0.45          # Code blocks
        SIZE_CAPTION = 0.4        # Captions
        SIZE_LABEL = 0.35         # Small labels
        SIZE_TINY = 0.3           # Smallest text
        
        # Line heights
        LINE_HEIGHT_TIGHT = 1.0
        LINE_HEIGHT_NORMAL = 1.4
        LINE_HEIGHT_LOOSE = 1.8
    
    # ═══════════════════════════════════════════════════════════════════════════
    # LAYOUT STANDARDS
    # ═══════════════════════════════════════════════════════════════════════════
    
    class Layout:
        """Positioning and spacing constants"""
        
        # Screen regions (based on 14.2 x 8 Manim frame)
        TITLE_POSITION = UP * 3.2
        SUBTITLE_POSITION = UP * 2.6
        CONTENT_TOP = UP * 2.0
        CONTENT_CENTER = ORIGIN
        CONTENT_BOTTOM = DOWN * 2.0
        CODE_POSITION = DOWN * 2.5
        CAPTION_POSITION = DOWN * 3.2
        
        # Corners with margin
        CORNER_UL = UL * 0.9
        CORNER_UR = UR * 0.9
        CORNER_DL = DL * 0.9
        CORNER_DR = DR * 0.9
        
        # Margins (φ-based)
        MARGIN_XS = 0.2
        MARGIN_SM = 0.382
        MARGIN_MD = 0.618
        MARGIN_LG = 1.0
        MARGIN_XL = 1.618
        
        # Spacing (φ-based)
        SPACING_TIGHT = 0.1
        SPACING_SM = 0.2
        SPACING_MD = 0.382
        SPACING_LG = 0.618
        SPACING_XL = 1.0
        
        # Grid system (3x3)
        GRID_LEFT = LEFT * 4
        GRID_RIGHT = RIGHT * 4
        GRID_TOP = UP * 2.5
        GRID_BOTTOM = DOWN * 2.5
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ANIMATION PARAMETERS
    # ═══════════════════════════════════════════════════════════════════════════
    
    class Animations:
        """Animation style parameters"""
        
        # Fade parameters
        FADE_IN_SCALE = 0.85
        FADE_IN_SHIFT_UP = UP * 0.3
        FADE_IN_SHIFT_DOWN = DOWN * 0.3
        FADE_IN_SHIFT_LEFT = LEFT * 0.3
        FADE_IN_SHIFT_RIGHT = RIGHT * 0.3
        
        # Emphasis
        EMPHASIS_SCALE = 1.15
        EMPHASIS_SCALE_LARGE = 1.3
        PULSE_ITERATIONS = 2
        
        # Glow effects
        GLOW_RADIUS = 0.1
        GLOW_INTENSITY = 0.8
        
        # Wiggle
        WIGGLE_ANGLE = 0.1  # radians
        WIGGLE_ITERATIONS = 3
        
        @staticmethod
        def smooth_in():
            return rate_functions.ease_in_cubic
        
        @staticmethod
        def smooth_out():
            return rate_functions.ease_out_cubic
        
        @staticmethod
        def smooth_in_out():
            return rate_functions.ease_in_out_cubic
        
        @staticmethod
        def bounce():
            return rate_functions.ease_out_bounce
        
        @staticmethod
        def elastic():
            return rate_functions.ease_out_elastic
    
    # ═══════════════════════════════════════════════════════════════════════════
    # COMPONENT DEFAULTS
    # ═══════════════════════════════════════════════════════════════════════════
    
    class Defaults:
        """Default parameters for reusable components"""
        
        # File boxes
        FILE_WIDTH = 3.0
        FILE_HEIGHT = 2.0
        FILE_WIDTH_SM = 2.0
        FILE_HEIGHT_SM = 1.5
        FILE_CORNER_RADIUS = 0.15
        FILE_STROKE_WIDTH = 3
        FILE_FILL_OPACITY = 0.15
        
        # Log entries
        LOG_ENTRY_WIDTH = 2.0
        LOG_ENTRY_HEIGHT = 0.8
        LOG_SPACING = 0.1
        
        # Arrows
        ARROW_STROKE_WIDTH = 4
        ARROW_TIP_LENGTH = 0.25
        ARROW_TIP_WIDTH = 0.2
        
        # Code blocks
        CODE_BOX_WIDTH = 8.0
        CODE_BOX_HEIGHT = 2.0
        CODE_PADDING = 0.2
        
        # Layers (storage diagram)
        LAYER_WIDTH = 6.0
        LAYER_HEIGHT = 1.0
        LAYER_SPACING = 0.5
        
        # Tables
        TABLE_CELL_PADDING = 0.2
        TABLE_LINE_WIDTH = 2
        
        # Circles/dots
        DOT_RADIUS = 0.1
        CIRCLE_STROKE_WIDTH = 3
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CHAPTER METADATA
    # ═══════════════════════════════════════════════════════════════════════════
    
    class Chapters:
        """Chapter-specific metadata"""
        
        CHAPTER_01 = {
            "number": 1,
            "title_ar": "من الملفات إلى قواعد البيانات",
            "title_en": "From Files to Databases",
            "accent_color": "#9A72AC",
            "sections": [
                ("1.1", "التحديث في نفس المكان", "In-Place Updates"),
                ("1.2", "إعادة التسمية الذرية", "Atomic Rename"),
                ("1.3", "سجلات الإلحاق فقط", "Append-Only Logs"),
            ]
        }


# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL SINGLETON
# ═══════════════════════════════════════════════════════════════════════════════

config = DBConfig()

# Convenience aliases
C = DBConfig.Colors
T = DBConfig.Timing
F = DBConfig.Fonts
L = DBConfig.Layout
A = DBConfig.Animations
D = DBConfig.Defaults
