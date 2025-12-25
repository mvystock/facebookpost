# Gemini Video CLI - Quick Reference

## 🎬 Video Generation Commands

### Generate from Prompt
```bash
./.venv/bin/python gemini_video_cli.py \
  --prompt "Bull market running on Wall Street with charts" \
  --aspect-ratio "16:9"
```

### Generate from Prompt File
```bash
./.venv/bin/python gemini_video_cli.py \
  --prompt-file "generated_content/prompts/PROMPT_*.txt" \
  --aspect-ratio "16:9"
```

### Generate with Reference Image
```bash
./.venv/bin/python gemini_video_cli.py \
  --prompt "Animated financial chart showing market trends" \
  --image "generated_content/images/GEMINI_IMG_*.png" \
  --aspect-ratio "16:9"
```

### Generate Vertical Video (Mobile/Reels)
```bash
./.venv/bin/python gemini_video_cli.py \
  --prompt "Stock market analysis for social media" \
  --aspect-ratio "9:16"
```

## 📐 Aspect Ratios
- `16:9` - Landscape (YouTube, Facebook, LinkedIn)
- `9:16` - Vertical (Instagram Reels, TikTok, Facebook Reels)

## ⏱️ Generation Time
- Typical: 2-5 minutes
- The script polls every 10 seconds
- Progress is shown in real-time

## 📁 Output Location
Default: `generated_content/videos/`

Files are named: `GEMINI_VID_YYYYMMDD_HHMMSS_[prompt].mp4`

## 🎨 Video Prompts

### Good Prompts
✅ "Cinematic view of stock market charts with rising trends"
✅ "Professional financial data visualization with graphs and numbers"
✅ "Trading floor atmosphere with market data displays"

### Tips
- Be specific about visual style
- Mention "professional", "cinematic", "corporate" for business content
- Include "charts", "graphs", "data" for financial videos
- Specify camera movement if needed ("zoom in", "pan across")

## 🔗 Integration with Existing Workflow

### Use Latest Generated Image
```bash
# Get latest image
IMAGE=$(ls -t generated_content/images/*.png | head -1)

# Generate video from it
./.venv/bin/python gemini_video_cli.py \
  --prompt "Animate this financial chart with smooth transitions" \
  --image "$IMAGE"
```

### Use Latest Prompt File
```bash
# Get latest prompt
PROMPT=$(ls -t generated_content/prompts/*.txt | head -1)

# Generate video
./.venv/bin/python gemini_video_cli.py \
  --prompt-file "$PROMPT" \
  --aspect-ratio "9:16"
```

## 📊 File Sizes
- Typical video: 5-15 MB
- Duration: ~5 seconds (Veo default)
- Format: MP4
- Quality: High (8K capable)

## 🚨 Troubleshooting

### API Key Error
```
❌ Error: GOOGLE_API_KEY not found
```
**Fix:** Add `GOOGLE_API_KEY` to `.env` file

### Generation Failed
```
❌ Video generation failed or was blocked
```
**Possible causes:**
- Safety filters triggered
- Prompt violates content policy
- API quota exceeded

### Image Upload Failed
```
❌ Error: Image file not found
```
**Fix:** Check image path is correct and file exists

## 📝 Example Workflow

### 1. Generate Image
```bash
./.venv/bin/python gemini_image_cli.py \
  --prompt "Trading psychology FOMO concept" \
  --tone "Professional"
```

### 2. Generate Video from Image
```bash
./.venv/bin/python gemini_video_cli.py \
  --prompt "Animate this trading concept with smooth camera movement" \
  --image "generated_content/images/GEMINI_IMG_*.png" \
  --aspect-ratio "9:16"
```

### 3. Use for Social Media
- 16:9 for YouTube, Facebook, LinkedIn
- 9:16 for Instagram Reels, TikTok, Facebook Reels

## 🎯 Best Practices

1. **Start with images** - Generate image first, then animate it
2. **Use prompt files** - Reuse detailed prompts for consistency
3. **Test aspect ratios** - Generate both 16:9 and 9:16 versions
4. **Be patient** - Video generation takes 2-5 minutes
5. **Check safety** - Avoid sensitive content that might be filtered

---

**Location:** `/Users/bhrushiravyas/Facbookmv/gemini_video_cli.py`
**Output:** `/Users/bhrushiravyas/Facbookmv/generated_content/videos/`
