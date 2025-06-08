# Path to the GB Studio CLI executable. Can be overridden, e.g.: make build-rom GB_STUDIO_CLI=/custom/path/gb-studio-cli.js
GB_STUDIO_CLI ?= /Users/madisonmilesmedia/gb-studio/out/cli/gb-studio-cli.js

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
	node "$(GB_STUDIO_CLI)" export BARRY-SHARP-PRO-MOVER-1.gbsproj build/
	node "$(GB_STUDIO_CLI)" make:rom BARRY-SHARP-PRO-MOVER-1.gbsproj build/game.gb
	cp build/game.gb build/rom.gb

build-web:
	node "$(GB_STUDIO_CLI)" make:web BARRY-SHARP-PRO-MOVER-1.gbsproj build/

build-and-test: build-rom
	./scripts/build/launch_openemu.sh

hash-rom: build-rom
	md5sum ./build/rom.gb > ./build/rom.md5

.PHONY: build-dirs check-bg check-scenes check-json build-rom build-web build-and-test hash-rom