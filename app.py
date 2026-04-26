from flask import Flask, request, render_template, send_file
from PIL import Image, ImageOps
from io import BytesIO
from dotenv import load_dotenv
from rembg import remove
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def process_single_image(input_image_bytes):
    """Remove background, enhance, and return a ready-to-paste passport PIL image."""
    # Step 1: Background removal via local rembg
    try:
        output_bytes = remove(input_image_bytes)
    except Exception as e:
        raise ValueError(f"bg_removal_failed:{str(e)}")

    bg_removed = BytesIO(output_bytes)
    img = Image.open(bg_removed)

    if img.mode in ("RGBA", "LA"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        processed_img = background
    else:
        processed_img = img.convert("RGB")

    return processed_img


@app.route("/process", methods=["POST"])
def process():
    print("==== /process endpoint hit ====")

    # Layout settings
    passport_width = int(request.form.get("width", 390))
    passport_height = int(request.form.get("height", 480))
    border = int(request.form.get("border", 2))
    spacing = int(request.form.get("spacing", 10))
    margin_x = 10
    margin_y = 10
    horizontal_gap = 10
    a4_w, a4_h = 2480, 3508

    # Collect images and their copy counts
    # Supports: image_0, image_1, ... and copies_0, copies_1, ...
    # Also supports legacy single: image + copies
    images_data = []

    # Multi-image mode
    i = 0
    while f"image_{i}" in request.files:
        file = request.files[f"image_{i}"]
        copies = int(request.form.get(f"copies_{i}", 6))
        images_data.append((file.read(), copies))
        i += 1

    # Fallback to single image mode
    if not images_data and "image" in request.files:
        file = request.files["image"]
        copies = int(request.form.get("copies", 6))
        images_data.append((file.read(), copies))

    if not images_data:
        return "No image uploaded", 400

    print(f"DEBUG: Processing {len(images_data)} image(s)")

    # Process all images
    passport_images = []
    for idx, (img_bytes, copies) in enumerate(images_data):
        print(f"DEBUG: Processing image {idx + 1} with {copies} copies")
        try:
            img = process_single_image(img_bytes)
            img = img.resize((passport_width, passport_height), Image.LANCZOS)
            img = ImageOps.expand(img, border=border, fill="black")
            passport_images.append((img, copies))
        except ValueError as e:
            err_str = str(e)
            print(err_str)
            return {"error": err_str}, 500
                

    paste_w = passport_width + 2 * border
    paste_h = passport_height + 2 * border

    # Build all pages
    pages = []
    current_page = Image.new("RGB", (a4_w, a4_h), "white")
    x, y = margin_x, margin_y

    def new_page():
        nonlocal current_page, x, y
        pages.append(current_page)
        current_page = Image.new("RGB", (a4_w, a4_h), "white")
        x, y = margin_x, margin_y

    for passport_img, copies in passport_images:
        for _ in range(copies):
            # Move to next row if needed
            if x + paste_w > a4_w - margin_x:
                x = margin_x
                y += paste_h + spacing

            # Move to next page if needed
            if y + paste_h > a4_h - margin_y:
                new_page()

            current_page.paste(passport_img, (x, y))
            print(f"DEBUG: Placed at x={x}, y={y}")
            x += paste_w + horizontal_gap

    pages.append(current_page)
    print(f"DEBUG: Total pages = {len(pages)}")

    # Export multi-page PDF
    output = BytesIO()
    if len(pages) == 1:
        pages[0].save(output, format="PDF", dpi=(300, 300))
    else:
        pages[0].save(
            output,
            format="PDF",
            dpi=(300, 300),
            save_all=True,
            append_images=pages[1:],
        )
    output.seek(0)
    print("DEBUG: Returning PDF to client")

    return send_file(
        output,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="passport-sheet.pdf",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)