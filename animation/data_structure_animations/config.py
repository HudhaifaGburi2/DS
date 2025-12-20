"""
Data Structure Animations - Global Configuration
=================================================

Centralized configuration for all data structure concept animations.
Uses golden ratio (φ = 1.618) for harmonious proportions and timing.

Usage:
    from config import C, T, F, L, DS
    
    # Colors
    node.set_fill(color=C.BTREE_NODE)
    
    # Timing
    self.play(animation, run_time=T.NORMAL)
    
    # Data structure specific
    node_width = DS.BTREE_NODE_WIDTH
"""

from manim import *
from dataclasses import dataclass
from typing import Dict, Any


# ══════════════════════════════════════════════════════════════════════════════
# MATHEMATICAL CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

PHI = 1.618033988749895  # Golden ratio
PHI_INV = 0.618033988749895  # 1/φ
PHI_SQ = 2.618033988749895  # φ²
PHI_CUBE = 4.236067977499790  # φ³

FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]


# ══════════════════════════════════════════════════════════════════════════════
# COLOR PALETTE
# ══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class Colors:
    """Semantic color system for data structure visualizations"""
    
    # Background
    BACKGROUND: str = "#1a1a2e"
    BACKGROUND_ALT: str = "#16213e"
    
    # Text hierarchy
    TEXT_PRIMARY: str = "#FFFFFF"
    TEXT_SECONDARY: str = "#B8B8B8"
    TEXT_TERTIARY: str = "#6B6B6B"
    TEXT_ACCENT: str = "#FFD93D"
    
    # B-Tree colors (cool, structured, read-optimized)
    BTREE_NODE: str = "#4A90D9"          # Primary blue
    BTREE_NODE_HIGHLIGHT: str = "#6BB3FF" # Bright blue
    BTREE_KEY: str = "#FFFFFF"           # White keys
    BTREE_KEY_ACTIVE: str = "#FFD93D"    # Yellow highlight
    BTREE_POINTER: str = "#7EC8E3"       # Light cyan
    BTREE_SPLIT: str = "#FF6B6B"         # Red for splits
    BTREE_MERGE: str = "#4ECDC4"         # Teal for merges
    BTREE_PAGE: str = "#2D5A87"          # Dark blue page
    
    # LSM-Tree colors (warm, flowing, write-optimized)
    LSM_MEMTABLE: str = "#4ECDC4"        # Teal (in-memory)
    LSM_MEMTABLE_HOT: str = "#7FFFD4"    # Aquamarine (active writes)
    LSM_SSTABLE: str = "#9B59B6"         # Purple (on-disk)
    LSM_SSTABLE_L0: str = "#E74C3C"      # Red (level 0 - hot)
    LSM_SSTABLE_L1: str = "#F39C12"      # Orange (level 1)
    LSM_SSTABLE_L2: str = "#3498DB"      # Blue (level 2)
    LSM_SSTABLE_L3: str = "#1ABC9C"      # Green (level 3 - cold)
    LSM_COMPACTION: str = "#F1C40F"      # Yellow (compaction)
    LSM_BLOOM: str = "#E91E63"           # Pink (bloom filter)
    
    # Storage hierarchy
    MEMORY_RAM: str = "#4ECDC4"          # Teal (fast)
    MEMORY_CACHE: str = "#7FFFD4"        # Aquamarine
    DISK_SSD: str = "#9B59B6"            # Purple
    DISK_HDD: str = "#34495E"            # Dark gray
    
    # I/O operations
    IO_READ: str = "#3498DB"             # Blue (read)
    IO_WRITE: str = "#E74C3C"            # Red (write)
    IO_SEQUENTIAL: str = "#2ECC71"       # Green (efficient)
    IO_RANDOM: str = "#E74C3C"           # Red (expensive)
    
    # Status & feedback
    SUCCESS: str = "#2ECC71"
    WARNING: str = "#F1C40F"
    ERROR: str = "#E74C3C"
    INFO: str = "#3498DB"
    
    # Comparison colors
    COMPARE_A: str = "#4A90D9"           # B-Tree side
    COMPARE_B: str = "#9B59B6"           # LSM-Tree side
    COMPARE_WINNER: str = "#2ECC71"      # Winner highlight
    COMPARE_LOSER: str = "#95A5A6"       # Dimmed loser
    
    # Amplification visualization
    WRITE_AMP: str = "#E74C3C"           # Write amplification
    READ_AMP: str = "#3498DB"            # Read amplification
    SPACE_AMP: str = "#F1C40F"           # Space amplification


