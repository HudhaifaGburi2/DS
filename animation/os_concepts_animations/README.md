# 🎬 OS Concepts Animations

Modular Manim framework for Operating Systems educational animations, focusing on concurrency and synchronization.

## 📁 Project Structure

```
os_concepts_animations/
├── config.py                    # Colors, timing, OS metaphors
├── base_scenes.py              # OSScene, ConcurrencyScene, TimelineScene
├── components/
│   ├── threads.py              # Thread, ThreadGroup, CPUCore
│   ├── locks.py                # Mutex, RWLock, SpinLock, FineGrainedLock
│   ├── critical_sections.py    # CriticalSection, SharedResource
│   ├── timelines.py            # TimeAxis, VersionTimeline, TransactionSpan
│   ├── memory.py               # MemoryCell, SnapshotView, VersionChain
│   └── effects.py              # ContentionPulse, ConflictFlash, RollbackWave
├── utils/
│   ├── animations.py           # Contention waves, conflict effects
│   ├── layout.py               # Thread lanes, timeline positioning
│   └── text_helpers.py         # Bilingual labels, state badges
├── os_concepts/
│   └── concurrency/
│       ├── mutex/              # 3 scenes: Race condition → Mutex → Costs
│       ├── fine_grained_locks/ # 3 scenes: Coarse vs Fine → Parallelism → Deadlock
│       ├── optimistic_concurrency/ # 3 scenes: Assumption → Validation → Retry
│       └── mvcc/               # 4 scenes: Versions → Reads → Writes → GC
└── render_all.py               # Batch renderer
```

## 🚀 Quick Start

```bash
# List all scenes
python render_all.py --list

# Render all mutex scenes
python render_all.py --module mutex --quality low

# Render single scene
manim -pql os_concepts/concurrency/mutex/scene_01_problem.py Scene01_RaceCondition

# Render all (production quality)
python render_all.py --quality high
```

## 🎨 Visual Design

### Color Semantics
- **Threads**: Blue, Orange, Green, Purple (T1-T4)
- **Lock States**: Green (free), Red (held), Amber (waiting)
- **Versions**: Blue (current), Green (new), Gray (old)
- **Conflicts**: Red flash, amber rollback

### Timing (Golden Ratio φ)
- Quick actions: 0.382s
- Normal transitions: 0.618s  
- Dramatic reveals: 1.618s

## 📚 Module Overview

### 1. Mutex (3 scenes)
- **Race Condition**: Why synchronization is needed
- **Mutex Basic**: Lock/unlock mechanism
- **Costs**: Blocking overhead, contention

### 2. Fine-Grained Locks (3 scenes)
- **Coarse vs Fine**: Lock scope comparison
- **Parallelism**: Throughput benefits
- **Complexity**: Deadlock risks

### 3. Optimistic Concurrency (3 scenes)
- **Assumption**: Low contention model
- **Validation**: Conflict detection
- **Retry**: Rollback on conflict

### 4. MVCC (4 scenes)
- **Versions**: Multiple data versions
- **Reads**: Snapshot isolation
- **Writes**: Copy-on-write
- **Garbage**: Version cleanup

## 🔮 Extensibility

Future OS topics can be added:
- `os_concepts/scheduling/` - CPU schedulers
- `os_concepts/memory/` - Virtual memory, paging
- `os_concepts/deadlocks/` - Detection & prevention

---
Built with [Manim Community](https://www.manim.community/)
