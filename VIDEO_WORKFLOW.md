# Video Generation Workflow

## 🎯 Strategy: Separate Image and Video Generation

**Why This Approach?**
- ✅ **Faster automated posts** - Images generate in 1-2 min vs videos 2-5 min
- ✅ **Cost effective** - Generate videos only when needed
- ✅ **Flexibility** - Choose which images to animate
- ✅ **Quality control** - Review images before creating videos

## 🔄 Complete Workflow

### Step 1: Automated Image + Content (Every 4 hours)
```bash
# This runs automatically
python facebook_poster.py
```

**What it does:**
1. ✅ Analyzes market
2. ✅ Generates detailed prompt → saves to `prompts/`
3. ✅ Generates AI image → saves to `images/`
4. ✅ Generates social content
5. ✅ Posts to Facebook with image
6. ✅ Archives everything

**Time:** ~2 minutes
**Output:** Image + Text post on Facebook

### Step 2: Manual Video Generation (When needed)
```bash
# Run this manually when you want videos
./generate_video.sh
```

**What it does:**
1. 📋 Shows available images and prompts
2. 📋 Asks for aspect ratio (16:9 or 9:16)
3. 🎬 Generates video using latest image + prompt
4. 💾 Saves to `videos/`

**Time:** 2-5 minutes
**Output:** MP4 video file

## 📁 File Organization

```
generated_content/
├── prompts/
│   └── PROMPT_20251225_150943_Education.txt    # Reused for video
├── images/
│   └── GEMINI_IMG_20251225_150950_*.png        # Used as reference
└── videos/
    └── GEMINI_VID_20251225_153000_*.mp4        # Generated separately
```

## 🎨 Using Existing Images for Videos

### Quick Method (Helper Script)
```bash
./generate_video.sh
```
- Interactive prompts
- Uses latest image + prompt automatically
- Choose aspect ratio

### Manual Method (Full Control)
```bash
# List available images
ls -lt generated_content/images/

# List available prompts
ls -lt generated_content/prompts/

# Generate video from specific image + prompt
./.venv/bin/python gemini_video_cli.py \
  --prompt-file "generated_content/prompts/PROMPT_20251225_150943_Education.txt" \
  --image "generated_content/images/GEMINI_IMG_20251225_150950_Create_a_financial_m.png" \
  --aspect-ratio "9:16"
```

## 📐 Aspect Ratio Guide

### 16:9 (Landscape)
**Best for:**
- YouTube
- Facebook feed
- LinkedIn
- Website embeds

**Command:**
```bash
--aspect-ratio "16:9"
```

### 9:16 (Vertical)
**Best for:**
- Instagram Reels
- TikTok
- Facebook Reels
- Mobile-first content

**Command:**
```bash
--aspect-ratio "9:16"
```

## 💡 Recommended Workflow

### Daily Routine
1. **Morning:** Let automated posts run (images only)
2. **Review:** Check `generated_content/images/` for best images
3. **Select:** Choose 1-2 best images from the day
4. **Generate:** Run `./generate_video.sh` for selected images
5. **Post:** Manually post videos to Instagram/TikTok

### Weekly Batch
1. **Let system run** all week (automated images)
2. **Friday:** Review all images from the week
3. **Select top 5-10** best performing/looking images
4. **Batch generate** videos for all selected images
5. **Schedule** videos for next week

## 🎯 Use Cases

### Facebook (Current - Automated)
- **Format:** Image posts
- **Frequency:** Every 4 hours
- **Status:** ✅ LIVE

### Instagram Reels (Manual)
- **Format:** 9:16 videos
- **Source:** Best images from automated posts
- **Frequency:** 1-2 per day (manual)
- **Status:** 🔄 Ready to use

### YouTube Shorts (Manual)
- **Format:** 9:16 videos
- **Source:** Best images from automated posts
- **Frequency:** 2-3 per week (manual)
- **Status:** 🔄 Ready to use

### TikTok (Manual)
- **Format:** 9:16 videos
- **Source:** Best images from automated posts
- **Frequency:** Daily (manual)
- **Status:** 🔄 Ready to use

## 📊 Time & Cost Comparison

### Automated (Images Only)
- **Time:** ~2 min per post
- **Cost:** ~$0.02 per post
- **Frequency:** Every 4 hours (6x/day)
- **Daily Cost:** ~$0.12

### Manual Videos (When Needed)
- **Time:** ~5 min per video
- **Cost:** ~$0.30 per video
- **Frequency:** 1-3 per day
- **Daily Cost:** ~$0.30-0.90

### Total Daily Cost
- **Images (automated):** $0.12
- **Videos (manual):** $0.30-0.90
- **Total:** $0.42-1.02/day

## 🚀 Quick Commands

### Generate video from latest image
```bash
./generate_video.sh
```

### Generate landscape video
```bash
LATEST_IMAGE=$(ls -t generated_content/images/*.png | head -1)
LATEST_PROMPT=$(ls -t generated_content/prompts/*.txt | head -1)

./.venv/bin/python gemini_video_cli.py \
  --prompt-file "$LATEST_PROMPT" \
  --image "$LATEST_IMAGE" \
  --aspect-ratio "16:9"
```

### Generate vertical video (Reels)
```bash
LATEST_IMAGE=$(ls -t generated_content/images/*.png | head -1)
LATEST_PROMPT=$(ls -t generated_content/prompts/*.txt | head -1)

./.venv/bin/python gemini_video_cli.py \
  --prompt-file "$LATEST_PROMPT" \
  --image "$LATEST_IMAGE" \
  --aspect-ratio "9:16"
```

### Batch generate videos for all images
```bash
for img in generated_content/images/*.png; do
    PROMPT=$(ls -t generated_content/prompts/*.txt | head -1)
    ./.venv/bin/python gemini_video_cli.py \
        --prompt-file "$PROMPT" \
        --image "$img" \
        --aspect-ratio "9:16"
    sleep 300  # Wait 5 min between generations
done
```

## 📝 Best Practices

1. **Review before animating** - Not all images make good videos
2. **Match aspect ratio to platform** - 16:9 for YouTube, 9:16 for Reels
3. **Batch generate** - Create multiple videos at once
4. **Reuse prompts** - Same prompt = consistent style
5. **Archive originals** - Keep source images for future use

---

**System:** Hybrid (Automated images + Manual videos)
**Status:** ✅ Optimized for speed and cost