C = Colors()


# ══════════════════════════════════════════════════════════════════════════════
# TIMING STANDARDS (φ-based)
# ══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class Timing:
    """Animation timing using golden ratio intervals"""
    
    # Core timings
    INSTANT: float = 0.1                 # Snap changes
    FLASH: float = 0.236                 # φ⁻³ - Quick flash
    QUICK: float = 0.382                 # φ⁻² - Fast reveals
    FAST: float = 0.618                  # φ⁻¹ - Quick transitions
    NORMAL: float = 1.0                  # Standard timing
    SLOW: float = 1.618                  # φ - Deliberate reveals
    DRAMATIC: float = 2.618              # φ² - Big moments
    EPIC: float = 4.236                  # φ³ - Chapter transitions
    
    # Pauses
    BEAT: float = 0.382                  # Quick beat
    BREATH: float = 0.618                # Short pause
    ABSORB: float = 1.0                  # Content absorption
    CONTEMPLATE: float = 1.618           # Deeper pause
    
    # Specific operations
    NODE_CREATE: float = 0.618
    NODE_HIGHLIGHT: float = 0.382
    KEY_INSERT: float = 0.5
    KEY_SEARCH: float = 0.3
    SPLIT_ANIMATE: float = 1.0
    MERGE_ANIMATE: float = 1.0
    COMPACTION: float = 1.618
    FLUSH: float = 0.8
    IO_ARROW: float = 0.5


T = Timing()


# ══════════════════════════════════════════════════════════════════════════════
# TYPOGRAPHY
# ══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class Fonts:
    """Font configuration"""
    
    # Font families
    DISPLAY: str = "Arial"               # Headers
    BODY: str = "Arial"                  # Body text
    CODE: str = "monospace"              # Code/keys
    ARABIC: str = "Arial"                # Arabic text
    
    # Sizes (relative scale)
    SIZE_HERO: float = 1.2               # Main titles
    SIZE_TITLE: float = 0.9              # Section titles
    SIZE_HEADING: float = 0.7            # Headings
    SIZE_BODY: float = 0.5               # Body text
    SIZE_CAPTION: float = 0.4            # Captions
    SIZE_LABEL: float = 0.35             # Labels
    SIZE_KEY: float = 0.3                # Node keys
    SIZE_TINY: float = 0.25              # Annotations


F = Fonts()


# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT STANDARDS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class Layout:
    """Spacing and layout using golden ratio"""
    
    # Margins
    MARGIN_XS: float = 0.1
    MARGIN_SM: float = 0.2
    MARGIN_MD: float = 0.382             # φ⁻²
    MARGIN_LG: float = 0.618             # φ⁻¹
    MARGIN_XL: float = 1.0
    
    # Spacing
    SPACING_TIGHT: float = 0.1
    SPACING_SM: float = 0.2
    SPACING_MD: float = 0.382
    SPACING_LG: float = 0.618
    SPACING_XL: float = 1.0
    
    # Tree layout
    TREE_LEVEL_HEIGHT: float = 1.5       # Vertical spacing between levels
    TREE_NODE_SPACING: float = 0.3       # Horizontal spacing
    TREE_MAX_WIDTH: float = 12           # Maximum tree width
    
    # Comparison layout
    COMPARE_SPLIT: float = 0.0           # Center line
    COMPARE_LEFT_CENTER: float = -3.5    # Left side center
    COMPARE_RIGHT_CENTER: float = 3.5    # Right side center
    COMPARE_WIDTH: float = 6.0           # Each side width


