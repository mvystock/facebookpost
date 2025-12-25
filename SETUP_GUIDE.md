# Facebook Auto-Poster - Complete Setup Guide

## 🎯 Overview
Automated Facebook posting system with AI-generated content and images. Posts educational financial content every 4 hours with professional AI-generated visuals.

## ✅ Current Status
**System is LIVE and fully operational!**
- ✅ Market volatility analysis
- ✅ Smart content selection (news vs education)
- ✅ AI content generation (Gemini)
- ✅ AI image generation (Gemini)
- ✅ Detailed prompt file creation
- ✅ Email notifications
- ✅ Facebook posting with images
- ✅ Complete archiving system

## 📁 Project Structure
```
/Users/bhrushiravyas/Facbookmv/
├── facebook_poster.py          # Main automation script
├── gemini_image_cli.py         # AI image generator (Gemini API)
├── gemini_video_cli.py         # AI video generator (Veo API)
├── ai_adapter.py               # AI content generation
├── email_notifier.py           # Email notifications
├── market_content.json         # Educational content templates
├── .env                        # Credentials (IMPORTANT!)
├── requirements.txt            # Python dependencies
└── generated_content/
    ├── prompts/                # Detailed AI image/video prompts
    ├── images/                 # AI-generated images (PNG)
    ├── videos/                 # AI-generated videos (MP4)
    └── *.md                    # Archived posts
```

## 🔑 Environment Variables (.env)
```bash
# Facebook API
PAGE_ACCESS_TOKEN="your_facebook_page_access_token_here"
PAGE_ID="283648501839927"
APP_ID="2101533297321283"
APP_SECRET="your_facebook_app_secret_here"

# Google Gemini API
GOOGLE_API_KEY="your_gemini_api_key_here"

# Email (for notifications)
EMAIL_SENDER_EMAIL="your_email@gmail.com"
EMAIL_SENDER_PASSWORD="your_app_password"
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USE_SSL="False"
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd /Users/bhrushiravyas/Facbookmv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Test Run (DRY_RUN mode)
```bash
# Edit facebook_poster.py: Set DRY_RUN = True
python facebook_poster.py --cron
```

### 3. Go Live
```bash
# Edit facebook_poster.py: Set DRY_RUN = False
python facebook_poster.py --cron
```

### 4. Run Scheduled (Every 4 hours)
```bash
# Just run without --cron flag
python facebook_poster.py
# Press Ctrl+C to stop
```

## 🎨 AI Image Generation

### Using Prompt Files (Recommended)
```bash
# Generate image from saved prompt file
python gemini_image_cli.py \
  --prompt-file "generated_content/prompts/PROMPT_20251225_150943_Education.txt" \
  --tone "Professional" \
  --output-dir "generated_content/images"
```

### Using Direct Prompt
```bash
python gemini_image_cli.py \
  --prompt "Bull market running on Wall Street" \
  --tone "Excited" \
  --output-dir "generated_content/images"
```

### Available Tones
- `Professional` - Clean, corporate, business-like
- `Urgent` - Dramatic, red theme, breaking news
- `Excited` - Vibrant, green theme, energetic
- `Sci-Fi` - Cyberpunk, futuristic, neon
- `Casual` - Minimalistic, clean, modern

## 🔄 Complete Workflow

### Automatic Mode (Default)
1. **Market Analysis** - Scans SPY, QQQ, BTC, NVDA, etc.
2. **Content Strategy**:
   - If volatile (>1% move) → Post breaking news
   - If quiet → Post educational content
3. **Prompt Generation** → Saves to `generated_content/prompts/`
4. **Image Generation** → Reads prompt file, generates with Gemini
5. **Content Generation** → AI creates Twitter/LinkedIn/Facebook posts
6. **Email Preview** → Sends notification to your email
7. **Facebook Post** → Posts with AI-generated image
8. **Archive** → Saves everything to `generated_content/`

### Manual Mode
```bash
python facebook_poster.py \
  --title "Market Update" \
  --summary "Stocks rallying today" \
  --tag "Trading" \
  --tone "Excited"
