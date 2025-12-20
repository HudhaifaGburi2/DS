#!/usr/bin/env python3
"""
B-Tree Evolution Animation - Batch Renderer
============================================

Renders all scenes in the B-Tree evolution animation series.

Usage:
    python render_all.py --list                    # List all scenes
    python render_all.py --quality low             # Render all (preview)
    python render_all.py --quality high            # Render all (production)
    python render_all.py --scene SceneA_DiskWrite  # Render single scene
    python render_all.py --part 1                  # Render Part 1 scenes
"""

import subprocess
import argparse
import sys
from pathlib import Path

# Scene registry organized by part
SCENES = {
    "part1": {
        "title": "Part 1: Disk Storage & Indexing",
        "file": "scenes_part1.py",
        "scenes": [
            ("SceneA_DiskWrite", "Writing Data to Disk"),
            ("SceneB_IndexTable", "Building the Indexing Table"),
            ("SceneC_BinarySearch", "Index Lookup (Binary Search)"),
            ("SceneD_IndexGrowth", "Index Growth Problem"),
        ]
    },
    "part2": {
        "title": "Part 2: M-Way Trees & Tree Formation",
        "file": "scenes_part2.py",
        "scenes": [
            ("SceneE_MWayRelation", "From Indexing to M-Way Trees"),
            ("SceneF_TreeFormation", "Index Blocks Form a Tree"),
            ("SceneG_BTreeGrowth", "B-Tree Bottom-Up Growth"),
            ("SceneH_CascadingSplits", "Propagating Splits Upward"),
        ]
    },
    "part3": {
        "title": "Part 3: B-Tree Balance & B+ Tree",
        "file": "scenes_part3.py",
        "scenes": [
            ("SceneI_Balance", "Balanced Tree Guarantee"),
            ("SceneJ_BPlusTransition", "From B-Tree to B+ Tree"),
            ("SceneK_BPlusStructure", "B+ Tree Structure"),
            ("SceneL_LeafLinking", "Leaf Node Linking"),
        ]
    },
    "part4": {
        "title": "Part 4: Range Queries & Summary",
        "file": "scenes_part4.py",
        "scenes": [
            ("SceneM_RangeQuery", "Range Query Efficiency"),
            ("SceneFinal_Timeline", "Evolution Timeline"),
            ("CompleteEvolution", "Complete Animation"),
        ]
    },
}

# Quality presets
QUALITY_FLAGS = {
    "low": "-pql",
    "medium": "-pqm",
    "high": "-pqh",
    "4k": "-pqk",
    "preview": "-pql",
    "production": "-pqh",
}


def list_scenes():
    """Print all available scenes"""
    print("\n🎬 B-Tree Evolution Animation - Available Scenes")
    print("=" * 65)
    
    total_scenes = 0
    for part_key, part_data in SCENES.items():
        print(f"\n📁 {part_data['title']}")
        print(f"   File: {part_data['file']}")
        print("-" * 55)
        for scene_name, description in part_data["scenes"]:
            print(f"   • {scene_name}")
            print(f"     └─ {description}")
            total_scenes += 1
    
    print(f"\n📊 Total: {total_scenes} scenes")
    print("\n")


def find_scene(scene_name: str):
    """Find which file contains a scene"""
    for part_key, part_data in SCENES.items():
        for name, desc in part_data["scenes"]:
            if name == scene_name:
                return part_data["file"], name, desc
    return None, None, None


def render_scene(file_name: str, scene_name: str, quality: str = "low"):
    """Render a single scene"""
    quality_flag = QUALITY_FLAGS.get(quality, "-pql")
    
    cmd = ["manim", quality_flag, file_name, scene_name]
    
    print(f"\n🎬 Rendering: {scene_name}")
    print(f"   File: {file_name}")
    print(f"   Quality: {quality}")
    print(f"   Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=Path(__file__).parent,
            capture_output=False
        )
        
        if result.returncode == 0:
            print(f"   ✅ Success!")
            return True
        else:
            print(f"   ❌ Failed (exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def render_part(part_key: str, quality: str = "low"):
    """Render all scenes in a part"""
    if part_key not in SCENES:
        print(f"❌ Unknown part: {part_key}")
        print(f"   Available: {', '.join(SCENES.keys())}")
        return False
    
    part_data = SCENES[part_key]
    print(f"\n📁 Rendering: {part_data['title']}")
    print("=" * 60)
    
    success_count = 0
    total_count = len(part_data["scenes"])
    
    for scene_name, description in part_data["scenes"]:
        if render_scene(part_data["file"], scene_name, quality):
            success_count += 1
    
    print(f"\n📊 Results: {success_count}/{total_count} scenes rendered")
    return success_count == total_count


def render_all(quality: str = "low"):
    """Render all scenes"""
    print("\n🎬 Rendering ALL B-Tree Evolution Scenes")
    print("=" * 60)
    
    total_success = 0
    total_count = 0
    
    for part_key, part_data in SCENES.items():
        print(f"\n📁 {part_data['title']}")
        for scene_name, description in part_data["scenes"]:
            total_count += 1
            if render_scene(part_data["file"], scene_name, quality):
                total_success += 1
    
    print(f"\n📊 Final Results: {total_success}/{total_count} scenes rendered")
    return total_success == total_count


def main():
    parser = argparse.ArgumentParser(
        description="B-Tree Evolution Animation - Batch Renderer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python render_all.py --list
    python render_all.py --scene SceneA_DiskWrite --quality low
    python render_all.py --part part1 --quality medium
    python render_all.py --quality high
        """
    )
    
    parser.add_argument("--list", "-l", action="store_true", help="List all scenes")
    parser.add_argument("--quality", "-q", choices=list(QUALITY_FLAGS.keys()), default="low",
                       help="Render quality (default: low)")
    parser.add_argument("--scene", "-s", help="Render specific scene")
    parser.add_argument("--part", "-p", choices=list(SCENES.keys()), help="Render specific part")
    
    args = parser.parse_args()
    
    if args.list:
        list_scenes()
        return 0
    
    if args.scene:
        file_name, scene_name, desc = find_scene(args.scene)
        if file_name:
            success = render_scene(file_name, scene_name, args.quality)
            return 0 if success else 1
        else:
            print(f"❌ Scene not found: {args.scene}")
            print("Use --list to see available scenes")
            return 1
    
    if args.part:
        success = render_part(args.part, args.quality)
        return 0 if success else 1
    
    # Render all by default
    success = render_all(args.quality)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
