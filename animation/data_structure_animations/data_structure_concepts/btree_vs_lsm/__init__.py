"""
B-Tree vs LSM-Tree Comparison Module
====================================

Five-scene comparison of B-Tree and LSM-Tree data structures:
1. Introduction - Why disk-based indexing matters
2. B-Tree Structure - Anatomy and operations
3. LSM-Tree Structure - Architecture and write path
4. Read/Write Paths - Side-by-side comparison
5. Trade-offs - Latency, amplification, use cases
"""

from .scene_01_intro import Scene01_WhyDiskIndexing
from .scene_02_btree_structure import Scene02_BTreeStructure
from .scene_03_lsm_structure import Scene03_LSMStructure
from .scene_04_read_write_paths import Scene04_ReadWritePaths
from .scene_05_tradeoffs import Scene05_Tradeoffs

__all__ = [
    "Scene01_WhyDiskIndexing",
    "Scene02_BTreeStructure",
    "Scene03_LSMStructure",
    "Scene04_ReadWritePaths",
    "Scene05_Tradeoffs",
]
