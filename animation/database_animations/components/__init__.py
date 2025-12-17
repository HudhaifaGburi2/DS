"""
Database Animation Framework - Components Package
==================================================

Reusable visual components for database animations.
Import commonly used components from this package.
"""

from components.files import FileBox, FileGroup, TempFile
from components.effects import (
    CrashEffect, 
    FsyncEffect, 
    AtomicEffect,
    CorruptionEffect,
    SuccessCheckmark,
    DataFlowDot
)
from components.code_display import CodeBlock, SyntaxHighlightedCode
from components.diagrams import (
    StorageLayer,
    StorageStack,
    LogEntry,
    LogSequence,
    ComparisonTable,
    Arrow as DiagramArrow
)

__all__ = [
    # Files
    'FileBox',
    'FileGroup', 
    'TempFile',
    
    # Effects
    'CrashEffect',
    'FsyncEffect',
    'AtomicEffect',
    'CorruptionEffect',
    'SuccessCheckmark',
    'DataFlowDot',
    
    # Code
    'CodeBlock',
    'SyntaxHighlightedCode',
    
    # Diagrams
    'StorageLayer',
    'StorageStack',
    'LogEntry',
    'LogSequence',
    'ComparisonTable',
    'DiagramArrow',
]
