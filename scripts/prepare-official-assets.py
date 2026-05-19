import os
import shutil

from PIL import Image


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOWNLOADS = r"C:\Users\Admin\Downloads"
THEME_IMAGES = os.path.join(ROOT, "ghost-theme", "julia-novaes", "assets", "images")
LOGO_DIR = os.path.join(THEME_IMAGES, "logo")
POSTS_DIR = os.path.join(THEME_IMAGES, "posts")


LOGOS = {
    "logo-official-light-wide.png": "ChatGPT Image May 19, 2026, 12_17_27 PM.png",
    "logo-official-dark-wide.png": "ChatGPT Image May 19, 2026, 12_15_53 PM (3).png",
}

POST_IMAGES = {
    "post-relacao-fim.png": "ChatGPT Image May 19, 2026, 11_47_38 AM (1).png",
    "post-casamentos.png": "ChatGPT Image May 19, 2026, 11_47_39 AM (2).png",
    "post-feliz-sozinho.png": "ChatGPT Image May 19, 2026, 11_47_39 AM (3).png",
    "post-akna.png": "ChatGPT Image May 19, 2026, 11_47_39 AM (4).png",
    "post-engravidar.png": "ChatGPT Image May 19, 2026, 11_47_40 AM (5).png",
    "post-psicoterapia.png": "ChatGPT Image May 19, 2026, 11_47_40 AM (6).png",
}


def copy_assets():
    os.makedirs(LOGO_DIR, exist_ok=True)
    os.makedirs(POSTS_DIR, exist_ok=True)

    for target, source in LOGOS.items():
        shutil.copyfile(os.path.join(DOWNLOADS, source), os.path.join(LOGO_DIR, target))

    for target, source in POST_IMAGES.items():
        shutil.copyfile(os.path.join(DOWNLOADS, source), os.path.join(POSTS_DIR, target))


def trim_and_transparent_logo(source_name, output_name):
    source = os.path.join(LOGO_DIR, source_name)
    output = os.path.join(LOGO_DIR, output_name)
    image = Image.open(source).convert("RGBA")
    pixels = image.load()

    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if r > 242 and g > 242 and b > 242:
                pixels[x, y] = (r, g, b, 0)

    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if bbox:
        image = image.crop(bbox)

    max_width = 680
    if image.width > max_width:
        ratio = max_width / image.width
        image = image.resize((max_width, round(image.height * ratio)), Image.Resampling.LANCZOS)

    image.save(output)


def main():
    copy_assets()
    trim_and_transparent_logo("logo-official-light-wide.png", "logo-header.png")
    print("Official logo and post assets prepared.")


if __name__ == "__main__":
    main()
