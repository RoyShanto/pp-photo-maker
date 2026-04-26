import base64
from flask import Flask, request, render_template, send_file, jsonify
from PIL import Image, ImageOps
from io import BytesIO
from rembg import remove
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def process_single_image(input_image_bytes):
    """Remove background, enhance, and return a ready-to-paste passport PIL image."""
    img = Image.open(BytesIO(input_image_bytes))
    
    # Limit max dimension to 1000px to prevent OOM errors during alpha_matting
    img.thumbnail((1000, 1000), Image.LANCZOS)

    # Step 1: Background removal via local rembg
    try:
        img = remove(img, post_process_mask=True, alpha_matting=True)
    except Exception as e:
        raise ValueError(f"bg_removal_failed:{str(e)}")

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

    try:
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
        images_data = []
        i = 0
        while f"image_{i}" in request.files:
            file = request.files[f"image_{i}"]
            copies = int(request.form.get(f"copies_{i}", 6))
            images_data.append((file.read(), copies))
            i += 1

        if not images_data and "image" in request.files:
            file = request.files["image"]
            copies = int(request.form.get("copies", 6))
            images_data.append((file.read(), copies))

        if not images_data:
            return "No image uploaded", 400

        passport_images = []
        for idx, (img_bytes, copies) in enumerate(images_data):
            img = process_single_image(img_bytes)
            img = ImageOps.fit(img, (passport_width, passport_height), method=Image.LANCZOS)
            img = ImageOps.expand(img, border=border, fill="black")
            passport_images.append((img, copies))

        paste_w = passport_width + 2 * border
        paste_h = passport_height + 2 * border

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
                if x + paste_w > a4_w - margin_x:
                    x = margin_x
                    y += paste_h + spacing
                if y + paste_h > a4_h - margin_y:
                    new_page()
                current_page.paste(passport_img, (x, y))
                x += paste_w + horizontal_gap

        pages.append(current_page)

        output = BytesIO()
        if len(pages) == 1:
            pages[0].save(output, format="PDF", resolution=300.0, quality=100)
        else:
            pages[0].save(
                output,
                format="PDF",
                resolution=300.0,
                quality=100,
                save_all=True,
                append_images=pages[1:],
            )
        output.seek(0)
        pdf_b64 = base64.b64encode(output.getvalue()).decode('utf-8')

        images_b64 = []
        for p_img, copies in passport_images:
            img_io = BytesIO()
            p_img.save(img_io, format="PNG")
            img_io.seek(0)
            images_b64.append(base64.b64encode(img_io.getvalue()).decode('utf-8'))

        return jsonify({
            "pdf": pdf_b64,
            "images": images_b64
        })
    except Exception as e:
        import traceback
        err_str = traceback.format_exc()
        print("ERROR IN PROCESS TOPLEVEL:\n", err_str)
        return {"error": str(e), "traceback": err_str}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)