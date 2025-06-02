import os
import json
import argparse

MAX_ACTORS = 20
MAX_TRIGGERS = 30
MAX_SPRITE_TILES = 96

def check_scene(path):
    with open(path, 'r') as f:
        data = json.load(f)

    actor_count = len(data.get("actors", []))
    trigger_count = len(data.get("triggers", []))
    sprite_tiles = data.get("spriteTilesUsed", 0)

    basename = os.path.basename(path)
    issues = []

    if actor_count > MAX_ACTORS:
        issues.append(f"❌ {actor_count} actors (limit: {MAX_ACTORS})")
    if trigger_count > MAX_TRIGGERS:
        issues.append(f"❌ {trigger_count} triggers (limit: {MAX_TRIGGERS})")
    if sprite_tiles > MAX_SPRITE_TILES:
        issues.append(f"❌ {sprite_tiles} sprite tiles (limit: {MAX_SPRITE_TILES})")

    if issues:
        print(f"⚠️  {basename}:")
        for issue in issues:
            print("   ", issue)
    else:
        print(f"✅ {basename}: All limits OK")

def main():
    parser = argparse.ArgumentParser(description="Check GB Studio scene limits")
    parser.add_argument("scene_dir", help="Directory of scene JSON files")
    args = parser.parse_args()

    for file in os.listdir(args.scene_dir):
        if file.endswith(".json"):
            check_scene(os.path.join(args.scene_dir, file))

if __name__ == "__main__":
    main()