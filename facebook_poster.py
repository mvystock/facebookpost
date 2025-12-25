import argparse
import random
import os
import requests
import json
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

import ai_adapter
import yfinance as yf
from email_notifier import send_email_notification
from gemini_image_cli import generate_gemini_image
# from ai_image_generator import generate_ai_image  # Archived - using Gemini API now


# Load environment variables
load_dotenv()

# Facebook Page Access Token (from Graph API Explorer)
# Ensure this is set in your .env file
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")

# App configuration
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

# Create directories for prompts and images
PROMPT_DIR = Path("generated_content/prompts")
IMAGE_DIR = Path("generated_content/images")
PROMPT_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# Safety Switch: Set to False to enable posting
DRY_RUN = False

def analyze_market_health(tickers):
    """
    Scans the watchlist to find the most significant market mover.
    Returns: (ticker, change_percent, current_price)
    """
    best_ticker = None
    max_change = -1.0
    stats = {}

    print("🔍 Analyzing Market Context (Volatility Scan)...")
    
    # Efficiently fetch data for all tickers
    # Using Tickers object to avoid multiple HTTP sessions if possible, 
    # though iterating .tickers is still sequential in yfinance wrappers.
    try:
        data = yf.Tickers(" ".join(tickers))
        
        for t_symbol in tickers:
            try:
                # fast_info is faster than .history()
                info = data.tickers[t_symbol].fast_info
                last_price = info.last_price
                prev_close = info.previous_close
                
                if prev_close and prev_close > 0:
                    change_pct = abs((last_price - prev_close) / prev_close) * 100
                    
                    # Debug log
                    # print(f"  {t_symbol}: {change_pct:.2f}%")
                    
                    if change_pct > max_change:
                        max_change = change_pct
                        best_ticker = t_symbol
                        stats = {
                            "symbol": t_symbol,
                            "change_pct": change_pct,
                            "price": last_price,
                            "raw_change": (last_price - prev_close) / prev_close
                        }
            except Exception:
                continue
                
    except Exception as e:
        print(f"⚠️ Market scan warning: {e}")

    return stats

def get_trending_stock_news():
    """
    Smart Content Selector.
    - If Market is Volatile (>1% move): POST LIVE NEWS (Urgent/Excited)
    - If Market is Flat: POST EDUCATIONAL CONTENT (Professional/Casual)
    """
    tickers = ["SPY", "QQQ", "IWM", "BTC-USD", "ETH-USD", "NVDA", "TSLA", "AAPL", "AMD", "COIN"]
    
    # 1. Get Context
    market_stats = analyze_market_health(tickers)
    
    selected_tag = ["Trading"]
    tone = "Professional"
    news_data = {}
    
    # Threshold for "Significant Move" (e.g., 1.0%)
    VOLATILITY_THRESHOLD = 1.0 
    
    is_volatile = market_stats.get("change_pct", 0) > VOLATILITY_THRESHOLD
    target_ticker = market_stats.get("symbol", "SPY")
    
    if is_volatile:
        # --- HIGH VOLATILITY STRATEGY (Live News) ---
        direction = "UP" if market_stats.get("raw_change", 0) > 0 else "DOWN"
        print(f"🔥 HOT TICKER: {target_ticker} is moving {direction} ({market_stats['change_pct']:.2f}%)")
        
        # Set Contextual Tone
        if direction == "UP":
            tone = "Excited: The market is rallying! Write a high-energy update."
        else:
            tone = "Urgent: The market is dropping! Write a cautionary, high-stakes update."
            
        print(f"🎭 Context Tone: {tone}")
        
        # Fetch News for THIS ticker
        # Fetch News for THIS ticker
        try:
            stock = yf.Ticker(target_ticker)
            news_items = stock.news
            if news_items:
                story = news_items[0] # Top story is most relevant for hot mover
                content = story.get('content', {})
                title = content.get('title', f"Huge Move in {target_ticker}")
                summary = content.get('summary', f"{target_ticker} is seeing major volatility today.")
                link = content.get('canonicalUrl', {}).get('url', "")
                
                # Generate detailed image prompt and save to file
                image_prompt, prompt_file = create_image_prompt(
                    news_title=title,
                    news_summary=summary,
                    tone=tone.split(':')[0],  # Extract just the tone name
                    ticker=target_ticker
                )
                print(f"💾 Detailed prompt saved to: {prompt_file}")
                
                return {
                    "title": f"🚨 {title}",
                    "summary": summary,
                    "url": link,
                    "trending_tags": [target_ticker, "MarketAlert"],
                    "image_path": None,
                    "image_prompt": image_prompt,
                    "prompt_file": prompt_file,
                    "tone": tone
                }
        except Exception as e:
            print(f"⚠️ News fetch failed: {e}")
            
    # --- LOW VOLATILITY / FALLBACK STRATEGY (Educational) ---
    print(f"😴 Market is Quiet ({market_stats.get('change_pct', 0):.2f}%). Synthesizing Educational Content.")
    
    tone = "Professional: Write a project update in a formal, corporate tone."
    # Occasionally be casual
    if random.random() < 0.3:
        tone = "Casual: Write a project update in a laid-back, conversational tone."

    try:
        with open("market_content.json", "r") as f:
            templates = json.load(f).get("templates", [])
            if templates:
                selected = random.choice(templates)
                
                # Generate detailed image prompt and save to file
                image_prompt, prompt_file = create_image_prompt(
                    news_title=selected['title'],
                    news_summary=selected.get('summary', selected.get('description', selected.get('core_idea', 'Educational content'))),
                    tone=tone.split(':')[0],  # Extract just the tone name (e.g., "Professional")
                    ticker="Education"
                )
                print(f"💾 Detailed prompt saved to: {prompt_file}")

                return {
                    "title": selected['title'],
                    "summary": selected.get('summary', selected.get('description', selected.get('core_idea', 'Content'))),
                    "url": "",
                    "trending_tags": ["Investing", "Education"],
                    "image_path": None,
                    "image_prompt": image_prompt,
                    "prompt_file": prompt_file,
                    "tone": tone
                }
    except Exception:
        pass

    return {
        "title": "Market Watch",
        "summary": "Staying patient in a flat market.",
        "url": "",
        "trending_tags": ["Trading"],
        "image_path": None,
        "tone": tone
    }

