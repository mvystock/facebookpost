# Facebook Auto-Poster - AI-Powered System

## 🤖 100% AI-Generated Content

This system uses **Google Gemini AI** for everything:
- ✅ **Images** - Gemini 2.5 Flash Image (8K, professional)
- ✅ **Videos** - Veo 3.1 (cinematic, 5-second clips)
- ✅ **Text Content** - AI-written social media posts
- ✅ **Prompts** - Detailed, context-aware prompts

## 🎯 What Makes This Different

### Old Approach (Removed)
- ❌ Simple GIF animations
- ❌ Template-based images
- ❌ Limited customization

### New AI-Powered Approach
- ✅ **Gemini-generated images** - Unique every time
- ✅ **Veo-generated videos** - Professional quality
- ✅ **Smart prompts** - Saved and reusable
- ✅ **Context-aware** - Adapts to market conditions

## 📊 AI Workflow

```
Market Analysis
    ↓
AI Prompt Generation (detailed, context-rich)
    ↓
┌─────────────────┬─────────────────┐
│                 │                 │
AI Image          AI Video          AI Text
(Gemini)          (Veo)             (Gemini)
    ↓                 ↓                 ↓
PNG (1.3MB)       MP4 (5-15MB)      Social Posts
    └─────────────────┴─────────────────┘
                      ↓
            Facebook Post (with media)
                      ↓
            Complete Archive (.md)
```

## 🎨 AI Tools

### 1. Gemini Image CLI
```bash
# Generate from text
python gemini_image_cli.py --prompt "Trading concept" --tone "Professional"

# Generate from detailed prompt file
python gemini_image_cli.py --prompt-file "prompts/PROMPT_*.txt"
```

**Output:**
- Format: PNG
- Size: ~1.3-1.4 MB
- Quality: 8K resolution
- Style: Professional, cinematic lighting

### 2. Veo Video CLI
```bash
# Generate from text
python gemini_video_cli.py --prompt "Animated chart" --aspect-ratio "16:9"

# Generate from prompt file with image reference
python gemini_video_cli.py \
  --prompt-file "prompts/PROMPT_*.txt" \
  --image "images/GEMINI_IMG_*.png" \
  --aspect-ratio "9:16"
```

**Output:**
- Format: MP4
- Size: ~5-15 MB
- Duration: ~5 seconds
- Quality: High (8K capable)
- Aspect Ratios: 16:9 (landscape) or 9:16 (vertical)

### 3. AI Content Generator
Integrated into `facebook_poster.py`:
- Analyzes market volatility
- Selects appropriate tone
- Generates platform-specific content (Twitter, LinkedIn, Facebook)
- Adds relevant hashtags and disclaimers

## 🔄 Automated AI Pipeline

### Smart Content Selection
```python
if market_volatility > 1%:
    # Breaking news with urgent/excited tone
    tone = "Urgent" or "Excited"
    content_type = "Market Alert"
else:
    # Educational content with professional tone
    tone = "Professional"
    content_type = "Educational"
```

### Prompt Generation
Every post creates a detailed prompt file:
```
Create a financial market image: [TITLE]

Context: [DETAILED EXPLANATION]

Style: professional, clean, corporate, business-like, 
       stock market themed, highly detailed, 8k resolution, 
       cinematic lighting

Visual elements: charts, graphs, market data, 
                 trading floor atmosphere
```

### Media Generation
1. **Image** - Generated from prompt file (1-2 min)
2. **Video** - Generated from same prompt + image reference (2-5 min)
3. **Both** - Attached to Facebook post

## 📈 Quality Metrics

### Images
- **Resolution:** 8K capable
- **Style:** Professional, corporate
- **Consistency:** High (same prompt = similar style)
- **Uniqueness:** Every image is unique

### Videos
- **Model:** Veo 3.1 (latest)
- **Quality:** Cinematic
- **Movement:** Smooth camera work
- **Duration:** ~5 seconds (perfect for social media)

### Content
- **Tone Accuracy:** Matches market conditions
- **Platform Optimization:** Custom for each platform
- **Compliance:** Auto-includes disclaimers

## 🎯 Use Cases

### Daily Educational Posts (Current)
- **Frequency:** Every 4 hours
- **Media:** AI-generated images
- **Platform:** Facebook
- **Status:** ✅ LIVE

### Social Media Reels (Ready)
- **Format:** 9:16 vertical videos
- **Media:** AI-generated videos
- **Platforms:** Instagram, Facebook Reels, TikTok
- **Status:** 🔄 Tools ready, not automated yet

### YouTube Content (Ready)
- **Format:** 16:9 landscape videos
- **Media:** AI-generated videos
- **Platform:** YouTube
- **Status:** 🔄 Tools ready, manual upload

## 🔧 Technical Stack

### AI Models
- **Gemini 2.5 Flash Image** - Image generation
- **Veo 3.1** - Video generation
- **Gemini Pro** - Text content generation

### APIs
- **Google Gemini API** - All AI generation
- **Facebook Graph API** - Social media posting
- **Yahoo Finance API** - Market data

### Languages & Frameworks
- **Python 3.13**
- **PIL/Pillow** - Image processing
- **APScheduler** - Task scheduling
- **python-dotenv** - Configuration

## 📊 Performance

### Generation Times
- **Prompt Creation:** Instant
- **Image Generation:** 1-2 minutes
- **Video Generation:** 2-5 minutes
- **Content Generation:** 5-10 seconds
- **Total (Image + Content):** ~2 minutes
- **Total (Video + Content):** ~5 minutes

### Costs (Approximate)
- **Images:** ~$0.01-0.05 per image
- **Videos:** ~$0.10-0.50 per video
- **Content:** Minimal (text generation)

## 🚀 Future Enhancements

### Planned
- [ ] Automated video posting to Facebook
- [ ] Multi-platform posting (Instagram, YouTube)
- [ ] A/B testing different AI styles
- [ ] Performance analytics integration

### Possible
- [ ] Voice-over generation for videos
- [ ] Multi-language content
- [ ] Custom AI model fine-tuning
- [ ] Real-time market reaction videos

## 📝 Key Files

| File | Purpose | AI Model |
|------|---------|----------|
| `gemini_image_cli.py` | Image generation | Gemini 2.5 Flash Image |
| `gemini_video_cli.py` | Video generation | Veo 3.1 |
| `ai_adapter.py` | Content generation | Gemini Pro |
| `facebook_poster.py` | Orchestration | All of the above |

## 🎓 Learning Resources

- **Gemini API Docs:** https://ai.google.dev/
- **Veo Documentation:** https://ai.google.dev/gemini-api/docs/veo
- **Facebook Graph API:** https://developers.facebook.com/docs/graph-api/

---

**System Status:** 🟢 Production (Images) + 🔄 Testing (Videos)
**Last Updated:** 2025-12-25
**AI-Powered:** 100%
