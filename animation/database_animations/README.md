# 🎬 Database Animation Framework

A modular, scalable Manim animation framework for creating professional educational animations about database concepts.

## 📁 Project Structure

```
database_animations/
├── config.py                 # Centralized configuration (colors, timing, fonts)
├── base_scenes.py           # Base classes for all scenes
├── components/              # Reusable visual components
│   ├── __init__.py
│   ├── files.py            # File visualizations (FileBox, TempFile)
│   ├── effects.py          # Visual effects (CrashEffect, FsyncEffect)
│   ├── code_display.py     # Code blocks with syntax highlighting
│   └── diagrams.py         # Tables, storage layers, log entries
├── utils/                   # Helper functions
│   ├── __init__.py
│   ├── animations.py       # Custom animation helpers
│   ├── math_helpers.py     # Golden ratio positioning, grids
│   └── text_helpers.py     # Bilingual text, bullet lists
├── chapter_01/             # Chapter 1: From Files to Databases
│   ├── __init__.py
│   ├── scene_01_inplace.py # In-place update dangers
│   ├── scene_02_rename.py  # Atomic rename solution
│   ├── scene_03_logs.py    # Append-only logs
│   ├── scene_04_fsync.py   # fsync and durability
│   ├── scene_05_comparison.py # Comparison table
│   └── scene_06_complete.py   # Chapter summary
└── render_all.py           # Batch rendering script
```

## 🚀 Quick Start

### Installation

```bash
# Install Manim Community
pip install manim

# Optional: Install additional fonts
# (Recommended for best typography)
```

### Render a Single Scene

```bash
cd database_animations

# Low quality preview (fast)
manim -pql chapter_01/scene_01_inplace.py Scene1_InPlaceUpdate

# High quality production
manim -pqh chapter_01/scene_01_inplace.py Scene1_InPlaceUpdate
```

### Batch Render

```bash
# List all available scenes
python render_all.py --list

# Render all scenes (preview quality)
python render_all.py --quality low

# Render all scenes (production quality)
python render_all.py --quality high

# Render specific chapter
python render_all.py --chapter chapter_01

# Render specific scene
python render_all.py --scene Scene1_InPlaceUpdate
```

## 🎨 Design System

### Colors
All colors are defined in `config.py` with semantic meaning:

| Color | Hex | Meaning |
|-------|-----|---------|
| `FILE_ORIGINAL` | `#58C4DD` | Original/source files |
| `FILE_NEW` | `#83C167` | New/temp files |
| `FILE_CORRUPT` | `#FF6B6B` | Corrupted data |
| `SUCCESS` | `#4CAF50` | Success states |
| `ERROR` | `#F44336` | Error states |
| `WARNING` | `#FFC107` | Warning states |

### Timing (Golden Ratio Based)
```python
INSTANT = 0.236   # φ⁻³ - Snap changes
QUICK = 0.382     # φ⁻² - Fast reveals
FAST = 0.618      # φ⁻¹ - Quick transitions
NORMAL = 1.0      # Standard timing
SLOW = 1.618      # φ   - Deliberate reveals
DRAMATIC = 2.618  # φ²  - Big moments
```

### Typography
- **Arabic**: Arial (best RTL support)
- **English**: SF Pro Display/Text
- **Code**: SF Mono

## 🧩 Using Components

### FileBox
```python
from components.files import FileBox

file = FileBox(
    filename="data.txt",
    content_text="Important Data",
    color=C.FILE_ORIGINAL
)
self.play(file.animate_create())
```

### CrashEffect
```python
from components.effects import CrashEffect

crash = CrashEffect(text="CRASH!", position=ORIGIN)
self.play(crash.animate_appear())
```

### StorageStack
```python
from components.diagrams import StorageStack

stack = StorageStack()
self.play(stack.animate_build())
```

## 📝 Creating New Scenes

1. **Inherit from base classes**:
```python
from base_scenes import DatabaseScene

class MyScene(DatabaseScene):
    def construct(self):
        title = self.create_title_card("عنوان", "Title")
        # Your animation logic here
```

2. **Use standardized components**:
```python
from components.files import FileBox
from components.effects import SuccessCheckmark
```

3. **Follow timing standards**:
```python
self.wait_beat()      # Short pause
self.wait_absorb()    # Medium pause for content
self.dramatic_pause() # Long pause for impact
```

## 📚 Extending for New Chapters

1. Create new chapter directory: `chapter_02/`
2. Add `__init__.py` with scene exports
3. Create scene files following the pattern
4. Register scenes in `render_all.py`

## 🎯 Best Practices

1. **Visual Narrative**: Every animation should tell a story
2. **Bilingual Support**: Always include Arabic and English text
3. **Consistent Timing**: Use config timing constants
4. **Component Reuse**: Use existing components, extend when needed
5. **Golden Ratio**: Use φ-based spacing and timing for harmony

## 📄 License

Part of the Database Systems educational series.

---

Created with 💜 using [Manim Community](https://www.manim.community/)