def create_post_message(news):
    """
    Format the post message with news, tags, and disclaimer (Fallback/Manual)
    """
    message = f"""📈 {news['title']}

{news['summary']}

Read more: {news['url']}

{' '.join(['#' + tag for tag in news['trending_tags']])}

⚠️ DISCLAIMER: This content is for educational purposes only. Not financial advice. Always do your own research before making investment decisions.
"""
    return message

def create_image_prompt(news_title, news_summary, tone, ticker="Market"):
    """
    Create an AI image prompt from news data and save it to a file.
    
    Args:
        news_title: The news headline
        news_summary: Brief summary of the news
        tone: The tone/style for the image
        ticker: Stock ticker symbol
        
    Returns:
        tuple: (prompt_text, prompt_file_path)
    """
    # Build context-aware prompt
    tone_styles = {
        'Professional': 'professional, clean, corporate, business-like',
        'Urgent': 'dramatic, urgent, breaking news, high impact, red theme',
        'Excited': 'energetic, vibrant, bullish, green theme, upward momentum',
        'Sci-Fi': 'futuristic, cyberpunk, neon, high-tech, digital',
        'Casual': 'friendly, approachable, modern, minimalist'
    }
    
    style = tone_styles.get(tone, tone_styles['Professional'])
    
    # Create detailed prompt
    prompt = f"""Create a financial market image: {news_title}

Context: {news_summary}

Style: {style}, stock market themed, {ticker} focus, highly detailed, 8k resolution, cinematic lighting

Visual elements: charts, graphs, market data, trading floor atmosphere, professional financial imagery"""
    
    # Save prompt to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_ticker = "".join([c for c in ticker if c.isalnum()])
    filename = f"PROMPT_{timestamp}_{safe_ticker}.txt"
    prompt_file = PROMPT_DIR / filename
    
    prompt_file.write_text(prompt, encoding='utf-8')
    print(f"💾 Image prompt saved to: {prompt_file}")
    
    return prompt, str(prompt_file)