L = Layout()


# ══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURE SPECIFIC CONFIG
# ══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class DataStructures:
    """Data structure specific configurations"""
    
    # B-Tree
    BTREE_ORDER: int = 4                 # Max keys per node (order-1)
    BTREE_NODE_WIDTH: float = 2.0
    BTREE_NODE_HEIGHT: float = 0.6
    BTREE_KEY_WIDTH: float = 0.45
    BTREE_KEY_HEIGHT: float = 0.5
    BTREE_POINTER_SIZE: float = 0.15
    
    # LSM-Tree
    LSM_MEMTABLE_HEIGHT: float = 1.5
    LSM_MEMTABLE_WIDTH: float = 3.0
    LSM_SSTABLE_HEIGHT: float = 0.5
    LSM_SSTABLE_WIDTH: float = 2.5
    LSM_LEVEL_SPACING: float = 0.8
    LSM_MAX_LEVELS: int = 4
    LSM_SIZE_RATIO: int = 10             # Level size multiplier
    
    # Disk page
    PAGE_WIDTH: float = 1.2
    PAGE_HEIGHT: float = 1.5
    PAGE_CORNER_RADIUS: float = 0.08
    
    # Memory buffer
    BUFFER_WIDTH: float = 3.0
    BUFFER_HEIGHT: float = 1.0


DS = DataStructures()


# ══════════════════════════════════════════════════════════════════════════════
# ANIMATION PARAMETERS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class AnimationParams:
    """Animation-specific parameters"""
    
    # Easing
    DEFAULT_RATE_FUNC: str = "smooth"
    BOUNCE_RATE_FUNC: str = "ease_out_bounce"
    
    # Lag ratios for staggered animations
    LAG_FAST: float = 0.05
    LAG_NORMAL: float = 0.1
    LAG_SLOW: float = 0.2
    
    # Glow/highlight
    GLOW_RADIUS: float = 0.3
    HIGHLIGHT_OPACITY: float = 0.3
    PULSE_SCALE: float = 1.1
    
    # Arrows
    ARROW_STROKE: float = 3
    ARROW_TIP_SIZE: float = 0.2
    
    # Path animations
    PATH_STROKE: float = 4
    PATH_DASH_LENGTH: float = 0.1


A = AnimationParams()


# ══════════════════════════════════════════════════════════════════════════════
# SCENE METADATA
# ══════════════════════════════════════════════════════════════════════════════

BTREE_VS_LSM_META = {
    "title_ar": "B-Tree مقابل LSM-Tree",
    "title_en": "B-Tree vs LSM-Tree",
    "chapter": "Data Structure Concepts",
    "scenes": [
        {
            "id": "scene_01_intro",
            "title_ar": "لماذا الفهرسة على القرص؟",
            "title_en": "Why Disk-Based Indexing?",
        },
        {
            "id": "scene_02_btree_structure",
            "title_ar": "بنية B-Tree",
            "title_en": "B-Tree Structure",
        },
        {
            "id": "scene_03_lsm_structure",
            "title_ar": "بنية LSM-Tree",
            "title_en": "LSM-Tree Structure",
        },
        {
            "id": "scene_04_read_write_paths",
            "title_ar": "مسارات القراءة والكتابة",
            "title_en": "Read & Write Paths",
        },
        {
            "id": "scene_05_tradeoffs",
            "title_ar": "المقايضات",
            "title_en": "Trade-offs",
        },
    ]
}


# ══════════════════════════════════════════════════════════════════════════════
# UTILITY EXPORTS
# ══════════════════════════════════════════════════════════════════════════════

# Convenience access to all config
config = {
    "colors": C,
    "timing": T,
    "fonts": F,
    "layout": L,
    "data_structures": DS,
    "animation": A,
    "phi": PHI,
    "fibonacci": FIBONACCI,
}
