# 🎬 Data Structure Animations

Modular Manim framework for data structure educational animations.

## 📁 Structure

```
data_structure_animations/
├── config.py                    # Colors, timing, φ ratios
├── base_scenes.py              # DataStructureScene, TreeScene, ComparisonScene
├── components/                 # Reusable visual components
├── utils/                      # Animation, layout, text helpers
├── data_structure_concepts/
│   └── btree_vs_lsm/          # B-Tree vs LSM-Tree comparison
└── render_all.py              # Batch renderer
```

## 🚀 Quick Start

```bash
# List scenes
python render_all.py --list

# Render all (preview)
manim -pql data_structure_concepts/btree_vs_lsm/all_scenes.py BTreeVsLSM_AllScenes

# Render single scene
manim -pql data_structure_concepts/btree_vs_lsm/scene_01_intro.py Scene01_WhyDiskIndexing
```

## 🎨 Design System

- **Golden ratio (φ=1.618)** for timing and spacing
- **Semantic colors**: B-Tree (blue), LSM-Tree (teal), I/O (read=blue, write=red)
- **Bilingual support**: Arabic + English

## 📚 Modules

### B-Tree vs LSM-Tree
1. Why Disk-Based Indexing
2. B-Tree Structure
3. LSM-Tree Structure  
4. Read/Write Paths Comparison
5. Trade-offs Analysis

---
Built with [Manim Community](https://www.manim.community/)
