# Video Generation - Quick Guide

## 🎬 Interactive Video Generator

### Run the Helper Script
```bash
./generate_video.sh
```

### What It Does
1. **Shows all available images** with size and date
2. **Shows all available prompts** with preview
3. **Lets you choose** which image/prompt to use
4. **Asks for aspect ratio** (16:9 or 9:16)
5. **Generates video** in 2-5 minutes

### Example Session
```
📁 Available Images:
   1) GEMINI_IMG_20251225_150950_*.png (1.3M) - Dec 25 15:09
   2) GEMINI_IMG_20251225_150847_*.png (1.3M) - Dec 25 15:08
   3) GEMINI_IMG_20251225_150714_*.png (1.4M) - Dec 25 15:07
   4) GEMINI_IMG_20251225_150532_*.png (1.3M) - Dec 25 15:05

Select image number (1-4) or press Enter for latest: 4

📝 Available Prompts:
   1) PROMPT_20251225_150943_Education.txt
      Create a financial market image: Trading Psychology...
   2) PROMPT_20251225_150839_Education.txt
      Create a financial market image: Technical Analysis...

Select prompt number (1-2) or press Enter for latest: 2

📐 Select aspect ratio:
   1) 16:9 (Landscape)
   2) 9:16 (Vertical)

Enter choice (1 or 2): 2

✅ Generating video...
```

## 📋 Quick Commands

### Use Latest (Default)
```bash
# Just press Enter for all prompts
./generate_video.sh
```

### Select Specific Image
```bash
# When prompted, enter the image number (e.g., "3")
./generate_video.sh
```

### Command Line (Advanced)
```bash
# Generate from specific prompt
./.venv/bin/python gemini_video_cli.py \
  --prompt-file "generated_content/prompts/PROMPT_20251225_150328_Education.txt" \
  --aspect-ratio "9:16"
```

## 📁 File Organization

### Images (4 available)
```
generated_content/images/
├── GEMINI_IMG_20251225_150950_*.png (1.3M) ← Latest
├── GEMINI_IMG_20251225_150847_*.png (1.3M)
├── GEMINI_IMG_20251225_150714_*.png (1.4M)
└── GEMINI_IMG_20251225_150532_*.png (1.3M) ← Oldest
```

### Prompts (3 available)
```
generated_content/prompts/
├── PROMPT_20251225_150943_Education.txt ← Latest (FOMO)
├── PROMPT_20251225_150839_Education.txt (Support/Resistance)
└── PROMPT_20251225_150328_Education.txt (FOMO)
```

### Videos (Generated)
```
generated_content/videos/
├── GEMINI_VID_20251225_153225_*.mp4 (2.5M, 16:9)
└── GEMINI_VID_20251225_152552_*.mp4 (2.2M, 9:16)
```

## 🎯 Use Cases

### Create Reel from Older Image
1. Run `./generate_video.sh`
2. Select image #4 (oldest, unused)
3. Select matching prompt
4. Choose 9:16 (vertical)
5. Post to Instagram Reels

### Create YouTube Video
1. Run `./generate_video.sh`
2. Select best performing image
3. Select matching prompt
4. Choose 16:9 (landscape)
5. Upload to YouTube

### Batch Create Videos
```bash
# Create videos for all unused images
for i in 1 2 3 4; do
    echo -e "$i\n\n2" | ./generate_video.sh
    sleep 300  # Wait 5 min between generations
done
```

## ⏱️ Generation Time
- **Average:** 2-5 minutes
- **Fastest:** 70 seconds (observed)
- **Slowest:** 5 minutes (typical max)

## 💰 Cost
- **Per video:** ~$0.30
- **Daily budget (3 videos):** ~$0.90
- **Weekly budget (10 videos):** ~$3.00

## ✅ Best Practices

1. **Review images first** - Pick the best ones
2. **Match prompts** - Use the prompt that created the image
3. **Choose platform** - 16:9 for YouTube, 9:16 for Reels
4. **Generate in batches** - Create multiple at once
5. **Test both ratios** - Same content, different formats

---

**Tool:** `./generate_video.sh`
**Status:** ✅ Ready to use
**Features:** Interactive selection, all images available
