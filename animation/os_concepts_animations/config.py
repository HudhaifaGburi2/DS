"""
OS Concepts Animation Configuration
====================================

Centralized configuration for Operating Systems animations.
Golden ratio (φ) based timing and spacing for visual harmony.

Topics: Concurrency, Synchronization, Memory Management, Scheduling
"""

from manim import *

# ══════════════════════════════════════════════════════════════════════════════
# MATHEMATICAL CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

PHI = 1.618033988749895  # Golden ratio
PHI_INV = 0.618033988749895  # 1/φ
PHI_SQ = PHI * PHI  # φ²


# ══════════════════════════════════════════════════════════════════════════════
# COLOR PALETTE - OS CONCEPTS
# ══════════════════════════════════════════════════════════════════════════════

class C:
    """Semantic color palette for OS animations"""
    
    # Background
    BACKGROUND = "#0d1117"
    BACKGROUND_ALT = "#161b22"
    
    # Thread Colors (distinct for up to 6 threads)
    THREAD_1 = "#58A6FF"      # Blue
    THREAD_2 = "#F78166"      # Orange
    THREAD_3 = "#7EE787"      # Green
    THREAD_4 = "#D2A8FF"      # Purple
    THREAD_5 = "#FFA657"      # Amber
    THREAD_6 = "#79C0FF"      # Light Blue
    THREAD_COLORS = [THREAD_1, THREAD_2, THREAD_3, THREAD_4, THREAD_5, THREAD_6]
    
    # Lock States
    LOCK_FREE = "#7EE787"         # Green - available
    LOCK_HELD = "#F85149"         # Red - locked
    LOCK_WAITING = "#FFA657"      # Amber - blocked
    LOCK_ICON = "#8B949E"         # Gray - lock icon base
    
    # Critical Section
    CRITICAL_SECTION = "#FF7B72"  # Red tint - danger zone
    SAFE_SECTION = "#238636"      # Green - safe
    SHARED_RESOURCE = "#BD93F9"   # Purple - shared data
    
    # Concurrency States
    RUNNING = "#58A6FF"           # Blue - executing
    BLOCKED = "#F85149"           # Red - waiting
    READY = "#FFA657"             # Amber - ready queue
    COMPLETED = "#7EE787"         # Green - done
    
    # MVCC / Versioning
    VERSION_OLD = "#484F58"       # Gray - old version
    VERSION_CURRENT = "#58A6FF"   # Blue - current
    VERSION_NEW = "#7EE787"       # Green - new version
    SNAPSHOT = "#D2A8FF"          # Purple - snapshot read
    GARBAGE = "#6E7681"           # Dark gray - to be collected
    
    # Optimistic Concurrency
    VALIDATION_PASS = "#7EE787"   # Green
    VALIDATION_FAIL = "#F85149"   # Red
    ROLLBACK = "#FFA657"          # Amber
    RETRY = "#58A6FF"             # Blue
    
    # Conflict & Contention
    CONFLICT = "#F85149"          # Red - conflict detected
    CONTENTION_HIGH = "#F85149"   # Red
    CONTENTION_MED = "#FFA657"    # Amber
    CONTENTION_LOW = "#7EE787"    # Green
    
    # Timeline
    TIME_AXIS = "#8B949E"         # Gray
    TIME_MARKER = "#58A6FF"       # Blue
    TIME_NOW = "#F0F6FC"          # White
    
    # Text Hierarchy
    TEXT_PRIMARY = "#F0F6FC"
    TEXT_SECONDARY = "#8B949E"
    TEXT_TERTIARY = "#6E7681"
    TEXT_ACCENT = "#58A6FF"
    
    # Status
    SUCCESS = "#7EE787"
    WARNING = "#FFA657"
    ERROR = "#F85149"
    INFO = "#58A6FF"


# ══════════════════════════════════════════════════════════════════════════════
# TIMING CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

class T:
    """Golden ratio-based timing for animations"""
    
    # Base timings
    INSTANT = 0.1
    QUICK = 0.25
    FAST = PHI_INV * 0.618        # ~0.382s
    NORMAL = PHI_INV              # ~0.618s
    SLOW = 1.0
    DRAMATIC = PHI                # ~1.618s
    
    # Concurrency-specific
    LOCK_ACQUIRE = 0.4
    LOCK_RELEASE = 0.3
    THREAD_SPAWN = 0.5
    THREAD_BLOCK = 0.4
    THREAD_WAKE = 0.3
    
    # MVCC-specific
    VERSION_CREATE = 0.5
    SNAPSHOT_PIN = 0.3
    GARBAGE_COLLECT = 0.8
    
    # Conflict animations
    CONFLICT_FLASH = 0.2
    ROLLBACK = 0.6
    RETRY_DELAY = 0.4
    VALIDATION = 0.5
    
    # Pacing
    BEAT = PHI_INV                # Quick pause
    ABSORB = PHI                  # Let information sink in
    CONTEMPLATE = PHI_SQ          # Major concept pause