def save_generated_content(x_post, li_post, fb_post, news_title, tag="N/A", image_path=None, image_prompt="N/A"):
    """
    Save the generated content and future AI prompts to a file.
    """
    try:
        output_dir = Path("generated_content")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_title = "".join([c for c in news_title if c.isalnum() or c in (' ', '-', '_')]).strip().replace(' ', '_')
        filename = output_dir / f"{timestamp}_{safe_title}.md"
        
        image_info = f"Image Path: {image_path}" if image_path else "Image Path: N/A"
        prompt_info = f"Future AI Image Prompt: {image_prompt}"
        
        content = f"""# Generated Content - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Source: {news_title}
Tag Used: {tag}
{image_info}
{prompt_info}

## X (Twitter) Post
{x_post}

## LinkedIn Post
{li_post}

## Facebook Post
{fb_post}
"""
        filename.write_text(content, encoding='utf-8')
        print(f"💾 Content saved to: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving content: {e}")
        return False

def post_to_facebook_page(message, image_path=None):
    """
    Post the message (and optional image) to your Facebook page.
    """
    if not PAGE_ACCESS_TOKEN or not PAGE_ID:
         print("❌ Error: Missing PAGE_ACCESS_TOKEN or PAGE_ID in .env file")
         return False

    try:
        if image_path and os.path.exists(image_path):
            print(f"📸 Posting with image: {image_path}")
            url = f"https://graph.facebook.com/v24.0/{PAGE_ID}/photos"
            
            payload = {
                'caption': message,
                'access_token': PAGE_ACCESS_TOKEN
            }
            
            with open(image_path, 'rb') as img_file:
                files = {
                    'source': img_file
                }
                response = requests.post(url, data=payload, files=files)
        else:
            print("📝 Posting text only (no image found or provided).")
            url = f"https://graph.facebook.com/v24.0/{PAGE_ID}/feed"
            payload = {
                'message': message,
                'access_token': PAGE_ACCESS_TOKEN
            }
            response = requests.post(url, data=payload)

        result = response.json()
        
        if 'id' in result:
            print(f"✅ Successfully posted to Facebook!")
            print(f"Post ID: {result.get('id', result.get('post_id'))}")
            return True
        else:
            print(f"❌ Error posting to Facebook: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Exception occurred during posting: {str(e)}")
        return False

def get_long_lived_token(short_lived_token):
    """
    Exchange short-lived token for long-lived token (lasts 60 days)
    """
    url = "https://graph.facebook.com/v24.0/oauth/access_token"
    
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': APP_ID,
        'client_secret': APP_SECRET,
        'fb_exchange_token': short_lived_token
    }
    
    response = requests.get(url, params=params)
    return response.json().get('access_token')

