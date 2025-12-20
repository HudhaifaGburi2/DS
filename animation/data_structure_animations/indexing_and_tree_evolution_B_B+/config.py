"""
B-Tree Evolution Animation - Configuration
==========================================

Centralized configuration for colors, timing, sizes, and typography.
All visual constants follow golden ratio (φ = 1.618) principles.
"""

from manim import *

# ══════════════════════════════════════════════════════════════════════════════
# GOLDEN RATIO CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

PHI = 1.618033988749895
PHI_INV = 0.618033988749895

# ══════════════════════════════════════════════════════════════════════════════
# COLOR PALETTE
# ══════════════════════════════════════════════════════════════════════════════

class Colors:
    """Semantic color definitions for B-Tree animations"""
    
    # Background
    BACKGROUND = "#1a1a2e"
    
    # Primary elements
    KEY = "#4fc3f7"           # Light blue for keys
    POINTER = "#ffd54f"       # Amber for pointers
    DATA = "#81c784"          # Green for data records
    
    # Disk and storage
    DISK_BLOCK = "#546e7a"    # Blue gray for disk blocks
    DISK_SURFACE = "#37474f"  # Dark blue gray
    MEMORY = "#7986cb"        # Indigo for memory
    
    # Tree nodes
    LEAF_NODE = "#4db6ac"     # Teal for leaf nodes
    INTERNAL_NODE = "#9575cd" # Purple for internal nodes
    ROOT_NODE = "#f06292"     # Pink for root
    
    # States and highlights
    HIGHLIGHT = "#ff7043"     # Deep orange for highlights
    SEARCH_PATH = "#ffca28"   # Amber for search paths
    SELECTED = "#e91e63"      # Pink for selected items
    SUCCESS = "#66bb6a"       # Green for success
    WARNING = "#ffa726"       # Orange for warnings
    ERROR = "#ef5350"         # Red for errors
    
    # Splits and promotions
    SPLIT_LEFT = "#42a5f5"    # Blue for left split
    SPLIT_RIGHT = "#ab47bc"   # Purple for right split
    PROMOTED = "#ffee58"      # Yellow for promoted keys
    
    # Leaf linking
    LEAF_LINK = "#26c6da"     # Cyan for leaf links
    RANGE_QUERY = "#69f0ae"   # Light green for range queries
    
    # Text
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b0bec5"
    TEXT_TERTIARY = "#616161"
    TEXT_ACCENT = "#80deea"
    TEXT_NARRATION = "#e0e0e0"
    
    # Arrows and edges
    EDGE = "#78909c"
    ARROW = "#90a4ae"


class C(Colors):
    """Shorthand alias for Colors"""
    pass


# ══════════════════════════════════════════════════════════════════════════════
# TIMING CONSTANTS (Golden Ratio Based)
# ══════════════════════════════════════════════════════════════════════════════

class Timing:
    """Animation timing constants"""
    
    # Core durations
    INSTANT = 0.1
    QUICK = PHI_INV * 0.618      # ~0.382s
    FAST = PHI_INV               # ~0.618s
    NORMAL = 1.0                 # 1.0s
    SLOW = PHI                   # ~1.618s
    DRAMATIC = PHI * PHI         # ~2.618s
    
    # Scene pacing
    BEAT = 0.5                   # Short pause
    ABSORB = 1.5                 # Let viewer absorb
    CONTEMPLATE = 2.5            # Deep understanding pause
    
    # Narration sync
    NARRATION_LINE = 2.0         # Time per narration line
    NARRATION_PAUSE = 0.8        # Pause between lines
    
    # Disk operations (slow, heavy feel)
    DISK_WRITE = 1.2
    DISK_READ = 0.8
    DISK_SEEK = 0.5
    
    # Tree operations
    SPLIT = 1.5
    PROMOTE = 1.0
    INSERT = 0.8
    SEARCH_STEP = 0.6
    
    # Transitions
    SCENE_TRANSITION = 0.8
    FADE_IN = 0.5
    FADE_OUT = 0.4


class T(Timing):
    """Shorthand alias for Timing"""
    pass


# ══════════════════════════════════════════════════════════════════════════════
# SIZE CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

