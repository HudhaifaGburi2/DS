"""
Chapter 01: From Files to Databases
====================================

Animations explaining fundamental database concepts:
- In-place file updates and their dangers
- Atomic rename operations
- Append-only logs with checksums
- fsync and durability guarantees
"""

from chapter_01.scene_01_inplace import Scene1_InPlaceUpdate
from chapter_01.scene_02_rename import Scene2_AtomicRename
from chapter_01.scene_03_logs import Scene3_AppendOnlyLog
from chapter_01.scene_04_fsync import Scene4_FSyncDiagram
from chapter_01.scene_05_comparison import Scene5_ComparisonTable
from chapter_01.scene_06_complete import Scene6_CompleteFlow, CompleteChapter

__all__ = [
    'Scene1_InPlaceUpdate',
    'Scene2_AtomicRename',
    'Scene3_AppendOnlyLog',
    'Scene4_FSyncDiagram',
    'Scene5_ComparisonTable',
    'Scene6_CompleteFlow',
    'CompleteChapter',
]
