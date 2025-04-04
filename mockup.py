
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

# Load the thumbnail image
thumb = Image.open("thumbnail.jpg").convert("RGB")
thumb = thumb.resize((1328, 747), Image.Resampling.LANCZOS)

# Create a rounded mask for the thumbnail
mask = Image.new("L", thumb.size, 0)
draw_mask = ImageDraw.Draw(mask)
draw_mask.rounded_rectangle([(0, 0), thumb.size], radius=50, fill=255)
thumb.putalpha(mask)

# Create base canvas
canvas = Image.new("RGBA", (1500, 1000), (0, 0, 0, 255))
canvas.paste(thumb, (86, 60), thumb)

# Load fonts
font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
font_channel = ImageFont.truetype("DejaVuSans.ttf", 45)
font_subs = ImageFont.truetype("DejaVuSans.ttf", 45)

# Draw title
draw = ImageDraw.Draw(canvas)
title = "Hide and Seek In Real Life!"
draw.text((66, 835), title, font=font_title, fill="white")

# Channel info box
box_x, box_y = 86, 910
box_width, box_height = 1328, 100
draw.rounded_rectangle(
    [(box_x, box_y), (box_x + box_width, box_y + box_height)],
    radius=50,
    fill=(24, 24, 24)
)

# Load and paste local channel image
pfp = Image.open("pfp.jpg").convert("RGB").resize((87, 87), Image.Resampling.LANCZOS)
mask = Image.new("L", (87, 87), 0)
ImageDraw.Draw(mask).ellipse((0, 0, 87, 87), fill=255)
canvas.paste(pfp, (box_x + 15, box_y + 6), mask)

# Draw channel name and sub count
channel_name = "MrBeast"
subscriber_count = "382.00M"

if subscriber_count.endswith(".00M"):
    subscriber_count = subscriber_count.replace(".00M", "M")

draw.text((box_x + 120, box_y + 25), channel_name, font=font_channel, fill="white")

# Align sub count text to the right inside the box
subs_text = f"{subscriber_count} subscribers"
subs_text_width = draw.textlength(subs_text, font=font_subs)
subs_x = box_x + box_width - subs_text_width - 20
draw.text((subs_x, box_y + 25), subs_text, font=font_subs, fill="gray")

# Save output
canvas.convert("RGB").save("final_mockup.jpg")
print("✅ Mockup generated and saved as final_mockup.jpg")