def main():
    """
    Main function to fetch news and post to Facebook
    Supports Manual Mode via CLI arguments.
    """
    # Parse Command Line Arguments
    parser = argparse.ArgumentParser(description="Facebook Auto Poster")
    parser.add_argument("--title", help="Manual post title")
    parser.add_argument("--summary", help="Manual post summary")
    parser.add_argument("--tag", help="Manual hashtag (single)")
    parser.add_argument("--cron", action="store_true", help="Run once and exit (for Cron usage)")
    parser.add_argument("--tone", help="Tone for the post/image (e.g., 'Urgent', 'Excited')")
    parser.add_argument("--skip-fb", action="store_true", help="Skip posting to Facebook (generate image and email only)")
    args, unknown = parser.parse_known_args()

    print("🚀 Starting Trending News Poster...")
    
    if args.title and args.summary:
        print("🛠️  MANUAL MODE ACTIVATED")
        selected_tag = [args.tag] if args.tag else ["Update"]
        
        # Determine Tone
        manual_tone = args.tone if args.tone else "Professional"
        
        # Step 2: Create AI image prompt and save to file
        ticker = args.tag if args.tag else "Market"
        image_prompt, prompt_file = create_image_prompt(
            news_title=args.title,
            news_summary=args.summary,
            tone=manual_tone,
            ticker=ticker
        )
        
        # Step 3: Generate image using Gemini
        print(f"🎨 Generating AI image with Gemini...")
        image_path = generate_gemini_image(
            prompt=image_prompt,
            tone=manual_tone,
            output_dir=str(IMAGE_DIR)
        )
        
        if image_path:
            print(f"✅ Image generated: {image_path}")
        else:
            print(f"⚠️  Image generation failed, continuing without image")
        
        news = {
            "title": args.title,
            "summary": args.summary,
            "url": "",
            "trending_tags": selected_tag,
            "image_path": image_path,
            "image_prompt": image_prompt,
            "tone": manual_tone
        }
    else:
        # Automatic Smart Mode
        print("🧠 SMART MODE ACTIVATED")
        news = get_trending_stock_news()
    
    print(f"📰 News/Topic: {news['title']}")
    print(f"🏷️  Selected Tag: {news['trending_tags'][0]}")
    
    # Tone is now determined by the Context Engine (or default for manual)
    selected_tone = news.get('tone', "Professional")
    print(f"🎭 Selected Tone: {selected_tone.split(':')[0]}")
    
    # Generate image if we have a prompt file (from automatic mode)
    if 'prompt_file' in news and news['prompt_file']:
        print(f"🎨 Generating AI image from prompt file...")
        try:
            # Read the prompt from the file
            with open(news['prompt_file'], 'r', encoding='utf-8') as f:
                image_prompt = f.read().strip()
            
            # Generate image using the prompt file content
            image_path = generate_gemini_image(
                prompt=image_prompt,
                tone=selected_tone.split(':')[0],  # Extract just the tone name
                output_dir=str(IMAGE_DIR)
            )
            
            if image_path:
                print(f"✅ Image generated: {image_path}")
                news['image_path'] = image_path
            else:
                print(f"⚠️  Image generation failed, continuing without image")
                news['image_path'] = None
        except Exception as e:
            print(f"⚠️  Image generation error: {e}")
            news['image_path'] = None
    elif not news.get('image_path'):
        # No image path and no prompt file
        news['image_path'] = None

    # 1. Attempt AI Generation
    print("🤖 Generating content with AI...")
    ai_result = ai_adapter.summarize_social_media_with_ai([news], news['trending_tags'], tone=selected_tone)
    
    message = ""
    
    if ai_result:
        x_post, li_post, fb_post = ai_result
        print("✅ AI Content Generated Successfully!")
        
        # Archive it
        image_path = news.get('image_path')
        image_prompt = news.get('image_prompt', 'N/A')
        save_generated_content(x_post, li_post, fb_post, news['title'], news['trending_tags'][0], image_path, image_prompt)
        
        # SEND EMAIL NOTIFICATION
        email_subject = f"🚀 New Post Generated: {news['title']}"
        email_body = f"""
New social media content has been generated!

📰 Source: {news['title']}
🏷️ Tag: {news['trending_tags'][0]}
🎭 Tone: {selected_tone}

Twitter:
{x_post}

LinkedIn:
{li_post}

Facebook:
{fb_post}
        """
        send_email_notification(email_subject, email_body, image_path)
        
        # Use Facebook content
        message = fb_post
        
        # Explicitly append trending hashtags to ensure they are present
        tags_line = ' '.join(['#' + t for t in news['trending_tags']])
        message += f"\n\n{tags_line}"
        
        # Append disclaimer manually if not present (AI might omit it)
        if "DISCLAIMER" not in message:
             message += "\n\n⚠️ DISCLAIMER: Educational purposes only. Not financial advice."
    else:
        print("⚠️ AI Generation failed. Fallback to manual template.")
        # Create formatted post message manually
        message = create_post_message(news)
    
    print(f"\n📝 Post message:\n{message}\n")
    
    # Post to Facebook page
    if DRY_RUN:
        print("🚧 DRY RUN MODE: Skipping actual post to Facebook.")
        print("✅ Message generation and archiving successful (No post made).")
        success = True
    else:
        image_path = news.get('image_path')
        success = post_to_facebook_page(message, image_path=image_path)
    
    if success:
        print("✅ Process completed successfully!")
    else:
        print("❌ Process failed")
    
    # At the end of main(), return the cron flag
    return args.cron

if __name__ == "__main__":
    # APScheduler setup
    scheduler = BlockingScheduler()

    # Post every 4 hours
    @scheduler.scheduled_job('interval', hours=4)
    def scheduled_post():
        main()

    # Run once immediately
    is_cron_mode = main()
    
    if is_cron_mode:
        print("⏱️  Cron Mode: Exiting after single run.")
    else:
        print("🕒 Scheduler started. Will post every 4 hours.")
        print("👉 Press Ctrl+C to exit.")
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            print("Stopped scheduler.")
