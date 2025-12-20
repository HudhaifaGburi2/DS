#!/usr/bin/env python3
"""
Data Structure Animations - Batch Renderer
==========================================

Renders all scenes in the data structure animation series.

Usage:
    python render_all.py --list                    # List all scenes
    python render_all.py --quality low             # Render all (preview)
    python render_all.py --quality high            # Render all (production)
    python render_all.py --module btree_vs_lsm     # Render specific module
    python render_all.py --scene Scene01_WhyDiskIndexing  # Render one scene
"""

import subprocess
import argparse
import sys
from pathlib import Path

# Scene registry
MODULES = {
    "btree_vs_lsm": {
        "title": "B-Tree vs LSM-Tree",
        "path": "data_structure_concepts/btree_vs_lsm",
        "scenes": [
            ("Scene01_WhyDiskIndexing", "scene_01_intro"),
            ("Scene02_BTreeStructure", "scene_02_btree_structure"),
            ("Scene03_LSMStructure", "scene_03_lsm_structure"),
            ("Scene04_ReadWritePaths", "scene_04_read_write_paths"),
            ("Scene05_Tradeoffs", "scene_05_tradeoffs"),
            ("BTreeVsLSM_AllScenes", "all_scenes"),
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
    print("\n📽️  Available Scenes")
    print("=" * 60)
    
    for module_key, module_data in MODULES.items():
        print(f"\n📁 {module_key}: {module_data['title']}")
        print("-" * 50)
        for scene_name, file_name in module_data["scenes"]:
            print(f"   • {scene_name} ({file_name}.py)")
    
    print("\n")


def render_scene(scene_name: str, module_path: str, file_name: str, quality: str = "low"):
    """Render a single scene"""
    quality_flag = QUALITY_FLAGS.get(quality, "-pql")
    
    # Build path
    file_path = f"{module_path}/{file_name}.py"
    
    cmd = ["manim", quality_flag, file_path, scene_name]
    
    print(f"\n🎬 Rendering: {scene_name}")
    print(f"   File: {file_path}")
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


def render_module(module_key: str, quality: str = "low"):
    """Render all scenes in a module"""
    if module_key not in MODULES:
        print(f"❌ Unknown module: {module_key}")
        print(f"   Available: {', '.join(MODULES.keys())}")
        return False
    
    module_data = MODULES[module_key]
    print(f"\n📁 Rendering Module: {module_data['title']}")
    print("=" * 60)
    
    success_count = 0
    total_count = len(module_data["scenes"])
    
    for scene_name, file_name in module_data["scenes"]:
        if render_scene(scene_name, module_data["path"], file_name, quality):
            success_count += 1
    
    print(f"\n📊 Results: {success_count}/{total_count} scenes rendered")
    return success_count == total_count


def render_all(quality: str = "low"):
    """Render all scenes"""
    print("\n🎬 Rendering ALL Scenes")
    print("=" * 60)
    
    total_success = 0
    total_count = 0
    
    for module_key, module_data in MODULES.items():
        for scene_name, file_name in module_data["scenes"]:
            total_count += 1
            if render_scene(scene_name, module_data["path"], file_name, quality):
                total_success += 1
    
    print(f"\n📊 Final Results: {total_success}/{total_count} scenes rendered")
    return total_success == total_count


def main():
    parser = argparse.ArgumentParser(
        description="Data Structure Animations - Batch Renderer"
    )
    
    parser.add_argument("--list", "-l", action="store_true", help="List all scenes")
    parser.add_argument("--quality", "-q", choices=list(QUALITY_FLAGS.keys()), default="low")
    parser.add_argument("--module", "-m", help="Render specific module")
    parser.add_argument("--scene", "-s", help="Render specific scene")
    
    args = parser.parse_args()
    
    if args.list:
        list_scenes()
        return 0
    
    if args.scene:
        # Find the scene
        for module_key, module_data in MODULES.items():
            for scene_name, file_name in module_data["scenes"]:
                if scene_name == args.scene:
                    success = render_scene(
                        scene_name, 
                        module_data["path"], 
                        file_name, 
                        args.quality
                    )
                    return 0 if success else 1
        
        print(f"❌ Scene not found: {args.scene}")
        return 1
    
    if args.module:
        success = render_module(args.module, args.quality)
        return 0 if success else 1
    
    success = render_all(args.quality)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
