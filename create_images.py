from PIL import Image, ImageDraw, ImageFont
import os, json, argparse

WIDTH, HEIGHT = 1080, 1350
BLUE = "#255CFF"
DEEP_BLUE = "#1238A8"
YELLOW = "#FFD84D"
CREAM = "#FFF8E7"
DARK = "#182033"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#DCE7FF"
BRAND = "Milywan Education"
HANDLE = "@milywan_education"

def load_font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def draw_centered_text(draw, text, y, font, fill, max_width, line_spacing=12):
    lines = wrap_text(draw, text, font, max_width)
    cy = y
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=font)
        w = bbox[2]-bbox[0]
        h = bbox[3]-bbox[1]
        draw.text(((WIDTH-w)/2, cy), line, font=font, fill=fill)
        cy += h + line_spacing

def draw_footer(draw, slide_num, light=False):
    footer_font = load_font(28, bold=False)
    small_font = load_font(24, bold=False)
    color = WHITE if light else DEEP_BLUE
    draw.text((70, HEIGHT-95), BRAND, font=footer_font, fill=color)
    page = f"{slide_num}/5"
    bbox = draw.textbbox((0, 0), page, font=small_font)
    draw.rounded_rectangle((WIDTH-145, HEIGHT-108, WIDTH-70, HEIGHT-63), radius=18, fill=LIGHT_BLUE)
    draw.text((WIDTH-107-(bbox[2]-bbox[0])/2, HEIGHT-96), page, font=small_font, fill=DEEP_BLUE)

def background(draw, variant=0):
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=CREAM)
    draw.ellipse((-160, -120, 330, 370), fill=YELLOW)
    draw.ellipse((820, 1040, 1220, 1440), fill=LIGHT_BLUE)
    draw.rounded_rectangle((70, 80, WIDTH-70, HEIGHT-150), radius=46, fill=WHITE)
    if variant % 2 == 0:
        draw.ellipse((850, 110, 930, 190), fill=YELLOW)
        draw.ellipse((130, 1040, 190, 1100), fill=LIGHT_BLUE)
    else:
        draw.ellipse((140, 145, 205, 210), fill=LIGHT_BLUE)
        draw.ellipse((830, 975, 920, 1065), fill=YELLOW)

def save_jpg(img, out_path):
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(out_path, format="JPEG", quality=92, optimize=True)

def draw_cover(post, out_path):
    img = Image.new("RGB", (WIDTH, HEIGHT), CREAM)
    draw = ImageDraw.Draw(img)
    background(draw, 0)
    label_font = load_font(32, bold=True)
    title_font = load_font(82, bold=True)
    sub_font = load_font(42, bold=False)
    draw.rounded_rectangle((130, 170, 430, 225), radius=24, fill=BLUE)
    draw.text((165, 184), "FRENCH B2", font=label_font, fill=WHITE)
    draw_centered_text(draw, post["slides"][0]["title"], 390, title_font, DARK, 850, line_spacing=20)
    draw_centered_text(draw, post["slides"][0].get("subtitle", ""), 790, sub_font, DEEP_BLUE, 790, line_spacing=12)
    draw.rounded_rectangle((250, 960, WIDTH-250, 1045), radius=35, fill=YELLOW)
    cta_font = load_font(34, bold=True)
    cta = "Save this carousel"
    bbox = draw.textbbox((0,0), cta, font=cta_font)
    draw.text(((WIDTH-(bbox[2]-bbox[0]))/2, 982), cta, font=cta_font, fill=DARK)
    draw_footer(draw, 1)
    save_jpg(img, out_path)

def draw_info(post, slide, slide_num, out_path):
    img = Image.new("RGB", (WIDTH, HEIGHT), CREAM)
    draw = ImageDraw.Draw(img)
    background(draw, slide_num)
    num_font = load_font(54, bold=True)
    title_font = load_font(58, bold=True)
    body_font = load_font(48, bold=False)
    draw.rounded_rectangle((135, 180, 255, 300), radius=36, fill=BLUE)
    label = str(slide_num-1)
    bbox = draw.textbbox((0,0), label, font=num_font)
    draw.text((195-(bbox[2]-bbox[0])/2, 204), label, font=num_font, fill=WHITE)
    title = slide.get("title", "").replace("1.", "").replace("2.", "").replace("3.", "").strip() or post["topic"]
    draw_centered_text(draw, title, 380, title_font, DARK, 820, line_spacing=16)
    body = slide.get("body", "")
    draw.rounded_rectangle((145, 650, WIDTH-145, 975), radius=36, fill=LIGHT_BLUE)
    draw_centered_text(draw, body, 725, body_font, DARK, 740, line_spacing=18)
    draw_footer(draw, slide_num)
    save_jpg(img, out_path)

def draw_cta(post, slide, out_path):
    img = Image.new("RGB", (WIDTH, HEIGHT), BLUE)
    draw = ImageDraw.Draw(img)
    draw.ellipse((-130, -90, 330, 370), fill=YELLOW)
    draw.ellipse((780, 980, 1200, 1400), fill=DEEP_BLUE)
    draw.rounded_rectangle((90, 120, WIDTH-90, HEIGHT-145), radius=52, fill=WHITE)
    title_font = load_font(76, bold=True)
    body_font = load_font(46, bold=False)
    handle_font = load_font(42, bold=True)
    draw_centered_text(draw, slide.get("title", "Want more?"), 330, title_font, DARK, 820, line_spacing=18)
    draw_centered_text(draw, slide.get("body", ""), 610, body_font, DEEP_BLUE, 790, line_spacing=18)
    draw.rounded_rectangle((205, 940, WIDTH-205, 1040), radius=42, fill=YELLOW)
    bbox = draw.textbbox((0,0), HANDLE, font=handle_font)
    draw.text(((WIDTH-(bbox[2]-bbox[0]))/2, 965), HANDLE, font=handle_font, fill=DARK)
    draw_footer(draw, 5, light=True)
    save_jpg(img, out_path)

def generate_post(post, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    slides = post["slides"]
    draw_cover(post, os.path.join(output_dir, "slide_1.jpg"))
    draw_info(post, slides[1], 2, os.path.join(output_dir, "slide_2.jpg"))
    draw_info(post, slides[2], 3, os.path.join(output_dir, "slide_3.jpg"))
    draw_info(post, slides[3], 4, os.path.join(output_dir, "slide_4.jpg"))
    draw_cta(post, slides[4], os.path.join(output_dir, "slide_5.jpg"))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--posts", default="posts.json")
    parser.add_argument("--post-id", default="day_01")
    parser.add_argument("--output", default="posts")
    args = parser.parse_args()
    with open(args.posts, "r", encoding="utf-8") as f:
        posts = json.load(f)
    post = next((p for p in posts if p["id"] == args.post_id), None)
    if not post:
        raise ValueError(f"Post id not found: {args.post_id}")
    generate_post(post, os.path.join(args.output, args.post_id))
    print(f"Generated JPG carousel images for {args.post_id}")

if __name__ == "__main__":
    main()
