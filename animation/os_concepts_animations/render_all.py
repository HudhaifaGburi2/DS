#!/usr/bin/env python3
"""
OS Concepts Animations - Batch Renderer
=======================================

Renders all scenes in the OS concepts animation series.

Usage:
    python render_all.py --list                    # List all scenes
    python render_all.py --quality low             # Render all (preview)
    python render_all.py --quality high            # Render all (production)
    python render_all.py --module mutex            # Render specific module
    python render_all.py --scene Scene01_RaceCondition  # Render one scene
"""

import subprocess
import argparse
import sys
from pathlib import Path

# Scene registry
MODULES = {
    "mutex": {
        "title": "Mutex Locks",
        "path": "os_concepts/concurrency/mutex",
        "scenes": [
            ("Scene01_RaceCondition", "scene_01_problem"),
            ("Scene02_MutexBasic", "scene_02_mutex_basic"),
            ("Scene03_MutexCosts", "scene_03_costs"),
        ]
    },
    "fine_grained_locks": {
        "title": "Fine-Grained Locks",
        "path": "os_concepts/concurrency/fine_grained_locks",
        "scenes": [
            ("Scene01_CoarseVsFine", "scene_01_coarse_vs_fine"),
            ("Scene02_Parallelism", "scene_02_parallelism"),
            ("Scene03_Complexity", "scene_03_complexity"),
        ]
    },
    "optimistic_concurrency": {
        "title": "Optimistic Concurrency Control",
        "path": "os_concepts/concurrency/optimistic_concurrency",
        "scenes": [
            ("Scene01_Assumption", "scene_01_assumption"),
            ("Scene02_Validation", "scene_02_validation"),
            ("Scene03_Retry", "scene_03_retry"),
        ]
    },
    "mvcc": {
        "title": "Multi-Version Concurrency Control",
        "path": "os_concepts/concurrency/mvcc",
        "scenes": [
            ("Scene01_Versions", "scene_01_versions"),
            ("Scene02_Reads", "scene_02_reads"),
            ("Scene03_Writes", "scene_03_writes"),
            ("Scene04_Garbage", "scene_04_garbage"),
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
    print("\n📽️  OS Concepts - Available Scenes")
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
    print("\n🎬 Rendering ALL OS Concepts Scenes")
    print("=" * 60)
    
    total_success = 0
    total_count = 0
    
    for module_key, module_data in MODULES.items():
        print(f"\n📁 Module: {module_data['title']}")
        for scene_name, file_name in module_data["scenes"]:
            total_count += 1
            if render_scene(scene_name, module_data["path"], file_name, quality):
                total_success += 1
    
    print(f"\n📊 Final Results: {total_success}/{total_count} scenes rendered")
    return total_success == total_count


def main():
    parser = argparse.ArgumentParser(
        description="OS Concepts Animations - Batch Renderer"
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