```

## 📊 Market Watchlist
The system monitors these tickers for volatility:
- SPY, QQQ, IWM (Indices)
- BTC-USD, ETH-USD (Crypto)
- NVDA, TSLA, AAPL, AMD, COIN (Stocks)

**Volatility Threshold:** 1.0% daily move

## 📝 Content Templates
Educational topics in `market_content.json`:
- Trading Psychology (FOMO, Discipline)
- Technical Analysis (Support/Resistance, Volume)
- Risk Management (Stop Loss, Position Sizing)
- Chart Patterns (Breakouts, Reversals)

## 🎯 Key Features

### Smart Content Selection
- **Volatile Market** → Breaking news with urgent/excited tone
- **Quiet Market** → Educational content with professional tone

### AI Image Prompts
Detailed prompts include:
- Title and context
- Visual style (professional, clean, corporate)
- Specific elements (charts, graphs, market data)
- Technical specs (8k, cinematic lighting)

### Safety Features
- **DRY_RUN mode** - Test without posting
- **Email previews** - Review before it goes live
- **Complete archiving** - Every post saved with metadata
- **Error handling** - Continues without image if generation fails

## 📧 Email Notifications
Every post triggers an email with:
- Generated content (Twitter, LinkedIn, Facebook)
- Topic and tags
- Tone used
- Image attachment (if generated)

## 🔧 Troubleshooting

### No Image Generated
- Check `GOOGLE_API_KEY` in `.env`
- Verify Gemini API quota
- Check `generated_content/prompts/` for prompt files

### Facebook Post Failed
- Verify `PAGE_ACCESS_TOKEN` is valid
- Check token hasn't expired (60 days)
- Ensure `PAGE_ID` is correct

### Email Not Sent
- Check SMTP credentials in `.env`
- For Gmail, use App Password (not regular password)
- Verify `EMAIL_SENDER_EMAIL` and recipient

## 📈 Recent Successful Posts

### Latest Live Post (2025-12-25 15:09)
- **Topic:** Trading Psychology - FOMO
- **Post ID:** 1758018065044100
- **Image:** GEMINI_IMG_20251225_150950_Create_a_financial_m.png
- **Content:** "Understanding and managing FOMO is crucial for preserving capital..."
- **Status:** ✅ Posted successfully with image

## 🔄 Cron Setup (Optional)
Add to crontab for automatic posting:
```bash
# Post every 4 hours (6am, 10am, 2pm, 6pm, 10pm)
0 6,10,14,18,22 * * * cd /Users/bhrushiravyas/Facbookmv && ./.venv/bin/python facebook_poster.py --cron >> /tmp/fb_poster.log 2>&1
```

## 🎨 Generated Files

### Prompt Files
- Location: `generated_content/prompts/PROMPT_*.txt`
- Format: Detailed multi-line prompts
- Usage: Can be used with any AI image generator

### Images
- Location: `generated_content/images/GEMINI_IMG_*.png`
- Size: ~1.3-1.4 MB each
- Quality: 8k, professional, cinematic

### Archives
- Location: `generated_content/*.md`
- Contains: All platform posts, image path, prompt, metadata

## 🚨 Important Notes

1. **Token Expiry:** Facebook tokens expire after 60 days - renew regularly
2. **API Limits:** Gemini API has rate limits - monitor usage
3. **DRY_RUN:** Always test with `DRY_RUN = True` first
4. **Backups:** Archive folder grows - clean old files periodically

## 📞 Support Resources
- Facebook Graph API: https://developers.facebook.com/docs/graph-api/
- Gemini API: https://ai.google.dev/
- Project Location: `/Users/bhrushiravyas/Facbookmv/`

---

**Last Updated:** 2025-12-25
**Status:** ✅ Production Ready
**Version:** 1.0
