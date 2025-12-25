#!/bin/bash
# Video Generation Helper Script
# Uses existing images and prompts to generate videos manually

echo "🎬 Facebook Auto-Poster - Video Generator"
echo "=========================================="
echo ""

# Check if we have images and prompts
IMAGE_COUNT=$(ls -1 generated_content/images/*.png 2>/dev/null | wc -l)
PROMPT_COUNT=$(ls -1 generated_content/prompts/*.txt 2>/dev/null | wc -l)

echo "📊 Available Assets:"
echo "   Images: $IMAGE_COUNT"
echo "   Prompts: $PROMPT_COUNT"
echo ""

if [ $IMAGE_COUNT -eq 0 ]; then
    echo "❌ No images found. Run facebook_poster.py first to generate images."
    exit 1
fi

if [ $PROMPT_COUNT -eq 0 ]; then
    echo "❌ No prompts found. Run facebook_poster.py first to generate prompts."
    exit 1
fi

# Show all available images
echo "📁 Available Images:"
echo ""
i=1
declare -a IMAGE_ARRAY
for img in $(ls -t generated_content/images/*.png); do
    IMAGE_ARRAY[$i]=$img
    SIZE=$(ls -lh "$img" | awk '{print $5}')
    DATE=$(ls -l "$img" | awk '{print $6, $7, $8}')
    echo "   $i) $(basename "$img") ($SIZE) - $DATE"
    i=$((i+1))
done
echo ""

# Ask user to select an image
read -p "Select image number (1-$IMAGE_COUNT) or press Enter for latest: " IMAGE_CHOICE

if [ -z "$IMAGE_CHOICE" ]; then
    SELECTED_IMAGE=$(ls -t generated_content/images/*.png | head -1)
    echo "✅ Using latest image: $(basename "$SELECTED_IMAGE")"
elif [ "$IMAGE_CHOICE" -ge 1 ] && [ "$IMAGE_CHOICE" -le $IMAGE_COUNT ]; then
    SELECTED_IMAGE="${IMAGE_ARRAY[$IMAGE_CHOICE]}"
    echo "✅ Selected: $(basename "$SELECTED_IMAGE")"
else
    echo "❌ Invalid choice. Using latest image."
    SELECTED_IMAGE=$(ls -t generated_content/images/*.png | head -1)
fi

echo ""

# Show all available prompts
echo "📝 Available Prompts:"
echo ""
i=1
declare -a PROMPT_ARRAY
for prompt in $(ls -t generated_content/prompts/*.txt); do
    PROMPT_ARRAY[$i]=$prompt
    FIRST_LINE=$(head -1 "$prompt")
    echo "   $i) $(basename "$prompt")"
    echo "      ${FIRST_LINE:0:60}..."
    i=$((i+1))
done
echo ""

# Ask user to select a prompt
read -p "Select prompt number (1-$PROMPT_COUNT) or press Enter for latest: " PROMPT_CHOICE

if [ -z "$PROMPT_CHOICE" ]; then
    SELECTED_PROMPT=$(ls -t generated_content/prompts/*.txt | head -1)
    echo "✅ Using latest prompt: $(basename "$SELECTED_PROMPT")"
elif [ "$PROMPT_CHOICE" -ge 1 ] && [ "$PROMPT_CHOICE" -le $PROMPT_COUNT ]; then
    SELECTED_PROMPT="${PROMPT_ARRAY[$PROMPT_CHOICE]}"
    echo "✅ Selected: $(basename "$SELECTED_PROMPT")"
else
    echo "❌ Invalid choice. Using latest prompt."
    SELECTED_PROMPT=$(ls -t generated_content/prompts/*.txt | head -1)
fi

echo ""

# Ask user for aspect ratio
echo "📐 Select aspect ratio:"
echo "   1) 16:9 (Landscape - YouTube, Facebook, LinkedIn)"
echo "   2) 9:16 (Vertical - Instagram Reels, TikTok, Facebook Reels)"
echo ""
read -p "Enter choice (1 or 2): " ASPECT_CHOICE

if [ "$ASPECT_CHOICE" = "1" ]; then
    ASPECT_RATIO="16:9"
    echo "✅ Selected: 16:9 (Landscape)"
elif [ "$ASPECT_CHOICE" = "2" ]; then
    ASPECT_RATIO="9:16"
    echo "✅ Selected: 9:16 (Vertical)"
else
    echo "❌ Invalid choice. Defaulting to 16:9"
    ASPECT_RATIO="16:9"
fi

echo ""
echo "🚀 Generating video from prompt..."
echo "   Selected Image: $(basename "$SELECTED_IMAGE")"
echo "   Selected Prompt: $(basename "$SELECTED_PROMPT")"
echo "   Aspect Ratio: $ASPECT_RATIO"
echo "   This will take 2-5 minutes..."
echo ""

# Generate video (without image reference - not supported in current API)
./.venv/bin/python gemini_video_cli.py \
    --prompt-file "$SELECTED_PROMPT" \
    --aspect-ratio "$ASPECT_RATIO"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Video generation complete!"
    echo ""
    echo "📁 Check generated_content/videos/ for your video"
    ls -lh generated_content/videos/*.mp4 | tail -1
else
    echo ""
    echo "❌ Video generation failed. Check the error above."
    exit 1
fi
