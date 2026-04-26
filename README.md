# 📸 Passport Photo Pro

A web-based tool to generate print-ready passport photo sheets from uploaded images. Supports multiple photos, per-photo copy counts, 100% free and offline AI background removal, and multi-page high-resolution PDF export — all on an A4 layout at 300 DPI.

---

## 🚀 Features

- **100% Free & Local AI** — Uses the local `rembg` library for background removal. No API keys, no internet connection required, and no usage limits!
- **Multi-photo upload** — drag & drop or click to upload one or more photos at once.
- **Download Individual Photos** — easily download the cleanly processed (background-removed) photos alongside the PDF.
- **Per-photo copy count** — set how many copies of each photo you need (1–54).
- **In-browser cropper** — crop each photo to the correct passport aspect ratio before processing.
- **A4 print layout** — photos are automatically arranged in a grid at 300 DPI for high-quality printing.
- **Multi-page PDF** — if photos exceed one A4 page, additional pages are created automatically.
- **Advanced options** — customize photo width, height, spacing, and border size.
- **Feedback system** — built-in bug report form powered by EmailJS.

---

## 🧰 Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Frontend  | HTML, Tailwind CSS, Vanilla JS    |
| Cropping  | Cropper.js                        |
| Backend   | Python, Flask                     |
| Image AI  | `rembg` (Local Machine Learning)  |
| PDF gen   | Pillow (PIL)                      |

---

## 🛠️ One-Click Installation (Windows)

We've made it incredibly easy to install and run the project on Windows without touching the command line!

1. **Download or Clone the project** to your computer.
2. Double-click the **`setup.bat`** file. This will automatically create a virtual environment and download all the necessary AI libraries (this may take a few minutes depending on your internet speed).
3. Once setup is complete, double-click **`run.bat`**. This will start the server and automatically open the application in your web browser!

---

## 🛠️ Manual Installation (Mac / Linux / Windows CLI)

If you prefer using the terminal, ensure you have Python 3.8+ installed, then run the following commands:

```bash
# 1. Clone the repository
git clone https://github.com/RoyShanto/pp-photo-maker.git
cd pp-photo-maker

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies (Includes ONNX runtime for AI)
pip install -r requirements.txt

# 5. Run the app
python app.py
```
The server will start at `http://localhost:5000`.

---

## 📁 Project Structure

```text
passport-photo-pro/
├── app.py                  # Flask backend — AI processing & PDF generation
├── requirements.txt        # Python dependencies
├── setup.bat               # 1-Click Windows Setup Script
├── run.bat                 # 1-Click Windows Run Script
├── templates/
│   └── index.html          # Frontend UI
└── README.md
```

---

## 🖼️ How It Works

### Upload
- Drag and drop one or more photos onto the upload zone, or click to browse.
- Each photo appears as a card with a thumbnail.

### Crop (Recommended)
- Click **Crop** on any photo card to open the cropper tool.
- Adjust the crop area and click **Crop & Save**. The image is kept at maximum resolution to ensure pristine print quality.

### Generate & Download
- Click **Generate Sheet**.
- The backend processes each photo locally using neural networks to cleanly cut out the background.
- It generates a high-quality 300 DPI PDF preview.
- You can now click **Download PDF** to get your printable sheet, or **Download Photo** to save the transparent PNGs!

---

## 📄 License

MIT License. See `LICENSE` for details.