class Sizes:
    """Visual element sizes"""
    
    # Disk blocks
    DISK_BLOCK_WIDTH = 1.4
    DISK_BLOCK_HEIGHT = 1.2
    DISK_BLOCK_SPACING = 0.3
    
    # Index entries
    INDEX_CELL_WIDTH = 1.0
    INDEX_CELL_HEIGHT = 0.5
    INDEX_ROW_SPACING = 0.1
    
    # Tree nodes
    NODE_KEY_WIDTH = 0.6
    NODE_KEY_HEIGHT = 0.5
    NODE_KEY_SPACING = 0.1
    NODE_PADDING = 0.2
    NODE_VERTICAL_SPACING = 1.8
    NODE_HORIZONTAL_SPACING = 0.8
    
    # Arrows and edges
    EDGE_STROKE = 2
    ARROW_STROKE = 3
    HIGHLIGHT_STROKE = 4
    
    # Layout
    MARGIN = 0.5
    MARGIN_LG = 0.8


class S(Sizes):
    """Shorthand alias for Sizes"""
    pass


# ══════════════════════════════════════════════════════════════════════════════
# TYPOGRAPHY
# ══════════════════════════════════════════════════════════════════════════════

class Typography:
    """Font and text styling"""
    
    # Fonts
    MAIN_FONT = "Arial"
    CODE_FONT = "Courier New"
    ARABIC_FONT = "Arial"
    
    # Sizes
    TITLE = 42
    HEADING = 36
    SUBHEADING = 28
    BODY = 24
    LABEL = 20
    CAPTION = 18
    TINY = 14
    
    # Key/value text in nodes
    KEY_SIZE = 22
    POINTER_SIZE = 16
    DATA_SIZE = 18
    
    # Narration
    NARRATION_SIZE = 26
    NARRATION_SPACING = 0.3


class F(Typography):
    """Shorthand alias for Typography"""
    pass


# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

class Layout:
    """Standard positions and regions"""
    
    # Screen regions
    TITLE_Y = 3.2
    NARRATION_Y = -3.2
    
    # Disk area
    DISK_Y = -1.5
    DISK_CENTER = DOWN * 1.5
    
    # Index table area
    INDEX_Y = 1.0
    INDEX_CENTER = UP * 1.0
    
    # Tree layout
    ROOT_Y = 2.0
    LEVEL_SPACING = 1.6
    
    # Comparison splits
    LEFT_HALF = LEFT * 3.5
    RIGHT_HALF = RIGHT * 3.5


class L(Layout):
    """Shorthand alias for Layout"""
    pass


# ══════════════════════════════════════════════════════════════════════════════
# ANIMATION PARAMETERS
# ══════════════════════════════════════════════════════════════════════════════

class AnimParams:
    """Animation-specific parameters"""
    
    # Opacity levels
    FULL = 1.0
    ACTIVE = 0.9
    NORMAL = 0.7
    DIMMED = 0.4
    FADED = 0.2
    GHOST = 0.1
    
    # Scale factors
    HIGHLIGHT_SCALE = 1.2
    FOCUS_SCALE = 1.15
    SHRINK_SCALE = 0.85
    
    # Rate functions
    SMOOTH = smooth
    EASE_IN = rate_functions.ease_in_cubic
    EASE_OUT = rate_functions.ease_out_cubic
    BOUNCE = rate_functions.ease_out_bounce
    
    # Node order (max keys per node)
    BTREE_ORDER = 4
    MIN_KEYS = 2  # ceil(order/2) - 1


class A(AnimParams):
    """Shorthand alias for AnimParams"""
    pass


# ══════════════════════════════════════════════════════════════════════════════
# SCENE METADATA
# ══════════════════════════════════════════════════════════════════════════════

SCENES = {
    "A": {"title": "Writing Data to Disk", "duration": 45},
    "B": {"title": "Building the Indexing Table", "duration": 40},
    "C": {"title": "Index Lookup (Binary Search)", "duration": 50},
    "D": {"title": "Index Growth Problem", "duration": 35},
    "E": {"title": "Relationship to M-Way Trees", "duration": 45},
    "F": {"title": "From Index Blocks to M-Way Tree", "duration": 40},
    "G": {"title": "B-Tree Bottom-Up Growth", "duration": 55},
    "H": {"title": "Propagating Splits Upward", "duration": 45},
    "I": {"title": "Balanced Tree Guarantee", "duration": 35},
    "J": {"title": "Transition to B+ Tree", "duration": 40},
    "K": {"title": "B+ Tree Structure", "duration": 45},
    "L": {"title": "Leaf Node Linking", "duration": 35},
    "M": {"title": "Range Query Efficiency", "duration": 50},
    "Final": {"title": "Evolution Timeline", "duration": 60},
}

# Total estimated duration: ~8-10 minutes
