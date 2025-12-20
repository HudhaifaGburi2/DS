"""
Fine-Grained Locks Module
=========================

Three scenes demonstrating fine-grained locking:
1. Coarse vs Fine - Lock scope comparison
2. Parallelism - Increased concurrency benefits
3. Complexity - Deadlock risks and ordering
"""

from .scene_01_coarse_vs_fine import Scene01_CoarseVsFine
from .scene_02_parallelism import Scene02_Parallelism
from .scene_03_complexity import Scene03_Complexity

__all__ = [
    "Scene01_CoarseVsFine",
    "Scene02_Parallelism",
    "Scene03_Complexity",
]
