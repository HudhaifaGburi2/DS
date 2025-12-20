"""
OS Concepts Animation Components
================================

Reusable visual components for OS animations.
"""

from .threads import (
    Thread,
    ThreadGroup,
    ProcessBlock,
    CPUCore,
)

from .locks import (
    Mutex,
    RWLock,
    SpinLock,
    LockQueue,
    FineGrainedLock,
)

from .critical_sections import (
    CriticalSection,
    SharedResource,
    ProtectedRegion,
    DataCell,
)

from .timelines import (
    TimeAxis,
    VersionTimeline,
    VersionMarker,
    TransactionSpan,
)

from .memory import (
    MemoryCell,
    SnapshotView,
    VersionChain,
    SharedVariable,
)

from .effects import (
    ContentionPulse,
    ConflictFlash,
    RollbackWave,
    LockAcquireEffect,
    ValidationCheckmark,
)

__all__ = [
    # Threads
    "Thread", "ThreadGroup", "ProcessBlock", "CPUCore",
    # Locks
    "Mutex", "RWLock", "SpinLock", "LockQueue", "FineGrainedLock",
    # Critical Sections
    "CriticalSection", "SharedResource", "ProtectedRegion", "DataCell",
    # Timelines
    "TimeAxis", "VersionTimeline", "VersionMarker", "TransactionSpan",
    # Memory
    "MemoryCell", "SnapshotView", "VersionChain", "SharedVariable",
    # Effects
    "ContentionPulse", "ConflictFlash", "RollbackWave", 
    "LockAcquireEffect", "ValidationCheckmark",
]
