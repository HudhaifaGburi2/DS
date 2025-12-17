#!/usr/bin/env python3
"""
Database Animation Framework - Batch Renderer
==============================================

Renders all scenes in the database animation series.

Usage:
    # Render all scenes (low quality for preview)
    python render_all.py --quality low
    
    # Render all scenes (high quality for production)
    python render_all.py --quality high
    
    # Render specific chapter
    python render_all.py --chapter 1
    
    # Render specific scene
    python render_all.py --scene Scene1_InPlaceUpdate
    
    # List all available scenes
    python render_all.py --list

Requirements:
    pip install manim
"""

import subprocess
import argparse
import sys
from pathlib import Path

# Scene registry - maps scene names to their module paths
SCENES = {
    # Chapter 1
    "chapter_01": {
        "title": "From Files to Databases",
        "scenes": [
            ("Scene1_InPlaceUpdate", "chapter_01.scene_01_inplace"),
            ("Scene2_AtomicRename", "chapter_01.scene_02_rename"),
            ("Scene3_AppendOnlyLog", "chapter_01.scene_03_logs"),
            ("Scene4_FSyncDiagram", "chapter_01.scene_04_fsync"),
            ("Scene5_ComparisonTable", "chapter_01.scene_05_comparison"),
            ("Scene6_CompleteFlow", "chapter_01.scene_06_complete"),
            ("CompleteChapter", "chapter_01.scene_06_complete"),
        ]
    },
    # Add more chapters here as they're developed
    # "chapter_02": {
    #     "title": "Data Structures",
    #     "scenes": [...]
    # },
}

# Quality presets
QUALITY_FLAGS = {
    "low": "-pql",      # Preview quality, low resolution
    "medium": "-pqm",   # Medium quality
    "high": "-pqh",     # High quality (1080p)
    "4k": "-pqk",       # 4K quality
    "preview": "-pql",  # Alias for low
    "production": "-pqh", # Alias for high
}


def get_all_scenes():
    """Get flat list of all scenes"""
    all_scenes = []
    for chapter_key, chapter_data in SCENES.items():
        for scene_name, module_path in chapter_data["scenes"]:
            all_scenes.append({
                "name": scene_name,
                "module": module_path,
                "chapter": chapter_key,
                "chapter_title": chapter_data["title"]
            })
    return all_scenes


def list_scenes():
    """Print all available scenes"""
    print("\n📽️  Available Scenes")
    print("=" * 60)
    
    for chapter_key, chapter_data in SCENES.items():
        print(f"\n📁 {chapter_key}: {chapter_data['title']}")
        print("-" * 50)
        for scene_name, module_path in chapter_data["scenes"]:
            print(f"   • {scene_name}")
    
    print("\n")


def render_scene(scene_name: str, module_path: str, quality: str = "low"):
    """Render a single scene"""
    quality_flag = QUALITY_FLAGS.get(quality, "-pql")
    
    # Build the manim command
    cmd = [
        "manim",
        quality_flag,
        f"{module_path.replace('.', '/')}.py",
        scene_name
    ]
    
    print(f"\n🎬 Rendering: {scene_name}")
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


def render_chapter(chapter_key: str, quality: str = "low"):
    """Render all scenes in a chapter"""
    if chapter_key not in SCENES:
        print(f"❌ Unknown chapter: {chapter_key}")
        print(f"   Available: {', '.join(SCENES.keys())}")
        return False
    
    chapter_data = SCENES[chapter_key]
    print(f"\n📁 Rendering Chapter: {chapter_data['title']}")
    print("=" * 60)
    
    success_count = 0
    total_count = len(chapter_data["scenes"])
    
    for scene_name, module_path in chapter_data["scenes"]:
        if render_scene(scene_name, module_path, quality):
            success_count += 1
    
    print(f"\n📊 Results: {success_count}/{total_count} scenes rendered successfully")
    return success_count == total_count


def render_all(quality: str = "low"):
    """Render all scenes in all chapters"""
    print("\n🎬 Rendering ALL Scenes")
    print("=" * 60)
    
    total_success = 0
    total_count = 0
    
    for chapter_key in SCENES:
        chapter_data = SCENES[chapter_key]
        for scene_name, module_path in chapter_data["scenes"]:
            total_count += 1
            if render_scene(scene_name, module_path, quality):
                total_success += 1
    
    print(f"\n📊 Final Results: {total_success}/{total_count} scenes rendered")
    return total_success == total_count


def main():
    parser = argparse.ArgumentParser(
        description="Database Animation Framework - Batch Renderer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python render_all.py --list                    # List all scenes
  python render_all.py --quality low             # Render all (preview)
  python render_all.py --quality high            # Render all (production)
  python render_all.py --chapter chapter_01      # Render Chapter 1
  python render_all.py --scene Scene1_InPlaceUpdate  # Render one scene
        """
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available scenes"
    )
    
    parser.add_argument(
        "--quality", "-q",
        choices=list(QUALITY_FLAGS.keys()),
        default="low",
        help="Render quality (default: low)"
    )
    
    parser.add_argument(
        "--chapter", "-c",
        help="Render specific chapter (e.g., chapter_01)"
    )
    
    parser.add_argument(
        "--scene", "-s",
        help="Render specific scene by name"
    )
    
    args = parser.parse_args()
    
    # List mode
    if args.list:
        list_scenes()
        return 0
    
    # Render specific scene
    if args.scene:
        all_scenes = get_all_scenes()
        scene_info = next(
            (s for s in all_scenes if s["name"] == args.scene),
            None
        )
        
        if scene_info:
            success = render_scene(
                scene_info["name"],
                scene_info["module"],
                args.quality
            )
            return 0 if success else 1
        else:
            print(f"❌ Unknown scene: {args.scene}")
            print("   Use --list to see available scenes")
            return 1
    
    # Render specific chapter
    if args.chapter:
        success = render_chapter(args.chapter, args.quality)
        return 0 if success else 1
    
    # Render all
    success = render_all(args.quality)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