# ══════════════════════════════════════════════════════════════════════════════
# TYPOGRAPHY
# ══════════════════════════════════════════════════════════════════════════════

class F:
    """Font configuration"""
    
    # Font families
    ARABIC = "Arial"
    BODY = "Arial"
    CODE = "Courier New"
    
    # Relative scales
    SIZE_TITLE = 0.8
    SIZE_HEADING = 0.55
    SIZE_BODY = 0.45
    SIZE_CAPTION = 0.35
    SIZE_LABEL = 0.28
    SIZE_TINY = 0.22
    SIZE_CODE = 0.3
    SIZE_THREAD_ID = 0.25


# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT STANDARDS
# ══════════════════════════════════════════════════════════════════════════════

class L:
    """Layout constants for consistent spacing"""
    
    # Margins
    MARGIN_LG = 0.8
    MARGIN_MD = 0.5
    MARGIN_SM = 0.3
    
    # Spacing
    SPACING_LG = PHI * 0.5        # ~0.809
    SPACING_MD = 0.5
    SPACING_SM = PHI_INV * 0.5    # ~0.309
    SPACING_TIGHT = 0.15
    
    # Thread lanes
    THREAD_LANE_HEIGHT = 0.8
    THREAD_LANE_SPACING = 0.3
    THREAD_WIDTH = 0.6
    
    # Lock dimensions
    LOCK_SIZE = 0.5
    LOCK_SPACING = 0.8
    
    # Critical section
    CRITICAL_WIDTH = 3.0
    CRITICAL_HEIGHT = 2.0
    
    # Timeline
    TIMELINE_HEIGHT = 4.0
    TIMELINE_TICK_SPACING = 0.8
    VERSION_HEIGHT = 0.5
    VERSION_SPACING = 0.6
    
    # Comparison layout
    COMPARE_LEFT_CENTER = -3.5
    COMPARE_RIGHT_CENTER = 3.5
    COMPARE_DIVIDER_X = 0


# ══════════════════════════════════════════════════════════════════════════════
# ANIMATION PARAMETERS
# ══════════════════════════════════════════════════════════════════════════════

class A:
    """Animation-specific parameters"""
    
    # Lag ratios for staggered animations
    LAG_TIGHT = 0.05
    LAG_NORMAL = 0.15
    LAG_RELAXED = 0.3
    
    # Stroke widths
    THREAD_STROKE = 3
    LOCK_STROKE = 2.5
    TIMELINE_STROKE = 2
    ARROW_STROKE = 2
    HIGHLIGHT_STROKE = 4
    
    # Opacities
    GHOST_OPACITY = 0.3
    HIGHLIGHT_OPACITY = 0.8
    BLOCKED_OPACITY = 0.5
    
    # Pulse parameters
    PULSE_SCALE = 1.15
    PULSE_COUNT = 2
    
    # Contention visualization
    CONTENTION_PARTICLES = 8
    CONFLICT_FLASH_COUNT = 3


# ══════════════════════════════════════════════════════════════════════════════
# OS-SPECIFIC CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

class OS:
    """OS and concurrency-specific constants"""
    
    # Thread limits
    MAX_THREADS = 6
    DEFAULT_THREADS = 3
    
    # Lock types
    LOCK_MUTEX = "mutex"
    LOCK_RWLOCK = "rwlock"
    LOCK_SPINLOCK = "spinlock"
    
    # MVCC
    MAX_VERSIONS = 5
    SNAPSHOT_ISOLATION = "snapshot"
    READ_COMMITTED = "read_committed"
    
    # Optimistic CC
    RETRY_LIMIT = 3
    CONFLICT_PROBABILITY = 0.3
    
    # Visual metaphors
    LOCK_ICON = "🔒"
    UNLOCK_ICON = "🔓"
    THREAD_ICON = "▶"
    BLOCKED_ICON = "⏸"
    CONFLICT_ICON = "⚡"
    SUCCESS_ICON = "✓"
    FAIL_ICON = "✗"
