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
GBSTUDIO_CLI_PATH ?= gb-studio-cli

build-rom:
	node "$(GBSTUDIO_CLI_PATH)" export BARRY-SHARP-PRO-MOVER-1.gbsproj build/
	node "$(GBSTUDIO_CLI_PATH)" make:rom BARRY-SHARP-PRO-MOVER-1.gbsproj build/game.gb
	cp build/game.gb build/rom.gb

build-web:
	node "$(GBSTUDIO_CLI_PATH)" make:web BARRY-SHARP-PRO-MOVER-1.gbsproj build/

build-and-launch-emulator: build-rom
	./scripts/build/launch_openemu.sh

hash-rom: build-rom
	md5sum ./build/rom.gb > ./build/rom.md5

.PHONY: build-dirs check-bg check-scenes check-json build-rom build-web build-and-launch-emulator hash-rom