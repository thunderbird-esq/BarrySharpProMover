from PIL import Image
import sys
import os
import argparse

TILE_SIZE = 8
MAX_TILES = 192

def get_tiles(image):
    tiles = set()
    width, height = image.size
    for y in range(0, height, TILE_SIZE):
        for x in range(0, width, TILE_SIZE):
            tile = image.crop((x, y, x + TILE_SIZE, y + TILE_SIZE))
            tiles.add(tile.tobytes())
    return tiles

def main():
    parser = argparse.ArgumentParser(description="Check GB Studio background tile counts")
    parser.add_argument("files", nargs='+', help="Path(s) to PNG files")
    args = parser.parse_args()

    for path in args.files:
        if not os.path.isfile(path):
            print(f"❌ File not found: {path}")
            continue

        img = Image.open(path)
        width, height = img.size

        if width != 160 or height != 144:
            print(f"⚠️  {os.path.basename(path)}: Size is {width}x{height}, expected 160x144")

        tiles = get_tiles(img)
        tile_count = len(tiles)

        if tile_count > MAX_TILES:
            print(f"❌ {os.path.basename(path)}: {tile_count} tiles (limit is {MAX_TILES})")
        else:
            print(f"✅ {os.path.basename(path)}: {tile_count} tiles OK")

if __name__ == "__main__":
    main()