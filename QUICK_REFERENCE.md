# Facebook Auto-Poster - Quick Reference

## 🚀 Common Commands

### Run Once (Test)
```bash
cd /Users/bhrushiravyas/Facbookmv
./.venv/bin/python facebook_poster.py --cron
```

### Run Scheduled (Every 4 hours)
```bash
./.venv/bin/python facebook_poster.py
# Press Ctrl+C to stop
```

### Generate Image from Prompt File
```bash
./.venv/bin/python gemini_image_cli.py \
  --prompt-file "generated_content/prompts/PROMPT_*.txt" \
  --tone "Professional"
```

### Manual Post
```bash
./.venv/bin/python facebook_poster.py \
  --title "Your Title" \
  --summary "Your summary" \
  --tag "Trading"
```

## ⚙️ Toggle Live/Test Mode

### Enable DRY_RUN (Test Mode)
Edit `facebook_poster.py` line 39:
```python
DRY_RUN = True  # No actual Facebook posts
```

### Disable DRY_RUN (Live Mode)
```python
DRY_RUN = False  # Posts to Facebook
```

## 📁 Important Files

| File | Purpose |
|------|---------|
| `facebook_poster.py` | Main script |
| `gemini_image_cli.py` | Image generator |
| `.env` | Credentials |
| `market_content.json` | Content templates |
| `generated_content/prompts/` | AI prompts |
| `generated_content/images/` | Generated images |

## 🔑 Quick Checks

### Check if tokens are valid
```bash
# View current .env
cat .env | grep PAGE_ACCESS_TOKEN
```

### View recent posts
```bash
ls -lt generated_content/*.md | head -5
```

### View generated images
```bash
ls -lh generated_content/images/
```

### View prompt files
```bash
ls -lt generated_content/prompts/
cat generated_content/prompts/PROMPT_*.txt | head -20
```

## 🎨 Image Tones
- `Professional` - Default, clean, corporate
- `Urgent` - Red theme, dramatic
- `Excited` - Green theme, energetic
- `Sci-Fi` - Cyberpunk, futuristic
- `Casual` - Minimalistic, modern

## 📊 System Status Check
```bash
# Check if virtual env is active
which python  # Should show .venv path

# Check dependencies
pip list | grep -E "requests|apscheduler|google-genai"

# Test Gemini API
./.venv/bin/python gemini_image_cli.py --prompt "Test" --tone "Professional"
```

## 🔄 Restart from Scratch
```bash
cd /Users/bhrushiravyas/Facbookmv
source .venv/bin/activate
pip install -r requirements.txt
python facebook_poster.py --cron
```

## 📧 Email Test
Check if email notifications work:
```bash
# Run a test post and check your email
python facebook_poster.py --cron
# Email should arrive at: mayur.vyas@gmail.com
```

## 🚨 Emergency Stop
If scheduler is running:
```bash
# Press Ctrl+C
# Or find and kill the process:
ps aux | grep facebook_poster
kill <PID>
```

## 📈 Latest Success
- **Date:** 2025-12-25 15:09
- **Post ID:** 1758018065044100
- **Topic:** Trading Psychology - FOMO
- **Image:** ✅ Generated and posted
- **Status:** ✅ Live on Facebook

---
**Quick Access:** `/Users/bhrushiravyas/Facbookmv/`
