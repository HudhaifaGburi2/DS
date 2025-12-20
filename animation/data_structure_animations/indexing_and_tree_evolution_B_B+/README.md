# 🌳 B-Tree Evolution Animation

Professional Manim animation visualizing the evolution from database indexing tables to B+ Trees.

## 📋 Overview

This animation series covers:
1. **Disk Storage** - How records are written to disk blocks
2. **Index Tables** - Building and searching sorted indexes
3. **M-Way Trees** - Evolution from tables to tree structures
4. **B-Trees** - Bottom-up growth and self-balancing
5. **B+ Trees** - Optimized structure with leaf linking
6. **Range Queries** - Efficient sequential scanning

**Total Duration:** ~8-10 minutes (14 scenes)

## 📁 Project Structure

```
indexing_and_tree_evolution_B_B+/
├── config.py           # Colors, timing, sizes, typography
├── components.py       # DiskBlock, IndexEntry, BTreeNode classes
├── scenes_part1.py     # Scenes A-D: Disk & Indexing
├── scenes_part2.py     # Scenes E-H: M-Way Trees & B-Tree Growth
├── scenes_part3.py     # Scenes I-L: B-Tree Balance & B+ Tree
├── scenes_part4.py     # Scenes M & Final: Range Queries & Summary
├── render_all.py       # Batch rendering script
└── README.md
```

## 🎬 Scene Guide

### Part 1: Disk Storage & Indexing
| Scene | Class | Description |
|-------|-------|-------------|
| A | `SceneA_DiskWrite` | Records written to disk blocks |
| B | `SceneB_IndexTable` | Index table creation |
| C | `SceneC_BinarySearch` | Binary search in index |
| D | `SceneD_IndexGrowth` | Index outgrowing memory |

### Part 2: M-Way Trees
| Scene | Class | Description |
|-------|-------|-------------|
| E | `SceneE_MWayRelation` | Index blocks → M-way nodes |
| F | `SceneF_TreeFormation` | Tree structure formation |
| G | `SceneG_BTreeGrowth` | Leaf insertion & splitting |
| H | `SceneH_CascadingSplits` | Splits propagating upward |

### Part 3: B+ Tree Introduction
| Scene | Class | Description |
|-------|-------|-------------|
| I | `SceneI_Balance` | Balanced tree guarantee |
| J | `SceneJ_BPlusTransition` | B-Tree → B+ Tree motivation |
| K | `SceneK_BPlusStructure` | B+ Tree structure (keys/data) |
| L | `SceneL_LeafLinking` | Horizontal leaf links |

### Part 4: Range Queries & Summary
| Scene | Class | Description |
|-------|-------|-------------|
| M | `SceneM_RangeQuery` | Efficient range query demo |
| Final | `SceneFinal_Timeline` | Evolution timeline summary |

## 🚀 Quick Start

```bash
cd /home/hg/Desktop/CMU\ DB/DS/animation/data_structure_animations/indexing_and_tree_evolution_B_B+

# List all scenes
python render_all.py --list

# Render single scene (preview quality)
manim -pql scenes_part1.py SceneA_DiskWrite

# Render single scene via script
python render_all.py --scene SceneA_DiskWrite --quality low

# Render entire part
python render_all.py --part part1 --quality medium

# Render all scenes (production)
python render_all.py --quality high
```

## 🎨 Visual Design

### Color Palette
- **Keys:** `#4fc3f7` (Light Blue)
- **Pointers:** `#ffd54f` (Amber)
- **Data:** `#81c784` (Green)
- **Leaf Nodes:** `#4db6ac` (Teal)
- **Internal Nodes:** `#9575cd` (Purple)
- **Highlights:** `#ff7043` (Deep Orange)
- **Leaf Links:** `#26c6da` (Cyan)

### Timing (Golden Ratio φ)
- Quick: 0.382s
- Fast: 0.618s
- Normal: 1.0s
- Slow: 1.618s
- Dramatic: 2.618s

## 📦 Components

### `DiskBlock`
Visual disk block with record slots.
```python
block = DiskBlock(block_id=1, records=[101, 205])
block.animate_write(312)  # Heavy disk write animation
block.animate_read()      # Highlight read
```

### `IndexEntry`
Key-pointer pair for index tables.
```python
entry = IndexEntry(key=100, block_addr=1)
entry.animate_highlight()
entry.animate_pointer_jump(target_block)
```

### `BTreeNode`
B-Tree/B+ Tree node with keys.
```python
node = BTreeNode([10, 20, 30], is_leaf=True)
node.animate_overflow()
node.animate_highlight_key(1)
```

## 🔧 Configuration

Edit `config.py` to customize:
- Color schemes (`Colors` class)
- Animation timing (`Timing` class)
- Node/block sizes (`Sizes` class)
- Typography (`Typography` class)

## 📺 Rendering for Production

### Individual Scenes (1080p)
```bash
manim -qh scenes_part1.py SceneA_DiskWrite
```

### All Scenes (1080p)
```bash
python render_all.py --quality high
```

### 4K Quality
```bash
python render_all.py --quality 4k
```

### Output Location
Videos are saved to:
```
media/videos/<filename>/1080p60/<SceneName>.mp4
```

## 📝 Narration Script

Each scene includes narration text synced to animations:

> **Scene A:** "When a record is inserted into a database, it is first written to disk..."

> **Scene Final:** "B-Trees balance the structure. B+ Trees optimize the disk."

## 🎯 Key Concepts Visualized

1. **Disk Block Organization** - Records packed into blocks
2. **Index Table Structure** - Sorted key-pointer pairs
3. **Binary Search** - Efficient index lookup
4. **M-Way Node Evolution** - Tables → Tree nodes
5. **Bottom-Up Growth** - Insert at leaves, split upward
6. **Self-Balancing** - All leaves at same depth
7. **B+ Tree Optimization** - Keys in internal, data in leaves
8. **Leaf Linking** - Sequential scan capability
9. **Range Query Efficiency** - Single traversal + leaf scan

---

Built with [Manim Community](https://www.manim.community/) 🎬
