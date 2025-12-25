# AI Media Generation CLI Tools

This directory contains command-line tools for generating images and videos using local AI engines.

## 📸 Image Generation

### Usage
```bash
# Basic usage
python3 generate_image_cli.py --prompt "Bull market running wild on wall street" --tone "Excited"

# With custom output
python3 generate_image_cli.py --prompt "Risk management strategy" --tone "Professional" --output my_chart.png

# Using virtual environment
.venv/bin/python3 generate_image_cli.py --prompt "Technical analysis" --tone "Sci-Fi"
```

### Available Tones
- `Professional` - Clean, corporate style
- `Urgent` - Dramatic, red theme, intense
- `Excited` - Vibrant, green theme, energetic
- `Sci-Fi` - Cyberpunk, futuristic, neon
- `Casual` - Minimalistic, clean, modern

### Options
- `--prompt` (required): Text description of the image
- `--tone`: Visual style (default: Professional)
- `--output`: Custom filename
- `--output-dir`: Output directory (default: generated_content)

---

## 🎬 Video Generation

### Usage
```bash
# Basic usage
python3 generate_video_cli.py --prompt "Market volatility animation" --duration 5

# With custom settings
python3 generate_video_cli.py --prompt "Risk management strategy" --fps 30 --duration 10 --output market.mp4
```

### Options
- `--prompt` (required): Text description of the video
- `--tone`: Visual style (default: Professional)
- `--duration`: Video length in seconds (default: 5)
- `--fps`: Frames per second - 24, 30, or 60 (default: 24)
- `--output`: Custom filename
- `--output-dir`: Output directory (default: generated_content)

### Note
Video generation requires additional models to be installed. See the script output for setup instructions.

---

## 🔧 Technical Details

### Image Generation
- **Model**: Stable Diffusion v1.5
- **Device**: Automatically uses MPS (Apple Silicon) or CUDA if available
- **Precision**: float32 for stability on Mac
- **Safety**: Safety checker disabled for financial/market imagery

### Video Generation (Placeholder)
- **Recommended Models**: 
  - Stable Video Diffusion (SVD)
  - AnimateDiff
  - Custom fine-tuned models
- **Setup Required**: Install additional dependencies and models

---

## 📝 Integration with Facebook Poster

The image prompts are automatically saved in the `generated_content/*.md` files under the field:
```
Future AI Image Prompt: Topic: [title], Tone: [tone]
```

You can extract these prompts and use them with the CLI tools:
```bash
# Example workflow
PROMPT=$(grep "Future AI Image Prompt" generated_content/latest.md | cut -d: -f2-)
python3 generate_image_cli.py --prompt "$PROMPT"
```

---

## 🚀 Quick Start

1. **Generate an image**:
   ```bash
   .venv/bin/python3 generate_image_cli.py --prompt "Golden cross pattern on stock chart" --tone "Professional"
   ```

2. **Check the output**:
   ```bash
   ls -lh generated_content/AI_IMG_*.png
   ```

3. **Use in your workflow**:
   - Images are saved in `generated_content/`
   - Use them for social media posts
   - Integrate with the Facebook poster

---

## 📦 Dependencies

Already installed in your `.venv`:
- `torch`
- `diffusers`
- `transformers`
- `accelerate`
- `pillow`

For video generation, you may need:
```bash
pip install opencv-python imageio
```
