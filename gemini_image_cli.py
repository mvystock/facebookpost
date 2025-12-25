#!/usr/bin/env python3
"""
CLI tool for generating images using Google Gemini API.

Usage:
    python3 gemini_image_cli.py --prompt "Bull market running wild on wall street" --tone "Excited"
    python3 gemini_image_cli.py --prompt "Risk management strategy" --output my_chart.png
"""

import argparse
import sys
import os
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def generate_gemini_image(prompt, tone="Professional", output_dir="generated_content", output_filename=None):
    """
    Generate an image using Google Gemini API.
    
    Args:
        prompt: Text description of the image
        tone: Visual style/tone
        output_dir: Output directory
        output_filename: Custom output filename
        
    Returns:
        Path to generated image file or None on failure
    """
    try:
        # Get API key from environment
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("❌ Error: GOOGLE_API_KEY not found in .env file")
            print("   Please add: GOOGLE_API_KEY=your_key_here")
            return None
        
        # Setup client
        print("🔗 Connecting to Google Gemini API...")
        client = genai.Client(api_key=api_key)
        
        # Enhance prompt based on tone
        style_modifiers = {
            'Professional': 'highly detailed, professional, 8k resolution, cinematic lighting, corporate style',
            'Urgent': 'dramatic, red theme, intense, breaking news style, high contrast',
            'Excited': 'vibrant, green theme, upward trending, energetic, neon colors',
            'Sci-Fi': 'cyberpunk, futuristic, neon lights, digital art, high-tech',
            'Casual': 'minimalistic, clean, soft lighting, modern illustration'
        }
        
        style = style_modifiers.get(tone, style_modifiers['Professional'])
        enhanced_prompt = f"{prompt}, {style}"
        
        print(f"🎨 Generating image with prompt: '{prompt}'")
        print(f"🎭 Style: {tone}")
        
        # Request image generation using Gemini 2.5 Flash Image
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[enhanced_prompt],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"]
            )
        )
        
        # Process and save the output
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        image_saved = False
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                # Convert binary data to an image object
                image_bytes = BytesIO(part.inline_data.data)
                img = Image.open(image_bytes)
                
                # Generate filename
                if output_filename:
                    filename = output_filename
                else:
                    safe_title = "".join([c for c in prompt[:20] if c.isalnum() or c in (' ', '-', '_')]).strip().replace(' ', '_')
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"GEMINI_IMG_{timestamp}_{safe_title}.png"
                
                full_path = output_path / filename
                
                # Save to disk
                img.save(full_path)
                print(f"✅ Image successfully generated!")
                print(f"📁 Saved to: {full_path}")
                image_saved = True
                return str(full_path)
        
        if not image_saved:
            print("❌ No image data received from API")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate AI images using Google Gemini API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 gemini_image_cli.py --prompt "Bull market on Wall Street" --tone "Excited"
  python3 gemini_image_cli.py --prompt "Technical analysis chart" --output my_chart.png
  
Note: Requires GOOGLE_API_KEY in .env file
        """
    )
    
    parser.add_argument(
        '--prompt',
        type=str,
        required=False,
        help='The text prompt describing the image you want to generate'
    )
    
    parser.add_argument(
        '--prompt-file',
        type=str,
        required=False,
        help='Path to a text file containing the prompt (alternative to --prompt)'
    )
    
    parser.add_argument(
        '--tone',
        type=str,
        default='Professional',
        choices=['Professional', 'Urgent', 'Excited', 'Sci-Fi', 'Casual'],
        help='The visual tone/style for the image (default: Professional)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Custom output filename (default: auto-generated in generated_content/)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='generated_content',
        help='Output directory for generated images (default: generated_content)'
    )
    
    args = parser.parse_args()
    
    # Validate that either --prompt or --prompt-file is provided
    if not args.prompt and not args.prompt_file:
        parser.error("Either --prompt or --prompt-file must be specified")
        return 1
    
    if args.prompt and args.prompt_file:
        parser.error("Cannot specify both --prompt and --prompt-file")
        return 1
    
    # Read prompt from file if specified
    if args.prompt_file:
        try:
            with open(args.prompt_file, 'r', encoding='utf-8') as f:
                prompt = f.read().strip()
            print(f"📄 Reading prompt from: {args.prompt_file}")
        except FileNotFoundError:
            print(f"❌ Error: Prompt file not found: {args.prompt_file}")
            return 1
        except Exception as e:
            print(f"❌ Error reading prompt file: {e}")
            return 1
    else:
        prompt = args.prompt
    
    # Generate the image
    image_path = generate_gemini_image(
        prompt=prompt,
        tone=args.tone,
        output_dir=args.output_dir,
        output_filename=args.output
    )
    
    if image_path:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
