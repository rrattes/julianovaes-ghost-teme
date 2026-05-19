from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
THEME_IMAGES = ROOT / "ghost-theme" / "julia-novaes" / "assets" / "images"
GHOST_IMAGES = ROOT / "ghost-local" / "content" / "images" / "2026" / "05"

TARGET_SIZE = (1600, 960)

SOURCES = {
    "artigo-relacao-fim.png": ASSETS / "artigo-1-crop.png",
    "artigo-casamentos.png": ASSETS / "artigo-3-crop.png",
    "artigo-feliz-sozinho.png": ASSETS / "artigo-2-crop.png",
    "artigo-akna.png": ASSETS / "consultorio-crop.png",
    "artigo-engravidar.png": ASSETS / "hero-julia-crop.png",
    "artigo-psicoterapia.png": ASSETS / "consultorio-crop.png",
}


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    image = image.convert("RGB")
    src_w, src_h = image.size
    dst_w, dst_h = size
    scale = max(dst_w / src_w, dst_h / src_h)
    resized = image.resize((round(src_w * scale), round(src_h * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - dst_w) // 2
    top = (resized.height - dst_h) // 2
    return resized.crop((left, top, left + dst_w, top + dst_h))


def trim_light_margin(image: Image.Image) -> Image.Image:
    image = image.convert("RGB")
    pixels = image.load()
    xs = []
    ys = []

    for y in range(image.height):
        for x in range(image.width):
            if min(pixels[x, y]) < 230:
                xs.append(x)
                ys.append(y)

    if not xs or not ys:
        return image

    left = max(min(xs) + 1, 0)
    top = max(min(ys) + 3, 0)
    right = min(max(xs), image.width)
    bottom = min(max(ys), image.height)
    return image.crop((left, top, right, bottom))


def make_editorial_image(source: Path, output: Path) -> None:
    base = trim_light_margin(Image.open(source).convert("RGB"))
    canvas = cover(base, TARGET_SIZE)
    canvas = ImageEnhance.Color(canvas).enhance(0.9)
    canvas = ImageEnhance.Contrast(canvas).enhance(1.04)
    canvas = ImageEnhance.Sharpness(canvas).enhance(1.25)
    canvas = canvas.filter(ImageFilter.UnsharpMask(radius=1.2, percent=90, threshold=4))

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, "PNG", optimize=True)


def main() -> None:
    for filename, source in SOURCES.items():
        theme_output = THEME_IMAGES / filename
        ghost_output = GHOST_IMAGES / filename
        make_editorial_image(source, theme_output)
        ghost_output.parent.mkdir(parents=True, exist_ok=True)
        ghost_output.write_bytes(theme_output.read_bytes())
        print(f"generated {filename} -> {TARGET_SIZE[0]}x{TARGET_SIZE[1]}")


if __name__ == "__main__":
    main()
