# GB Studio Build Automation Targets

# Ensure build directories exist
build-dirs:
	mkdir -p build

# Validation targets
check-bg:
	python3 scripts/validation/check_bg_tiles.py assets/backgrounds/*.png

check-scenes:
	python3 scripts/validation/check_scene_limits.py project/scenes/

check-json:
	find . -name "*.json" -exec jq . {} \;

# Build targets
build-rom:
	node "/Users/madisonmilesmedia/gb-studio/out/cli/gb-studio-cli.js" export BARRY-SHARP-PRO-MOVER-1.gbsproj build/
	node "/Users/madisonmilesmedia/gb-studio/out/cli/gb-studio-cli.js" make:rom BARRY-SHARP-PRO-MOVER-1.gbsproj build/game.gb
	cp build/game.gb build/rom.gb

build-web:
	node "/Users/madisonmilesmedia/gb-studio/out/cli/gb-studio-cli.js" make:web BARRY-SHARP-PRO-MOVER-1.gbsproj build/

build-and-test: build-rom
	./scripts/build/launch_openemu.sh

hash-rom: build-rom
	md5sum ./build/rom.gb > ./build/rom.md5

.PHONY: build-dirs check-bg check-scenes check-json build-rom build-web build-and-test hash-rom