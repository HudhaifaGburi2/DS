"""
Optimistic Concurrency Module
=============================

Three scenes demonstrating optimistic concurrency control:
1. Assumption - Low contention model
2. Validation - Conflict detection at commit
3. Retry - Rollback and retry on conflict
"""

from .scene_01_assumption import Scene01_Assumption
from .scene_02_validation import Scene02_Validation
from .scene_03_retry import Scene03_Retry

__all__ = [
    "Scene01_Assumption",
    "Scene02_Validation",
    "Scene03_Retry",
]
