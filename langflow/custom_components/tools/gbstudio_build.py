# THUNDERBIRD.ESQ – GBStudio Build node for LangFlow 1.4.x
from __future__ import annotations

import datetime
import pathlib
import subprocess

# LangFlow 1.4.x locates CustomComponent here ↓
from langflow.components.base.custom import CustomComponent


class GBStudioBuild(CustomComponent):
    """
    Compile a GB Studio project with gbstudio-cli and (optionally) open it in OpenEmu.
    """

    display_name = "GBStudio Build"
    description = "Compile a GB Studio project into a ROM and (optionally) launch OpenEmu."

    def build(
        self,
        project_dir: str,
        cli_path: str = "gbstudio-cli",
        open_emulator: bool = True,
        target: str = "rom",            # rom | web | all
        code: str | None = None,        # ← LangFlow injects this; we just ignore it
        **_: object,                    # ← future-proof
    ) -> str:
        pd = pathlib.Path(project_dir).expanduser().resolve()
        if not pd.exists():
            raise ValueError(f"Project dir not found: {pd}")

        ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        dist = pd / "dist" / ts
        dist.mkdir(parents=True, exist_ok=True)

        cmd = [
            cli_path,
            "--project",
            str(pd),
            "--output",
            str(dist),
            f"--{target}",
        ]
        if open_emulator:
            cmd.append("--open")

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(result.stderr or result.stdout)

        try:
            rom_path = next(dist.rglob("*.gb"))
        except StopIteration:
            raise RuntimeError("Build succeeded but no .gb file was produced.")

        return str(rom_path)


