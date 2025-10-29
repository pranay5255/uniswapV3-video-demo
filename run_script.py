"""Render the UniswapLiquidityBasics scene and produce a demo video."""

from pathlib import Path

from manim import tempconfig

from uniswap_liquidity_formulas import UniswapLiquidityBasics


def render_scene() -> None:
    project_dir = Path(__file__).parent
    media_dir = project_dir / "media"
    media_dir.mkdir(parents=True, exist_ok=True)

    overrides = {
        "quality": "medium_quality",
        "output_file": "uniswap_liquidity_basics",
        "media_dir": str(media_dir),
        "format": "mp4",
        "preview": False,
    }

    with tempconfig(overrides):
        scene = UniswapLiquidityBasics()
        scene.render()
        output_path = Path(scene.renderer.file_writer.movie_file_path)

    print(f"Rendered video to {output_path}")


if __name__ == "__main__":
    render_scene()
