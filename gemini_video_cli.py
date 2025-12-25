#!/usr/bin/env python3
"""
CLI tool for generating videos using Google Gemini Veo API.

Usage:
    python3 gemini_video_cli.py --prompt "Bull market running wild on wall street"
    python3 gemini_video_cli.py --prompt-file "generated_content/prompts/PROMPT_*.txt"
    python3 gemini_video_cli.py --prompt "Market analysis" --image "path/to/image.png"
"""

import argparse
import sys
import os
import time
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def generate_gemini_video(prompt, image_path=None, output_dir="generated_content/videos", output_filename=None, aspect_ratio="16:9"):
    """
    Generate a video using Google Gemini Veo API.
    
    Args:
        prompt: Text description of the video
        image_path: Optional path to an image to base the video on
        output_dir: Output directory for videos
        output_filename: Custom output filename
        aspect_ratio: "16:9" or "9:16"
        
    Returns:
        Path to generated video file or None on failure
    """
    try:
        # Get API key from environment
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("❌ Error: GOOGLE_API_KEY not found in .env file")
            print("   Please add: GOOGLE_API_KEY=your_key_here")
            return None
        
        # Setup client
        print("🔗 Connecting to Google Gemini Veo API...")
        client = genai.Client(api_key=api_key)
        
        print(f"🎬 Generating video with prompt: '{prompt[:100]}...'")
        if image_path:
            print(f"🖼️  Using reference image: {image_path}")
        print(f"📐 Aspect ratio: {aspect_ratio}")
        
        # Prepare generation config
        config = types.GenerateVideosConfig(
            aspect_ratio=aspect_ratio
        )
        
        # Start the generation operation
        if image_path and os.path.exists(image_path):
            # Upload the image first
            print("📤 Uploading reference image...")
            from google.genai.types import UploadFileConfig
            with open(image_path, 'rb') as f:
                uploaded_file = client.files.upload(
                    file=f,
                    config=UploadFileConfig(mime_type="image/png")
                )
            print(f"✅ Image uploaded: {uploaded_file.name}")
            
            # Generate video with image reference
            operation = client.models.generate_videos(
                model="veo-3.1-generate-preview",
                prompt=prompt,
                image_file=uploaded_file,
                config=config
            )
        else:
            # Generate video from prompt only
            operation = client.models.generate_videos(
                model="veo-3.1-generate-preview",
                prompt=prompt,
                config=config
            )
        
        # Poll the operation until it's finished
        print("⏳ Video generation in progress...")
        print("   This may take several minutes (typically 2-5 minutes)")
        
        poll_count = 0
        while not operation.done:
            poll_count += 1
            elapsed = poll_count * 10
            print(f"   ⏱️  Waiting... ({elapsed}s elapsed)")
            time.sleep(10)
            operation = client.operations.get(operation)
        
        # Handle the result and download
        if operation.result:
            generated_video = operation.result.generated_videos[0]
            
            # Create output directory
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            if output_filename:
                filename = output_filename
            else:
                from datetime import datetime
                safe_title = "".join([c for c in prompt[:20] if c.isalnum() or c in (' ', '-', '_')]).strip().replace(' ', '_')
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"GEMINI_VID_{timestamp}_{safe_title}.mp4"
            
            full_path = output_path / filename
            
            
            print(f"📥 Downloading video to {full_path}...")
            
            # Download the video content
            video_content = client.files.download(file=generated_video.video)
            
            # Write to file
            with open(full_path, 'wb') as f:
                f.write(video_content)
            
            print(f"✅ Video successfully generated!")
            print(f"📁 Saved to: {full_path}")
            
            # Get file size
            file_size = os.path.getsize(full_path) / (1024 * 1024)  # MB
            print(f"📊 File size: {file_size:.2f} MB")
            
            return str(full_path)
        else:
            print("❌ Video generation failed or was blocked by safety filters.")
            if hasattr(operation, 'error'):
                print(f"   Error details: {operation.error}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate AI videos using Google Gemini Veo API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 gemini_video_cli.py --prompt "Bull market on Wall Street"
  python3 gemini_video_cli.py --prompt-file "prompts/PROMPT_*.txt"
  python3 gemini_video_cli.py --prompt "Market rally" --image "chart.png" --aspect-ratio "9:16"
  
Note: Requires GOOGLE_API_KEY in .env file
Video generation typically takes 2-5 minutes
        """
    )
    
    parser.add_argument(
        '--prompt',
        type=str,
        required=False,
        help='The text prompt describing the video you want to generate'
    )
    
    parser.add_argument(
        '--prompt-file',
        type=str,
        required=False,
        help='Path to a text file containing the prompt (alternative to --prompt)'
    )
    
    parser.add_argument(
        '--image',
        type=str,
        default=None,
        help='Path to an image to use as reference for the video'
    )
    
    parser.add_argument(
        '--aspect-ratio',
        type=str,
        default='16:9',
        choices=['16:9', '9:16'],
        help='Video aspect ratio (default: 16:9 for landscape, 9:16 for vertical/mobile)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Custom output filename (default: auto-generated in generated_content/videos/)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='generated_content/videos',
        help='Output directory for generated videos (default: generated_content/videos)'
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
    
    # Validate image path if provided
    if args.image and not os.path.exists(args.image):
        print(f"❌ Error: Image file not found: {args.image}")
        return 1
    
    # Generate the video
    video_path = generate_gemini_video(
        prompt=prompt,
        image_path=args.image,
        output_dir=args.output_dir,
        output_filename=args.output,
        aspect_ratio=args.aspect_ratio
    )
    
    if video_path:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
